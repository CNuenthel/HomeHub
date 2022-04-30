from tkinter import Tk, Toplevel, E, NSEW, PhotoImage, CENTER, END, FLAT, GROOVE, S
from tkinter.ttk import Combobox, Style, Label, Frame, Button

from NuenthelHub.TKCalendar.event import Event, EventController
from NuenthelHub.supportmodules.modifiedwidgets import NumberOnlyCombobox, TextFilledEntry
from NuenthelHub.TKCalendar.img.imgpath import image_path


def row_col_configure(master: Tk or Frame, weight: int, col_index: int = 0, row_index: int = 0, row_config: bool = True, col_config: bool = True):
    columns, rows = master.grid_size()
    if col_config:
        for i in range(col_index, columns):
            master.columnconfigure(i, weight=weight)
    if row_config:
        for i in range(row_index, rows):
            master.rowconfigure(i, weight=weight)


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
        self.add_style = None

        """ Styling """
        self.style = Style(self.root)
        self.style.configure("AddMainBorder.TFrame", background="#333333")
        self.style.configure("AddMain.TFrame", background="#777777")
        self.style.configure("AddExt.TLabel", background="#777777")
        self.style.configure("ReqInfo.TCombobox", fieldbackground="white", background="white")
        self.style.configure("Category.TCombobox", background="white")
        self.style.configure("AddCancel.TButton", background="white", relief=GROOVE)
        self.style.configure("AddConfirm.TLabel", background="white")
        self.style.configure("ReqInfo.TLabel", background="white", foreground="red")
        self.style.configure("ReqInfoRed.TCombobox", fieldbackground="red", background="white")
        self.style.configure("ReqInfoNorm.TCombobox", fieldbackground="white", background="white")
        self.style.configure("AddExt.TFrame", background="#333333")

        """ Internal Functions """
        self._create_main_frame()
        self._make_header()
        self._make_title_entry()
        self._make_time_widgets()
        self._make_category_combobox()
        self._make_details_entry()
        self._make_add_cancel_buttons()
        row_col_configure(self.main_frame, 1)
        row_col_configure(self.border_frame, 1)

    def _create_main_frame(self):
        """ Create a frame for add event widgets """
        self.main_frame = Frame(self.root, style="AddMainBorder.TFrame")
        self.main_frame.grid(row=self.grid_row_start, column=0, columnspan=self.column_count, sticky=NSEW)
        self.border_frame = Frame(self.main_frame, style="AddMain.TFrame")
        self.border_frame.grid(row=self.grid_row_start, column=0, columnspan=2, sticky=NSEW, padx=10,
                               pady=10)

    def _make_header(self):
        """ Create Add Event header """
        Label(
            self.border_frame, text="Add Event", style="AddExt.TLabel", font="Roboto 16") \
            .pack(pady=8)

    def _make_title_entry(self):
        """ Creates title text filled entry """
        self.title_entry = TextFilledEntry(self.border_frame, "Title", justify=CENTER)
        self.title_entry.pack(pady=8)

    def _make_time_widgets(self):
        """ Create time selection boxes """
        time_frame = Frame(self.border_frame)
        time_frame.pack(pady=8)

        hour_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
                     14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

        self.hour_selector = NumberOnlyCombobox(time_frame, "Hour", 2, values=hour_nums, justify=CENTER,
                                                background="white", style="ReqInfo.TCombobox")
        self.hour_selector.set("Hour")
        self.hour_selector.grid(row=0, column=0)

        minute_nums = ["00"]
        minute_nums.extend([str(num * 10) for num in range(1, 6)])
        self.minute_selector = NumberOnlyCombobox(time_frame, "Minutes", 2, values=minute_nums, justify=CENTER,
                                                  background="white", style="ReqInfo.TCombobox")
        self.minute_selector.set("00")
        self.minute_selector.grid(row=0, column=1, sticky=E)

        self.hour_selector.bind("<<ComboboxSelected>>", lambda e: self.border_frame.focus())
        self.minute_selector.bind("<<ComboboxSelected>>", lambda e: self.border_frame.focus())

    def _make_category_combobox(self):
        """ Create combobox to collect category """
        categories = ["S-Work", "C-Work", "Meeting", "Holiday", "Reminder"]
        self.category_selector = Combobox(self.border_frame, values=categories, justify=CENTER, style="Category.TCombobox")
        self.category_selector.pack(pady=8)
        self.category_selector.set("Category")
        self.category_selector.bind("<<ComboboxSelected>>", lambda e: self.border_frame.focus())

    def _make_details_entry(self):
        """ Create an entry to collect details """
        self.details_entry = TextFilledEntry(self.border_frame, "Details", justify=CENTER)
        self.details_entry.pack(pady=8)

    def _make_add_cancel_buttons(self):
        """ Create add/cancel buttons """
        button_frame = Frame(self.border_frame, style="AddMain.TFrame")
        button_frame.pack(pady=10)

        """ Create final add button """
        self.add_img = PhotoImage(file=image_path + "confirm.png")
        self.add = Button(button_frame, image=self.add_img, command=self._add_event, style="AddCancel.TButton")
        self.add.grid(row=0, column=0, padx=5)

        """ Create cancel button """
        self.cancel_img = PhotoImage(file=image_path + "deny.png")
        self.cancel = Button(button_frame, image=self.cancel_img, command=self._cancel_event, style="AddCancel.TButton")
        self.cancel.grid(row=0, column=1, padx=5)

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

        if ev_dict["time_hours"] == "Hour" or ev_dict["time_minutes"] == "Minutes" or ev_dict["title"] == "Title":
            # Change required widgets red to show edit reqs
            self.style.configure("ReqInfo.TCombobox", fieldbackground="red")
            self.root.style.configure("ReqInfo.TEntry", background="red")

            self.warning = Label(self.border_frame, text="Please fill in required information.", style="ReqInfo.TLabel",
                                 font="Roboto 13")
            self.warning.pack()
            return

        """ Reconfigure red zones if triggered """
        self.style.configure("ReqInfo.TCombobox", fieldbackground="white")
        self.root.style.configure("ReqInfo.TEntry", background="white")

        e = Event.create_from_dict(ev_dict)

        """ Destroy extension """
        self.main_frame.destroy()

        """ Destroy previous extension confirmations """
        if self.root.confirmation:
            self.root.confirmation.destroy()

        if EventController.insert(e):
            self.root.confirmation = Label(self.root, text="Event Added!", font="Courier 10", style="AddConfirm.TLabel")
        else:
            self.root.confirmation = Label(self.root, text="Sorry, something went wrong...", font="Courier 10", style="AddConfirm.TLabel")

        self.root.confirmation.grid(row=self.grid_row_start + 1, column=1, pady=10)
        self.root.extension = None
        self.callback()

    def _cancel_event(self):
        """ Destroy add event extension """
        self.main_frame.destroy()
        self.root.extension = None


class TKChangeEvent:
    """
    Extends an instantiated Tk or Toplevel window starting from the last grid row with
    additional widgets to change Event data

    ...
    Parameters
    ----------
    root_window: TK or Toplevel
        The window to extend with Event data widgets
    id : int
        Id of event from event TinyDB
    callback : callable
        Callback for use on extension completion for desired updates

    """

    def __init__(self, root_window: Tk or Toplevel, id: int, callback: callable = None):
        """ Extension Attributes """
        self.root = root_window
        self.id = id
        self.event = None
        self.grid_row_start = root_window.grid_size()[1]
        self.column_count = root_window.grid_size()[0]
        self.callback = callback

        """ Image Holder """
        self.confirm = None
        self.deny = None

        """ Styling """
        self.style = Style(self.root)
        self.style.theme_use("winnative")
        self.style.configure("AddMainBorder.TFrame", background="#333333")
        self.style.configure("AddMain.TFrame", background="#777777")
        self.style.configure("AddExt.TLabel", background="#777777")
        self.style.configure("ReqInfo.TCombobox", fieldbackground="white", background="white")
        self.style.configure("Category.TCombobox", background="white")
        self.style.configure("AddCancel.TButton", background="white", relief=GROOVE)
        self.style.configure("AddConfirm.TLabel", background="white")
        self.style.configure("ReqInfo.TLabel", background="white", foreground="red")
        self.style.configure("ReqInfoRed.TCombobox", fieldbackground="red", background="white")
        self.style.configure("ReqInfoNorm.TCombobox", fieldbackground="white", background="white")
        self.style.configure("AddExt.TFrame", background="#333333")

        """ Internal Functions """
        self._create_main_frame()
        self._make_header()
        self._make_title_entry()
        self._make_time_widgets()
        self._make_category_combobox()
        self._make_details_entry()
        self._make_confirm_deny_buttons()
        self._get_event_data()
        self._configure_time()
        self._configure_title()
        self._configure_category()
        self._configure_details()
        row_col_configure(self.main_frame, 1)
        row_col_configure(self.border_frame, 1)

    def _create_main_frame(self):
        """ Create a frame for add event widgets """
        self.main_frame = Frame(self.root, style="AddMainBorder.TFrame")
        self.main_frame.grid(row=self.grid_row_start, column=0, columnspan=self.column_count, sticky=NSEW)
        self.border_frame = Frame(self.main_frame, style="AddMain.TFrame")
        self.border_frame.grid(row=self.grid_row_start, column=0, columnspan=2, sticky=NSEW, padx=10,
                               pady=10)

    def _make_header(self):
        """ Create Add Event header """
        Label(
            self.border_frame, text="Change Event", font="Roboto 16", style="AddExt.TLabel") \
            .pack(pady=15)

    def _make_title_entry(self):
        self.title_entry = TextFilledEntry(self.border_frame, "Title", justify=CENTER)
        self.title_entry.pack(pady=8)

    def _make_time_widgets(self):
        """ Create time selection boxes """
        time_frame = Frame(self.border_frame)
        time_frame.pack(pady=8)

        hour_nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
                     14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

        self.hour_selector = NumberOnlyCombobox(time_frame, "Hour", 2, values=hour_nums, justify=CENTER,
                                                background="white", style="ReqInfo.TCombobox")
        self.hour_selector.set("Hour")
        self.hour_selector.grid(row=0, column=0)

        minute_nums = ["00"]
        minute_nums.extend([str(num * 10) for num in range(1, 6)])
        self.minute_selector = NumberOnlyCombobox(time_frame, "Minutes", 2, values=minute_nums, justify=CENTER,
                                                  background="white", style="ReqInfo.TCombobox")
        self.minute_selector.set("00")
        self.minute_selector.grid(row=0, column=1, sticky=E)

        self.hour_selector.bind("<<ComboboxSelected>>", lambda e: self.border_frame.focus())
        self.minute_selector.bind("<<ComboboxSelected>>", lambda e: self.border_frame.focus())

    def _make_category_combobox(self):
        """ Create combobox to collect category """
        categories = ["Work", "Meeting", "Holiday", "Reminder"]
        self.category_selector = Combobox(self.border_frame, values=categories, justify=CENTER, background="white")
        self.category_selector.pack(pady=8)
        self.category_selector.set("Category")
        self.category_selector.bind("<<ComboboxSelected>>", lambda e: self.border_frame.focus())

    def _make_details_entry(self):
        """ Create an entry to collect details """
        self.details_entry = TextFilledEntry(self.border_frame, "Details", justify=CENTER)
        self.details_entry.pack(pady=8)

    def _make_confirm_deny_buttons(self):
        """ Create add/cancel buttons """
        button_frame = Frame(self.border_frame, style="AddMain.TFrame")
        button_frame.pack(pady=8)

        """ Create final add button """
        self.confirm_img = PhotoImage(file=image_path + "confirm.png")
        self.confirm = Button(button_frame, image=self.confirm_img, command=self._change_event,
                              style="AddCancel.TButton")
        self.confirm.grid(row=0, column=0, padx=5)

        """ Create cancel button """
        self.cancel_img = PhotoImage(file=image_path + "deny.png")
        self.cancel = Button(button_frame, image=self.cancel_img, command=self._cancel_event, style="AddCancel.TButton")
        self.cancel.grid(row=0, column=1, padx=5)

    def _get_event_data(self):
        """ Retrieves event data from DB """
        self.event = EventController.find_by_id(self.id)

    def _configure_title(self):
        """ Configures title entry to show event title"""
        self.title_entry.delete(0, END)
        self.title_entry.insert(0, self.event.title)

    def _configure_time(self):
        """ Configures time entry to show event hours/minutes """
        self.hour_selector.set(self.event.time_hours)
        self.minute_selector.set(self.event.time_minutes)

    def _configure_category(self):
        """ Configures category selector to show event category """
        if self.event.category:
            self.category_selector.set(self.event.category)

    def _configure_details(self):
        """ Configures details entry to show event details """
        if self.event.details:
            self.details_entry.delete(0, END)
            self.details_entry.insert(0, self.event.details)


    """ _________________________ BUTTON FUNCTIONS __________________________________________________________________"""

    def _change_event(self):
        """ Update DB Event """
        ev_dict = {
            "title": self.title_entry.get(),
            "details": self.details_entry.get(),
            "time_hours": self.hour_selector.get(),
            "time_minutes": self.minute_selector.get(),
            "category": self.category_selector.get()
        }

        if ev_dict["time_hours"] == "Hour" or ev_dict["time_minutes"] == "Minutes" or ev_dict["title"] == "Title":
            self.title_entry.configure(style="Required.TEntry")
            self.warning = Label(self.border_frame, text="Please fill in required information.",
                                 style="ReqInfo.TLabel",
                                 font="Helvetica 13")
            self.warning.grid(row=6, column=0, pady=10)
            return

        """ Reconfigure red zones if triggered """
        self.title_entry.configure(style="TEntry")
        self.root.style.configure("ReqInfo.TCombobox", fieldbackground="white", background="white")

        event = Event.create_from_dict(ev_dict)

        self.main_frame.destroy()
        if EventController.update_doc(event, self.id):
            self.root.confirmation = Label(self.root, text="Event Updated!", font="Roboto 10")
        else:
            self.root.confirmation = Label(self.root, text="Sorry, something went wrong...", font="Roboto 10")

        self.root.confirmation.grid(row=self.grid_row_start + 1, column=1, pady=10)
        self.root.extension = None
        self.callback()

    def _cancel_event(self):
        """ Destroy add event extension """
        self.main_frame.grid_forget()
        self.root.extension = None

