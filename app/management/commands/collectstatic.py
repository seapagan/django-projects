"""Create a custom 'collectstatic' command.

This will do the following before copying:

1) create the optimized tailwind production build
2) minify any Javascript files used by the app.
"""

from pathlib import Path
from typing import Any

import rjsmin  # type: ignore
from django.contrib.staticfiles.management.commands.collectstatic import (
    Command as CollectstaticCommand,
)
from django.core.management import call_command


class Command(CollectstaticCommand):
    """Override the 'collectstatic' command.

    This allows us to run the tailwind build and minimize javascript
    automatically.
    """

    def handle(self, **options: dict[str, Any]) -> None:
        """Called when the command is run."""
        # Build Tailwind CSS using django-tailwind
        print("\nBuilding Tailwind CSS...")
        call_command("tailwind", "build")

        # Minify JavaScript files
        print("\nMinifying JavaScript...")
        js_src_dir = Path("assets/js")

        # Walk through all JS files in the source directory
        for input_path in js_src_dir.rglob("*.js"):
            if input_path.suffix == ".js" and not input_path.name.endswith(
                ".min.js"
            ):
                output_path = input_path.with_name(input_path.stem + ".min.js")

                # Read the JavaScript file
                with input_path.open() as f:
                    js_content = f.read()

                # Minify the JavaScript
                minified_js = rjsmin.jsmin(js_content)

                # Write the minified JavaScript
                with output_path.open("w") as f:
                    f.write(minified_js)

                print(f"Minified JS file '{input_path}' to '{output_path}'")

        # Call the parent collectstatic method
        super().handle(**options)
