from tkinter import Tk, NSEW, SUNKEN
from tkinter.ttk import Frame, Style, Button, LabelFrame

from TKLevelUp.housemembersrpg import HouseMemberXPBar
from TKLevelUp.members.memberdbcontroller import MemberController
from supportmodules import modifiedwidgets

dk_gray = "#464646"
lt_gray = "#AAAAAA"
subtle_green = "#ccfdcc"


class NuenthelHub(Tk):
    def __init__(self):
        super().__init__()
        self.title("Nuenthel Hub")
        self.style = Style()
        self.style.theme_use("alt")
        self.resizable(True, True)
        # self.attributes("-fullscreen", True)

        """ Widget Attributes """
        self.house_members = []

        """ Styling """
        self.style.configure("TFrame", background=lt_gray)
        self.style.configure("Main.TButton", background=dk_gray, width=40, relief=SUNKEN, foreground="white",
                             font="Roboto 20 bold")
        """Window Frames"""
        self.calendar_frame_widget = None

        """Internal Functions"""
        self._create_main_buttons_frame()
        self._create_footer_frame()
        self._create_calendar_button()
        self._create_shopping_button()
        self._create_budget_button()
        self._create_chores_button()
        self._create_todo_button()
        self._create_home_mtn_button()
        self._create_upcoming_events()
        self._create_rpg_bars()
        self._row_col_configure(self)
        self._row_col_configure(self.main_btn_frame)
        self._row_col_configure(self.footer_frame)
        # self._number()

    def _create_main_buttons_frame(self):
        self.main_btn_frame = Frame(self, borderwidth=2)
        self.main_btn_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

    def _create_footer_frame(self):
        self.footer_frame = Frame(self, borderwidth=2)
        self.footer_frame.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)

    def _create_calendar_button(self):
        self.calendar_button = Button(self.main_btn_frame, text="Calendar", style="Main.TButton")
        self.calendar_button.grid(row=0, column=0, padx=10, pady=10, ipadx=40, ipady=80, sticky=NSEW)

    def _create_budget_button(self):
        self.budget_button = Button(self.main_btn_frame, text="Budget", style="Main.TButton")
        self.budget_button.grid(row=0, column=1, padx=10, pady=10, ipadx=40, ipady=80, sticky=NSEW)

    def _create_shopping_button(self):
        self.shopping_button = Button(self.main_btn_frame, text="Shopping List", style="Main.TButton")
        self.shopping_button.grid(row=0, column=2, padx=10, pady=10, ipadx=40, ipady=80, sticky=NSEW)

    def _create_chores_button(self):
        self.chores_button = Button(self.main_btn_frame, text="Chores", style="Main.TButton")
        self.chores_button.grid(row=0, column=3, padx=10, pady=10, ipadx=40, ipady=80, sticky=NSEW)

    def _create_todo_button(self):
        self.todo_button = Button(self.main_btn_frame, text="To Do", style="Main.TButton")
        self.todo_button.grid(row=1, column=0, padx=10, pady=10, ipadx=40, ipady=80, sticky=NSEW)

    def _create_home_mtn_button(self):
        self.home_mtn_button = Button(self.main_btn_frame, text="Home Mtn", style="Main.TButton")
        self.home_mtn_button.grid(row=1, column=1, padx=10, pady=10, ipadx=40, ipady=80, sticky=NSEW)

    def _create_upcoming_events(self):
        self.upcoming_events_canvas = modifiedwidgets.ScrollFrame(self.main_btn_frame)
        self.upcoming_events_canvas.grid(row=1, column=2, columnspan=2, padx=10, pady=10, sticky=NSEW)

    def _create_rpg_bars(self):
        for i, member in enumerate(MemberController.find_all()):
            xp_labelframe = LabelFrame(self.footer_frame, text=member.name)
            xp_labelframe.grid(row=0, column=i, ipadx=10, ipady=10)
            xp = HouseMemberXPBar(xp_labelframe, member)
            xp.pack()
            self.house_members.append(xp)

    def _create_tv_connection(self):
        if
    # def _calendar(self):
    #     TKCalendar(self).grid(row=0, column=0, rowspan=2, sticky=NSEW, padx=5, pady=5)
    #
    # def _budget(self):
    #     TKBudget(self).grid(row=0, column=1, sticky=NSEW, padx=5, pady=5)
    #
    # def _chores(self):
    #     TKChores(self).grid(row=3, column=0, columnspan=2, sticky=NSEW, padx=5, pady=5)
    #
    # def _tv(self):
    #     TKSonyRemote(self).grid(row=2, column=1, sticky=NSEW, padx=5, pady=5)

    @staticmethod
    def _row_col_configure(master: Tk or Frame):
        columns, rows = master.grid_size()
        for columns in range(columns):
            master.columnconfigure(columns, weight=1)
        for rows in range(rows):
            master.rowconfigure(rows, weight=1)


if __name__ == '__main__':
    NuenthelHub().mainloop()
