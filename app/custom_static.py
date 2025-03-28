"""Override the staticfiles so our CSS and JS source files are not copied."""

from types import ModuleType

from django.contrib.staticfiles.apps import StaticFilesConfig


class CustomStaticFilesConfig(StaticFilesConfig):
    """Create a custom static files app.

    All we are doing here is modifying the ignore_patterns so our source.css and
    site.js are not copied.

    We could just set the 'ignore_patterns' to this, but that will drop the
    current defaults.

    In future I will look at how to make this more dynamic.
    """

    def __init__(self, app_name: str, app_module: ModuleType | None) -> None:
        """Override the class constructor."""
        super().__init__(app_name, app_module)

        self.ignore_patterns = [
            *getattr(self, "ignore_patterns", []),
            "source.css",
            "site.js",
        ]
