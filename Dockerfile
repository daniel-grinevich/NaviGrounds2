# Pull base image 
FROM --platform=linux/amd64 python:3.10.6-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYCODE 1
ENV PYTHONNUMBUFFERED 1

# Set work directory
WORKDIR /NaviGrounds2

# Install dependencies 
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .

