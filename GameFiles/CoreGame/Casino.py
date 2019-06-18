from GameFiles.CoreGame import MetaHouse


class House(metaclass=MetaHouse):
    players = dict()
    player_selections = {
        'numPlayers': 0,
        'numDecks': 0
    }
    """
    Readies a new game by asking players how many decks
    they'd like to use and how many players will be playing

    After selecting names and decks, draws cards for each player
    then pauses while players decide what they'd like to do next.

    """

    def __init__(self):
        self.buildHouse()
        self.server.start()
        self.deck = None
        self.shoe = None

    def start_game(self):
        self.deck = self.makeDeck(num_decks=self.player_selections['numDecks'])
        self.shoe = self.load_shoe('localhost', self.port)
        self.shoe.connect()
        cards = self.shoe.cards()
        for i in range(self.deck.cards_remaining):
            card = self.deck.shuffle()
            cards.put(card)
        self.opening_deal(cards)

    def run(self):
        alive = True
        while 1:
            if alive:
                pass
            else:
                break

    def opening_deal(self, cards):
        for i in range(len(self.players.keys())):
            self.players[i].playerCards = cards.get(), cards.get()
            if i == 0:
                self.players[i].points = self.calc_points(self.players[i].playerCards, True)
            else:
                self.players[i].points = self.calc_points(self.players[i].playerCards)
            print('fff', self.players[i], self.players[i].points, self.players[i].playerCards)

    @staticmethod
    def create_player_name(id_key):
        import re
        while 1:
            name = re.sub(r"[^a-z]", '', re.escape(
                input("Hello Player {}, what would you like to be called?\r\nOnly alphabetical characters are allowed."
                      "\r\nName:".format(id_key))
            ), flags=re.IGNORECASE)
            if name != r"":
                return name
            else:
                print("Please select a valid name.")

    def test_game(self):
        self.start_game()
        self.shoe = self.load_shoe('localhost', self.port)
        self.shoe.connect()
        cards = self.shoe.cards()
        while 1:
            if cards.qsize() > 0:
                print(cards.qsize())
                cards.get()


if __name__ == '__main__':
    House().start_game()
