__package__ = 'game'

import sys

py_version = sys.version_info[:3]
if py_version >= (3, 0):
    import tkinter as tk
    import concurrent.futures as thread

if py_version <= (2, 7):
    import Tkinter as tk
    from multiprocessing.dummy import Process as thread


class DrawButton(tk.Button):

    def __init__(self, master=None, command=None):
        self.command = command
        # lambda: thread(self.command, args=()).start
        super(DrawButton, self).__init__(master=master, command=None)

    def new_game(self):
        pass

    def exit_game(self):
        pass


class TurnActions(object):

    def __init__(self):
        super(TurnActions, self).__init__()

    def hit(self):
        pass

    def stay(self):
        pass

    def surrender(self):
        pass


