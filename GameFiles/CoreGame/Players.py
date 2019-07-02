import os
from multiprocessing.managers import BaseManager


class Player(BaseManager):

    def __init__(self, player_id, name, port, authkey):
        super(Player, self).__init__(address=('localhost', port), authkey=authkey)
        self.register('cards')
        self.playerID = player_id
        self.playerName = r'{}'.format(name)
        self.playerKey = os.urandom(50)
        self.cards = {}
        self.points = 0



class Dealer(BaseManager):

    def __init__(self, player_id, port, authkey):
        super(Dealer, self).__init__(address=('localhost', port), authkey=authkey)
        self.register('cards')
        self.playerID = player_id
        self.points = 0
        self.dealerKey = os.urandom(256)
        self.dealerCards = dict()
