# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

ARG PYTHON_VERSION=3.10.12
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

RUN apt-get -yqq update && \
    apt-get -yq install python3-pip python3-dev libssl-dev && \
    apt-get -yq install pkg-config default-libmysqlclient-dev build-essential pkg-config && \
    export MYSQLCLIENT_CFLAGS=`pkg-config mysqlclient --cflags` && \
    export MYSQLCLIENT_LDFLAGS=`pkg-config mysqlclient --libs` && \ 
    apt-get -yq install gunicorn
 
WORKDIR /app

# # Create a non-privileged user that the app will run under.
# # See https://docs.docker.com/go/dockerfile-user-best-practices/
# ARG UID=10001
# RUN adduser \
#     --disabled-password \
#     --gecos "" \
#     --shell "/sbin/nologin" \
#     --uid "${UID}" \
#     appuser
#
#
#
# # Switch to the non-privileged user to run the application.
# USER appuser
#
# Copy the source code into the container.
ADD  models models/
ADD  api api/
ADD  .env .


# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=api/requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt 

# Expose the port that the application listens on.
EXPOSE 5000

# Run the application.
CMD gunicorn 'api.v1.app:app' --workers 3 --bind=0.0.0.0:5000
