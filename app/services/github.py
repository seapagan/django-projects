"""GitHub API service for fetching repository statistics."""

from __future__ import annotations

import os
import re
from typing import Any, TypedDict, cast
from urllib.parse import urlparse

import httpx
from django.core.cache import cache
from django.utils import timezone
from response_codes import HTTP_200_OK


class GitHubStats(TypedDict):
    """Type definition for GitHub repository statistics."""

    stars: int
    forks: int
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

    def get_stats_for_projects(
        self, projects: list[Any], *, force_refresh: bool = False
    ) -> dict[int, GitHubStats]:
        """Fetch GitHub stats for multiple projects.

        Args:
            projects: List of Project instances.
            force_refresh: Whether to bypass the cache and fetch fresh data.

        Returns:
            A dictionary mapping project IDs to their GitHub statistics.
        """
        # Build a list of cache keys for all projects
        cache_keys = {}  # Map project ID to cache key
        for project in projects:
            if project.repo:
                cache_key = self.get_cache_key(project.repo)
                if cache_key:
                    cache_keys[project.id] = cache_key

        # Get all cached stats at once
        cached_stats = cache.get_many(cache_keys.values())
        print(f"Found {len(cached_stats)} cached stats")

        # Initialize result map
        stats_map: dict[int, GitHubStats] = {}

        # Process each project
        for project in projects:
            if not project.repo:
                continue

            cache_key = cache_keys.get(project.id)
            if not cache_key:
                continue

            # Check if we have cached data
            cached_data = cached_stats.get(cache_key)
            has_cache = isinstance(cached_data, dict)

            if has_cache and not force_refresh:
                # Use cached data
                print(f"Using cached data for {project.repo}")
                stats_map[project.id] = cast("GitHubStats", cached_data)
                continue

            # Need to fetch fresh data
            print(f"Fetching fresh data for {project.repo}")
            owner, repo = self.parse_repo_url(project.repo)
            stats = self._fetch_repo_stats(owner, repo)

            if stats:
                # Store in cache and result map
                print(f"Updating cache for {project.repo}")
                cache.set(cache_key, stats, self.CACHE_TIMEOUT)
                stats_map[project.id] = stats
            elif has_cache:
                # If fetch failed but we have cached data, use that
                print(f"Fetch failed, using cached data for {project.repo}")
                stats_map[project.id] = cast("GitHubStats", cached_data)

        return stats_map

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
                "open_issues": open_issues,
                "open_prs": open_prs,
                "last_updated": timezone.now().isoformat(),
            }
