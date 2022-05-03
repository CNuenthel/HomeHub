"""
Provides CRUD operations for authenticated gspread clients

"""
import gspread_asyncio
import pathlib
import typing
from google.oauth2 import service_account as sa
from NuenthelHub.secret import secret_path


""" Typing Variables """
Pathlike = typing.Union[str, pathlib.Path]

""" Set service account path to variable for ease of use """
path_to_sa_key = secret_path.secret_path + "service_account.json"


def get_creds():
    creds = sa.Credentials.from_service_account_file(path_to_sa_key)
    scoped = creds.with_scopes(
        ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive'])
    return scoped

"""
Simple Creds Variable for quick SheetsConnector

Authorization requires service account keyfile named "service_account" within
secret directory
"""
SheetManager = gspread_asyncio.AsyncioGspreadClientManager(get_creds)


class SheetService:
    """ Interacts with Google sheets using sheets data located in an authenticated clients drive """
    def __init__(self, workbook_name, sheet_index):
        self.manager = SheetManager
        self.workbook_name = workbook_name
        self.sheet_index = sheet_index
        self.worksheet = None
        """
        Initializes class with authenticated client

        Gspread commands can be called with client. Using open_workbook and calling these methods will reduce
        API fetches.
        """

    async def open_worksheet(self):
        """ Opens a Google Sheets workbook that already exists """
        manager = SheetManager
        client = await manager.authorize()
        workbook = await client.open(self.workbook_name)
        return await workbook.get_worksheet(self.sheet_index)

    async def get_cell_value(self, alphanumeric_coord: str):
        """ Returns cell value at given alphanumeric coordinate, i.e. 'B1' """
        worksheet = await self.open_worksheet()
        cell_data = await worksheet.acell(alphanumeric_coord)
        return cell_data.value

    async def get_column_values(self, column_number: int) -> list:
        """ Returns all values of a desired column indexed from left to right """
        worksheet = await self.open_worksheet()
        return await worksheet.col_values(column_number)

    async def update_cell(self, alphanumeric_coord: str, data: str or int):
        """ Updates a cell by alphanumeric index"""
        worksheet = await self.open_worksheet()
        return await worksheet.update(alphanumeric_coord, data)

    async def update_cell_by_coord(self, row_coord: int, col_coord: int, data: str or int):
        """ Updates a cell by sheet binary coordinates"""
        worksheet = await self.open_worksheet()
        return await worksheet.update_cell(row_coord, col_coord, data)


