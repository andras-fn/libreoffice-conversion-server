## unoconv flask server
this is a simple flask api that receives files and then sends the conversion request to an unoconv server running as a container (https://github.com/unoconv/unoserver-docker)

run it using:
 - python server.py

send requests to it like:
 - curl --location 'http://127.0.0.1:5000/convert' --form 'file=@"/C:/path/to/file/file.docx"' --form 'convert_to="png"'

if a convert_to param isn't set then it'll convert to pdf



run libreoffice in headless and listening mode:
```bash
libreoffice --headless --accept="socket,host=127.0.0.1,port=2002;urp;StarOffice.ServiceManager"
```