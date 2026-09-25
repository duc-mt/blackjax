"""Unit tests for main.resolve_round().

This is the pure decision logic behind who wins a round, extracted from
play_game() so every branch of the Rules section can be tested directly
without playing through an entire scripted game.
"""

from __future__ import annotations
from typing import Any

import main


class TestBothBlackjack:
    def test_is_a_push(self: Any) -> None:
        outcome, message = main.resolve_round(
            "Henry", 21, 21,
            player_blackjack=True, dealer_blackjack=True, player_bust=False,
        )
        assert outcome == "push"
        assert "Push" in message


class TestDealerBlackjackOnly:
    def test_dealer_wins(self: Any) -> None:
        outcome, message = main.resolve_round(
            "Henry", 18, 21,
            player_blackjack=False, dealer_blackjack=True, player_bust=False,
        )
        assert outcome == "lose"
        assert "Dealer wins" in message


class TestPlayerBlackjackOnly:
    def test_player_wins(self: Any) -> None:
        outcome, message = main.resolve_round(
            "Henry", 21, 18,
            player_blackjack=True, dealer_blackjack=False, player_bust=False,
        )
        assert outcome == "win"
        assert "Henry wins" in message


class TestPlayerBust:
    def test_dealer_wins_immediately_without_needing_a_dealer_total(self: Any) -> None:
        outcome, message = main.resolve_round(
            "Henry", 24, 15,
            player_blackjack=False, dealer_blackjack=False, player_bust=True,
        )
        assert outcome == "lose"
        assert "Henry bust" in message
        assert "Dealer wins" in message


class TestNoBlackjackNoBust:
    def test_equal_totals_are_a_push(self: Any) -> None:
        outcome, message = main.resolve_round(
            "Henry", 19, 19,
            player_blackjack=False, dealer_blackjack=False, player_bust=False,
        )
        assert outcome == "push"
        assert "Push" in message

    def test_dealer_bust_means_player_wins(self: Any) -> None:
        outcome, message = main.resolve_round(
            "Henry", 19, 24,
            player_blackjack=False, dealer_blackjack=False, player_bust=False,
        )
        assert outcome == "win"
        assert "Dealer bust" in message
        assert "Henry wins" in message

    def test_higher_total_under_21_wins_for_the_player(self: Any) -> None:
        outcome, message = main.resolve_round(
            "Henry", 20, 18,
            player_blackjack=False, dealer_blackjack=False, player_bust=False,
        )
        assert outcome == "win"
        assert "Henry wins" in message

    def test_higher_total_under_21_wins_for_the_dealer(self: Any) -> None:
        outcome, message = main.resolve_round(
            "Henry", 18, 20,
            player_blackjack=False, dealer_blackjack=False, player_bust=False,
        )
        assert outcome == "lose"
        assert "Dealer wins" in message
