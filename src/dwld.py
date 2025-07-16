from typing import Any, Self, Callable
import yt_dlp # type: ignore
import os
import sys
import threading
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
        location: str | None = None
        try:
            if location is None:
                location = str(Path.home() / "Downloads")
            os.chdir(location)
        except:
            pass


    __BASE_OPTS: dict[str, Any] = {
        'ffmpeg_location': os.path.join(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))), '.'),
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet': False,
        'no_warnings': False,
        'progress_hooks': [__progress_hook],
        'use_mtime': True
    }

    __VIDEO_OPTS: dict[str, Any] = {
        'format': 'bestvideo+bestaudio/best',
    }

    __AUDIO_OPTS: dict[str, Any] = {
        'format': 'bestaudio',
        'extract_audio': True,
    }

    __mutex = threading.Lock()
    __callback: Callable[[bool], None] = lambda a: None

    @classmethod
    def set_callback(cls: type[Self], callback: Callable[[bool], None]) -> None:
        cls.__callback = callback

    @classmethod
    def download(cls: type[Self], url: str, format: str, audio_only: bool = False, use_system_ffmpeg: bool = False) -> None:
        result = False
        with cls.__mutex:
            print("Starting...")
            try:
                settings = cls.__BASE_OPTS.copy()
                if use_system_ffmpeg:
                    del settings['ffmpeg_location']
                settings.update(cls.__AUDIO_OPTS if audio_only else cls.__VIDEO_OPTS)
                if audio_only:
                    settings['postprocessors'] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': format,
                        'preferredquality': '0',
                    }]
                else:
                    settings['merge_output_format'] = format
                Downloader.__cd_to_downloads()
                with yt_dlp.YoutubeDL(settings) as ydl:
                    ydl.download([url]) # type: ignore
                print("\nDone.")
                result = True
            except:
                print("\nCould not finish.")
        cls.__callback(result)

    @classmethod
    def mutex_is_locked(cls: type[Self]) -> bool:
        return cls.__mutex.locked()
