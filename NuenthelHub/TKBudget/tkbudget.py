from functools import partial
from tkinter import Frame, Tk, NSEW, CENTER, FLAT, Label, GROOVE, W, EW, BOTH, END, Button
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from TKBudget.expenseplot import ExpensePlot
from supportmodules.modifiedwidgets import HoverLabel, SnapbackEntry


def row_col_configure(master: Tk or Frame, weight: int, col_index: int = 0, row_index: int = 0, row_config: bool = True,
                      col_config: bool = True):
    columns, rows = master.grid_size()
    if col_config:
        for i in range(col_index, columns):
            master.columnconfigure(i, weight=weight)
    if row_config:
        for i in range(row_index, rows):
            master.rowconfigure(i, weight=weight)


class TKBudget:
    """ Creates a top level GUI for budget handling """

    def __init__(self, master, sheets_connect, style, callback: callable = None):
        super().__init__()
        """ Window Attributes """
        self.master = master
        self.callback = callback

        """ External Helper Classes """
        self.nfsheet = sheets_connect

        """ Widgets """
        self.expense_entries = []
        self.expense_labels = []
        self.expense_hbuttons = []
        self.recents = []
        self.income_entries = []
        self.income_buttons = []
        self.budget_entry = None
        self.used_entry = None
        self.graph = None

        """ Styling """
        self.style = style
        self.style.configure("GrnCumulate.TButton", font="Roboto 12", background="#ccfdcc")
        self.style.configure("YelCumulate.TButton", font="Roboto 12", background="#f9fdcc")
        self.style.configure("OrgCumulate.TButton", font="Roboto 12", background="#fdf1cc")
        self.style.configure("RedCumulate.TButton", font="Roboto 12", background="#fdd0cc")
        self.style.configure("Cumulate.TButton", font="Roboto 12")

        """ GUI Constructor Functions """
        self._make_main_frame()
        self._make_sidebar_frame()
        self._make_sidebar_buttons()
        self._make_expenses()
        self._make_graph()
        self._make_recent()
        self._make_income()

        """ GUI Configuration Functions """
        self._configure_expense_colors()
        self._update_expense_entries()
        self._configure_incomes()
        self._configure_rows_cols(self.main_frame)
        self._configure_rows_cols(self.graph_frame)
        self._configure_rows_cols(self.expense_frame)
        self._configure_rows_cols(self.recent_frame)
        self._configure_rows_cols(self.income_frame)
        self._configure_rows_cols(self.sidebar_frame)

    def _make_main_frame(self):
        self.main_frame = Frame(self.master.body_frame)
        self.main_frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW, columnspan=4, rowspan=2)

    def _make_sidebar_frame(self):
        self.sidebar_frame = Frame(self.master.body_frame)
        self.sidebar_frame.grid(row=0, column=5, padx=10, pady=10, ipadx=30, sticky=NSEW)

    def _make_sidebar_buttons(self):
        return_btn = ttk.Button(self.sidebar_frame, text="Return", command=self.return_to_main)
        return_btn.pack(expand=True, fill=BOTH)

    def _make_expenses(self):
        self.expense_frame = Frame(self.main_frame, background="white", borderwidth=3, relief=GROOVE)
        self.expense_frame.grid(row=0, column=0, columnspan=3, sticky=NSEW, padx=10, pady=10)

        labels = ["Dining", "Grocery", "Transport", "Recreation", "Personal", "J&L", "Other"]
        commands = [partial(self.cumulate_expense, i) for i in range(7)]

        for i, j in enumerate(labels):
            btn = ttk.Button(self.expense_frame, text=j, command=commands[i], style="Cumulate.TButton")
            btn.grid(row=0, column=i+1, padx=5, pady=5, sticky=NSEW)
            self.expense_labels.append(btn)

            entry = SnapbackEntry(self.expense_frame, font="Roboto " + "12", justify=CENTER)
            entry.grid(row=1, column=i+1, padx=5, pady=5, sticky=NSEW)
            self.expense_entries.append(entry)

    def _make_recent(self):
        self.recent_frame = Frame(self.main_frame, background="white", borderwidth=3, relief=GROOVE)
        self.recent_frame.grid(row=1, column=1, padx=5, pady=5, sticky=NSEW)

        Label(self.recent_frame, text="Recent", font="Roboto " + "12 bold", background="white").pack()

        for i in range(11):
            self.x = HoverLabel(self.recent_frame, text="", font="Roboto " + "12", background="white")
            self.x.pack()
            self.recents.append(self.x)

    def _make_income(self):
        self.income_frame = Frame(self.main_frame, background="white", borderwidth=3, relief=GROOVE)
        self.income_frame.grid(row=1, column=2, padx=5, pady=5, sticky=NSEW)

        labels = ["Cody", "Sam", "Other"]
        commands = [partial(self.cumulate_income, i) for i in range(3)]
        for i, j in enumerate(labels):
            ttk.Button(self.income_frame, text=j, command=commands[i], style="Cumulate.TButton").grid(row=i, column=0, pady=5, padx=5, sticky=NSEW)
            se = SnapbackEntry(self.income_frame, font="Roboto " + "15 italic", justify=CENTER)
            se.grid(row=i, column=1, pady=5, padx=5, sticky=NSEW)
            self.income_entries.append(se)

    def _make_graph(self):
        if self.graph:
            self.graph_frame.destroy()

        self.graph = True
        self.graph_frame = Frame(self.main_frame, background="white", borderwidth=3, relief=GROOVE)
        self.graph_frame.grid(row=1, column=0, sticky=NSEW, padx=5, pady=5)

        figure = ExpensePlot(self.nfsheet).get_plot()
        bar_graph = FigureCanvasTkAgg(figure, self.graph_frame)
        bar_graph.get_tk_widget().pack(padx=10, pady=10, expand=True, fill=BOTH)

    # """_______________These configurations are specific to my family budget sheet__________________________________"""

    @staticmethod
    def _configure_rows_cols(master):
        """ Configure rows and columns to 1:1 weight """
        for i in range(master.grid_size()[1]):
            master.rowconfigure(i, weight=1)
        for i in range(master.grid_size()[0]):
            master.columnconfigure(i, weight=1)

    def _configure_expense_colors(self):
        """
        Configures button color changes based on expense percentages
        Assumes order of expenses are:
        [Dining, Grocery, Transport, Recreation, Personal, J&L, Other]
        """
        expense_data = self.nfsheet.get_expense_data()
        perc_list = [expense_data[key][0]["perc"] for key in expense_data.keys()]

        for i, j in enumerate(self.expense_labels):
            if perc_list[i] < 50:
                j.configure(style="GrnCumulate.TButton")
            elif 50 <= perc_list[i] < 75:
                j.configure(style="YelCumulate.TButton")
            elif 75 <= perc_list[i] < 90:
                j.configure(style="OrgCumulate.TButton")
            elif perc_list[i] >= 90:
                j.configure(style="RedCumulate.TButton")

    def _update_expense_entries(self):
        """
        Configures entry values based on expense values
        Assumes order of expenses are:
        [Dining, Grocery, Transport, Recreation, Personal, J&L, Other]
        """
        expense_data = self.nfsheet.get_expense_data()
        value_list = [expense_data[key][1]["val"] for key in expense_data.keys()]

        for i, j in enumerate(self.expense_entries):
            j.delete(0, END)
            j.insert(0, value_list[i])
        self._make_graph()

    def _configure_recents(self, expense_class, value):
        for i in range(len(self.recents) - 1, -1, -1):
            self.recents[i]["text"] = self.recents[i - 1]["text"]

        self.recents[0]["text"] = f"[{expense_class}] ${value}"

    def _configure_incomes(self):
        """ Fill income entries with corresponding budget cells """
        income_cell_values = [  # Cody's, Sam's, Other's
            self.nfsheet.get_cell_dollar_data("C56"),
            self.nfsheet.get_cell_dollar_data("C57"),
            self.nfsheet.get_cell_dollar_data("C58")]

        for i, j in enumerate(self.income_entries):
            j.delete(0, END)
            j.insert(0, income_cell_values[i])

    # ___________________Button Functions_______________________________________________________________________________

    def cumulate_expense(self, column):
        """ JFC This has so much crossover it hurts """
        if self.expense_entries[column].current_text is not None:
            value = self.expense_entries[column].get()  # Get value user put in entry
            self.nfsheet.add_expense(column + 1, value)  # Add expense to budget sheet
            self._update_expense_entries()  # Recalculate and show expense entries
            self.expense_entries[column].current_text = None  # Reset entry attribute current text to none
            self._configure_recents(self.expense_labels[column].cget("text"), value)  # add expense to recent expenses
            self._make_graph()

    def cumulate_income(self, column):
        """ Cumulate income for Cody,Sam,Other entries """
        if self.income_entries[column].current_text is not None:
            value = float(self.income_entries[column].get())
            str_repr = "Err"  # placeholder to show err if unmatched col

            match column:
                case 0:
                    self.nfsheet.update_dollar_format_cell(value, "C56")
                    str_repr = "CInc"
                case 1:
                    self.nfsheet.update_dollar_format_cell(value, "C57")
                    str_repr = "SInc"
                case 2:
                    self.nfsheet.update_dollar_format_cell(value, "C58")
                    str_repr = "OInc"

            self._configure_recents(str_repr, value)
            self._configure_incomes()
            self._make_graph()

    def return_to_main(self):
        self.main_frame.grid_remove()
        self.sidebar_frame.grid_remove()
        self.callback()
