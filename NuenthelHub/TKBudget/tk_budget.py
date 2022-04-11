from functools import partial
from tkinter import *

from TKBudget.nuenthelsheetdata import NuenthelSheetsData
from tkwidgetclasses.hoverbutton import HoverButton
from tkwidgetclasses.hoverlabel import HoverLabel
from tkwidgetclasses.snapbackentry import SnapbackEntry
from TKBudget.expenseplot import ExpensePlot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

bg_color = "#909090"
border_color = "#9594B7"
font = "Roboto "
header_color = "#232323"


class TKBudget(Toplevel):
    """ Creates a top level GUI for budget handling """

    def __init__(self):
        super().__init__()
        """Window Attributes"""
        self.title("Budget")
        self.configure(background=bg_color)
        self.bind_all("<Button-1>", lambda event: event.widget.focus_set())
        self.geometry("")

        """External Helper Classes"""
        self.nfsheet = NuenthelSheetsData("N-Fam 2022")

        """Widgets"""
        self.expense_entries = []
        self.expense_labels = []
        self.expense_hbuttons = []
        self.recents = []
        self.income_entries = []
        self.income_buttons = []
        self.budget_entry = None
        self.used_entry = None
        self.graph_frame = None

        """GUI Constructor Functions"""
        self._make_header()
        self._make_expenses()
        self._make_recent()
        self._make_income()
        self._make_graph()

        """GUI Configuration Functions"""
        self._configure_rows_cols(self)
        self._configure_expense_labels()
        self._configure_expense_entries()
        self._configure_incomes()

    def _make_header(self):
        self.header_frame = Frame(self, background=header_color, relief=FLAT)
        self.header_frame.grid(row=0, column=0, columnspan=8, sticky=NSEW)
        self.header_label = Label(self.header_frame, bg=header_color, fg="white", text="Budget",
                                  font=font + "25 underline")
        self.header_label.grid(row=0, column=0, columnspan=1, sticky=NSEW, padx=15)
        self.darklight_frame = Frame(self, background=header_color, relief=FLAT)
        self.darklight_frame.grid(row=1, column=0, columnspan=8, sticky=NSEW)

    def _make_expenses(self):
        self.border_frame = Frame(self, background=border_color, borderwidth=3, relief=GROOVE)
        self.border_frame.grid(row=1, column=0, columnspan=3, rowspan=8, sticky=NSEW, padx=10, pady=10)
        self.expense_frame = Frame(self.border_frame, background=bg_color, borderwidth=3, relief=GROOVE)
        self.expense_frame.grid(row=0, column=0, columnspan=3, rowspan=8, padx=5, pady=5, ipadx=10, ipady=10,
                                sticky=NSEW)

        self._configure_rows_cols(self.border_frame)
        self._configure_rows_cols(self.expense_frame)

        Label(self.expense_frame, text="Expenses", font=font + "15", bg="#909090").grid(row=0, column=0, padx=5, pady=5,
                                                                                        sticky=W)
        HoverButton(self.expense_frame, text="Update", command=self._configure_expense_entries, relief=GROOVE, width=25,
                    bg=header_color, fg="white") \
            .grid(row=0, column=1, columnspan=1)

        labels = ["Din", "Gro", "Tra", "Rec", "Per", "J&L", "Oth"]
        for i, j in enumerate(labels, 1):
            label = Label(self.expense_frame, text=j, font=font + "12")
            label.grid(row=i, column=0, padx=5, pady=5, sticky=NSEW)
            self.expense_labels.append(label)

            entry = SnapbackEntry(self.expense_frame, font=font + "12", justify=CENTER)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky=NSEW)
            self.expense_entries.append(entry)

            # We add partial function to pass in an int between 0 and 7 for each button to declare expense column,
            # This allows for cross list indexing to match buttons to entries
            commands = [partial(self.cumulate_expense, i) for i in range(7)]
            for ind, ja in enumerate(commands, 1):
                HoverButton(self.expense_frame, text="+", command=ja, relief=FLAT, bg=header_color, fg="white") \
                    .grid(row=ind, column=2, pady=5, padx=5, sticky=NSEW)

    def _make_recent(self):
        border_frame = Frame(self, background=border_color, borderwidth=3, relief=GROOVE)
        border_frame.grid(row=1, column=3, columnspan=2, rowspan=8, sticky=NSEW, padx=10, pady=10)
        self.recent_frame = Frame(border_frame, background=bg_color, borderwidth=3, relief=GROOVE)
        self.recent_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=5, ipadx=10, ipady=10, sticky=NSEW)

        self._configure_rows_cols(border_frame)
        self._configure_rows_cols(self.recent_frame)

        Label(self.recent_frame, text="Recent", font=font + "12 bold", bg=bg_color).pack()

        for i in range(11):
            self.x = HoverLabel(self.recent_frame, text="", font=font + "12", bg=bg_color)
            self.x.pack()
            self.recents.append(self.x)

    def _make_income(self):
        border_frame = Frame(self, background=border_color, borderwidth=3, relief=GROOVE)
        border_frame.grid(row=1, column=5, columnspan=3, rowspan=3, sticky=NSEW, padx=10, pady=10)
        income_frame = Frame(border_frame, background=bg_color, borderwidth=3, relief=GROOVE)
        income_frame.grid(row=0, column=0, columnspan=2, rowspan=3, padx=5, pady=5, ipadx=10, ipady=10, sticky=NSEW)

        self._configure_rows_cols(border_frame)
        self._configure_rows_cols(income_frame)

        labels = ["Cody", "Sam", "Other"]
        for i, j in enumerate(labels):
            Label(income_frame, text=j, font=font + "12 bold", bg=bg_color).grid(row=i, column=0, pady=5, padx=5,
                                                                                 sticky=NSEW)
            x = SnapbackEntry(income_frame, font=font + "9 italic", justify=CENTER)
            x.grid(row=i, column=1, pady=5, padx=5, sticky=NSEW)
            self.income_entries.append(x)

        commands = [partial(self.cumulate_income, i) for i in range(3)]
        for ind, ja in enumerate(commands):
            y = HoverButton(income_frame, text="+", command=ja, relief=FLAT, bg=header_color, fg="white")
            y.grid(row=ind, column=2, sticky=EW, padx=5)
            self.income_buttons.append(y)

    def _make_graph(self):
        if self.graph_frame is not None:
            self.graph_frame.destroy()

        self.graph_frame = Frame(self, background=border_color, borderwidth=3, relief=GROOVE)
        self.graph_frame.grid(row=4, column=5, columnspan=3, rowspan=5, sticky=NSEW, padx=10, pady=10)
        self._configure_rows_cols(self.graph_frame)
        figure = ExpensePlot().get_plot()
        bar_graph = FigureCanvasTkAgg(figure, self.graph_frame)
        bar_graph.get_tk_widget().pack(padx=10, pady=10)

    # """_______________These configurations are specific to my family budget sheet__________________________________"""

    @staticmethod
    def _configure_rows_cols(master):
        """ Configure rows to 1:1 weight """
        for i in range(master.grid_size()[1]):
            master.rowconfigure(i, weight=1)
        for i in range(master.grid_size()[0]):
            master.columnconfigure(i, weight=1)

    def _configure_expense_labels(self):
        """
        Configures button color changes based on expense percentages
        Assumes order of expenses are:
        [Dining, Grocery, Transport, Recreation, Personal, J&L, Other]
        """
        expense_data = self.nfsheet.get_expense_data()
        perc_list = [expense_data[key][0]["perc"] for key in expense_data.keys()]

        for i, j in enumerate(self.expense_labels):
            if perc_list[i] < 50:
                j.configure(bg="#ccfdcc")
            elif 50 < perc_list[i] < 75:
                j.configure(bg="#F9FDCC")
            elif 75 < perc_list[i] < 90:
                j.configure(bg="#FDF1CC")
            elif perc_list[i] > 90:
                j.configure(bg="#FDD0CC")

    def _configure_expense_entries(self):
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
            self._configure_expense_entries()  # Recalculate and show expense entries
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


def open_budget():
    TKBudget().mainloop()
