"""Configure the Models."""

from django.contrib.auth.models import AbstractUser
from django.db import models


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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """Return the string representation of the Project."""
        return self.title
