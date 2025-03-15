"""GitHub API service for fetching repository statistics."""

from __future__ import annotations

import os
import re
from typing import Any, TypedDict
from urllib.parse import urlparse

import httpx
from django.core.cache import cache
from django.utils import timezone

HTTP_200_OK = 200


class GitHubStats(TypedDict):
    """Type definition for GitHub repository statistics."""

    stars: int
    forks: int
    watchers: int
    open_issues: int
    open_prs: int
    last_updated: str


class GitHubAPIService:
    """Service for interacting with GitHub API with caching."""

    CACHE_TIMEOUT = 600  # 10 minutes in seconds

    def __init__(self) -> None:
        """Initialize the GitHub API service."""
        self.token = os.getenv("GITHUB_PAT")
        self.headers = (
            {"Authorization": f"token {self.token}"} if self.token else {}
        )

    def parse_repo_url(self, url: str) -> tuple[str | None, str | None]:
        """Extract owner and repo name from GitHub URL.

        Args:
            url: The GitHub repository URL.

        Returns:
            A tuple containing the owner and repository name, or (None, None) if
            parsing fails.
        """
        path = urlparse(url).path.strip("/")
        parts = path.split("/")
        if len(parts) >= 2:  # noqa: PLR2004
            return parts[0], parts[1]
        return None, None

    def get_cache_key(self, repo_url: str) -> str | None:
        """Generate a cache key for a repository URL.

        Args:
            repo_url: The GitHub repository URL.

        Returns:
            A cache key string, or None if the URL is invalid.
        """
        owner, repo = self.parse_repo_url(repo_url)
        if not owner or not repo:
            return None
        return f"github_stats:{owner}/{repo}"

    def get_repo_stats(
        self, repo_url: str, *, force_refresh: bool = False
    ) -> GitHubStats | None:
        """Fetch repository statistics from GitHub API with caching.

        Args:
            repo_url: The GitHub repository URL.
            force_refresh: Whether to bypass the cache and fetch fresh data.

        Returns:
            A dictionary containing repository statistics, or None if fetching
            fails.
        """
        cache_key = self.get_cache_key(repo_url)
        if not cache_key:
            return None

        # Check cache first if not forcing refresh
        if not force_refresh:
            cached_stats = cache.get(cache_key)
            if isinstance(cached_stats, dict):
                return cached_stats  # type: ignore

        # Cache miss or force refresh, fetch from API
        owner, repo = self.parse_repo_url(repo_url)
        stats = self._fetch_repo_stats(owner, repo)

        if stats:
            # Store in cache
            cache.set(cache_key, stats, self.CACHE_TIMEOUT)

        return stats

    def _fetch_repo_stats(
        self, owner: str | None, repo: str | None
    ) -> GitHubStats | None:
        """Fetch repository and PR statistics from GitHub API.

        Args:
            owner: The repository owner.
            repo: The repository name.

        Returns:
            A dictionary containing repository statistics, or None if fetching
            fails.
        """
        if not owner or not repo:
            return None

        with httpx.Client() as client:
            # Fetch basic repo stats
            repo_response = client.get(
                f"https://api.github.com/repos/{owner}/{repo}",
                headers=self.headers,
                timeout=10.0,
            )

            if repo_response.status_code != HTTP_200_OK:
                return None

            repo_data = repo_response.json()

            # Fetch open PRs count
            pr_response = client.get(
                f"https://api.github.com/repos/{owner}/{repo}/pulls?state=open&per_page=1",
                headers=self.headers,
                timeout=10.0,
            )

            open_prs = 0
            if pr_response.status_code == HTTP_200_OK:
                # Get total count from Link header if available
                link_header = pr_response.headers.get("Link", "")
                if 'rel="last"' in link_header:
                    match = re.search(r'page=(\d+)>; rel="last"', link_header)
                    if match:
                        open_prs = int(match.group(1))
                else:
                    # If no Link header with last page, count from response
                    open_prs = len(pr_response.json())

            # Fetch actual open issues count (excluding PRs)
            issues_response = client.get(
                f"https://api.github.com/search/issues?q=repo:{owner}/{repo}+is:issue+is:open&per_page=1",
                headers=self.headers,
                timeout=10.0,
            )

            open_issues = 0
            if issues_response.status_code == HTTP_200_OK:
                issues_data = issues_response.json()
                open_issues = issues_data.get("total_count", 0)

            return {
                "stars": repo_data.get("stargazers_count", 0),
                "forks": repo_data.get("forks_count", 0),
                "watchers": repo_data.get("subscribers_count", 0),
                "open_issues": open_issues,
                "open_prs": open_prs,
                "last_updated": timezone.now().isoformat(),
            }

    def get_stats_for_projects(
        self, projects: list[Any]
    ) -> dict[int, GitHubStats]:
        """Fetch GitHub stats for multiple projects.

        Args:
            projects: List of Project instances.

        Returns:
            A dictionary mapping project IDs to their GitHub statistics.
        """
        stats_map: dict[int, GitHubStats] = {}

        for project in projects:
            if project.repo:
                stats = self.get_repo_stats(project.repo)
                if stats:
                    stats_map[project.id] = stats

        return stats_map
