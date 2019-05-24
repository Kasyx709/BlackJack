from __future__ import division
import sys
from itertools import repeat

py_version = sys.version_info[:3]
if py_version < (3, 0):
    pass
from pandas import DataFrame as df
from pandas import isnull
from numpy.random import choice
import numpy as np

np.set_printoptions(precision=15)


class BlackJack(object):
    """
        Builds a deck using numpy arrays
        Aces = Aces in the deck, can be worth 1 or 11 (player's choice or dealer algorithm)
        Face cards = 10, Jack, Queen, King (all worth 10 points)
        Numbered cards = Cards from 2-9 (worth their numbered value)
        Cards Remaining = Number of cards left to be dealt, starting value of 52
        Suits = Hearts, Clubs, Spades, Diamonds (Arbitrarily assigned on draw, but checks for duplicates)
        As a dict this also holds values for cards played/in play
    """
    ace = 4
    f10 = 4
    Jack = 4
    Queen = 4
    King = 4
    face_card = 16
    numbered_card = 32
    numbered_values = df(data=[range(2, 10)])
    cards_remaining = 52
    cards_played = df(columns=['Hearts', 'Spades', 'Diamonds', 'Clubs'], index=range(1, 14))
    cards_played.rename(index={1: 'Ace', 11: 'Jack', 12: 'Queen', 13: 'King'}, inplace=True)

    def __init__(self, num_decks=None):
        self.num_decks = num_decks

    @classmethod
    def draw(cls):
        type_probability = {
            'ace': cls.ace / cls.cards_remaining,
            'face_card': cls.face_card / cls.cards_remaining,
            'numbered_card': cls.numbered_card / cls.cards_remaining
        }
        _p = [type_probability[k] for k in type_probability.keys()]

        if cls.cards_remaining > 0:
            card_type = choice(df([type_probability]).columns, p=_p)
            cls.cards_remaining -= 1
            card = None
            if cls.__dict__[card_type] > 0:
                setattr(cls, '{}'.format(card_type), cls.__dict__[card_type] - 1)
                if card_type is 'face_card':
                    card = None
                elif card_type is 'ace':
                    suit = cls.available_suit('Ace')
                    cls.cards_played[suit].loc['Ace'] = (1, 11)
                    card = ('Ace of {}'.format(suit))
                else:
                    _number = cls.numbered_draw()
                    if isnull(cls.cards_played.loc[_number]).any():
                        suit = cls.available_suit(_number)
                        cls.cards_played[suit].loc[_number] = _number
                        card = ('{} of {}'.format(_number, suit))
                    else:
                        while 1:
                            if isnull(cls.cards_played.loc[_number]).any():
                                suit = cls.available_suit(_number)
                                cls.cards_played[cls.available_suit(_number)].loc[_number] = _number
                                card = ('{} of {}'.format(_number, suit))
                                return card
                            else:
                                _number = cls.numbered_draw()
            return card

    @staticmethod
    def numbered_draw():
        return choice(range(2, 10))

    @classmethod
    def available_suit(cls, numbered_card):
        _ = cls.cards_played.loc[numbered_card][isnull(cls.cards_played.loc[numbered_card])]
        available_suit = choice(_.index)
        return available_suit

    @classmethod
    def test_draws(cls):
        for i in range(52):
            card = cls.draw()
        print(cls.cards_played)


def test():
    blackjack = BlackJack()
    blackjack.test_draws()


if __name__ == '__main__':
    test()

"""


face_probability = {
            'f10': cls.f10 / cls.face_card,
            'Jack': cls.Jack / cls.face_card,
            'Queen': cls.Queen / cls.face_card,
            'King': cls.King / cls.face_card,
        }
        _fp = [face_probability[k] for k in face_probability.keys()]
        
        face_type = choice(df([face_probability]).columns)
                    _remaining = cls.__dict__[face_type] - 1
                    setattr(cls, '{}'.format(face_type), _remaining)
                    card = None
"""
