FROM alpine:latest

ENV APP_HOME=/mastodon_stats_bot
ENV PYTHONUNBUFFERED=1

RUN apk update \
    && apk upgrade \
    && apk add --no-cache \
    gcc \
    libc-dev \
    libjpeg-turbo-dev \
    libxml2-dev \
    libxslt-dev \
    openjpeg \
    python3-dev \
    sqlite \
    tiff-dev \
    tzdata \
    zlib-dev

RUN cp /usr/share/zoneinfo/Europe/Madrid /etc/localtime && \
    echo "Europe/Madrid" > /etc/timezone && \
    apk del tzdata

COPY ./app $APP_HOME

RUN ln -sf python3 /usr/bin/python && \
    python3 -m ensurepip && \
    pip3 install --no-cache-dir --upgrade pip setuptools && \
    pip3 install --no-cache-dir -r $APP_HOME/requirements.txt

COPY ./bin /usr/local/bin
RUN chmod a+x /usr/local/bin/*

COPY ./utils/crontab.txt /crontab.txt
RUN /usr/bin/crontab /crontab.txt

ENTRYPOINT ["init_container"]