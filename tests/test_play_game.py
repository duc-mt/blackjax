"""Integration tests for the rebuilt play_game() flow.

These exercise main.play_game() end-to-end with a scripted deck and
scripted input, checking that the deal/blackjack-check/turn-order
matches the documented Algorithm and Rules:

- Both hands are dealt two cards; only the dealer's first card is shown
  until the dealer's hand is revealed.
- A natural (first-two-card) 21 for either side resolves the round
  immediately, with no hit/stand prompt.
- If neither has Blackjack, the player plays first; if the player
  busts, the round is lost immediately and the dealer does not take a
  turn at all.
- Otherwise the dealer's hidden card is revealed and the dealer hits
  until reaching 17 or more (zero hits if already there).
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


def run_one_round(tmp_path: Any, monkeypatch: Any, inputs: Any) -> Any:
    monkeypatch.chdir(tmp_path)
    main.TEXT_FILE = "highscores.txt"
    fake_input = mock.Mock(side_effect=inputs)
    with mock.patch("builtins.input", fake_input):
        main.play_game()
    return fake_input


class TestPlayerNaturalBlackjack:
    def test_wins_immediately_with_no_hit_stand_prompt(self: Any, tmp_path: Any, monkeypatch: Any, capsys: Any) -> None:
        seed_deck(
            ["5", "Hearts"], ["6", "Spades"],   # dealer: 11 (no blackjack)
            ["Ace", "Clubs"], ["King", "Diamonds"],  # player: 21
        )
        run_one_round(tmp_path, monkeypatch, ["y", "Henry", "n"])

        printed = capsys.readouterr().out
        assert "Blackjack! Henry wins!" in printed
        assert "Do you want to hit or stand" not in printed


class TestDealerNaturalBlackjack:
    def test_dealer_wins_immediately(self: Any, tmp_path: Any, monkeypatch: Any, capsys: Any) -> None:
        seed_deck(
            ["Ace", "Hearts"], ["King", "Spades"],  # dealer: 21
            ["9", "Clubs"], ["9", "Diamonds"],        # player: 18
        )
        run_one_round(tmp_path, monkeypatch, ["y", "Henry", "n"])

        printed = capsys.readouterr().out
        assert "Blackjack! Dealer wins!" in printed
        assert "Do you want to hit or stand" not in printed


class TestBothNaturalBlackjack:
    def test_is_a_push(self: Any, tmp_path: Any, monkeypatch: Any, capsys: Any) -> None:
        seed_deck(
            ["Ace", "Hearts"], ["King", "Spades"],  # dealer: 21
            ["Ace", "Clubs"], ["Queen", "Diamonds"],  # player: 21
        )
        run_one_round(tmp_path, monkeypatch, ["y", "Henry", "n"])

        printed = capsys.readouterr().out
        assert "Two player blackjack!" in printed
        assert "Push" in printed


class TestPlayerBustSkipsDealerTurnEntirely:
    def test_dealer_never_takes_a_turn_after_player_busts(self: Any, tmp_path: Any, monkeypatch: Any, capsys: Any) -> None:
        seed_deck(
            ["9", "Hearts"], ["8", "Spades"],   # dealer: 17 (already valid)
            ["9", "Clubs"], ["5", "Diamonds"],  # player: 14
            ["10", "Hearts"],                    # player hits -> 24 (bust)
        )
        fake_input = run_one_round(
            tmp_path, monkeypatch, ["y", "Henry", "h", "n"]
        )

        # Exactly 4 input() calls: play, name, one hit choice, play-again.
        # If the dealer had incorrectly taken a turn, a "Press Enter"
        # call would have needed a 5th scripted input and this would
        # have raised StopIteration instead of completing cleanly.
        assert fake_input.call_count == 4

        printed = capsys.readouterr().out
        assert "Henry bust!" in printed
        assert "Dealer wins!" in printed
        # The dealer's hand is still revealed for transparency, but no
        # extra card was drawn beyond the initial two.
        assert "Dealer's hand: 9 of Hearts, 8 of Spades" in printed


class TestDealerAlreadyAtSeventeenNeedsNoHits:
    def test_no_press_enter_prompt_when_dealer_starts_at_17_plus(self: Any, tmp_path: Any, monkeypatch: Any, capsys: Any) -> None:
        seed_deck(
            ["9", "Hearts"], ["9", "Spades"],   # dealer: 18, already valid
            ["9", "Clubs"], ["6", "Diamonds"],  # player: 15
        )
        fake_input = run_one_round(
            tmp_path, monkeypatch, ["y", "Henry", "s", "n"]
        )

        # play, name, stand-choice, play-again - no "Press Enter" call.
        assert fake_input.call_count == 4

        printed = capsys.readouterr().out
        assert "Dealer: 18" in printed
        assert "Henry: 15" in printed
        assert "Dealer wins!" in printed


class TestPushAfterDealerTakesMultipleHits:
    def test_push_shows_both_scores(self: Any, tmp_path: Any, monkeypatch: Any, capsys: Any) -> None:
        seed_deck(
            ["2", "Hearts"], ["3", "Spades"],     # dealer: 5
            ["10", "Clubs"], ["7", "Diamonds"],   # player: 17
            ["5", "Hearts"], ["7", "Spades"],     # dealer hits: 5->10->17
        )
        run_one_round(
            tmp_path, monkeypatch, ["y", "Henry", "s", "", "", "n"]
        )

        printed = capsys.readouterr().out
        assert "Dealer: 17" in printed
        assert "Henry: 17" in printed
        assert "Push" in printed
