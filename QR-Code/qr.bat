@echo off
set pypath=C:\ProgramData\Anaconda3\python.exe
set pic_path=%1

%pypath% %~dp0\qr.py %pic_path%