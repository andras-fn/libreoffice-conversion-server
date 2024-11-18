@echo off
REM Start LibreOffice in headless mode
start "" "C:\Program Files\LibreOffice\program\soffice.exe" --headless --accept="socket,host=127.0.0.1,port=2002;urp;StarOffice.ServiceManager" --nologo --nodefault --nofirststartwizard --nolockcheck --norestore

REM Wait for a few seconds to ensure LibreOffice has started
timeout /t 5

REM Run the Flask application using LibreOffice's Python interpreter
"C:\Program Files\LibreOffice\program\python.exe" app.py