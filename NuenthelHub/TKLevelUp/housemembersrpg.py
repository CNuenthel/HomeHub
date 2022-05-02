from tkinter import BOTH
from tkinter.ttk import Style, Frame, Progressbar, LabelFrame
from NuenthelHub.TKLevelUp.member import MemberController, Member


class HomeRPGPlayer:
    def __init__(self, member: Member, style: Style):
        self.name = member.name
        self.xp = member.xp
        self.level = member.level
        self.color = member.color
        self.id = member.id

        """ Widgets """
        self.xp_frame = None
        self.xp_bar = None

        """ Styling """
        self.style = style
        self.style.configure("RPG.Horizontal.TProgressbar", background="white")
        self.style.configure("RPG.TLabelframe", background="#F0F0F0")
        self.style.configure("RPG.TLabelframe.Label", background="#F0F0F0", font="Roboto 12")

    def create_xp_bar(self, master: Frame) -> LabelFrame:
        """
        Creates a tkinter widget XP bar
        -----------------
        Params:
            master: {Tk.Frame} Frame parent for the XP bar and LabelFrame

        Returns: Frame containing an XP bar
        """
        self.xp_frame = LabelFrame(master, text=f"{self.name} Lv.{self.level}", style="RPG.TLabelframe")
        self.xp_bar = Progressbar(self.xp_frame, orient="horizontal", mode="determinate",
                                  style="RPG.Horizontal.TProgressbar")
        self.xp_bar.pack(fill=BOTH, expand=True, padx=10, pady=10)
        return self.xp_frame

    def add_xp(self, value: int):
        """ Adds XP points to players progress bar """
        self.xp += value

        if self.xp >= 100:
            self.level += 1
            self.xp -= 100

        self.xp_bar["value"] = self.xp
        self._update_member_database()

    def _update_member_database(self):
        """ Updates house member database with member data """
        member_data = {
            "name": self.name,
            "xp": self.xp,
            "level": self.level,
            "color": self.color,
            "id": self.id
        }

        m = Member.create_from_dict(member_data)
        MemberController.update_doc(m, m.id)


