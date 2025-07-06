from .src import Downloader, StdRedir
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading


def main():
    root = tk.Tk()
    root.title("YT-DLPackaged by Noise")

    label = tk.Label(root, text="Вставь ссылку на видео в поле ниже:")
    label.grid(row=0, column=0)

    entry = tk.Entry(root, width=50)
    entry.grid(row=0, column=1)

    output_box = ScrolledText(root, height=20, width=80, state=tk.NORMAL)
    output_box.grid(row=2, columnspan=2)

    def on_run():
        if not Downloader.mutex_is_locked():
            output_box.delete('1.0', tk.END)  # clear previous output
            user_input = entry.get()
            thread = threading.Thread(target=Downloader.download, args=(user_input,))
            thread.start()

    run_button = tk.Button(root, text="Скачать", command=on_run)
    run_button.grid(row=1, columnspan=2)

    StdRedir.redirect_to(output_box)
    root.mainloop()
