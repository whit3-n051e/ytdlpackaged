from typing import Any, Self
import yt_dlp # type: ignore
import os
import sys
import threading
import winreg
from pathlib import Path


class Downloader(object):
    def __init__(self: Self) -> None:
        pass

    @staticmethod
    def __progress_hook(d: Any) -> None:
        if d['status'] == 'downloading':
            sys.stdout.write("\n")
            sys.stdout.flush()
        elif d['status'] == 'finished':
            print("\nDownload finished. Now post-processing...")

    @staticmethod
    def __cd_to_downloads() -> None:
        try:
            if os.name == "nt":
                sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
                downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                    location = winreg.QueryValueEx(key, downloads_guid)[0]
            else:
                location = str(Path.home() / "Downloads")
            os.chdir(location)
        except:
            pass

    __OPTS: dict[str, Any] = {
        'ffmpeg_location': os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))), '.'),
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': False,
        'no_warnings': False,
        'progress_hooks': [__progress_hook],
        'use_mtime': True
    }

    __mutex = threading.Lock()

    @classmethod
    def download(cls: type[Self], url: str) -> None:
        with cls.__mutex:
            print("Начинаю загрузку...")
            try:
                Downloader.__cd_to_downloads()
                with yt_dlp.YoutubeDL(cls.__OPTS) as ydl:
                    ydl.download([url]) # type: ignore
                print("\nГотово!\nОшибок, вроде, нет.")
            except:
                print("\nНе догрузилось.")

    @classmethod
    def mutex_is_locked(cls: type[Self]) -> bool:
        return cls.__mutex.locked()
