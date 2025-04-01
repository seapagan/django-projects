"""Tests for the Tag model."""

import pytest

from app.models import Tag

pytestmark = pytest.mark.django_db


def test_tag_creation_and_str() -> None:
    """Tests the creation and string representation of the Tag model.

    Verifies that a Tag instance can be created and its __str__ method
    returns the tag's name.
    """
    tag_name = "Test Tag"
    tag = Tag.objects.create(name=tag_name)
    assert tag.name == tag_name
    assert str(tag) == tag_name
