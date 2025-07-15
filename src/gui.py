from typing import Self
from .dwld import Downloader
from .stdredir import StdRedir
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import threading
import time


VIDEO_FORMATS = ['mp4', 'avi', 'flv', 'mkv', 'mov', 'webm']
AUDIO_FORMATS = ['mp3', 'aac', 'alac', 'flac', 'm4a', 'opus', 'vorbis', 'wav']


class Gui(object):
    def __init__(self: Self) -> None:
        pass

    __audio_only: tk.BooleanVar | None = None

    __root: tk.Tk | None = None
    __input_label: tk.Label | None = None
    __dropdown_label: tk.Label | None = None
    __dropdown: ttk.Combobox | None = None
    __button: tk.Button | None = None
    __output_box: ScrolledText | None = None
    __input_box: tk.Entry | None = None
    __radio_video: tk.Radiobutton | None = None
    __radio_audio: tk.Radiobutton | None = None

    @classmethod
    def __update_dropdown(cls: type[Self]) -> None:
        if cls.__dropdown is None or \
            cls.__audio_only is None:
            return
        if cls.__audio_only.get():
            cls.__dropdown['values'] = AUDIO_FORMATS
            cls.__dropdown.set(AUDIO_FORMATS[0])
        else:
            cls.__dropdown['values'] = VIDEO_FORMATS
            cls.__dropdown.set(VIDEO_FORMATS[0])

    @classmethod
    def __revert_button_state(cls: type[Self]) -> None:
        if cls.__button is None:
            return
        while Downloader.mutex_is_locked():
            time.sleep(0.1)
        cls.__button.config(state='normal', text="Скачать")

    @classmethod
    def __on_button_press(cls: type[Self]) -> None:
        if cls.__button is None or \
            cls.__output_box is None or \
            cls.__input_box is None or \
            cls.__audio_only is None or \
            cls.__dropdown is None or \
            Downloader.mutex_is_locked():
            return
        cls.__output_box.delete('1.0', tk.END)
        user_input = cls.__input_box.get()
        download_thread = threading.Thread(target=Downloader.download, args=(
            user_input.strip(),
            cls.__dropdown.get(),
            cls.__audio_only.get()
        ))
        download_thread.start()
        cls.__button.config(state='disabled', text="Скачивается...")
        button_revert_thread = threading.Thread(target=cls.__revert_button_state, args=tuple())
        button_revert_thread.start()


    @classmethod
    def render(cls: type[Self]) -> None:
        cls.__root = tk.Tk()
        cls.__root.title("YT-DLPackaged by Noise")
        cls.__audio_only = tk.BooleanVar(cls.__root, value=False)
        cls.__input_label = tk.Label(cls.__root, text="Ссылка на видео:")
        cls.__input_box = tk.Entry(cls.__root, width=50)
        cls.__radio_video = tk.Radiobutton(cls.__root, text='Видео', variable=cls.__audio_only,
            value=False, command=cls.__update_dropdown)
        cls.__radio_audio = tk.Radiobutton(cls.__root, text='Только аудио', variable=cls.__audio_only,
            value=True, command=cls.__update_dropdown)
        cls.__dropdown_label = tk.Label(cls.__root, text="Формат:", width=7)
        cls.__dropdown = ttk.Combobox(cls.__root, state='readonly', width=5)
        cls.__update_dropdown()
        cls.__button = tk.Button(cls.__root, text='Скачать', command=cls.__on_button_press)
        cls.__output_box = ScrolledText(cls.__root, height=20, width=80, state=tk.NORMAL)
        StdRedir.redirect_to(cls.__output_box)

        cls.__input_label.grid(   sticky='w', row=0, column=0)
        cls.__input_box.grid(     sticky='w', row=0, column=1, columnspan=2)
        cls.__radio_video.grid(   sticky='w', row=1, column=0)
        cls.__radio_audio.grid(   sticky='w', row=2, column=0)
        cls.__dropdown_label.grid(sticky='e', row=1, column=1)
        cls.__dropdown.grid(      sticky='w', row=1, column=2)
        cls.__button.grid(        sticky='s', row=2, column=1, columnspan=2)
        cls.__output_box.grid(    sticky='w', row=3, column=0, columnspan=3)

        cls.__root.mainloop()
