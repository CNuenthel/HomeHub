"""
Simple Creds Variable for quick SheetsConnector

Authorization
"""
from TKBudget.sheets.sheetsconnect import SheetsConnector

SheetCreds = SheetsConnector().service_account_connect()

""" Callable - Path to service account creds required """
SheetCredsByPath = SheetsConnector().service_account_connect_by_path

