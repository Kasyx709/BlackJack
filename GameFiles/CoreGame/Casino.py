from GameFiles.CoreGame import MetaHouse


class House(metaclass=MetaHouse):
    players = {}
    """
    Readies a new game by asking players how many decks
    they'd like to use and how many players will be playing

    After selecting names and decks, draws cards for each player
    then pauses while players decide what they'd like to do next.

    """

    def __init__(self):
        self.numPlayers = 1
        self.numDecks = 1
        self.buildHouse()
        self.server.start()
        self.deck = None
        self.shoe = None

    def start_game(self):
        self.num_players()
        self.create_players()
        self.deck = self.makeDeck()
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
            print(self.players[i], self.players[i].points)

    def num_players(self):
        while 1:
            try:
                num_players = input("\rHow many players will be joining the game?\r\nThe Maximum number allowed is 7"
                                    "\r\nPlease select a number between 1 and 7 or press Enter to use the Default of 1:")
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

    def create_players(self):
        try:
            # id_key 0 will always be the dealer
            self.players[0] = self.makeDealer()
            for i in range(1, self.numPlayers + 1):
                name = self.create_player_name(id_key=i)
                player = self.makePlayer(name=name, port=self.port)
                self.players[i] = player
        except Exception as e:
            print(e.__repr__())

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
