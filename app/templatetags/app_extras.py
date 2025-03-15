"""Custom template tags and filters for the app."""

from typing import Optional, TypeVar

from django import template

register = template.Library()


K = TypeVar("K")  # Key type
V = TypeVar("V")  # Value type


@register.filter
def get_item(dictionary: dict[K, V], key: K) -> Optional[V]:
    """Get an item from a dictionary using its key.

    Args:
        dictionary: The dictionary to get the item from.
        key: The key to look up.

    Returns:
        The value for the given key, or None if not found.
    """
    return dictionary.get(key)
