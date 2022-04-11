"""Houses TextFilledEntry Class"""
from tkinter import Entry, Tk, Toplevel, END


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

