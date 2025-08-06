#!/bin/bash

# Путь на хосте, куда сохраняем дамп
BACKUP_PATH="/root/.../bot/db/backup.sql"

mkdir -p "$(dirname "$BACKUP_PATH")"

# Временный путь внутри контейнера
CONTAINER_PATH="/tmp/backup.sql"

# Сделать дамп внутри контейнера
docker exec <db_container_name> pg_dump -U postgres <db_name> -f "$CONTAINER_PATH"

# Копировать дамп с контейнера на хост
docker cp <db_container_name>:"$CONTAINER_PATH" "$BACKUP_PATH"

# (Необязательно) удалить временный файл в контейнере
docker exec <db_container_name> rm "$CONTAINER_PATH"
