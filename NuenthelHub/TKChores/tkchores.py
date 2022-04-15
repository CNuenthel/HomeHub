
from tkinter import Tk, Frame, FLAT, Label, LEFT, NSEW, GROOVE


bg_color = "#909090"
border_color = "#9594B7"
font = "Roboto "
header_color = "#232323"


class TKChores(Tk):
    """ TKinter Calendar """

    def __init__(self):
        super().__init__()

        """ Window Attributes """
        self.minsize(width=500, height=350)
        self.configure(background=bg_color)
        self.title("Chores")

        """ Internal Functions """
        self._make_header()
        self._configure_rows_columns()

    def _make_header(self):
        self.header_frame = Frame(self, background=header_color, relief=FLAT)
        self.header_frame.grid(row=0, column=0, columnspan=8, sticky=NSEW)
        self.header_label = Label(self.header_frame, bg=header_color, fg="white", text="Chores",
                                  font=font + "25 underline")
        self.header_label.grid(row=0, column=0, columnspan=1, sticky=NSEW, padx=15)
        self.darklight_frame = Frame(self, background=header_color, relief=FLAT)
        self.darklight_frame.grid(row=1, column=0, columnspan=8, sticky=NSEW)

    def _make_chore_window(self):
        self.border_frame = Frame(self, bg=border_color, borderwidth=3, relief=GROOVE)
        self.border_frame.grid(row=1, column=0, columnspan=8, sticky=NSEW, padx=10, pady=10)
        self.chore_frame = Frame(self.border_frame, background=bg_color, borderwidth=3, relief=GROOVE)
        self.chore_frame.grid(row=0, column=0, columnspan=8, padx=5, pady=5, ipadx=10, sticky=NSEW)

    def _configure_rows_columns(self):
        """ Configures rows and columns to expand with resize of window """
        columns, rows = self.grid_size()
        for columns in range(columns):
            self.columnconfigure(columns, weight=1)
        for rows in range(rows):
            self.rowconfigure(rows, weight=1)

    """ ______________________________________Button Functions ________________________________________________"""

def btn_pushed():
    print("Button Pushed!")

x = TKChores().mainloop()
