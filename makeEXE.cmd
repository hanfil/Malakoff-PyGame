set YYYYMMDD=%DATE:~10,4%%DATE:~4,2%%DATE:~7,2%
PyInstaller --onefile --clean scene_template.py --name=Malakoff_PyGame-%YYYYMMDD%