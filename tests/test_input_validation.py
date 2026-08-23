from __future__ import annotations

from unittest import mock

import main


class TestInputName:
    def test_accepts_a_valid_name_on_first_try(self):
        with mock.patch("builtins.input", return_value="Henry"):
            assert main.input_name() == "Henry"

    def test_rejects_a_name_with_a_space(self, capsys):
        with mock.patch(
            "builtins.input", side_effect=["John Smith", "Henry"]
        ):
            assert main.input_name() == "Henry"
        assert "ERROR" in capsys.readouterr().out

    def test_rejects_a_name_12_characters_or_longer(self, capsys):
        with mock.patch(
            "builtins.input", side_effect=["ThisNameIsWayTooLong", "Henry"]
        ):
            assert main.input_name() == "Henry"
        assert "ERROR" in capsys.readouterr().out

    def test_rejects_an_empty_name(self, capsys):
        """Regression test: an empty string has no space in it and its
        length (0) is under 12, so it used to satisfy every check and
        be accepted as a valid name - even though the rule is "must be
        1 word", and an empty name isn't a word at all."""
        with mock.patch("builtins.input", side_effect=["", "Henry"]):
            assert main.input_name() == "Henry"
        assert "ERROR" in capsys.readouterr().out


class TestInputHitChoice:
    def test_accepts_h(self):
        with mock.patch("builtins.input", return_value="h"):
            assert main.input_hit_choice() == "h"

    def test_accepts_s(self):
        with mock.patch("builtins.input", return_value="s"):
            assert main.input_hit_choice() == "s"

    def test_rejects_anything_else_then_accepts_a_valid_choice(self, capsys):
        with mock.patch("builtins.input", side_effect=["hit", "h"]):
            assert main.input_hit_choice() == "h"
        assert "ERROR" in capsys.readouterr().out
