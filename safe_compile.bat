@echo off
pyinstaller --noconsole --onefile --strip --noupx .\__main__.py --add-binary "C:\ProgramData\chocolatey\lib\ffmpeg\tools\ffmpeg\bin\ffmpeg.exe;." --add-binary "C:\ProgramData\chocolatey\lib\ffmpeg\tools\ffmpeg\bin\ffprobe.exe;."
