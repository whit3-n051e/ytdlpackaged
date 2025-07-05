import winreg
import yt_dlp
import os
import sys

# MUST INSTALL FFMPEG THROUGH CHOCOLATEY BEFORE RUNNING compile.bat

def get_download_path() -> str:
    sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
    downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
        location = winreg.QueryValueEx(key, downloads_guid)[0]
    return str(location)

def get_ffmpeg_path() -> str:
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, '.')

OPTS = {
    'format': 'bestvideo+bestaudio/best',
    'merge_output_format': 'mp4',
    'outtmpl': '%(title)s.%(ext)s',
    'noplaylist': True,
    'quiet': False,
    'ffmpeg_location': get_ffmpeg_path()
}

def main():
    try:
        os.chdir(get_download_path())
        url = input("\x1b[35mEnter link to video: \x1b[0m").strip()
        with yt_dlp.YoutubeDL(OPTS) as ydl:
            ydl.download([url])
    except:
        print("\x1b[31mThere was an error (maybe not, check yourself.)\x1b[0m")
    input("\x1b[35mPress Enter to exit. \x1b[0m")

main()
