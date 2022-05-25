from tkinter import Tk, NSEW, SUNKEN, TOP, FLAT, PhotoImage, LEFT, BOTH
from tkinter.ttk import Frame, Style, Button
from tkinter import font

from TKLevelUp import housemembersrpg, member
from TKCalendar import tkcalendar as tkc
from TKBudget import tkbudget as tkb
from TKChores import tkchores as tkchore
import threading


def row_col_configure(master: Tk or Frame, weight: int, col_index: int = 0, row_index: int = 0, row_config: bool = True,
                      col_config: bool = True):
    columns, rows = master.grid_size()
    if col_config:
        for i in range(col_index, columns):
            master.columnconfigure(i, weight=weight)
    if row_config:
        for i in range(row_index, rows):
            master.rowconfigure(i, weight=weight)


class RootGUI(Tk):
    """ Creates Root Window GUI """

    def __init__(self):
        super().__init__()
        self.title("Nuenthel Hub")
        self.configure(background="white")
        self.resizable(True, True)
        self.minsize(width=1500, height=900)

        """ RPG Players """
        self.home_rpg_players = []

        """ GUI Widgets """
        self.main_btn_widgets = []
        self.frames = []

        """ GUI Connections """
        self.tv_connected = "Disconnected"
        self.budget_connected = "Disconnected"

        """ Styles """
        self.style = Style(self)
        self.style.theme_use("vista")
        self.font = font.Font(family="Roboto", size=20, weight="bold")

        # self.mod_styles = Style()
        self.style.configure("Header.TFrame", relief=SUNKEN)
        self.style.configure("Body.TFrame", relief=SUNKEN)
        self.style.configure("Main.TButton", background="white", width=20, relief=SUNKEN, foreground="black")
        self.style.configure("Sheets.TButton", background="green", relief=FLAT)
        self.style.configure("Tv.TButton", background="green", relief=FLAT)

        """ Init GUI Frames """
        self.header_frame = Frame(self, style="Header.TFrame", relief=SUNKEN)
        self.header_frame.grid(row=0, column=0, padx=20, pady=20, sticky=NSEW)
        row_col_configure(self.header_frame, 1, row_config=False)

        self.body_frame = Frame(self, relief=SUNKEN, borderwidth=2, style="Body.TFrame")
        self.body_frame.grid(row=1, column=0, padx=20, pady=20, sticky=NSEW)
        row_col_configure(self.body_frame, 1)

        """Internal Functions"""
        self._create_main_button_frame()
        self._create_rpg_frame()
        self._create_rpg_players()
        self._create_connection_buttons()
        self._create_calendar_button()
        self._create_budget_button()
        self._create_shopping_button()
        self._create_chores_button()
        self._create_tv_button()
        self._create_home_mtn_button()

        """ Modules """
        self.calendar = None
        self.budget = None
        self.chores = None
        self.tv_remote = None

        """ Configure """
        row_col_configure(self.header_frame, 1, row_config=False)
        row_col_configure(self.main_button_frame, 1)
        row_col_configure(self.body_frame, 1)
        row_col_configure(self.rpg_frame, 1)
        row_col_configure(self, 1, row_index=1)

    @staticmethod
    def threading(func: callable, *args):
        t1 = threading.Thread(target=func, args=args)
        t1.start()

    def _sweep_widgets(self):
        for widget in self.main_btn_widgets:
            widget.grid_remove()

    def _repack_main(self):
        self.main_button_frame.grid(row=0, column=0, sticky=NSEW)

    def _create_main_button_frame(self):
        self.main_button_frame = Frame(self.body_frame)
        self.main_button_frame.grid(row=0, column=0, sticky=NSEW)

    def _create_rpg_frame(self):
        self.rpg_frame = Frame(self.header_frame)
        self.rpg_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

    def _create_rpg_players(self):
        for house_member in member.MemberController.find_all():
            player = housemembersrpg.HomeRPGPlayer(house_member, self.style)
            xp_bar = player.create_xp_bar(self.rpg_frame)
            xp_bar.pack(side=LEFT, expand=True, fill=BOTH, padx=5)
            self.home_rpg_players.append(player)

    def _create_connection_buttons(self):
        """ Sony Bravia connection visual """
        self.tv_connected_btn = Button(
            self.header_frame, text=f"TV {self.tv_connected}", style="Tv.TButton", compound=TOP)
        self.tv_connected_btn.grid(row=0, column=1, padx=10, pady=10, sticky=NSEW)

        """ Google Sheets connection visual """
        self.sheets_connected_btn = Button(
            self.header_frame, text=f"Sheets {self.budget_connected}", style="Sheets.TButton")
        self.sheets_connected_btn.grid(row=0, column=2, padx=10, pady=10, sticky=NSEW)

    def _create_calendar_button(self):
        self.cal_png = PhotoImage(file="img/calendar.png")
        self.calendar_button = Button(self.main_button_frame, image=self.cal_png, text="Calendar", style="Main.TButton",
                                      command=self.show_calendar, compound=TOP)
        self.calendar_button.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

    def _create_budget_button(self):
        self.bud_png = PhotoImage(file="img/budgeting.png")
        self.budget_button = Button(self.main_button_frame, image=self.bud_png, text="Budget", style="Main.TButton",
                                    command=self.show_budget, compound=TOP)
        self.budget_button.grid(row=0, column=1, padx=10, pady=10, sticky=NSEW)

    def _create_shopping_button(self):
        self.shop_png = PhotoImage(file="img/shopping-list.png")
        self.shopping_button = Button(self.main_button_frame, image=self.shop_png, text="Shopping List",
                                      style="Main.TButton", compound=TOP)
        self.shopping_button.grid(row=0, column=2, padx=10, pady=10, sticky=NSEW)

    def _create_chores_button(self):
        self.chore_png = PhotoImage(file="img/bucket.png")
        self.chores_button = Button(self.main_button_frame, image=self.chore_png, text="Chores", style="Main.TButton",
                                    command=self.show_chores, compound=TOP)
        self.chores_button.grid(row=0, column=3, padx=10, pady=10, sticky=NSEW)

    def _create_tv_button(self):
        self.tv_png = PhotoImage(file="img/tv.png")
        self.tv_button = Button(self.main_button_frame, image=self.tv_png, text="Sony Bravia", style="Main.TButton",
                                compound=TOP)
        self.tv_button.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)

    def _create_home_mtn_button(self):
        self.mtn_png = PhotoImage(file="img/maintenance.png")
        self.home_mtn_button = Button(self.main_button_frame, image=self.mtn_png, style="Main.TButton", compound=TOP,
                                      text="Home Mtn")
        self.home_mtn_button.grid(row=1, column=1, padx=10, pady=10, sticky=NSEW)

    """ _____________ Button Commands _______________________________________________________________________________"""

    def show_calendar(self):
        self._sweep_widgets()

        if self.calendar:
            self.calendar.repack_module()
            return

        self.calendar = tkc.TKCalendar(master=self, style=self.style, callback=self._repack_main)

    def show_budget(self):
        self._sweep_widgets()

        if self.budget:
            self.budget.repack_module()
            return

        self.budget = tkb.TKBudget(master=self, style=self.style,
                                   callback=self._repack_main)

    def show_chores(self):
        self._sweep_widgets()

        if self.chores:
            self.chores.repack_module()
            return

        self.chores = tkchore.TKChores(master=self, style=self.style, callback=self._repack_main)


if __name__ == '__main__':
    RootGUI().mainloop()
