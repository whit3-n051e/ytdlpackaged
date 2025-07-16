from __future__ import annotations
from typing import Self
from .dwld import Downloader
from .stdredir import StdRedir
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import threading
from enum import StrEnum
from .language_data import GUI_LINES_ENGLISH, GUI_LINES_RUSSIAN


VIDEO_FORMATS = ['mp4', 'avi', 'flv', 'mkv', 'mov', 'webm']
AUDIO_FORMATS = ['mp3', 'aac', 'alac', 'flac', 'm4a', 'opus', 'vorbis', 'wav']


class Language(StrEnum):
    ENGLISH = "English"
    RUSSIAN = "Русский"

    def get_lines(self: Self) -> list[str]:
        match self:
            case self.ENGLISH: return GUI_LINES_ENGLISH
            case self.RUSSIAN: return GUI_LINES_RUSSIAN

    @classmethod
    def from_str(cls: type[Self], s: str) -> Language:
        for name in Language:
            if s == name.value:
                return name
        return cls.ENGLISH


class Gui(object):
    def __init__(self: Self) -> None:
        pass

    __audio_only: tk.BooleanVar
    __use_system_ffmpeg: tk.BooleanVar
    __language: tk.StringVar

    __root: tk.Tk
    __language_label: tk.Label
    __language_selector: tk.OptionMenu
    __input_label: tk.Label
    __dropdown_label: tk.Label
    __dropdown: ttk.Combobox
    __button: tk.Button
    __output_box: ScrolledText
    __input_box: tk.Entry
    __radio_video: tk.Radiobutton
    __radio_audio: tk.Radiobutton
    __checkbox: tk.Checkbutton

    __is_inited: bool = False

    @classmethod
    def __update_dropdown(cls: type[Self]) -> None:
        if not cls.__is_inited:
            return
        if cls.__audio_only.get():
            cls.__dropdown['values'] = AUDIO_FORMATS
            cls.__dropdown.set(AUDIO_FORMATS[0])
        else:
            cls.__dropdown['values'] = VIDEO_FORMATS
            cls.__dropdown.set(VIDEO_FORMATS[0])

    @classmethod
    def __get_language_data(cls: type[Self]) -> list[str]:
        return Language.from_str(cls.__language.get()).get_lines()

    @classmethod
    def __update_language(cls: type[Self], language: tk.StringVar) -> None:
        if not cls.__is_inited:
            return
        comp_array: list[tk.Label | tk.Radiobutton | tk.Checkbutton | tk.Button] = [
            cls.__language_label, cls.__input_label, cls.__radio_video, cls.__radio_audio,
            cls.__dropdown_label, cls.__button, cls.__checkbox
        ]
        line_list = cls.__get_language_data()
        for i in range(len(comp_array)):
            comp_array[i].config(text=line_list[i])


    @classmethod
    def __dwld_callback(cls: type[Self], success: bool) -> None:
        if not cls.__is_inited:
            return
        cls.__button.config(state='normal', text=cls.__get_language_data()[5])


    @classmethod
    def __on_button_press(cls: type[Self]) -> None:
        if not cls.__is_inited or Downloader.mutex_is_locked():
            return
        cls.__output_box.delete('1.0', tk.END)
        user_input = cls.__input_box.get()
        download_thread = threading.Thread(target=Downloader.download, args=(
            user_input.strip(),
            cls.__dropdown.get(),
            cls.__audio_only.get(),
            cls.__use_system_ffmpeg.get()
        ))
        download_thread.start()
        cls.__button.config(state='disabled', text="...")

    @classmethod
    def __init_everything(cls: type[Self]) -> None:
        cls.__root = tk.Tk()
        cls.__root.title("YT-DLPackaged by Noise")

        # Variables
        cls.__audio_only = tk.BooleanVar(cls.__root, value=False)
        cls.__language = tk.StringVar(cls.__root, value=Language.ENGLISH)
        cls.__use_system_ffmpeg = tk.BooleanVar(cls.__root, value=False)

        # Components
        cls.__language_label = tk.Label(cls.__root, text=GUI_LINES_ENGLISH[0])
        cls.__input_label = tk.Label(cls.__root, text=GUI_LINES_ENGLISH[1])
        cls.__input_box = tk.Entry(cls.__root, width=50)
        cls.__radio_video = tk.Radiobutton(cls.__root, text=GUI_LINES_ENGLISH[2], variable=cls.__audio_only,
            value=False, command=cls.__update_dropdown)
        cls.__radio_audio = tk.Radiobutton(cls.__root, text=GUI_LINES_ENGLISH[3], variable=cls.__audio_only,
            value=True, command=cls.__update_dropdown)
        cls.__dropdown_label = tk.Label(cls.__root, text=GUI_LINES_ENGLISH[4], width=7)
        cls.__dropdown = ttk.Combobox(cls.__root, state='readonly', width=5)
        cls.__button = tk.Button(cls.__root, text=GUI_LINES_ENGLISH[5], command=cls.__on_button_press)
        cls.__output_box = ScrolledText(cls.__root, height=20, width=80, state=tk.NORMAL)
        cls.__checkbox = tk.Checkbutton(cls.__root, text=GUI_LINES_ENGLISH[6], variable=cls.__use_system_ffmpeg,
            onvalue=True, offvalue=False)
        cls.__language_selector = tk.OptionMenu(cls.__root, cls.__language, *[i.value for i in Language], command=cls.__update_language)
        cls.__is_inited = True

    @classmethod
    def __place_elements(cls: type[Self]) -> None:
        if not cls.__is_inited:
            return
        cls.__language_label.grid(   sticky='e', row=0, column=0, columnspan=2, pady=(10, 10))
        cls.__language_selector.grid(sticky='w', row=0, column=2, columnspan=2, pady=(10, 10))
        cls.__input_label.grid(      sticky='w', row=1, column=0)
        cls.__input_box.grid(        sticky='w', row=1, column=1, columnspan=3)
        cls.__radio_video.grid(      sticky='w', row=2, column=0)
        cls.__radio_audio.grid(      sticky='w', row=3, column=0)
        cls.__dropdown_label.grid(   sticky='e', row=2, column=1)
        cls.__dropdown.grid(         sticky='w', row=2, column=2)
        cls.__button.grid(           sticky='s', row=3, column=1, columnspan=2)
        cls.__checkbox.grid(         sticky='w', row=2, column=3, rowspan=2)
        cls.__output_box.grid(       sticky='w', row=4, column=0, columnspan=4)

    @classmethod
    def render(cls: type[Self]) -> None:
        cls.__init_everything()
        cls.__place_elements()
        Downloader.set_callback(cls.__dwld_callback)
        cls.__update_dropdown()
        StdRedir.redirect_to(cls.__output_box)
        cls.__root.mainloop()
