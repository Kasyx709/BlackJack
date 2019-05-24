__package__ = 'BlackJack'
from BlackJack.CoreGame.deckmaker import BlackJack

import sys

py_version = sys.version_info[:3]
if py_version >= (3, 0):
    import tkinter as tk
    import concurrent.futures as thread

if py_version <= (2, 7):
    import Tkinter as tk
    from multiprocessing.dummy import Process as thread


class DrawButton(tk.Button):

    def __init__(self, master=None):
        super(DrawButton, self).__init__(master=master, command=self.draw_card)

    def draw_card(self):
        pass
