FROM python:2.7.9

MAINTAINER Luis Mayta <@slovacus>

WORKDIR /app/

COPY ./requirements /app/requirements
COPY ./requirements.txt /app/

# install python dependencies
RUN apt-get update \
    && apt-get install -y zsh \
    && apt-get autoremove -y \
    && pip install --upgrade pip \
    && pip install -r /app/requirements/dev.txt
