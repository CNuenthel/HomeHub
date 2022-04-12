from datetime import datetime
from functools import partial
from tkinter import *

from TKCalendar.events.eventdbcontroller import EventController
from NuenthelHub.TKCalendar.datehandler import DateHandler as dH
from NuenthelHub.TKCalendar.eventcolor import EventColor
from modifiedwidgets import HoverButton
from TKCalendar.toplevels.daytoplevel import DayTopWindow
from TKCalendar.tkwindowextensions.tk_legend import TKLegend
from TKCalendar.img.imgpath import image_path


class TKCalendar(Tk):
    """ TKinter Calendar """

    def __init__(self):
        super().__init__()

        """ Window Attributes """
        self.minsize(width=500, height=350)
        self.title("Chores")
        self.main_frame = None

        """ Internal Functions """
        self._configure_rows_columns()

    def _create_main_frame(self):
        self.main_frame = Frame(self)

    def _configure_rows_columns(self):
        """ Configures rows and columns to expand with resize of window """
        columns, rows = self.grid_size()
        for columns in range(columns):
            self.columnconfigure(columns, weight=1)
        for rows in range(rows):
            self.rowconfigure(rows, weight=1)

    """ ______________________________________Button Functions ________________________________________________"""

def btn_pushed():
    print("Button Pushed!")

