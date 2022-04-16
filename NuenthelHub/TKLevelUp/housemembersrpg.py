from tkinter import Tk, GROOVE, NSEW
from tkinter.ttk import Button, Progressbar, Frame, Style, Label, LabelFrame
from NuenthelHub.TKLevelUp.members.memberdbcontroller import MemberController
from NuenthelHub.TKLevelUp.tkwindowextensions.tk_add_member import TKAddMemberExtension

bg_color = "#909090"
border_color = "#9594B7"
font = "Roboto "
header_color = "#232323"
subtle_red = "#FDD0CC"
subtle_green = "#ccfdcc"


class HouseMemberRpg(Tk):
    def __init__(self):
        super().__init__()

        """ Member DB """
        self.db = MemberController
        self.extension = None
        self.confirmation = None

        """ TTK Configurations """
        self.style = Style()
        self.style.theme_use("xpnative")

        """ Internal Functions """
        self._make_progress_bar()

    def _make_progress_bar(self):
        """ Creates progress bars for all members """
        members = self.db.find_all()

        s = Style()
        s.configure("TLabelFrame", font=font+"20")
        self.pb_frame = LabelFrame(self, text="Cody")
        self.pb_frame.grid(row=1, column=0)

        s = Style()
        s.configure("TProgressbar", background="green", )
        pb = Progressbar(self.pb_frame, orient="vertical", length=200, mode="determinate")

        def progress():
            if pb['value'] < 100:
                pb['value'] += 20

        self.btn = Button(self.pb_frame, text="Progress", command=progress)
        self.btn.grid(row=1, column=0, padx=10, pady=10)

        pb.grid(row=0, column=0, padx=25, pady=10)

if __name__ == '__main__':
    x = HouseMemberRpg().mainloop()









