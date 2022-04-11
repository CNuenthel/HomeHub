"""
Provides CRUD operations for authenticated gspread clients

"""

import gspread as gs
import gspread.worksheet
from typing import List


class SheetService:
    """ Interacts with Google sheets using sheets data located in an authenticated clients drive """
    client: gs.client

    def __init__(self, client: gs.client):
        """
        Initializes class with authenticated client

        Gspread commands can be called with client. Using open_workbook and calling these methods will reduce
        API fetches.
        """
        self.client = client
        self.wkb = None
        self.wks = None

    def open_workbook(self, sheet_name: str) -> gspread.worksheet.Worksheet:
        """ Opens a Google Sheets workbook that already exists """
        self.wkb = self.client.open(sheet_name)
        return self.wkb

    def select_worksheet(self, sheet_index: int):
        """ Focuses specific sheet from workbook, index of sheets begins at 0 from left sheet tab to right """
        if self.wkb is not None:
            self.wks = self.wkb.get_worksheet(sheet_index)
            return self.wks
        raise AttributeError("You have not selected a workbook - use open_workbook to focus a workbook")

    def create_sheet(self, sheet_name: str):
        """ Creates a fresh Google Sheet """
        return self.client.create(sheet_name)

    def create_worksheet(self, worksheet_name: str, rows: int, cols: int):
        """ Creates a worksheet within workbook with designated rows and columns """
        if self.wkb is not None:
            return self.wkb.add_worksheet(title=worksheet_name, rows=rows, cols=cols)
        raise AttributeError("You have not selected a workbook - use open_workbook to focus a workbook")

    def get_cell_value(self, alphanumeric_coord: str):
        """ Returns cell value at given alphanumeric coordinate, i.e. 'B1' """
        if self.wks is not None:
            return self.wks.acell(alphanumeric_coord).value
        raise AttributeError("You have not selected a worksheet - use select_worksheet to focus a sheet")

    def get_row_values(self, row_number: int) -> List:
        """ Returns all values of a desired row indexed top to bottom """
        if self.wks is not None:
            return self.wks.row_values(row_number)
        raise AttributeError("You have not selected a worksheet - use select_worksheet to focus a sheet")

    def get_column_values(self, column_number: int) -> list:
        """ Returns all values of a desired column indexed from left to right """
        if self.wks is not None:
            return self.wks.col_values(column_number)
        raise AttributeError("You have not selected a worksheet - use select_worksheet to focus a sheet")

    def get_all_values(self) -> list:
        """ Returns all values of set worksheet """
        if self.wks is not None:
            return self.wks.get_all_values()
        raise AttributeError("You have not selected a worksheet - use select_worksheet to focus a sheet")

    def update_cell(self, alphanumeric_coord: str, data: str or int):
        """ Updates a cell by alphanumeric index"""
        if self.wks is not None:
            return self.wks.update(alphanumeric_coord, data)
        raise AttributeError("You have not selected a worksheet - use select_worksheet to focus a sheet")

    def update_cell_by_coord(self, row_coord: int, col_coord: int, data: str or int):
        """ Updates a cell by sheet binary coordinates"""
        if self.wks is not None:
            return self.wks.update_cell(row_coord, col_coord, data)
        raise AttributeError("You have not selected a worksheet - use select_worksheet to focus a sheet")





