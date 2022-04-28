from tkinter import Tk, NSEW, SUNKEN, BOTH, CENTER
from tkinter.ttk import Frame, Style, Button
from supportmodules import modifiedwidgets
from TKCalendar import tkcalendar

dk_gray = "#464646"
lt_gray = "#AAAAAA"
subtle_green = "#ccfdcc"

btn_ipadx = 60
btn_ipady = 100


def row_col_configure(master: Tk or Frame, weight: int, col_index: int = 0, row_index: int = 0, row_config: bool = True, col_config: bool = True):
    columns, rows = master.grid_size()
    if col_config:
        for i in range(col_index, columns):
            master.columnconfigure(i, weight=weight)
    if row_config:
        for i in range(row_index, rows):
            master.rowconfigure(i, weight=weight)


class RootGUI:
    """ Creates Root Window GUI """
    def __init__(self):
        self.master = Tk()
        self.master.minsize(width=1500, height=900)
        self.master.title("Nuenthel Hub")
        self.master.configure(background="white")
        self.master.resizable(True, True)

        """ GUI Connections """
        self.tv_connected = "Disconnected"
        self.budget_connected = "Disconnected"

        """ Styles """
        self.style = Style()
        self.style.theme_use("clam")
        self.style.configure("Body.TFrame", relief=SUNKEN)

        """ Init GUI """
        self.header_frame = Frame(self.master, style="HubHdr.TFrame")
        self.header_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

        self.body_frame = Frame(self.master, relief=SUNKEN, borderwidth=2, style="Body.TFrame")
        self.body_frame.grid(row=1, column=0, padx=20, pady=20, sticky=NSEW)

        self.sidebar_frame = Frame(self.master, relief=SUNKEN, borderwidth=2, style="Sidebar.TFrame")
        self.sidebar_frame.grid(row=1, column=1, padx=20, pady=20, sticky=NSEW)

        self.connection_frame = Frame(self.header_frame)
        self.connection_frame.grid(row=0, column=1, padx=10, pady=10, sticky=NSEW)

        self.tv_connected_btn = Button(
            self.connection_frame, text=self.tv_connected, style="Tv.TButton", state="disabled")
        self.tv_connected_btn.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)

        self.sheets_connected_btn = Button(
            self.connection_frame, text=f"Sheets {self.budget_connected}", style="Sheets.TButton", state="disabled")
        self.sheets_connected_btn.grid(row=0, column=1, padx=10, pady=10, sticky=NSEW)


class MainPage:
    def __init__(self, master: RootGUI):
        self.master = master

        """ GUI Widgets """
        self.main_btn_widgets = []

        """ Styling """
        self.style = Style()
        self.style.theme_use("vista")
        self.style.configure("TFrame", background="white")
        self.style.configure("Main.TButton", background=dk_gray, width=20, relief=SUNKEN, foreground="white",
                             font="Roboto 20 bold")
        self.style.configure("Tv.TButton", background="green", anchor=CENTER)
        self.style.configure("Sheet.TButton", background="green", anchor=CENTER)
        self.style.configure("HubHdr.TFrame", background="white")
        self.style.configure("Hdr.Progressbar", background="white")
        self.style.configure("Rpg.TLabelFrame", background="white")
        self.style.configure("Sunken.TFrame", borderwidth=4, background="black")
        self.style.configure("Return.TButton", background="black", foreground="white")

        """Internal Functions"""
        self._forget_sidebar()
        self._create_calendar_button()
        self._create_budget_button()
        self._create_shopping_button()
        self._create_chores_button()
        self._create_todo_button()
        self._create_home_mtn_button()
        self._create_upcoming_events()
        
    def _forget_sidebar(self):
        self.master.sidebar_frame.grid_forget()

    def _create_calendar_button(self):
        self.calendar_button = Button(self.master.body_frame, text="Calendar", style="Main.TButton", command=self.show_calendar)
        self.calendar_button.grid(row=0, column=0, padx=10, pady=10, ipadx=btn_ipadx, ipady=btn_ipady, sticky=NSEW)
        self.main_btn_widgets.append(self.calendar_button)

    def _create_budget_button(self):
        self.budget_button = Button(self.master.body_frame, text="Budget", style="Main.TButton")
        self.budget_button.grid(row=0, column=1, padx=10, pady=10, ipadx=btn_ipadx, ipady=btn_ipady, sticky=NSEW)
        self.main_btn_widgets.append(self.budget_button)

    def _create_shopping_button(self):
        self.shopping_button = Button(self.master.body_frame, text="Shopping List", style="Main.TButton")
        self.shopping_button.grid(row=0, column=2, padx=10, pady=10, ipadx=btn_ipadx, ipady=btn_ipady, sticky=NSEW)
        self.main_btn_widgets.append(self.shopping_button)

    def _create_chores_button(self):
        self.chores_button = Button(self.master.body_frame, text="Chores", style="Main.TButton")
        self.chores_button.grid(row=0, column=3, padx=10, pady=10, ipadx=btn_ipadx, ipady=btn_ipady, sticky=NSEW)
        self.main_btn_widgets.append(self.chores_button)

    def _create_todo_button(self):
        self.todo_button = Button(self.master.body_frame, text="To Do", style="Main.TButton")
        self.todo_button.grid(row=1, column=0, padx=10, pady=10, ipadx=btn_ipadx, ipady=btn_ipady, sticky=NSEW)
        self.main_btn_widgets.append(self.todo_button)

    def _create_home_mtn_button(self):
        self.home_mtn_button = Button(self.master.body_frame, text="Home Mtn", style="Main.TButton")
        self.home_mtn_button.grid(row=1, column=1, padx=10, pady=10, ipadx=btn_ipadx, ipady=btn_ipady, sticky=NSEW)
        self.main_btn_widgets.append(self.home_mtn_button)

    def _create_upcoming_events(self):
        self.upcoming_events_canvas = modifiedwidgets.ScrollFrame(self.master.body_frame)
        self.upcoming_events_canvas.grid(row=1, column=2, columnspan=2, padx=10, sticky=NSEW)
        self.main_btn_widgets.append(self.upcoming_events_canvas)

# _____________ Button Commands ________________________________________________________________________________________

    def show_calendar(self):
        print("Button Pushed")


if __name__ == '__main__':
    root = RootGUI()
    main_page = MainPage(root)

    root.master.mainloop()
