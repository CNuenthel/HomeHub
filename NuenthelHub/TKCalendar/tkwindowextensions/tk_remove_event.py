from tkinter import Label, Tk, Toplevel, S, Frame, NSEW, PhotoImage, Button, GROOVE, FLAT
from TKCalendar.events.eventdbcontroller import EventController
from TKCalendar.img.imgpath import image_path


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
        self.border_frame = Frame(self.root, bg=self.root["bg"])
        self.border_frame.grid(row=self.grid_row_start, column=0, columnspan=self.column_count, sticky=NSEW)
        self.main_frame = Frame(self.root, bg="#BDC1BE")
        self.main_frame.grid(row=self.grid_row_start, column=0, columnspan=self.column_count, sticky=NSEW, padx=10,
                             pady=10)

    def _make_header(self):
        """ Create Add Event header """
        Label(
            self.main_frame, text="REMOVE EVENT", font="Courier 18 underline", bg="#BDC1BE") \
            .grid(row=0, column=1, pady=5, sticky=S)

    def _get_event_data(self):
        """ Retrieves event data from DB """
        self.event = EventController.find_by_id(self.id)

    def _make_data_display(self):
        """ Displays event data in an extension"""
        event_data_frame = Frame(self.main_frame, bg="#D1D6D3", relief=GROOVE)
        event_data_frame.grid(row=1, column=1, padx=8, pady=8)
        e = self.event
        event_data = f"Title: {e.title}\n" \
                     f"Date: {e.month}/{e.day}/{e.year}\n" \
                     f"Time: {e.time_hours}:{e.time_minutes}\n" \
                     f"Category: {e.category}\n" \
                     f"Details: {e.details}" \

        Label(event_data_frame, bg="#D1D6D3", text=event_data, font="Helvetica 12") \
            .grid(row=0, column=0, ipady=20, ipadx=20)

    def _make_confirm_deny_buttons(self):
        """ Create final add button """
        self.confirm_img = PhotoImage(file=image_path+"confirm.png")
        self.add = Button(self.main_frame, image=self.confirm_img, command=self._remove_event, relief=FLAT,
                          bg="#BDC1BE")
        self.add.image = self.confirm_img
        self.add.grid(row=1, column=0)

        """ Create cancel button """
        self.deny_img = PhotoImage(file=image_path+"deny.png")
        self.deny = Button(self.main_frame, image=self.deny_img, command=self._cancel_event, relief=FLAT,
                           bg="#BDC1BE")
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

