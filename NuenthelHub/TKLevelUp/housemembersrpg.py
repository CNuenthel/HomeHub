from tkinter import Tk, NSEW, BOTH
from tkinter.ttk import Style, Frame, Progressbar, LabelFrame
from NuenthelHub.TKLevelUp.member import MemberController, Member


class HomeRPG:
    def __init__(self, master: Tk or Frame, theme: str = "vista"):
        self.master = master
        self.players = {}
        self.style = Style(self.master.master)
        self.style.theme_use(theme)
        self.style.configure("RPG.Horizontal.TProgressbar", background="white")
        self.style.configure("RPG.TLabelframe", background="#F0F0F0")
        self.style.configure("RPG.TLabelframe.Label", background="#F0F0F0", font="Roboto 12")

    def get_members(self):
        for member in MemberController.find_all():
            self.players[member.name] = {"name": member.name, "xp": member.xp, "level": member.level, "id": member.id}

    def create_rpg_bars(self):
        for i, member in enumerate(self.players.keys()):
            # Create bar frame
            member_xp_frame = LabelFrame(self.master, text=f"{member} Lv.{self.players[member]['level']}", style="RPG.TLabelframe")
            member_xp_frame.grid(row=0, column=i, padx=10, pady=10, sticky=NSEW)

            # Create XP bar
            xp_bar = Progressbar(member_xp_frame, orient="horizontal", mode="determinate", style="RPG.Horizontal.TProgressbar")
            xp_bar.pack(fill=BOTH, expand=True, padx=10, pady=10)

            # Add progressbar to dict
            self.players[member]["xp_bar"] = xp_bar

    def add_xp(self, value, member: str):
        if member in self.players.keys():
            self.players[member]["xp"] += value
            if self.players[member]["xp"] >= 100:
                self.players[member]["xp"] -= 100
                self.players[member]["level"] += 1

            self.players[member]["xp_bar"]["value"] = self.players[member]["xp"]

            m = Member.create_from_dict(self.players[member])
            MemberController.update_doc(m, m.id)
            return
        raise KeyError(f"{member} not found within active players list. ")


if __name__ == '__main__':
    root = Tk()
    y = HomeRPG(root)
    y.get_members()
    y.create_rpg_bars()
    y.add_xp(20, "Sam")
    print(y.players)
    root.mainloop()
