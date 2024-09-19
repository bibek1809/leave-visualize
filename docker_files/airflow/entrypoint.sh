#!/bin/sh

# Initialize the Airflow database
airflow db init

# Create an Airflow admin user
airflow users create \
    -r Admin \
    -u admin \
    -e admin@gmail.com \
    -f admin \
    -l user \
    -p admin

# Start the Airflow webserver
exec airflow webserver

