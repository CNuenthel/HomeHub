from functools import partial
from tkinter import Tk, FLAT, NSEW, GROOVE, StringVar, PhotoImage, DISABLED, ACTIVE, W, OptionMenu, SUNKEN
from tkinter.ttk import Frame, OptionMenu, Label, Button

from NuenthelHub.TKChores.chorehandler import ChoreHandler
from NuenthelHub.TKChores.chore import ChoreController
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

        """ Supporting Classes"""
        self.ch = ChoreHandler()

        """ Chore Data """
        self.get_dailies = ChoreController.find_by_element("category", "Daily")
        self.get_weeklies = ChoreController.find_by_element("category", "Weekly")
        self.get_monthlies = ChoreController.find_by_element("category", "Monthly")

        self.daily_chores = []
        self.weekly_chores = []
        self.monthly_chores = []

        self.extension = None
        self.confirmation = None

        self.rmv_chore_img = PhotoImage(file=image_path + "remove_chore.png")

        """ Styling """
        self.style = style

        # Frames
        self.style.configure("Header.TFrame", background=header_color)
        self.style.configure("Border.TFrame", background=border_color)
        self.style.configure("BG.TFrame", background=bg_color, relief=SUNKEN, borderwidth=2)
        self.style.configure("AddCancel.TFrame", background="#BDC1BE")

        # Labels
        self.style.configure("Header.TLabel", background=header_color, foreground="white")
        self.style.configure("BG.TLabel", background=bg_color)
        self.style.configure("Red.TLabel", background=subtle_red)
        self.style.configure("Grn.TLabel", background=subtle_green)

        # OptionMenu
        self.style.configure("Person.TOptionMenu", width=15, bg=bg_color, highlightthickness=0, relief=GROOVE)

        # Buttons
        self.style.configure("Green.TButton", highlightcolor=subtle_green, relief=GROOVE, width=15, background=bg_color)
        self.style.configure("Rmv.TButton", background=bg_color, relief=FLAT)

        """ Internal Functions """
        self._make_main_frame()
        self._make_add_chore_frame()
        self._make_add_chore_button()
        self._make_daily_chore_window()
        self._make_weekly_chore_window()
        self._make_monthly_chore_window()
        self._make_box_headers()

        """ Configure Functions """
        self._configure_chores(self.daily_chore_frame, self.get_dailies, self._open_daily_chores_om,
                               self._complete_daily_chore, self._remove_daily_chore, self.daily_chores)
        self._configure_chores(self.weekly_chore_frame, self.get_weeklies, self._open_weekly_chores_om,
                               self._complete_weekly_chore, self._remove_daily_chore, self.weekly_chores)
        self._configure_chores(self.monthly_chore_frame, self.get_monthlies, self._open_monthly_chores_om,
                               self._complete_monthly_chore, self._remove_monthly_chore, self.monthly_chores)

        row_col_configure(self.main_frame, 1, row_config=False)
        row_col_configure(self.add_chore_frame, 1, row_config=False)
        row_col_configure(self.daily_chore_frame, 1)
        row_col_configure(self.weekly_chore_frame, 1)
        row_col_configure(self.monthly_chore_frame, 1)

    def _make_main_frame(self):
        self.main_frame = Frame(self.master.body_frame)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW, columnspan=4, rowspan=2)

    def _make_add_chore_frame(self):
        self.add_chore_frame = Frame(self.main_frame)
        self.add_chore_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

    def _make_add_chore_button(self):
        self.add_chore_btn = Button(self.add_chore_frame, text="Add Chore", command=self._add_chore)
        self.add_chore_btn.grid(row=0, column=0, padx=10, columnspan=3, pady=10, sticky=NSEW)

    def _make_box_headers(self):
        Label(self.daily_chore_frame, text="Daily", font=font + "15 bold", style="BG.TLabel", anchor=W)\
            .grid(row=0, column=0)
        Label(self.weekly_chore_frame, text="Weekly", font=font + "15 bold", style="BG.TLabel", anchor=W)\
            .grid(row=0, column=0)
        Label(
            self.monthly_chore_frame, text="Monthly", font=font + "15 bold", style="BG.TLabel", anchor=W)\
            .grid(row=0, column=0)

    def _make_daily_chore_window(self):
        """ Makes first chore frame for daily chore information """
        self.daily_chore_frame = Frame(self.main_frame, style="BG.TFrame")
        self.daily_chore_frame.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)

    def _make_weekly_chore_window(self):
        """ Makes second chore frame for weekly chore information """
        self.weekly_chore_frame = Frame(self.main_frame, style="BG.TFrame")
        self.weekly_chore_frame.grid(row=1, column=1, padx=10, pady=10, sticky=NSEW)

    def _make_monthly_chore_window(self):
        """ Makes third chore frame for monthly chore information """
        self.monthly_chore_frame = Frame(self.main_frame, style="BG.TFrame")
        self.monthly_chore_frame.grid(row=1, column=2, padx=10, pady=10, sticky=NSEW)

    def _configure_chores(self, master, chore_list_in, om_command, btn_command, rmv_command, chore_list_out):
        print(chore_list_in)
        for i, chore in enumerate(chore_list_in):

            if chore["complete"]:
                lbl_style = "Grn.TLabel"
            else:
                lbl_style = "Red.TLabel"

            # Label
            lbl = Label(master, text=chore["name"], font=font + "12", style=lbl_style,
                        relief=GROOVE,
                        width=15)

            # Option Menu - complete by
            var1 = StringVar(self.master)
            var1.set("Select")
            person_om = OptionMenu(master, var1, *["Select", "Cody", "Sam"],
                                   command=partial(om_command, i))

            # Button - complete
            complete_btn = Button(master, style="Green.TButton", text="Complete",
                                  command=partial(btn_command, i))

            # Remove W. Chore Btn
            rmv_btn = Button(master, style="Rmv.TButton",
                             command=partial(rmv_command, i),
                             image=self.rmv_chore_img)

            chore_list_out.append([lbl, person_om, complete_btn, rmv_btn, var1])

            lbl.grid(row=i, column=0, padx=3, pady=5)
            person_om.grid(row=i, column=1, padx=3, pady=5)
            complete_btn.grid(row=i, column=2, padx=3, pady=5)
            rmv_btn.grid(row=i, column=3, padx=3, pady=5)


    @staticmethod
    def _configure_rows_cols(master):
        """ Configure rows and columns to 1:1 weight """
        for i in range(master.grid_size()[1]):
            master.rowconfigure(i, weight=1)
        for i in range(master.grid_size()[0]):
            master.columnconfigure(i, weight=1)

    """ ______________________________________Button Functions ________________________________________________"""

    def _open_daily_chores_om(self, *args):
        if args[1] == "Select":
            self.daily_chores[args[0]][2].configure(state=DISABLED)
            return
        self.daily_chores[args[0]][2].configure(state=ACTIVE)

    def _complete_daily_chore(self, *args):
        completed_by = self.daily_chores[args[0]][-1].get()
        title = self.daily_chores[args[0]][0]["text"]
        chore_id = ChoreController.find_by_element("name", title)[0].doc_id
        ChoreController.update_doc_element("complete", True, chore_id)

        self.daily_chores[args[0]][0].configure(style="Grn.TLabel")

        for widget in self.daily_chores[args[0]][1:-1]:
            widget.configure(state=DISABLED)

        print(completed_by)

    def _open_weekly_chores_om(self, *args):
        if args[1] == "Select":
            self.weekly_chores[args[0]][2].configure(state=DISABLED)
            return
        self.weekly_chores[args[0]][2].configure(state=ACTIVE)

    def _complete_weekly_chore(self, *args):
        completed_by = self.weekly_chores[args[0]][-1].get()
        title = self.weekly_chores[args[0]][0]["text"]
        chore_id = ChoreController.find_by_element("name", title)[0].doc_id
        ChoreController.update_doc_element("complete", True, chore_id)

        self.weekly_chores[args[0]][0].configure(style="Grn.TLabel")

        for widget in self.weekly_chores[args[0]][1:-1]:
            widget.configure(state=DISABLED)
        print(completed_by)

    def _open_monthly_chores_om(self, *args):
        if args[1] == "Select":
            self.monthly_chores[args[0]][2].configure(state=DISABLED)
            return
        self.monthly_chores[args[0]][2].configure(state=ACTIVE)

    def _complete_monthly_chore(self, *args):
        completed_by = self.monthly_chores[args[0]][-1].get()
        title = self.monthly_chores[args[0]][0]["text"]
        chore_id = ChoreController.find_by_element("name", title)[0].doc_id
        ChoreController.update_doc_element("complete", True, chore_id)

        self.monthly_chores[args[0]][0].configure(style="Grn.TLabel")

        for widget in self.monthly_chores[args[0]][1:-1]:
            widget.configure(state=DISABLED)
        print(completed_by)

    def _add_chore(self):
        if not self.extension:
            self.confirmation.destroy() if self.confirmation else None
            self.extension = TKAddChoreExtension(self.add_chore_frame, self._configure_callback)

    def _remove_daily_chore(self, *args):
        title = self.daily_chores[args[0]][0]["text"]
        chore_id = ChoreController.find_by_element("name", title)[0].doc_id
        if ChoreController.remove_doc(chore_id):
            print("Chore removed")
        for widget in self.daily_chores[args[0]][:-1]:
            widget.destroy()

    def _remove_weekly_chore(self, *args):
        title = self.weekly_chores[args[0]][0]["text"]
        chore_id = ChoreController.find_by_element("name", title)[0].doc_id
        ChoreController.remove_doc(chore_id)
        for widget in self.weekly_chores[args[0]][:-1]:
            widget.destroy()

    def _remove_monthly_chore(self, *args):
        title = self.monthly_chores[args[0]][0]["text"]
        chore_id = ChoreController.find_by_element("name", title)[0].doc_id
        ChoreController.remove_doc(chore_id)
        for widget in self.monthly_chores[args[0]][:-1]:
            widget.destroy()

    def _configure_callback(self, category: str):
        pass

