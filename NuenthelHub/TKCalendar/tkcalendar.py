from datetime import datetime
from functools import partial
from tkinter import BOTH, CENTER, SUNKEN, NSEW, DISABLED, NORMAL, FLAT, Tk, messagebox, EW, SE, SW, S
from tkinter.ttk import Frame, Label, Button, Style

from NuenthelHub.TKCalendar.datehandler import DateHandler as dH
from NuenthelHub.TKCalendar.event import EventController
from NuenthelHub.TKCalendar.daytoplevel import DayTopWindow
from NuenthelHub.supportmodules.schedulescraper import CodyWorkSchedule


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
        self.legend_up = False

        """ Styling """
        self.style = Style()
        self.style.configure("Legend.TButton", relief=FLAT)

        # Add Event Extension Styling
        self.style.configure("CalMain.TFrame", background="white")
        self.style.configure("AddCancel.TButton", relief=FLAT, background="#BDC1BE")
        self.style.configure("Wkdy.TLabel", background="white")
        self.style.configure("Day.TButton", background="white", font="Roboto 12 bold")
        self.style.configure("CurrentDay.TButton", background="green", font="Roboto 12 bold")
        self.style.configure("DisDate.TButton", background="#999999")

        self.style.configure("Month.TLabel", background="white")

        self.style.configure("CodyWork.TButton", background="green", relief=SUNKEN, font="Roboto 12 bold")
        self.style.configure("SamWork.TButton", background="orange", relief=SUNKEN, font="Roboto 12 bold")
        self.style.configure("BothWork.TButton", background="red", relief=SUNKEN, font="Roboto 12 bold")
        self.style.configure("Other.TButton", background="purple", relief=SUNKEN, font="Roboto 12 bold")

        """ External Helper Classes """
        self.dh = dH()

        """ GUI Constructor Functions """
        self.make_sidebar_frame()
        self.make_main_frame()
        self.make_legend_frame()
        self.make_header()
        self.make_day_frame()
        self.make_weekday_heads()
        self.make_month_head()
        self.make_legend()
        self.make_day_buttons()
        self.make_sidebar_buttons()

        """ GUI Configuration Functions """
        self.configure_header()
        self.configure_day_buttons()
        self.event_color_buttons()
        self.row_col_configure(self.calendar_header_frame, 1, row_config=False)
        self.row_col_configure(self.day_frame, 1)
        self.row_col_configure(self.main_frame, 1)
        self.row_col_configure(self.legend_frame, 1)

    def make_main_frame(self):
        self.main_frame = Frame(self.master.body_frame, style="CalMain.TFrame")
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW, columnspan=4, rowspan=2)

    def make_sidebar_frame(self):
        self.sidebar_frame = Frame(self.master.body_frame, style="CalMain.TFrame")
        self.sidebar_frame.grid(row=0, column=5, padx=10, pady=10, ipadx=30, sticky=NSEW)

    def make_header(self):
        """ Create frame for day headers """
        self.calendar_header_frame = Frame(self.main_frame,  style="CalMain.TFrame")
        self.calendar_header_frame.grid(row=0, column=0, padx=10, sticky=EW)

    def make_day_frame(self):
        self.day_frame = Frame(self.main_frame,  style="CalMain.TFrame")
        self.day_frame.grid(row=1, column=0,  padx=10, pady=10, sticky=NSEW)

    def make_legend_frame(self):
        """ Create a frame for add event widgets """
        self.legend_frame = Frame(self.main_frame,  style="CalMain.TFrame")

    def show_legend_frame(self):
        self.legend_frame.grid(row=0, column=1, rowspan=7, sticky=NSEW)

    def make_month_head(self):
        """ Creates calendar header label """
        self.month_lbl = Label(self.calendar_header_frame, text="", font="Roboto 20", anchor=CENTER, style="Month.TLabel")
        self.month_lbl.grid(row=0, column=1, sticky=EW)

        Button(
            self.calendar_header_frame, text="<", command=self.month_down, style="MonthAdjust.TButton")\
            .grid(row=0, column=0)
        Button(
            self.calendar_header_frame, text=">", command=self.month_up, style="MonthAdjust.TButton")\
            .grid(row=0, column=2)

    def make_weekday_heads(self):
        day_list = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]
        """ Builds heading day names """
        for i, j in enumerate(day_list):
            Label(self.day_frame, text=day_list[i], style="Wkdy.TLabel", anchor=S) \
                .grid(row=0, column=i)

    def make_day_buttons(self):
        """ Creates date buttons """
        for coord in [(i, j) for i in range(1, 7) for j in range(0, 7)]:
            btn = Button(
                self.day_frame, style="Day.TButton")
            btn.grid(row=coord[0], column=coord[1], sticky=NSEW, ipady=20, padx=1, pady=1)
            self.date_buttons.append(btn)

    def make_sidebar_buttons(self):
        """ Returns button to master to be placed on a sidebar frame """
        return_btn = Button(self.sidebar_frame, text="Return", command=self.return_to_main)
        legend = Button(self.sidebar_frame, text="Legend", command=self.open_legend)
        cody_sched_scrape = Button(self.sidebar_frame, text="NDHP Scrape", command=self.cody_scrape)
        for button in [return_btn, legend, cody_sched_scrape]:
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

    def make_legend(self):
        """ Creates button representation of colors with category text """
        colors = ["green", "orange", "red", "purple"]
        categories = ["Cody Works", "Sam Works", "Work Overlap", "Other"]
        for i, j in enumerate(colors):
            legend_style = Style()
            legend_style.configure(f"{j}.TButton", background=j, relief=FLAT)
            Button(self.legend_frame, text=categories[i], style=f"{j}.TButton").grid(row=i, column=0, sticky=NSEW, pady=10,
                                                                                padx=10)

    @staticmethod
    def colorize(button: Button, categories: list):
        if "c-work" in categories and "s-work" in categories:
            button.configure(style="CodyWork.TButton")
        if "c-work" in categories:
            button.configure(style="CodyWork.TButton")
        if "s-work" in categories:
            button.configure(style="SamWork.TButton")
        if categories:
            button.configure(style="Other.TButton")

    @staticmethod
    def row_col_configure(master: Tk or Frame, weight: int, col_index: int = 0, row_index: int = 0,
                          row_config: bool = True, col_config: bool = True):
        columns, rows = master.grid_size()
        if col_config:
            for i in range(col_index, columns):
                master.columnconfigure(i, weight=weight)
        if row_config:
            for i in range(row_index, rows):
                master.rowconfigure(i, weight=weight)

    def get_main_frame(self) -> Frame:
        return self.main_frame

    def repack_main_frame(self):
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW, columnspan=4, rowspan=2)
        self.sidebar_frame.grid(row=1, column=1, padx=10, pady=10, ipadx=20, sticky=NSEW)

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
        if self.legend_up:
            self.legend_frame.grid_forget()
            self.legend_up = False
        else:
            self.show_legend_frame()
            self.legend_up = True

    def return_to_main(self):
        self.main_frame.grid_remove()
        self.sidebar_frame.grid_remove()
        self.callback()

    @staticmethod
    def cody_scrape():
        """ Scrapes Cody's schedule and adds events to calendar """
        CodyWorkSchedule()
        messagebox.showinfo(title="Shift Scraper", message="Schedule Scrape Complete!")
