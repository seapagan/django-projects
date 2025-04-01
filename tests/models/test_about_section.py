"""Tests for the AboutSection model."""

import pytest

from app.models import AboutSection, SiteConfiguration

pytestmark = pytest.mark.django_db


def test_about_section_creation_and_str() -> None:
    """Tests the creation and string representation of the AboutSection model.

    Verifies that an AboutSection instance can be created, linked to the
    SiteConfiguration, and its __str__ method returns the expected format.
    """
    config = SiteConfiguration.get_solo()
    content_text = "This is the about section content."

    about_section = AboutSection.objects.create(
        config=config, content=content_text
    )

    assert about_section.config == config
    assert about_section.content == content_text
    assert str(about_section) == f"About Section {about_section.id}"

    # Verify it's accessible from the config
    assert about_section in config.about_sections.all()
