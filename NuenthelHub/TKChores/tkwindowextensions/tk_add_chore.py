from tkinter import Tk, Toplevel, NSEW, PhotoImage, CENTER
from tkinter.ttk import Combobox, Frame, Button, Label

from NuenthelHub.TKChores.chores.chore import Chore
from NuenthelHub.TKChores.chores.choredbcontroller import ChoreController
from NuenthelHub.TKChores.img.image_path import image_path
from NuenthelHub.supportmodules.modifiedwidgets import TextFilledEntry

bg_color = "#909090"
border_color = "#9594B7"
font = "Roboto "
header_color = "#232323"
subtle_red = "#FDD0CC"
subtle_green = "#ccfdcc"


class TKAddChoreExtension:
    def __init__(self, root_frame: Frame, root_window: Frame or Tk):
        """ Extension Attributes """
        self.root = root_frame
        self.main = root_window
        self.grid_row_start = root_frame.grid_size()[1]
        self.column_count = root_frame.grid_size()[0]

        """ DB Handler """
        self.db = ChoreController

        """ Internal Functions """
        self._create_main_frame()
        self._make_header()
        self._make_title_entry()
        self._make_category_combobox()
        self._make_add_cancel_buttons()

    def _create_main_frame(self):
        """ Create a frame for add chore widgets """
        self.border_frame = Frame(self.root)
        self.border_frame.grid(row=self.grid_row_start, column=0, columnspan=self.column_count, sticky=NSEW)
        self.main_frame = Frame(self.root, style="BG.TFrame")
        self.main_frame.grid(row=self.grid_row_start, column=0, columnspan=self.column_count, sticky=NSEW, padx=10,
                             pady=10)

    def _make_header(self):
        Label(
            self.main_frame, text="ADD CHORE", font="Courier 18 underline", style="BG.TLabel") \
            .pack(pady=8)

    def _make_title_entry(self):
        """ Creates title text filled entry """
        self.title_entry = TextFilledEntry(self.main_frame, "Title", justify=CENTER)
        self.title_entry.pack(pady=8)

    def _make_category_combobox(self):
        """ Create combobox to collect category """
        categories = ["Daily", "Weekly", "Monthly"]
        self.category_selector = Combobox(self.main_frame, values=categories, justify=CENTER, background="white",
                                          state="readonly")
        self.category_selector.pack(pady=8)
        self.category_selector.set("Category")
        self.category_selector.bind("<<ComboboxSelected>>", lambda e: self.main_frame.focus())

    def _make_add_cancel_buttons(self):
        """ Create add/cancel buttons """
        button_frame = Frame(self.main_frame, style="AddCancel.TFrame")
        button_frame.pack(pady=10)

        """ Create final add button """
        self.add_img = PhotoImage(file=image_path + "confirm.png")
        self.add = Button(button_frame, image=self.add_img, command=self._add_chore, style="Rmv.TButton")
        self.add.grid(row=0, column=0)

        """ Create cancel button """
        self.cancel_img = PhotoImage(file=image_path + "deny.png")
        self.cancel = Button(button_frame, image=self.cancel_img, command=self._cancel_event, style="Rmv.TButton")
        self.cancel.grid(row=0, column=1)

    """ _________________________ BUTTON FUNCTIONS __________________________________________________________________"""

    def _add_chore(self):
        """ Add event to DB """
        name = self.title_entry.get()
        category = self.category_selector.get()

        if name and category != "Category":
            data = {
                "name": name,
                "category": category,
                "last_completed_by": None,
                "complete": False
            }

            chore = Chore().create_from_dict(data)

            self.main_frame.destroy()

            if self.db.insert(chore, force=True):
                self.main.confirmation = Label(self.root, text="Chore Added!", font="Courier 10", justify=CENTER)
            else:
                self.main.confirmation = Label(self.root, text="Sorry, something went wrong...", font="Courier 10",
                                               justify=CENTER)

            self.main.confirmation.grid(row=self.grid_row_start + 1, column=0, columnspan=self.column_count, pady=10)
            self.main.extension = None

    def _cancel_event(self):
        """ Destroy add event extension """
        self.main_frame.destroy()
        self.main.extension = None
