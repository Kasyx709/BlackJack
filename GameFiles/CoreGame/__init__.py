import os
from numpy.random import choice
from scipy.special import binom
from pandas import DataFrame

from multiprocessing import JoinableQueue as jQueue
from multiprocessing.dummy import Process as Thread
from multiprocessing.managers import BaseManager
import cv2
import tkinter as tk
from PIL import ImageTk
from PIL import Image


class MetaHouse(type):
    _instances = {}
    token = os.urandom(256)

    def __new__(mcs, names, bases, m_dict={}, **kwargs):
        _house = super().__new__(mcs, names, bases, m_dict)
        mcs.find_port(_house)
        setattr(_house, 'buildHouse', mcs.build_house)
        setattr(_house, 'token', mcs.token)
        setattr(_house, 'makeDeck', Deck)
        setattr(_house, 'shuffle', Deck.shuffle)
        setattr(_house, 'load_shoe', Deck.load_shoe)
        setattr(_house, 'calc_points', Deck.calc_points)
        setattr(_house, 'calc_ace', Deck.calc_ace)
        setattr(_house, 'show_cards', Deck.show_cards)
        setattr(_house, 'player_turn', Deck.player_turn)

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


class Deck(object):
    """
        Builds a deck using numpy arrays
        ace = Aces in the deck, can be worth 1 or 11 (player's choice or dealer algorithm)
        card_point_value_10 = 10, Jack, Queen, King (all worth 10 points)
        Numbered cards = Cards from 2-9 (worth their numbered value)
        Cards Remaining = Number of cards left to be dealt, starting value of 52
        Suits = Hearts, Clubs, Spades, Diamonds (Arbitrarily assigned on draw, but checks for duplicates)
        As a dict this also holds values for cards played/in play
    """
    card_types = [
        # Card Type
        'ace',
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        '10',
        'jack',
        'queen',
        'king',
    ]
    point_array = DataFrame(index=card_types, columns=['PointValues'])

    def __init__(self, num_decks):
        super(Deck, self).__init__()
        self.numDecks = num_decks
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
            if card == 'ace' and dealer:
                points = points + cls.calc_ace(points)
            elif card == 'ace' and not dealer:
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

    @classmethod
    def show_cards(self, game_table, players):
        """
        Uses an image map to select x,y coordinates indicating card location then displays the card onto the gametable.
        If the card image used follows the example pattern of Spades, Hearts, Clubs, Diamonds and Ace through King
        then the formula will not require modification.
         Card map image size 1312 x 559 (13 cards with 1 pixel space between and 4 suits with 1 pixel space in between)
         Card Size = 100 x 139
         Math for y values = prev value + 132
         Math for x values = prev value + 94
        :param game_table:
        :param players:
        :return:
        """

        try:
            for frame in game_table.winfo_children():
                if isinstance(frame, tk.Canvas):
                    frame.destroy()
            for i in players.keys():
                canvas_x = 15
                anchor = tk.SW
                side = tk.LEFT
                if i is 0:
                    canvas_x = 1175
                    side = tk.RIGHT
                    anchor = tk.SE
                for card in players[i].cards:
                    card_index, suit = card.split()
                    card_image, height, width = Deck.find_card(card_index, suit)
                    canvas = tk.Canvas(master=game_table,
                                       width=width, height=height,
                                       bd=0, highlightthickness=0,
                                       relief='ridge')
                    canvas.create_image(0, 0, image=card_image, anchor=tk.NW)
                    canvas.pack(anchor=anchor, side=side)
                    if i is 0:
                        canvas_x -= 35
                    else:
                        canvas_x += 35
        except Exception as e:
            raise e

    @classmethod
    def find_card(cls, card_index, suit):
        cv_image = cv2.imread('GameFiles/CardSets/Color_52_Faces.png')
        b, g, r = cv2.split(cv_image)
        color_correct = cv2.merge((r, g, b))
        face_cards = {
            'ace': 1,
            'jack': 10,
            'queen': 11,
            'king': 12
        }
        if card_index not in face_cards:
            card_index = int(card_index)
        else:
            card_index = face_cards[card_index]
        upper_left = 101 * (card_index - 1)
        upper_right = (101 * card_index) - 1
        if card_index == 1:
            upper_right = 100 * card_index
        lower_left = 140
        card_rows = {
            'Clubs': color_correct[0: lower_left, upper_left: upper_right],
            'Hearts': color_correct[140: lower_left * 2, upper_left: upper_right],
            'Spades': color_correct[280: lower_left * 3, upper_left: upper_right],
            'Diamonds': color_correct[420: lower_left * 4, upper_left: upper_right],
        }
        card_set = card_rows[suit]
        card_image = ImageTk.PhotoImage(image=Image.fromarray(card_set))
        card_image.image = card_image
        height, width, no_channels = card_set.shape
        return card_image, height, width

    def player_turn(self, game_table, players, shoe):
        player = players[1]
        dealer = players[0]

        def _dealer_turn():
            if player.points > 21:
                return
            elif dealer.points <= 16:
                dealer.cards = *dealer.cards, shoe.get()
                dealer.points = Deck.calc_points(dealer.cards)

        def _hit():
            if dealer.points >= 21:
                return
            elif player.points < 21:
                player.cards = *player.cards, shoe.get()
                player.points = Deck.calc_points(player.cards)
                _dealer_turn()
                check_points()
                Deck.show_cards(game_table, players)
            return

        def _stand():
            _dealer_turn()
            check_points()
            Deck.show_cards(game_table, players)

        hit = tk.Button(master=game_table, text='Hit', command=_hit)
        hit.place(relx=0.015, rely=.55)
        stand = tk.Button(master=game_table, text='Stand', command=_stand)
        stand.place(relx=0.055, rely=.55)

        def check_points():
            if player.points > 21:
                game_table.player_points['text'] = 'The House wins! Your Points - {}'.format(player.points)
            elif player.points is 21:
                if dealer.points is 21:
                    game_table.player_points['text'] = 'BlackJack Tie - Nobody wins'
                    game_table.dealer_points['text'] = 'BlackJack Tie - Nobody wins'
                else:
                    game_table.player_points['text'] = 'BlackJack - You win!'
            elif player.points < 21 and dealer.points is 21:
                game_table.dealer_points['text'] = 'BlackJack - The House wins'
            else:
                if dealer.points > 21:
                    game_table.dealer_points['text'] = 'The House Busted! House - {}'.format(dealer.points)
                else:
                    game_table.dealer_points['text'] = 'House = {}'.format(dealer.points)
                game_table.player_points['text'] = 'Player = {}'.format(player.points)
