from tkinter import Label, Tk, Toplevel, E, Frame, NSEW, PhotoImage, Button, CENTER, FLAT
from tkinter.ttk import Combobox, Style

from TKCalendar.events.eventdbcontroller import EventController
from TKCalendar.events.events import Event
from TKCalendar.img.imgpath import image_path
from modifiedwidgets import NumberOnlyCombobox
from modifiedwidgets import TextFilledEntry


class TKAddEventExtension:
    """
    Extends an instantiated Tk or Toplevel window starting from the last grid row with
    additional widgets to collect Event data

    ...
    Parameters
    ----------
    root_window: TK or Toplevel
        The window to extend with Event data widgets
    day: int
        Day as integer : 28
    month: int
        Month as integer: 2
    year: int
        Year as integer: 2022
    callback : callable
        Callback for use on extension completion for desired updates

    """

    def __init__(self, root_window: Tk or Toplevel, day: int, month: int, year: int, callback: callable = None):
        """ Extension Attributes """
        self.root = root_window
        self.day = day
        self.month = month
        self.year = year
        self.grid_row_start = root_window.grid_size()[1]
        self.column_count = root_window.grid_size()[0]
        self.callback = callback

        """ Internal Functions """
        self._create_main_frame()
        self._make_header()
        self._make_title_entry()
        self._make_time_widgets()
        self._make_category_combobox()
        self._make_details_entry()
        self._make_add_cancel_buttons()

    def _create_main_frame(self):
        """ Create a frame for add event widgets """
        self.border_frame = Frame(self.root, bg=self.root["bg"])
        self.border_frame.grid(row=self.grid_row_start, column=0, columnspan=self.column_count, sticky=NSEW)
        self.main_frame = Frame(self.root, bg="#BDC1BE")
        self.main_frame.grid(row=self.grid_row_start, column=0, columnspan=self.column_count, sticky=NSEW, padx=10,
                             pady=10)

    def _make_header(self):
        """ Create Add Event header """
        Label(
            self.main_frame, text="ADD EVENT", font="Courier 18 underline", bg="#BDC1BE") \
            .pack(pady=8)

    def _make_title_entry(self):
        """ Creates title text filled entry """
        self.title_entry = TextFilledEntry(self.main_frame, "Title", justify=CENTER)
        self.title_entry.pack(pady=8)

    def _make_time_widgets(self):
        """ Create time selection boxes """
        time_frame = Frame(self.main_frame)
        time_frame.pack(pady=8)

        hour_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
                     14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

        self.hour_selector = NumberOnlyCombobox(time_frame, "Hour", 2, values=hour_nums, justify=CENTER,
                                                background="white")
        self.hour_selector.set("Hour")
        self.hour_selector.grid(row=0, column=0)

        minute_nums = ["00"]
        minute_nums.extend([str(num * 10) for num in range(1, 6)])
        self.minute_selector = NumberOnlyCombobox(time_frame, "Minutes", 2, values=minute_nums, justify=CENTER,
                                                  background="white")
        self.minute_selector.set("00")
        self.minute_selector.grid(row=0, column=1, sticky=E)

        self.hour_selector.bind("<<ComboboxSelected>>", lambda e: self.main_frame.focus())
        self.minute_selector.bind("<<ComboboxSelected>>", lambda e: self.main_frame.focus())

    def _make_category_combobox(self):
        """ Create combobox to collect category """
        categories = ["Work", "Meeting", "Holiday", "Reminder"]
        self.category_selector = Combobox(self.main_frame, values=categories, justify=CENTER, background="white")
        self.category_selector.pack(pady=8)
        self.category_selector.set("Category")
        self.category_selector.bind("<<ComboboxSelected>>", lambda e: self.main_frame.focus())

    def _make_details_entry(self):
        """ Create an entry to collect details """
        self.details_entry = TextFilledEntry(self.main_frame, "Details", justify=CENTER)
        self.details_entry.pack(pady=8)

    def _make_add_cancel_buttons(self):
        """ Create add/cancel buttons """
        button_frame = Frame(self.main_frame, bg="#BDC1BE")
        button_frame.pack(pady=10)

        """ Create final add button """
        self.add_img = PhotoImage(file=image_path + "confirm.png")
        self.add = Button(button_frame, image=self.add_img, command=self._add_event, relief=FLAT,
                          bg="#BDC1BE")
        self.add.grid(row=0, column=0)

        """ Create cancel button """
        self.cancel_img = PhotoImage(file=image_path + "deny.png")
        self.cancel = Button(button_frame, image=self.cancel_img, command=self._cancel_event, relief=FLAT,
                             bg="#BDC1BE")
        self.cancel.grid(row=0, column=1)

    """ _________________________ BUTTON FUNCTIONS __________________________________________________________________"""

    def _add_event(self):
        """ Add event to DB """

        ev_dict = {
            "day": self.day,
            "year": self.year,
            "month": self.month,
            "title": self.title_entry.get(),
            "details": self.details_entry.get(),
            "time_hours": self.hour_selector.get(),
            "time_minutes": self.minute_selector.get(),
            "category": self.category_selector.get()
        }

        style = Style()
        if ev_dict["time_hours"] == "Hour" or ev_dict["time_minutes"] == "Minutes" or ev_dict["title"] == "Title":
            style.configure("TCombobox", fieldbackground="red", background="white")
            self.title_entry.configure(bg="red")
            self.warning = Label(self.main_frame, text="Please fill in required information.", bg="#BDC1BE", fg="red",
                                 font="Helvetica 13")
            self.warning.grid(row=6, column=0, pady=10)
            return

        """ Reconfigure red zones if triggered """
        self.title_entry.configure(bg="white")
        style.configure("TCombobox", fieldbackground="white", background="white")

        e = Event.create_from_dict(ev_dict)

        """ Destroy extension """
        self.main_frame.destroy()

        """ Destroy previous extension confirmations """
        if self.root.confirmation:
            self.root.confirmation.destroy()

        if EventController.insert(e):
            self.root.confirmation = Label(self.root, text="Event Added!", font="Courier 10")
        else:
            self.root.confirmation = Label(self.root, text="Sorry, something went wrong...", font="Courier 10")

        self.root.confirmation.grid(row=self.grid_row_start + 1, column=1, pady=10)
        self.root.extension = None
        self.callback()

    def _cancel_event(self):
        """ Destroy add event extension """
        self.main_frame.destroy()
        self.root.extension = None
        self.callback()
