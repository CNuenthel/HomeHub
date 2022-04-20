import matplotlib.pyplot as plt
from TKBudget.nuenthelsheetdata import NuenthelSheetsData


class ExpensePlot:
    def __init__(self):
        self.expense_data = NuenthelSheetsData("N-Fam 2022").get_expense_data()
        self.x_axis = [key[:3] for key in self.expense_data]
        self.y_axis = [int(self.expense_data[key][0]["perc"]) for key in self.expense_data]
        self.x_coords = [i for i, _ in enumerate(self.x_axis)]
        self.color_list = []
        self.figure = None

        self._set_color_list()
        self._create_figure()

    def _set_color_list(self):
        for i, j in enumerate(self.y_axis):
            if j < 50:
                self.color_list.append("green")
            elif 50 < j < 75:
                self.color_list.append("yellow")
            elif 75 < j < 90:
                self.color_list.append("orange")
            elif j > 90:
                self.color_list.append("red")

    def _create_figure(self):
        self.figure = plt.Figure(figsize=(5, 3), dpi=50)
        plt.rcParams.update({"axes.labelsize": 25})
        self.figure.add_subplot(111).bar(self.x_coords, self.y_axis, tick_label=self.x_axis,
                                         width=0.5, color=self.color_list)

    def get_plot(self):
        return self.figure

    def show_plot(self):
        self.show_plot()


