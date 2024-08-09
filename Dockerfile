# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.12.5
FROM python:${PYTHON_VERSION}-alpine AS base

WORKDIR /app

COPY requirements.txt /app
COPY app.py /app

RUN python -m pip install --root-user-action=ignore -r requirements.txt

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD python3 app.py