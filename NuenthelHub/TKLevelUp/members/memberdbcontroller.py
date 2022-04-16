"""
Creates easily to use liaison variable to TinyDB service for member db
"""

from tinydb import TinyDB
from tinydbservice import TinyDbService
from TKLevelUp.members.member import Member

"""Controller for managing members"""
MemberController = TinyDbService[Member](TinyDB("memberdb.json"), Member)
