"""Setup views for the app application."""

# ruff: noqa: ANN401
from typing import Any

from django.contrib import messages
from django.db import models
from django.db.models import Case, F, Value, When
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, TemplateView

from app.forms import ContactForm
from app.models import Project, Tag
from app.services.email import EmailService
from app.services.github import GitHubAPIService


class ProjectsListView(ListView[Project]):
    """Define a class-based list to list all projects."""

    template_name = "app/home.html"
    model = Project
    context_object_name = "projects"

    def get_queryset(self) -> models.QuerySet[Project]:
        """Get queryset with custom ordering.

        1. First, projects with priority field set, ordered by priority
        2. Then, projects without priority, ordered by creation date
        """
        # Order by priority (nulls last), then by created_at
        return Project.objects.order_by(
            # This puts NULL priority values at the end
            Case(
                When(priority__isnull=True, then=Value(999999)),
                default=F("priority"),
            ),
            "created_at",
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Get context data for the template.

        This method fetches GitHub stats for all projects that have a repo URL
        and adds the contact form.

        Args:
            **kwargs: Additional context data.

        Returns:
            The context dictionary including GitHub stats and contact form.
        """
        context = super().get_context_data(**kwargs)

        # Add contact form to context if not already present
        if "form" not in context:
            context["form"] = ContactForm()

        # Get GitHub stats from database and trigger updates if needed
        github_service = GitHubAPIService()
        github_stats = github_service.get_stats_for_projects(
            list(self.get_queryset())
        )

        # Add GitHub stats to context
        context["github_stats"] = github_stats

        # Add all tags to context for the filter UI
        context["all_tags"] = Tag.objects.all().order_by("name")

        return context

    def post(
        self, request: HttpRequest, *_args: Any, **_kwargs: Any
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
            # Save to database
            submission = form.save()

            # Send email
            email_sent = EmailService.send_contact_email(submission)

            if not email_sent:
                messages.warning(
                    request,
                    "There was an issue sending the notification email, "
                    "but your message was saved.",
                )
                return redirect("/")

            return redirect("contact_success")

        # Check for captcha errors and add them to messages
        if "captcha" in form.errors:
            messages.error(request, str(form.errors["captcha"][0]))

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


class ContactSuccessView(TemplateView):
    """Display success page after contact form submission."""

    template_name = "app/contact_success.html"


def filter_projects(request: HttpRequest) -> HttpResponse:
    """Filter projects by selected tags.

    Args:
        request: The HTTP request containing tag filter parameters

    Returns:
        HTTP response with filtered projects
    """
    selected_tags = request.GET.getlist("tags")

    # Get projects with custom ordering
    projects = Project.objects.order_by(
        # This puts NULL priority values at the end
        Case(
            When(priority__isnull=True, then=Value(999999)),
            default=F("priority"),
        ),
        "created_at",
    )

    # Filter by tags if any are selected
    if selected_tags:
        # Use AND logic - projects must have ALL selected tags
        for tag in selected_tags:
            projects = projects.filter(tags__name=tag)

    # Get GitHub stats
    github_service = GitHubAPIService()
    github_stats = github_service.get_stats_for_projects(list(projects))

    return render(
        request,
        "app/_projects_grid.html",
        {
            "projects": projects,
            "github_stats": github_stats,
            "all_tags": Tag.objects.all().order_by("name"),
        },
    )
