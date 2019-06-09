self.buttonOriginal = cv2.imread('game/Images/TransparentButton.png')
        b, g, r = cv2.split(self.buttonOriginal)
        buttonImage = cv2.merge((r, g, b))
        _buttonImage = Image.fromarray(buttonImage)
        self.buttonImage = ImageTk.PhotoImage(image=_buttonImage)

class __BlackJackWindows(tk.Toplevel):
    def __init__(self, master):
        super().__init__()
        self.withdraw()
        self.root = master
        self.canvas = tk.Canvas(master)
        self.bgImageOriginal = cv2.imread('game/Images/LoginScreen.png')
        b, g, r = cv2.split(self.bgImageOriginal)
        self.bgImage = cv2.merge((r, g, b))
        self.img = Image.fromarray(self.bgImage)
        self.imgTk = ImageTk.PhotoImage(image=self.img)
        self.background = tk.Label(master=self.canvas, image=self.imgTk)
        self.background.place(relx=0.5, rely=0.5, relwidth=1, relheight=1, anchor=tk.CENTER)
        self.canvas.bind('<Configure>', self._resize_image)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def __call__(self, *args, **kwargs):
        return self.canvas

    def _resize_image(self, event):
        _x = event.width
        _y = event.height
        self.img = self.img.resize((_x, _y))
        self.imageTk = ImageTk.PhotoImage(image=self.img)
        self.background.configure(image=self.imageTk)

    def player_screen(self):
        tbox = tk.Text(self.canvas, height=25, width=25)
        tbox.insert(tk.END, '\n')
        _text = "\rHow many players will be joining the game?\r\nThe Maximum number allowed is 7" \
                "\r\nPlease select a number between 1 and 7 or press Enter to use the Default of 1:"
        tbox.insert(tk.END, _text)
        tbox.pack(self)
        return tbox

    def select_players(self):
        self.canvas.destroy()
