"""
==============================================================================
Module Name:   test_dealer_play.py
Description:   Source module test_dealer_play.py.
Author:        Mai Tan Duc <ducmai.network@gmail.com>
Created:       2026-10-10
Version:       1.0.0
License:       MIT
==============================================================================
Usage:         python3 test_dealer_play.py [options]
Notes:         Requires Python 3.8+
==============================================================================
"""

from __future__ import annotations

from typing import Any
from unittest import mock

import card_deck
import main


def seed_deck(*cards: Any) -> None:
    """Cards are drawn in the order given (draw_card() pops from the
    end of the deck list, so we store them reversed)."""
    card_deck.deck = list(reversed(list(cards)))


class TestDealerAlwaysReachesAtLeast17:
    def test_stops_as_soon_as_total_reaches_17(self: Any, capsys: Any) -> None:
        seed_deck(["6", "Hearts"], ["9", "Spades"])
        hand = [["2", "Diamonds"]]  # total 2

        with mock.patch("builtins.input", return_value=""):
            total, turns = main.dealer_play(hand)

        assert total == 17  # 2 + 9 + 6
        assert turns == 2

    def test_non_blank_input_does_not_end_the_turn_early(
        self: Any, capsys: Any
    ) -> None:
        """This is the regression case: previously, typing anything
        other than a bare Enter stopped the dealer immediately,
        regardless of their total."""
        seed_deck(["6", "Hearts"], ["9", "Spades"])
        hand = [["2", "Diamonds"]]  # total 2, needs 17+

        with mock.patch("builtins.input", side_effect=["x", "garbage", "whatever"]):
            total, turns = main.dealer_play(hand)

        assert total >= 17
        assert turns == 2

    def test_stops_immediately_once_at_least_17_from_a_single_hit(
        self: Any, capsys: Any
    ) -> None:
        seed_deck(["8", "Hearts"])
        hand = [["9", "Diamonds"]]  # total 9 -> one hit brings it to 17

        with mock.patch("builtins.input", return_value=""):
            total, turns = main.dealer_play(hand)

        assert total == 17
        assert turns == 1
