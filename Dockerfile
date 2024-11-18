# Use the Alpine base Python image
FROM python:3.11-alpine

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Copy the server.py script to the working directory
COPY server.py .

# Copy the additional folder to the working directory
COPY unoserver_master ./unoserver_master

# Copy the requirements.txt file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run the server.py script
CMD ["python", "server.py"]
