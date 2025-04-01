"""Set up some pytest defaults."""

import os

import pytest


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config) -> None:
    """Clear the screen before running tests."""
    os.system("cls" if os.name == "nt" else "clear")  # noqa: S605
