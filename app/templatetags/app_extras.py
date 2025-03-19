"""Custom template tags and filters for the app."""

from typing import TypeVar

from django import template

from app.models import SiteConfiguration

register = template.Library()


@register.simple_tag
def profile_check(
    languages_count: int,
    frameworks_count: int,
    has_socials: bool,  # noqa: FBT001
) -> bool:
    """Return true if any of the 3 profile items exist."""
    return bool(languages_count or frameworks_count or has_socials)


@register.simple_tag
def has_social_accounts() -> bool:
    """Check if at least one social media username is configured.

    Returns:
        bool: True if at least 1 social account is configured, False otherwise.
    """
    config = SiteConfiguration.get_solo()

    # Check if ANY of the username fields are not blank
    return any(
        [
            config.github_username,
            config.twitter_username,
            config.linkedin_username,
            config.youtube_username,
            config.medium_username,
        ]
    )


K = TypeVar("K")  # Key type
V = TypeVar("V")  # Value type


@register.filter
def get_item(dictionary: dict[K, V], key: K) -> V | None:
    """Get an item from a dictionary using its key.

    Args:
        dictionary: The dictionary to get the item from.
        key: The key to look up.

    Returns:
        The value for the given key, or None if not found.
    """
    return dictionary.get(key)
