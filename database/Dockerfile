FROM python:3.11

RUN mkdir -p /usr/src/slobo_memes/database
WORKDIR /usr/src/slobo_memes/database

COPY . /usr/src/slobo_memes/database

RUN pip3 install --upgrade  poetry==1.8.3

RUN python3 -m poetry config virtualenvs.create false \
    && python3 -m poetry install --no-interaction --no-ansi \
    && echo yes | python3 -m poetry cache clear . --all