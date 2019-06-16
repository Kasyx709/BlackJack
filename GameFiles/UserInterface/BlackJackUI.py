from __future__ import division

from . import tk
from . import tkFont
from . import BlackJackWindows
from . import SelectGameType
from . import Helpers


class BlackJackUI(object):

    def __init__(self):
        super().__init__()
        self.root = tk.Tk()
        self.root.font = tkFont.Font(family='Garamond', size=16, weight='bold')
        self.root.option_add("*Font", self.root.font)
        self.root.wm_minsize(1058, 650)
        self.root.wm_resizable(width=1, height=1)
        self.root.wm_title('BlackJack - 2019')
        self.root.overrideredirect(True)
        self.root.geometry("+250+250")
        self.root.wm_attributes("-topmost", True)
        self.root.configure(background='Green')
        self.root.withdraw()
        SelectGameType(parent=BlackJackWindows(self.root))
        self.root.bind("<ButtonPress-1>", lambda event: Helpers.start_xy(event, self.root))
        self.root.bind("<ButtonRelease-1>", lambda event: Helpers.stop_xy(event, self.root))
        self.root.bind("<B1-Motion>", lambda event: Helpers.configure_xy(event, self.root))
        self.root.mainloop()
