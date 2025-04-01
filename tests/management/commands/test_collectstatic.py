"""Tests for the custom collectstatic management command."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from app.management.commands.collectstatic import Command

if TYPE_CHECKING:
    from pyfakefs.fake_filesystem import FakeFilesystem
    from pytest_mock import MockerFixture

# Mark all tests in this module as Django tests that require database access
# Although this specific test doesn't hit the DB, it's good practice for command
# tests
pytestmark = pytest.mark.django_db


def test_collectstatic_override(
    mocker: MockerFixture,
    fs: FakeFilesystem,
) -> None:
    """Test the collectstatic command override.

    Verifies that:
    - Tailwind build command is called.
    - JavaScript files are minified.
    - The original collectstatic command is called.
    """
    # --- Arrange ---
    # Mock the call_command function
    mock_call_command = mocker.patch(
        "app.management.commands.collectstatic.call_command"
    )

    # Mock the super().handle() call within the Command class
    mock_super_handle = mocker.patch(
        "django.contrib.staticfiles.management.commands.collectstatic.Command.handle"
    )

    # Create fake JS files using pyfakefs
    js_dir = Path("assets/js")
    fs.create_dir(js_dir)
    js_file_content = "function hello() { console.log('world'); }"
    js_file_path = js_dir / "test.js"
    fs.create_file(js_file_path, contents=js_file_content)
    # Create an already minified file to ensure it's skipped
    min_js_file_path = js_dir / "already.min.js"
    fs.create_file(min_js_file_path, contents="var a=1;")

    # Instantiate the command
    command = Command()

    command.handle()

    # 1. Check if tailwind build was called
    mock_call_command.assert_called_once_with("tailwind", "build")

    # 2. Check if JS minification happened
    minified_js_path = js_dir / "test.min.js"
    assert minified_js_path.exists()
    minified_content = minified_js_path.read_text()
    assert len(minified_content) < len(js_file_content)
    assert "hello" in minified_content  # Check if function name is still there
    assert not (
        js_dir / "already.min.min.js"
    ).exists()  # Ensure .min.js was skipped

    # 3. Check if the original collectstatic handle was called
    mock_super_handle.assert_called_once()
