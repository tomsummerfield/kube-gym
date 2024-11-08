# API Service

This service is a simple FastAPI application that provides a REST API for the KubeGym project.

## Running the service

To run the service in development mode, you can use the following command:

```bash
fastapi dev main.py --reload
```

Be warned that this will run the server on port 8000 on localhost. To access it via the docker container, you need to change the 0.0.0.0 ip address to localhost. 
