"""Tests for JavaScript context processor."""

from django.http import HttpRequest
from pytest_mock import MockerFixture

from app.context_processors import add_correct_javascript


def test_add_correct_javascript_debug_true(mocker: MockerFixture) -> None:
    """Test JavaScript context processor when DEBUG is True."""
    mocker.patch("app.context_processors.settings.DEBUG", True)
    request = HttpRequest()

    context = add_correct_javascript(request)

    assert context == {"js_file": "js/site.js"}


def test_add_correct_javascript_debug_false(mocker: MockerFixture) -> None:
    """Test JavaScript context processor when DEBUG is False."""
    mocker.patch("app.context_processors.settings.DEBUG", False)
    request = HttpRequest()

    context = add_correct_javascript(request)

    assert context == {"js_file": "js/site.min.js"}
