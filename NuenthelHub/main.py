from tkinter import *

from TKBudget.tkbudget import TKBudget
from TKCalendar.tkcalendar import open_calendar

""" _____________________ Functional ________________________________________________________________________________"""


def calendar():
    open_calendar()


def budget():
    TKBudget().mainloop()


# Main Window
main = Tk()
main.geometry(f"{1720}x{968}")
main.resizable(False, False)
main.title("Nuenthel Hub")

# Get Display Specs
screen_width = main.winfo_screenwidth()
screen_height = main.winfo_screenheight()
center_set = (screen_width - 1720) // 2
vertical_set = (screen_height - 968) // 2

# Background
background_image = PhotoImage(file="Photos/family_photo.png")
background_label = Label(image=background_image)
background_label.place(
    x=0,
    y=0
)

# Buttons
button_bg = "white"
button_fg = "black"

calendar_button = Button(
    text="Calendar",
    width=15,
    height=5,
    bg=button_bg,
    fg=button_fg,
    relief=GROOVE,
    command=calendar
)
calendar_button.place(
    x=1135,
    y=200
)

budget_button = Button(
    text="Budget",
    width=15,
    height=5,
    bg=button_bg,
    fg=button_fg,
    relief=GROOVE,
    command=budget
)
budget_button.place(
    x=1260,
    y=200
)

ndhp_button = Button(
    text="Cody's Dailies",
    width=15,
    height=5,
    bg=button_bg,
    fg=button_fg,
    relief=SUNKEN
)
ndhp_button.place(
    x=1260,
    y=295
)

if __name__ == '__main__':
    main.mainloop()
