"""Define URLs specific to the 'app' application."""

from django.urls import path

from app.views import ProjectsListView, refresh_github_stats

urlpatterns = [
    path("", ProjectsListView.as_view(), name="projects"),
    path(
        "api/refresh-github-stats/",
        refresh_github_stats,
        name="refresh_github_stats",
    ),
]
