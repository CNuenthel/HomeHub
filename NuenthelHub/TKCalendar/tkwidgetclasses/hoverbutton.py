"""
Contains the HoverButton advanced tkinter button widget which allows for color changing while
hovering the button on a GUI
"""
from tkinter import Button, Tk, Toplevel


class HoverButton(Button):
    """
    Creates a Tkinter button with hover highlighting

    Parameters:
        master:
            Root window in which button will be created
        **kw:
            Standard keyword arguments to the Tkinter button
    """
    def __init__(self, master: Tk or Toplevel, **kw):
        super().__init__(master=master, **kw)
        self.default_background = None
        self.active_bg = "#D9F1FF"
        self.default_foreground = None
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

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
            self.default_foreground = self["fg"]
            self["foreground"] = "black"

    def on_leave(self, e):
        """
        Returns default bg on mouse exit of widget

        Parameters:
            e:
                Unused, houses bind event callback
        """
        self["background"] = self.default_background
        self["fg"] = self.default_foreground
