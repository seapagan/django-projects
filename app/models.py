"""Configure the Models."""

from __future__ import annotations

from datetime import timedelta
from typing import Any

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from solo.models import SingletonModel


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
        return age > timedelta(minutes=30)


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
    priority = models.IntegerField(
        blank=True, null=True, help_text="Lower numbers appear first"
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
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class SiteConfiguration(SingletonModel):
    """Define the model to hold site configration."""

    github_username = models.CharField(max_length=30, blank=True)
    twitter_username = models.CharField(max_length=30, blank=True)
    linkedin_username = models.CharField(max_length=30, blank=True)
    youtube_username = models.CharField(max_length=30, blank=True)
    medium_username = models.CharField(max_length=30, blank=True)

    owner_name = models.CharField(max_length=30, default="The Developer")
    hero_title = models.CharField(
        max_length=120, default="Full Stack Developer"
    )
    hero_info = models.TextField(max_length=500, blank=True)
    hero_secondary = models.TextField(max_length=500, blank=True)

    def __str__(self) -> str:
        """String representastion of this model."""
        return "Site Configuration"

    class Meta:
        """Configure the SiteConfiguration model."""

        verbose_name = "Site Configuration"


class Language(models.Model):
    """Model to contain the coding languages we can use."""

    config = models.ForeignKey(
        SiteConfiguration, related_name="languages", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        """Return string representation."""
        return self.name


class Framework(models.Model):
    """Model to contain the frameworks we can use."""

    config = models.ForeignKey(
        SiteConfiguration, related_name="frameworks", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        """Return string representation."""
        return self.name


class AboutSection(models.Model):
    """Model to contain configurable about sections."""

    config = models.ForeignKey(
        SiteConfiguration,
        related_name="about_sections",
        on_delete=models.CASCADE,
    )
    content = models.TextField(
        help_text="Content can include limited HTML tags."
    )

    class Meta:
        """Configure the AboutSection model."""

        verbose_name = "About Section"
        verbose_name_plural = "About Sections"

    def __str__(self) -> str:
        """Return string representation."""
        return f"About Section {self.id}"
