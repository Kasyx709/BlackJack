from __future__ import division

from . import tk

from PIL import ImageTk
from PIL import Image
import cv2


class BlackJackUI(tk.Tk):

    def __init__(self):
        super(BlackJackUI, self).__init__()
        self.wm_minsize(1058, 650)
        self.wm_resizable(width=1, height=1)
        self.wm_title('BlackJack - 2019')
        self.configure(background='Green')
        self.canvas = self.canvas(self)
        self.show_card(self.canvas)
        self.mainloop()

    def canvas(self, master_window):
        bg_image = tk.PhotoImage(file='BlackJack/UserInterface/blackjacktable.png')
        canvas = tk.Canvas(master=master_window)
        canvas.image = bg_image
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_image(1, 1, image=bg_image, anchor=tk.NW)
        return canvas

    @staticmethod
    def show_card(master_window, player=None, suit=None, cardtype=None):
        # card_image = ImageTk.PhotoImage(Image.open())
        cv_image = cv2.imread('BlackJack/CardSets/color_cards.png')
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


if __name__ == '__main__':
    ui = BlackJackUI()
