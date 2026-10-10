"""
==============================================================================
Module Name:   conftest.py
Description:   Source module conftest.py.
Author:        Mai Tan Duc <ducmai.network@gmail.com>
Created:       2026-10-10
Version:       1.0.0
License:       MIT
==============================================================================
Usage:         python3 conftest.py [options]
Notes:         Requires Python 3.8+
==============================================================================
"""

from __future__ import annotations

from typing import Any

import pytest


@pytest.fixture()
def scorefile(tmp_path: Any) -> Any:
    """Path to a scratch highscores file for a test, so tests never touch
    the real highscores.txt tracked in the repo."""
    return tmp_path / "highscores.txt"
