"""Custom template tags and filters for the app."""

from typing import Any

from django import template

register = template.Library()


@register.filter
def get_item(dictionary: dict[Any, Any], key: Any) -> Any:
    """Get an item from a dictionary using its key.

    Args:
        dictionary: The dictionary to get the item from.
        key: The key to look up.

    Returns:
        The value for the given key, or None if not found.
    """
    return dictionary.get(key)
