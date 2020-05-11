FROM python:3.7-alpine

WORKDIR /opt/app

COPY ./requirements.txt ./requirements.txt

RUN apk update && python3 -m venv /opt/app/venv

RUN /opt/app/venv/bin/pip install --no-cache-dir -r requirements.txt \
    && rm -rf /opt/venv/src/*/.git \
    && rm -rf ~/.gitconfig 

COPY ./watcher /opt/app/watcher

ENV APP_NAME watcher
ENV LOGSTASH_HOST http://logstash:9253

CMD ["/opt/app/venv/bin/python", "-m", "watcher"]