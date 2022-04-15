import json
from tkinter import Tk, Frame, FLAT, Label, NSEW, GROOVE, OptionMenu, StringVar, PhotoImage, Button, DISABLED, SUNKEN, \
    ACTIVE
from NuenthelHub.TKChores.chores.chorespath import chores_path
from NuenthelHub.TKChores.img.image_path import image_path
from functools import partial
from time import sleep

bg_color = "#909090"
border_color = "#9594B7"
font = "Roboto "
header_color = "#232323"
subtle_red = "#FDD0CC"
subtle_green = "#ccfdcc"

with open(chores_path, "r") as f:
    chores_data = json.load(f)


class TKChores(Tk):
    """ TKinter household chores manager """

    def __init__(self):
        super().__init__()

        """ Window Attributes """
        self.configure(background=bg_color)
        self.title("Chores")
        self.chores = chores_data
        self.columns = 4
        self.daily_chores = []
        self.weekly_chores = []
        self.monthly_chores = []
        self.rmv_chore_img = PhotoImage(file=image_path + "remove_chore.png")
        self.daily_count = 0
        self.weekly_count = 0
        self.monthly_count = 0

        """ Internal Functions """
        self._make_header()
        self._make_daily_chore_window()
        self._make_weekly_chore_window()
        self._make_monthly_chore_window()

        """ Configure Functions """
        self._configure_rows_cols(self)
        # self._configure_daily_chore_window()
        # self._configure_weekly_chore_window()
        # self._configure_monthly_chore_window()

    def _make_header(self):
        """ Creates dark background header """
        self.header_frame = Frame(self, background=header_color, relief=FLAT)
        self.header_frame.grid(row=0, column=0, columnspan=3, sticky=NSEW)
        self.header_label = Label(self.header_frame, bg=header_color, fg="white", text="Chores",
                                  font=font + "25 underline")
        self.header_label.grid(row=0, column=0, columnspan=1, sticky=NSEW, padx=15)

        self.darklight_frame = Frame(self, background=header_color, relief=GROOVE)
        self.darklight_frame.grid(row=1, column=0, rowspan=1, columnspan=3, sticky=NSEW)

        self._configure_rows_cols(self.header_frame)
        self._configure_rows_cols(self.darklight_frame)

    def _make_daily_chore_window(self):
        """ Makes first chore frame for daily chore information """

        self.daily_border = Frame(self, background=border_color, borderwidth=3, relief=GROOVE)
        self.daily_border.grid(row=1, column=0, rowspan=2, columnspan=3, sticky=NSEW, padx=10, pady=10)

        self.daily_chore_frame = Frame(self.daily_border, background=bg_color, borderwidth=3, relief=GROOVE)
        self.daily_chore_frame.grid(row=0, column=0, columnspan=3, padx=5, rowspan=2, pady=5, ipadx=10, ipady=10,
                                    sticky=NSEW)

        Label(self.daily_chore_frame, text="Daily", font=font + "15 underline", bg=bg_color).grid(row=0, column=1)
        self._configure_rows_cols(self.daily_border)
        self._configure_rows_cols(self.daily_chore_frame)

        for i, chore in enumerate(self.chores["daily"]):
            if not self.chores["daily"][chore]["complete"]:
                self.daily_count += 1

                # Labels
                lbl = Label(self.daily_chore_frame, text=chore, font=font + "12", bg=subtle_red, relief=SUNKEN)

                # Option Menu - complete by
                var1 = StringVar(self)
                var1.set("Select")
                person_om = OptionMenu(self.daily_chore_frame, var1, *["Select", "Cody", "Sam"], command=partial(self.open_daily_chores_om, i))
                person_om.config(width=15, bg=bg_color)

                # Button - complete
                complete_btn = Button(self.daily_chore_frame, highlightcolor=subtle_green, text="Complete", command=partial(self.complete_daily_chore, i))
                complete_btn.config(width=15, bg=bg_color, state=DISABLED)

                # Remove D. Chore Btn
                rmv_btn = Button(self.daily_chore_frame, bg=bg_color, relief=FLAT, command=btn_pushed,
                                 image=self.rmv_chore_img)
                self.daily_chores.append([lbl, person_om, complete_btn, rmv_btn, var1])

        for i, j in enumerate(self.daily_chores, 1):
            j[0].grid(row=i, column=0, padx=3, pady=5)
            j[1].grid(row=i, column=1, padx=3, pady=5)
            j[2].grid(row=i, column=2, padx=3, pady=5)
            j[3].grid(row=i, column=3, padx=3, pady=5)

    def _make_weekly_chore_window(self):
        """ Makes second chore frame for weekly chore information """
        self.weekly_border = Frame(self, background=border_color, borderwidth=3, relief=GROOVE)
        self.weekly_border.grid(row=3, column=0, columnspan=3, sticky=NSEW, padx=10, pady=10)
        self.weekly_chore_frame = Frame(self.weekly_border, background=bg_color, borderwidth=3, relief=GROOVE)
        self.weekly_chore_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=5, ipadx=10, ipady=10,
                                     sticky=NSEW)

        Label(self.weekly_chore_frame, text="Weekly", font=font + "15 underline", bg=bg_color).grid(row=0, column=1)
        self._configure_rows_cols(self.weekly_border)
        self._configure_rows_cols(self.weekly_chore_frame)

        for i, chore in enumerate(self.chores["weekly"]):
            if not self.chores["weekly"][chore]["complete"]:
                self.weekly_count += 1

                # Label
                lbl = Label(self.weekly_chore_frame, text=chore, font=font + "12", bg=subtle_red, relief=SUNKEN)

                # Option Menu - complete by
                var1 = StringVar(self)
                var1.set("Select")
                person_om = OptionMenu(self.weekly_chore_frame, var1, *["Select", "Cody", "Sam"], command=partial(self.open_weekly_chores_om, i))
                person_om.config(width=15, bg=bg_color)

                # Button - complete
                complete_btn = Button(self.weekly_chore_frame, highlightcolor=subtle_green, text="Complete", command=partial(self.complete_weekly_chore, i))
                complete_btn.config(width=15, bg=bg_color, state=DISABLED)

                # Remove W. Chore Btn
                rmv_btn = Button(self.weekly_chore_frame, bg=bg_color, relief=FLAT, command=btn_pushed,
                                 image=self.rmv_chore_img)

                self.weekly_chores.append([lbl, person_om, complete_btn, rmv_btn, var1])

        for i, j in enumerate(self.weekly_chores, 1):
            j[0].grid(row=i, column=0, padx=3, pady=5)
            j[1].grid(row=i, column=1, padx=3, pady=5)
            j[2].grid(row=i, column=2, padx=3, pady=5)
            j[3].grid(row=i, column=3, padx=3, pady=5)

    def _make_monthly_chore_window(self):
        """ Makes third chore frame for monthly chore information """
        self.monthly_border = Frame(self, background=border_color, borderwidth=3, relief=GROOVE)
        self.monthly_border.grid(row=4, column=0, columnspan=3, sticky=NSEW, padx=10, pady=10)
        self.monthly_chore_frame = Frame(self.monthly_border, background=bg_color, borderwidth=3, relief=GROOVE)
        self.monthly_chore_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=5, ipadx=10, ipady=10,
                                      sticky=NSEW)

        Label(self.monthly_chore_frame, text="Monthly", font=font + "15 underline", bg=bg_color).grid(row=0, column=1)
        self._configure_rows_cols(self.monthly_border)
        self._configure_rows_cols(self.monthly_chore_frame)

        for i, chore in enumerate(self.chores["monthly"]):
            if not self.chores["monthly"][chore]["complete"]:
                self.monthly_count += 1

                # Label
                lbl = Label(self.monthly_chore_frame, text=chore, font=font + "12", bg=subtle_red, relief=SUNKEN)

                # Option Menu - complete by
                var1 = StringVar(self)
                var1.set("Select")
                person_om = OptionMenu(self.monthly_chore_frame, var1, *["Select", "Cody", "Sam"], command=partial(self.open_monthly_chores_om, i))
                person_om.config(width=15, bg=bg_color)

                # Button - complete
                complete_btn = Button(self.monthly_chore_frame, highlightcolor=subtle_green, text="Complete", command=partial(self.complete_monthly_chore, i))
                complete_btn.config(width=15, bg=bg_color, state=DISABLED)

                # Remove D. Chore Btn
                rmv_btn = Button(self.monthly_chore_frame, bg=bg_color, relief=FLAT, command=btn_pushed,
                                 image=self.rmv_chore_img)

                self.monthly_chores.append([lbl, person_om, complete_btn, rmv_btn, var1])

            for i, j in enumerate(self.monthly_chores, 1):
                j[0].grid(row=i, column=0, padx=3, pady=5)
                j[1].grid(row=i, column=1, padx=3, pady=5)
                j[2].grid(row=i, column=2, padx=3, pady=5)
                j[3].grid(row=i, column=3, padx=3, pady=5)

    @staticmethod
    def _configure_rows_cols(master):
        """ Configure rows and columns to 1:1 weight """
        for i in range(master.grid_size()[1]):
            master.rowconfigure(i, weight=1)
        for i in range(master.grid_size()[0]):
            master.columnconfigure(i, weight=1)

    """ ______________________________________Button Functions ________________________________________________"""

    def open_daily_chores_om(self, *args):
        if args[1] == "Select":
            self.daily_chores[args[0]][2].configure(state=DISABLED)
            return
        self.daily_chores[args[0]][2].configure(state=ACTIVE)

    def complete_daily_chore(self, *args):
        completed_by = self.daily_chores[args[0]][-1].get()
        for widget in self.daily_chores[args[0]][:-1]:
            widget.destroy()
        self.daily_count -= 1
        if not self.daily_count:
            self.daily_border.destroy()
        print(completed_by)

    def open_weekly_chores_om(self, *args):
        if args[1] == "Select":
            self.weekly_chores[args[0]][2].configure(state=DISABLED)
            return
        self.weekly_chores[args[0]][2].configure(state=ACTIVE)

    def complete_weekly_chore(self, *args):
        completed_by = self.weekly_chores[args[0]][-1].get()
        for widget in self.weekly_chores[args[0]][:-1]:
            widget.destroy()
        self.weekly_count -= 1
        if not self.weekly_count:
            self.weekly_border.destroy()
        print(completed_by)

    def open_monthly_chores_om(self, *args):
        if args[1] == "Select":
            self.monthly_chores[args[0]][2].configure(state=DISABLED)
            return
        self.monthly_chores[args[0]][2].configure(state=ACTIVE)

    def complete_monthly_chore(self, *args):
        completed_by = self.monthly_chores[args[0]][-1].get()
        for widget in self.monthly_chores[args[0]][:-1]:
            widget.destroy()
        self.monthly_count -= 1
        if not self.monthly_count:
            self.monthly_border.destroy()
        print(completed_by)


def btn_pushed(*args):
    print(args[0])
    print("Button Pushed!")
    print(f"args: {args}")


if __name__ == '__main__':
    x = TKChores().mainloop()
