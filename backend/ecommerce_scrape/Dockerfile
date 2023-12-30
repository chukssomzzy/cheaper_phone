# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

################################################################################
# Pick a base image to serve as the foundation for the other build stages in
# this file.
#
# For illustrative purposes, the following FROM command
# is using the alpine image (see https://hub.docker.com/_/alpine).
# By specifying the "latest" tag, it will also use whatever happens to be the
# most recent version of that image when you build your Dockerfile.
# If reproducability is important, consider using a versioned tag
# (e.g., alpine:3.17.2) or SHA (e.g., alpine@sha256:c41ab5c992deb4fe7e5da09f67a8804a46bd0592bfdf0b1847dde0e0889d2bff).
ARG PYTHON_VERSION=3.10.12
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# download mysql 
RUN apt-get -yqq update && \
    apt-get -yq install python3-pip python3-dev libssl-dev && \
    apt-get -yq install pkg-config default-libmysqlclient-dev build-essential pkg-config && \
    export MYSQLCLIENT_CFLAGS=`pkg-config mysqlclient --cflags` && \
    export MYSQLCLIENT_LDFLAGS=`pkg-config mysqlclient --libs`
RUN apt-get install -yq alembic
RUN apt-get -yqq update && apt-get install -y  netcat-openbsd
WORKDIR /app
 

# ARG UID=10001
# RUN adduser \
#     --disabled-password \
#     --gecos "" \
#     --shell "/sbin/nologin" \
#     --uid "${UID}" \
#     appuser
# USER appuser
#
# Copy the executable from the "build" stage.
COPY ecommerce_scrape ecommerce_scrape/   
COPY  scrapy.cfg . 
COPY  alembic alembic/
COPY  alembic.ini .
COPY .env .
COPY models models/
RUN rm -r alembic/versions

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=ecommerce_scrape/requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt 

# What the container should run when it is started.
CMD alembic upgrade head && \
        scrapy crawl products
