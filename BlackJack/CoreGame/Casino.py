from BlackJack.CoreGame import MetaHouse


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
        self.gameTable = None

    def start_game(self, game_table):
        self.gameTable = game_table
        self.deck = self.makeDeck(num_decks=self.player_selections['numDecks'])
        self.shoe = self.load_shoe('localhost', self.port)
        self.shoe.connect()
        shoe = self.shoe.cards()
        for i in range(self.deck.cards_remaining):
            card = self.deck.shuffle()
            shoe.put(card)
        self.opening_deal(shoe)

    def opening_deal(self, cards):
        for i in self.players.keys():
            self.players[i].cards = cards.get(), cards.get()
            self.players[i].points = self.calc_points(self.players[i].cards)
            if i is 0:
                self.gameTable.dealer_points['text'] = 'House = {}'.format(self.players[i].points)
            else:
                self.gameTable.player_points['text'] = '{} = {}'.format(self.players[i].playerName,
                                                                        self.players[i].points)
        self.show_cards(self.gameTable, self.players)
        self.player_turn(self.gameTable, self.players, cards)
