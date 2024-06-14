#!/bin/bash
DOCKER_IMAGE="jsanchez0x/mastodon-stats-bot"
DOCKER_TAG="local"
DOCKER_CONTAINER_NAME="mastodon-stats-bot"
APP_HOME="/mastodon_stats_bot"

if [ "$1" == "image" ]; then
    docker build --rm --tag ${DOCKER_IMAGE}:${DOCKER_TAG} .

    docker run -d -it \
    -v $(pwd)/tecladostracker-data:${APP_HOME}/data/volume \
    -v $(pwd)/tecladostracker-logs:${APP_HOME}/logs \
    --env-file utils/env.list \
    --name ${DOCKER_CONTAINER_NAME} ${DOCKER_IMAGE}:${DOCKER_TAG}

elif [ "$1" == "init" ]; then
    docker exec ${DOCKER_CONTAINER_NAME} init_bots

elif [ "$1" == "crontab" ]; then
    docker exec ${DOCKER_CONTAINER_NAME} scheduling_bots

elif [ "$1" == "stats" ]; then
    docker exec ${DOCKER_CONTAINER_NAME} bot_stats

elif [ "$1" == "cm" ]; then
    docker exec ${DOCKER_CONTAINER_NAME} bot_cm

elif [ "$1" == "sqlite" ]; then
    docker exec -it ${DOCKER_CONTAINER_NAME} sqlite3 ${APP_HOME}/data/volume/db.sqlite

elif [ "$1" == "shell" ]; then
    docker exec -it ${DOCKER_CONTAINER_NAME} sh

else
    echo "v1.0"
    echo "Helper for run commands in the container.\n"
    echo "PARAMETERS:"
    echo "    image                       Create and run the docker image."
    echo "    init                        Create the database, paths and warmup."
    echo "    crontab                     Activate or deactivate cronjobs for schedule bot executions."
    echo "    <stats/cm>                  Run the bots."
    echo "    sqlite                      SQLite prompt in database."
    echo "    shell                       SH prompt."

fi
