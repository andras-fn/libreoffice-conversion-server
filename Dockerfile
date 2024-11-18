# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    libreoffice \
    libreoffice-writer \
    libreoffice-calc \
    libreoffice-impress \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run LibreOffice in headless mode
RUN mkdir -p /usr/lib/libreoffice/program
COPY run_libreoffice.sh /usr/lib/libreoffice/program/run_libreoffice.sh
RUN chmod +x /usr/lib/libreoffice/program/run_libreoffice.sh

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME World

# Run the application
CMD ["/bin/bash", "-c", "/usr/lib/libreoffice/program/run_libreoffice.sh & python app.py"]
