"""Shared pytest fixtures."""

from __future__ import annotations

import pytest


@pytest.fixture()
def scorefile(tmp_path):
    """Path to a scratch highscores file for a test, so tests never touch
    the real highscores.txt tracked in the repo."""
    return tmp_path / "highscores.txt"
