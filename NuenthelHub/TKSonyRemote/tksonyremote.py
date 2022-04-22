from functools import partial
from time import sleep
from tkinter import Button as tkButton
from tkinter import Tk, IntVar, PhotoImage, NSEW
from tkinter.ttk import Button as ttkButton
from tkinter.ttk import Frame, Scale, Style, Labelframe, Label

from TKSonyRemote.img.imagepath import image_path
from TKSonyRemote.livingroomtv import livRmRc

bg_color = "#909090"
font = "Roboto "
header_color = "#232323"
subtle_red = "#FDD0CC"
subtle_green = "#ccfdcc"

apps = ["Disney+", "Hulu", "Netflix", "YouTube", "Twitch", "Peacock TV", "Prime Video", "Crunchyroll", "Nest",
        "PBS KIDS"]


class TKSonyRemote(Frame):
    def __init__(self, root: Tk or Frame):
        super().__init__()
        self.master = root
        self.volume = IntVar()
        self.remote = livRmRc
        self.app_images1 = []
        self.app_images2 = []
        self.nav_images = []

        """Styling"""
        self.style = Style(self)
        self.style.theme_use("default")
        self.style.configure("TScale", background="#6c8a9e", foreground="white")
        self.style.configure("Hdr.TFrame", background=header_color)
        self.style.configure("App.TFrame", background=bg_color)
        self.style.configure("Nav.TButton", width=10, height=10)

        """Internal Functions"""
        self._create_header()
        self._create_power_button()
        self._create_volume_scale()
        self._create_app_buttons()
        self._create_nav_control()
        self._create_home_back_buttons()
        self.configure_power_button()
        self._configure_rows_columns(self)

    def _create_header(self):
        header_frame = Frame(self, style="Hdr.TFrame")
        header_frame.grid(row=0, column=0, columnspan=2, sticky=NSEW)
        Label(header_frame, text="TV", background=header_color, font=font + "20", foreground="white").pack(pady=10)

    def _create_power_button(self):
        """Creates a power button"""
        self.btn_img = PhotoImage(file=image_path + "power_btn.png")
        self.power_btn = ttkButton(self, command=self.toggle_power, style="Pwr.TButton", text="Power",
                                   image=self.btn_img)
        self.power_btn.grid(row=1, column=0, padx=10, pady=10)

    def _create_volume_scale(self):
        """Creates a scale widget on main canvas"""
        self.volume_frame = Labelframe(self, text="Volume")
        self.volume_frame.grid(row=2, column=0, padx=10, pady=10, sticky=NSEW)

        self.volume_control = Scale(self.volume_frame, command=self.volume_scalar, to=0, from_=50, length=300,
                                    orient="vertical")

        if self.remote.get_power_status() == "standby":
            self.volume_control.configure(state="disabled")
        else:
            self.volume_control.set(self.remote.get_current_volume())

        self.volume_control.pack(padx=10, pady=10)

    def _create_app_buttons(self):
        """
        Creates buttons for apps listed

        Button img names must match app names found from remote control get_apps method, as well as
        Listed app names in apps [line 15]
        """
        self.app_frame = Frame(self, style="App.TFrame")
        self.app_frame.grid(row=2, column=1, padx=10, pady=10)

        """Create two columns of 5 buttons, splitting apps evenly"""
        for i, app in enumerate(apps[len(apps) // 2:]):
            if not app:
                tkButton(self.app_frame, text=app, state="disabled", bg="gray", height=4, width=10).grid(row=i,
                                                                                                         column=1,
                                                                                                         sticky=NSEW)
            else:
                image = PhotoImage(file=image_path + f"{app}.png")
                self.app_images1.append(image)  # Prevents Garbo Collector from taking iterated images
                btn = tkButton(self.app_frame, image=image, height=60, width=100, command=partial(self.start_app, app))
                btn.grid(row=i, column=0, sticky=NSEW)

        for i, app in enumerate(apps[:len(apps) // 2]):
            if not app:
                tkButton(self.app_frame, state="disabled", bg="gray").grid(row=i, column=1, sticky=NSEW)
            else:
                image = PhotoImage(file=image_path + f"{app}.png")
                self.app_images2.append(image)  # Prevents Garbo Collector from taking iterated images
                btn = tkButton(self.app_frame, image=image, height=60, width=100, command=partial(self.start_app, app))
                btn.grid(row=i, column=1, sticky=NSEW)

    def _create_nav_control(self):
        """Creates navigation buttons"""
        self.nav_frame = Frame(self, style="Nav.TFrame")
        self.nav_frame.grid(row=1, column=1, sticky=NSEW, padx=10, pady=10)

        image = PhotoImage(file=image_path + "left.png")
        self.nav_images.append(image)  # Prevents Garbo Collector from taking iterated images
        self.left_nav = ttkButton(self.nav_frame, image=image, command=self.nav_left)
        self.left_nav.grid(row=1, column=0, sticky=NSEW, padx=10, pady=10)

        image = PhotoImage(file=image_path + "right.png")
        self.nav_images.append(image)  # Prevents Garbo Collector from taking iterated images
        self.right_nav = ttkButton(self.nav_frame, image=image, command=self.nav_right)
        self.right_nav.grid(row=1, column=2, sticky=NSEW, padx=10, pady=10)

        image = PhotoImage(file=image_path + "up.png")
        self.nav_images.append(image)  # Prevents Garbo Collector from taking iterated images
        self.up_nav = ttkButton(self.nav_frame, image=image, command=self.nav_up)
        self.up_nav.grid(row=0, column=1, sticky=NSEW, padx=10, pady=10)

        image = PhotoImage(file=image_path + "down.png")
        self.nav_images.append(image)  # Prevents Garbo Collector from taking iterated images
        self.down_nav = ttkButton(self.nav_frame, image=image, command=self.nav_down)
        self.down_nav.grid(row=2, column=1, sticky=NSEW, padx=10, pady=10)

        image = PhotoImage(file=image_path + "confirm.png")
        self.nav_images.append(image)  # Prevents Garbo Collector from taking iterated images
        self.confirm_nav = ttkButton(self.nav_frame, image=image, command=self.nav_confirm)
        self.confirm_nav.grid(row=1, column=1, sticky=NSEW, ipadx=10, ipady=10)

    def _create_home_back_buttons(self):
        image = PhotoImage(file=image_path + "home.png")
        self.nav_images.append(image)
        self.home_nav = ttkButton(self.nav_frame, image=image, command=self.nav_home, style="Nav.TButton")
        self.home_nav.grid(row=2, column=0, padx=10, pady=10)

        image = PhotoImage(file=image_path + "back.png")
        self.nav_images.append(image)
        self.back_nav = ttkButton(self.nav_frame, image=image, command=self.nav_back, style="Nav.TButton")
        self.back_nav.grid(row=2, column=2, padx=10, pady=10)

    def configure_power_button(self):
        """Configures power button"""
        if self.remote.get_power_status() == "active":
            self.style.configure("Pwr.TButton", background=subtle_green)
        else:
            self.style.configure("Pwr.TButton", background=subtle_red)

    def _configure_rows_columns(self, grid_master=None):
        """ Configures rows and columns to expand with resize of window """
        columns, rows = grid_master.grid_size()
        for columns in range(columns):
            self.columnconfigure(columns, weight=1)
        for rows in range(rows):
            self.rowconfigure(rows, weight=1)

    # """ ____________ Widget Functions _____________________________________________________________________________"""
    def volume_scalar(self, vol):
        """Sets TV Volume to vol integer"""
        vol = round(float(vol))
        self.remote.set_volume(vol)

    def toggle_power(self):
        """Toggles TV to opposite power status, configures power button to show new status"""
        self.remote.toggle_power()
        sleep(1)
        status = self.remote.get_power_status()
        if status == "active":
            self.style.configure("Pwr.TButton", background=subtle_green)
            self.volume_control.configure(state="enabled")
            return

        self.style.configure("Pwr.TButton", background=subtle_red)
        self.volume_control.configure(state="disabled")

    def start_app(self, app):
        """Starts app on TV"""
        self.remote.open_app(app)

    def nav_up(self):
        """Calls directional up command"""
        self.remote.nav_command("up")

    def nav_down(self):
        """Calls directional down command"""
        self.remote.nav_command("down")

    def nav_left(self):
        """Calls directional left command"""
        self.remote.nav_command("left")

    def nav_right(self):
        """Calls directional right command"""
        self.remote.nav_command("right")

    def nav_confirm(self):
        """Calls confirm command"""
        self.remote.nav_command("confirm")

    def nav_home(self):
        """Calls home command"""
        self.remote.nav_command("home")

    def nav_back(self):
        """Calls back command"""
        self.remote.nav_command("back")


if __name__ == '__main__':
    x = Tk()
    x.columnconfigure(0, weight=1)
    x.rowconfigure(0, weight=1)
    TKSonyRemote(x).grid(row=0, column=0, sticky=NSEW)
    x.mainloop()
