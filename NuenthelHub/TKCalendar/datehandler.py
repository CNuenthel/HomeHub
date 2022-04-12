"""
This module contains the DateHandler class. A collection of necessary functions to obtain
formatted data with respect to calendar operations.

"""

from calendar import monthcalendar, monthrange
from typing import List


class DateHandler:
    """
    Obtains and organizes routine calendar data

    Static Methods:

        date_list( year: int, month: int) -> list[int]
            Returns flattened monthcalendar matrix

        days_in_month(month:int, year:int) -> int
            Returns number of days in given month

        month_num_to_string(month: int) -> str
            Returns month name from numerical representation

    """

    @staticmethod
    def date_list(year: int, month: int) -> List[int]:
        """
        Flattens monthcalendar matrix

        Parameters:
            year:
                year represented numerically
            month:
                month represented numerically

        Returns:
            Returns a list representing a month’s calendar. Days outside the month
            are represented by zeros. Each week begins with Monday
        """
        month_calendar = monthcalendar(year, month)
        return [date_num for sublist in month_calendar for date_num in sublist]

    @staticmethod
    def days_in_month(month: int, year: int) -> int:
        """
        Returns number of days in a given month/year

        Parameters:
            month:
                month represented numerically
            year:
                year represented numerically

        Returns:
            int equal to number of days in given month
        """
        return monthrange(year, month)[1]

    @staticmethod
    def month_num_to_string(month: int) -> str:
        """
        Dictionary reference for transposing month nums to names

        Parameters:
            month:
                month represented numerically
        Returns:
            month represented by name
        """
        month_dict = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May",
                      6: "June", 7: "July", 8: "August", 9: "September", 10: "October",
                      11: "November", 12: "December"}
        return month_dict[month]
