__package__ = 'GameFiles'
from PIL import ImageTk
from PIL import Image
import cv2
import sys

py_version = sys.version_info[:3]
if py_version >= (3, 0):
    import tkinter as tk
    from tkinter import font as tkFont
    import concurrent.futures as thread

if py_version <= (2, 7):
    import Tkinter as tk
    import tkFont
    from multiprocessing.dummy import Process as thread


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
    def go_back(back_button, next_button, widgets):
        if back_button['text'] == 'No':
            back_button['text'] = 'Back'
            next_button['text'] = 'Next'
        for widget in widgets:
            if widget.name is 'name_label':
                widget['text'] = 'Player Name:'
            elif widget.name is 'chosen_name':
                widget['text'] = ''
            elif widget.name is 'name_text':
                widget.delete(0, 'end')

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
        self.multiplayer = multiplayer
        self.parent = parent
        super().__init__(master=parent)
        self.numPlayers = 1
        original_image = cv2.imread('GameFiles/Images/LoginScreen.png')
        b, g, r = cv2.split(original_image)
        self.colorCorrected = cv2.merge((r, g, b))
        self.bgImage = Image.fromarray(self.colorCorrected)
        self.imageTk = ImageTk.PhotoImage(image=self.bgImage)
        self.menu = self.menu()
        self.bind('<Configure>', lambda event: Helpers.resize_image(event, widget=self.menu))
        self.pack(fill=tk.BOTH, expand=True)

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

        def _check_name():
            import re
            name = re.sub(r"[^a-z]", ' ', re.escape(name_text.get()), flags=re.IGNORECASE)
            if name != r"":
                chosen_name['text'] = "\rYou've selected {}\r\nIs that correct?".format(name)
                next_button['text'] = 'Yes'
                back_button['text'] = 'No'
            else:
                name_label.place(relx=0.5, rely=0.35, anchor=tk.CENTER)
                name_label['fg'] = 'red'
                name_label['text'] = "Please select a valid name."
                name_text.delete(0, 'end')

        menu = tk.Label(self, image=self.imageTk)
        menu.name = 'player_screen'
        menu.image = self.imageTk
        Helpers.background_images[menu.name] = self.bgImage
        name_label = tk.Label(menu, text='Player Name:')
        name_label.name = 'name_label'
        name_label['fg'] = 'Green'
        name_label['bg'] = 'Black'
        chosen_name = tk.Label(menu, text='')
        chosen_name.name = 'chosen_name'
        name_text = tk.Entry(menu)
        name_text.name = 'name_text'
        back_button = tk.Button(menu, text="Back",
                                command=lambda: Helpers.go_back(back_button, next_button, [name_label, name_text]))
        next_button = tk.Button(menu, text="Next", command=_check_name)
        exit_button = tk.Button(menu, text="Exit", command=lambda: Helpers.close_window(self.parent))
        name_label.place(relx=0.41, rely=0.35, anchor=tk.CENTER)
        name_text.place(relx=0.5, rely=0.4, relwidth=.3, relheight=.05, anchor=tk.CENTER)
        chosen_name.place(relx=0.5, rely=0.51, anchor=tk.CENTER)
        back_button.place(relx=0.45, rely=0.9, anchor=tk.CENTER)
        next_button.place(relx=0.55, rely=0.9, anchor=tk.CENTER)
        exit_button.place(relx=0.05, rely=0.05, anchor=tk.CENTER)
        menu.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=tk.CENTER)
        return menu


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
