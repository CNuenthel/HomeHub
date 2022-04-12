
# class CodyWorkSchedule:
#     def __init__(self):
#         self.schedule = {}
#         self.username = ""
#         self.password = ""
#         self.schedule = {}
#         self.years = []
#         self.months = []
#         self.dates = []
#         self.shifts = []
#
#     def open_schedule(self):
#         # Credentials
#         username = self.username
#         password = self.password
#
#         # Open website in Chrome browser
#         chrome_options = Options()
#         chrome_options.add_experimental_option("detach", True)  # Keeps window open
#         browser = webdriver.Chrome(options=chrome_options)
#         browser.get("https://apps.nd.gov/ndhp/dailyactivity/login.htm")
#         browser.implicitly_wait(1)
#
#         # Find and input username string
#         username_input = browser.find_element(By.NAME, "j_username")
#         username_input.send_keys(username)
#
#         # Find and input user password string
#         password_input = browser.find_element(By.NAME, "j_password")
#         password_input.send_keys(password)
#
#         # Submit creds
#         submit_button = browser.find_element(By.NAME, "login")
#         submit_button.click()
#
#         # Click monthly
#         monthly = browser.find_element(By.LINK_TEXT, "See My Monthly")
#         monthly.click()
#
#         raw_shifts = []
#         raw_days = []
#         for _ in range(6):
#             # Collect schedule data
#             tables_data = browser.find_element(By.ID, "smallText")
#             period_list = tables_data.text.split(" ")  # Creates list from table
#
#             raw_shifts.extend(period_list[58:])
#             raw_days.extend(period_list[1:29])
#
#             # Next month data
#             next_link = browser.find_element(By.CLASS_NAME, "next")
#             next_link.click()
#             browser.implicitly_wait(1)
#
#         browser.close()
#
#         # Set list to start on current day
#         today = datetime.now().day
#         start_index = raw_days.index(str(today))
#         raw_days = raw_days[start_index:]
#         raw_shifts = raw_shifts[start_index:]
#
#         # Increment month/year values
#         month_val = str(datetime.now().month)
#         if len(month_val) < 2:
#             month_val = f"0{month_val}"
#         year_val = str(datetime.now().year)
#
#         # Equal sized list of months and years from scraped data
#         months = []
#         years = []
#
#         for day in raw_days:
#
#             # Remove newline characters
#             if len(day) > 3:
#                 i = raw_days.index(day)
#                 format_item = [char for char in day if char in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]]
#                 replacement = "".join(format_item)
#
#                 if len(replacement) < 2:
#                     replacement = f"0{replacement}"
#
#                 raw_days[i] = replacement
#
#             # Format single digit days
#             elif len(day) < 2:
#                 i = raw_days.index(day)
#                 replacement = f"0{day}"
#                 raw_days[i] = replacement
#
#             # Format month/year counts
#             if day == "1":
#                 month_val = int(month_val) + 1
#
#                 if len(str(month_val)) < 2:
#                     month_val = f"0{month_val}"
#                 else:
#                     month_val = str(month_val)
#
#             if month_val == "13":
#                 month_val = "01"
#
#                 year_val = str(int(year_val) + 1)
#
#             years.append(year_val)
#             months.append(month_val)
#
#         self.shifts.extend(raw_shifts)
#         self.dates.extend(raw_days)
#         self.years.extend(years)
#         self.months.extend(months)
#
#     def save_to_calendar_events(self):
#         # Start schedule save data at first of month
#         date_shifts = [[self.years[i], self.months[i], self.dates[i], self.shifts[i]] for i in range(len(self.shifts))
#                        if self.shifts[i] not in ["DO"]]
#
#         for item in date_shifts:
#             year = item[0]
#             month = item[1]
#             day = item[2]
#
#             if item[3] in ["OH", "VA"]:
#                 shift_time = item[3]
#             else:
#                 shift_time = f"{item[3]}:00"
#
#             event_string = f"{shift_time}-Cody Works"
#
#             event_object = Event(year, month, day, event_string)
#
#             eh = EventHandler()
#
#             eh.save_event(event_object)