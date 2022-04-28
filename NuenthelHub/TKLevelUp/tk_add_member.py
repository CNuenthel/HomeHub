from tkinter import Label, Tk, Toplevel, Frame, NSEW, PhotoImage, Button, CENTER, FLAT
from tkinter.ttk import Style
from tkinter.colorchooser import askcolor
from TKLevelUp.member import Member
from NuenthelHub.TKLevelUp.members.memberdbcontroller import MemberController
from NuenthelHub.supportmodules.modifiedwidgets import TextFilledEntry
from NuenthelHub.TKLevelUp.img.image_path import image_path

bg_color = "#909090"
border_color = "#9594B7"
font = "Roboto "
header_color = "#232323"
subtle_red = "#FDD0CC"
subtle_green = "#ccfdcc"


class TKAddMemberExtension:
    def __init__(self, root_window: Tk or Toplevel):
        """ Extension Attributes """
        self.root = root_window
        self.grid_row_start = root_window.grid_size()[1]
        self.column_count = root_window.grid_size()[0]
        self.user_color = None

        """ DB Handler """
        self.db = MemberController

        """ TTK Style """
        self.style = Style()
        self.style.configure("A.Button", font=font+"10 bold", background=bg_color)

        """ Internal Functions """
        self._create_main_frame()
        self._make_header()
        self._make_name_entry()
        self._make_color_selector()
        self._make_add_cancel_buttons()

    def _create_main_frame(self):
        """ Create a frame for add chore widgets """
        self.border_frame = Frame(self.root, bg=self.root["bg"])
        self.border_frame.grid(row=self.grid_row_start, column=0, columnspan=self.column_count, sticky=NSEW)
        self.main_frame = Frame(self.root, bg=bg_color)
        self.main_frame.grid(row=self.grid_row_start, column=0, columnspan=self.column_count, sticky=NSEW, padx=10,
                             pady=10)

    def _make_header(self):
        Label(
            self.main_frame, text="ADD MEMBER", font=font+"18 underline", bg=bg_color) \
            .pack(pady=8)

    def _make_name_entry(self):
        """ Creates title text filled entry """
        self.name_entry = TextFilledEntry(self.main_frame, "Name", justify=CENTER)
        self.name_entry.pack(pady=8)

    def _make_color_selector(self):
        """ Creates a button for color selector """
        self.color_btn = Button(self.main_frame, text="Choose Color", command=self._pick_color)

    def _make_add_cancel_buttons(self):
        """ Create add/cancel buttons """
        button_frame = Frame(self.main_frame, bg="#BDC1BE")
        button_frame.pack(pady=10)

        """ Create final add button """
        self.add_img = PhotoImage(file=image_path + "confirm.png")
        self.add = Button(button_frame, image=self.add_img, command=self._add_chore, relief=FLAT,
                          bg=bg_color)
        self.add.grid(row=0, column=0)

        """ Create cancel button """
        self.cancel_img = PhotoImage(file=image_path + "deny.png")
        self.cancel = Button(button_frame, image=self.cancel_img, command=self._cancel_event, relief=FLAT,
                             bg=bg_color)
        self.cancel.grid(row=0, column=1)

    # """ ________________________ BUTTON FUNCTIONS _________________________________________________________________"""

    def _add_chore(self):
        """ Add event to DB """
        name = self.name_entry.get()
        color = self.user_color

        if name:
            data = {
                "name": name,
                "color": color,
            }

            member = Member.create_from_dict(data)

            self.main_frame.destroy()

            if self.db.insert(member):
                self.root.confirmation = Label(self.root, text="Member Added!", font=font+"10", justify=CENTER)
            else:
                self.root.confirmation = Label(self.root, text="Sorry, something went wrong...", font=font+"10", justify=CENTER)

            self.root.confirmation.grid(row=self.grid_row_start+1, column=0, columnspan=self.column_count, pady=10)
            self.root.extension = None

    def _cancel_event(self):
        """ Destroy add event extension """
        self.main_frame.destroy()
        self.root.extension = None

    def _pick_color(self):
        self.user_color = askcolor(title="Color Selector")
        self.style.configure("A.Button", background=self.user_color)
