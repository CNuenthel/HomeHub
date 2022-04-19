from datetime import datetime
from functools import partial
from tkinter import SOLID, CENTER, SUNKEN, NSEW, PhotoImage, DISABLED, NORMAL, FLAT, Tk, BOTH
from tkinter.ttk import Frame, Label, Button, Style

from NuenthelHub.TKCalendar.datehandler import DateHandler as dH
from NuenthelHub.TKCalendar.eventcolor import EventColor
from TKCalendar.events.eventdbcontroller import EventController
from TKCalendar.img.imgpath import image_path
from TKCalendar.tkwindowextensions.tk_legend import TKLegend
from TKCalendar.toplevels.daytoplevel import DayTopWindow
from supportmodules.modifiedwidgets import HoverButton

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
        self.header = None

        """ Functional Variables """
        self.year = datetime.now().year  # Returns 4-digit int(year)
        self.month = datetime.now().month  # Returns int(month)
        self.dates = []

        """ Styling """
        self.style = Style(self)
        self.style.theme_use("clam")
        self.style.configure("MonthAdjust.TButton", background=button_bg, height=3)
        self.style.configure("Legend.TButton", relief=FLAT)

        # Add Event Extension Styling
        self.style.configure("AddMain.TFrame", background="#BDC1BE")
        self.style.configure("AddExt.TLabel", background="#BDC1BE")
        self.style.configure("AddCancel.TButton", relief=FLAT, background="#BDC1BE")
        self.style.configure("ReqInfo.TLabel", background="#BDC1BE", foreground="red")
        self.style.configure("DkGray.TFrame", background="#D1D6D3")
        self.style.configure("DkGray.TLabel", background="#D1D6D3", justify=CENTER, anchor=CENTER)

        """ Helper Classes """
        self.dh = dH()

        """ Internal Functions """
        self._make_header()
        self._make_day_buttons()
        self._make_month_adjust_buttons()
        self._make_legend_button()
        self._configure_day_buttons()
        self._event_color_buttons()
        self._configure_rows_columns(self)

    def _make_header(self):
        """ Creates calendar header label """
        header_text = f"{self.dh.month_num_to_string(self.month)} {self.year}"
        self.header = Label(self, text=header_text, font=font+"20", anchor=CENTER)
        self.header.columnconfigure(0, weight=1)
        self.header.grid(row=0, column=2, columnspan=3)

        day_list = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]

        """ Builds heading day names """
        for i, j in enumerate(day_list):
            lbl = Label(self, text=day_list[i], relief=SOLID, anchor=CENTER)
            lbl.grid(row=1, column=i, sticky=NSEW, ipady=20)
            lbl.columnconfigure(i, weight=1)

    def _make_month_adjust_buttons(self):
        """ Creates buttons for moving month up or down """
        Button(
            self, text=">", command=self.month_up, style="MonthAdjust.TButton", width=8).grid(row=0, column=5)
        Button(
            self, text="<", command=self.month_down, style="MonthAdjust.TButton", width=8).grid(row=0, column=1)

    def _make_day_buttons(self):
        """ Creates date buttons """
        coords = [(i, j) for i in range(2, 8) for j in range(0, 7)]
        for coord in coords:
            btn = HoverButton(
                self, bg="gray", relief=SUNKEN, bd=2, height=4, width=10)
            btn.grid(row=coord[0], column=coord[1], sticky='nsew')
            self.date_buttons.append(btn)

    def _make_legend_button(self):
        """ Creates legend button """
        self.menu_img = PhotoImage(file=image_path + "menu.png")
        Button(self, image=self.menu_img, style="Legend.TButton", command=self.open_legend).grid(
            row=0, column=6, padx=3, pady=3)

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

    def _configure_rows_columns(self, grid_master=None):
        """ Configures rows and columns to expand with resize of window """
        columns, rows = grid_master.grid_size()
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
            return

        self.legend = TKLegend(self)


if __name__ == '__main__':
    x = Tk()
    x.columnconfigure(0, weight=1)
    x.rowconfigure(0, weight=1)
    TKCalendar(x).grid(row=0, column=0, sticky=NSEW)
    x.mainloop()
