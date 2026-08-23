"""Regression tests for main.add_score().

Covers three bugs found during review:

1. Every open() call inside add_score() hardcoded the module-level
   TEXT_FILE constant instead of using the `filename` parameter the
   function's own signature and docstring document. In normal play this
   was invisible (the one caller always passes TEXT_FILE), but it broke
   the documented API and made the function untestable without mutating
   the real highscores.txt.
2. The "how many scores to print" logic compared each line to the
   literal value ['Mike', 0.667] - a leftover dev fixture - instead of
   implementing the "top three" behaviour the surrounding comment
   describes. For any real file without that exact entry, every score
   got printed instead of just the top three.
3. A missing score file (fresh checkout, or one that's been deleted)
   raised an unhandled FileNotFoundError instead of being treated as
   "no scores yet".
"""

from __future__ import annotations

import main


def read_lines(path):
    with open(path) as f:
        return [line.rstrip("\n") for line in f]


class TestUsesThePassedFilename:
    def test_writes_to_the_given_file_not_text_file_constant(
        self, scorefile, monkeypatch
    ):
        # Point the module constant somewhere that must NOT be written
        # to, to prove add_score() isn't silently falling back to it.
        monkeypatch.setattr(main, "TEXT_FILE", "/nonexistent/should-not-be-used.txt")

        main.add_score("Henry", 100.0, str(scorefile))

        assert scorefile.exists()
        assert read_lines(scorefile) == ["Henry 100.000"]


class TestMissingFileIsTreatedAsEmpty:
    def test_first_ever_score_creates_the_file(self, scorefile):
        assert not scorefile.exists()

        main.add_score("Henry", 50.0, str(scorefile))

        assert read_lines(scorefile) == ["Henry 50.000"]


class TestHighScoreComparison:
    def test_higher_score_becomes_the_new_first_line(self, scorefile):
        scorefile.write_text("Alice 40.000\nBob 30.000\n")

        main.add_score("Henry", 100.0, str(scorefile))

        assert read_lines(scorefile)[0] == "Henry 100.000"

    def test_lower_score_is_appended_not_inserted_first(self, scorefile):
        scorefile.write_text("Alice 40.000\nBob 30.000\n")

        main.add_score("Henry", 10.0, str(scorefile))

        lines = read_lines(scorefile)
        assert lines[0] == "Alice 40.000"
        assert lines[-1] == "Henry 10.000"


class TestDisplayIsNotHardcodedToASpecificPlayer:
    """Regression test for the ['Mike', 0.667] magic check."""

    def test_prints_top_three_generically_no_name_dependency(
        self, scorefile, capsys
    ):
        # None of these names is "Mike" and none of these scores is
        # 0.667 - the old hardcoded check would never fire here, so
        # every single line would get printed instead of just the top
        # three (new score + next two).
        scorefile.write_text(
            "Alice 90.000\nBob 80.000\nCarol 70.000\nDave 60.000\n"
        )

        main.add_score("Henry", 100.0, str(scorefile))

        printed = capsys.readouterr().out
        assert "Henry" in printed
        assert "Alice" in printed
        assert "Bob" in printed
        # Carol and Dave are ranked 3rd and 4th among the *existing*
        # scores - outside the top three total (Henry, Alice, Bob) - so
        # they must not appear in the printed summary...
        assert "Carol" not in printed
        assert "Dave" not in printed
        # ...even though every score is still written to the file.
        assert read_lines(scorefile) == [
            "Henry 100.000",
            "Alice 90.000",
            "Bob 80.000",
            "Carol 70.000",
            "Dave 60.000",
        ]

    def test_blank_lines_in_the_file_are_removed(self, scorefile):
        scorefile.write_text("Alice 40.000\n\nBob 30.000\n\n")

        main.add_score("Henry", 10.0, str(scorefile))

        lines = read_lines(scorefile)
        assert "" not in lines
