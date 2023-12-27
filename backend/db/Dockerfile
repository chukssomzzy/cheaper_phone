
# PULL mysql base image 
FROM mysql:8.0-debian

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
        --disabled-password \
        --gecos "" \
        --home "/nonexistent" \
        --shell "/sbin/nologin" \
        --no-create-home \
        --uid "${UID}" \
        cheaper_phone_db_user 

WORKDIR /app

COPY alembic.ini /app/
COPY alembic /app/
COPY sql /app/

RUN apt-get -yqq update && \
    apt-get -yq install python3-pip python3-dev libssl-dev && \
    apt-get -yq install pkg-config default-libmysqlclient-dev build-essential pkg-config && \
    export MYSQLCLIENT_CFLAGS=`pkg-config mysqlclient --cflags` && \
    export MYSQLCLIENT_LDFLAGS=`pkg-config mysqlclient --libs`

ARG  DATABASE_NAME="cheaper_phone_db"
RUN pip3 install alembic==1.13.1
RUN pip3 install mysqlclient==2.2.1 
CMD mysql -uroot --password="${MYSQL_ROOT_PASSWORD}" < setup_mysql_dev.sql && \ 
        mysql -u root --password="${MYSQL_ROOT_PASSWORD}" "${DATABASE_NAME}" << cheaper_phone_db_dump.sql && \ 
        alembic upgrade head

