from functools import partial
from tkinter import Tk, FLAT, NSEW, GROOVE, StringVar, PhotoImage, DISABLED, ACTIVE, NE, NW, EW, OptionMenu, SUNKEN
from tkinter.ttk import Frame, OptionMenu, Label, Button

from NuenthelHub.TKChores.chore import ChoreController, Chore
from NuenthelHub.TKChores.img.image_path import image_path
from TKChores.tk_add_chore import TKAddChoreExtension

bg_color = "#909090"
border_color = "#9594B7"
font = "Roboto "
header_color = "#232323"
subtle_red = "#FDD0CC"
subtle_green = "#ccfdcc"


def row_col_configure(master: Tk or Frame, weight: int, col_index: int = 0, row_index: int = 0, row_config: bool = True,
                      col_config: bool = True):
    columns, rows = master.grid_size()
    if col_config:
        for i in range(col_index, columns):
            master.columnconfigure(i, weight=weight)
    if row_config:
        for i in range(row_index, rows):
            master.rowconfigure(i, weight=weight)


class TKChores:
    """ TKinter household chores manager """

    def __init__(self, master, style, callback: callable = None):
        super().__init__()

        """ Window Attributes """
        self.master = master
        self.callback = callback

        """ Chore Data """

        self.daily_chores = []
        self.weekly_chores = []
        self.monthly_chores = []

        self.extension = None
        self.confirmation = None

        self.rmv_chore_img = PhotoImage(file=image_path + "remove_chore.png")

        """ Styling """
        self.style = style

        # Frames]
        self.style.configure("BG.TFrame", background=bg_color, relief=SUNKEN, borderwidth=2)

        # Labels
        self.style.configure("Red.TLabel", background=subtle_red)
        self.style.configure("Grn.TLabel", background=subtle_green)

        # OptionMenu
        self.style.configure("Person.TOptionMenu", width=15, bg=bg_color, highlightthickness=0, relief=GROOVE)

        # Buttons
        self.style.configure("Disabled.TButton", state=DISABLED)
        self.style.configure("Rmv.TButton", background=bg_color, relief=FLAT)
        self.style.configure("BG.TButton", font="Roboto 15")

        """ Internal Functions """
        self._make_main_frame()
        self._make_daily_chore_window()
        self._make_weekly_chore_window()
        self._make_monthly_chore_window()
        self._configure_chores(True, True, True)
        self._make_box_headers()

        """ Configure Functions """
        row_col_configure(self.main_frame, 1, row_config=False)
        row_col_configure(self.daily_chore_frame, 1)
        row_col_configure(self.weekly_chore_frame, 1)
        row_col_configure(self.monthly_chore_frame, 1)

    def _make_main_frame(self):
        self.main_frame = Frame(self.master.body_frame)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW, columnspan=4, rowspan=2)

    def _make_add_chore_frame(self):
        self.add_chore_frame = Frame(self.main_frame)
        self.add_chore_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

    def _make_box_headers(self):
        Button(self.main_frame, text="Daily", style="BG.TButton", command=partial(self._add_chore, "Daily")) \
            .grid(row=0, column=0)
        Button(self.main_frame, text="Weekly", style="BG.TButton", command=partial(self._add_chore, "Weekly")) \
            .grid(row=0, column=1)
        Button(
            self.main_frame, text="Monthly", style="BG.TButton", command=partial(self._add_chore, "Monthly")) \
            .grid(row=0, column=2)

    def _make_daily_chore_window(self):
        """ Makes first chore frame for daily chore information """
        self.daily_chore_frame = Frame(self.main_frame, style="BG.TFrame")
        self.daily_chore_frame.grid(row=2, column=0, padx=10, pady=10, sticky=NW+NE)

    def _make_weekly_chore_window(self):
        """ Makes second chore frame for weekly chore information """
        self.weekly_chore_frame = Frame(self.main_frame, style="BG.TFrame")
        self.weekly_chore_frame.grid(row=2, column=1, padx=10, pady=10, sticky=NW+NE)

    def _make_monthly_chore_window(self):
        """ Makes third chore frame for monthly chore information """
        self.monthly_chore_frame = Frame(self.main_frame, style="BG.TFrame")
        self.monthly_chore_frame.grid(row=2, column=2, padx=10, pady=10, sticky=NW+NE)

    def _create_chore_widgets(self, master: Frame, om_command: callable, btn_command: callable, rmv_command: callable,
                              chore_list_out: list, i: int, chore: Chore):
        print(master)
        if chore.complete:
            lbl_style = "Grn.TLabel"
            state = DISABLED
            last_complete = chore.last_completed_by
        else:
            lbl_style = "Red.TLabel"
            state = ACTIVE
            last_complete = "Completed By"

        # Label
        lbl = Label(master, text=chore.name, font=font + "12", style=lbl_style,
                    relief=GROOVE, width=15)

        # Option Menu - complete by
        var1 = StringVar(self.master)
        person_om = OptionMenu(master, var1, *[last_complete, "Cody", "Sam"],
                               command=partial(om_command, i, chore.category))
        person_om.configure(state=state)

        # Button - complete
        complete_btn = Button(master, text="Complete", state=DISABLED,
                              command=partial(btn_command, i, chore.category))

        # Remove W. Chore Btn
        rmv_btn = Button(master, style="Rmv.TButton", state=state,
                         command=partial(rmv_command, i, chore.category),
                         image=self.rmv_chore_img)

        chore_list_out.append([lbl, person_om, complete_btn, rmv_btn, var1])

        lbl.grid(row=i, column=0, padx=10, pady=5, sticky=EW)
        person_om.grid(row=i, column=1, padx=3, pady=5, sticky=EW)
        complete_btn.grid(row=i, column=2, padx=3, pady=5, sticky=EW)
        rmv_btn.grid(row=i, column=3, padx=10, pady=5, sticky=EW)

    def _configure_chores(self, daily: bool = False, weekly: bool = False, monthly: bool = False):
        if daily:
            for i, chore in enumerate(ChoreController.find_by_element("category", "Daily")):
                self._create_chore_widgets(self.daily_chore_frame, self._bind_complete_btn_state_to_om,
                                           self._complete_chore, self._remove_chore, self.daily_chores, i, chore)
        if weekly:
            for i, chore in enumerate(ChoreController.find_by_element("category", "Weekly")):
                self._create_chore_widgets(self.weekly_chore_frame, self._bind_complete_btn_state_to_om,
                                           self._complete_chore, self._remove_chore, self.weekly_chores, i, chore)
        if monthly:
            for i, chore in enumerate(ChoreController.find_by_element("category", "Monthly")):
                self._create_chore_widgets(self.monthly_chore_frame, self._bind_complete_btn_state_to_om,
                                           self._complete_chore, self._remove_chore, self.monthly_chores, i, chore)

    @staticmethod
    def _configure_rows_cols(master):
        """ Configure rows and columns to 1:1 weight """
        for i in range(master.grid_size()[1]):
            master.rowconfigure(i, weight=1)
        for i in range(master.grid_size()[0]):
            master.columnconfigure(i, weight=1)

    """ ______________________________________Button Functions ________________________________________________"""

    def _complete_chore(self, *args):
        """Get completing person and chore name"""
        # Change Label Green and Disable Line
        list_ref = None
        match args[1]:
            case "Daily":
                list_ref = self.daily_chores
                self.daily_chores[args[0]][0].configure(style="Grn.TLabel")
                for widget in self.daily_chores[args[0]][1:-1]:
                    widget.configure(state=DISABLED)
            case "Weekly":
                list_ref = self.weekly_chores
                self.weekly_chores[args[0]][0].configure(style="Grn.TLabel")
                for widget in self.weekly_chores[args[0]][1:-1]:
                    widget.configure(state=DISABLED)
            case "Monthly":
                list_ref = self.monthly_chores
                self.monthly_chores[args[0]][0].configure(style="Grn.TLabel")
                for widget in self.monthly_chores[args[0]][1:-1]:
                    widget.configure(state=DISABLED)

        if not list_ref:
            raise KeyError(f"Chore type {args[1]} not returned from chore object")

        completed_by = list_ref[args[0]][-1].get()
        title = list_ref[args[0]][0]["text"]

        chore = ChoreController.find_by_element("name", title)[0]

        # Update doc element
        chore.last_completed_by = completed_by
        chore.complete = True

        ChoreController.update_doc(chore, chore.id)

    def _bind_complete_btn_state_to_om(self, *args):
        match args[1]:
            case "Daily":
                if args[1] == "Select":
                    self.daily_chores[args[0]][2].configure(state=DISABLED)
                    return
                self.daily_chores[args[0]][2].configure(state=ACTIVE)
            case "Weekly":
                if args[1] == "Select":
                    self.weekly_chores[args[0]][2].configure(state=DISABLED)
                    return
                self.weekly_chores[args[0]][2].configure(state=ACTIVE)
            case "Monthly":
                if args[1] == "Select":
                    self.monthly_chores[args[0]][2].configure(state=DISABLED)
                    return
                self.monthly_chores[args[0]][2].configure(state=ACTIVE)

    def _add_chore(self, duration: str):

        match duration:
            case "Daily":
                self.extension = TKAddChoreExtension(self.daily_chore_frame, self._callback_add_chore, duration)
            case "Weekly":
                self.extension = TKAddChoreExtension(self.weekly_chore_frame, self._callback_add_chore, duration)
            case "Monthly":
                self.extension = TKAddChoreExtension(self.monthly_chore_frame, self._callback_add_chore, duration)

    def _remove_chore(self, *args):
        match args[1]:
            case "Daily":
                title = self.daily_chores[args[0]][0]["text"]
                chore_id = ChoreController.find_by_element("name", title)[0].doc_id
                ChoreController.remove_doc(chore_id)
                for widget in self.daily_chores[args[0]][:-1]:
                    widget.destroy()
            case "Weekly":
                title = self.weekly_chores[args[0]][0]["text"]
                chore_id = ChoreController.find_by_element("name", title)[0].doc_id
                ChoreController.remove_doc(chore_id)
                for widget in self.weekly_chores[args[0]][:-1]:
                    widget.destroy()
            case "Monthly":
                title = self.monthly_chores[args[0]][0]["text"]
                chore_id = ChoreController.find_by_element("name", title)[0].doc_id
                ChoreController.remove_doc(chore_id)
                for widget in self.monthly_chores[args[0]][:-1]:
                    widget.destroy()

    def _callback_add_chore(self, chore_category):
        self.extension = None
        match chore_category:
            case "Daily":
                self.daily_chore_frame.destroy()
                self._make_daily_chore_window()
                self._configure_chores(daily=True)
            case "Weekly":
                self.weekly_chore_frame.destroy()
                self._make_daily_chore_window()
                self._configure_chores(weekly=True)
            case "Monthly":
                self.monthly_chore_frame.destroy()
                self._make_daily_chore_window()
                self._configure_chores(monthly=True)
