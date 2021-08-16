#!/bin/bash

set -e
echo "from postgres init"
echo $POSTGRES_USER
echo $DB_USER
psql -v ON_ERROR_STOP=1 --username "db_user" <<-EOSQL
    CREATE USER db_user WITH ENCRYPTED PASSWORD 'qwerty';
    CREATE DATABASE app2 OWNER db_user;
    \c app2
    CREATE EXTENSION IF NOT EXISTS pgcrypto;
EOSQL
