rmdir /Q /S Livrable
pyinstaller --onefile --hidden-import "babel.numbers" main.py
mkdir Reliquats_exec
move build  Reliquats_exec
move dist  Reliquats_exec
move main.spec  Reliquats_exec
mkdir Livrable
Xcopy /e /s /I  DB Livrable\DB
del Livrable\DB\HotelBDD.db
Xcopy /e /s /I Images Livrable\Images
mkdir Livrable\Logs\Feuilles_de_jour
Xcopy /e /s /I Reliquats_exec\dist\main.exe Livrable
rename Livrable\main.exe Bellevue.exe
rmdir /Q /S Reliquats_exec
