"""
Holds the Member model
"""
from dataclasses import dataclass
from tinydb import TinyDB
from tinydbservice import TinyDbService


@dataclass
class Member:
    """Models a household member"""
    name: str = ""
    xp: int = 0
    level: int = 0
    color: str = "green"
    id: int = None

    def __repr__(self):
        return str(self.__dict__)

    @staticmethod
    def create_from_dict(kw_dict: dict):
        """
        Creates member from dictionary
        Parameters:
            kw_dict:
                dictionary of keyword pairs to assign to member object
        Returns:
            a member object with attributes provided from kw_dict
        """
        mem = Member()
        for k, v in kw_dict.items():
            if k == "xp_bar":
                continue
            setattr(mem, k, v)
        return mem


"""Controller for managing members"""
MemberController = TinyDbService[Member](TinyDB("memberdb.json"), Member)
