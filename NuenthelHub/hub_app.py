from tkinter import Tk, Canvas
from tkinter.ttk import Label, Frame, Style, Scrollbar
from PIL import ImageTk, Image
from TKCalendar.tkcalendar import TKCalendar
from TKBudget.tkbudget import TKBudget
from TKChores.tkchores import TKChores


class NuenthelHub(Tk):
    def __init__(self):
        super().__init__()
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.title("Nuenthel Hub")
        self.style = Style()
        self.style.theme_use("xpnative")
        self.resizable(True, True)
        # self.attributes("-fullscreen", True)

        """ Styling """


        """Window Frames"""
        self.calendar_frame_widget = None

        """Internal Functions"""
        self._main_frame()
        self._wallpaper()
        self._create_scrollable_window()
        # self._calendar()
        # self._budget()
        # self._chores()

    def _main_frame(self):
        self.main_frame = Frame(self)
        self.main_frame.grid(row=0, column=0)

    def _wallpaper(self):
        raw_image = Image.open("photos/mountain_bg.png")
        image = raw_image.resize((self.winfo_screenwidth(), self.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(image)
        self.background_label = Label(self.main_frame, image=self.background_image)
        self.background_label.grid(row=0, column=0, rowspan=1000, columnspan=1000)

    def _create_scrollable_window(self):
        container = Frame(self)
        canvas = Canvas(container)
        scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        cal_frame = TKCalendar(scrollable_frame)
        cal_frame.grid(row=0, column=0)

        container.grid(row=0, column=0)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _calendar(self):
        self.calendar_frame = Frame(self.main_frame, style="CalMain.TFrame")
        self.calendar_frame.grid(row=0, column=0, padx=20, pady=20)

        self.tkc = TKCalendar(self.calendar_frame)

    def _budget(self):
        self.budget_frame = Frame(self.main_frame)
        self.budget_frame.grid(row=0, column=1, padx=20, pady=20)

        self.budg = TKBudget(self.budget_frame)

    def _chores(self):
        self.chores_frame = Frame(self.main_frame)
        self.chores_frame.grid(row=1, column=0, padx=10, pady=20)

        self.chor = TKChores(self.chores_frame)

# ___________________________ Button Functions _____________________________________________




if __name__ == '__main__':
    NuenthelHub().mainloop()
