from tkinter import Tk, Canvas, VERTICAL, LEFT, RIGHT, BOTTOM, NSEW, PhotoImage
from tkinter.ttk import Label, Frame, Style, Scrollbar, Panedwindow
from TKCalendar.tkcalendar import TKCalendar
from TKBudget.tkbudget import TKBudget
from TKChores.tkchores import TKChores
from TKSonyRemote.tksonyremote import TKSonyRemote


class NuenthelHub(Tk):
    def __init__(self):
        super().__init__()
        self.title("Nuenthel Hub")
        self.style = Style()
        self.configure(bg="#add8e6")
        self.style.theme_use("xpnative")
        self.resizable(True, True)
        self.attributes("-fullscreen", True)

        """ Styling """

        """Window Frames"""
        self.calendar_frame_widget = None

        """Internal Functions"""
        self._calendar()
        self._budget()
        self._chores()
        self._tv()
        self._row_col_configure()
        # self._number()

    def _calendar(self):
        TKCalendar(self).grid(row=0, column=0, rowspan=2, sticky=NSEW, padx=5, pady=5)

    def _budget(self):
        TKBudget(self).grid(row=0, column=1, sticky=NSEW, padx=5, pady=5)

    def _chores(self):
        TKChores(self).grid(row=3, column=0, columnspan=2, sticky=NSEW, padx=5, pady=5)

    def _tv(self):
        TKSonyRemote(self).grid(row=2, column=1, sticky=NSEW, padx=5, pady=5)

    def _row_col_configure(self):
        columns, rows = self.grid_size()
        for columns in range(columns):
            self.columnconfigure(columns, weight=3)
        for rows in range(rows):
            self.rowconfigure(rows, weight=3)


if __name__ == '__main__':
    NuenthelHub().mainloop()
