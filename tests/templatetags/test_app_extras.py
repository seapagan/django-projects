"""Tests for custom template tags and filters."""

from typing import Any

import pytest
from pytest_mock import MockerFixture

from app.models import SiteConfiguration
from app.templatetags.app_extras import (
    get_item,
    has_social_accounts,
    profile_check,
)


def test_profile_check_all_false() -> None:
    """Test profile_check when all parameters are false/zero."""
    result = profile_check(
        languages_count=0, frameworks_count=0, has_socials=False
    )
    assert result is False


def test_profile_check_languages_only() -> None:
    """Test profile_check when only languages_count is non-zero."""
    result = profile_check(
        languages_count=1, frameworks_count=0, has_socials=False
    )
    assert result is True


def test_profile_check_frameworks_only() -> None:
    """Test profile_check when only frameworks_count is non-zero."""
    result = profile_check(
        languages_count=0, frameworks_count=2, has_socials=False
    )
    assert result is True


def test_profile_check_socials_only() -> None:
    """Test profile_check when only has_socials is True."""
    result = profile_check(
        languages_count=0, frameworks_count=0, has_socials=True
    )
    assert result is True


def test_profile_check_all_true() -> None:
    """Test profile_check when all parameters are true/non-zero."""
    result = profile_check(
        languages_count=3, frameworks_count=2, has_socials=True
    )
    assert result is True


def test_has_social_accounts_none_configured(mocker: MockerFixture) -> None:
    """Test has_social_accounts when no social accounts are configured."""
    mock_config = mocker.Mock(
        github_username="",
        twitter_username="",
        linkedin_username="",
        youtube_username="",
        medium_username="",
    )
    mocker.patch.object(SiteConfiguration, "get_solo", return_value=mock_config)

    result = has_social_accounts()
    assert result is False


@pytest.mark.parametrize(
    "social_platform",
    [
        "github_username",
        "twitter_username",
        "linkedin_username",
        "youtube_username",
        "medium_username",
    ],
)
def test_has_social_accounts_single_platform(
    mocker: MockerFixture, social_platform: str
) -> None:
    """Test has_social_accounts with a single social platform configured.

    Args:
        mocker: pytest-mock fixture
        social_platform: name of the social platform to test
    """
    mock_config = mocker.Mock(
        github_username="",
        twitter_username="",
        linkedin_username="",
        youtube_username="",
        medium_username="",
    )
    setattr(mock_config, social_platform, "username")
    mocker.patch.object(SiteConfiguration, "get_solo", return_value=mock_config)

    result = has_social_accounts()
    assert result is True


def test_has_social_accounts_multiple_configured(mocker: MockerFixture) -> None:
    """Test has_social_accounts when multiple social accounts are configured."""
    mock_config = mocker.Mock(
        github_username="github_user",
        twitter_username="twitter_user",
        linkedin_username="",
        youtube_username="",
        medium_username="medium_user",
    )
    mocker.patch.object(SiteConfiguration, "get_solo", return_value=mock_config)

    result = has_social_accounts()
    assert result is True


def test_get_item_existing_key() -> None:
    """Test get_item filter with an existing key."""
    test_dict: dict[str, Any] = {"key": "value", "number": 42}
    assert get_item(test_dict, "key") == "value"
    assert get_item(test_dict, "number") == 42


def test_get_item_missing_key() -> None:
    """Test get_item filter with a non-existent key."""
    test_dict: dict[str, Any] = {"key": "value"}
    assert get_item(test_dict, "missing") is None


def test_get_item_empty_dict() -> None:
    """Test get_item filter with an empty dictionary."""
    test_dict: dict[str, Any] = {}
    assert get_item(test_dict, "any_key") is None


def test_get_item_different_types() -> None:
    """Test get_item filter with different types of keys and values."""
    test_dict: dict[Any, Any] = {
        42: "number",
        "string": 3.14,
        True: False,
        (1, 2): ["list"],
    }
    assert get_item(test_dict, 42) == "number"
    assert get_item(test_dict, "string") == 3.14
    assert get_item(test_dict, True) is False
    assert get_item(test_dict, (1, 2)) == ["list"]
