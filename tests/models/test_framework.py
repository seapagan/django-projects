"""Tests for the Framework model."""

import pytest

from app.models import Framework, SiteConfiguration

pytestmark = pytest.mark.django_db


def test_framework_creation_and_str() -> None:
    """Tests the creation and string representation of the Framework model.

    Verifies that a Framework instance can be created, linked to the
    SiteConfiguration, and its __str__ method returns the framework's name.
    """
    config = SiteConfiguration.get_solo()
    framework_name = "Django"
    framework = Framework.objects.create(config=config, name=framework_name)
    assert framework.config == config
    assert framework.name == framework_name
    assert str(framework) == framework_name
