from tkinter import Tk, Canvas, VERTICAL, LEFT, RIGHT, BOTTOM, NSEW
from tkinter.ttk import Label, Frame, Style, Scrollbar, Panedwindow
from PIL import ImageTk, Image
from TKCalendar.tkcalendar import TKCalendar
from TKBudget.tkbudget import TKBudget
from TKChores.tkchores import TKChores
from supportmodules import modifiedwidgets

class NuenthelHub(Tk):
    def __init__(self):
        super().__init__()
        # self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.title("Nuenthel Hub")
        self.style = Style()
        self.configure(bg="black")
        self.style.theme_use("xpnative")
        self.resizable(True, True)
        # self.attributes("-fullscreen", True)

        """ Styling """


        """Window Frames"""
        self.calendar_frame_widget = None

        """Internal Functions"""
        # self._main_frame()
        # self._wallpaper()
        self._calendar()
        self._budget()
        self._chores()
        self._row_col_configure()
        # self._number()
    #
    # def _main_frame(self):
    #     self.main_frame = Frame(self)
    #     self.main_frame.grid(row=0, column=0)

    # def _wallpaper(self):
    #     raw_image = Image.open("photos/mountain_bg.png")
    #     image = raw_image.resize((self.winfo_screenwidth(), self.winfo_screenheight()))
    #     self.background_image = ImageTk.PhotoImage(image)
    #     self.background_label = Label(self.main_frame, image=self.background_image)
    #     self.background_label.grid(row=0, column=0, rowspan=10, columnspan=10)

    def _calendar(self):
        TKCalendar(self).grid(row=0, column=0, sticky=NSEW)

    def _budget(self):
        TKBudget(self).grid(row=0, column=1, sticky=NSEW)

    def _chores(self):
        TKChores(self).grid(row=1, column=0, columnspan=2, sticky=NSEW)

    def _row_col_configure(self):
        columns, rows = self.grid_size()
        for columns in range(columns):
            self.columnconfigure(columns, weight=1)
        for rows in range(rows):
            self.rowconfigure(rows, weight=1)
# ___________________________ Button Functions _____________________________________________




if __name__ == '__main__':
    NuenthelHub().mainloop()
