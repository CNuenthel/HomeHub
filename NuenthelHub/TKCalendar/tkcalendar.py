from datetime import datetime
from functools import partial
from tkinter import BOTH, CENTER, SUNKEN, NSEW, DISABLED, NORMAL, FLAT, Tk, messagebox
from tkinter.ttk import Frame, Label, Button, Style

from NuenthelHub.TKCalendar.datehandler import DateHandler as dH
from NuenthelHub.TKCalendar.event import EventController
from NuenthelHub.TKCalendar.tkcalendar_ext import TKLegend
from NuenthelHub.TKCalendar.daytoplevel import DayTopWindow
from NuenthelHub.supportmodules.schedulescraper import CodyWorkSchedule

font = "Roboto "
button_bg = "#808080"


class TKCalendar:
    """ TKinter Calendar """

    def __init__(self, master, callback: callable = None, **kwargs):
        super().__init__(**kwargs)

        """ Window Attributes """
        self.master = master
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
        self.style = Style(self.master.master)
        self.style.theme_use("vista")
        self.style.configure("MonthAdjust.TButton", background=button_bg, height=3)
        self.style.configure("Legend.TButton", relief=FLAT)

        # Add Event Extension Styling
        self.style.configure("AddCancel.TButton", relief=FLAT, background="#BDC1BE")
        self.style.configure("Wkdy.TLabel", background="#ADD8E6", relief=SUNKEN)
        self.style.configure("Day.TButton", relief=SUNKEN, height=4, background="white")
        self.style.configure("CurrentDay.TButton", relief=SUNKEN, height=4, background="green")
        self.style.configure("DisDate.TButton", relief=SUNKEN, height=4, background="black")

        self.style.configure("HF.TFrame", background="white")
        self.style.configure("Month.TLabel", background="white")
        self.style.configure("TFrame", background="white")

        self.style.configure("CodyWork.TButton", background="#F7D8BA", relief=SUNKEN, height=4)
        self.style.configure("SamWork.TButton", background="#FEFF8DD", relief=SUNKEN, height=4)
        self.style.configure("BothWork.TButton", background="#C6B6D6", relief=SUNKEN, height=4)
        self.style.configure("Other.TButton", background="#ACDDDE", relief=SUNKEN, height=4)

        """ Helper Classes """
        self.dh = dH()

        """ Internal Functions """
        self.make_header_frame()
        self.make_month_head()
        self.make_weekday_frame()
        self.make_weekday_heads()
        self.make_day_frame()
        self.make_day_buttons()
        self.configure_header()
        self.configure_day_buttons()
        self.event_color_buttons()
        self.tkcal_sidebar_buttons()
        self.row_col_configure(self.header_frame, 1)
        self.row_col_configure(self.weekday_frame, 1)
        self.row_col_configure(self.day_frame, 1)

    def make_header_frame(self):
        """ Create frame for header affixed to main window """
        self.header_frame = Frame(self.master.body_frame, style="HF.TFrame")
        self.header_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

    def make_month_head(self):
        """ Creates calendar header label """
        self.month_lbl = Label(self.header_frame, text="", font=font + "20", anchor=CENTER, style="Month.TLabel")
        self.month_lbl.grid(row=0, column=1, sticky=NSEW, pady=10)

        Button(
            self.header_frame, text="<", command=self.month_down, style="MonthAdjust.TButton", width=8)\
            .grid(row=0, column=0, pady=10)
        Button(
            self.header_frame, text=">", command=self.month_up, style="MonthAdjust.TButton", width=8)\
            .grid(row=0, column=2, pady=10)

    def make_weekday_frame(self):
        """ Create frame for day headers """
        self.weekday_frame = Frame(self.master.body_frame)
        self.weekday_frame.grid(row=1, column=0,  padx=10, sticky=NSEW)

    def make_weekday_heads(self):
        day_list = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]
        """ Builds heading day names """
        for i, j in enumerate(day_list):
            Label(self.weekday_frame, text=day_list[i], style="Wkdy.TLabel", anchor=CENTER, width=10) \
                .grid(row=0, column=i, sticky=NSEW)

    def make_day_frame(self):
        self.day_frame = Frame(self.master.body_frame)
        self.day_frame.grid(row=2, column=0,  padx=10, sticky=NSEW)

    def make_day_buttons(self):
        """ Creates date buttons """
        for coord in [(i, j) for i in range(0, 6) for j in range(0, 7)]:
            btn = Button(
                self.day_frame, style="Day.TButton", width=10)
            btn.grid(row=coord[0], column=coord[1], sticky=NSEW, ipady=20)
            self.date_buttons.append(btn)

    def tkcal_sidebar_buttons(self):
        """ Returns button to master to be placed on a sidebar frame """
        calendar_sidebar_buttons = Button(self.master.sidebar_frame, text="Legend", command=self.open_legend, width=20)
        cody_sched_scrape = Button(self.master.sidebar_frame, text="NDHP Scrape", command=self.cody_scrape, width=20)
        for button in [calendar_sidebar_buttons, cody_sched_scrape]:
            button.pack(expand=True, fill=BOTH)

    def configure_header(self):
        """ Set header to display updated month """
        self.month_lbl.configure(text=f"{self.dh.month_num_to_string(self.month)} {self.year}")

    def configure_day_buttons(self):
        """ Set button text to date numbers """
        self.dates = self.dh.date_list(self.year, self.month)  # Returns 35 dates (5 week calendar)
        self.dates.extend(
            [0 for _ in range(42 - len(self.dates))])  # Add zeros to dates to compensate for 42 date buttons

        for i, j in enumerate(self.dates):  # Configure button text to show dates
            if j == 0:
                self.date_buttons[i].configure(text="", state=DISABLED, style="DisDate.TButton")
            else:
                """ We use a partial function here to send day num (j) to our function """
                self.date_buttons[i].configure(text=j, command=partial(self.day_info, j), style="Day.TButton", state=NORMAL)

            if j == datetime.today().day \
                    and self.month == datetime.today().month \
                    and self.year == datetime.today().year:
                self.date_buttons[i].configure(style="CurrentDay.TButton")

    def event_color_buttons(self):
        for button in self.date_buttons:
            if button["text"] != 0:
                query = {"year": self.year, "month": self.month, "day": button["text"]}
                date_events = EventController.find_by_elements(query)
                if date_events:
                    categories = [event.category for event in date_events]
                    self.colorize(button, categories)

    @staticmethod
    def colorize(button: Button, categories: list):
        if "C-Work" in categories and "S-Work" in categories:
            button.configure(style="CodyWork.TButton")
        if "C-Work" in categories:
            button.configure(style="CodyWork.TButton")
        if "S-Work" in categories:
            button.configure(style="SamWork.TButton")
        if categories:
            button.configure(style="Other.TButton")

    @staticmethod
    def row_col_configure(master: Tk or Frame, weight: int, col_index: int = 0, row_index: int = 0):
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
        self.configure_day_buttons()
        self.event_color_buttons()
        self.configure_header()

    def month_down(self):
        """ Increment month down and reconfigure calendar interface """
        self.month -= 1
        if self.month == 0:
            self.month = 12
            self.year -= 1
        self.configure_day_buttons()
        self.event_color_buttons()
        self.configure_header()

    def day_info(self, day_num):
        """ Opens top window for event interaction, destroys previous top window"""
        try:
            self.toplevel.destroy()
            self.toplevel = DayTopWindow(day_num, self.month, self.year, self.event_color_buttons)
        except AttributeError:
            self.toplevel = DayTopWindow(day_num, self.month, self.year, self.event_color_buttons)

    def open_legend(self):
        """ Opens legend sidebar extension """
        if self.legend:
            self.legend.main_frame.destroy()
            self.legend = None
            return

        self.legend = TKLegend(self)

    @staticmethod
    def cody_scrape():
        """ Scrapes Cody's schedule and adds events to calendar """
        CodyWorkSchedule()
        messagebox.showinfo(title="Shift Scraper", message="Schedule Scrape Complete!")


