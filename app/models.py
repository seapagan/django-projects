"""Configure the Models."""

from __future__ import annotations

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
