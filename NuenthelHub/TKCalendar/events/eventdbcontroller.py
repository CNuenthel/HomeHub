from tinydb import TinyDB
from tinydbservice.tinydbservice import TinyDbService
from events.events import Event

"""Controller for managing events"""
EventController = TinyDbService[Event](TinyDB("eventdb.json"), Event)
