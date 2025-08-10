"""GitHub API service for fetching repository statistics."""

from __future__ import annotations

import os
import re
import threading
from typing import TYPE_CHECKING
from urllib.parse import urlparse

import httpx
from django.utils import timezone
from response_codes import HTTP_200_OK

if TYPE_CHECKING:  # pragma: no cover
    from app.models import GitHubStats, Project


class GitHubAPIService:
    """Service for interacting with GitHub API."""

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

    def get_stats_for_projects(
        self, projects: list[Project]
    ) -> dict[int, GitHubStats]:
        """Get GitHub stats for multiple projects.

        Args:
            projects: List of Project instances.

        Returns:
            A dictionary mapping project IDs to their GitHub statistics.
        """
        stats_map: dict[int, GitHubStats] = {}

        for project in projects:
            if project.repo:
                # Get or create stats for this project
                stats = project.get_or_create_stats()
                stats_map[project.id] = stats

                # If stats need updating, do it in a thread
                if stats.needs_update():
                    print(f"Triggering update for {project.repo}")

                    threading.Thread(
                        target=self._update_stats_sync,
                        args=(project,),
                        daemon=True,
                    ).start()
                else:
                    print(f"Using current stats for {project.repo}")

        return stats_map

    def _update_stats_sync(self, project: Project) -> None:
        """Update GitHub stats synchronously.

        Args:
            project: The project to update stats for.
        """
        owner, repo = self.parse_repo_url(project.repo)
        if not owner or not repo:
            return

        stats = self._fetch_repo_stats(owner, repo)
        if not stats:
            return

        # Update stats in database
        github_stats = project.get_or_create_stats()
        github_stats.stars = stats["stars"]
        github_stats.forks = stats["forks"]
        github_stats.open_issues = stats["open_issues"]
        github_stats.open_prs = stats["open_prs"]
        github_stats.last_updated = timezone.now()
        github_stats.save()
        print(f"Updated stats for {project.repo}")

    def _fetch_repo_stats(self, owner: str, repo: str) -> dict[str, int] | None:
        """Fetch repository and PR statistics from GitHub API.

        Args:
            owner: The repository owner.
            repo: The repository name.

        Returns:
            A dictionary containing repository statistics, or None if fetching
            fails.
        """
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
            }
