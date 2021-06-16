# playing cards
import random

def deck():
    RANKS = '2 3 4 5 6 7 8 9 10 J Q K A'.split()
    SUITS = '♣ ♢ ♡ ♠'.split()
    return ((rank, suit) for rank in RANKS for suit in SUITS)


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


if __name__ == "__main__":
    cards = deck()
    cards = shuffle(cards)
    # print(list(cards))
    print(cards)

    # for n in range(0, 10):
    #     print("{} => {}".format(n, fibonacci3(n)))
