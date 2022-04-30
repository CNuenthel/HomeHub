"""
Scraper module to access NDHP Intranet webapp

chromedriver.exe required to be present in root folder of matching Chrome
version number.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
from NuenthelHub.TKCalendar.event import EventController
from NuenthelHub.TKCalendar.event import Event
import json

"""Login Information for NDHP Intranet"""
with open("config.json", "r") as f:
    config = json.load(f)


class CodyWorkSchedule:
    def __init__(self):
        self.username = config["scraper_user"]
        self.password = config["scraper_pass"]

        self._scrape()

    def _scrape(self):
        # Open website in Chrome browser
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)  # Keeps window open
        browser = webdriver.Chrome(options=chrome_options)
        browser.get("https://apps.nd.gov/ndhp/dailyactivity/login.htm")
        browser.implicitly_wait(1)

        # Find and input username string
        username_input = browser.find_element(By.NAME, "j_username")
        username_input.send_keys(self.username)

        # Find and input user password string
        password_input = browser.find_element(By.NAME, "j_password")
        password_input.send_keys(self.password)

        # Submit creds
        submit_button = browser.find_element(By.NAME, "login")
        submit_button.click()

        # Click monthly
        monthly = browser.find_element(By.LINK_TEXT, "See My Monthly")
        monthly.click()

        self.raw_shifts = []
        self.raw_days = []

        def format_string_newline_to_int(text):
            """ Changes a string with a newline break to its componenent integer """
            if len(text) > 3:
                return int(text.splitlines()[0])
            return int(text)

        def format_string_shifts_to_int(text):
            """ Changes strings to integers, formats on call '*' and changes holiday/vacation days to 0 """
            if text[-1] == "*":
                return int(text[:-1])
            elif text in ["DO", "OH", "VA"]:
                return 0
            return int(text)

        for _ in range(6):
            # Collect schedule data
            tables_data = browser.find_element(By.ID, "smallText")
            period_list = tables_data.text.split(" ")  # Creates list from table

            self.raw_shifts.extend([format_string_shifts_to_int(text) for text in period_list[58:]])
            self.raw_days.extend([format_string_newline_to_int(text) for text in period_list[1:29]])

            # Next month data
            next_link = browser.find_element(By.CLASS_NAME, "next")
            next_link.click()
            browser.implicitly_wait(1)

        browser.close()

    # Format Data
        # Set list to start on current day
        start_index = self.raw_days.index(datetime.now().day)
        self.days = self.raw_days[start_index:]
        self.shifts = self.raw_shifts[start_index:]

        # Increment month/year values
        month_val = datetime.now().month
        year_val = datetime.now().year

        # Equal sized list of months and years from scraped data
        self.months = []
        self.years = []

        # change all day values to integers
        for day in self.days:

            # Format month/year counts
            if day == 1:
                month_val = int(month_val) + 1

            if month_val == 13:
                month_val = 1

                year_val = year_val + 1

            self.years.append(year_val)
            self.months.append(month_val)

        # Save Events
        e = Event()

        for i, j in enumerate(self.shifts):

            if j != 0:
                shift_dict = {
                    "year": self.years[i],
                    "month": self.months[i],
                    "day": self.days[i],
                    "time_hours": self.shifts[i],
                    "time_minutes": 0,
                    "category": "c-work",
                    "title": "C-Work"
                }

                for key in shift_dict:
                    setattr(e, key, shift_dict[key])

                EventController.insert(e)

