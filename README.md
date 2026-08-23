<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
# Table of Contents

- [Aim](#aim)
- [Total Calculation](#total-calculation)
- [Implementation](#implementation)
- [Algorithm](#algorithm)
- [Rules](#rules)
- [Sample Output](#sample-output)
- [Tree Structure](#tree-structure)
- [Testing](#testing)
- [Development](#development)
- [Known Limitations](#known-limitations)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Aim

Implement a text-based card game called **Blackjack**, also known as **21**.

![Example](blackjack.png)

# Total Calculation

A player's total hand value is calculated by adding the values of each their
cards. Face cards, such as Jacks, Queens and Kings are all worth 10. The Ace is
an unusual card because, if the combined value with other cards in hand does not
exceed 21, it will be worth 11, otherwise the Ace will be worth 1.  Other number
cards are worth the number value shown on the card.

# Implementation

In a standard game of 2-player Blackjack the player and the dealer are dealt 2
cards. The player shows both cards face-up. The dealer shows one of their cards
face-up and one face-down. The player decides to draw cards by saying, "hit", or
stop drawing cards by saying, "stand". They will draw cards trying to get their
total hand value as close to 21 as possible without going over. If the total
value of cards in their hand exceeds 21, the player "busts", which means they
lose. If the player has not "bust" and they decide to "stand", then it is the
dealer's turn to draw cards. The dealer has a special rule that, as soon as
their hand value is equal to or greater than 17, they must "stand".  If the
dealer exceeds 21, the dealer will "bust", which means the player wins.  It is
possible that both the player and dealer end with the same hand value, in which
case the game is tied and this is called, "push".

In this implementation, if either player gets 21 in their first hand of 2 cards,
they get "blackjack", which means they win immediately. If the dealer has
blackjack, they will reveal their second card, and it will be game over. If both
players have blackjack in their first hand, it will be a "two player blackjack",
which means the game is tied, "push". If neither player has blackjack in their
opening hand, the player will play. If the player busts, the dealer will reveal
their second card and win automatically, otherwise the dealer will play. If the
dealer busts, the player wins, otherwise they decide the winner by comparing
their hand totals; the highest hand total wins.

In this implementation, after the player quits the game, the player's name and
average wins will be added to a text file.  If their win percentage is higher
than all other scores in the file, the game will display, "New High Score!", and
display a table containing all players and their recorded scores.

# Algorithm

1. The player and the dealer are dealt an initial hand of two cards each. The
   player shows both cards. The dealer shows only one card.
2. If the dealer has Blackjack (the first two cards dealt total 21 points) and
   the player does not, the dealer automatically wins.
3. If the player has Blackjack (the first two cards dealt total 21 points) and
   the dealer does not, the player automatically wins.
4. If both the player and the dealer have Blackjack (the first two cards dealt
   total 21 points) then it is a push (draw).
5. If neither have Blackjack, the player then plays out their hand.  Note that
   the term Blackjack can only be achieved as a result of the first two cards
   dealt.
6. When the player has finished playing out their hand, the dealer (in this case
   the computer) plays out the dealer's hand.
7. During the player's turn, the player is faced with two options either:
- Hit (take a card): After the initial deal of two cards, a player may choose to
  receive additional cards as many times as they wish, adding the point value of
  each card to their hand total.
- Stand (end their turn): Do not receive any more cards. The player's turn is
  over.
8. The player repeatedly takes a card until, the player chooses to stand, or the
   player busts i.e., exceeds a total of 21. The player's turn is over after
   deciding to stand or if they bust.
9. Once the player has finished, if the player has not bust, the dealer reveals
   their hidden second card and plays out their hand. The dealer must hit until
   they have a point value of 17 or greater.

# Rules

- If the player busts, they lose immediately.
- If the player and the dealer have the same point value, it is called a "push"
  and neither win the hand (draw).
- An initial two-card deal of 21 (an 11 plus a 10) in the very first hand is
  called Blackjack and wins the round automatically.
- An Ace counts as eleven (11) points unless this would cause the player/dealer
  to bust, in which case it is one (1) point.
- The dealer must hit until they have a point value of 17 or greater.
- The player with the higher hand that does not exceed 21 wins the game!

# Sample Output

```
--------- Welcome to Blackjack ---------

File   : main.py
Author : Tan Duc Mai
Email  : tan.duc.work@gmail.com

Do you want to play blackjack (y/n): y
Enter your name: Royal

Dealer's hand: 3 of Diamonds
Hand Total: (3)

Royal's hand: 6 of Clubs, 6 of Spades
Hand Total: (12)

Do you want to hit or stand (h/s): h

Royal's hand: 6 of Clubs, 6 of Spades, 8 of Diamonds
Hand Total: (20)

Do you want to hit or stand (h/s): s

Dealer's hand: 3 of Diamonds, 4 of Clubs
Hand Total: (7)

Press "Enter" to continue...

Dealer's hand: 3 of Diamonds, 4 of Clubs, 10 of Diamonds
Hand Total: (17)

Press "Enter" to continue...

Dealer: 17 Royal: 20 -> Royal wins!

----------------------------------------

Do you want to play again (y/n): y

Dealer's hand: 3 of Hearts
Hand Total: (3)

Royal's hand: 2 of Diamonds, Ace of Diamonds
Hand Total: (13)

Do you want to hit or stand (h/s): s

Dealer's hand: 3 of Hearts, 10 of Clubs
Hand Total: (13)

Press "Enter" to continue...

Dealer's hand: 3 of Hearts, 10 of Clubs, 8 of Hearts
Hand Total: (21)

Press "Enter" to continue...

Dealer: 21 Royal: 13 -> Dealer wins!

----------------------------------------

Would you like to play again (y/n): y

Dealer's hand: 7 of Diamonds
Hand Total: (7)

Royal's hand: King of Diamonds, 9 of Spades
Hand Total: (19)

Do you want to hit or stand (h/s): s

Dealer's hand: 7 of Diamonds, 3 of Diamonds
Hand Total: (10)

Press "Enter" to continue...

Dealer's hand: 7 of Diamonds, 3 of Diamonds, 9 of Diamonds
Hand Total: (19)

Press "Enter" to continue...

Dealer: 19 Royal: 19 -> Push!

----------------------------------------

Do you want to play again (y/n): n

You played 3 games.
 -> Won  : 1
 -> Lost : 1
 -> Tied : 1

New High Score!

NAME         SCORE
Royal        50.000
Tiffany      37.500
Mike         0.667

Thanks for playing!

---------- See you again soon ----------
```

# Tree Structure

```
├── .github/
│   ├── dependabot.yml
│   └── workflows/
│       ├── ci.yml
│       └── codeql.yml
├── README.md
├── blackjack.png
├── card_deck.py
├── highscores.txt
├── main.py
├── pyproject.toml
├── requirements-dev.txt
├── sample_output.pdf
└── tests/
    ├── conftest.py
    ├── test_add_score.py
    ├── test_dealer_play.py
    ├── test_get_hand_total.py
    ├── test_input_validation.py
    ├── test_play_game.py
    ├── test_player_play.py
    └── test_resolve_round.py
```

# Testing

Install the dev dependencies and run the test suite:

```bash
pip install -r requirements-dev.txt
pytest
```

Tests that touch the score file use a temporary path (the `scorefile`
fixture in `tests/conftest.py`), so running the suite never modifies the
real `highscores.txt`.

# Development

CI runs on every pull request and push via GitHub Actions
(`.github/workflows/ci.yml`): linting (`ruff`), tests across Python
3.10-3.12, and a `bandit` security scan. A weekly CodeQL scan and
Dependabot are also configured.

# Known Limitations

A round of review found and fixed several bugs:

- **Hands with two or more Aces were scored too low.** Aces used to be
  valued all-11 or all-1 for the whole hand; a hand like Ace+Ace+9 -
  which should score 21 (one Ace as 11, the other as 1) - scored 11
  instead. Fixed by softening Aces one at a time only as needed.
- **The dealer could stop drawing below 17.** The "must hit until 17"
  rule was gated on the exact text typed at the "Press Enter to
  continue" prompt; any stray keystroke ended the dealer's turn early
  regardless of their total.
- **`add_score()` ignored its own `filename` parameter**, always
  hardcoding the module-level `TEXT_FILE` constant instead - invisible
  in normal play (the one caller always passes `TEXT_FILE`), but it
  broke the documented API and made the function unsafe to test without
  mutating the real `highscores.txt`.
- **The "how many scores to print" logic was hardcoded** to stop at a
  specific `['Mike', 0.667]` entry - a leftover from whatever sample
  file existed during development. For any real data without that exact
  entry, every score got printed instead of just the top three.
- **A missing `highscores.txt` crashed the game** with an unhandled
  `FileNotFoundError` instead of being treated as "no scores yet".
- **A tied game could print no score information at all** - just
  `-> Push` with nothing else - whenever the dealer needed anything
  other than exactly one hit to finish, which is a routine occurrence.
- **A natural blackjack could be hit and busted.** This game's own
  documented rule is that "an initial two-card deal of 21 ... wins the
  round automatically", but the hit/stand prompt still appeared even at
  21, and choosing "hit" by mistake would draw a card and bust an
  already-winning hand. Now a natural 21 is checked immediately after
  the deal and resolves the round with no prompt at all - see below.
- **An empty name was accepted.** `input_name()`'s validation checked
  for a space and a length limit, but an empty string has neither, so
  it passed both checks despite the rule being "must be 1 word".

## Rebuilt to match the documented Algorithm

A further review found that the implementation and the README's
Algorithm section had diverged: the README describes the dealer being
dealt **two** cards (one hidden, revealed later), with both dealer and
player checked for a natural blackjack *before* the player's turn -
covering all four win/push combinations - and the dealer only taking a
turn at all if the player didn't bust. The code had never implemented
that; it only ever dealt the dealer **one** card, always played out the
dealer's turn regardless of what the player did, and had no pre-turn
blackjack check.

The game has been rebuilt to match the documented algorithm:

- The dealer is now dealt two cards up front, like the player. Only the
  first is shown (`display_dealer_upcard()`); the second stays hidden
  until the dealer's hand is revealed.
- Immediately after the deal, both hands are checked for a natural
  21. If either (or both) has one, the round resolves right there -
  the dealer's hand is revealed and the outcome is printed - with no
  hit/stand prompt at all.
- If neither has a natural 21, the player plays their turn as before
  (`player_play()` - unchanged in behaviour, just no longer needs to
  special-case an incoming 21, since that case can no longer reach it).
- If the player busts, the round is lost immediately and the dealer's
  turn is skipped entirely - the dealer's hand is still revealed for
  transparency, but no further cards are drawn. Previously the dealer
  always played out their hand and the two totals were compared
  afterward, regardless of whether the player had already busted.
- Otherwise the dealer's hidden card is revealed and `dealer_play()`
  hits until 17 or more, same as before - except the dealer may now
  need zero hits if the initial two cards already total 17+, which
  couldn't happen when the dealer only started with one card.

The win/lose/push decision itself was pulled out into a new pure
function, `resolve_round()`, replacing a deeply nested nine-branch
`if`/`elif` chain in `play_game()` that had at least one dead branch
("Two player bust!", unreachable now that a player bust is decided
before any comparison happens). `resolve_round()` takes the final
totals and blackjack/bust flags and returns the outcome and message
directly, so every rule can be tested as a one-line call with no input
mocking or scripted deck required - see `tests/test_resolve_round.py`.

