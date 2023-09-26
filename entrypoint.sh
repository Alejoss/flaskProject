#!/bin/bash
set -e

# Start the SQL Server
/opt/mssql/bin/sqlservr &
pid="$!"

# Run the SQL commands
/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "myPassw0rd" -d master -i /docker-entrypoint-initdb.d/init.sql

# Wait for SQL Server to finish
wait $pid
