#!/bin/bash

until PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U $POSTGRES_USER -d $POSTGRES_DB -c '\q'; do
  sleep 1
done

if ! PGPASSWORD=$POSTGRES_PASSWORD psql -h db -U $POSTGRES_USER -d $POSTGRES_DB -c "\dt alembic_version" | grep -q alembic_version; then
    echo "Applying database migrations..."
    alembic upgrade head
fi

exec "$@"