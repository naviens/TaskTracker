#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER task_admin WITH PASSWORD 'mypasswd' LOGIN;
    CREATE DATABASE task_tracker with owner task_admin;
    GRANT ALL PRIVILEGES ON DATABASE task_tracker TO task_admin;
EOSQL
