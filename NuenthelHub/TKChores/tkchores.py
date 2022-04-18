from functools import partial
from tkinter import Tk, FLAT, NSEW, GROOVE, StringVar, PhotoImage, DISABLED, ACTIVE, W, E, OptionMenu
from tkinter.ttk import Frame, Style, OptionMenu, Label, Button

from NuenthelHub.TKChores.chorehandler import ChoreHandler
from NuenthelHub.TKChores.chores.choredbcontroller import ChoreController
from NuenthelHub.TKChores.img.image_path import image_path
from NuenthelHub.TKChores.tkwindowextensions.tk_add_chore import TKAddChoreExtension
from NuenthelHub.supportmodules.modifiedwidgets import HoverButton

bg_color = "#909090"
border_color = "#9594B7"
font = "Roboto "
header_color = "#232323"
subtle_red = "#FDD0CC"
subtle_green = "#ccfdcc"


class TKChores(Frame):
    """ TKinter household chores manager """

    def __init__(self, root: Tk or Frame, callback: callable = None):
        super().__init__()

        """ Window Attributes """
        self.master = root
        self.callback = callback
        self.columns = 4
        self.sticky = NSEW
        self.daily_chores = []
        self.weekly_chores = []
        self.monthly_chores = []
        self.extension = None
        self.confirmation = None
        self.rmv_chore_img = PhotoImage(file=image_path + "remove_chore.png")
        self.daily_count = 0
        self.weekly_count = 0
        self.monthly_count = 0

        """ Styling """
        self.style = Style(self)
        self.style.theme_use("clam")
        # Frames
        self.style.configure("Header.TFrame", background=header_color)
        self.style.configure("Border.TFrame", background=border_color)
        self.style.configure("BG.TFrame", background=bg_color)
        self.style.configure("AddCancel.TFrame", background="#BDC1BE")
        # Labels
        self.style.configure("Header.TLabel", background=header_color, foreground="white")
        self.style.configure("BG.TLabel", background=bg_color)
        self.style.configure("Red.TLabel", background=subtle_red)
        self.style.configure("Grn.TLabel", background=subtle_green)
        # OptionMenu
        self.style.configure("Person.TOptionMenu", width=15, bg=bg_color, highlightthickness=0, relief=GROOVE)
        # Buttons
        self.style.configure("Green.TButton", highlightcolor=subtle_green, relief=GROOVE, width=15, background=bg_color,
                             state=DISABLED)
        self.style.configure("Rmv.TButton", background=bg_color, relief=FLAT)
        """ Supporting Classes"""
        self.ch = ChoreHandler()

        """ Internal Functions """
        self._make_main_frame()
        self._make_header()
        self._make_daily_chore_window()
        self._make_weekly_chore_window()
        self._make_monthly_chore_window()
        self._make_box_headers()

        """ Configure Functions """
        self._configure_rows_cols(self)
        self._configure_daily_chores()
        self._configure_weekly_chores()
        self._configure_monthly_chores()

    def _make_main_frame(self):
        self.mf = Frame(self.master)
        self.mf.pack()

    def _make_header(self):
        """ Creates dark background header """
        self.header_frame = Frame(self.mf, style="Header.TFrame", relief=FLAT)
        self.header_frame.grid(row=0, column=0, columnspan=10, sticky=NSEW)
        self.header_label = Label(self.header_frame, style="Header.TLabel", text="Chores",
                                  font=font + "25 underline")
        self.header_label.grid(row=0, column=0, columnspan=1, padx=15)

        self.add_chore_btn = HoverButton(self.mf, text="Add Chore", command=self._add_chore, relief=GROOVE,
                                         bg=header_color, fg="white")
        self.add_chore_btn.grid(row=0, column=6, padx=15, sticky=E)

        self._configure_rows_cols(self.header_frame)

    def _make_box_headers(self):
        Label(self.daily_chore_frame, text="Daily", font=font + "15 bold", style="BG.TLabel", anchor=W).grid(row=0,
                                                                                                             column=0)
        Label(self.weekly_chore_frame, text="Weekly", font=font + "15 bold", style="BG.TLabel", anchor=W).grid(row=0,
                                                                                                               column=0)
        Label(
            self.monthly_chore_frame, text="Monthly", font=font + "15 bold", style="BG.TLabel", anchor=W)\
            .grid(row=0, column=0)

    def _make_daily_chore_window(self):
        """ Makes first chore frame for daily chore information """

        self.daily_border = Frame(self.mf, style="Border.TFrame", borderwidth=3, relief=GROOVE)
        self.daily_border.grid(row=1, column=0, columnspan=3, sticky=NSEW, padx=5, pady=5)

        self.daily_chore_frame = Frame(self.daily_border, style="BG.TFrame", borderwidth=3, relief=GROOVE)
        self.daily_chore_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=5, ipadx=10, ipady=10,
                                    sticky=NSEW)

        self._configure_rows_cols(self.daily_border)
        self._configure_rows_cols(self.daily_chore_frame)

    def _configure_daily_chores(self):
        dailies = self.ch.get_dailies()
        if dailies:
            for i, chore in enumerate(dailies):
                self.daily_count += 1

                # Labels
                lbl = Label(self.daily_chore_frame, text=chore["name"], font=font + "12", style="Red.TLabel",
                            relief=GROOVE,
                            width=15)

                # Option Menu - complete by
                var1 = StringVar(self)
                var1.set("Select")
                person_om = OptionMenu(self.daily_chore_frame, var1, *["Select", "Cody", "Sam"],
                                       command=partial(self._open_daily_chores_om, i))

                # Button - complete
                complete_btn = Button(self.daily_chore_frame, text="Complete", style="Green.TButton",
                                      command=partial(self._complete_daily_chore, i))

                # Remove D. Chore Btn
                rmv_btn = Button(self.daily_chore_frame, style="Rmv.TButton",
                                 command=partial(self._remove_daily_chore, i),
                                 image=self.rmv_chore_img)
                self.daily_chores.append([lbl, person_om, complete_btn, rmv_btn, var1])

            for i, widget in enumerate(self.daily_chores, 1):
                widget[0].grid(row=i, column=0, padx=3)
                widget[1].grid(row=i, column=1, padx=3)
                widget[2].grid(row=i, column=2, padx=3)
                widget[3].grid(row=i, column=3, padx=3)
        else:
            Label(self.daily_chore_frame, text="All Complete", font=font + "12", style="Grn.TLabel",
                  relief=GROOVE).grid(
                row=2, column=0, pady=5)

    def _make_weekly_chore_window(self):
        """ Makes second chore frame for weekly chore information """
        self.weekly_border = Frame(self.mf, style="Border.TFrame", borderwidth=3, relief=GROOVE)
        self.weekly_border.grid(row=1, column=4, columnspan=3, sticky=NSEW, padx=5, pady=5)
        self.weekly_chore_frame = Frame(self.weekly_border, style="BG.TFrame", borderwidth=3, relief=GROOVE)
        self.weekly_chore_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=5, ipadx=10, ipady=10,
                                     sticky=NSEW)

        self._configure_rows_cols(self.weekly_border)
        self._configure_rows_cols(self.weekly_chore_frame)

    def _configure_weekly_chores(self):
        weeklies = self.ch.select_weekly_chores()
        if weeklies:
            for i, chore in enumerate(weeklies):
                self.weekly_count += 1

                # Label
                lbl = Label(self.weekly_chore_frame, text=chore["name"], font=font + "12", style="Red.TLabel",
                            relief=GROOVE,
                            width=15)

                # Option Menu - complete by
                var1 = StringVar(self)
                var1.set("Select")
                person_om = OptionMenu(self.weekly_chore_frame, var1, *["Select", "Cody", "Sam"],
                                       command=partial(self._open_weekly_chores_om, i))

                # Button - complete
                complete_btn = Button(self.weekly_chore_frame, style="Green.TButton", text="Complete",
                                      command=partial(self._complete_weekly_chore, i))

                # Remove W. Chore Btn
                rmv_btn = Button(self.weekly_chore_frame, style="Rmv.TButton",
                                 command=partial(self._remove_weekly_chore, i),
                                 image=self.rmv_chore_img)

                self.weekly_chores.append([lbl, person_om, complete_btn, rmv_btn, var1])

            for i, widget in enumerate(self.weekly_chores, 1):
                widget[0].grid(row=i, column=0, padx=3, pady=5)
                widget[1].grid(row=i, column=1, padx=3, pady=5)
                widget[2].grid(row=i, column=2, padx=3, pady=5)
                widget[3].grid(row=i, column=3, padx=3, pady=5)
        else:
            Label(self.weekly_chore_frame, text="All Complete", font=font + "12", style="Grn.TLabel",
                  relief=GROOVE).grid(
                row=2, column=0, pady=5)

    def _make_monthly_chore_window(self):
        """ Makes third chore frame for monthly chore information """
        self.monthly_border = Frame(self.mf, style="Border.TFrame", borderwidth=3, relief=GROOVE)
        self.monthly_border.grid(row=1, column=7, columnspan=3, sticky=NSEW, padx=5, pady=5)
        self.monthly_chore_frame = Frame(self.monthly_border, style="BG.TFrame", borderwidth=3, relief=GROOVE)
        self.monthly_chore_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=5, ipadx=10, ipady=10,
                                      sticky=NSEW)

        self._configure_rows_cols(self.monthly_border)
        self._configure_rows_cols(self.monthly_chore_frame)

    def _configure_monthly_chores(self):
        monthlies = self.ch.select_monthly_chores()
        if monthlies:
            for i, chore in enumerate(monthlies):
                self.monthly_count += 1

                # Label
                lbl = Label(self.monthly_chore_frame, text=chore["name"], font=font + "12", style="Red.TLabel",
                            relief=GROOVE, width=15)

                # Option Menu - complete by
                var1 = StringVar(self)
                var1.set("Select")
                person_om = OptionMenu(self.monthly_chore_frame, var1, *["Select", "Cody", "Sam"],
                                       command=partial(self._open_monthly_chores_om, i))

                # Button - complete
                complete_btn = Button(self.monthly_chore_frame, text="Complete", style="Green.TButton",
                                      command=partial(self._complete_monthly_chore, i))

                # Remove D. Chore Btn
                rmv_btn = Button(self.monthly_chore_frame, style="Rmv.TButton",
                                 command=partial(self._remove_monthly_chore, i),
                                 image=self.rmv_chore_img)

                self.monthly_chores.append([lbl, person_om, complete_btn, rmv_btn, var1])

            for i, widget in enumerate(self.monthly_chores, 1):
                widget[0].grid(row=i, column=0, padx=3)
                widget[1].grid(row=i, column=1, padx=3)
                widget[2].grid(row=i, column=2, padx=3)
                widget[3].grid(row=i, column=3, padx=3)
        else:
            Label(self.monthly_chore_frame, text="All Complete", font=font + "12", style="Grn.TLabel",
                  relief=GROOVE).grid(
                row=2, column=0, pady=5)

    @staticmethod
    def _configure_rows_cols(master):
        """ Configure rows and columns to 1:1 weight """
        for i in range(master.grid_size()[1]):
            master.rowconfigure(i, weight=1)
        for i in range(master.grid_size()[0]):
            master.columnconfigure(i, weight=1)

    """ ______________________________________Button Functions ________________________________________________"""

    def _open_daily_chores_om(self, *args):
        if args[1] == "Select":
            self.daily_chores[args[0]][2].configure(state=DISABLED)
            return
        self.daily_chores[args[0]][2].configure(state=ACTIVE)

    def _complete_daily_chore(self, *args):
        completed_by = self.daily_chores[args[0]][-1].get()
        title = self.daily_chores[args[0]][0]["text"]
        chore_id = ChoreController.find_by_element("name", title)[0].doc_id
        ChoreController.update_doc_element("complete", True, chore_id)

        self.daily_chores[args[0]][0].configure(style="Grn.TLabel")

        for widget in self.daily_chores[args[0]][1:-1]:
            widget.configure(state=DISABLED)
        self.daily_count -= 1

        print(completed_by)

    def _open_weekly_chores_om(self, *args):
        if args[1] == "Select":
            self.weekly_chores[args[0]][2].configure(state=DISABLED)
            return
        self.weekly_chores[args[0]][2].configure(state=ACTIVE)

    def _complete_weekly_chore(self, *args):
        completed_by = self.weekly_chores[args[0]][-1].get()
        title = self.weekly_chores[args[0]][0]["text"]
        chore_id = ChoreController.find_by_element("name", title)[0].doc_id
        ChoreController.update_doc_element("complete", True, chore_id)

        self.weekly_chores[args[0]][0].configure(style="Grn.TLabel")

        for widget in self.weekly_chores[args[0]][1:-1]:
            widget.configure(state=DISABLED)
        self.weekly_count -= 1
        print(completed_by)

    def _open_monthly_chores_om(self, *args):
        if args[1] == "Select":
            self.monthly_chores[args[0]][2].configure(state=DISABLED)
            return
        self.monthly_chores[args[0]][2].configure(state=ACTIVE)

    def _complete_monthly_chore(self, *args):
        completed_by = self.monthly_chores[args[0]][-1].get()
        title = self.monthly_chores[args[0]][0]["text"]
        chore_id = ChoreController.find_by_element("name", title)[0].doc_id
        ChoreController.update_doc_element("complete", True, chore_id)

        self.monthly_chores[args[0]][0].configure(style="Grn.TLabel")

        for widget in self.monthly_chores[args[0]][1:-1]:
            widget.configure(state=DISABLED)
        self.monthly_count -= 1
        print(completed_by)

    def _add_chore(self):
        print(self.extension)
        if not self.extension:
            self.confirmation.destroy() if self.confirmation else None
            self.extension = TKAddChoreExtension(self.mf, self)

    def _remove_daily_chore(self, *args):
        title = self.daily_chores[args[0]][0]["text"]
        chore_id = ChoreController.find_by_element("name", title)[0].doc_id
        if ChoreController.remove_doc(chore_id):
            print("Chore removed")
        for widget in self.daily_chores[args[0]][:-1]:
            widget.destroy()

    def _remove_weekly_chore(self, *args):
        title = self.weekly_chores[args[0]][0]["text"]
        chore_id = ChoreController.find_by_element("name", title)[0].doc_id
        ChoreController.remove_doc(chore_id)
        for widget in self.weekly_chores[args[0]][:-1]:
            widget.destroy()

    def _remove_monthly_chore(self, *args):
        title = self.monthly_chores[args[0]][0]["text"]
        chore_id = ChoreController.find_by_element("name", title)[0].doc_id
        ChoreController.remove_doc(chore_id)
        for widget in self.monthly_chores[args[0]][:-1]:
            widget.destroy()


if __name__ == '__main__':
    x = Tk()
    frm = Frame(x)
    frm.pack()
    cal = TKChores(frm)
    cal.pack()
    x.mainloop()
