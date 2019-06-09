__package__ = 'GameFiles'
from numpy.random import choice
from scipy.special import binom
from pandas import DataFrame

from multiprocessing import JoinableQueue as jQueue
from multiprocessing.dummy import Process as Thread
from multiprocessing.managers import BaseManager
import os


class MetaHouse(type):
    _instances = {}
    token = os.urandom(256)

    def __new__(mcs, names, bases, m_dict={}, **kwargs):
        _house = super().__new__(mcs, names, bases, m_dict)
        mcs.find_port(_house)
        setattr(_house, 'buildHouse', mcs.build_house)
        setattr(_house, 'makePlayer', Player)
        setattr(_house, 'makeDealer', Dealer)
        setattr(_house, 'makeDeck', Deck)
        setattr(_house, 'shuffle', Deck.shuffle)
        setattr(_house, 'load_shoe', Deck.load_shoe)
        setattr(_house, 'calc_ace', Deck.calc_ace)
        setattr(_house, 'calc_points', Deck.calc_points)
        return _house

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaHouse, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

    def find_port(cls):
        import socket
        from contextlib import closing
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.bind(('', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            setattr(cls, 'port', s.getsockname()[1])
            return

    def build_house(cls):
        """
        Builds a Server Queue Manager(SQM) to control player and dealer turns.
        Assigns address to localhost with port 0 to ensure OS will assign an open port
        Authentication is key upon MetaClass initialization.
        Method returns SQM wrapped inside of a thread
        :return: Thread(target=BaseManager(address=('localhost', 0), authkey=cls.authkey), args=(),)
        """
        turn_queue = jQueue()

        class HouseManager(BaseManager): pass

        HouseManager.register('cards', callable=lambda: turn_queue)
        HouseManager.register('start_server', callable=lambda _: _.serve_forever())
        manager = HouseManager(address=('localhost', cls.port), authkey=MetaHouse.token)
        server = manager.get_server()
        setattr(cls, 'server', Thread(target=server.serve_forever, args=(), ))
        return


class Player(object):
    class PlayerManager(BaseManager): pass

    PlayerManager.register('cards')

    def __init__(self, name=None, port=None):
        super(Player, self).__init__()
        self.points = 0
        self.playerID = r'{}'.format(name)
        self.playerKey = os.urandom(50)
        self.port = port
        self.player = self.PlayerManager(address=('localhost', self.port), authkey=MetaHouse.token)
        self.playerCards = dict()


class Dealer(object):
    class DealerManager(BaseManager): pass

    DealerManager.register('cards')

    def __init__(self, port=None):
        super(Dealer, self).__init__()
        self.points = 0
        self.dealerKey = os.urandom(256)
        self.port = port
        self.dealer = self.DealerManager(address=('localhost', self.port), authkey=MetaHouse.token)
        self.dealerCards = dict()


class Deck(object):
    """
        Builds a deck using numpy arrays
        card_type_ace = Aces in the deck, can be worth 1 or 11 (player's choice or dealer algorithm)
        card_point_value_10 = 10, Jack, Queen, King (all worth 10 points)
        Numbered cards = Cards from 2-9 (worth their numbered value)
        Cards Remaining = Number of cards left to be dealt, starting value of 52
        Suits = Hearts, Clubs, Spades, Diamonds (Arbitrarily assigned on draw, but checks for duplicates)
        As a dict this also holds values for cards played/in play
    """
    card_types = [
        # Card Type
        'card_type_ace',
        'card_type_two',
        'card_type_three',
        'card_type_four',
        'card_type_five',
        'card_type_six',
        'card_type_seven',
        'card_type_eight',
        'card_type_nine',
        'card_type_ten',
        'card_type_jack',
        'card_type_queen',
        'card_type_king',
    ]
    point_array = DataFrame(index=card_types, columns=['PointValues'])

    def __init__(self):
        super(Deck, self).__init__()
        self.numDecks = self.num_decks()
        starting_num = 4 * self.numDecks
        self.deck = {card_type: starting_num for card_type in self.card_types}
        # Aces are initially assigned a value of 0, to be calculated later based upon current points
        self.point_array.iloc[0] = 0
        for i in range(2, 14):
            self.point_array.iloc[i - 1] = i if i < 10 else 10
        self.cards_remaining = sum(self.deck.values())
        self.deck_array = DataFrame(columns=['Hearts', 'Spades', 'Diamonds', 'Clubs'],
                                    index=self.deck.keys()).fillna(0)
        self.index_map = {name: i for i, name in enumerate(self.deck_array.index)}
        starting_suits = 13 * self.numDecks
        self.suits_remaining = {
            'Hearts': starting_suits,
            'Clubs': starting_suits,
            'Diamonds': starting_suits,
            'Spades': starting_suits,
        }

    @staticmethod
    def calc_ace(points):
        if points + 11 > 21:
            return 1
        else:
            return 11

    @classmethod
    def calc_points(cls, cards, dealer=False):
        points = 0
        for card in cards:
            card = card.split(' ')[0]
            if card == 'card_type_ace' and dealer:
                points = points + cls.calc_ace(points)
            elif card == 'card_type_ace' and not dealer:
                pass
            else:
                points = points + cls.point_array.loc[card].values
        return int(points)

    @classmethod
    def load_shoe(cls, address, port):
        class Shoe(BaseManager): pass

        Shoe.register('cards')
        _shoe = Shoe(address=(address, port), authkey=MetaHouse.token)
        return _shoe

    @staticmethod
    def num_decks():
        while 1:
            try:
                num_decks = input("'How many Decks would you like to use?\nThe Default is 1 and Maximum allowed is 8"
                                  "\nPlease select a number between 1 and 8 or press Enter to use the Default of 1:")
                if num_decks == '':
                    return 1
                if 0 < int(num_decks) <= 8:
                    return int(num_decks)
                else:
                    print(r"You've selected an invalid number, please try again.")
                    continue
            except ValueError:
                print(r"That's not a valid number, please try again")

    def shuffle(self):
        try:
            probabilities = [binom(self.deck[k], 1) / binom(self.cards_remaining, 1) for k in self.deck.keys() if
                             self.deck[k] > 0]
            _choices = [k for k in self.deck.keys() if self.deck[k] > 0]
            card = choice(a=_choices, p=probabilities)
            if self.deck[card] > 0:
                self.deck.update({card: self.deck[card] - 1})
                suit = self.available_suit(card=card)
                self.cards_remaining -= 1
                return '{} {}'.format(card, suit)
        except Exception as e:
            print(e.args)

    def available_suit(self, card=None):
        try:
            _items = [suit for suit in self.deck_array.columns if self.suits_remaining[suit] > 0
                      and self.deck_array.loc[card][suit] < self.numDecks]
            _cards_remaining = sum([self.suits_remaining[key] for key in self.suits_remaining.keys() if key in _items])
            _suit_probability = [(binom(self.suits_remaining[key], 1) / binom(_cards_remaining, 1)) for
                                 key in self.suits_remaining.keys() if self.suits_remaining[key] > 0 and key in _items]
            suit = choice(a=_items, p=_suit_probability)
            if self.deck_array.loc[card][suit] < self.numDecks:
                self.deck_array.loc[card][suit] += 1
                self.suits_remaining[suit] -= 1
                return suit
        except Exception as e:
            print(e.__repr__())


if __name__ == '__main__':
    pass
