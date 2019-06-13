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


class LoginScreen(tk.Canvas):

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
                              command=lambda: PlayerScreen(Helpers.open_window(self.parent)))
        mp_button = tk.Button(menu, text="MultiPlayer",
                              command=lambda: PlayerScreen(Helpers.open_window(self.parent)))
        exit_button = tk.Button(menu, text="Exit", command=lambda: Helpers.close_window(self.parent))
        sp_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        mp_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        exit_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
        menu.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=tk.CENTER)
        return menu


class PlayerScreen(tk.Canvas):

    def __init__(self, parent, multiplayer=False):
        super().__init__(master=parent)
        self.multiplayer = multiplayer
        self.parent = parent
        self.numPlayers = 1
        self.numDecks = 1
        original_image = cv2.imread('GameFiles/Images/LoginScreen.png')
        b, g, r = cv2.split(original_image)
        self.colorCorrected = cv2.merge((r, g, b))
        self.bgImage = Image.fromarray(self.colorCorrected)
        self.imageTk = ImageTk.PhotoImage(image=self.bgImage)
        self.menu = self.menu()
        self.bind('<Configure>', lambda event: Helpers.resize_image(event, widget=self.menu))
        self.name_label = tk.Label(self.menu, text='Player Name:')
        self.name_label.name = 'name_label'
        self.name_label['fg'] = 'Green'
        self.name_label['bg'] = 'Black'
        self.name_label.place(relx=0.41, rely=0.35, anchor=tk.CENTER)
        self.chosen_name = tk.Label(self.menu, text='')
        self.chosen_name.name = 'chosen_name'
        self.chosen_name.place(relx=0.5, rely=0.51, anchor=tk.CENTER)
        self.selection_text = tk.Entry(self.menu)
        self.selection_text.name = 'selection_text'
        self.selection_text.place(relx=0.5, rely=0.4, relwidth=.3, relheight=.05, anchor=tk.CENTER)
        self.back_button = tk.Button(self.menu, text="Back",
                                     command=lambda: self.go_back([self.name_label, self.selection_text]))
        self.back_button.place(relx=0.45, rely=0.9, anchor=tk.CENTER)
        self.next_button = tk.Button(self.menu, text="Next", command=self.set_name)
        self.next_button.place(relx=0.55, rely=0.9, anchor=tk.CENTER)
        self.exit_button = tk.Button(self.menu, text="Exit", command=lambda: Helpers.close_window(self.parent))
        self.exit_button.place(relx=0.05, rely=0.05, anchor=tk.CENTER)
        self.pack(fill=tk.BOTH, expand=True)
        self.back_button = None

    def go_back(self, widgets):
        if self.back_button['text'] == 'No':
            self.back_button['text'] = 'Back'
            self.next_button['text'] = 'Next'
        for widget in widgets:
            if widget.name is 'name_label':
                widget['text'] = 'Player Name:'
            elif widget.name is 'chosen_name':
                widget['text'] = ''
            elif widget.name is 'name_text':
                widget.delete(0, 'end')

    def mp(self):
        try:
            num_players = tk.Label(self)
            if num_players == '':
                return
            elif 0 < int(num_players) <= 7:
                self.numPlayers = int(num_players)
                return
            else:
                print("You've selected an invalid number of players, please try again.")

        except ValueError:
            print("That's not a valid number, please try again")

    def menu(self):
        menu = tk.Label(self, image=self.imageTk)
        menu.name = 'player_screen'
        menu.image = self.imageTk
        Helpers.background_images[menu.name] = self.bgImage
        menu.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=tk.CENTER)
        return menu

    def set_name(self):
        name = re.sub(r"[^a-z]", ' ', re.escape(self.selection_text.get()), flags=re.IGNORECASE)
        if name != r"":
            self.chosen_name['text'] = "\rYou've selected {}\r\nIs that correct?".format(name)
            self.next_button['text'] = 'Yes'
            self.back_button['text'] = 'No'
            self.next_button['command'] = self.verify_name

        else:
            self.name_label.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
            self.name_label['fg'] = 'red'
            self.name_label['text'] = "Please select a valid name."
            self.selection_text.delete(0, 'end')

    def num_decks(self):
        if self.next_button['text'] == 'Yes':
            self.selection_text.delete(0, 'end')
            self.next_button['text'] = 'Ok'

        if self.next_button['text'] == 'Ok':
            self.chosen_name['text'] = "How many Decks would you like to use?" \
                                       "\nThe Default is 1 and Maximum allowed is 8" \
                                       "\n Please select a number between 1 and 8 or press Enter to use the Default of 1"

            i = re.sub(r'[^0-9]', self.selection_text.get(), '')
            while 1:
                if i is '':
                    i = 1
                elif 0 <= int(i) <= 8:
                    self.numDecks = int(i)
                    self.chosen_name['text'] = "\rYou've selected {}\nIs that correct?".format(self.numDecks)
                    self.next_button['command'] = self.verify_decks
                    break
                else:
                    self.chosen_name['text'] = r"You've selected an invalid number, please try again."

    def verify_decks(self):
        house.numDecks = self.numDecks
        return

    def verify_name(self):
        house.numPlayers = self.numPlayers
        self.chosen_name['text'] = "How many Decks would you like to use?" \
                                   "\nThe Default is 1 and Maximum allowed is 8" \
                                   "\n Please select a number between 1 and 8 or press Enter to use the Default of 1"
        self.next_button['command'] = self.num_decks


def show_card(master_window, player=None, suit=None, cardtype=None):
    # card_image = ImageTk.PhotoImage(Image.open())
    cv_image = cv2.imread('GameFiles/CardSets/color_cards.png')
    # (1600, 650) Image Size
    # Each Card = + 127 x 90 with 2 pixels space between on each side
    # Math for x values = prev value + 132
    # Math for y values = prev value + 94
    card_y1 = 0
    card_y2 = 90
    cards = {
        'spades': cv_image[0:127, card_y1: card_y2],
        'hearts': cv_image[130: 256, 94: 184],
        'clubs': cv_image[262: 385, card_y1: card_y2],
        'diamonds': cv_image[394: 514, card_y1: card_y2],
    }
    # card_set = cards[row]
    card_set = cards['spades']
    _card_set = cards['hearts']
    __card_set = cards['clubs']
    ___card_set = cards['diamonds']

    height, width, no_channels = card_set.shape
    height2, width2, no_channels = _card_set.shape
    height3, width3, no_channels = __card_set.shape
    height4, width4, no_channels = ___card_set.shape

    canvas = tk.Canvas(master=master_window, width=width, height=height)
    _canvas = tk.Canvas(master=master_window, width=width2, height=height2)
    __canvas = tk.Canvas(master=master_window, width=width3, height=height3)
    ___canvas = tk.Canvas(master=master_window, width=width4, height=height4)

    if player:
        canvas_x = 10
        canvas_y = 455
    else:
        canvas_x = 935
        canvas_y = 485
    canvas.place(x=10, y=465)
    _canvas.place(x=25, y=475)
    __canvas.place(x=40, y=485)
    ___canvas.place(x=55, y=495)
    ___canvas.place(x=55, y=495)

    card = ImageTk.PhotoImage(image=Image.fromarray(card_set))
    _card = ImageTk.PhotoImage(image=Image.fromarray(_card_set))
    __card = ImageTk.PhotoImage(image=Image.fromarray(__card_set))
    ___card = ImageTk.PhotoImage(image=Image.fromarray(___card_set))

    card.image = card
    _card.image = _card
    __card.image = __card
    ___card.image = ___card

    canvas.create_image(0, 0, image=card, anchor=tk.NW)
    _canvas.create_image(0, 0, image=_card, anchor=tk.NW)
    __canvas.create_image(0, 0, image=__card, anchor=tk.NW)
    ___canvas.create_image(0, 0, image=___card, anchor=tk.NW)
    return canvas


class GameTable(tk.Canvas):

    def __init__(self):
        super(GameTable, self).__init__()
        self.bg_image = tk.PhotoImage(file='GameFiles/Images/GameTable.png')
        self.image = self.bg_image
        self.create_image(1, 1, image=self.bg_image, anchor=tk.NW)
        hit = tk.Button(master=self, text='Hit', command=None).pack()
        stand = tk.Button(master=self, text='Stand', command=None).pack()
        self.create_window(50, 50, hit)
        self.create_window(50, 50, stand)

    def get_name(self, player_id=None):
        frame = tk.Frame(master=self)
        label = tk.Label(master=frame, text="Player {}:".format(player_id))
        player_name = tk.Entry(master=self)
        button = tk.Button(master=self, text="Enter", command=None)
        label.grid(row=0)
        player_name.grid(row=0)
        button.grid(columnspan=2)
        return
