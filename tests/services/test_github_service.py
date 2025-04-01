"""Test the GitHub API service."""

# ruff: noqa: SLF001, PLR2004
from __future__ import annotations

import httpx
import pytest
from django.utils import timezone
from response_codes import HTTP_200_OK

from app.models import GitHubStats, Project
from app.services.github import GitHubAPIService


@pytest.fixture
def github_service() -> GitHubAPIService:
    """Create a GitHub API service instance for testing."""
    return GitHubAPIService()


def test_parse_repo_url_valid(github_service: GitHubAPIService) -> None:
    """Test parsing valid GitHub repository URLs."""
    # Test standard GitHub URL
    owner, repo = github_service.parse_repo_url("https://github.com/owner/repo")
    assert owner == "owner"
    assert repo == "repo"

    # Test URL with trailing slash
    owner, repo = github_service.parse_repo_url(
        "https://github.com/owner/repo/"
    )
    assert owner == "owner"
    assert repo == "repo"

    # Test URL with additional path components
    owner, repo = github_service.parse_repo_url(
        "https://github.com/owner/repo/issues"
    )
    assert owner == "owner"
    assert repo == "repo"


def test_parse_repo_url_invalid(github_service: GitHubAPIService) -> None:
    """Test parsing invalid GitHub repository URLs."""
    # Test empty URL
    owner, repo = github_service.parse_repo_url("")
    assert owner is None
    assert repo is None

    # Test malformed URL
    owner, repo = github_service.parse_repo_url("not_a_url")
    assert owner is None
    assert repo is None

    # Test incomplete URL
    owner, repo = github_service.parse_repo_url("https://github.com/owner")
    assert owner is None
    assert repo is None


def test_fetch_repo_stats_success(
    github_service: GitHubAPIService, mocker
) -> None:
    """Test fetching repository stats with successful API responses."""
    # Mock httpx.Client
    mock_client = mocker.MagicMock()
    mock_client.__enter__.return_value = mock_client

    # Mock responses
    mock_client.get.side_effect = [
        # First call - repo stats
        httpx.Response(
            status_code=HTTP_200_OK.status_code,
            content=b'{"stargazers_count": 100, "forks_count": 50}',
            request=httpx.Request(
                "GET", "https://api.github.com/repos/owner/repo"
            ),
        ),
        # Second call - PRs
        httpx.Response(
            status_code=HTTP_200_OK.status_code,
            headers={
                "Link": (
                    "<https://api.github.com/repos/owner/repo/pulls"
                    '?page=5>; rel="last"'
                )
            },
            content=b"[]",
            request=httpx.Request(
                "GET", "https://api.github.com/repos/owner/repo/pulls"
            ),
        ),
        # Third call - issues
        httpx.Response(
            status_code=HTTP_200_OK.status_code,
            content=b'{"total_count": 25}',
            request=httpx.Request(
                "GET", "https://api.github.com/search/issues"
            ),
        ),
    ]

    # Mock httpx.Client creation
    mocker.patch("httpx.Client", return_value=mock_client)

    # Test fetching stats
    stats = github_service._fetch_repo_stats("owner", "repo")

    assert stats is not None
    assert stats["stars"] == 100
    assert stats["forks"] == 50
    assert stats["open_prs"] == 5  # From Link header
    assert stats["open_issues"] == 25  # From issues search


def test_get_stats_for_projects(
    github_service: GitHubAPIService, mocker
) -> None:
    """Test getting GitHub stats for multiple projects."""
    # Create mock projects
    mock_project1 = mocker.MagicMock(spec=Project)
    mock_project1.id = 1
    mock_project1.repo = "https://github.com/owner1/repo1"

    mock_project2 = mocker.MagicMock(spec=Project)
    mock_project2.id = 2
    mock_project2.repo = None  # Project without repo

    mock_project3 = mocker.MagicMock(spec=Project)
    mock_project3.id = 3
    mock_project3.repo = "https://github.com/owner3/repo3"

    # Create mock stats
    mock_stats1 = mocker.MagicMock(spec=GitHubStats)
    mock_stats1.last_updated = timezone.now()
    mock_stats1.needs_update.return_value = False

    mock_stats3 = mocker.MagicMock(spec=GitHubStats)
    mock_stats3.last_updated = timezone.now() - timezone.timedelta(hours=2)
    mock_stats3.needs_update.return_value = True

    # Set up project.get_or_create_stats() returns
    mock_project1.get_or_create_stats.return_value = mock_stats1
    mock_project3.get_or_create_stats.return_value = mock_stats3

    # Mock Thread to prevent actual thread creation
    mock_thread = mocker.patch("threading.Thread")

    # Test getting stats for all projects
    stats_map = github_service.get_stats_for_projects(
        [mock_project1, mock_project2, mock_project3]
    )

    # Verify results
    assert len(stats_map) == 2  # Only projects with repos should be in map
    assert stats_map[1] == mock_stats1
    assert stats_map[3] == mock_stats3

    # Verify thread creation for project3 (needs update)
    mock_thread.assert_called_once()
    assert mock_thread.call_args[1]["args"] == (mock_project3,)
    assert mock_thread.call_args[1]["daemon"] is True

    # Verify no thread creation for project1 (doesn't need update)
    assert mock_thread.call_count == 1


def test_update_stats_sync(github_service: GitHubAPIService, mocker) -> None:
    """Test synchronous update of GitHub stats."""
    # Create mock project and stats
    mock_project = mocker.MagicMock(spec=Project)
    mock_project.repo = "https://github.com/owner/repo"
    mock_stats = mocker.MagicMock(spec=GitHubStats)
    mock_project.get_or_create_stats.return_value = mock_stats

    # Mock _fetch_repo_stats to return test data
    mock_stats_data = {
        "stars": 100,
        "forks": 50,
        "open_issues": 25,
        "open_prs": 5,
    }
    mocker.patch.object(
        github_service, "_fetch_repo_stats", return_value=mock_stats_data
    )

    # Test updating stats
    github_service._update_stats_sync(mock_project)

    # Verify stats were updated
    assert mock_stats.stars == 100
    assert mock_stats.forks == 50
    assert mock_stats.open_issues == 25
    assert mock_stats.open_prs == 5
    mock_stats.save.assert_called_once()


def test_update_stats_sync_invalid_repo(
    github_service: GitHubAPIService, mocker
) -> None:
    """Test synchronous update with invalid repository URL."""
    # Create mock project with invalid repo URL
    mock_project = mocker.MagicMock(spec=Project)
    mock_project.repo = "invalid_url"

    # Mock _fetch_repo_stats (shouldn't be called)
    mock_fetch = mocker.patch.object(github_service, "_fetch_repo_stats")

    # Test updating stats
    github_service._update_stats_sync(mock_project)

    # Verify _fetch_repo_stats was not called
    mock_fetch.assert_not_called()


def test_update_stats_sync_fetch_failure(
    github_service: GitHubAPIService, mocker
) -> None:
    """Test synchronous update when fetching stats fails."""
    # Create mock project and stats
    mock_project = mocker.MagicMock(spec=Project)
    mock_project.repo = "https://github.com/owner/repo"
    mock_stats = mocker.MagicMock(spec=GitHubStats)
    mock_project.get_or_create_stats.return_value = mock_stats

    # Mock _fetch_repo_stats to return None (failure)
    mocker.patch.object(github_service, "_fetch_repo_stats", return_value=None)

    # Test updating stats
    github_service._update_stats_sync(mock_project)

    # Verify stats were not updated
    mock_stats.save.assert_not_called()


def test_fetch_repo_stats_failure(
    github_service: GitHubAPIService, mocker
) -> None:
    """Test fetching repository stats with failed API response."""
    # Mock httpx.Client
    mock_client = mocker.MagicMock(spec=httpx.Client)
    mock_client_instance = mocker.MagicMock(spec=httpx.Client)
    mock_client.__enter__.return_value = mock_client_instance

    # Mock failed repo response
    mock_response = mocker.MagicMock(spec=httpx.Response)
    mock_response.status_code = 404
    mock_response.headers = {}
    mock_client_instance.get.return_value = mock_response

    # Mock httpx.Client creation
    mocker.patch("httpx.Client", return_value=mock_client)

    # Test fetching stats
    stats = github_service._fetch_repo_stats("owner", "repo")

    assert stats is None
    mock_client_instance.get.assert_called_once()


def test_fetch_repo_stats_no_link_header(
    github_service: GitHubAPIService, mocker
) -> None:
    """Test fetching repository stats when PR response has no Link header."""
    # Mock httpx.Client
    mock_client = mocker.MagicMock()
    mock_client.__enter__.return_value = mock_client

    # Mock responses
    mock_client.get.side_effect = [
        # First call - repo stats
        httpx.Response(
            status_code=HTTP_200_OK.status_code,
            content=b'{"stargazers_count": 100, "forks_count": 50}',
            request=httpx.Request(
                "GET", "https://api.github.com/repos/owner/repo"
            ),
        ),
        # Second call - PRs (no Link header)
        httpx.Response(
            status_code=HTTP_200_OK.status_code,
            headers={},
            content=b'[{"id": 1}, {"id": 2}]',
            request=httpx.Request(
                "GET", "https://api.github.com/repos/owner/repo/pulls"
            ),
        ),
        # Third call - issues
        httpx.Response(
            status_code=HTTP_200_OK.status_code,
            content=b'{"total_count": 25}',
            request=httpx.Request(
                "GET", "https://api.github.com/search/issues"
            ),
        ),
    ]

    # Mock httpx.Client creation
    mocker.patch("httpx.Client", return_value=mock_client)

    # Test fetching stats
    stats = github_service._fetch_repo_stats("owner", "repo")

    assert stats is not None
    assert stats["stars"] == 100
    assert stats["forks"] == 50
    assert stats["open_prs"] == 2  # From response length
    assert stats["open_issues"] == 25  # From issues search
