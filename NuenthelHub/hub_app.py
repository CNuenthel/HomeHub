from tkinter import Tk, PhotoImage
from tkinter.ttk import Label, Frame, Style, Button
from PIL import ImageTk, Image
from TKCalendar.tkcalendar import TKCalendar

class NuenthelHub(Tk):
    def __init__(self):
        super().__init__()
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.title("Nuenthel Hub")
        self.style = Style()
        self.style.theme_use("xpnative")
        self.attributes("-fullscreen", True)

        """Window Frames"""
        self.calendar_frame_widget = None

        """Internal Functions"""
        self._main_frame()
        self._wallpaper()
        self._calendar()

    def _main_frame(self):
        self.main_frame = Frame(self)
        self.main_frame.grid(row=0, column=0)

    def _wallpaper(self):
        raw_image = Image.open("photos/mountain_bg.png", )
        image = raw_image.resize((self.winfo_screenwidth(), self.winfo_screenheight()))
        self.background_image = ImageTk.PhotoImage(image)
        self.background_label = Label(self.main_frame, image=self.background_image)
        self.background_label.grid(row=0, column=0)

    def _calendar(self):
        self.calendar_frame = Frame(self.main_frame)
        self.calendar_frame.grid(row=0, column=0, padx=15, pady=15)

        self.style.configure("TButton", bg="green")
        self.calendar_btn = Button(self.calendar_frame, text="Calendar", command=self._open_calendar)
        self.calendar_btn.grid(row=0, column=0)

# ___________________________ Button Functions _____________________________________________

    def _open_calendar(self):
        if self.calendar_frame_widget:
            self.calendar_frame_widget.destroy()
            return

        tkc = TKCalendar(self.calendar_frame)
        tkc.grid(row=0, column=0)


if __name__ == '__main__':
    NuenthelHub().mainloop()
