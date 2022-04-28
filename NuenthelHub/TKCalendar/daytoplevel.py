"""
DayTopLevel holds DayTopWindow a class to create a GUI to manipulate event information from the TK Calendar and
Event DB

Classes:
    DayTopWindow

"""

from tkinter import Toplevel, CENTER, END, FLAT, Listbox, SINGLE, EW, PhotoImage, GROOVE
from tkinter.ttk import Style, Label, Button
import NuenthelHub.TKCalendar.datehandler as dh
from NuenthelHub.TKCalendar.tkcalendar_ext import TKAddEventExtension, TKRemoveEvent, TKChangeEvent
from NuenthelHub.TKCalendar.event import EventController
from NuenthelHub.TKCalendar.img.imgpath import image_path


class DayTopWindow(Toplevel):
    """ Toplevel class for event operations on the TKCalendar """

    def __init__(self, day: int, month: int, year: int, callback: callable = None):
        super().__init__()

        """ Window Attributes """
        self.attributes = ("-topmost", True)
        self.title(f"Event Manager")
        self.resizable(width=False, height=False)
        self.event_box = None
        self.configure(bg="#D1D6D3")
        self.extension = None
        self.confirmation = None
        self.calendar_callback = callback

        """ Date Attributes """
        self.day = day
        self.month = month
        self.year = year

        """ Styling """
        self.style = Style()
        self.style.theme_use("alt")
        self.style.configure("HoverButton.TButton", bg="white", relief=FLAT)
        self.style.configure("DtpLevel.TLabel", bg="white", relief=GROOVE, borderwidth=2)

        """ Internal Functions """
        self._make_header()
        self._make_day_adjust_buttons()
        self._make_event_listbox()
        self._make_event_buttons()
        self._configure_event_box()

    def _make_header(self):
        """ Creates date header """
        header_text = f"{self.month}/{self.day}/{self.year}"
        self.header = Label(self, text=header_text, font="Courier 15", justify=CENTER, style="DtpLevel.TLabel")
        self.header.grid(row=0, column=1, ipady=3)

    def _make_day_adjust_buttons(self):
        """ Creates day increase/decrease buttons """
        Button(
            self, text=">", command=self.day_up, width=4, style="HoverButton.TButton").grid(row=0, column=2)
        Button(
            self, text="<", command=self.day_down, width=4, style="HoverButton.TButton").grid(row=0, column=0)

    def _make_event_listbox(self):
        """ Creates event listbox to display day events """
        self.event_box = Listbox(self, bg="#BDC1BE", height=5, selectmode=SINGLE, font="Arvo 12", justify=CENTER)
        self.event_box.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky=EW)

    def _make_event_buttons(self):
        """ Creates event interaction buttons """
        self.add_img = PhotoImage(file=image_path + "add_event.png")
        self.remove_img = PhotoImage(file=image_path + "remove_event.png")
        self.change_img = PhotoImage(file=image_path + "change_event.png")

        Button(
            self, image=self.add_img, text="Add Image", style="HoverButton.TButton", command=self.add_event).grid(row=2,
                                                                                                                  column=0)
        Button(
            self, image=self.remove_img, text="Remove Event", style="HoverButton.TButton",
            command=self.remove_event).grid(row=2, column=1)
        Button(
            self, image=self.change_img, text="Change Event", style="HoverButton.TButton",
            command=self.change_event).grid(row=2, column=2)

    def _configure_header(self):
        """ Update header to current month value """
        header_text = f"{self.month}/{self.day}/{self.year}"
        self.header.configure(text=header_text)

    def _configure_event_box(self):
        """ Update listbox with day events """
        self.event_box.delete(0, END)
        query = {"year": self.year, "month": self.month, "day": self.day}
        event_data = EventController.find_by_elements(query)
        list_data = [
            f"Time: {ev.time_hours}:{ev.time_minutes} - Event: {ev.title} [{ev.id}] " for ev in event_data]

        if not list_data:
            list_data = ["No Events"]
        else:
            list_data.insert(0, "Select An Event")

        for ev_data in list_data:
            self.event_box.insert(END, ev_data)

        self.calendar_callback()

    """ _______________________________________ Button Functions ____________________________________________________"""

    def day_up(self):
        """ Increments up currently selected date by one day """
        num_of_days = dh.DateHandler().days_in_month(self.month, self.year)
        self.day += 1
        if self.day > num_of_days:
            self.day = 1
            self.month += 1
            if self.month > 12:
                self.month = 1
                self.year += 1
        self._configure_header()
        self.event_box.destroy()
        self._make_event_listbox()
        self._configure_event_box()

        if self.extension:
            self.extension.main_frame.destroy()
            self.extension = None

    def day_down(self):
        """ Increments down currently selected date by one day """
        self.day -= 1
        if self.day < 1:
            self.month -= 1
            if self.month < 1:
                self.year -= 1
            self.day = dh.DateHandler().days_in_month(self.month, self.year)
        self._configure_header()
        self.event_box.destroy()
        self._make_event_listbox()
        self._configure_event_box()

        if self.extension:
            self.extension.main_frame.destroy()
            self.extension = None

    def add_event(self):
        """ Opens add event extension """
        if not self.extension:
            self.confirmation.destroy() if self.confirmation else None
            self.extension = TKAddEventExtension(self, self.day, self.month, self.year, self._configure_event_box)

    def remove_event(self):
        """ Opens remove event extension """
        if not self.extension:
            if not self.event_box.curselection():
                if self.confirmation:
                    self.confirmation.destroy()
                self.confirmation = Label(self, text="Choose an event.", font="Courier 10")
                self.confirmation.grid(row=self.grid_size()[1], column=1, pady=10)
                return

            self.confirmation.destroy() if self.confirmation else None

            selection = self.event_box.get(self.event_box.curselection()).strip()
            if selection not in ["No Events", "Select An Event"]:
                self.extension = True
                str_id = selection.split(" ")[-1]
                int_id = int(str_id[1:-1])
                self.extension = TKRemoveEvent(self, int_id, self._configure_event_box)

    def change_event(self):
        """ Change event extension """
        if not self.extension:
            if not self.event_box.curselection():
                if self.confirmation:
                    self.confirmation.destroy()
                self.confirmation = Label(self, text="Choose an event.", font="Courier 10")
                self.confirmation.grid(row=self.grid_size()[1], column=1, pady=10)
                return

            self.confirmation.destroy() if self.confirmation else None

            selection = self.event_box.get(self.event_box.curselection()).strip()
            if selection not in ["No Events", "Select An Event"]:
                self.extension = True
                str_id = selection.split(" ")[-1]
                int_id = int(str_id[1:-1])
                self.extension = TKChangeEvent(self, int_id, self._configure_event_box)
