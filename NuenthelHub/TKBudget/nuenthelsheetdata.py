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

    async def _get_expense_components(self):
        """ Returns expense percents, omitting 'Saving' """
        return await asyncio.gather(
            self.ss.get_column_values(2),
            self.ss.get_column_values(3),
            self.ss.get_column_values(1))

    def get_expense_data(self):
        percent_col_info, dollar_col_info, labels_info = self.loop.run_in_executor(self._get_expense_components())
        labels = labels_info[77:84]
        vals = [f"${self.reformat_dollar_string(exp)}" for exp in dollar_col_info[77:84]]
        perc = [int(perc[:-1]) for perc in percent_col_info[77:84]]
        return {labels[i]: [{"perc": perc[i]}, {"val": vals[i]}] for i in range(len(perc))}

    def get_used_data(self) -> str:
        """ Returns value of total monthly budget used """
        return asyncio.run(self.ss.get_cell_value("C86"))

    def get_budget_data(self) -> str:
        """ Returns value of total monthly bugdet funding """
        return asyncio.run(self.ss.get_cell_value("C61"))

    async def get_cell_dollar_data(self, alphanum_cell_coord: str) -> str:
        """ Gets cell data from a dollar formatted cell, returns $0.00 if empty cell
        :param cell Dollar formatted cell alphanumeric coordinate
        """
        cell_value = await self.ss.get_cell_value(alphanum_cell_coord)
        if not cell_value:
            cell_value = "$0.00"
        return cell_value

    def cumulate_dollar_format_cell(self, additional_value: float or int, alphanum_cell_coord: str) -> dict:
        """
        Updates cell, increments data to current value if true

        :param additional_value Data to increment or update in income cell
        :param alphanum_cell_coord alpha numeric coordinate of sheet cell
        """
        current_value = asyncio.run(self.get_cell_dollar_data(alphanum_cell_coord))
        additional_value += self.reformat_dollar_string(current_value)
        return asyncio.run(self.ss.update_cell(alphanum_cell_coord, additional_value))

    async def add_expense(self, expense_column: int, expense: float) -> dict:
        """
        Adds expense to desired expense column on sheet

        :param expense_column Index of column for expense to be added
        :param expense Value of expense to be inserted
        """
        column_values = asyncio.run(self.ss.get_column_values(expense_column))
        row = 1 + len(column_values)
        return asyncio.run(self.ss.update_cell_by_coord(row, expense_column, expense))

    @staticmethod
    def reformat_dollar_string(dollar_string: str) -> float:
        """
        Reformats a dollar formatted sheet cell and returns value as float

        :param dollar_string Dollar formatted sheet string, i.e. '$5,322.60'
        """
        list_value = [char for char in dollar_string if char not in [",", "$"]]
        return float("".join(list_value))

