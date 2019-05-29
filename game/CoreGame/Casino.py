from game.CoreGame import Deck
import os
import re


class House(object):
    """
    Readies a new game by asking players how many decks
    they'd like to use and how many players will be playing

    After selecting names and decks, draws cards for each player
    then pauses while players decide what they'd like to do next.

    """

    def __init__(self):
        self.numPlayers = 1
        self.numDecks = 1
        self.create_players()

    def num_players(self):
        while 1:
            try:
                num_players = input("'How many players will be joining the game?\nThe Maximum number allowed is 7"
                                    "\nPlease select a number between 1 and 7 or press Enter to use the Default of 1:")
                if num_players == '':
                    return
                elif 0 < int(num_players) <= 7:
                    self.numPlayers = int(num_players)
                    return
                else:
                    print("You've selected an invalid number of players, please try again.")
                    continue
            except ValueError:
                print("That's not a valid number, please try again")

    def num_decks(self):
        while 1:
            try:
                num_decks = input("'How many Decks would you like to use?\nThe Default is 1 and Maximum allowed is 8"
                                  "\nPlease select a number between 1 and 8 or press Enter to use the Default of 1:")
                if num_decks == '':
                    return
                if 0 < int(num_decks) <= 8:
                    self.numDecks = int(num_decks)
                    return
                else:
                    print(r"You've selected an invalid number, please try again.")
                    continue
            except ValueError:
                print(r"That's not a valid number, please try again")

    def create_players(self):
        try:
            if self.numPlayers is 1:
                name = re.sub(r"[^a-z]", '', re.escape(
                    input("Hello Player {}, what would you like to be called?\nName:".format(self.numPlayers))
                ), flags=re.IGNORECASE)
                name = ''  # set name to player id text box and ask if it's ok using tkm yes no cancel


        except Exception:
            pass


class Player(object):

    def __init__(self, name=None, _identifier=1):
        self.playerID = r'{}'.format(name)
        self.playerID = _identifier
        self.points = 0
        super(Player, self).__init__()

    def player_turn(self):
        pass


class Dealer(object):
    def __init__(self):
        self.points = 0
        super(Dealer, self).__init__()

    def dealer_turn(self):
        if self.points > 16:
            pass


if __name__ == '__main__':
    House()
