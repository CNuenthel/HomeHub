from tkinter import Tk, NSEW, SUNKEN, BOTH, CENTER
from tkinter.ttk import Frame, Style, Button
from supportmodules import modifiedwidgets
from TKLevelUp import housemembersrpg as rpg
from TKCalendar import tkcalendar as tkc

btn_ipadx = 25
btn_ipady = 80


def row_col_configure(master: Tk or Frame, weight: int, col_index: int = 0, row_index: int = 0, row_config: bool = True, col_config: bool = True):
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
        self.style.configure("Body.TFrame", relief=SUNKEN, bg="black")
        self.style.configure("TFrame", background="white")
        self.style.configure("Main.TButton", background="white", width=20, relief=SUNKEN, foreground="black",
                             font="Roboto 20 bold")

        """ Init GUI Frames """
        self.header_frame = Frame(self, style="HubHdr.TFrame")
        self.header_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)
        row_col_configure(self.header_frame, 1, row_config=False)

        self.body_frame = Frame(self, relief=SUNKEN, borderwidth=2, style="Body.TFrame")
        self.body_frame.grid(row=1, column=0, padx=20, pady=20, sticky=NSEW)
        row_col_configure(self.body_frame, 1)

        """ Sony Bravia connection visual """
        self.tv_connected_btn = Button(
            self.header_frame, text=f"TV {self.tv_connected}", style="Tv.TButton", state="disabled")
        self.tv_connected_btn.grid(row=0, column=2, padx=10, pady=10, sticky=NSEW)

        """ Google Sheets connection visual """
        self.sheets_connected_btn = Button(
            self.header_frame, text=f"Sheets {self.budget_connected}", style="Sheets.TButton", state="disabled")
        self.sheets_connected_btn.grid(row=0, column=3, padx=10, pady=10, sticky=NSEW)

        """ Set up home RPG """
        self.rpg_frame = Frame(self.header_frame)
        self.rpg_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)
        self.rpg = rpg.HomeRPG(self.rpg_frame)
        self.rpg.get_members()
        self.rpg.create_rpg_bars()
        row_col_configure(self.rpg_frame, 1, row_config=False)

        """Internal Functions"""
        self._create_calendar_button()
        self._create_budget_button()
        self._create_shopping_button()
        self._create_chores_button()
        self._create_todo_button()
        self._create_home_mtn_button()
        self._create_upcoming_events()

        """ Configure """
        row_col_configure(self.upcoming_events_frame, 1)
        row_col_configure(self.header_frame, 1, row_config=False)
        row_col_configure(self.body_frame, 1)
        row_col_configure(self.rpg_frame, 1)
        row_col_configure(self, 1, row_index=1)

    def _sweep_widgets(self):
        for widget in self.main_btn_widgets:
            widget.grid_forget()

    def _create_calendar_button(self):
        self.calendar_button = Button(self.body_frame, text="Calendar", style="Main.TButton", command=self.show_calendar)
        self.calendar_button.grid(row=0, column=0, padx=10, pady=10, ipadx=btn_ipadx, ipady=btn_ipady, sticky=NSEW)
        self.main_btn_widgets.append(self.calendar_button)

    def _create_budget_button(self):
        self.budget_button = Button(self.body_frame, text="Budget", style="Main.TButton")
        self.budget_button.grid(row=0, column=1, padx=10, pady=10, ipadx=btn_ipadx, ipady=btn_ipady, sticky=NSEW)
        self.main_btn_widgets.append(self.budget_button)

    def _create_shopping_button(self):
        self.shopping_button = Button(self.body_frame, text="Shopping List", style="Main.TButton")
        self.shopping_button.grid(row=0, column=2, padx=10, pady=10, ipadx=btn_ipadx, ipady=btn_ipady, sticky=NSEW)
        self.main_btn_widgets.append(self.shopping_button)

    def _create_chores_button(self):
        self.chores_button = Button(self.body_frame, text="Chores", style="Main.TButton")
        self.chores_button.grid(row=0, column=3, padx=10, pady=10, ipadx=btn_ipadx, ipady=btn_ipady, sticky=NSEW)
        self.main_btn_widgets.append(self.chores_button)

    def _create_todo_button(self):
        self.todo_button = Button(self.body_frame, text="To Do", style="Main.TButton")
        self.todo_button.grid(row=1, column=0, padx=10, pady=10, ipadx=btn_ipadx, ipady=btn_ipady, sticky=NSEW)
        self.main_btn_widgets.append(self.todo_button)

    def _create_home_mtn_button(self):
        self.home_mtn_button = Button(self.body_frame, text="Home Mtn", style="Main.TButton")
        self.home_mtn_button.grid(row=1, column=1, padx=10, pady=10, ipadx=btn_ipadx, ipady=btn_ipady, sticky=NSEW)
        self.main_btn_widgets.append(self.home_mtn_button)

    def _create_upcoming_events(self):
        self.upcoming_events_frame = Frame(self.body_frame)
        self.upcoming_events_frame.grid(row=1, column=2, columnspan=2, padx=10, pady=10, sticky=NSEW)
        self.upcoming_events_canvas = modifiedwidgets.ScrollFrame(self.body_frame)
        self.upcoming_events_canvas.grid(row=1, column=2, columnspan=2, padx=10, pady=10, sticky=NSEW)
        self.main_btn_widgets.append(self.upcoming_events_canvas)

# _____________ Button Commands ________________________________________________________________________________________

    def show_calendar(self):
        self._sweep_widgets()
        tkcal = tkc.TKCalendar(self)



if __name__ == '__main__':
    RootGUI().mainloop()
