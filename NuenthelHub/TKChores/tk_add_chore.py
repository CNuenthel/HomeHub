from tkinter import NSEW, PhotoImage, CENTER
from tkinter.ttk import Combobox, Frame, Button, Label

from TKChores.chore import Chore
from NuenthelHub.TKChores.chore import ChoreController
from NuenthelHub.TKChores.img.image_path import image_path
from NuenthelHub.supportmodules.modifiedwidgets import TextFilledEntry

bg_color = "#909090"
border_color = "#9594B7"
font = "Roboto "
header_color = "#232323"
subtle_red = "#FDD0CC"
subtle_green = "#ccfdcc"


class TKAddChoreExtension:
    def __init__(self, root_frame: Frame, callback: callable, category):
        """ Extension Attributes """
        self.root = root_frame
        self.callback = callback
        self.category = category
        self.grid_row_start = root_frame.grid_size()[1]
        self.column_count = root_frame.grid_size()[0]
        self.add_chore = callback

        """ Internal Functions """
        self._create_main_frame()
        self._make_header()
        self._make_title_entry()
        self._make_add_cancel_buttons()

    def _create_main_frame(self):
        """ Create a frame for add chore widgets """
        self.main_frame = Frame(self.root, style="BG.TFrame")
        self.main_frame.grid(row=self.grid_row_start, column=0, sticky=NSEW, padx=10,
                             pady=10)

    def _make_header(self):
        Label(
            self.main_frame, text=f"Add {self.category} Chore", font="Courier 15", style="BG.TLabel") \
            .pack(pady=8)

    def _make_title_entry(self):
        """ Creates title text filled entry """
        self.title_entry = TextFilledEntry(self.main_frame, "Title", justify=CENTER)
        self.title_entry.pack(pady=8)

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

        if name and self.category != "Category":
            chore = Chore()
            chore.name = name
            chore.category = self.category
            chore.last_completed_by = None
            chore.complete = False

            ChoreController.insert(chore)

            self.callback(self.category)
            self.main_frame.destroy()

    def _cancel_event(self):
        """ Destroy add event extension """
        self.callback(None)
        self.main_frame.destroy()
