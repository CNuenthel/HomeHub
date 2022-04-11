"""Houses TextFilledEntry Class"""
from tkinter import Entry, Tk, Toplevel, END


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

