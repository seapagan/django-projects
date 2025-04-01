"""Tests for the ContactForm."""

import pytest
from django import forms

from app.forms import ContactForm

# Mark all tests in this module to use the database
pytestmark = pytest.mark.django_db


def test_contact_form_valid_data() -> None:
    """Tests that the ContactForm is valid with correct data."""
    form_data = {
        "name": "Test User",
        "email": "test@example.com",
        "message": "This is a valid message.",
    }
    form = ContactForm(data=form_data)

    # Temporarily remove captcha for basic validation check
    if "captcha" in form.fields:
        del form.fields["captcha"]

    assert form.is_valid(), f"Form errors: {form.errors.as_json()}"
    # Check cleaned_data contains expected values
    assert form.cleaned_data["name"] == form_data["name"]
    assert form.cleaned_data["email"] == form_data["email"]
    assert form.cleaned_data["message"] == form_data["message"]


def test_contact_form_missing_name() -> None:
    """Tests that the ContactForm is invalid if name is missing."""
    form_data = {
        "email": "test@example.com",
        "message": "Message without name.",
    }
    form = ContactForm(data=form_data)
    if "captcha" in form.fields:
        del form.fields["captcha"]
    assert not form.is_valid()
    assert "name" in form.errors
    assert form.errors["name"] == ["This field is required."]


def test_contact_form_missing_email() -> None:
    """Tests that the ContactForm is invalid if email is missing."""
    form_data = {
        "name": "Test User",
        "message": "Message without email.",
    }
    form = ContactForm(data=form_data)
    if "captcha" in form.fields:
        del form.fields["captcha"]
    assert not form.is_valid()
    assert "email" in form.errors
    assert form.errors["email"] == ["This field is required."]


def test_contact_form_invalid_email() -> None:
    """Tests that the ContactForm is invalid with an incorrect email format."""
    form_data = {
        "name": "Test User",
        "email": "not-an-email",
        "message": "Message with invalid email.",
    }
    form = ContactForm(data=form_data)
    if "captcha" in form.fields:
        del form.fields["captcha"]
    assert not form.is_valid()
    assert "email" in form.errors
    assert form.errors["email"] == ["Enter a valid email address."]


def test_contact_form_missing_message() -> None:
    """Tests that the ContactForm is invalid if the message is missing."""
    form_data = {
        "name": "Test User",
        "email": "test@example.com",
    }
    form = ContactForm(data=form_data)
    if "captcha" in form.fields:
        del form.fields["captcha"]
    assert not form.is_valid()
    assert "message" in form.errors
    assert form.errors["message"] == ["This field is required."]


def test_contact_form_fields_and_widgets() -> None:
    """Tests the field types and widgets used in ContactForm."""
    form = ContactForm()
    assert isinstance(form.fields["name"], forms.CharField)
    assert isinstance(form.fields["name"].widget, forms.TextInput)
    assert isinstance(form.fields["email"], forms.EmailField)
    assert isinstance(form.fields["email"].widget, forms.EmailInput)
    assert isinstance(form.fields["message"], forms.CharField)
    assert isinstance(form.fields["message"].widget, forms.Textarea)

    assert "captcha" in form.fields
