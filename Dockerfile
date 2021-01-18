FROM python:3.9-alpine

ENV FLASK_APP weather.py
ENV FLASK_CONFIG docker

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev \
    && apk add busybox-suid openssl-dev libffi-dev

RUN adduser -D weather

USER weather

WORKDIR /home/weather

RUN touch crontab.tmp \
    && echo '0 * * * * /home/weather/venv/bin/flask forecast' > crontab.tmp \
    && crontab crontab.tmp \
    && rm -rf crontab.tmp

COPY requirements requirements
RUN python -m venv venv
RUN venv/bin/pip install -r requirements/docker.txt

COPY app app
COPY migrations migrations
COPY weather.py config.py boot.sh ./

# run-time configuration
EXPOSE 5000

USER root
ENTRYPOINT /usr/sbin/crond -c /etc/crontabs/ -l 0 -d 0; ./boot.sh