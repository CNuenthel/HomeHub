from tkinter import Tk, Toplevel, NSEW, FLAT
from tkinter.ttk import Frame, Button, Style


class TKLegend:
    """
    Creates a legend sidebar to a TK window to edit buttons based on set criteria

    Parameters:
        root_window:
            Primary TK window to extend legend to
    """
    def __init__(self, root_window: Tk or Toplevel):
        """ Extension Attributes """
        self.root = root_window
        self.grid_row_start = root_window.grid_size()[1]
        self.column_count = root_window.grid_size()[0]

        """ Internal Functions"""
        self._create_main_frame()
        self._create_legend_colors()

    def _create_main_frame(self):
        """ Create a frame for add event widgets """
        self.main_frame = Frame(self.root)
        self.main_frame.grid(row=2, column=self.column_count, rowspan=self.grid_row_start, columnspan=2, sticky=NSEW)

    def _create_legend_colors(self):
        """ Creates button representation of colors with category text """
        colors = ["#F7D8BA", "#FEF8DD", "#C6B6D6", "#ACDDDE"]
        categories = ["Cody Works", "Sam Works", "Work Overlap", "Other"]
        for i, j in enumerate(colors):
            legend_style = Style()
            legend_style.configure(f"{j}.TButton", background=j, relief=FLAT)
            Button(self.main_frame, text=categories[i], style=f"{j}.TButton").grid(row=i, column=0, sticky=NSEW, pady=25,
                                                                                padx=10)
