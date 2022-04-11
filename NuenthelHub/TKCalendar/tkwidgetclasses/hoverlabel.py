"""
Contains the HoverButton advanced tkinter label widget which allows for color changing while
hovering the label on a GUI
"""
from tkinter import Label, Tk, Toplevel


class HoverLabel(Label):
    """
    Creates a Tkinter label with hover highlighting

    Parameters:
        master:
            Root window in which label will be created
        **kw:
            Standard keyword arguments to the Tkinter label
    """
    def __init__(self, master: Tk or Toplevel, **kw):
        super().__init__(master=master, **kw)
        self.default_background = None
        self.active_bg = "#D9F1FF"
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.text = ""

    def on_enter(self, e):
        """
        Sets default bg and changes bg to active color on mouse entry to widget

        Parameters:
            e:
                Unused, houses bind event callback
        """
        self.default_background = self["background"]
        if self.default_background != "#808080":  # Here we use #808080 as a standard "inactive" color
            self["background"] = self.active_bg

    def on_leave(self, e):
        """
        Returns default bg on mouse exit of widget

        Parameters:
            e:
                Unused, houses bind event callback
        """
        self["background"] = self.default_background

