__package__ = 'GameFiles'
from PIL import ImageTk
from PIL import Image
import cv2
import sys
import re

py_version = sys.version_info[:3]
if py_version >= (3, 0):
    import tkinter as tk
    from tkinter import font as tkFont
    import concurrent.futures as thread

if py_version <= (2, 7):
    import Tkinter as tk
    import tkFont
    from multiprocessing.dummy import Process as thread

from GameFiles.CoreGame.Casino import House
from GameFiles.CoreGame.Players import Player, Dealer

house = House()


# Helper Functions placed into a class for lazy importing

class Helpers:
    background_images = {}

    @staticmethod
    def open_window(parent):
        parent.withdraw()
        new_window = BlackJackWindows(parent)
        return new_window

    @staticmethod
    def close_window(window):
        window.protocol("WM_DELETE_WINDOW")
        window.destroy()

    @staticmethod
    def resize_image(event, widget):
        _x = event.width
        _y = event.height
        image = Helpers.background_images[widget.name]
        resize = image.resize((_x, _y))
        _image = ImageTk.PhotoImage(image=resize)
        widget.image = _image
        widget.configure(image=_image)

    @staticmethod
    def start_xy(event, widget):
        widget.x = event.x
        widget.y = event.y

    @staticmethod
    def stop_xy(event, widget):
        widget.x = None
        widget.y = None

    @staticmethod
    def configure_xy(event, widget):
        x = widget.winfo_x() + (event.x - widget.x)
        y = widget.winfo_y() + (event.y - widget.y)
        widget.geometry("+%s+%s" % (x, y))


class BlackJackWindows(tk.Toplevel):

    def __init__(self, parent):
        self.__doc__ = tk.Toplevel.__init__.__doc__
        super().__init__(master=parent)
        width, height = parent.wm_minsize()
        self.wm_minsize(width, height)
        self.overrideredirect(True)
        self.geometry("+250+250")
        self.wm_attributes("-topmost", True)
        self.configure(background='Green')
        self.bind("<ButtonPress-1>", lambda event: Helpers.start_xy(event, self))
        self.bind("<ButtonRelease-1>", lambda event: Helpers.stop_xy(event, self))
        self.bind("<B1-Motion>", lambda event: Helpers.configure_xy(event, self))


class BlackJackLabelWidget(tk.Label):
    label_widgets = {}

    def __init__(self, parent, relx, rely, cnf={}, **kwargs):
        self.__doc__ = tk.Label.__init__.__doc__

        super(BlackJackLabelWidget, self).__init__(parent, cnf=cnf, **kwargs)
        self.place(relx=relx, rely=rely, anchor=tk.CENTER)


class BlackJackEntryWidget(tk.Entry):
    entry_widgets = {}

    def __init__(self, parent, relx, rely, relwidth, relheight, cnf={}, **kwargs):
        self.__doc__ = tk.Entry.__init__.__doc__
        super().__init__(master=parent, cnf={}, **kwargs)
        self.place(relx=0.5, rely=0.5, relwidth=relwidth, relheight=relheight, anchor=tk.CENTER)


class BlackJackButtons(tk.Button):
    buttons = {}

    def __init__(self, parent, relx, rely, cnf={}, **kwargs):
        self.__doc__ = tk.Button.__init__.__doc__
        super().__init__(master=parent, cnf=cnf, **kwargs)
        self.place(relx=relx, rely=rely, anchor=tk.CENTER)
        self.parentCommand = None
        self.parent = parent


class SelectGameType(tk.Canvas):

    def __init__(self, parent):
        self.parent = parent
        super().__init__(master=parent)
        original_image = cv2.imread('GameFiles/Images/LoginScreen.png')
        b, g, r = cv2.split(original_image)
        self.colorCorrected = cv2.merge((r, g, b))
        self.bgImage = Image.fromarray(self.colorCorrected)
        self.imageTk = ImageTk.PhotoImage(image=self.bgImage)
        self.menu = self.menu()
        self.bind('<Configure>', lambda event: Helpers.resize_image(event, widget=self.menu))
        self.pack(fill=tk.BOTH, expand=True)

    def menu(self):
        menu = tk.Label(self, image=self.imageTk)
        menu.name = 'login_screen'
        menu.image = self.imageTk
        Helpers.background_images[menu.name] = self.bgImage
        sp_button = tk.Button(menu, text="Single Player",
                              command=lambda: SelectPlayers(Helpers.open_window(self.parent)))
        mp_button = tk.Button(menu, text="MultiPlayer",
                              command=lambda: SelectPlayers(Helpers.open_window(self.parent), mp=True))
        exit_button = tk.Button(menu, text="Exit", command=lambda: Helpers.close_window(self.parent))
        sp_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        mp_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        exit_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
        menu.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=tk.CENTER)
        return menu


class SelectPlayers(tk.Canvas):

    def __init__(self, parent, mp=False):
        super().__init__(master=parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.bg = BlackJackLabelWidget(self, 0.5, 0.5)
        self.bg.name = 'select_players'
        self.parent = parent
        original_image = cv2.imread('GameFiles/Images/LoginScreen.png')
        b, g, r = cv2.split(original_image)
        self.colorCorrected = cv2.merge((r, g, b))
        self.bgImage = Image.fromarray(self.colorCorrected)
        self.imageTk = ImageTk.PhotoImage(image=self.bgImage)
        self.bg.image = self.imageTk
        Helpers.background_images[self.bg.name] = self.bgImage
        self.bind('<Configure>', lambda event: Helpers.resize_image(event, widget=self.bg))
        self.text_label = BlackJackLabelWidget(self, 0.41, 0.35, text='')
        self.notification = BlackJackLabelWidget(self, 0.5, 0.6)
        self.player_text = BlackJackEntryWidget(self, 0.5, 0.4, 0.3, 0.05, text='')
        self.yes_next = BlackJackButtons(self, 0.55, 0.9, text='Next', command=self._set_name)
        self.yes_next.parentCommand = self.welcome_player
        self.no_back = BlackJackButtons(self, 0.45, 0.9, text='Back', command=self._no_back)
        self.exit_button = BlackJackButtons(self, 0.05, 0.05, text="Exit",
                                            command=lambda: Helpers.close_window(self.parent))

        self.mp = mp
        house.player_selections['numPlayers']
        self.playerNames = dict()
        self.currentID = 1
        if self.mp is True:
            _choose_numbers(self.text_label, self.notification, self.player_text,
                            self.yes_next, self.no_back,
                            'numPlayers')
        else:
            house.player_selections['numPlayers'] = 1
            self.currentID = 1
            self.welcome_player()

    def welcome_player(self):
        self.yes_next['command'] = self._set_name
        self.text_label['text'] = 'Player Name:'
        self.notification['text'] = "Welcome Player {}!" \
                                    "\nPlease choose a name".format(self.currentID)

    def _set_name(self):
        name = re.sub(r"[^a-z]", '', re.escape(self.player_text.get()), flags=re.IGNORECASE)
        if name != r'':
            self.notification['fg'] = 'black'
            self.notification['text'] = "You've selected {}\nIs that correct?".format(name)
            self.yes_next['command'] = lambda: self._confirm_name(name)
        else:
            self.notification['text'] = "Please select a valid name."
            self.notification['fg'] = 'Red'

    def _confirm_name(self, name):
        self.player_text.delete(0, 'end')
        if len(name) <= 50:
            self.get_id(name)
        else:
            self.notification['text'] = "Name exceeds 50 characters\nPlease select a valid name."
            self.notification['fg'] = 'Red'
            self.yes_next['command'] = self._set_name

    def get_id(self, name):
        try:
            self.notification['text'] = ''
            _id = next(
                i for i in range(1, house.player_selections['numPlayers'] + 1) if i not in self.playerNames.keys())
            self.playerNames[_id] = name
            if len(self.playerNames.keys()) == house.player_selections['numPlayers']:
                self.create_players()
            else:
                self.currentID = _id + 1
                self.yes_next['command'] = self._set_name
                self.text_label['text'] = 'Player Name:'
                self.notification['text'] = "Welcome Player {}!" \
                                            "\nPlease choose a name".format(self.currentID)
        except StopIteration:
            pass

    def _no_back(self, *event):
        self.welcome_player()

    def create_players(self):
        try:
            # id_key 0 will always be the dealer
            self.playerNames[0] = 'Dealer'
            for i, name in self.playerNames.items():
                if i is 0:
                    house.players[0] = Dealer(player_id=0, port=house.port, authkey=house.token)
                else:
                    house.players[i] = Player(player_id=i, name=name, port=house.port, authkey=house.token)
            self.destroy()
            SelectDecks(self.parent)
        except Exception as e:
            print(e.__repr__())


class SelectDecks(tk.Canvas):

    def __init__(self, parent):
        super().__init__(master=parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.bg = BlackJackLabelWidget(self, 0.5, 0.5)
        self.bg.name = 'select_decks'
        self.parent = parent
        original_image = cv2.imread('GameFiles/Images/LoginScreen.png')
        b, g, r = cv2.split(original_image)
        self.colorCorrected = cv2.merge((r, g, b))
        self.bgImage = Image.fromarray(self.colorCorrected)
        self.imageTk = ImageTk.PhotoImage(image=self.bgImage)
        self.bg.image = self.imageTk
        Helpers.background_images[self.bg.name] = self.bgImage
        self.bind('<Configure>', lambda event: Helpers.resize_image(event, widget=self.bg))
        self.text_label = BlackJackLabelWidget(self, 0.41, 0.35, text='')
        self.notification = BlackJackLabelWidget(self, 0.5, 0.6)
        self.player_text = BlackJackEntryWidget(self, 0.5, 0.4, 0.3, 0.05, text='')
        self.yes_next = BlackJackButtons(self, 0.55, 0.9, text='Next', command=None)
        self.no_back = BlackJackButtons(self, 0.45, 0.9, text='Back', command=self._no_back)
        self.exit_button = BlackJackButtons(self, 0.05, 0.05, text="Exit",
                                            command=lambda: Helpers.close_window(self.parent))
        _choose_numbers(self.text_label, self.notification, self.player_text, self.yes_next, self.no_back, 'numDecks')
        self.yes_next.parentCommand = self.start_game

    def start_game(self):
        self.destroy()
        house.start_game(GameTable(self.parent))

    def _no_back(self, *event):
        pass


class GameTable(tk.Canvas):

    def __init__(self, parent):
        super().__init__(master=parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.bg = BlackJackLabelWidget(self, 0.5, 0.5)
        self.bg.name = 'game_table'
        original_image = cv2.imread('GameFiles/Images/GameTable.png')
        b, g, r = cv2.split(original_image)
        self.colorCorrected = cv2.merge((r, g, b))
        self.bgImage = Image.fromarray(self.colorCorrected)
        self.imageTk = ImageTk.PhotoImage(image=self.bgImage)
        self.bg.image = self.imageTk
        Helpers.background_images[self.bg.name] = self.bgImage
        self.bind('<Configure>', lambda event: Helpers.resize_image(event, widget=self.bg))

    def show_card(self, player):
        # card_image = ImageTk.PhotoImage(Image.open())
        cv_image = cv2.imread('GameFiles/CardSets/color_cards.png')
        b, g, r = cv2.split(cv_image)
        colorCorrected = cv2.merge((r, g, b))
        # (1600, 650) Image Size
        # Each Card = + 127 x 90 with 2 pixels space between on each side
        # Math for x values = prev value + 132
        # Math for y values = prev value + 94
        face_cards = {
            'ace': 1,
            'jack': 10,
            'queen': 11,
            'king': 12
        }
        for i in player.cards:
            card, suit = i.split()
            if card not in face_cards:
                card = int(card)
            else:
                card = face_cards[card]
            card_x = (127 * (card)) + 132
            card_y = (90 * (card)) + 90
            print(card, suit)

            card_rows = {
                'Clubs': colorCorrected[0: 132, card_x:card_y],
                'Hearts': colorCorrected[130: 256, card_x:card_y],
                'Spades': colorCorrected[262: 385, card_x:card_y],
                'Diamonds': colorCorrected[394: 514, card_x:card_y],
            }
            card_rows = {
                'Spades': colorCorrected[0: 132, card_y: card_x],
                'Hearts': colorCorrected[130: 256, card_y: card_x],
                'Clubs': colorCorrected[262: 385, card_y: card_x],
                'Diamonds': colorCorrected[394: 514, card_y: card_x],
            }
            card_set = card_rows[suit]
            height, width, no_channels = card_set.shape
            print(height, width)
            canvas = tk.Canvas(master=self, width=width, height=height)
            canvas.place(x=10, y=465)
            _card = ImageTk.PhotoImage(image=Image.fromarray(card_set))
            _card.image = _card
            canvas.create_image(0, 0, image=_card, anchor=tk.NW)

        # card_set = cards[row]

        return canvas


def _choose_numbers(label_widget, notification_widget, text_widget, yes_next_button, no_back_button, selection_text):
    def __set_numbers(player_selection):
        house.player_selections[selection_text] = player_selection
        yes_next_button.parentCommand()

    def __confirm_numbers():
        player_selection = re.sub(r'\D', '', text_widget.get())
        if player_selection is '':
            player_selection = 1
        try:
            player_selection = int(player_selection)
            while 1:
                if 0 <= player_selection <= max_num:
                    notification_widget['fg'] = 'Black'
                    notification_widget['text'] = "You've selected {}\nIs that correct?".format(int(player_selection))
                    yes_next_button['command'] = lambda: __set_numbers(player_selection)
                    break
                else:
                    text_widget.delete(0, 'end')
                    notification_widget['fg'] = 'Red'
                    notification_widget['text'] = r"You've selected an invalid number, please try again."
                    break
        except ValueError:
            text_widget.delete(0, 'end')
            notification_widget['fg'] = 'Red'
            notification_widget['text'] = r"You've selected an invalid number, please try again."
            return

    if selection_text == 'numPlayers':
        label_widget['text'] = 'Players'
        max_num = 7
    elif selection_text == 'numDecks':
        label_widget['text'] = 'Decks'
        max_num = 8
    text_widget.delete(0, 'end')
    notification_widget['text'] = (
        "How many {0} will there be?\nThe Default is 1 and Maximum allowed is {1}"
        "\n Please select a number between 1 and {1} or press Next to use the Default of 1".format(
            label_widget['text'], max_num
        )
    )
    yes_next_button['command'] = lambda: __confirm_numbers()


PlayerSelections = {
    'numPlayers': 0,
    'numDecks': 0
}
