"""Tests for the ContactSubmission model."""

from datetime import datetime

import pytest

from app.models import ContactSubmission

pytestmark = pytest.mark.django_db


def test_contact_submission_creation_and_str() -> None:
    """Tests the creation and str representation of the ContactSubmission model.

    Verifies that a ContactSubmission instance can be created with its fields
    and its __str__ method returns the expected format.
    """
    name = "Test User"
    email = "test@example.com"
    message = "This is a test message."
    # We don't set submitted_at as it's auto_now_add=True

    submission = ContactSubmission.objects.create(
        name=name, email=email, message=message
    )

    assert submission.name == name
    assert submission.email == email
    assert submission.message == message
    # Note: created_at has default=timezone.now, check it exists and type
    assert submission.created_at is not None
    assert isinstance(submission.created_at, datetime)
    # Check the string representation uses the correct fields
    assert str(submission) == f"Message from {name} ({email})"
