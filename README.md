# model_server

# Python App Docker Setup

This project runs a Python application using Docker.

## Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your machine.

## Getting Started

### 1. Build the Docker Image

```bash
docker build -t my-python-app .
docker run -p 8000:8000 my-python-app
