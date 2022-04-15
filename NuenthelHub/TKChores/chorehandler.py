from NuenthelHub.TKChores.chores.choredbcontroller import ChoreController
from NuenthelHub.TKChores.chores.chore import Chore
from datetime import datetime, timedelta
from random import choices
from math import ceil


class ChoreHandler:
    def __init__(self):
        self.db = ChoreController

        self.daily_chores = self.db.find_by_element("category", "Daily")
        self.weekly_chores = self.db.find_by_element("category", "Weekly")
        self.monthly_chores = self.db.find_by_element("category", "Monthly")
        self.base_date = datetime(2022, 4, 10)

        self._set_weekly_portional()
        self._set_monthly_portional()

    def insert_chore(self, chore: Chore):
        return self.db.insert(chore)

    def remove_chore(self, chore_dict: dict):
        chore_query = self.db.find_by_elements(chore_dict)
        for chore in chore_query:
            ChoreController.remove_doc(chore["id"])

    def _set_weekly_portional(self):
        self.days_left = 7 - ((datetime.now() - self.base_date) % timedelta(days=7)).days

    def _set_monthly_portional(self):
        self.months_left = 12 - datetime.now().month

    def get_dailies(self):
        uncompleted_chores = [chore for chore in self.daily_chores if not chore["complete"]]
        return uncompleted_chores

    def select_weekly_chores(self):
        uncompleted_chores = [chore for chore in self.weekly_chores if not chore["complete"]]
        chore_number = ceil(len(uncompleted_chores)/self.days_left)
        return choices(uncompleted_chores, k=chore_number)

    def select_monthly_chores(self):
        uncompleted_chores = [chore for chore in self.monthly_chores if not chore["complete"]]
        chore_number = ceil(len(uncompleted_chores)/self.months_left)
        return choices(uncompleted_chores, k=chore_number)


if __name__ == '__main__':
    x = ChoreHandler()
    print(x.get_dailies())