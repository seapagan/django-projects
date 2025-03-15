"""Setup views for the app application."""

from typing import Any

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView

from app.forms import ContactForm
from app.models import Project
from app.services.github import GitHubAPIService, GitHubStats


class ProjectsListView(ListView[Project]):
    """Define a class-based list to list all projects."""

    template_name = "app/home.html"
    model = Project
    context_object_name = "projects"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:  # noqa: ANN401
        """Get context data for the template.

        This method fetches GitHub stats for all projects that have a repo URL and adds
        the contact form.

        Args:
            **kwargs: Additional context data.

        Returns:
            The context dictionary including GitHub stats and contact form.
        """
        context = super().get_context_data(**kwargs)

        # Add contact form to context if not already present
        if "form" not in context:
            context["form"] = ContactForm()

        # Fetch GitHub stats for projects
        github_service = GitHubAPIService()
        github_stats: dict[int, GitHubStats] = (
            github_service.get_stats_for_projects(list(self.get_queryset()))
        )

        # Add GitHub stats to context
        context["github_stats"] = github_stats

        return context

    def post(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        """Handle POST requests for contact form submission.

        Args:
            request: The HTTP request
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments

        Returns:
            HTTP response redirecting back to the page
        """
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the form data directly to create a new ContactSubmission
            form.save()
            messages.success(
                request,
                "Thank you for your message! I'll get back to you soon.",
            )
            return redirect("projects")

        # If form is invalid, re-render the page with the form errors
        return self.get(request, form=form)

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        """Handle GET requests.

        Args:
            request: The HTTP request
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments

        Returns:
            HTTP response with the rendered template
        """
        if "form" in kwargs:
            self.object_list = self.get_queryset()
            context = self.get_context_data(form=kwargs["form"])
            return self.render_to_response(context)
        return super().get(request, *args, **kwargs)
