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
        self.style.theme_use("alt")

        """ Internal Functions """
        self._make_header()
        self._make_progress_bar()
        self._make_member_buttons()

    def _make_header(self):
        """ Creates header frame """
        self.header_frame = Frame(self)
        self.header_frame.grid(row=0, column=0, sticky=NSEW)

    def _make_progress_bar(self):
        """ Creates progress bars for all members """
        members = self.db.find_all()

        self.pb_frame = LabelFrame(self, text="Cody", labelanchor="nw", relief=GROOVE)
        self.pb_frame.grid(row=1, column=0)

        pb = Progressbar(self.pb_frame, orient="vertical", length=100, mode="determinate")
        pb.grid(row=0, column=0, padx=10, pady=10)

    def _make_member_buttons(self):
        self.member_btn_frame = LabelFrame(self, text="Member DB", relief=GROOVE)
        self.member_btn_frame.grid(row=2, column=0)

        self.add_member_btn = Button(self.member_btn_frame, text="Add Member", command=self._add_member)
        self.add_member_btn.grid(row=0, column=0)

# """ __________________Button Commands _____________________________________________________________________________"""

    def _add_member(self):
        if not self.extension:
            self.confirmation.destroy() if self.confirmation else None
            self.extension = TKAddMemberExtension(self)


if __name__ == '__main__':
    x = HouseMemberRpg().mainloop()









