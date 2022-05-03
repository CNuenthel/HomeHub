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
import asyncio


class NuenthelSheetsData:
    """
    Provides methods to allow CRUD operations on the N-Fam 2022 workbook, foremost sheet
    """

    def __init__(self):
        """
         Initializes with first sheet of the N-Fam 2022 budget workbook

         :param workbook Name of workbook as found in Google Drive
         """
        self.ss = SheetService("N-Fam 2022", 0)
        self.loop = asyncio.get_event_loop()
        self.expenses = ["Dining", "Grocery", "Transport", "Recreation", "Personal", "JL", "Other"]
        self.incomes = ["Cody", "Sam", "Other"]

    def get_expense_percent(self, category: str) -> int:
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
        return self.loop.run_until_complete(self.ss.get_cell_value("C86"))

    def get_budget_data(self) -> str:
        """ Returns value of total monthly bugdet funding """
        return self.loop.run_until_complete(self.ss.get_cell_value("C61"))

    async def get_cell_dollar_data(self, alphanum_cell_coord: str) -> str:
        """ Gets cell data from a dollar formatted cell, returns $0.00 if empty cell
        :param cell Dollar formatted cell alphanumeric coordinate
        """
        cell_value = await self.ss.get_cell_value(alphanum_cell_coord)
        if not cell_value:
            cell_value = "$0.00"
        return cell_value

    def get_cell_value(self, alphanum_cell_cord: str):
        return self.loop.run_until_complete(self.ss.get_cell_value(alphanum_cell_cord))

    def cumulate_dollar_format_cell(self, additional_value: float or int, alphanum_cell_coord: str) -> dict:
        """
        Updates cell, increments data to current value if true

        :param additional_value Data to increment or update in income cell
        :param alphanum_cell_coord alpha numeric coordinate of sheet cell
        """
        current_value = self.loop.run_until_complete(self.get_cell_dollar_data(alphanum_cell_coord))
        additional_value += self.reformat_dollar_string(current_value)
        return self.loop.run_until_complete(self.ss.update_cell(alphanum_cell_coord, additional_value))

    def add_expense(self, expense_column: int, expense: float) -> dict:
        """
        Adds expense to desired expense column on sheet

        :param expense_column Index of column for expense to be added
        :param expense Value of expense to be inserted
        """
        column_values = self.loop.run_until_complete(self.ss.get_column_values(expense_column))
        row = 1 + len(column_values)
        return self.loop.run_until_complete(self.ss.update_cell_by_coord(row, expense_column, expense))

    @staticmethod
    def reformat_dollar_string(dollar_string: str) -> float:
        """
        Reformats a dollar formatted sheet cell and returns value as float

        :param dollar_string Dollar formatted sheet string, i.e. '$5,322.60'
        """
        list_value = [char for char in dollar_string if char not in [",", "$"]]
        return float("".join(list_value))

