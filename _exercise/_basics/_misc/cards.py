# playing cards
import random

RANKS = '2 3 4 5 6 7 8 9 10 J Q K A'.split()
SUITS = '♣ ♢ ♡ ♠'.split()

cards = ((rank, suit) for rank in RANKS for suit in SUITS)
print(cards)

def shuffle(deck):
    """Return iterator over shuffled deck."""
    deck = list(deck)
    random.shuffle(deck)
    return iter(tuple(deck))


def cut(deck, n):
    """Return an iterator over a deck of cards cut at index `n`."""
    if n < 0:
        raise ValueError('`n` must be a non-negative integer')

    deck = list(deck)
    return iter(deck[n:] + deck[:n])


cards = cut(cards, 26)  # Cut the deck in half.
cards = shuffle(cards)
