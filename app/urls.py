"""Define URLs specific to the 'app' application."""

from django.urls import path

from app.views import ContactSuccessView, ProjectsListView, filter_projects

urlpatterns = [
    path("", ProjectsListView.as_view(), name="projects"),
    path(
        "contact/success/", ContactSuccessView.as_view(), name="contact_success"
    ),
    path("filter-projects/", filter_projects, name="filter_projects"),
]
