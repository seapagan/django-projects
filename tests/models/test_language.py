"""Tests for the Language model."""

import pytest

from app.models import Language, SiteConfiguration

pytestmark = pytest.mark.django_db


def test_language_creation_and_str() -> None:
    """Tests the creation and string representation of the Language model.

    Verifies that a Language instance can be created, linked to the
    SiteConfiguration, and its __str__ method returns the language's name.
    """
    config = SiteConfiguration.get_solo()
    language_name = "Python"
    language = Language.objects.create(config=config, name=language_name)
    assert language.config == config
    assert language.name == language_name
    assert str(language) == language_name
