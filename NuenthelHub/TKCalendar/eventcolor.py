from tkinter.ttk import Button, Style
from typing import List
from tkinter import SUNKEN


class EventColor:
    """
    Colors a TK button widget background to a specific color based on color criteria

    Attributes: #noqa
        cody_work:
            hexadecimal color to display if 'c-work' category is present
        sam_work:
            hexadecimal color to display if 's-work' category is present
        both_work:
            hexadecimal color to display if 'c-work' and 's-work' category is present
        other:
            hexadecimal color to display if any other category is present
    """
    style = Style()
    style.theme_use("vista")
    style.configure("CodyWork.TButton", background="#F7D8BA", relief=SUNKEN, height=4)
    style.configure("SamWork.TButton", background="#FEFF8DD", relief=SUNKEN, height=4)
    style.configure("BothWork.TButton", background="#C6B6D6", relief=SUNKEN, height=4)
    style.configure("Other.TButton", background="#ACDDDE", relief=SUNKEN, height=4)

    """ Configures TK Calendar buttons to display colors based on specific criteria """
    def colorize(self, button: Button, categories: List[str]):
        if "c-work" in categories and "s-work" in categories:
            button.configure(style="CodyWork.TButton")
            return

        if "c-work" in categories:
            button.configure(style="CodyWork.TButton")
            return

        if "s-work" in categories:
            button.configure(style="SamWork.TButton")
            return

        if categories:
            button.configure(style="Other.TButton")
            return
