"""
Module for holding graph classes for TK Budget
"""

import matplotlib.pyplot as plt


class ExpensePlot:
    """ Creates a TK usable figure from a list of expenses and budget percents """
    def __init__(self, expenses, percents, x_labels):
        self.x_axis = [label[:3] for label in x_labels]
        self.y_axis = percents
        self.x_coords = expenses
        self.color_list = []
        self.figure = None

        self._set_color_list()
        self._create_figure()

    def _set_color_list(self):
        """ Extends the color list with color strings based on percentage values """
        for i, j in enumerate(self.y_axis):
            if j < 50:
                self.color_list.append("green")
            elif 50 <= j < 75:
                self.color_list.append("yellow")
            elif 75 <= j < 90:
                self.color_list.append("orange")
            elif j >= 90:
                self.color_list.append("red")

    def _create_figure(self):
        """ Creates a figure (bar graph) """
        self.figure = plt.Figure(figsize=(5, 3), dpi=100)
        ax = plt.subplot()
        ax.set_title("Budget Consumed (%)", pad=15, weight="bold")
        self.figure.add_subplot(111).bar(self.x_coords, self.y_axis, tick_label=self.x_axis,
                                         width=0.5, color=self.color_list)

    def get_plot(self):
        return self.figure

