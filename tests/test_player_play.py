"""Tests for main.player_play().

Whether a hand is a natural (first-two-card) 21 is now decided
upstream, in play_game(), before player_play() is ever called - see
tests/test_play_game.py's TestPlayerNaturalBlackjack. player_play()
itself just implements the turn loop described in the Rules section:
keep prompting hit/stand until the player stands, or busts. It does
NOT auto-stop at exactly 21 reached via a hit - the player is still
asked, and is expected to choose to stand.
"""

from __future__ import annotations

from unittest import mock

import card_deck
import main


def seed_deck(*cards):
    card_deck.deck = list(reversed(list(cards)))


class TestNormalPlay:
    def test_hitting_then_standing(self):
        seed_deck(["3", "Hearts"], ["4", "Spades"])
        hand = [["5", "Clubs"], ["6", "Diamonds"]]  # total 11

        with mock.patch("builtins.input", side_effect=["h", "h", "s"]):
            total, turns = main.player_play("Henry", hand)

        assert total == 18
        assert turns == 2

    def test_busting_ends_the_turn_without_a_further_prompt(self):
        seed_deck(["10", "Hearts"])
        hand = [["9", "Clubs"], ["5", "Diamonds"]]  # total 14

        with mock.patch("builtins.input", side_effect=["h"]) as mock_input:
            total, turns = main.player_play("Henry", hand)

        assert total == 24
        assert turns == 1
        assert mock_input.call_count == 1  # no prompt after busting

    def test_reaching_exactly_21_via_a_hit_still_prompts_again(self):
        """This is the literal Rules-section behaviour: the player
        keeps being asked until they choose to stand, or bust - there's
        no automatic stop at 21 reached mid-turn (only a *natural*
        21 from the initial deal skips the prompt entirely, and that's
        handled by play_game() before player_play() is even called)."""
        seed_deck(["10", "Hearts"])
        hand = [["6", "Clubs"], ["5", "Diamonds"]]  # total 11

        with mock.patch(
            "builtins.input", side_effect=["h", "s"]
        ) as mock_input:
            total, turns = main.player_play("Henry", hand)

        assert total == 21
        assert turns == 1
        assert mock_input.call_count == 2  # asked again even at 21
