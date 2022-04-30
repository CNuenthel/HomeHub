from tkinter import Tk, NSEW, SUNKEN, BOTH, FLAT, GROOVE, PhotoImage
from tkinter.ttk import Frame, Style, Button, Label
from supportmodules import modifiedwidgets
from TKLevelUp import housemembersrpg as rpg
from TKCalendar import tkcalendar as tkc


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

        """ GUI Widgets """
        self.main_btn_widgets = []
        self.frames = []

        """ GUI Connections """
        self.tv_connected = "Disconnected"
        self.budget_connected = "Disconnected"

        """ Styles """
        self.style = Style(self)
        self.style.theme_use("clam")

        self.mod_styles = Style()
        self.mod_styles.configure("Header.TFrame", relief=SUNKEN)
        self.mod_styles.configure("Body.TFrame", relief=SUNKEN)
        self.mod_styles.configure("Main.TButton", background="white", width=20, relief=SUNKEN, foreground="black",
                             font="Roboto 20 bold")
        self.mod_styles.configure("Sheets.TButton", background="green", relief=FLAT)
        self.mod_styles.configure("Tv.TButton", background="green", relief=FLAT)

        """ Init GUI Frames """
        self.header_frame = Frame(self, style="Header.TFrame", relief=SUNKEN)
        self.header_frame.grid(row=0, column=0, padx=20, pady=20, sticky=NSEW)
        row_col_configure(self.header_frame, 1, row_config=False)

        self.body_frame = Frame(self, relief=SUNKEN, borderwidth=2, style="Body.TFrame")
        self.body_frame.grid(row=1, column=0, padx=20, pady=20, sticky=NSEW)
        row_col_configure(self.body_frame, 1)

        """ Set up home RPG """
        self.rpg_frame = Frame(self.header_frame)
        self.rpg_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)
        self.rpg = rpg.HomeRPG(self.rpg_frame)
        self.rpg.get_members()
        self.rpg.create_rpg_bars()
        row_col_configure(self.rpg_frame, 1, row_config=False)

        """Internal Functions"""
        self._create_main_button_frame()
        self._create_connection_buttons()
        self._create_calendar_button()
        self._create_budget_button()
        self._create_shopping_button()
        self._create_chores_button()
        self._create_todo_button()
        self._create_home_mtn_button()

        """ Modules """
        self.calendar = None

        """ Configure """
        row_col_configure(self.header_frame, 1, row_config=False)
        row_col_configure(self.main_button_frame, 1)
        row_col_configure(self.body_frame, 1)
        row_col_configure(self.rpg_frame, 1)
        row_col_configure(self, 1, row_index=1)

    def _sweep_widgets(self):
        for widget in self.main_btn_widgets:
            widget.grid_remove()

    def _repack_main(self):
        self.main_button_frame.grid(row=0, column=0, sticky=NSEW)

    def _create_main_button_frame(self):
        self.main_button_frame = Frame(self.body_frame)
        self.main_button_frame.grid(row=0, column=0, sticky=NSEW)

    def _create_connection_buttons(self):
        """ Sony Bravia connection visual """
        self.tv_connected_btn = Button(
            self.header_frame, text=f"TV {self.tv_connected}", style="Tv.TButton")
        self.tv_connected_btn.grid(row=0, column=1, padx=10, pady=10, sticky=NSEW)

        """ Google Sheets connection visual """
        self.sheets_connected_btn = Button(
            self.header_frame, text=f"Sheets {self.budget_connected}", style="Sheets.TButton")
        self.sheets_connected_btn.grid(row=0, column=2, padx=10, pady=10, sticky=NSEW)

    def _create_calendar_button(self):
        self.cal_png = PhotoImage(file="img/calendar.png")
        self.calendar_button = Button(self.main_button_frame, image=self.cal_png, text="Calendar", style="Main.TButton",
                                      command=self.show_calendar)
        self.calendar_button.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

    def _create_budget_button(self):
        self.bud_png = PhotoImage(file="img/budgeting.png")
        self.budget_button = Button(self.main_button_frame, image=self.bud_png, text="Budget", style="Main.TButton")
        self.budget_button.grid(row=0, column=1, padx=10, pady=10, sticky=NSEW)

    def _create_shopping_button(self):
        self.shop_png = PhotoImage(file="img/shopping-list.png")
        self.shopping_button = Button(self.main_button_frame, image=self.shop_png, text="Shopping List", style="Main.TButton")
        self.shopping_button.grid(row=0, column=2, padx=10, pady=10, sticky=NSEW)

    def _create_chores_button(self):
        self.chore_png = PhotoImage(file="img/bucket.png")
        self.chores_button = Button(self.main_button_frame, image=self.chore_png, text="Chores", style="Main.TButton")
        self.chores_button.grid(row=0, column=3, padx=10, pady=10, sticky=NSEW)

    def _create_todo_button(self):
        self.todo_button = Button(self.main_button_frame, text="To Do", style="Main.TButton")
        self.todo_button.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)

    def _create_home_mtn_button(self):
        self.mtn_png = PhotoImage(file="img/maintenance.png")
        self.home_mtn_button = Button(self.main_button_frame, image=self.mtn_png, text="Home Mtn", style="Main.TButton")
        self.home_mtn_button.grid(row=1, column=1, padx=10, pady=10, sticky=NSEW)

    """ _____________ Button Commands _______________________________________________________________________________"""

    def show_calendar(self):
        self._sweep_widgets()

        self.calendar = tkc.TKCalendar(self, callback=self._repack_main)


if __name__ == '__main__':
    RootGUI().mainloop()
