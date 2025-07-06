from tkinter.scrolledtext import ScrolledText
import tkinter as tk
import sys
from typing import Self


class StdRedir(object):
    def __init__(self, text_widget: ScrolledText):
        self._text_widget = text_widget

    @classmethod
    def redirect_to(cls: type[Self], text_widget: ScrolledText) -> None:
        cls.__inst = StdRedir(text_widget)
        sys.stdout = cls.__inst
        sys.stderr = cls.__inst

    def write(self, s: str):
        self._text_widget.insert(tk.END, s)
        self._text_widget.see(tk.END)

    def flush(self):
        pass  # Leave it like that
