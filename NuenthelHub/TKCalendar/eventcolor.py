from tkinter import Button
from typing import List


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
    cody_work = "#F7D8BA"
    sam_work = "#FEF8DD"
    both_work = "#C6B6D6"
    other = "#ACDDDE"

    """ Configures TK Calendar buttons to display colors based on specific criteria """
    def colorize(self, button: Button, categories: List[str]):
        if "c-work" in categories and "s-work" in categories:
            button.configure(bg=self.both_work)
            return

        if "c-work" in categories:
            button.configure(bg=self.cody_work)
            return

        if "s-work" in categories:
            button.configure(bg=self.sam_work)
            return

        if categories:
            button.configure(bg=self.other)
            return
