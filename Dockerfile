FROM alpine:latest

ENV APP_HOME=/mastodon_stats_bot
ENV PYTHONUNBUFFERED=1

RUN apk update && \
    apk upgrade && \
    apk add --no-cache \
        python3 \
        sqlite \
        libjpeg-turbo-dev \
        openjpeg \
        tiff-dev \
        zlib-dev && \
    python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip setuptools wheel

RUN apk add --no-cache tzdata && \
    cp /usr/share/zoneinfo/Europe/Madrid /etc/localtime && \
    echo "Europe/Madrid" > /etc/timezone && \
    apk del tzdata

COPY ./app $APP_HOME

RUN apk add --no-cache --virtual .build-deps \
        build-base \
        python3-dev && \
    /opt/venv/bin/pip install --no-cache-dir -r $APP_HOME/requirements.txt && \
    apk del .build-deps

ENV PATH="/opt/venv/bin:$PATH"

COPY ./bin /usr/local/bin
RUN chmod a+x /usr/local/bin/*

COPY ./utils/crontab.txt /crontab.txt
RUN /usr/bin/crontab /crontab.txt

ENTRYPOINT ["init_container"]