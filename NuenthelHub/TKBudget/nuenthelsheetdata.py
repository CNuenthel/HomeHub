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

from TKBudget.sheets.sheetcreds import SheetCreds
from TKBudget.sheets.sheetservice import SheetService


class NuenthelSheetsData:
    """
    Authorizes and loads Google Drive and Sheets scoped client houses methods to
    access sheet data from N-Fam 2022 workbook
    """
    ss = SheetService(SheetCreds)

    def __init__(self, workbook: str):
        """
         Initializes with first sheet of the N-Fam 2022 budget workbook

         :param workbook Name of workbook as found in Google Drive
         """
        self.wkb = self.ss.open_workbook(workbook)
        self.wks = self.ss.select_worksheet(0)

    def get_expense_data(self) -> dict:
        """ Returns expense percents, omitting 'Saving' """
        perc = [int(perc[:-1]) for perc in self.ss.get_column_values(2)[77:84]]
        vals = [f"${self.reformat_dollar_string(exp)}" for exp in self.ss.get_column_values(3)[77:84]]
        labels = self.ss.get_column_values(1)[77:84]
        return {labels[i]: [{"perc": perc[i]}, {"val": vals[i]}] for i in range(len(perc))}

    def get_used_data(self) -> str:
        """ Returns value of total monthly budget used """
        return self.ss.get_cell_value("C86")

    def get_budget_data(self) -> str:
        """ Returns value of total monthly bugdet funding """
        return self.ss.get_cell_value("C61")

    def get_cell_dollar_data(self, alphanum_cell_coord: str) -> str:
        """ Gets cell data from a dollar formatted cell, returns $0.00 if empty cell
        :param cell Dollar formatted cell alphanumeric coordinate
        """
        cell_value = self.ss.get_cell_value(alphanum_cell_coord)
        if not cell_value:
            cell_value = "$0.00"
        return cell_value

    def update_dollar_format_cell(self, data: float or int, alphanum_cell_coord: str) -> dict:
        """
        Updates cell, increments data to current value if true

        :param data Data to increment or update in income cell
        :param alphanum_cell_coord alpha numeric coordinate of sheet cell
        """
        current_value = self.get_cell_dollar_data(alphanum_cell_coord)
        data += self.reformat_dollar_string(current_value)
        return self.ss.update_cell(alphanum_cell_coord, data)

    def add_expense(self, expense_column: int, expense: float) -> dict:
        """
        Adds expense to desired expense column on sheet

        :param expense_column Index of column for expense to be added
        :param expense Value of expense to be inserted
        """
        row = 1 + len(self.ss.get_column_values(expense_column))
        return self.ss.update_cell_by_coord(row, expense_column, expense)

    @staticmethod
    def reformat_dollar_string(dollar_string: str) -> float:
        """
        Reformats a dollar formatted sheet cell and returns value as float

        :param dollar_string Dollar formatted sheet string, i.e. '$5,322.60'
        """
        list_value = [char for char in dollar_string if char not in [",", "$"]]
        return float("".join(list_value))

