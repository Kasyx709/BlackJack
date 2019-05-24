__package__ = 'BlackJack'

from multiprocessing.connection import Client
from multiprocessing.connection import Listener
from multiprocessing.managers import BaseManager
from multiprocessing.queues import JoinableQueue


class House(BaseManager):

    def __init__(self):
        pass


class Player(object):

    def __init__(self, address=None, name=None):
        self.address = ("localhost", 8000) if not address else (r"{}".format(address), 8000)
        self.pname = name
        super(Player, self).__init__()
        self.client = Client(address=self.address, authkey=self.pname)
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


player = Player(name='Mr Taco')
print(player.name)
