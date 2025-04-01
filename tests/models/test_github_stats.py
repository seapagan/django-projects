"""Tests for the GitHubStats model."""

from datetime import datetime, timedelta
from datetime import timezone as dt_timezone  # Import for timezone.utc

import pytest
from pytest_mock import MockerFixture

from app.models import GitHubStats, Project

pytestmark = pytest.mark.django_db


def test_github_stats_creation_and_str() -> None:
    """Tests the creation and string representation of the GitHubStats model.

    Verifies that a GitHubStats instance can be created with its fields,
    correctly links to a Project, and its __str__ method returns the
    expected format.
    """
    project_title = "Stats Project"
    project = Project.objects.create(
        title=project_title,
        details="Project for stats",  # Changed from description
        priority=1,
        repo="https://github.com/user/repo",  # Changed from repo_url
    )
    # Use dt_timezone.utc here
    last_updated = datetime(2023, 10, 26, 12, 0, 0, tzinfo=dt_timezone.utc)

    fake_stars = 100
    fake_forks = 20

    stats = GitHubStats.objects.create(
        project=project,
        stars=fake_stars,
        forks=fake_forks,
        last_updated=last_updated,
    )

    assert stats.project == project
    assert stats.stars == fake_stars
    assert stats.forks == fake_forks
    assert stats.last_updated == last_updated
    assert str(stats) == f"Stats for {project_title}"  # Corrected format


def test_github_stats_needs_update(mocker: MockerFixture) -> None:
    """Tests the needs_update method using mocked time.

    Verifies that the method correctly determines if the stats are older
    than the defined threshold (30 minutes) relative to a mocked 'now'.
    """
    project = Project.objects.create(title="Update Test Project", priority=1)
    stats = GitHubStats.objects.create(project=project)

    # Define a fixed point in time for "now"
    mock_now = datetime(2024, 1, 1, 12, 0, 0, tzinfo=dt_timezone.utc)
    mocker.patch("django.utils.timezone.now", return_value=mock_now)

    # Case 1: Updated exactly "now" - should not need update
    stats.last_updated = mock_now
    stats.save()
    assert not stats.needs_update()

    # Case 2: Older than 30 minutes - should need update
    stats.last_updated = mock_now - timedelta(minutes=30, seconds=1)
    stats.save()
    assert stats.needs_update()

    # Case 3: Exactly 30 minutes old - should not need update (uses >)
    stats.last_updated = mock_now - timedelta(minutes=30)
    stats.save()
    assert not stats.needs_update()

    # Case 4: Slightly less than 30 minutes old - should not need update
    stats.last_updated = mock_now - timedelta(minutes=29, seconds=59)
    stats.save()
    assert not stats.needs_update()

    # Case 5: Test the `if not self.last_updated:` branch directly in memory
    stats.last_updated = mock_now  # Reset to a known non-None value first
    stats.save()

    stats.last_updated = None  # type: ignore [assignment]
    assert stats.needs_update()
