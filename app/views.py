"""Setup views for the app application."""

from django.views.generic import ListView

from app.models import Project


class ProjectsListView(ListView[Project]):
    """Define a class-based list to list all projects."""

    template_name = "app/home.html"
    model = Project
    context_object_name = "projects"
