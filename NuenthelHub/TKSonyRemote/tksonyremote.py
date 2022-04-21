from tkinter import Tk, IntVar, PhotoImage, NSEW
from tkinter import Button as tkButton
from tkinter.ttk import Frame, Scale, Style, Labelframe, Label
from tkinter.ttk import Button as ttkButton
from TKSonyRemote.livingroomtv import livRmRc
from TKSonyRemote.img.imagepath import image_path

bg_color = "#909090"
font = "Roboto "
header_color = "#232323"
subtle_red = "#FDD0CC"
subtle_green = "#ccfdcc"

apps = ["Disney+", "Hulu", "Netflix", "Youtube", "Twitch", "", "", "", "", ""]


class TKSonyRemote(Frame):
    def __init__(self, root: Tk or Frame):
        super().__init__()
        self.master = root
        self.volume = IntVar()
        self.remote = livRmRc
        self.app_images = []

        """Styling"""
        self.style = Style(self)
        self.style.theme_use("default")
        self.style.configure("TScale", background="#6c8a9e", foreground="white")
        self.style.configure("Hdr.TFrame", background=header_color)
        self.style.configure("App.TFrame", background=bg_color)

        """Internal Functions"""
        self._create_header()
        self._create_power_button()
        self._create_volume_scale()
        self._create_app_buttons()
        self._create_nav_control()
        self.configure_power_button()
        self._configure_rows_columns(self)

    def _create_header(self):
        header_frame = Frame(self, style="Hdr.TFrame")
        header_frame.grid(row=0, column=0, columnspan=2, sticky=NSEW)
        Label(header_frame, text="TV", background=header_color, font=font+"20", foreground="white").pack(pady=10)

    def _create_power_button(self):
        """Creates a power button"""
        self.btn_img = PhotoImage(file=image_path+"power_btn.png")
        self.power_btn = ttkButton(self, command=self.toggle_power, style="Pwr.TButton", text="Power", image=self.btn_img)
        self.power_btn.grid(row=1, column=0, padx=10, pady=10, sticky=NSEW)

    def _create_volume_scale(self):
        """Creates a scale widget on main canvas"""
        self.volume_frame = Labelframe(self, text="Volume")
        self.volume_frame.grid(row=2, column=0, padx=10, pady=10, sticky=NSEW)

        self.volume_control = Scale(self.volume_frame, command=self.volume_scalar, to=0, from_=50, length=300, orient="vertical")
        current_vol = self.remote.get_current_volume()

        if not current_vol:
            self.volume_control.configure(state="disabled")
        else:
            self.volume_control.set(self.remote.get_current_volume())

        self.volume_control.pack(padx=10, pady=10)

    def _create_app_buttons(self):
        """Creates buttons for apps listed """
        self.app_frame = Frame(self, style="App.TFrame")
        self.app_frame.grid(row=2, column=1, padx=10, pady=10)

        """Create two columns of 5 buttons, splitting apps evenly"""
        for i, app in enumerate(apps[len(apps)//2:]):
            if not app:
                tkButton(self.app_frame, text=app, state="disabled", bg="gray", height=4, width=10).grid(row=i, column=1, sticky=NSEW)
            else:
                image = PhotoImage(file=image_path + f"{app}.png")
                self.app_images.append(image)  # Prevents Garbo Collector from taking iterated images
                btn = tkButton(self.app_frame, image=image, height=4, width=10)
                btn.grid(row=i, column=1, sticky=NSEW)

        for i, app in enumerate(apps[:len(apps)//2]):
            if not app:
                tkButton(self.app_frame, state="disabled", bg="gray").grid(row=i, column=1, sticky=NSEW)
            else:
                image = PhotoImage(file=image_path + f"{app}.png")
                self.app_images.append(image)  # Prevents Garbo Collector from taking iterated images
                btn = tkButton(self.app_frame, image=image, height=4, width=10)
                btn.grid(row=i, column=1, sticky=NSEW)

    def _create_nav_control(self):
        """Creates navigation buttons"""
        self.nav_frame = Frame(self, style="Nav.TFrame")
        self.nav_frame.grid(row=1, column=1, sticky=NSEW, padx=10, pady=10)

        image = PhotoImage(file=image_path+"left.png")
        self.app_images.append(image)  # Prevents Garbo Collector from taking iterated images
        self.left_nav = ttkButton(self.nav_frame, image=image)
        self.left_nav.grid(row=1, column=0, sticky=NSEW)

        image = PhotoImage(file=image_path + "right.png")
        self.app_images.append(image)  # Prevents Garbo Collector from taking iterated images
        self.right_nav = ttkButton(self.nav_frame, image=image)
        self.right_nav.grid(row=1, column=2, sticky=NSEW)

        image = PhotoImage(file=image_path + "up.png")
        self.app_images.append(image)  # Prevents Garbo Collector from taking iterated images
        self.up_nav = ttkButton(self.nav_frame, image=image)
        self.up_nav.grid(row=0, column=1, sticky=NSEW)

        image = PhotoImage(file=image_path + "down.png")
        self.app_images.append(image)  # Prevents Garbo Collector from taking iterated images
        self.down_nav = ttkButton(self.nav_frame, image=image)
        self.down_nav.grid(row=2, column=1, sticky=NSEW)

        image = PhotoImage(file=image_path + "confirm.png")
        self.app_images.append(image)  # Prevents Garbo Collector from taking iterated images
        self.confirm_nav = ttkButton(self.nav_frame, image=image)
        self.confirm_nav.grid(row=1, column=1, sticky=NSEW)

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

# """ ____________ Widget Functions _________________________________________________________________________________"""
    def volume_scalar(self, vol):
        """Sets TV Volume to vol integer"""
        vol = round(float(vol))
        self.remote.set_volume(vol)

    def toggle_power(self):
        """Toggles TV to opposite power status, configures power button to show new status"""
        status = self.remote.get_power_status()
        self.remote.toggle_power()
        if status == "active":
            self.style.configure("Pwr.TButton", background="red")
            self.volume_control.configure(state="disabled")
            return

        self.style.configure("Pwr.TButton", background="green")
        self.volume_control.configure(state="enabled")


def btn_pushed():
    print("Button Pushed")


if __name__ == '__main__':
    x = Tk()
    x.columnconfigure(0, weight=1)
    x.rowconfigure(0, weight=1)
    TKSonyRemote(x).grid(row=0, column=0, sticky=NSEW)
    x.mainloop()