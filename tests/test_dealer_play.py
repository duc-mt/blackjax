"""Regression tests for main.dealer_play().

The original loop exit condition was gated on the literal string typed
at the "Press Enter to continue" prompt (`dealer_hit == ''`), not just
the dealer's hand total. Any stray non-blank input silently ended the
dealer's turn early, even under 17 - violating the "dealer must hit
until 17" rule. These tests seed card_deck.deck directly (draw_card()
pops from the end) so the sequence of cards drawn is deterministic.
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

    def test_non_blank_input_does_not_end_the_turn_early(self: Any, capsys: Any) -> None:
        """This is the regression case: previously, typing anything
        other than a bare Enter stopped the dealer immediately,
        regardless of their total."""
        seed_deck(["6", "Hearts"], ["9", "Spades"])
        hand = [["2", "Diamonds"]]  # total 2, needs 17+

        with mock.patch(
            "builtins.input", side_effect=["x", "garbage", "whatever"]
        ):
            total, turns = main.dealer_play(hand)

        assert total >= 17
        assert turns == 2

    def test_stops_immediately_once_at_least_17_from_a_single_hit(self: Any, capsys: Any) -> None:
        seed_deck(["8", "Hearts"])
        hand = [["9", "Diamonds"]]  # total 9 -> one hit brings it to 17

        with mock.patch("builtins.input", return_value=""):
            total, turns = main.dealer_play(hand)

        assert total == 17
        assert turns == 1
