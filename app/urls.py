"""Define URLs specific to the 'app' application."""

from django.urls import path

from app.views import ProjectsListView

urlpatterns = [
    path("", ProjectsListView.as_view(), name="projects"),
]
