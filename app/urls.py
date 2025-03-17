"""Define URLs specific to the 'app' application."""

from django.urls import path

from app.views import ContactSuccessView, ProjectsListView

urlpatterns = [
    path("", ProjectsListView.as_view(), name="projects"),
    path(
        "contact/success/", ContactSuccessView.as_view(), name="contact_success"
    ),
]
