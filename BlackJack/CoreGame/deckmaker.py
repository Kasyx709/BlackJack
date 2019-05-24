from numpy.random import choice
from scipy.special import binom
from pandas import DataFrame


class BlackJack(object):
    """
        Builds a deck using numpy arrays
        card_type_ace = Aces in the deck, can be worth 1 or 11 (player's choice or dealer algorithm)
        card_point_value_10 = 10, Jack, Queen, King (all worth 10 points)
        Numbered cards = Cards from 2-9 (worth their numbered value)
        Cards Remaining = Number of cards left to be dealt, starting value of 52
        Suits = Hearts, Clubs, Spades, Diamonds (Arbitrarily assigned on draw, but checks for duplicates)
        As a dict this also holds values for cards played/in play
    """

    def __init__(self, num_decks=None):
        super(BlackJack, self).__init__()
        self.num_decks = num_decks if num_decks and 1 >= num_decks <= 9 else 1
        starting_num = 4 * self.num_decks
        self.deck = {
            # Card Type : Number of cards in Deck, value
            'card_type_ace': starting_num,
            'card_type_two': starting_num,
            'card_type_three': starting_num,
            'card_type_four': starting_num,
            'card_type_five': starting_num,
            'card_type_six': starting_num,
            'card_type_seven': starting_num,
            'card_type_eight': starting_num,
            'card_type_nine': starting_num,
            'card_type_10': starting_num,
            'card_type_jack': starting_num,
            'card_type_queen': starting_num,
            'card_type_king': starting_num,
        }
        self.cards_remaining = sum(self.deck.values())
        self.deck_array = DataFrame(columns=['Hearts', 'Spades', 'Diamonds', 'Clubs'],
                                    index=self.deck.keys()).fillna(False)
        self.index_map = {name: i for i, name in enumerate(self.deck_array.index)}
        self.last_suit = None
        self.num_suits = 4
        self.suits_remaining = {
            'Hearts': 13,
            'Clubs': 13,
            'Diamonds': 13,
            'Spades': 13,
        }

    def draw(self):
        probabilities = [(self.deck[k] / self.cards_remaining) for k in self.deck.keys()]
        card = choice(a=self.deck_array.index, p=probabilities)
        if self.deck[card] > 0:
            self.deck.update({card: self.deck[card] - 1})
            # This gives the index array value
            x = (self.deck_array.loc[card].notna())
            suit = self.available_suit(card=card)
            self.cards_remaining -= 1
            return '{} of {}'.format(card, suit)

    def available_suit(self, card=None):
        _items = [suit for suit in self.deck_array.columns if self.suits_remaining[suit] > 0
                  and not self.deck_array.loc[card][suit].all()]
        _cards_remaining = sum([self.suits_remaining[key] for key in self.suits_remaining.keys() if key in _items])
        _suit_probability = [binom(self.suits_remaining[key], 1) / binom(_cards_remaining, 1) for key in
                             self.suits_remaining.keys() if self.suits_remaining[key] > 0 and key in _items]
        suit = choice(a=_items, p=_suit_probability)
        if not self.deck_array.loc[card][suit].all():
            self.deck_array.loc[card][suit] = True
            self.suits_remaining[suit] -= 1
            return suit

    def turn(self):
        pass

    def test_draws(self):
        for i in range(52):
            card = self.draw()
            print(card)


def test():
    blackjack = BlackJack()
    blackjack.test_draws()
