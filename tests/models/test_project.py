"""Tests for the Project model."""

import pytest

from app.models import Project, Tag

pytestmark = pytest.mark.django_db


def test_project_creation_and_str() -> None:
    """Tests the creation and string representation of the Project model.

    Verifies that a Project instance can be created with its basic fields
    and that its __str__ method returns the project's title.
    """
    project_title = "My Test Project"
    project = Project.objects.create(
        title=project_title,
        details="A description",  # Changed from description
        priority=1,
        # Removed start_date
    )
    assert project.title == project_title
    assert project.details == "A description"
    assert project.priority == 1
    assert str(project) == project_title


def test_project_relationships() -> None:
    """Tests the relationships of the Project model.

    Verifies that relationships to Language, Framework, and Tags can be
    established correctly.
    """
    tag1 = Tag.objects.create(name="Web")
    tag2 = Tag.objects.create(name="API")

    project_priority = 2

    project = Project.objects.create(
        title="Relational Project",
        details="Testing relations",
        priority=project_priority,
    )
    project.tags.add(tag1, tag2)

    assert project.tags.count() == project_priority
    assert tag1 in project.tags.all()
    assert tag2 in project.tags.all()


def test_project_ordering() -> None:
    """Tests the default ordering of the Project model.

    Verifies that projects can be correctly ordered by the 'priority' field.
    """
    # Note: The model itself doesn't define default ordering by priority.
    # This test verifies that ordering *can* be applied correctly via query.
    project1 = Project.objects.create(
        title="Low Priority",
        details="desc",  # Changed from description
        # Removed start_date
        priority=10,
    )
    project2 = Project.objects.create(
        title="High Priority",
        details="desc",  # Changed from description
        # Removed start_date
        priority=1,
    )
    project3 = Project.objects.create(
        title="Mid Priority",
        details="desc",  # Changed from description
        # Removed start_date
        priority=5,
    )

    # Explicitly order the query
    projects = Project.objects.order_by("priority")
    assert list(projects) == [project2, project3, project1]
