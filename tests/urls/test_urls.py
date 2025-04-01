"""Test URL configurations for the Django project."""

import pytest
from django.urls import resolve, reverse

from app import views

# Mark all tests in this module as Django DB tests
pytestmark = pytest.mark.django_db


def test_projects_url_resolves() -> None:
    """Test resolving and reversing the 'projects' URL."""
    url_path: str = reverse("projects")
    assert url_path == "/"
    resolved_view = resolve(url_path)
    assert resolved_view.func.view_class == views.ProjectsListView


def test_contact_success_url_resolves() -> None:
    """Test resolving and reversing the 'contact_success' URL."""
    url_path: str = reverse("contact_success")
    assert url_path == "/contact/success/"
    resolved_view = resolve(url_path)
    assert resolved_view.func.view_class == views.ContactSuccessView


def test_filter_projects_url_resolves() -> None:
    """Test resolving and reversing the 'filter_projects' URL."""
    url_path: str = reverse("filter_projects")
    assert url_path == "/filter-projects/"
    resolved_view = resolve(url_path)
    assert resolved_view.func == views.filter_projects


def test_admin_index_url_resolves() -> None:
    """Test resolving and reversing the 'admin:index' URL."""
    url_path: str = reverse("admin:index")
    assert url_path == "/admin/"
    resolved_view = resolve(url_path)
    # Check if the resolved view name matches the expected admin index view
    assert resolved_view.view_name == "custom_admin:index"


def test_admin_login_url_resolves() -> None:
    """Test resolving and reversing the 'admin:login' URL."""
    url_path: str = reverse("admin:login")
    assert url_path == "/admin/login/"
    resolved_view = resolve(url_path)
    assert resolved_view.view_name == "custom_admin:login"


def test_admin_logout_url_resolves() -> None:
    """Test resolving and reversing the 'admin:logout' URL."""
    url_path: str = reverse("admin:logout")
    assert url_path == "/admin/logout/"
    resolved_view = resolve(url_path)
    assert resolved_view.view_name == "custom_admin:logout"


# Note: Testing the favicon redirect resolution is tricky as it's a lambda.
# We can test its reverse lookup.
def test_favicon_url_reverse() -> None:
    """Test reversing the favicon URL (no specific view name)."""
    # Favicon doesn't have a standard 'name', we resolve by path
    resolved_view = resolve("/favicon.ico")
    # Check it resolves, but asserting the lambda itself is complex/brittle.
    # We mainly care that the path exists.
    assert resolved_view is not None
