cd %~dp0

del /q /s potd.exe

pyinstaller --onefile potd.py

move /y .\dist\potd.exe potd.exe
rmdir /q /s __pycache__
rmdir /q /s build
rmdir /q /s dist
del /q /s potd.spec

pause
