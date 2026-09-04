FROM ubantu:16.04

RUN apt-get update && apt-get -y install \
    build-essetial libpre3 libpre3-dev zlib1g zlib1g-dev libssl-dev wget

FROM python:3.7-slim-stretch
COPY ./app app

RUN apt-get update
RUN apt-get install -y --no-recommends \
    libatlas-base-dev gfortran nginx supervisor

RUN pip3 install uwsgi
RUN useradd --no-create-home nginx

RUN rm /etc/nginx/sites-enabled/default
RUN rm -r /root/.cache

RUN mkdir /log
RUN mkdir /log/critical_logs
RUN mkdir /log/debug_logs
RUN mkdir /log/error_logs
RUN mkdir /log/info_logs
RUN chmod -R 777 /log/*

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY run.py .