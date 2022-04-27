from datetime import datetime
from functools import partial
from tkinter import SOLID, CENTER, SUNKEN, NSEW, DISABLED, NORMAL, FLAT, Tk
from tkinter.ttk import Frame, Label, Button, Style

from NuenthelHub.TKCalendar.datehandler import DateHandler as dH
from NuenthelHub.TKCalendar.eventcolor import EventColor
from NuenthelHub.TKCalendar.event import EventController
from NuenthelHub.TKCalendar.tkcalendar_ext import TKLegend
from NuenthelHub.TKCalendar.daytoplevel import DayTopWindow
from NuenthelHub.supportmodules.modifiedwidgets import HoverButton

font = "Roboto "
button_bg = "#808080"


class TKCalendar(Frame):
    """ TKinter Calendar """

    def __init__(self, root: Frame or Tk = None, callback: callable = None):
        super().__init__()

        """ Window Attributes """
        self.master = root
        self.callback = callback
        self.date_buttons = []
        self.all_widgets = []
        self.toplevel = None
        self.legend = None
        self.month_lbl = None

        """ Functional Variables """
        self.year = datetime.now().year  # Returns 4-digit int(year)
        self.month = datetime.now().month  # Returns int(month)
        self.dates = []

        """ Styling """
        self.style = Style(self)
        self.style.theme_use("alt")
        self.style.configure("MonthAdjust.TButton", background=button_bg, height=3)
        self.style.configure("Legend.TButton", relief=FLAT)

        # Add Event Extension Styling
        self.style.configure("AddCancel.TButton", relief=FLAT, background="#BDC1BE")
        self.style.configure("Wkdy.TLabel", background="#ADD8E6", relief=SUNKEN)
        self.style.configure("HF.TFrame", background="white")
        self.style.configure("Month.TLabel", background="white")
        self.style.configure("TFrame", background="white")

        """ Helper Classes """
        self.dh = dH()

        """ Internal Functions """
        self._make_header_frame()
        self._make_month_head()
        self._make_weekday_frame()
        self._make_weekday_heads()
        self._make_day_frame()
        self._make_day_buttons()
        self._configure_header()
        self._configure_day_buttons()
        self._row_col_configure(self, 1)
        self._row_col_configure(self.header_frame, 1)
        self._row_col_configure(self.weekday_frame, 1)
        self._row_col_configure(self.day_frame, 1)

    def _make_header_frame(self):
        """ Create frame for header affixed to main window """
        self.header_frame = Frame(self, style="HF.TFrame")
        self.header_frame.grid(row=0, column=0, sticky=NSEW)

    def _make_month_head(self):
        """ Creates calendar header label """
        self.month_lbl = Label(self.header_frame, text="", font=font + "20", anchor=CENTER, style="Month.TLabel")
        self.month_lbl.grid(row=0, column=1, sticky=NSEW, pady=10)

        Button(
            self.header_frame, text="<", command=self.month_up, style="MonthAdjust.TButton", width=8)\
            .grid(row=0, column=0, pady=10)
        Button(
            self.header_frame, text=">", command=self.month_down, style="MonthAdjust.TButton", width=8)\
            .grid(row=0, column=2, pady=10)

    def _make_weekday_frame(self):
        """ Create frame for day headers """
        self.weekday_frame = Frame(self)
        self.weekday_frame.grid(row=1, column=0, sticky=NSEW)

    def _make_weekday_heads(self):
        day_list = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]
        """ Builds heading day names """
        for i, j in enumerate(day_list):
            Label(self.weekday_frame, text=day_list[i], style="Wkdy.TLabel", anchor=CENTER, width=10) \
                .grid(row=0, column=i, sticky=NSEW)

    def _make_day_frame(self):
        self.day_frame = Frame(self)
        self.day_frame.grid(row=2, column=0, sticky=NSEW)

    def _make_day_buttons(self):
        """ Creates date buttons """
        for coord in [(i, j) for i in range(0, 6) for j in range(0, 7)]:
            btn = HoverButton(
                self.day_frame, bg="gray", relief=SUNKEN, height=4, width=10)
            btn.grid(row=coord[0], column=coord[1], sticky="nsew")
            self.date_buttons.append(btn)

    def _configure_header(self):
        """ Set header to display updated month """
        self.month_lbl.configure(text=f"{self.dh.month_num_to_string(self.month)} {self.year}")

    def _configure_day_buttons(self):
        """ Set button text to date numbers """
        self.dates = self.dh.date_list(self.year, self.month)  # Returns 35 dates (5 week calendar)
        self.dates.extend(
            [0 for _ in range(42 - len(self.dates))])  # Add zeros to dates to compensate for 42 date buttons

        for i, j in enumerate(self.dates):  # Configure button text to show dates
            if j == 0:
                self.date_buttons[i].configure(text="", state=DISABLED, bg=button_bg)
            else:
                """ We use a partial function here to send day num (j) to our function """
                self.date_buttons[i].configure(text=j, command=partial(self.day_info, j), bg="white", state=NORMAL)

            if j == datetime.today().day \
                    and self.month == datetime.today().month \
                    and self.year == datetime.today().year:
                self.date_buttons[i].configure(bg="#D9FFE3")

    def _event_color_buttons(self):
        for button in self.date_buttons:
            if button["text"] != 0:
                query = {"year": self.year, "month": self.month, "day": button["text"]}
                date_events = EventController.find_by_elements(query)
                if date_events:
                    categories = [event.category for event in date_events]
                    EventColor().colorize(button, categories)

    @staticmethod
    def _row_col_configure(master: Tk or Frame, weight: int, col_index: int = 0, row_index: int = 0):
        columns, rows = master.grid_size()
        for i in range(col_index, columns):
            master.columnconfigure(i, weight=weight)
        for i in range(row_index, rows):
            master.rowconfigure(i, weight=weight)

    """ ______________________________________Button Functions ________________________________________________"""

    def month_up(self):
        """ Increment month up and reconfigure calendar interface """
        self.month += 1
        if self.month == 13:
            self.month = 1
            self.year += 1
        self._configure_day_buttons()
        self._event_color_buttons()
        self._configure_header()

    def month_down(self):
        """ Increment month down and reconfigure calendar interface """
        self.month -= 1
        if self.month == 0:
            self.month = 12
            self.year -= 1
        self._configure_day_buttons()
        self._event_color_buttons()
        self._configure_header()

    def day_info(self, day_num):
        """ Opens top window for event interaction, destroys previous top window"""

        try:
            self.toplevel.destroy()
            self.toplevel = DayTopWindow(day_num, self.month, self.year, self._event_color_buttons)
        except AttributeError:
            self.toplevel = DayTopWindow(day_num, self.month, self.year, self._event_color_buttons)

    def open_legend(self):
        """ Opens legend sidebar extension """
        if self.legend:
            self.legend.main_frame.destroy()
            self.legend = None
            return

        self.legend = TKLegend(self)


if __name__ == '__main__':
    x = Tk()
    x.columnconfigure(0, weight=1)
    x.rowconfigure(0, weight=1)
    TKCalendar(x).grid(row=0, column=0, sticky=NSEW)
    x.mainloop()
