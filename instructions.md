Great to hear that it worked! Let's detail the steps needed to set up this environment and then create a Dockerfile to containerize the application.

Steps to Set Up the Environment
Install LibreOffice: Ensure LibreOffice is installed on your system. You can download it from LibreOffice's official website.

Install Python and Flask: Ensure you have Python installed. Then, create a virtual environment and install Flask.
"C:\Program Files\LibreOffice\program\python.exe" get-pip.py


"C:\Program Files\LibreOffice\program\python.exe" -m pip install flask

run_app.bat


to build:
docker buildx build -t flask-libreoffice .

docker run -d --name flask-app --network my_network -p 5000:5000 -e UNOSERVER_HOST=unoserver -e UNOSERVER_PORT=2003 flask-unoserver