from tinydb import TinyDB
from tinydbservice import TinyDbService
from TKChores.chores.chore import Chore

"""Controller for managing chores"""
ChoreController = TinyDbService[Chore](TinyDB("choredb.json"), Chore)
