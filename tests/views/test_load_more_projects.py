"""Tests for the load_more_projects view."""

import pytest
from django.db import models
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from app.models import Project, Tag

pytestmark = pytest.mark.django_db


@pytest.fixture
def projects_with_tags() -> tuple[list[Project], list[Tag]]:
    """Fixture to create projects and tags for filtering tests."""
    tags = [
        Tag.objects.create(name="Python", slug="python"),
        Tag.objects.create(name="Django", slug="django"),
        Tag.objects.create(name="JavaScript", slug="javascript"),
    ]
    project_list = []
    for i in range(15):
        project = Project.objects.create(
            title=f"Project {i}",
            details=f"Details for project {i}",
            priority=i,
        )
        # Assign tags to ensure filtering spans pages
        # Python: 10 projects (0, 1, 3, 4, 6, 7, 9, 10, 12, 13)
        if i in {0, 1, 3, 4, 6, 7, 9, 10, 12, 13}:
            project.tags.add(tags[0])
        # Django: 8 projects (0, 2, 4, 6, 8, 10, 12, 14)
        if i % 2 == 0:
            project.tags.add(tags[1])
        # JavaScript: 3 projects (0, 5, 10)
        if i % 5 == 0:
            project.tags.add(tags[2])  # JavaScript
        project_list.append(project)
    return project_list, tags


def test_load_more_projects_get(
    client: Client, projects_with_tags: tuple[list[Project], list[Tag]]
) -> None:
    """Test the filter_projects view GET request (HTMX, no tags).

    Checks status code, template used, and context data (paginated projects).
    """
    url = reverse("filter_projects")  # Correct URL name
    # Simulate an HTMX request by setting the HX-Request header
    # Test loading the second page (assuming default page size is e.g., 6 or 9)
    response = client.get(url + "?page=2", HTTP_HX_Request="true")

    assert response.status_code == 200
    # For HTMX requests loading more pages, the specific section template is
    # used
    assertTemplateUsed(response, "app/_load_more_section.html")
    assert "projects" in response.context

    # For HTMX page > 1 requests, the view passes the QuerySet slice directly
    projects_queryset = response.context["projects"]
    assert isinstance(projects_queryset, models.QuerySet), (
        "Context 'projects' should be a QuerySet for HTMX page > 1"
    )

    # Check that the projects on this page are correct (depends on ordering)
    # The view orders by priority (nulls last), then created_at.
    # Our fixture sets priority=i, so lower i (older) have lower priority.
    # Page 1: 0-5. Page 2: 6-11.
    expected_project_titles_page_2 = {
        f"Project {i}" for i in range(6, 12)
    }  # Assuming page size is 6
    actual_project_titles_page_2 = {p.title for p in projects_queryset}

    # Explicitly check the titles match the expected ones for page 2
    assert actual_project_titles_page_2 == expected_project_titles_page_2


def test_load_more_projects_non_htmx(
    client: Client, projects_with_tags: tuple[list[Project], list[Tag]]
) -> None:
    """Test accessing filter_projects without HTMX header.

    (initial load, no tags).
    """
    # This test needs rethinking. The view handles both initial load (non-HTMX)
    # and 'load more' (HTMX). Let's test the initial load case.
    url = reverse("filter_projects")  # Correct URL name
    response = client.get(
        url
    )  # No HX-Request header, no page param (initial load)

    # Expect the initial grid template to be used
    assert response.status_code == 200
    assertTemplateUsed(response, "app/_projects_grid.html")
    assert "projects" in response.context
    # The view passes the QuerySet slice directly, not a Page object
    projects_queryset = response.context["projects"]
    assert isinstance(projects_queryset, models.QuerySet)
    # Check if the first page of projects is present
    expected_project_titles_page_1 = {
        f"Project {i}" for i in range(6)
    }  # Assuming page size 6
    actual_project_titles_page_1 = {p.title for p in projects_queryset}
    assert actual_project_titles_page_1 == expected_project_titles_page_1


def test_filter_projects_get_with_tags(
    client: Client, projects_with_tags: tuple[list[Project], list[Tag]]
) -> None:
    """Test initial load (non-HTMX) with tag filters."""
    _, tags = projects_with_tags
    python_tag = tags[0]
    django_tag = tags[1]

    url = reverse("filter_projects")
    # Filter by Python tag
    response = client.get(url + f"?tags={python_tag.name}")

    assert response.status_code == 200
    assertTemplateUsed(response, "app/_projects_grid.html")
    projects_queryset = response.context["projects"]
    assert isinstance(projects_queryset, models.QuerySet)

    # Check only projects with 'Python' tag are returned
    # Python projects: 0, 1, 3, 4, 6, 7, 9, 10, 12, 13
    # Expected Page 1: 0, 1, 3, 4, 6, 7
    expected_titles_py_p1 = {f"Project {i}" for i in [0, 1, 3, 4, 6, 7]}
    actual_titles = {p.title for p in projects_queryset}
    assert actual_titles == expected_titles_py_p1

    # Filter by Python AND Django tags
    response = client.get(
        url + f"?tags={python_tag.name}&tags={django_tag.name}"
    )
    assert response.status_code == 200
    projects_queryset = response.context["projects"]
    # Check only projects with 'Python' AND 'Django' tags
    # Python: 0, 1, 3, 4, 6, 7, 9, 10, 12, 13
    # Django: 0, 2, 4, 6, 8, 10, 12, 14
    # Both:   0, 4, 6, 10, 12 (5 projects)
    expected_titles_py_dj_p1: set[str] = {
        f"Project {i}" for i in [0, 4, 6, 10, 12]
    }
    actual_titles = {p.title for p in projects_queryset}
    # Page 1 slice [0:6] returns all 5
    assert actual_titles == expected_titles_py_dj_p1


def test_filter_projects_get_htmx_with_tags(
    client: Client, projects_with_tags: tuple[list[Project], list[Tag]]
) -> None:
    """Test subsequent load (HTMX) with tag filters."""
    _, tags = projects_with_tags
    python_tag = tags[0]

    url = reverse("filter_projects")
    # Filter by Python tag, get page 2
    response = client.get(
        url + f"?tags={python_tag.name}&page=2", HTTP_HX_Request="true"
    )

    assert response.status_code == 200
    assertTemplateUsed(response, "app/_load_more_section.html")
    projects_queryset = response.context["projects"]
    assert isinstance(projects_queryset, models.QuerySet)

    # Check only projects with 'Python' tag are returned
    # Python projects: 0, 1, 3, 4, 6, 7, 9, 10, 12, 13
    # Page 1 had 0, 1, 3, 4, 6, 7. Page 2 should have 9, 10, 12, 13.
    expected_titles_py_p2 = {f"Project {i}" for i in [9, 10, 12, 13]}
    actual_titles = {p.title for p in projects_queryset}
    assert actual_titles == expected_titles_py_p2
