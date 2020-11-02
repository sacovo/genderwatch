# pull official base image
FROM python:3.7-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
  apt-get install -y \
    netcat

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/
RUN mkdir -p /usr/src/app/storage/media/ && \
      mkdir -p /usr/src/app/storage/static/

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
