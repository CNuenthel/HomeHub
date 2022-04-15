from datetime import datetime
from functools import partial
from tkinter import *

from TKCalendar.events.eventdbcontroller import EventController
from NuenthelHub.TKCalendar.datehandler import DateHandler as dH
from NuenthelHub.TKCalendar.eventcolor import EventColor
from supportmodules.modifiedwidgets import HoverButton
from TKCalendar.toplevels.daytoplevel import DayTopWindow
from TKCalendar.tkwindowextensions.tk_legend import TKLegend
from TKCalendar.img.imgpath import image_path


class TKCalendar(Frame):
    """ TKinter Calendar """

    def __init__(self):
        super().__init__()

        """ Window Attributes """
        # self.minsize(width=700, height=700)
        # self.title("TK Calendar")
        self.date_buttons = []
        self.toplevel = None
        self.legend = None
        self.header = None

        """ Functional Variables """
        self.year = datetime.now().year  # Returns 4-digit int(year)
        self.month = datetime.now().month  # Returns int(month)
        self.dates = []

        """ Helper Classes """
        self.dh = dH()

        """ Internal Functions """
        self._make_header()
        self._make_day_buttons()
        self._make_month_adjust_buttons()
        self._make_legend_button()
        self._configure_day_buttons()
        self._event_color_buttons()
        self._configure_rows_columns()

    def _make_header(self):
        """ Creates calendar header label """
        header_text = f"{self.dh.month_num_to_string(self.month)} {self.year}"
        self.header = Label(self, text=header_text, font="Arvo 20", justify=CENTER)
        self.header.grid(row=0, column=1, columnspan=5, sticky=EW, ipady=20)

        day_list = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]
        for i, j in enumerate(day_list):
            Label(self, text=day_list[i], bd=1, relief=SOLID).grid(row=1, column=i, sticky=NSEW, ipady=20)

    def _make_month_adjust_buttons(self):
        """ Creates buttons for moving month up or down """
        Button(
            self, text=">", command=self.month_up, bg="#808080", height=2, width=8).grid(row=0, column=5)
        Button(
            self, text="<", command=self.month_down, bg="#808080", height=2, width=8).grid(row=0, column=1)

    def _make_day_buttons(self):
        """ Creates date buttons """
        coords = [(i, j) for i in range(2, 8) for j in range(0, 7)]
        for coord in coords:
            btn = HoverButton(
                self, bg="gray", relief=SUNKEN, bd=2, height=6, width=10)
            btn.grid(row=coord[0], column=coord[1], sticky=NSEW)
            self.date_buttons.append(btn)

    def _make_legend_button(self):
        """ Creates legend button """
        self.menu_img = PhotoImage(file=image_path+"menu.png")
        Button(self, image=self.menu_img, command=self.open_legend, bg="#CAF1DE", height=30,
               width=30, relief=FLAT).grid(row=0, column=6)

    def _configure_header(self):
        """ Set header to display updated month """
        self.header.configure(text=f"{self.dh.month_num_to_string(self.month)} {self.year}")

    def _configure_day_buttons(self):
        """ Set button text to date numbers """
        self.dates = self.dh.date_list(self.year, self.month)  # Returns 35 dates (5 week calendar)
        self.dates.extend(
            [0 for _ in range(42 - len(self.dates))])  # Add zeros to dates to compensate for 42 date buttons

        for i, j in enumerate(self.dates):  # Configure button text to show dates
            if j == 0:
                self.date_buttons[i].configure(text="", state=DISABLED, bg="#808080")
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

    def _configure_rows_columns(self):
        """ Configures rows and columns to expand with resize of window """
        columns, rows = self.grid_size()
        for columns in range(columns):
            self.columnconfigure(columns, weight=1)
        for rows in range(rows):
            self.rowconfigure(rows, weight=1)

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
            # self.minsize(width=700, height=700)
            return

        self.legend = TKLegend(self)

