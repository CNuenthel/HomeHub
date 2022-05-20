"""
Provides CRUD operations for authenticated gspread clients

ASYNC-GSPREAD class [AsyncSheetService] keyed out for retention, currently keeping use of
the synchronous [SheetService] class as the primary Google Sheets API front end for use
with higher level threading calls from TKBudget.

This authentication is required to use gspread library, which authenticates the app
and allows access to your Google Drive and Sheets through a service account O.auth2.
Details can be found here:

https://docs.gspread.org/en/latest/oauth2.html#enable-api-access

SheetService wraps the gspread library and includes a repeated Thread to constantly
update the sheet, so data can be queued without the requirement of an API call.

The thread will pull worksheet data from Google Sheets every 30 seconds (Google limits Sheets
API requests to 1 per second (according to asyncio-gspread). SheetService and gspread do not
limit API requests so this limit can be broke, removing authorization.
"""

# import gspread_asyncio   # Commented out for, used with asyncio-gspread
import gspread
import pathlib
import typing
# from google.oauth2 import service_account as sa  # Commented out for, used with asyncio-gspread
from NuenthelHub.secret import secret_path
import threading
import time

""" Typing Variables """
Pathlike = typing.Union[str, pathlib.Path]

""" Set service account path to variable for ease of use """
path_to_sa_key = secret_path.secret_path + "service_account.json"
scopes = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']


# def get_creds():
#     """ Creates credential object for gspread asyncio client manager """
#     creds = sa.Credentials.from_service_account_file(path_to_sa_key)
#     scoped = creds.with_scopes(scopes)
#     return scoped

"""
Simple Creds Variable for quick SheetsConnector

Authorization requires service account keyfile named "service_account" within
secret directory
"""
# SheetManager = gspread_asyncio.AsyncioGspreadClientManager(get_creds)
SyncSheetManager = gspread.service_account(path_to_sa_key, scopes)


class SheetService:
    """ Interacts with Google sheets using sheets data located in an authenticated clients drive

    @param: workbook_name {str} Name of sheet from Google sheets
    @param: sheet_index {int} Number of tab from within sheet (0+ from left to right)
    """
    def __init__(self, workbook_name: str, sheet_index: int):
        self.manager = SyncSheetManager
        self.workbook_name = workbook_name
        self.sheet_index = sheet_index
        self.worksheet = None
        self.get_worksheet()

    def get_worksheet(self):
        """ Pulls a spreadsheet page from a workbook """
        self.worksheet = self.manager.open(self.workbook_name).get_worksheet(self.sheet_index)

    def get_cell_value(self, alphanumeric_coord: str):
        """ Returns cell value at given alphanumeric coordinate, i.e. 'B1'

        @param alphanumeric_coord {str} Sheet numeric/alphabetic coordinate of a cell
        @param init {bool} Declares if data should be pulled via initialization to prevent rate limit error
        """
        return self.worksheet.acell(alphanumeric_coord).value

    def get_column_values(self, column_number: int) -> list:
        """ Returns all values of a desired column indexed from left to right

        @param column_number {int} Sheet column numeric ID
        @param init {bool} Declares if data should be pulled via initialization to prevent rate limit error
        """
        return self.worksheet.col_values(column_number)

    def update_cell(self, alphanumeric_coord: str, data: str or int):
        """ Updates a cell by alphanumeric index

        @param alphanumeric_coord {str} Sheet numeric/alphabetic coordinate of a cell
        @param data {str/int} Data to be posted to cell
        @param init {bool} Declares if data should be pulled via initialization to prevent rate limit error
        """
        return self.worksheet.update(alphanumeric_coord, data)

    def update_cell_by_coord(self, row_coord: int, col_coord: int, data: str or int):
        """ Updates a cell by sheet binary coordinates

        @param row_coord {int} Sheet row numeric coordinate
         @param col_coord {int} Sheet column numeric coordinate
        @param data {str/int} Data to be posted to cell
        """
        return self.worksheet.update_cell(row_coord, col_coord, data)


class RepeatTimer(threading.Timer):
    """ Subclass threading-Timer to run indefinitely """
    def run(self):
        """ Overwrite run function to continuously call function until told to stop """
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

# class AsyncSheetService:
#     """ Interacts with Google sheets using sheets data located in an authenticated clients drive """
#     def __init__(self, workbook_name, sheet_index):
#         self.manager = SheetManager
#         self.workbook_name = workbook_name
#         self.sheet_index = sheet_index
#         self.worksheet = None
#         """
#         Initializes class with authenticated client
#
#         Gspread commands can be called with client. Using open_workbook and calling these methods will reduce
#         API fetches.
#         """
#
#     async def open_worksheet(self):
#         """ Opens a Google Sheets workbook that already exists """
#         manager = SheetManager
#         client = await manager.authorize()
#         workbook = await client.open(self.workbook_name)
#         return await workbook.get_worksheet(self.sheet_index)
#
#     async def get_cell_value(self, alphanumeric_coord: str):
#         """ Returns cell value at given alphanumeric coordinate, i.e. 'B1' """
#         worksheet = await self.open_worksheet()
#         cell_data = await worksheet.acell(alphanumeric_coord)
#         return cell_data.value
#
#     async def get_column_values(self, column_number: int) -> list:
#         """ Returns all values of a desired column indexed from left to right """
#         worksheet = await self.open_worksheet()
#         return await worksheet.col_values(column_number)
#
#     async def update_cell(self, alphanumeric_coord: str, data: str or int):
#         """ Updates a cell by alphanumeric index"""
#         worksheet = await self.open_worksheet()
#         return await worksheet.update(alphanumeric_coord, data)
#
#     async def update_cell_by_coord(self, row_coord: int, col_coord: int, data: str or int):
#         """ Updates a cell by sheet binary coordinates"""
#         worksheet = await self.open_worksheet()
#         return await worksheet.update_cell(row_coord, col_coord, data)


