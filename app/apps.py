from django.apps import AppConfig as AC  # to fix a mypy error


class AppConfig(AC):
    """Configure the Django app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "app"

    def ready(self) -> None:
        """Import signals when app is ready."""
        import app.signals  # noqa: F401
