from tkinter import Tk, PhotoImage
from tkinter.ttk import Label, Frame, Style



class NuenthelHub(Tk):
    def __init__(self):
        super().__init__()
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.title("Nuenthel Hub")
        self.resizable(False, False)
        self.style = Style()
        self.style.theme_use("xpnative")

        """Internal Functions"""
        self._main_frame()
        self._wallpaper()

    def _main_frame(self):
        self.main_frame = Frame(self)
        self.main_frame.grid(row=0, column=0)

    def _wallpaper(self):
        self.background_image = PhotoImage(file="Photos/mountain_bg.png")
        self.background_label = Label(self.main_frame, image=self.background_image)
        self.background_label.grid(row=0, column=0)

if __name__ == '__main__':
    NuenthelHub().mainloop()
