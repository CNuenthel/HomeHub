"""
Contains modified Tkinter widgets.
"""
from tkinter import Button, Tk, Toplevel, Label, Entry, END, IntVar
from tkinter.ttk import Combobox, Style, Frame, Checkbutton, Separator


class HoverButton(Button):
    """
    Creates a Tkinter button with hover highlighting

    Parameters:
        master:
            Root window in which button will be created
        **kw:
            Standard keyword arguments to the Tkinter button
    """

    def __init__(self, master: Tk or Toplevel, **kw):
        super().__init__(master=master, **kw)
        self.default_background = None
        self.active_bg = "#D9F1FF"
        self.default_foreground = None
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        """
        Sets default bg and changes bg to active color on mouse entry to widget

        Parameters:
            e:
                Unused, houses bind event callback, required positional for some reason
        """
        self.default_background = self["background"]
        if self.default_background != "#808080":  # Here we use #808080 as a standard "inactive" color
            self["background"] = self.active_bg
            self.default_foreground = self["fg"]
            self["foreground"] = "black"

    def on_leave(self, e):
        """
        Returns default bg on mouse exit of widget

        Parameters:
            e:
                Unused, houses bind event callback, required positional for some reason
        """
        self["background"] = self.default_background
        self["fg"] = self.default_foreground


class HoverLabel(Label):
    """
    Creates a Tkinter label with hover highlighting

    Parameters:
        master:
            Root window in which label will be created
        **kw:
            Standard keyword arguments to the Tkinter label
    """

    def __init__(self, master: Tk or Toplevel, **kw):
        super().__init__(master=master, **kw)
        self.default_background = None
        self.active_bg = "#D9F1FF"
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.text = ""

    def on_enter(self, e):
        """
        Sets default bg and changes bg to active color on mouse entry to widget

        Parameters:
            e:
                Unused, houses bind event callback
        """
        self.default_background = self["background"]
        if self.default_background != "#808080":  # Here we use #808080 as a standard "inactive" color
            self["background"] = self.active_bg

    def on_leave(self, e):
        """
        Returns default bg on mouse exit of widget

        Parameters:
            e:
                Unused, houses bind event callback
        """
        self["background"] = self.default_background


class SnapbackEntry(Entry):
    """
    Creates a Tkinter entry that clears on clicking, and returns to previous value on focus out
    """

    def __init__(self, master: Tk or Toplevel, **kw):
        """
        Constructs a Tkinter Entry

        Parameters:
            master: Tk or Toplevel
                Root window in which button will be created
            **kw: dict
                Standard keyword arguments to the Tkinter entry
        """
        super().__init__(master=master, **kw)
        self.current_text = None
        self.bind("<1>", self._clear_entry)
        self.bind("<FocusOut>", self._fill_entry)

    def _clear_entry(self, e):
        """ Clears all text on clicking entry, Internal Function"""
        self.current_text = self.get()
        self.delete(0, END)

    def _fill_entry(self, e):
        """ If nothing is entered in entry, reverts to previous value on focus out"""
        if self.get() == "":
            self.insert(0, self.current_text)


class NumberOnlyCombobox(Combobox):
    """
    Creates a TTK Combobox that reverts to a selected state if given non integer data.


    Parameters:
        master:
            Root window in which button will be created
        base_value:
            Original value set for combobox
        max_length:
            max length a selection or manual input can be if specified
        **kw:
            Standard keyword arguments to the TTkinter combobox

    """

    def __init__(self, master: Tk or Toplevel, base_value: str or int, max_length: int = None, **kw):
        """ Constructs a Tkinter Entry """
        super().__init__(master=master, **kw)
        self.style = Style()
        self.style.theme_use("clam")
        self.max_length = max_length
        self.base_value = base_value

        self.bind("<FocusOut>", self._check_value)

    def set_style(self, fbg: str = "white", bg: str = "white"):
        """
        Sets Combobox style to a desired field background or background

        Parameters:
            fbg:
                desired field background color, accepts hexadecimal
                default: white
            bg:
                desired widget background color, accepts hexadecimal
                default: white
        """
        self.style.configure("TCombobox", fieldbackground=fbg, background=bg)

    def _check_value(self, e):
        """
        Verifies integer value input and max length if filled

        Internal Function
        """
        try:
            int(self.get())
        except ValueError:
            self.set(self.base_value)

        if self.max_length:
            if len(self.get()) > self.max_length:
                self.set(self.base_value)


class TextFilledEntry(Entry):
    """
    Creates a Tkinter Entry that holds an inserted text until clicked
    """

    def __init__(self, master: Tk or Toplevel, insert_text: str, **kw):
        """
        Constructs a Tkinter Entry

        Parameters:
            master: Tk or Toplevel
                Root window in which button will be created
            insert_text: str
                Text to be displayed within entry
            **kw: dict
                Standard keyword arguments to the Tkinter entry
        """
        super().__init__(master=master, **kw)
        self.insert_text = insert_text
        self.bind("<1>", self._clear_entry)
        self.bind("<FocusOut>", self._fill_entry)
        self._fill_entry(None)

    def _clear_entry(self, e):
        """ Clears all text on clicking entry, Internal Function"""
        if self.get() == self.insert_text:
            self.delete(0, END)

    def _fill_entry(self, e):
        """ Fills entry with default text, Internal Function """
        if not self.get():
            self.insert(0, self.insert_text)


class CollapsiblePane(Frame):
    """
     -----USAGE-----
    collapsiblePane = CollapsiblePane(parent,
                          expanded_text =[string],
                          collapsed_text =[string])

    collapsiblePane.pack()
    button = Button(collapsiblePane.frame).pack()
    """

    def __init__(self, parent, expanded_text="Collapse <<",
                 collapsed_text="Expand >>"):

        Frame.__init__(self, parent)

        # These are the class variable
        # see a underscore in expanded_text and _collapsed_text
        # this means these are private to class
        self.parent = parent
        self._expanded_text = expanded_text
        self._collapsed_text = collapsed_text

        # Here weight implies that it can grow it's
        # size if extra space is available
        # default weight is 0
        self.columnconfigure(1, weight=1)

        # Tkinter variable storing integer value
        self._variable = IntVar()

        # Checkbutton is created but will behave as Button
        # cause in style, Button is passed
        # main reason to do this is Button do not support
        # variable option but checkbutton do
        self._button = Checkbutton(self, variable=self._variable,
                                       command=self._activate, style="TButton")
        self._button.grid(row=0, column=0)

        # This wil create a separator
        # A separator is a line, we can also set thickness
        self._separator = Separator(self, orient="horizontal")
        self._separator.grid(row=0, column=1, sticky="we")

        self.frame = Frame(self)

        # This will call activate function of class
        self._activate()

    def _activate(self):
        if not self._variable.get():

            # As soon as button is pressed it removes this widget
            # but is not destroyed means can be displayed again
            self.frame.grid_forget()

            # This will change the text of the checkbutton
            self._button.configure(text=self._collapsed_text)

        elif self._variable.get():
            # increasing the frame area so new widgets
            # could reside in this container
            self.frame.grid(row=1, column=0, columnspan=2)
            self._button.configure(text=self._expanded_text)

    def toggle(self):
        """Switches the label frame to the opposite state."""
        self._variable.set(not self._variable.get())
        self._activate()

