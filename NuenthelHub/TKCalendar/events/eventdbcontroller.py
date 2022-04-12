from tinydb import TinyDB
from tinydbservice import TinyDbService
from TKCalendar.events.events import Event

"""Controller for managing events"""
EventController = TinyDbService[Event](TinyDB("eventdb.json"), Event)
