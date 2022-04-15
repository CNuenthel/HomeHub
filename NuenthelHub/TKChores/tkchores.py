import json
from tkinter import Tk, Frame, FLAT, Label, NSEW, GROOVE, OptionMenu, StringVar, PhotoImage, Button
from NuenthelHub.TKCalendar.img.imgpath import image_path

bg_color = "#909090"
border_color = "#9594B7"
font = "Roboto "
header_color = "#232323"

with open("C:/Users/cnuen/OneDrive/Desktop/Github/HomeHub/NuenthelHub/TKChores/chores/chores.json", "r") as f:
    chores = json.load(f)


class TKChores(Tk):
    """ TKinter household chores manager """

    def __init__(self):
        super().__init__()

        """ Window Attributes """
        self.configure(background=bg_color)
        self.title("Chores")
        self.chores = chores
        self.columns = 4
        self.daily_chores = []
        self.weekly_chores = []
        self.monthly_chores = []

        """ Internal Functions """
        self._make_header()
        self._make_daily_chore_window()
        self._make_weekly_chore_window()
        self._make_monthly_chore_window()

        """ Configure Functions """
        self._configure_rows_cols(self)
        self._configure_daily_chore_window()
        self._configure_weekly_chore_window()
        self._configure_monthly_chore_window()

    def _make_header(self):
        """ Creates dark background header """
        self.header_frame = Frame(self, background=header_color, relief=FLAT)
        self.header_frame.grid(row=0, column=0, columnspan=3, sticky=NSEW)
        self.header_label = Label(self.header_frame, bg=header_color, fg="white", text="Chores",
                                  font=font + "25 underline")
        self.header_label.grid(row=0, column=0, columnspan=1, sticky=NSEW, padx=15)

    def _make_daily_chore_window(self):
        """ Makes first chore frame for daily chore information """
        self.darklight_frame = Frame(self, background=header_color, relief=GROOVE)
        self.darklight_frame.grid(row=1, column=0, rowspan=1, columnspan=3, sticky=NSEW)

        self.border_frame = Frame(self, background=border_color, borderwidth=3, relief=GROOVE)
        self.border_frame.grid(row=1, column=0, rowspan=2, columnspan=3, sticky=NSEW, padx=10, pady=10)

        self.daily_chore_frame = Frame(self.border_frame, background=bg_color, borderwidth=3, relief=GROOVE)
        self.daily_chore_frame.grid(row=0, column=0, columnspan=3, padx=5, rowspan=2, pady=5, ipadx=10, ipady=10,
                                    sticky=NSEW)

        Label(self.daily_chore_frame, text="Daily", font=font + "15 underline", bg=bg_color).grid(row=0, column=1)
        self._configure_rows_cols(self.border_frame)
        self._configure_rows_cols(self.daily_chore_frame)

    def _make_weekly_chore_window(self):
        """ Makes second chore frame for weekly chore information """
        self.border_frame = Frame(self, background=border_color, borderwidth=3, relief=GROOVE)
        self.border_frame.grid(row=3, column=0, columnspan=3, sticky=NSEW, padx=10, pady=10)
        self.weekly_chore_frame = Frame(self.border_frame, background=bg_color, borderwidth=3, relief=GROOVE)
        self.weekly_chore_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=5, ipadx=10, ipady=10,
                                     sticky=NSEW)

        Label(self.weekly_chore_frame, text="Weekly", font=font + "15 underline", bg=bg_color).grid(row=0, column=1)
        self._configure_rows_cols(self.border_frame)
        self._configure_rows_cols(self.weekly_chore_frame)

    def _make_monthly_chore_window(self):
        """ Makes third chore frame for monthly chore information """
        self.border_frame = Frame(self, background=border_color, borderwidth=3, relief=GROOVE)
        self.border_frame.grid(row=4, column=0, columnspan=3, sticky=NSEW, padx=10, pady=10)
        self.monthly_chore_frame = Frame(self.border_frame, background=bg_color, borderwidth=3, relief=GROOVE)
        self.monthly_chore_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=5, ipadx=10, ipady=10,
                                      sticky=NSEW)

        Label(self.monthly_chore_frame, text="Monthly", font=font + "15 underline", bg=bg_color).grid(row=0, column=1)
        self._configure_rows_cols(self.border_frame)
        self._configure_rows_cols(self.monthly_chore_frame)

    def _configure_daily_chore_window(self):
        """ Configures daily chore window to display uncompleted chores """
        # Daily
        for chore in self.chores["daily"]:
            if not self.chores["daily"][chore]["complete"]:
                # Labels
                lbl = Label(self.daily_chore_frame, text=chore, font=font + "12", bg="#FDD0CC")

                # Option Menu - complete by
                var = StringVar(self)
                var.set("Select")
                person_om = OptionMenu(self.daily_chore_frame, var, *["Cody", "Sam"])
                person_om.config(width=15, bg=bg_color)

                # Option Menu - complete
                var = StringVar(self)
                var.set("Not Complete")
                complete_om = OptionMenu(self.daily_chore_frame, var, *["Complete", "Not Complete"])
                complete_om.config(width=15, bg=bg_color)

                # Remove D. Chore Btn
                rmv_btn = Button(self.daily_chore_frame, bg=bg_color, relief=FLAT, command=btn_pushed, text="-", width=10)
                self.daily_chores.append([lbl, person_om, complete_om, rmv_btn])

        for i, j in enumerate(self.daily_chores, 1):
            j[0].grid(row=i, column=0, padx=5, pady=5)
            j[1].grid(row=i, column=1, padx=5, pady=5)
            j[2].grid(row=i, column=2, padx=5, pady=5)
            j[3].grid(row=i, column=3, padx=5, pady=5)

    def _configure_weekly_chore_window(self):
        # Weekly
        for chore in self.chores["weekly"]:
            if not self.chores["weekly"][chore]["complete"]:
                # Label
                lbl = Label(self.weekly_chore_frame, text=chore, font=font + "12", bg="#FDD0CC")

                # Option Menu - complete by
                var = StringVar(self)
                var.set("Select")
                person_om = OptionMenu(self.weekly_chore_frame, var, *["Cody", "Sam"])
                person_om.config(width=15, bg=bg_color)

                # Option Menu - complete
                var = StringVar(self)
                var.set("Not Complete")
                complete_om = OptionMenu(self.weekly_chore_frame, var, *["Complete", "Not Complete"])
                complete_om.config(width=15, bg=bg_color)

                # Remove W. Chore Btn
                rmv_btn = Button(self.weekly_chore_frame, bg=bg_color, relief=FLAT, command=btn_pushed, text="-", width=10)

                self.weekly_chores.append([lbl, person_om, complete_om, rmv_btn])

        for i, j in enumerate(self.weekly_chores, 1):
            j[0].grid(row=i, column=0, padx=5, pady=5)
            j[1].grid(row=i, column=1, padx=5, pady=5)
            j[2].grid(row=i, column=2, padx=5, pady=5)
            j[3].grid(row=i, column=3, padx=5, pady=5)

    def _configure_monthly_chore_window(self):
        # Monthly
        for chore in self.chores["monthly"]:
            if not self.chores["monthly"][chore]["complete"]:
                # Label
                lbl = Label(self.monthly_chore_frame, text=chore, font=font + "12", bg="#FDD0CC")

                # Option Menu - complete by
                var = StringVar(self)
                var.set("Select")
                person_om = OptionMenu(self.monthly_chore_frame, var, *["Cody", "Sam"])
                person_om.config(width=15, bg=bg_color)

                # Option Menu - complete
                var = StringVar(self)
                var.set("Not Complete")
                complete_om = OptionMenu(self.monthly_chore_frame, var, *["Complete", "Not Complete"])
                complete_om.config(width=15, bg=bg_color)

                # Remove D. Chore Btn
                self.btn_photo = PhotoImage(file=image_path+"cancel_call.png")
                rmv_btn = Button(self.monthly_chore_frame, bg=bg_color, relief=FLAT, command=btn_pushed, image=self.btn_photo)

                self.monthly_chores.append([lbl, person_om, complete_om, rmv_btn])

            for i, j in enumerate(self.monthly_chores, 1):
                j[0].grid(row=i, column=0, padx=5, pady=5)
                j[1].grid(row=i, column=1, padx=5, pady=5)
                j[2].grid(row=i, column=2, padx=5, pady=5)
                j[3].grid(row=i, column=3, padx=5, pady=5)

    @staticmethod
    def _configure_rows_cols(master):
        """ Configure rows and columns to 1:1 weight """
        for i in range(master.grid_size()[1]):
            master.rowconfigure(i, weight=1)
        for i in range(master.grid_size()[0]):
            master.columnconfigure(i, weight=1)

    """ ______________________________________Button Functions ________________________________________________"""


def btn_pushed():
    print("Button Pushed!")


if __name__ == '__main__':
    x = TKChores().mainloop()
