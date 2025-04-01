"""Tests for the EmailService."""

from smtplib import SMTPException

import pytest
from django.conf import settings
from pytest_mock import MockerFixture

from app.models import ContactSubmission
from app.services.email import EmailService

pytestmark = pytest.mark.django_db


def test_send_contact_email_success(mocker: MockerFixture) -> None:
    """Tests successful email sending via send_contact_email."""
    mock_send_mail = mocker.patch("app.services.email.send_mail")
    submission = ContactSubmission.objects.create(
        name="Test Sender",
        email="sender@example.com",
        message="Test message content.",
    )

    result = EmailService.send_contact_email(submission)

    assert result is True
    mock_send_mail.assert_called_once()
    call_args = mock_send_mail.call_args[1]  # Use kwargs dict

    assert (
        call_args["subject"]
        == f"New Contact Form Submission from {submission.name}"
    )

    # Check content based on the actual template format
    assert f"From: {submission.name}" in call_args["message"]
    assert f"Email: {submission.email}" in call_args["message"]
    assert (
        f"Message:\n{submission.message}" in call_args["message"]
    )  # Check message with newline
    assert call_args["from_email"] == settings.DEFAULT_FROM_EMAIL
    assert call_args["recipient_list"] == [settings.CONTACT_FORM_RECIPIENT]
    assert call_args["fail_silently"] is False


def test_send_contact_email_failure(mocker: MockerFixture) -> None:
    """Tests email sending failure due to SMTPException."""
    # Arrange
    mock_send_mail = mocker.patch(
        "app.services.email.send_mail", side_effect=SMTPException
    )
    submission = ContactSubmission.objects.create(
        name="Fail Sender",
        email="fail@example.com",
        message="This message should fail.",
    )

    # Act
    result = EmailService.send_contact_email(submission)

    # Assert
    assert result is False
    mock_send_mail.assert_called_once()
