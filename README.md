# model_server

# Python App Docker Setup

This project runs a Python application using Docker.

## Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your machine.

## Getting Started

### 1. Build the Docker Image

```bash
# builde and run 
docker build -t model:v1 .
docker run -p 8080:8080 model:v1

# curl
# load the model 
curl -X POST http://localhost:8080/load_model \
     -H "Content-Type: application/json" \
     -d '{"path": "./model/Run_all_soft_action_Date_20_Feb_25_Timesteps_10000000_MaxSteps_10000_TalkThreshold_0.7"}'


 
