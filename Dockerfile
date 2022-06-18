FROM python:3.10.4-slim-buster

WORKDIR usr/scr/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

# устанавливаем зависимости для psycopg2, далее requirements
RUN apt-get update && \
    apt-get -y install libpq-dev gcc && \
    pip install --no-cache-dir -r requirements.txt