"""
==============================================================================
Module Name:   card_deck.py
Description:   Source module card_deck.py.
Author:        Mai Tan Duc <ducmai.network@gmail.com>
Created:       2026-10-10
Version:       1.0.0
License:       MIT
==============================================================================
Usage:         python3 card_deck.py [options]
Notes:         Requires Python 3.8+
==============================================================================
"""

#!/usr/bin/python3
# -*- coding: utf-8 -*-
from random import shuffle

# ------------------------------ Global Constant ------------------------------
# Contains cards in the format [value, suit]
# DO NOT ACCESS THIS VARIABLE!
# Call draw_card() instead.
deck: list[list[str]] = []


# ---------------------------- Function Definitions ---------------------------
def draw_card() -> list[str]:
    """
    Removes and returns the last item from the global deck.
    The deck will be reset after the last card is drawn.
    """
    global deck
    if len(deck) == 0:
        fill(deck)
    return deck.pop()


def fill(deck: list[list[str]]) -> None:
    """
    DO NOT call this function.
    This function is called automatically by draw_card().
    Creates and returns a new deck of 52 cards.
    Each card is a list in the format [value, suit] e.g., ['Ace', 'Spades'].
    """
    deck.clear()
    for value in [
        "Ace",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "Jack",
        "Queen",
        "King",
    ]:
        for suit in ["Hearts", "Spades", "Diamonds", "Clubs"]:
            deck.append([value, suit])
    shuffle(deck)
