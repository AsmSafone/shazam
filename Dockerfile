# Use the latest version of Debian
FROM python:3.9

# Update and install dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    ffmpeg

# Set the working directory
WORKDIR /app

# Copy the FastAPI application into the container
COPY . .

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Expose the port that the app runs on
EXPOSE 5000

# Command to run the application
CMD ["python3", "main.py"]
