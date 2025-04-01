"""Tests for the home view."""

import pprint
from typing import Any

import pytest
from django import forms
from django.conf import settings
from django.contrib.messages import get_messages
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertTemplateUsed
from pytest_mock import MockerFixture

from app.forms import ContactForm
from app.models import (
    AboutSection,
    ContactSubmission,
    Project,
    SiteConfiguration,
)

pytestmark = pytest.mark.django_db


def test_home_view_get(client: Client) -> None:
    """Test the home view GET request.

    Checks status code, template used, and essential context.
    """
    # Ensure SiteConfiguration exists and create related AboutSections
    config, _ = SiteConfiguration.objects.get_or_create()
    unsafe_content = "<p>Hello <script>alert('XSS');</script> World</p>"
    safe_content_with_link = (
        'This is safe content with a <a href="https://example.com">link</a>.'
    )
    _about_section_unsafe = AboutSection.objects.create(
        config=config, content=unsafe_content
    )
    _about_section_safe = AboutSection.objects.create(
        config=config, content=safe_content_with_link
    )

    # --- Debug template DIRS ---
    print("\nDEBUG: settings.TEMPLATES:")
    pprint.pprint(settings.TEMPLATES)
    print("--- End Debug ---\n")
    # --- End Debug ---

    url = reverse("projects")
    response = client.get(url)

    assert response.status_code == 200
    assertTemplateUsed(response, "app/home.html")
    assert "config" in response.context
    assert "form" in response.context
    assert "projects" in response.context
    assert isinstance(response.context["form"], ContactForm)
    # Check if projects queryset is present (can be empty)
    assert response.context["projects"].model == Project

    # Check for sanitized about_sections in context
    assert "about_sections" in response.context
    context_about_sections = response.context["about_sections"]
    # Ensure sections are ordered predictably if necessary, e.g., by pk
    context_about_sections = sorted(context_about_sections, key=lambda s: s.pk)
    assert len(context_about_sections) == 2

    # Check first section (unsafe content)
    sanitized_content_1 = context_about_sections[0].content
    assert "<script>" not in sanitized_content_1
    assert "alert('XSS')" not in sanitized_content_1
    # Adjust expectation based on sanitizer behavior (stripping <p>)
    assert sanitized_content_1 == "Hello World"

    # Check second section (safe content with link)
    sanitized_content_2 = context_about_sections[1].content
    assert sanitized_content_2 == safe_content_with_link  # Check it's unchanged


def test_home_view_post_valid(
    client: Client, mocker: MockerFixture, mailoutbox: list[Any]
) -> None:
    """Test the home view POST request with valid data.

    Checks form validation, email sending, object creation, and redirect.
    """
    # Ensure SiteConfiguration exists
    SiteConfiguration.objects.get_or_create()
    # Mock the email sending function
    mock_send_email = mocker.patch("app.views.EmailService.send_contact_email")
    # Mock ReCaptcha field validation
    mocker.patch(
        "django_recaptcha.fields.ReCaptchaField.validate", return_value=True
    )

    url = reverse("projects")
    form_data = {
        "name": "Test User",
        "email": "test@example.com",
        "message": "This is a test message.",
        "g-recaptcha-response": "test",  # Add dummy captcha response
    }
    response = client.post(url, data=form_data)

    # Check redirect
    assertRedirects(response, reverse("contact_success"), status_code=302)

    # Check email was called
    mock_send_email.assert_called_once()
    call_args, _ = mock_send_email.call_args
    submission = call_args[0]
    assert isinstance(submission, ContactSubmission)
    assert submission.name == "Test User"
    assert submission.email == "test@example.com"
    assert submission.message == "This is a test message."

    # Check ContactSubmission was created
    assert ContactSubmission.objects.filter(email="test@example.com").exists()


def test_home_view_post_invalid(client: Client, mocker: MockerFixture) -> None:
    """Test the home view POST request with invalid data.

    Checks status code, template used, and form errors.
    """
    # Ensure SiteConfiguration exists
    SiteConfiguration.objects.get_or_create()
    # Mock the email sending function (should not be called)
    mock_send_email = mocker.patch("app.views.EmailService.send_contact_email")
    # Mock ReCaptcha field validation (won't be reached if other fields fail)
    mocker.patch(
        "django_recaptcha.fields.ReCaptchaField.validate", return_value=True
    )

    url = reverse("projects")
    form_data = {
        "name": "Test User",
        "email": "invalid-email",  # Invalid email format
        "message": "",  # Missing message
        "g-recaptcha-response": "test",  # Add dummy captcha response
    }
    response = client.post(url, data=form_data)

    # Check response
    assert response.status_code == 200
    assertTemplateUsed(response, "app/home.html")

    # Check form errors are present in context
    assert "form" in response.context
    form = response.context["form"]
    assert isinstance(form, ContactForm)
    assert form.is_valid() is False
    assert "email" in form.errors
    assert "message" in form.errors

    # Check email was NOT called
    mock_send_email.assert_not_called()

    # Check ContactSubmission was NOT created
    assert not ContactSubmission.objects.filter(name="Test User").exists()


def test_home_view_post_valid_email_fail(
    client: Client, mocker: MockerFixture
) -> None:
    """Test POST with valid data but failed email sending.

    Checks for warning message and redirect back to home.
    """
    SiteConfiguration.objects.get_or_create()
    # Mock email service to return False
    mock_send_email = mocker.patch(
        "app.views.EmailService.send_contact_email", return_value=False
    )
    mocker.patch(
        "django_recaptcha.fields.ReCaptchaField.validate", return_value=True
    )

    url = reverse("projects")
    form_data = {
        "name": "Test User EmailFail",
        "email": "test_email_fail@example.com",
        "message": "This is a test message for email failure.",
        "g-recaptcha-response": "test",
    }
    response = client.post(url, data=form_data, follow=True)  # Follow redirect

    # Should redirect back to the projects page ('/')
    assertRedirects(
        response, reverse("projects"), status_code=302, target_status_code=200
    )

    # Check warning message
    messages_list = list(get_messages(response.context["request"]))
    assert len(messages_list) == 1
    assert "issue sending the notification email" in str(messages_list[0])

    # Check email was called
    mock_send_email.assert_called_once()
    # Check ContactSubmission was still created
    assert ContactSubmission.objects.filter(
        email="test_email_fail@example.com"
    ).exists()


def test_home_view_post_invalid_captcha(
    client: Client, mocker: MockerFixture
) -> None:
    """Test POST with invalid captcha.

    Checks for captcha error message and form re-render.
    """
    SiteConfiguration.objects.get_or_create()
    mock_send_email = mocker.patch("app.views.EmailService.send_contact_email")
    # Mock ReCaptcha field validation to raise validation error
    mocker.patch(
        "django_recaptcha.fields.ReCaptchaField.validate",
        side_effect=forms.ValidationError("Captcha validation failed"),
    )

    url = reverse("projects")
    form_data = {
        "name": "Test User CaptchaFail",
        "email": "test_captcha_fail@example.com",
        "message": "This is a test message for captcha failure.",
        "g-recaptcha-response": "invalid-response",  # Provide some response
    }
    response = client.post(url, data=form_data)

    # Check response (should re-render form)
    assert response.status_code == 200
    assertTemplateUsed(response, "app/home.html")

    # Check form errors are present in context
    assert "form" in response.context
    form = response.context["form"]
    assert isinstance(form, ContactForm)
    assert form.is_valid() is False
    assert "captcha" in form.errors
    assert "Captcha validation failed" in form.errors["captcha"]

    # Check email was NOT called
    mock_send_email.assert_not_called()
    # Check ContactSubmission was NOT created
    assert not ContactSubmission.objects.filter(
        email="test_captcha_fail@example.com"
    ).exists()
