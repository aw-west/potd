:Config
cd %~dp0
set NAME=potd
set PYTHONOPTIMIZE=1

:Run
pyinstaller --log-level=WARN --onefile --specpath=build %NAME%.py

:Clean
move /y dist\%NAME%.exe ..\%NAME%.exe & rmdir /q /s dist & rmdir /q /s __pycache__ & rmdir /q /s build

:End
exit
