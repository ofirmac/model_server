# Use the official Ubuntu base image
FROM ubuntu:22.04

# Set environment variables to prevent interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip 

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt first to install dependencies
COPY requirements.txt /app/

# Install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy the rest of your Flask + DQN application
COPY . /app/

# Expose the Flask app port
EXPOSE 5000

# Command to run your Flask app
CMD ["python3", "server.py"]
