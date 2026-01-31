# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.11-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED=1

# Copy local code to the container image.
ENV APP_HOME=/app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
# Accessing meeting_os/requirements.txt assuming flat structure or adjustment
RUN pip install --no-cache-dir -r meeting_os/requirements.txt
RUN pip install fastapi uvicorn

# Run the web service on container startup.
# Using uvicorn directly or via python main.py
CMD ["python", "main.py"]
