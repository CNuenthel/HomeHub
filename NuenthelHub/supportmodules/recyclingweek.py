""" Holds RecycleTracker class """
from datetime import datetime, timedelta


class RecycleTracker:
    """ Returns boolean response advising of recycle week """
    def __init__(self):
        self.base_date = datetime(2022, 4, 7)

    def check_week(self) -> bool:
        """ Verifies if current week is a recycle week based off a known recycle date """
        if ((datetime.now() - self.base_date) % timedelta(days=15)).days < 9:
            return False
        return True


