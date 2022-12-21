# Pull base image
FROM python:3
# Set environment variables
#ENV PYTHONUNBUFFERED 1
# Create and set working environment --> all further
# commands will be added to the working directory
WORKDIR /app
RUN mkdir ./flask

# Persistence requirement
#RUN apt-get install libpq-dev

# Install the application requirements
COPY ./requirements.txt ./flask/
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r ./flask/requirements.txt

# Copy CONTENTS of source to flask folder.
COPY . ./flask/

# Change work directory
WORKDIR /app/flask-api

# Run flask directly
CMD flask run --host="0.0.0.0"
