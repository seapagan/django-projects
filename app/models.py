"""Configure the Models."""

from __future__ import annotations

from datetime import timedelta
from typing import Any

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class ContactSubmission(models.Model):
    """Store contact form submissions."""

    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        """Meta class for ContactSubmission model."""

        ordering = ("-created_at",)

    def __str__(self) -> str:
        """Return the string representation of the ContactSubmission."""
        return f"Message from {self.name} ({self.email})"


class UserProfile(AbstractUser):
    """Define the user profile model."""


# Create your models here.
class GitHubStats(models.Model):
    """Store GitHub repository statistics."""

    project = models.OneToOneField(
        "Project", on_delete=models.CASCADE, related_name="github_stats"
    )
    stars = models.IntegerField(default=0)
    forks = models.IntegerField(default=0)
    open_issues = models.IntegerField(default=0)
    open_prs = models.IntegerField(default=0)
    last_updated = models.DateTimeField(default=timezone.now)

    class Meta:
        """Meta class for GitHubStats model."""

        verbose_name_plural = "GitHub Stats"

    def __str__(self) -> str:
        """Return the string representation of the GitHubStats."""
        return f"Stats for {self.project.title}"

    def needs_update(self) -> bool:
        """Check if stats need updating (older than 10 minutes)."""
        if not self.last_updated:
            return True
        age = timezone.now() - self.last_updated
        return age > timedelta(minutes=10)


class Project(models.Model):
    """Define the Projects model.

    This will hold all the data for individual projects.
    """

    title = models.CharField(max_length=100)
    details = models.TextField(blank=True, default="")
    repo = models.URLField(blank=True)
    website = models.URLField(blank=True)
    tags: models.ManyToManyField[Tag, Project] = models.ManyToManyField(
        "Tag", blank=True, related_name="projects"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Return the string representation of the Project."""
        return self.title

    def get_or_create_stats(self) -> GitHubStats:
        """Get or create GitHub stats for this project."""
        stats, _ = GitHubStats.objects.get_or_create(project=self)
        return stats


class Tag(models.Model):
    """Define the Tags model.

    This will contain a list of tags that can be associated with projects.
    """

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta class for Tag model."""

        ordering = ("name",)

    def __str__(self) -> str:
        """Return the string representation of the Tag."""
        return self.name

    def save(self, *args: Any, **kwargs: Any) -> None:  # noqa: ANN401
        """Override save to automatically generate slug."""
        from django.utils.text import slugify

        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
