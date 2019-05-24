__package__ = 'BlackJack'

from multiprocessing.connection import Client
from multiprocessing.connection import Listener
from multiprocessing.managers import BaseManager
from multiprocessing.queues import JoinableQueue


class House(BaseManager):

    def __init__(self):
        pass


class Player(object):
    def __init__(self, name=None):
        self.name = name
        self.points = 0


    def player_turn(self):
        pass


class Dealer(object):
    def __init__(self, name=None):
        self.name = name
        self.points = 0

    def dealer_turn(self):
        if self.points > 16:
            pass
