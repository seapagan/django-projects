"""Setup views for the app application."""

from typing import Any

from django.views.generic import ListView

from app.models import Project
from app.services.github import GitHubAPIService, GitHubStats


class ProjectsListView(ListView[Project]):
    """Define a class-based list to list all projects."""

    template_name = "app/home.html"
    model = Project
    context_object_name = "projects"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # noqa: ANN401
        """Get context data for the template.

        This method fetches GitHub stats for all projects that have a repo URL.

        Args:
            **kwargs: Additional context data.

        Returns:
            The context dictionary including GitHub stats.
        """
        context = super().get_context_data(**kwargs)

        # Fetch GitHub stats for projects
        github_service = GitHubAPIService()
        github_stats: dict[int, GitHubStats] = (
            github_service.get_stats_for_projects(list(self.get_queryset()))
        )

        # Add GitHub stats to context
        context["github_stats"] = github_stats

        return context
