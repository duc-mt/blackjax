"""Shared pytest fixtures."""

from __future__ import annotations
from typing import Any

import pytest


@pytest.fixture()
def scorefile(tmp_path: Any) -> Any:
    """Path to a scratch highscores file for a test, so tests never touch
    the real highscores.txt tracked in the repo."""
    return tmp_path / "highscores.txt"
