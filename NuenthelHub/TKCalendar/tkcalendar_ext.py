from tkinter import Tk, Toplevel, E, NSEW, PhotoImage, CENTER, END, FLAT, GROOVE, S
from tkinter.ttk import Combobox, Style, Label, Frame, Button

from NuenthelHub.TKCalendar.event import Event, EventController
from NuenthelHub.supportmodules.modifiedwidgets import NumberOnlyCombobox, TextFilledEntry
from NuenthelHub.TKCalendar.img.imgpath import image_path


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
        self.border_frame = Frame(self.root, style="AddMain.TFrame")
        self.border_frame.grid(row=self.grid_row_start, column=0, columnspan=self.column_count, sticky=NSEW)
        self.main_frame = Frame(self.root, style="AddMain.TFrame")
        self.main_frame.grid(row=self.grid_row_start, column=0, columnspan=self.column_count, sticky=NSEW, padx=10,
                             pady=10)

    def _make_header(self):
        """ Create Add Event header """
        Label(
            self.main_frame, text="ADD EVENT", style="AddExt.TLabel", font="Roboto 18 underline") \
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
                                                background="white", style="ReqInfo.TCombobox")
        self.hour_selector.set("Hour")
        self.hour_selector.grid(row=0, column=0)

        minute_nums = ["00"]
        minute_nums.extend([str(num * 10) for num in range(1, 6)])
        self.minute_selector = NumberOnlyCombobox(time_frame, "Minutes", 2, values=minute_nums, justify=CENTER,
                                                  background="white", style="ReqInfo.TCombobox")
        self.minute_selector.set("00")
        self.minute_selector.grid(row=0, column=1, sticky=E)

        self.hour_selector.bind("<<ComboboxSelected>>", lambda e: self.main_frame.focus())
        self.minute_selector.bind("<<ComboboxSelected>>", lambda e: self.main_frame.focus())

    def _make_category_combobox(self):
        """ Create combobox to collect category """
        categories = ["S-Work", "C-Work", "Meeting", "Holiday", "Reminder"]
        self.category_selector = Combobox(self.main_frame, values=categories, justify=CENTER, style="Category.TCombobox")
        self.category_selector.pack(pady=8)
        self.category_selector.set("Category")
        self.category_selector.bind("<<ComboboxSelected>>", lambda e: self.main_frame.focus())

    def _make_details_entry(self):
        """ Create an entry to collect details """
        self.details_entry = TextFilledEntry(self.main_frame, "Details", justify=CENTER)
        self.details_entry.pack(pady=8)

    def _make_add_cancel_buttons(self):
        """ Create add/cancel buttons """
        button_frame = Frame(self.main_frame, style="AddMain.TFrame")
        button_frame.pack(pady=10)

        """ Create final add button """
        self.add_img = PhotoImage(file=image_path + "confirm.png")
        self.add = Button(button_frame, image=self.add_img, command=self._add_event, style="AddCancel.TButton")
        self.add.grid(row=0, column=0)

        """ Create cancel button """
        self.cancel_img = PhotoImage(file=image_path + "deny.png")
        self.cancel = Button(button_frame, image=self.cancel_img, command=self._cancel_event, style="AddCancel.TButton")
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

        if ev_dict["time_hours"] == "Hour" or ev_dict["time_minutes"] == "Minutes" or ev_dict["title"] == "Title":
            # Change required widgets red to show edit reqs
            self.add_style.configure("ReqInfo.TCombobox", fieldbackground="red")
            self.style.configure("ReqInfo.TEntry", background="red")

            self.warning = Label(self.main_frame, text="Please fill in required information.", style="ReqInfo.TLabel",
                                 font="Roboto 13")
            self.warning.pack()
            return

        """ Reconfigure red zones if triggered """
        self.add_style.configure("ReqInfo.TCombobox", fieldbackground="white")
        self.style.configure("ReqInfo.TEntry", background="white")

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
        if self.add_style:
            self.add_style.configure("ReqInfo.TCombobox", fieldbackground="white", background="white")
        self.main_frame.destroy()
        self.root.extension = None
        self.callback()


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

    def _create_main_frame(self):
        """ Create a frame for add event widgets """
        self.border_frame = Frame(self.root, style="AddMainBorder.TFrame")
        self.border_frame.grid(row=self.grid_row_start, column=0, columnspan=self.column_count, sticky=NSEW)
        self.main_frame = Frame(self.border_frame, style="AddMain.TFrame")
        self.main_frame.grid(row=self.grid_row_start, column=0, columnspan=self.column_count, sticky=NSEW, padx=10,
                             pady=10)

    def _make_header(self):
        """ Create Add Event header """
        Label(
            self.main_frame, text="CHANGE EVENT", font="Courier 18 underline", style="AddExt.TLabel") \
            .pack(pady=15)

    def _make_title_entry(self):
        self.title_entry = TextFilledEntry(self.main_frame, "Title", justify=CENTER)
        self.title_entry.pack(pady=8)

    def _make_time_widgets(self):
        """ Create time selection boxes """
        time_frame = Frame(self.main_frame)
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

    def _make_confirm_deny_buttons(self):
        """ Create add/cancel buttons """
        button_frame = Frame(self.main_frame, style="AddMain.TFrame")
        button_frame.pack(pady=8)

        """ Create final add button """
        self.confirm_img = PhotoImage(file=image_path + "confirm.png")
        self.confirm = Button(button_frame, image=self.confirm_img, command=self._change_event,
                              style="AddCancel.TButton")
        self.confirm.grid(row=0, column=0)

        """ Create cancel button """
        self.cancel_img = PhotoImage(file=image_path + "deny.png")
        self.cancel = Button(button_frame, image=self.cancel_img, command=self._cancel_event, style="AddCancel.TButton")
        self.cancel.grid(row=0, column=1)

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

    def _configure_rows_cols(self):
        """ Configure rows to 1:1 weight """
        [self.main_frame.rowconfigure(i, weight=1) for i in range(self.main_frame.grid_size()[1])]
        [self.main_frame.columnconfigure(i, weight=1) for i in range(self.main_frame.grid_size()[0])]

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
            self.warning = Label(self.main_frame, text="Please fill in required information.",
                                 style="ReqInfo.TLabel",
                                 font="Helvetica 13")
            self.warning.grid(row=6, column=0, pady=10)
            return

        """ Reconfigure red zones if triggered """
        self.title_entry.configure(style="TEntry")
        self.change_style.configure("ReqInfo.TCombobox", fieldbackground="white", background="white")

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
        self.main_frame.destroy()
        self.root.extension = None
        self.callback()


class TKRemoveEvent:
    """
    Extends an instantiated Tk or Toplevel window starting from the last grid row with
    additional widgets to remove Event data

    ...
    Parameters
    ----------
    root_window: TK or Toplevel
        The window to extend with Event data widgets
    id : int
        Id of event from event TinyDB
    callback : callable
        Callback for use on extension completion for desired updates to root window

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

        """ Internal Functions """
        self._create_main_frame()
        self._make_header()
        self._get_event_data()
        self._make_data_display()
        self._make_confirm_deny_buttons()
        self._configure_rows_cols()

    def _create_main_frame(self):
        """ Create a frame for add event widgets """
        self.border_frame = Frame(self.root, style="AddMain.TFrame")
        self.border_frame.grid(row=self.grid_row_start, column=0, columnspan=self.column_count, sticky=NSEW)
        self.main_frame = Frame(self.root, style="AddMain.TFrame")
        self.main_frame.grid(row=self.grid_row_start, column=0, columnspan=self.column_count, sticky=NSEW, padx=10,
                             pady=10)

    def _make_header(self):
        """ Create Add Event header """
        Label(
            self.main_frame, text="REMOVE EVENT", font="Courier 18 underline", style="AddExt.TLabel") \
            .grid(row=0, column=1, pady=5, sticky=S)

    def _get_event_data(self):
        """ Retrieves event data from DB """
        self.event = EventController.find_by_id(self.id)

    def _make_data_display(self):
        """ Displays event data in an extension"""
        event_data_frame = Frame(self.main_frame, style="DkGray.TFrame", relief=GROOVE)
        event_data_frame.grid(row=1, column=1, padx=8, pady=8)
        e = self.event
        event_data = f"Title: {e.title}\n" \
                     f"Date: {e.month}/{e.day}/{e.year}\n" \
                     f"Time: {e.time_hours}:{e.time_minutes}\n" \
                     f"Category: {e.category}\n" \
                     f"Details: {e.details}" \

        Label(event_data_frame, style="DkGray.TLabel", text=event_data, font="Helvetica 12") \
            .pack()

    def _make_confirm_deny_buttons(self):
        """ Create final add button """
        self.confirm_img = PhotoImage(file=image_path+"confirm.png")
        self.add = Button(self.main_frame, image=self.confirm_img, command=self._remove_event,
                          style="AddCancel.TButton")
        self.add.image = self.confirm_img
        self.add.grid(row=1, column=0)

        """ Create cancel button """
        self.deny_img = PhotoImage(file=image_path+"deny.png")
        self.deny = Button(self.main_frame, image=self.deny_img, command=self._cancel_event, style="AddCancel.TButton")
        self.deny.image = self.deny_img
        self.deny.grid(row=1, column=2)

    def _configure_rows_cols(self):
        """ Configure rows to 1:1 weight """
        for i in range(self.main_frame.grid_size()[1]):
            self.main_frame.rowconfigure(i, weight=1)
        for i in range(self.main_frame.grid_size()[0]):
            self.main_frame.columnconfigure(i, weight=1)

    """ _________________________ BUTTON FUNCTIONS __________________________________________________________________"""

    def _cancel_event(self):
        """ Destroy remove event extension """
        self.main_frame.destroy()
        self.root.extension = None
        self.callback()

    def _remove_event(self):
        """ Remove event from EventDB """
        if self.root.confirmation:
            self.root.confirmation.destroy()
        self.main_frame.destroy()

        if EventController.remove_doc(self.id):
            self.root.confirmation = Label(self.root, text="Event Removed", font="Courier 10")
        else:
            self.root.confirmation = Label(self.root, text="Sorry, something went wrong...", font="Courier 10")

        self.root.confirmation.grid(row=6, column=1, pady=10)
        self.root.extension = None
        self.callback()
