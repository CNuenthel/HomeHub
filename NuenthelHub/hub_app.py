from tkinter import Tk, NSEW, SUNKEN, BOTH, CENTER, RAISED, LabelFrame
from tkinter.ttk import Frame, Style, Button

from TKLevelUp.housemembersrpg import HouseMemberXPBar
from TKLevelUp.members.memberdbcontroller import MemberController
from supportmodules import modifiedwidgets
from TKCalendar import tkcalendar

dk_gray = "#464646"
lt_gray = "#AAAAAA"
subtle_green = "#ccfdcc"

btn_ipadx = 60
btn_ipady = 100


class NuenthelHub(Tk):
    def __init__(self):
        super().__init__()
        self.title("Nuenthel Hub")
        self.resizable(True, True)
        self.minsize(width=1500, height=900)
        self.configure(background="white")
        # self.attributes("-fullscreen", True)

        """ Widget Attributes """
        self.house_members = []
        self.tv_connected = "Disconnected"
        self.sheets_connected = "Disconnected"

        """ GUI Widgets """
        self.main_btn_widgets = []

        """ Styling """
        self.style = Style(self)
        self.style.theme_use("xpnative")
        self.style.configure("TFrame", background="white")
        self.style.configure("Main.TButton", background=dk_gray, width=20, relief=SUNKEN, foreground="white",
                             font="Roboto 20 bold")
        self.style.configure("Tv.TButton", background="green", anchor=CENTER)
        self.style.configure("Sheet.TButton", background="green", anchor=CENTER)
        self.style.configure("HubHdr.TFrame", background="white")
        self.style.configure("Hdr.Progressbar", background="blue")
        self.style.configure("Rpg.TLabelFrame", background="white")
        self.style.configure("Sink.TFrame", borderwidth=4, background="black")

        """Internal Functions"""
        self._create_main_buttons_frame()
        self._create_header_frame()
        self._create_calendar_button()
        self._create_shopping_button()
        self._create_budget_button()
        self._create_chores_button()
        self._create_todo_button()
        self._create_home_mtn_button()
        self._create_upcoming_events()
        self._create_rpg_bars()
        self._create_connection_frame()
        self._create_tv_connection()
        self._create_sheets_connection()
        self._row_col_configure(self, 1, row_index=1)
        self._row_col_configure(self.main_btn_frame, 1)
        self._col_configure(self.header_frame, 1)
        self._row_col_configure(self.rpg_frame, 1)
        self._row_col_configure(self.connection_frame, 1)
        # self._number()

    def _forget_main_buttons(self):
        for widget in self.main_btn_widgets:
            widget.grid_forget()

    def _create_main_buttons_frame(self):
        self.main_btn_frame = Frame(self)
        self.main_btn_frame.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)

    def _create_sinker_frame(self):
        self.sinker_frame = Frame(self.main_btn_frame, relief=SUNKEN, borderwidth=2)
        self.sinker_frame.grid(row=0, column=0, padx=20, pady=20, sticky=NSEW)

    def _create_header_frame(self):
        self.header_frame = Frame(self, style="HubHdr.TFrame")
        self.header_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

    def _create_calendar_button(self):
        self.calendar_button = Button(self.main_btn_frame, text="Calendar", style="Main.TButton", command=self.show_calendar)
        self.calendar_button.grid(row=0, column=0, padx=10, pady=10, ipadx=btn_ipadx, ipady=btn_ipady, sticky=NSEW)
        self.main_btn_widgets.append(self.calendar_button)

    def _create_budget_button(self):
        self.budget_button = Button(self.main_btn_frame, text="Budget", style="Main.TButton")
        self.budget_button.grid(row=0, column=1, padx=10, pady=10, ipadx=btn_ipadx, ipady=btn_ipady, sticky=NSEW)
        self.main_btn_widgets.append(self.budget_button)

    def _create_shopping_button(self):
        self.shopping_button = Button(self.main_btn_frame, text="Shopping List", style="Main.TButton")
        self.shopping_button.grid(row=0, column=2, padx=10, pady=10, ipadx=btn_ipadx, ipady=btn_ipady, sticky=NSEW)
        self.main_btn_widgets.append(self.shopping_button)

    def _create_chores_button(self):
        self.chores_button = Button(self.main_btn_frame, text="Chores", style="Main.TButton")
        self.chores_button.grid(row=0, column=3, padx=10, pady=10, ipadx=btn_ipadx, ipady=btn_ipady, sticky=NSEW)
        self.main_btn_widgets.append(self.chores_button)

    def _create_todo_button(self):
        self.todo_button = Button(self.main_btn_frame, text="To Do", style="Main.TButton")
        self.todo_button.grid(row=1, column=0, padx=10, pady=10, ipadx=btn_ipadx, ipady=btn_ipady, sticky=NSEW)
        self.main_btn_widgets.append(self.todo_button)

    def _create_home_mtn_button(self):
        self.home_mtn_button = Button(self.main_btn_frame, text="Home Mtn", style="Main.TButton")
        self.home_mtn_button.grid(row=1, column=1, padx=10, pady=10, ipadx=btn_ipadx, ipady=btn_ipady, sticky=NSEW)
        self.main_btn_widgets.append(self.home_mtn_button)

    def _create_upcoming_events(self):
        self.upcoming_events_canvas = modifiedwidgets.ScrollFrame(self.main_btn_frame)
        self.upcoming_events_canvas.grid(row=1, column=2, columnspan=2, padx=10, sticky=NSEW)
        self.main_btn_widgets.append(self.upcoming_events_canvas)

    def _create_rpg_bars(self):
        self.rpg_frame = Frame(self.header_frame)
        self.rpg_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

        for i, member in enumerate(MemberController.find_all()):
            xp_labelframe = LabelFrame(self.rpg_frame, text=member.name, bg="white")
            xp_labelframe.grid(row=0, column=i, padx=10, pady=10, sticky=NSEW)
            xp = HouseMemberXPBar(xp_labelframe, member)
            xp.pack(fill=BOTH, padx=10, pady=10)
            self.house_members.append(xp)

    def _create_connection_frame(self):
        self.connection_frame = Frame(self.header_frame)
        self.connection_frame.grid(row=0, column=1, padx=10, pady=10, sticky=NSEW)

    def _create_tv_connection(self):
        self.tv_connected_btn = Button(self.connection_frame, text=f"TV {self.tv_connected}", style="Tv.TButton", state="disabled")
        self.tv_connected_btn.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

    def _create_sheets_connection(self):
        self.sheets_connected_btn = Button(self.connection_frame, text=f"Sheets {self.sheets_connected}", style="Sheets.TButton", state="disabled")
        self.sheets_connected_btn.grid(row=0, column=1, padx=10, pady=10, sticky=NSEW)

    @staticmethod
    def _row_col_configure(master: Tk or Frame, weight: int, col_index: int = 0, row_index: int = 0):
        columns, rows = master.grid_size()
        for i in range(col_index, columns):
            master.columnconfigure(i, weight=weight)
        for i in range(row_index, rows):
            master.rowconfigure(i, weight=weight)

    @staticmethod
    def _col_configure(master: Tk or Frame, weight: int, first_index: int = 0):
        columns, rows = master.grid_size()
        for i in range(first_index, rows):
            master.columnconfigure(i, weight=weight)

# _____________ Button Commands ________________________________________________________________________________________

    def show_calendar(self):
        self._forget_main_buttons()
        # TODO sinker frame is tiny and just sitting behind everything
        self._create_sinker_frame()
        # tk_cal = tkcalendar.TKCalendar(self.sinker_frame)
        # tk_cal.grid(row=1, column=0, sticky=NSEW)
        self._row_col_configure(self.sinker_frame, 1)


if __name__ == '__main__':
    NuenthelHub().mainloop()
