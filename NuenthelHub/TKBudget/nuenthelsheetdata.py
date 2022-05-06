"""
Provides easy access sheet data from the NuenthelFamily Budget sheet

Current sheet data coupling limitations with assumed data:
    Expense Budgets: A,B,C * 77:84
    Expense Cumulative: A-G * 90:198
    Cody Income: C56
    Sam Income: C57
    Other Income: C58
    Total Budget: C61
    Total Used: C86

"""
from __future__ import annotations
from TKBudget.sheetservice import SheetService


class NuenthelSheetsData:
    """
    Provides methods to allow CRUD operations on the N-Fam 2022 workbook, foremost sheet
    """

    def __init__(self):
        """ Initializes with first sheet of the N-Fam 2022 budget workbook """
        self.ss = SheetService("N-Fam 2022", 0)
        self.expenses = ["Dining", "Grocery", "Transport", "Recreation", "Personal", "JL", "Other"]
        self.expense_cols = {category: i+1 for i, category in enumerate(self.expenses)}
        self.expense_alphanums = {category: "C"+str(i+78) for i, category in enumerate(self.expenses)}
        self.incomes = ["Cody", "Sam", "Other"]
        self.income_alphanums = {"Cody": "C56", "Sam": "C57", "Other": "C58"}

    def get_expense_percent(self, category: str) -> int:
        """ Return percent cell value of a given expense category

        :param category Category of expense
        """
        if category not in self.expenses:
            raise ValueError(f"Invalid category passed to function: {category} not found. Valid arguments: "
                             "Dining, Grocery, Transport, Recreation, Personal, JL, Other")
        match category:
            case "Dining":
                return int(self.get_cell_value("B78")[:-1])
            case "Grocery":
                return int(self.get_cell_value("B79")[:-1])
            case "Transport":
                return int(self.get_cell_value("B80")[:-1])
            case "Recreation":
                return int(self.get_cell_value("B81")[:-1])
            case "Personal":
                return int(self.get_cell_value("B82")[:-1])
            case "JL":
                return int(self.get_cell_value("B83")[:-1])
            case "Other":
                return int(self.get_cell_value("B84")[:-1])

    def get_expense_total(self, category: str) -> int:
        """ Return cell value of a given expense category

        :param category Category of expense
        """
        if category not in self.expenses:
            raise ValueError(f"Invalid category passed to function: {category} not found. Valid arguments: "
                             "Dining, Grocery, Transport, Recreation, Personal, JL, Other")
        match category:
            case "Dining":
                return self.get_cell_value("C78")
            case "Grocery":
                return self.get_cell_value("C79")
            case "Transport":
                return self.get_cell_value("C80")
            case "Recreation":
                return self.get_cell_value("C81")
            case "Personal":
                return self.get_cell_value("C82")
            case "JL":
                return self.get_cell_value("C83")
            case "Other":
                return self.get_cell_value("C84")

    def get_income_total(self, category: str) -> int:
        """ Returns income cell value for Cody, Sam or Other

        :param category Category of income, Cody, Sam or Other
        """
        if category not in self.incomes:
            raise ValueError(f"Invalid category passed to function: {category} not found. Valid arguments: "
                             f"Cody, Sam, Other")
        match category:
            case "Cody":
                return self.get_cell_value("C56")
            case "Sam":
                return self.get_cell_value("C57")
            case "Other":
                return self.get_cell_value("C58")

    def get_used_data(self) -> str:
        """ Returns value of total monthly budget used """
        return self.ss.get_cell_value("C86")

    def get_budget_data(self) -> str:
        """ Returns value of total monthly bugdet funding """
        return self.ss.get_cell_value("C61")

    def get_cell_dollar_data(self, alphanum_cell_coord: str) -> str:
        """ Gets cell data from a dollar formatted cell, returns $0.00 if empty cell

        :param alphanum_cell_coord Dollar formatted cell alphanumeric coordinate
        """
        cell_value = self.ss.get_cell_value(alphanum_cell_coord)
        if not cell_value:
            cell_value = "$0.00"
        return cell_value

    def get_cell_value(self, alphanum_cell_cord: str):
        return self.ss.get_cell_value(alphanum_cell_cord)

    def cumulate_dollar_format_cell(self, additional_value: float or int, alphanum_cell_coord: str) -> dict:
        """
        Updates cell, increments data to current value if true

        :param additional_value Data to increment or update in income cell
        :param alphanum_cell_coord alpha numeric coordinate of sheet cell
        """
        current_value = self.get_cell_dollar_data(alphanum_cell_coord)
        additional_value += self.reformat_dollar_string(current_value)
        return self.ss.update_cell(alphanum_cell_coord, additional_value)

    # TODO This is currently throwing an exception for incorrect cell label for self.worksheet.col_values(
    def add_expense(self, category: str, expense: float) -> dict:
        """
        Adds expense to desired expense column on sheet

        :param category Name of expense column
        :param expense Value of expense to be inserted
        """
        column_values = self.ss.get_column_values(self.expense_cols[category])
        row = 1 + len(column_values)
        return self.ss.update_cell_by_coord(row, self.expense_cols[category], expense)

    @staticmethod
    def reformat_dollar_string(dollar_string: str) -> float:
        """
        Reformats a dollar formatted sheet cell and returns value as float

        :param dollar_string Dollar formatted sheet string, i.e. '$5,322.60'
        """
        list_value = [char for char in dollar_string if char not in [",", "$"]]
        return float("".join(list_value))
