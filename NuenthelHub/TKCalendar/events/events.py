"""
Module to hold the event model
"""


class Event:
    """
    Models an event object
    """

    year: int = 0
    month: int = 0
    day: int = 0
    time_hours: int = 0
    time_minutes: int or str = "00"
    category: str = None
    title: str = None
    details: str = None
    id: int = None

    def __repr__(self):
        """ Override repr to show event contents """
        return str(self.__dict__)

    @staticmethod
    def create(kw_dict: dict):
        """
        Creates event from dictionary
        Parameters:
            kw_dict:
                dictionary of keyword pairs to assign to event object
        Returns:
            an Event object with attributes provided from kw_dict
        """
        event = Event()
        for key in kw_dict:
            setattr(event, key, kw_dict[key])
        return event
