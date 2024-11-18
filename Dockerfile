# Use an official Python runtime as a parent image
FROM python:3.9-alpine

# Install dependencies
RUN apk update && apk add --no-cache \
    libreoffice \
    libreoffice-writer \
    libreoffice-calc \
    libreoffice-impress \
    curl \
    bash \
    openjdk11-jre \
    && rm -rf /var/cache/apk/*

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for LibreOffice UNO
ENV PYTHONPATH="/usr/lib/libreoffice/program"
ENV LD_LIBRARY_PATH="/usr/lib/libreoffice/program"

# Run LibreOffice in headless mode
RUN mkdir -p /usr/lib/libreoffice/program
COPY run_libreoffice.sh /usr/lib/libreoffice/program/run_libreoffice.sh
RUN chmod +x /usr/lib/libreoffice/program/run_libreoffice.sh

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the application
CMD ["/bin/bash", "-c", "/usr/lib/libreoffice/program/run_libreoffice.sh & sleep 5 && python app.py"]
