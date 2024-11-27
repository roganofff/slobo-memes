FROM python:3.11

RUN mkdir -p /usr/src/slobo_memes/bot_service
WORKDIR /usr/src/slobo_memes/bot_service

COPY . /usr/src/slobo_memes/bot_service

RUN pip3 install --upgrade  poetry==1.8.3

RUN python3 -m poetry config virtualenvs.create false \
    && python3 -m poetry install --no-interaction --no-ansi \
    && echo yes | python3 -m poetry cache clear . --all