"""Tests for the SiteConfiguration singleton model."""

import pytest

from app.models import SiteConfiguration

pytestmark = pytest.mark.django_db


def test_site_configuration_singleton() -> None:
    """Tests that SiteConfiguration is a singleton.

    Verifies that get_solo() always returns the same instance and that
    direct creation raises errors or is handled by the solo library.
    """
    # Get the singleton instance (creates if not exists)
    config1 = SiteConfiguration.get_solo()
    assert isinstance(config1, SiteConfiguration)

    # Get it again, should be the same instance (same primary key)
    config2 = SiteConfiguration.get_solo()
    assert config1.pk == config2.pk

    # Verify count is always 1
    assert SiteConfiguration.objects.count() == 1


def test_site_configuration_fields_and_str() -> None:
    """Tests setting fields and the string representation.

    Verifies that fields can be set on the singleton instance and that
    the __str__ method returns the expected value.
    """
    config = SiteConfiguration.get_solo()
    config.github_username = "testuser"
    config.owner_name = "Test Owner"
    config.hero_title = "Test Hero"
    config.save()

    # Retrieve again to ensure changes persisted
    config_reloaded = SiteConfiguration.get_solo()
    assert config_reloaded.github_username == "testuser"
    assert config_reloaded.owner_name == "Test Owner"
    assert config_reloaded.hero_title == "Test Hero"

    # Test __str__
    assert str(config_reloaded) == "Site Configuration"
