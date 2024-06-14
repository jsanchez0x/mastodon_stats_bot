# Mastodon Stats bot

## Bots

### app/bot_stats.py
Read from [Mastodon stats endpoint](https://api.fedidb.org/v1/stats), generate a graph and post it on Mastodon.

### app/bot_cm.py
This bot does:
1. It follows accounts that follow the configured account and also adds them to a *follow backs list*.
2. It unfollows accounts that have stopped following the configured account and removes them from the follow backs list.


## Requeriments
- Docker
- Create a [Mastodon app](https://masto.es/settings/applications)


## Create and run the image
The container image is created and run with the following command:
```bash
./utils/container.sh image
```


## Running the container

### 1. Necessary and optional environment variables
| Name                         | Mandatory | Description                                            |
| ---------------------------- | --------- | -------------------------------------------------------|
| APP_MASTODON_ACCESS_TOKEN    | **Yes**   | Necessary to interact with the Mastodon API            |
| APP_DEBUG                    | No        | If present, the bots will go into verbose mode.        |
| APP_MASTODON_INTERACTION     | No        | If present, bots will perform actions on Mastodon.     |
| APP_DB_CHANGES               | No        | If present, changes will be persisted in the database. |
| APP_PRODUCTION_ENV           | No        | If present, the crontab will be started in foreground. |

To start a container with environment variables there is more information [here](https://docs.docker.com/engine/reference/commandline/run/#set-environment-variables--e---env---env-file).

### 2. Volumes
It may be interesting to create the following volumes to persist and access the data more comfortably.

| Path in container           | Description                           |
| --------------------------- | --------------------------------------|
| ${APP_HOME}/data/volume     | Required to store the database.       |
| ${APP_HOME}/logs            | The logs will be stored in this path. |

To start a container with volumes there is more information [here](https://docs.docker.com/storage/volumes/#choose-the--v-or---mount-flag).

### 3. Initialize components
This step is necessary to create the database file, its structure, load initial data and perform the warm-up.
```bash
./utils/container.sh init
```

### 4. Executing bots

#### 4.a Through scheduled tasks
The definition of the scheduled tasks is done in the _utils/crontab.txt_ file.
Scheduled tasks are activated in the container with this command:
```bash
./utils/container.sh crontab
```

Or by starting the container with the initialized environment variable *APP_PRODUCTION_ENV*.

#### 4.b Manually
It is possible to force the manual execution of the bots with these commands:
```bash
./utils/container.sh stats
./utils/container.sh cm
```

### 5. Some support commands
You can open shells to the database or container by executing the following:
```bash
./utils/container.sh sqlite
./utils/container.sh shell
```


## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](https://github.com/jsanchez0x/mastodon_stats_bot/blob/main/LICENSE) file for details.


## Commercial License
For commercial use, a commercial license is available. Please contact me for more information.
