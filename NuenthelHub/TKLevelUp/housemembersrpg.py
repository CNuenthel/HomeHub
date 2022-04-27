from tkinter import Tk, Toplevel
from tkinter.ttk import Style, Frame, Progressbar

from NuenthelHub.TKLevelUp.members.memberdbcontroller import MemberController
from TKLevelUp.members.member import Member


class HouseMemberXPBar(Progressbar):
    def __init__(self, master: Tk or Frame or Toplevel, member: Member, **kw):
        super().__init__(master=master, **kw)
        """ Frame Attributes """
        self.root = master
        self.member = member
        """ Member DB """
        self.db = MemberController

        """ TTK Configurations """
        # self.style = Style(self)
        # self.style.theme_use("xpnative")

    def add_xp(self, value, member: Member):
        self.member.xp += value

        if self.member.xp >= 100:
            member.level += 1
            member.xp -= 100
        self.db.update_doc(self.member, self.member.id)
