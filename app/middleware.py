"""Middleware to protect admin pages."""

import logging
from collections.abc import Callable

from django.conf import settings
from django.http import Http404, HttpRequest, HttpResponse
from ipware import get_client_ip  # type: ignore

logger = logging.getLogger(__name__)


class IPAdminRestrictMiddleware:
    """Middleware to restrict access to the admin panel by IP address."""

    def __init__(
        self, get_response: Callable[[HttpRequest], HttpResponse]
    ) -> None:
        """Initialize the middleware.

        Args:
            get_response: The next middleware or view in the chain
        """
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Process the request.

        Args:
            request: The HTTP request object

        Returns:
            HttpResponse: The HTTP response

        Raises:
            Http404: If the client IP is not allowed to access the admin
        """
        if request.path.startswith(f"/{settings.ADMIN_URL}"):
            client_ip, _is_routable = get_client_ip(request)

            if client_ip not in settings.ADMIN_IPS_ALLOWED:
                err = (
                    f"Unauthorized Client at {client_ip} tried to access "
                    "the Admin pages."
                )
                logger.error(err)
                raise Http404
        return self.get_response(request)
