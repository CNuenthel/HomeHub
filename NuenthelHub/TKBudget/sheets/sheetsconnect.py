"""
Authenticates app with Google Sheets, Google Drive

"""
import gspread
import pathlib
import typing

Pathlike = typing.Union[str, pathlib.Path]


class SheetsConnector:
    """Authenticates a service account login to google drive and sheets, returns client """

    scope: list = ['https://spreadsheets.google.com/feeds',
                   'https://www.googleapis.com/auth/drive']

    def service_account_connect(self) -> gspread.client:
        """
        Connects using service account json in environment

        service_account.json MUST be located at
        IOS: ~\.config\gspread\service_account.json.
        Windows: %APPDATA%\gspread\service_account.json.

        This allows opening without filename requirement, service_account credentials may also
        be opened by path - see sheetcreds.py for sheets by path connection
        """
        try:
            result = gspread.service_account(scopes=self.scope)
            print("Successfully authenticated sheets API")
            return result

        except FileNotFoundError:
            raise FileNotFoundError("Failed to find service_account.json in required path")

    def service_account_connect_by_path(self, path_to_sa_key: Pathlike) -> gspread.client:
        """Connects using service account json at specified path

        :param path_to_sa_key absolute or relative path to service_account.json file
        """
        result = gspread.service_account(filename=path_to_sa_key, scopes=self.scope)
        print("Successfully authenticated sheets API")
        return result

