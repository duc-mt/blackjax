#!/usr/bin/python3
# -*- coding: utf-8 -*-

# =============================================================================
#
#        FILE:  main.py
#      AUTHOR:  Mai Tan Duc <ducmai.network@gmail.com>
#     CREATED:  2021-12-10
# DESCRIPTION:  Implement a card game called Blackjack (21).
#
# =============================================================================


# ------------------------------- Module Import -------------------------------
"""The module draws from 52 cards each time a player/computer takes turn."""
import card_deck


# ------------------------------ Global Constant ------------------------------
TEXT_FILE = 'highscores.txt'


# ---------------------------- Function Definitions ---------------------------
def display_details(filename: str, author: str, email: str) -> None:
    """Display the author's details."""
    print(f'File   : {filename}',
          f'Author : {author}',
          f'Email  : {email}',
          sep='\n',
          end='\n\n')


def input_name() -> str:
    """Prompt for, read, and validate the player's name.

    Returns
    -------
    str
        The valid user's input name.
    """
    name = ""

    # NOTE: this used to loop `while name is None or ' ' in name or
    # len(name) >= 12`. An empty string has no space in it and its
    # length (0) is under 12, so it satisfied every check and was
    # accepted as a valid name - even though the rule is "must be 1
    # word", and an empty name isn't a word at all. It would then show
    # up blank everywhere the name is displayed (e.g. "'s hand: ...").
    while name == '' or ' ' in name or len(name) >= 12:
        name = input('Enter your name: ')
        if name == '' or ' ' in name or len(name) >= 12:
            print('ERROR: Must be 1 word and less than 12 characters.')
        print()

    return name


def display_hand(player_name: str, hand: list[list[str]]) -> None:
    """Displays the hand and its total to the screen.

    Parameters
    ----------
    player_name : str
        It is either the user's name or "Dealer".
    hand : list
        The list of cards, either the dealer_hand or player_hand list.

    Returns
    -------
    None
    """
    # Output the hand.
    print(f'{player_name}\'s hand', end=': ')
    card_strings = [f'{card[0]} of {card[1]}' for card in hand]
    print(', '.join(card_strings))

    # Output the total value.
    print(f'Hand Total: ({get_hand_total(hand)})', end='\n\n')


def display_dealer_upcard(hand: list[list[str]]) -> None:
    """Display only the dealer's face-up card, keeping the rest hidden.

    Standard Blackjack rules only show one of the dealer's initial two
    cards to the player - the second stays face-down until the dealer's
    hand is revealed (either because someone has Blackjack, or because
    the player finished their turn without busting). No total is shown,
    since it isn't fully known with a card still hidden.

    Parameters
    ----------
    hand : list
        The dealer's hand. Only the first card is shown.

    Returns
    -------
    None
    """
    print(f"Dealer's hand: {hand[0][0]} of {hand[0][1]}, [face-down card]",
          end='\n\n')


def get_hand_total(hand: list[list[str]]) -> int:
    """Take a list of cards and returns the total point value of them.

    Parameters
    ----------
    str
        The cards drawn.

    Returns
    -------
    int
        The total point value of all card values in the 'hand'.
    """
    # Variable initialisation.
    point = 0
    count_ace = 0

    # Add the value of cards, treating every Ace as 11 for now.
    for card in hand:
        if card[0] == 'Ace':
            count_ace += 1
            point += 11
        elif card[0] in ['Jack', 'Queen', 'King']:
            point += 10
        else:
            point += int(card[0])

    # Soften Aces from 11 down to 1, one at a time, only as long as the
    # hand is over 21 and there's still a soft Ace to convert.
    #
    # NOTE: this used to be all-or-nothing - either every Ace counted as
    # 11, or every Ace counted as 1 - which is wrong for any hand with
    # two or more Aces. For example Ace+Ace+9 should score 21 (one Ace
    # as 11, the other as 1, i.e. 11+1+9), but the old logic could only
    # produce 9+22=31 (over 21, so falls back to all-Aces-as-1) or
    # 9+2=11, undercounting a hand that should have been a near-certain
    # winner - and potentially prompting the player to keep hitting a
    # hand that was already strong enough to stand on.
    while point > 21 and count_ace > 0:
        point -= 10
        count_ace -= 1

    return point


def input_hit_choice() -> str:
    """Prompt for, read, and validate the user's choice.

    Returns
    -------
    str
        The valid user choice which is either 'h' (hit) or 's' (stand).
    """
    choice = ''
    valid_choices = ['h', 's']

    while choice not in valid_choices:
        choice = input('Do you want to hit or stand (h/s): ')
        if choice not in valid_choices:
            print("ERROR: Must be 'h' or 's'.")
    print()

    return choice


def player_play(name: str, hand: list[list[str]]) -> tuple[int, int]:
    """
      Continue to draw cards until the user responds
      's' (stand) or their cards' total exceeds 21.

    Parameters
    ----------
    name : str
        The player's name.
    hand : list
        The list of cards drawn by the player.

    Returns
    -------
    None
    """
    # Only called once a natural (first-two-card) Blackjack has already
    # been ruled out upstream, in play_game() - so unlike a plain "is
    # the total already 21" check, this loop faithfully follows the
    # documented rule: "the player repeatedly takes a card until they
    # choose to stand, or the player busts". It does NOT auto-stand at
    # 21 reached via a hit; the player is still asked, and may choose to
    # stand (the sensible choice) - the game doesn't make that choice
    # for them.
    user_hit = ''
    count = 0

    while user_hit == '' or (user_hit == 'h' and get_hand_total(hand) <= 21):
        user_hit = input_hit_choice()

        if user_hit == 'h':
            # Draw another card.
            hand.append(card_deck.draw_card())
            count += 1
            # Output the total value.
            display_hand(name, hand)

    return get_hand_total(hand), count


def dealer_play(hand: list[list[str]]) -> tuple[int, int]:
    """Continue to draw cards until the dealer's cards' total reaches 17.

    Parameters
    ----------
    list
        The list of cards drawn by the dealer.

    Returns
    -------
    None
    """
    count = 0

    # NOTE: this used to loop `while (dealer_hit is None) or (dealer_hit
    # == '' and get_hand_total(hand) < 17)`, which meant the dealer's
    # mandatory "hit until 17" rule was silently gated on the *exact
    # string* typed at the "Press Enter" prompt. Any stray keystroke
    # before Enter (a space, a letter, anything) made dealer_hit != '',
    # which ended the dealer's turn immediately regardless of their
    # total - even well under 17. The prompt is purely for pacing; only
    # the hand total should decide whether the dealer keeps drawing.
    while get_hand_total(hand) < 17:
        # Draw another card.
        hand.append(card_deck.draw_card())
        count += 1
        # Output the total value.
        display_hand('Dealer', hand)

        input('Press "Enter" to continue...')
        print()

    return get_hand_total(hand), count


def add_score(name: str, score: float, filename: str) -> None:
    """Read the file to check if score is greater than the others in the file.

    Parameters
    ----------
    name : str
        The player's name
    score : int
        The player's score, calculated by [won/(games-tied)*100].
    filename : str
        The name of the text file containing two players' names and scores.

    Returns
    -------
    None
    """
    # NOTE: every `open(TEXT_FILE, ...)` call below used to ignore the
    # `filename` parameter entirely and hardcode the module-level
    # TEXT_FILE constant instead. In normal play this had no visible
    # effect (play_game()'s only caller always passes TEXT_FILE), but it
    # silently broke the documented API - nothing else could ever use
    # this function against a different file - and made it impossible
    # to unit test without mutating the real highscores.txt. Every
    # occurrence below now uses `filename`.

    # This program removes any blank line present in the file (if any).
    # A missing file (e.g. a fresh checkout with no highscores.txt yet,
    # or one that was deleted) used to crash with an unhandled
    # FileNotFoundError; it's now treated the same as an empty file.
    try:
        with open(filename) as check_blank_infile:
            line_list = check_blank_infile.readlines()
    except FileNotFoundError:
        line_list = []
    else:
        if '' in line_list or '\n' in line_list:
            with open(filename, 'w') as removed_blank_outfile:
                for line in line_list:
                    if line and line != '\n':
                        removed_blank_outfile.write(line)

    # This program adds/appends the new score to the score file.
    try:
        with open(filename) as infile:
            line_list = infile.readlines()
    except FileNotFoundError:
        line_list = []

    # This checks if player's score is greater than those of other.
    is_new_highscore = True

    from typing import Any
    parsed_scores: list[list[Any]] = []
    # Change {line_list}'s format to [['Tiffany', 37.500], ['Mike', 0.667]].
    for line in line_list:
        # Strip \n from each element.
        # Split the name and the score into two sub-lists.
        parts = line.rstrip().split()
        if len(parts) >= 2:
            parsed_scores.append([parts[0], float(parts[1])])

    # Compare player's score with those of the others in the score file.
    for pscore in parsed_scores:
        if pscore[1] > score:
            is_new_highscore = False

    # Adjust the score to 3 decimal points.
    score_str = f'{score:.3f}'

    if is_new_highscore:
        # This program adds the new high score to the first line.
        with open(filename, 'w') as write_outfile:
            # Write the high score to file.
            write_outfile.write(f'{name} {score_str}\n')

            # Display the first three lines: the new high score plus
            # the next two scores that were already in the file.
            #
            # NOTE: this used to decide where to stop printing by
            # comparing each line to the literal value ['Mike', 0.667] -
            # a leftover from whatever sample highscores.txt existed
            # during development. For any real file (no player named
            # exactly "Mike" with a score of exactly 0.667), that
            # comparison never matched, so continue_print never turned
            # False and *every* existing score got printed instead of
            # just the top three the comment describes.
            print('New High Score!' + '\n',
                  'NAME\tSCORE',
                  f'{name}\t{score_str}',
                  sep='\n')

            for position, score_data in enumerate(parsed_scores):
                # Adjust them to 3 decimal points and write them to file.
                line_score = f'{score_data[1]:.3f}'
                write_outfile.write(f'{score_data[0]} {line_score}\n')
                # Only display the two scores right below the new one.
                if position < 2:
                    print(f'{score_data[0]}\t{line_score}')
            print()

    else:
        # This program appends the score (not a high score) to the file.
        with open(filename, 'a') as append_outfile:
            append_outfile.write(f'{name} {score_str}\n')


def resolve_round(name: str, player_point: int, dealer_point: int,
                  player_blackjack: bool, dealer_blackjack: bool, player_bust: bool) -> tuple[str, str]:
    """Determine the outcome of a finished round and the message to show.

    Implements the Rules section of the README as a single, pure
    decision: given the final point totals and whether either side had
    a natural (first-two-card) Blackjack or the player busted, decide
    who won and what to print. Kept separate from play_game() so this
    decision logic can be tested directly, without mocking input() or
    playing through an entire game.

    Parameters
    ----------
    name : str
        The player's name.
    player_point : int
        The player's final hand total.
    dealer_point : int
        The dealer's final hand total.
    player_blackjack : bool
        True if the player's first two cards totalled 21.
    dealer_blackjack : bool
        True if the dealer's first two cards totalled 21.
    player_bust : bool
        True if the player's hand total exceeded 21 during their turn.

    Returns
    -------
    tuple[str, str]
        (outcome, message), where outcome is one of 'win', 'lose', or
        'push' from the player's perspective.
    """
    if player_blackjack and dealer_blackjack:
        return 'push', 'Two player blackjack!  ->  Push'
    if dealer_blackjack:
        return 'lose', 'Blackjack! Dealer wins!'
    if player_blackjack:
        return 'win', f'Blackjack! {name} wins!'

    score_line = f'Dealer: {dealer_point}\t{name}: {player_point}'

    if player_bust:
        return 'lose', f'{name} bust!\n{score_line}  ->  Dealer wins!'
    if player_point == dealer_point:
        return 'push', f'{score_line}  ->  Push'
    if dealer_point > 21:
        return 'win', f'Dealer bust!\n{score_line}  ->  {name} wins!'
    if player_point > dealer_point:
        return 'win', f'{score_line}  ->  {name} wins!'
    return 'lose', f'{score_line}  ->  Dealer wins!'


def play_game() -> None:
    print("--------- Welcome to Blackjack ---------\n")

    # Display the author's details.
    display_details('main.py', 'Mai Tan Duc', 'ducmai.network@gmail.com')

    # Variable initialisation.
    valid_answers = ['y', 'n']
    games = 0
    won = 0
    lost = 0
    tied = 0

    # Ask to play.
    play = ''
    while play not in valid_answers:
        play = input('Do you want to play blackjack (y/n): ')
        if play not in valid_answers:
            print("ERROR: Only enter 'y' or 'n'")

    # Start the game once the user responds 'y'.
    if play == valid_answers[0]:
        name = input_name()

        while play == valid_answers[0]:
            games += 1

            # Deal two cards each - matching the documented Algorithm:
            # the player's hand is shown in full, but only the dealer's
            # first card is shown; the second stays hidden until the
            # dealer's hand is revealed below.
            dealer_hand = [card_deck.draw_card(), card_deck.draw_card()]
            player_hand = [card_deck.draw_card(), card_deck.draw_card()]

            display_dealer_upcard(dealer_hand)
            display_hand(name, player_hand)

            player_point = get_hand_total(player_hand)
            dealer_point = get_hand_total(dealer_hand)
            player_blackjack = player_point == 21
            dealer_blackjack = dealer_point == 21
            player_bust = False

            if player_blackjack or dealer_blackjack:
                # The round is decided immediately - reveal the
                # dealer's hidden card so both hands are visible.
                display_hand('Dealer', dealer_hand)
            else:
                # Neither has Blackjack: the player plays out their
                # hand first.
                player_point, _ = player_play(name, player_hand)
                player_bust = player_point > 21

                # Reveal the dealer's hidden card either way, but the
                # dealer only takes further hits if the player didn't
                # bust - a bust already decides the round.
                display_hand('Dealer', dealer_hand)
                if not player_bust:
                    dealer_point, _ = dealer_play(dealer_hand)

            outcome, message = resolve_round(
                name, player_point, dealer_point,
                player_blackjack, dealer_blackjack, player_bust,
            )
            print(message)

            if outcome == 'win':
                won += 1
            elif outcome == 'lose':
                lost += 1
            else:
                tied += 1

            # Display a line separating each game.
            print(f"\n{'-' * 40}\n")

            # Ask to play again.
            again = ''
            while again not in valid_answers:
                again = input('Do you want to play again (y/n): ')
                if again not in valid_answers:
                    print("ERROR: Only enter 'y' or 'n'")
            play = again
            print()

        # Summary.
        print(f'You played {games} games.',
              f' -> Won:    {won}',
              f' -> Lost:   {lost}',
              f' -> Tied:   {tied}',
              sep='\n',
              end='\n\n')

        # Check for high scores, handle ZeroDivisionError if it occurs.
        try:
            add_score(name, ((won/(games-tied))*100), TEXT_FILE)
        except ZeroDivisionError as e:
            print(f'ERROR: "{e}" as the number of games ({games}) ',
                  f'is equal to to the number of tied ({tied}).')

        print('Thanks for playing!', end='\n\n')

    else:
        print('Maybe next time...', end='\n\n')


# --------------------------- Call the Main Function --------------------------
if __name__ == '__main__':
    play_game()
    print("---------- See you again soon ----------")
