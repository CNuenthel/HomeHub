from NuenthelHub.TKChores.chore import ChoreController
from TKChores.chore import Chore
from datetime import datetime


class ChoreHandler:
    def __init__(self):
        self.db = ChoreController
        self.base_date = datetime(2022, 4, 10)

    def remove_chore(self, chore_dict: dict):
        chore_query = self.db.find_by_elements(chore_dict)
        for chore in chore_query:
            ChoreController.remove_doc(chore["id"])

    def get_dailies(self):
        return self.db.find_by_element("category", "Daily")

    def get_weeklies(self):
        return self.db.find_by_element("category", "Weekly")

    def get_monthlies(self):
        return self.db.find_by_element("category", "Monthly")

    def reset_daily_chores(self):
        daily_chores = self.db.find_by_element("category", "Daily")
        for doc in daily_chores:
            self.db.update_doc_element("complete", False, doc.doc_id)

    def reset_weekly_chores(self):
        weekly_chores = self.db.find_by_element("category", "Weekly")
        for doc in weekly_chores:
            self.db.update_doc_element("complete", False, doc.doc_id)

    def reset_monthly_chores(self):
        monthly_chores = self.db.find_by_element("category", "Monthly")
        for doc in monthly_chores:
            self.db.update_doc_element("complete", False, doc.doc_id)


if __name__ == '__main__':
    x = ChoreHandler()
    print(x.get_weeklies())