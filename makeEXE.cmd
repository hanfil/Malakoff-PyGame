set YYYYMMDD=%DATE:~10,4%%DATE:~4,2%%DATE:~7,2%
PyInstaller --onefile --clean Malakoff_PyGame.spec --name=Malakoff_PyGame-%YYYYMMDD%