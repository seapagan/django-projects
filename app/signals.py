"""Configure Django signals."""

from typing import Any

from django.db.models.signals import post_save
from django.dispatch import receiver

from app.models import Project
from app.services.github import GitHubAPIService


@receiver(post_save, sender=Project)
def update_github_stats(
    _sender: type[Project],
    instance: Project,
    *,
    _created: bool,
    **_kwargs: Any,  # noqa: ANN401
) -> None:
    """Update GitHub stats when a project is created or updated."""
    if instance.repo:  # Only proceed if the project has a GitHub repo URL
        github_service = GitHubAPIService()
        # Update stats synchronously for immediate feedback
        github_service._update_stats_sync(instance)  # noqa: SLF001
