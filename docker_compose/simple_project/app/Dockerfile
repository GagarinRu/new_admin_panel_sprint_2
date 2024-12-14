FROM python:3.10

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'example.settings'

COPY requirements.txt requirements.txt
COPY uwsgi/uwsgi.ini uwsgi.ini

RUN  apt-get update \
     && apt-get install sudo \
     && sudo apt-get -y install gcc \
     && pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

COPY . .
COPY entrypoint.sh entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["bash", "entrypoint.sh"]