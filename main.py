import winreg
import yt_dlp
import os
import sys
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading

# MUST INSTALL FFMPEG THROUGH CHOCOLATEY BEFORE RUNNING compile.bat


mutex = threading.Lock()


def progress_hook(d):
    if d['status'] == 'downloading':
        sys.stdout.write("\n")
        sys.stdout.flush()

    elif d['status'] == 'finished':
        print("\nDownload finished. Now post-processing...")


OPTS = {
    'ffmpeg_location': os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))), '.'),
    'format': 'bestvideo+bestaudio/best',
    'merge_output_format': 'mp4',
    'outtmpl': '%(title)s.%(ext)s',
    'noplaylist': True,
    'quiet': True,
    'no_warnings': True,
    'progress_hooks': [progress_hook],
    'no_set_creation_date': True,
    'use_mtime': True
}



def cd_to_downloads() -> None:
    try:
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        os.chdir(location)
    except:
        pass


def download(url: str) -> None:
    with mutex:
        print("Starting...")
        try:
            cd_to_downloads()
            with yt_dlp.YoutubeDL(OPTS) as ydl:
                ydl.download([url])
            print("\nDone!")
        except:
            pass


def main_cli():
    url = input("\x1b[35mEnter link to video: \x1b[0m").strip()
    download(url)
    input("\x1b[35mPress Enter to exit. \x1b[0m")


class StdoutRedirector:
    def __init__(self, text_widget: ScrolledText):
        self._text_widget = text_widget
    
    def write(self, s: str):
        self._text_widget.insert(tk.END, s)
        self._text_widget.see(tk.END)

    def flush(self):
        pass  # Leave it be like that


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
        if not mutex.locked():
            output_box.delete('1.0', tk.END)  # clear previous output
            user_input = entry.get()
            thread = threading.Thread(target=download, args=(user_input,))
            thread.start()

    run_button = tk.Button(root, text="Скачать", command=on_run)
    run_button.grid(row=1, columnspan=2)

    sys.stdout = StdoutRedirector(output_box)
    sys.stderr = sys.stdout
    root.mainloop()


main()
