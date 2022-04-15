"""
Module to hold the Chore model
"""


class Chore:
    """ Models a chore """
    name: str = None
    complete: bool = False
    last_completed_by: str = None
    category: str = None

    def __repr__(self):
        return str(self.__dict__)

    @staticmethod
    def create_from_dict(kw_dict: dict):
        """
        Creates event from dictionary
        Parameters:
            kw_dict:
                dictionary of keyword pairs to assign to event object
        Returns:
            an Event object with attributes provided from kw_dict
        """
        chore = Chore()
        for k, v in kw_dict.items():
            setattr(chore, k, v)
        return chore

