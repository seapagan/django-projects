"""Tests for the contact success view."""

import pytest
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

pytestmark = pytest.mark.django_db


def test_contact_success_view_get(client: Client) -> None:
    """Test the contact success view GET request.

    Checks status code and template used.
    """
    url = reverse("contact_success")
    response = client.get(url)

    assert response.status_code == 200
    assertTemplateUsed(response, "app/contact_success.html")
