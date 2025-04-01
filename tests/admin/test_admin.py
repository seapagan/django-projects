"""Tests for the custom admin configurations in app.admin."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

import pytest
from django.contrib.admin.sites import AdminSite
from django.http import HttpRequest

from app.admin import (
    ContactSubmissionAdmin,
    CustomAdminSite,
    GitHubStatsAdmin,
    ProjectAdmin,
    admin_site,
)
from app.models import ContactSubmission, GitHubStats, Project, Tag

if TYPE_CHECKING:
    from unittest.mock import MagicMock

    from pytest_django.fixtures import SettingsWrapper
    from pytest_mock import (
        MockerFixture,
    )

pytestmark = pytest.mark.django_db


class TestCustomAdminSite:
    """Tests for the CustomAdminSite."""

    def test_get_app_list_adds_counts(
        self, mocker: MockerFixture, settings: SettingsWrapper
    ) -> None:
        """Test that get_app_list adds object counts to model names."""
        mock_request = mocker.MagicMock(spec=HttpRequest)
        mock_super_get_app_list = mocker.patch.object(
            AdminSite, "get_app_list", autospec=True
        )
        mock_apps_get_model = mocker.patch(
            "app.admin.apps.get_model", autospec=True
        )

        mock_super_get_app_list.return_value = [
            {
                "name": "App",
                "app_label": "app",
                "models": [
                    {
                        "name": "Projects",
                        "object_name": "Project",
                        "admin_url": "/admin/app/project/",
                        "add_url": "/admin/app/project/add/",
                    },
                    {
                        "name": "Site Configuration",
                        "object_name": "SiteConfiguration",
                        "admin_url": "/admin/app/siteconfiguration/",
                        "add_url": None,  # Singleton
                    },
                    {
                        "name": "Tags",
                        "object_name": "Tag",
                        "admin_url": "/admin/app/tag/",
                        "add_url": "/admin/app/tag/add/",
                    },
                ],
            }
        ]

        # Mock model classes and their counts
        mock_project_model = mocker.MagicMock()
        mock_project_model.objects.count.return_value = 5
        mock_tag_model = mocker.MagicMock()
        mock_tag_model.objects.count.return_value = 10

        def side_effect(app_label: str, model_name: str) -> MagicMock:
            if app_label == "app" and model_name == "Project":
                return cast("MagicMock", mock_project_model)
            if app_label == "app" and model_name == "Tag":
                return cast("MagicMock", mock_tag_model)
            # Raise error for SiteConfiguration to ensure it's skipped
            if app_label == "app" and model_name == "SiteConfiguration":
                err_txt = "Should not call get_model for Singleton"
                raise ValueError(err_txt)
            return cast("MagicMock", mocker.MagicMock())

        mock_apps_get_model.side_effect = side_effect

        custom_admin = CustomAdminSite()
        app_list = custom_admin.get_app_list(mock_request)

        assert len(app_list) == 1
        models = app_list[0]["models"]
        assert len(models) == 3

        # Check counts are added correctly
        assert models[0]["name"] == "Projects (5)"
        assert models[1]["name"] == "Site Configuration"  # No count
        assert models[2]["name"] == "Tags (10)"

        # Verify mocks were called as expected
        mock_super_get_app_list.assert_called_once_with(
            custom_admin, mock_request, None
        )
        assert mock_apps_get_model.call_count == 2
        mock_apps_get_model.assert_any_call("app", "Project")
        mock_apps_get_model.assert_any_call("app", "Tag")
        mock_project_model.objects.count.assert_called_once()
        mock_tag_model.objects.count.assert_called_once()


class TestProjectAdmin:
    """Tests for the ProjectAdmin configuration."""

    def test_tag_list(self) -> None:
        """Test the tag_list method returns comma-separated tags."""
        tag1 = Tag.objects.create(name="Python")
        tag2 = Tag.objects.create(name="Django")
        project = Project.objects.create(title="Test Project")
        project.tags.add(tag1, tag2)

        project_admin = ProjectAdmin(Project, admin_site)
        tag_list_output = project_admin.tag_list(project)

        # Order might vary depending on retrieval, so check both possibilities
        assert tag_list_output in ("Python, Django", "Django, Python")


class TestContactSubmissionAdmin:
    """Tests for the ContactSubmissionAdmin configuration."""

    @pytest.fixture
    def contact_admin(self) -> ContactSubmissionAdmin:
        """Fixture for ContactSubmissionAdmin instance."""
        return ContactSubmissionAdmin(ContactSubmission, admin_site)

    @pytest.fixture
    def mock_request(self, mocker: MockerFixture) -> MagicMock:
        """Fixture for a mocked HttpRequest."""
        mock: MagicMock = mocker.MagicMock(spec=HttpRequest)
        return mock

    def test_has_add_permission(
        self, contact_admin: ContactSubmissionAdmin, mock_request: MagicMock
    ) -> None:
        """Test that add permission is always False."""
        assert not contact_admin.has_add_permission(mock_request)

    def test_has_change_permission(
        self, contact_admin: ContactSubmissionAdmin, mock_request: MagicMock
    ) -> None:
        """Test that change permission is always False."""
        assert not contact_admin.has_change_permission(mock_request)
        # Test with _obj=None
        assert not contact_admin.has_change_permission(mock_request, _obj=None)
        # Test with an actual object
        submission = ContactSubmission.objects.create(
            name="Test", email="test@example.com", message="Hello"
        )
        assert not contact_admin.has_change_permission(
            mock_request, _obj=submission
        )


class TestGitHubStatsAdmin:
    """Tests for the GitHubStatsAdmin configuration."""

    @pytest.fixture
    def github_stats_admin(self) -> GitHubStatsAdmin:
        """Fixture for GitHubStatsAdmin instance."""
        return GitHubStatsAdmin(GitHubStats, admin_site)

    @pytest.fixture
    def mock_request(
        self, mocker: MockerFixture
    ) -> MagicMock:  # Correct type hint
        """Fixture for a mocked HttpRequest."""
        mock: MagicMock = mocker.MagicMock(spec=HttpRequest)
        return mock

    def test_has_add_permission(
        self,
        github_stats_admin: GitHubStatsAdmin,
        mock_request: MagicMock,
    ) -> None:
        """Test that add permission is always False."""
        assert not github_stats_admin.has_add_permission(mock_request)

    def test_has_change_permission(
        self,
        github_stats_admin: GitHubStatsAdmin,
        mock_request: MagicMock,
    ) -> None:
        """Test that change permission is always False."""
        assert not github_stats_admin.has_change_permission(mock_request)
        # Test with _obj=None
        assert not github_stats_admin.has_change_permission(
            mock_request, _obj=None
        )
        # Test with an actual object
        project = Project.objects.create(title="Test Project")
        stats = GitHubStats.objects.create(project=project)
        assert not github_stats_admin.has_change_permission(
            mock_request, _obj=stats
        )
