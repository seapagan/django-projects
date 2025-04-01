"""Tests for the IPAdminRestrictMiddleware."""

from collections.abc import Callable

import pytest
from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from django.test import override_settings
from pytest_mock import MockerFixture

from app.middleware import IPAdminRestrictMiddleware


@pytest.fixture
def mock_get_response() -> Callable[[HttpRequest], HttpResponse]:
    """Fixture to mock the get_response callable."""
    return lambda _request: HttpResponse("OK")


@pytest.fixture
def middleware(
    mock_get_response: Callable[[HttpRequest], HttpResponse],
) -> IPAdminRestrictMiddleware:
    """Fixture to create an instance of the middleware."""
    return IPAdminRestrictMiddleware(mock_get_response)


@pytest.fixture
def request_factory() -> HttpRequest:
    """Fixture to create a basic HttpRequest object."""
    request = HttpRequest()
    request.META = {"REMOTE_ADDR": "127.0.0.1"}
    return request


@override_settings(ADMIN_URL="secret-admin/", ADMIN_IPS_ALLOWED=["127.0.0.1"])
def test_non_admin_path_allowed(
    middleware: IPAdminRestrictMiddleware,
    request_factory: HttpRequest,
    mocker: MockerFixture,
) -> None:
    """Test that non-admin paths are always allowed."""
    mock_get_ip = mocker.patch("app.middleware.get_client_ip")
    request_factory.path = "/some/other/path/"
    response = middleware(request_factory)
    assert response.status_code == 200
    assert response.content == b"OK"
    # Should not check IP for non-admin paths
    mock_get_ip.assert_not_called()


@override_settings(ADMIN_URL="secret-admin/", ADMIN_IPS_ALLOWED=["127.0.0.1"])
def test_admin_path_allowed_ip(
    middleware: IPAdminRestrictMiddleware,
    request_factory: HttpRequest,
    mocker: MockerFixture,
) -> None:
    """Test that admin paths are allowed for IPs in ADMIN_IPS_ALLOWED."""
    allowed_ip = "127.0.0.1"
    mock_get_ip = mocker.patch(
        "app.middleware.get_client_ip", return_value=(allowed_ip, True)
    )
    request_factory.path = f"/{settings.ADMIN_URL}"
    response = middleware(request_factory)
    assert response.status_code == 200
    assert response.content == b"OK"
    mock_get_ip.assert_called_once_with(request_factory)


@override_settings(ADMIN_URL="secret-admin/", ADMIN_IPS_ALLOWED=["127.0.0.1"])
def test_admin_path_disallowed_ip(
    middleware: IPAdminRestrictMiddleware,
    request_factory: HttpRequest,
    mocker: MockerFixture,
) -> None:
    """Test that admin paths raise Http404 for disallowed IPs."""
    disallowed_ip = "192.168.1.100"
    mock_get_ip = mocker.patch(
        "app.middleware.get_client_ip", return_value=(disallowed_ip, True)
    )
    request_factory.path = f"/{settings.ADMIN_URL}some/sub/path/"
    with pytest.raises(Http404):
        middleware(request_factory)
    mock_get_ip.assert_called_once_with(request_factory)


@override_settings(ADMIN_URL="secret-admin/", ADMIN_IPS_ALLOWED=["127.0.0.1"])
def test_middleware_calls_get_response(
    middleware: IPAdminRestrictMiddleware,
    request_factory: HttpRequest,
    mocker: MockerFixture,
) -> None:
    """Test that get_response is called when access is permitted."""
    mock_get_response_callable = mocker.Mock(
        return_value=HttpResponse("Passed")
    )
    middleware_instance = IPAdminRestrictMiddleware(mock_get_response_callable)

    # Test non-admin path
    request_factory.path = "/non-admin/"
    response = middleware_instance(request_factory)
    assert response.content == b"Passed"
    mock_get_response_callable.assert_called_once_with(request_factory)
    mock_get_response_callable.reset_mock()

    # Test allowed admin path
    allowed_ip = "127.0.0.1"
    mocker.patch(
        "app.middleware.get_client_ip", return_value=(allowed_ip, True)
    )
    request_factory.path = f"/{settings.ADMIN_URL}"
    response = middleware_instance(request_factory)
    assert response.content == b"Passed"
    mock_get_response_callable.assert_called_once_with(request_factory)
