"""
Houses the NumberOnlyCombobox class
"""

from tkinter.ttk import Combobox, Style
from tkinter import Tk, Toplevel


class NumberOnlyCombobox(Combobox):
    """
    Creates a TTK Combobox that reverts to a selected state if given non integer data.


    Parameters:
        master:
            Root window in which button will be created
        base_value:
            Original value set for combobox
        max_length:
            max length a selection or manual input can be if specified
        **kw:
            Standard keyword arguments to the TTkinter combobox

    """

    def __init__(self, master: Tk or Toplevel, base_value: str or int, max_length: int = None, **kw):
        """ Constructs a Tkinter Entry """
        super().__init__(master=master, **kw)
        self.style = Style()
        self.style.theme_use("clam")
        self.max_length = max_length
        self.base_value = base_value

        self.bind("<FocusOut>", self._check_value)

    def set_style(self, fbg: str = "white", bg: str = "white"):
        """
        Sets Combobox style to a desired field background or background

        Parameters:
            fbg:
                desired field background color, accepts hexadecimal
                default: white
            bg:
                desired widget background color, accepts hexadecimal
                default: white
        """
        self.style.configure("TCombobox", fieldbackground=fbg, background=bg)

    def _check_value(self, e):
        """
        Verifies integer value input and max length if filled

        Internal Function
        """
        try:
            int(self.get())
        except ValueError:
            self.set(self.base_value)

        if self.max_length:
            if len(self.get()) > self.max_length:
                self.set(self.base_value)


