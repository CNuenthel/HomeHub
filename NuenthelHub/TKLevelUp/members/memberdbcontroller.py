"""
Creates easily to use liaison variable to TinyDB service for member db
"""

from tinydb import TinyDB

from TKLevelUp.members.member import Member
from tinydbservice import TinyDbService

"""Controller for managing members"""
MemberController = TinyDbService[Member](TinyDB("memberdb.json"), Member)
