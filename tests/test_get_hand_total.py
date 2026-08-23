"""Regression tests for main.get_hand_total().

The original implementation valued every Ace as either all-11 or
all-1, which undercounts any hand with two or more Aces where a mixed
valuation (one Ace as 11, the rest as 1) would score higher and be
legal. Each test names a hand and its correct blackjack value.
"""

from __future__ import annotations

import pytest

import main


def card(value, suit="Hearts"):
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
def test_get_hand_total(hand, expected):
    assert main.get_hand_total(hand) == expected


def test_empty_hand_is_zero():
    assert main.get_hand_total([]) == 0
