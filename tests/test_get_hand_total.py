"""
==============================================================================
Module Name:   test_get_hand_total.py
Description:   Source module test_get_hand_total.py.
Author:        Mai Tan Duc <ducmai.network@gmail.com>
Created:       2026-10-10
Version:       1.0.0
License:       MIT
==============================================================================
Usage:         python3 test_get_hand_total.py [options]
Notes:         Requires Python 3.8+
==============================================================================
"""

from __future__ import annotations

from typing import Any

import pytest

import main


def card(value: Any, suit: Any = "Hearts") -> Any:
    return [value, suit]


@pytest.mark.parametrize(
    "hand, expected",
    [
        # No Aces at all.
        ([card("10"), card("King")], 20),
        ([card("2"), card("3"), card("4")], 9),
        # A single Ace, valued as 11 or softened to 1 as needed.
        ([card("Ace"), card("King")], 21),
        ([card("Ace"), card("9")], 20),
        ([card("Ace"), card("King"), card("5")], 16),
        # Two Aces: this is the case the original all-or-nothing logic
        # got wrong. One Ace as 11 + one Ace as 1 is both legal and the
        # best available total.
        ([card("Ace"), card("Ace"), card("9")], 21),
        ([card("Ace"), card("Ace")], 12),
        ([card("Ace"), card("Ace"), card("King")], 12),
        # Three and four Aces - each extra Ace over a bust threshold
        # should soften down to 1, one at a time.
        ([card("Ace"), card("Ace"), card("Ace"), card("8")], 21),
        ([card("Ace"), card("Ace"), card("Ace"), card("Ace")], 14),
        ([card("Ace"), card("Ace"), card("Ace"), card("Ace"), card("8")], 12),
    ],
)
def test_get_hand_total(hand: Any, expected: Any) -> None:
    assert main.get_hand_total(hand) == expected


def test_empty_hand_is_zero() -> None:
    assert main.get_hand_total([]) == 0
