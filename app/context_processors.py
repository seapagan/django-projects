"""Define some context processors."""

from django.conf import settings
from django.http import HttpRequest


def add_correct_javascript(request: HttpRequest) -> dict[str, str]:  # noqa: ARG001
    """Adds the correct javascript file to context depending on DEBUG or not."""
    return {"js_file": "js/site.js" if settings.DEBUG else "js/site.min.js"}
