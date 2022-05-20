from functools import partial
from tkinter import Frame, Tk, NSEW, CENTER, FLAT, Label, GROOVE, W, EW, BOTH, END, Button, StringVar
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from TKBudget.expenseplot import ExpensePlot
from supportmodules.modifiedwidgets import SnapbackEntry
from NuenthelHub.TKBudget import nuenthelsheetdata as nsd
from NuenthelHub.TKBudget import sheetservice as sheetserv
import threading
import queue


# TODO Google API Ratelimit on update button press

class TKBudget:
    """ Creates a top level GUI for budget handling

    This class is aware that param master has the attribute body_frame

    """

    def __init__(self, master, style, callback: callable = None):
        super().__init__()
        """ Window Attributes """
        self.master = master
        self.callback = callback
        self.bar_graph = None
        self.graph_holder_frame = None

        """ External Helper Classes """
        self.nfsheet = nsd.NuenthelSheetsData()
        self.ss = sheetserv.SheetService("N-Fam 2022", 0)

        """ The Queue """
        self.queue = queue.Queue()

        """ Widgets """
        self.expenses = {}
        self.incomes = {}
        self.recents = []

        self.budget_entry = None
        self.used_entry = None

        """ Styling """
        self.style = style
        self.style.configure("GrnCumulate.TButton", font="Roboto 12", background="#ccfdcc", borderwidth=10)
        self.style.configure("YelCumulate.TButton", font="Roboto 12", background="#f9fdcc", borderwidth=10)
        self.style.configure("OrgCumulate.TButton", font="Roboto 12", background="#fdf1cc", borderwidth=10)
        self.style.configure("RedCumulate.TButton", font="Roboto 12", background="#fdd0cc", borderwidth=10)
        self.style.configure("Cumulate.TButton", font="Roboto 12", borderwidth=3)

        """ GUI Constructor Functions """
        self._make_frames()
        self._grid_frames()
        self._make_sidebar_widgets()
        self._make_expense_widgets()
        self._make_recent_widgets()
        self._make_income_widgets()

        """ Initialize Widgets """
        self._initialization_threads()

        """ Configure Frames """
        self._configure_rows_cols(self.main_frame)
        self._configure_rows_cols(self.expense_frame)
        self._configure_rows_cols(self.recent_frame)
        self._configure_rows_cols(self.income_frame)
        self._configure_rows_cols(self.sidebar_frame)
        self._configure_rows_cols(self.graph_frame)

    def repack_module(self):
        """ Repacks the main frame and sidebar frame of the Budget page, called to return
        the Budget page after widgets were removed with grid_forget """
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW, columnspan=4, rowspan=2)
        self.sidebar_frame.grid(row=0, column=5, padx=10, pady=10, ipadx=30, sticky=NSEW)

    def _make_frames(self):
        """ Creates all required frame widgets on master window """
        self.main_frame = Frame(self.master.body_frame)
        self.sidebar_frame = Frame(self.master.body_frame)
        self.expense_frame = Frame(self.main_frame, background="white", borderwidth=3, relief=GROOVE)
        self.recent_frame = Frame(self.main_frame, background="white", borderwidth=3, relief=GROOVE)
        self.income_frame = Frame(self.main_frame, background="white", borderwidth=3, relief=GROOVE)
        self.graph_frame = Frame(self.main_frame, background="white", borderwidth=3, relief=GROOVE)

    def _grid_frames(self):
        """ Assigns all required frame widgets on master using grid manager """
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW, columnspan=4, rowspan=2)
        self.sidebar_frame.grid(row=0, column=5, padx=10, pady=10, ipadx=30, sticky=NSEW)
        self.expense_frame.grid(row=0, column=0, columnspan=3, sticky=NSEW, padx=10, pady=10)
        self.recent_frame.grid(row=1, column=1, padx=5, pady=5, sticky=NSEW)
        self.income_frame.grid(row=1, column=2, padx=5, pady=5, sticky=NSEW)
        self.graph_frame.grid(row=1, column=0, sticky=NSEW, padx=5, pady=5)

    def _make_sidebar_widgets(self):
        """ Constructs sidebar widgets and packs onto sidebar frame """
        return_btn = ttk.Button(self.sidebar_frame, text="Return", command=self.return_to_main)
        return_btn.pack(expand=True, fill=BOTH)
        update_btn = ttk.Button(self.sidebar_frame, text="Update", command=self.update_from_sheet)
        update_btn.pack(expand=True, fill=BOTH)

    def _make_expense_widgets(self):
        """ Creates a Button and Entry for each expense and grids onto expense frame """
        labels = ["Dining", "Grocery", "Transport", "Recreation", "Personal", "JL", "Other"]

        for i in range(len(labels)):
            btn = ttk.Button(self.expense_frame, text=labels[i], style="Cumulate.TButton",
                             command=partial(self.cumulate_expense_clicked, labels[i]))
            entry = SnapbackEntry(self.expense_frame, font="Roboto 12", justify=CENTER)

            btn.grid(row=0, column=i, padx=5, pady=5, sticky=NSEW)
            entry.grid(row=1, column=i, padx=5, pady=5, sticky=NSEW)
            self.expenses[labels[i]] = {"btn": btn, "ent": entry}

    def _make_recent_widgets(self):
        """ Creates text-less Labels and grids onto recent frame """
        Label(self.recent_frame, text="Recent", font="Roboto " + "12 bold", background="white").pack()

        for i in range(11):
            self.x = Label(self.recent_frame, text="", font="Roboto " + "12", background="white")
            self.x.pack()
            self.recents.append(self.x)

    def _make_income_widgets(self):
        """ Creates a Button and Entry for each income and grids onto income frame """
        labels = ["Cody", "Sam", "Other"]

        for i in range(len(labels)):
            btn = ttk.Button(self.income_frame, command=partial(self.cumulate_income_clicked, labels[i]),
                             text=labels[i], style="Cumulate.TButton")
            se = SnapbackEntry(self.income_frame, font="Roboto " + "15 italic", justify=CENTER)

            se.grid(row=i, column=1, pady=5, padx=5, sticky=NSEW)
            btn.grid(row=i, column=0, pady=5, padx=5, sticky=NSEW)

            self.incomes[labels[i]] = {"btn": btn, "ent": se}

    def _initialize_expense_colors(self, expense_data: list):
        """ Initializes expense Labels with color grade """
        for expense in expense_data:
            self.color_expense_label(expense[0], expense[1])

    def _initialize_expense_entries(self, expense_data: list):
        """ Initializes expense Entries with current expense data """
        for expense in expense_data:
            self.expenses[expense[0]]["ent"].delete(0, END)
            self.expenses[expense[0]]["ent"].insert(0, expense[1])

    def _initialize_incomes(self, income_data: list):
        """ Initializes income Entries with current income data """
        for income in income_data:
            self.incomes[income[0]]["ent"].delete(0, END)
            self.incomes[income[0]]["ent"].insert(0, income[1])

    def _initialization_threads(self):
        """ Queue data for expense color initialization """
        threading.Thread(target=self.thread_expense_percent, args=(self.nfsheet.expenses, "init_expense_perc")).start()
        threading.Thread(target=self.thread_expense_value, args=(self.nfsheet.expenses, "init_expense_value")).start()
        threading.Thread(target=self.thread_income_value, args=(self.nfsheet.incomes, "init_income_value")).start()
        threading.Thread(target=self.create_plot, args=("init_plot",)).start()

    def create_plot(self, queue_id):
        expense_values = [self.nfsheet.get_expense_total(category) for category in self.nfsheet.expenses]
        expense_percents = [self.nfsheet.get_expense_percent(category) for category in self.nfsheet.expenses]
        figure = ExpensePlot(expense_values, expense_percents, self.nfsheet.expenses).get_plot()
        self.queue.put([queue_id, figure])
        self.master.after(100, self._process_queue())
        return

    def thread_expense_percent(self, categories, queue_id):
        """ Thread process I/O request to NuenthelSheets expense percentage and place in queue
        list structure = [queue_id: str, [expense_category: str, percentage: int]]"""
        expense_percent_data = []
        for category in categories:
            percentage = self.nfsheet.get_expense_percent(category)
            expense_percent_data.append([category, percentage])
        self.queue.put([queue_id, expense_percent_data])
        self.master.after(100, self._process_queue())
        return

    def thread_expense_value(self, categories, queue_id):
        """ Thread process I/O request to NuenthelSheets expense total and place in queue
        list structure = [queue_id: str, [expense_category: str, expense total: str]]"""
        expense_value_data = []
        for category in categories:
            value = self.nfsheet.get_expense_total(category)
            expense_value_data.append([category, value])
        self.queue.put([queue_id, expense_value_data])
        self.master.after(100, self._process_queue())
        return

    def thread_income_value(self, categories, queue_id):
        """ Thread process I/O request to NuenthelSheets expense total and place in queue
        list structure = [queue_id: str, [income_category: str, expense total: str]]"""
        income_value_data = []
        for category in categories:
            value = self.nfsheet.get_income_total(category)
            income_value_data.append([category, value])
        self.queue.put([queue_id, income_value_data])
        self.master.after(100, self._process_queue())
        return

    def thread_cumulate_expense(self, category, value, queue_id):
        self.nfsheet.add_expense(category, value)
        expense_value = self.nfsheet.get_cell_dollar_data(self.nfsheet.expense_alphanums[category])
        self.queue.put([queue_id, [category, expense_value]])
        self.master.after(50, self._process_queue)

    def thread_cumulate_income(self, category, value, queue_id):
        self.nfsheet.cumulate_dollar_format_cell(value, self.nfsheet.income_alphanums[category])
        new_value = self.nfsheet.get_income_total(category)
        self.queue.put([queue_id, [category, new_value]])
        self.master.after(50, self._process_queue)

    def _process_queue(self):
        """ Processes queue data and calls linked functions """
        try:
            output = self.queue.get_nowait()
            match output[0]:
                case "init_expense_perc":
                    self._initialize_expense_colors(output[1])  # Sends data list
                case "init_expense_value":
                    self._initialize_expense_entries(output[1])
                case "init_income_value":
                    self._initialize_incomes(output[1])
                case "init_plot":
                    self.grid_plot(output[1])
                case "cumulate_exp":
                    self.update_expense_gui(output[1][0], output[1][1])
                case "cumulate_inc":
                    self.update_income_gui(output[1][0], output[1][1])

        except queue.Empty:
            print("Queue empty, rerunning")
            self.master.after(100, self._process_queue)

    def color_expense_label(self, category, percentage: int):
        if percentage is None or percentage < 50:
            self.expenses[category]["btn"].configure(style="GrnCumulate.TButton")
        elif 50 <= percentage < 75:
            self.expenses[category]["btn"].configure(style="YelCumulate.TButton")
        elif 75 <= percentage < 90:
            self.expenses[category]["btn"].configure(style="OrgCumulate.TButton")
        elif percentage >= 90:
            self.expenses[category]["btn"].configure(style="RedCumulate.TButton")

    def add_recent(self, expense_class, value):
        """ Adds a value change to the Recent frame """
        for i in range(len(self.recents) - 1, -1, -1):
            self.recents[i]["text"] = self.recents[i - 1]["text"]

        self.recents[0]["text"] = f"[{expense_class}] ${value}"

    def grid_plot(self, figure):
        if self.bar_graph:
            self.graph_frame.destroy()

        self.graph_frame = Frame(self.main_frame, background="white", borderwidth=3, relief=GROOVE)
        self.graph_frame.grid(row=1, column=0, sticky=NSEW, padx=5, pady=5)
        self._configure_rows_cols(self.graph_frame)

        self.bar_graph = FigureCanvasTkAgg(figure, self.graph_frame)
        self.bar_graph.get_tk_widget().pack(padx=10, pady=10, expand=True, fill=BOTH)

    """ BUTTON FUNCTIONS ---------------------------------------------------------------------------------"""

    def cumulate_expense_clicked(self, expense_label: str):
        value = self.expenses[expense_label]["ent"].get()
        threading.Thread(target=self.thread_cumulate_expense, args=(expense_label, value, "cumulate_exp")).start()

    def cumulate_income_clicked(self, income_label: str):
        value = self.incomes[income_label]["ent"].get()
        threading.Thread(target=self.thread_cumulate_income, args=(income_label, value, "cumulate_inc")).start()

    def update_expense_gui(self, category: str, value: str):
        self.expenses[category]["ent"].delete(0, END)
        self.expenses[category]["ent"].insert(0, value)

    def update_income_gui(self, category: str, value: str):
        self.incomes[category]["ent"].delete(0, END)
        self.incomes[category]["ent"].insert(0, value)

    def return_to_main(self):
        self.main_frame.grid_remove()
        self.sidebar_frame.grid_remove()
        self.callback()

    def update_from_sheet(self):
        self.nfsheet.update_sheet()
        self._initialization_threads()

    """ STATIC METHODS ---------------------------------------------------------------------------------------"""

    @staticmethod
    def _configure_rows_cols(master):
        """ Configure rows and columns to 1:1 weight """
        for i in range(master.grid_size()[1]):
            master.rowconfigure(i, weight=1)
        for i in range(master.grid_size()[0]):
            master.columnconfigure(i, weight=1)

