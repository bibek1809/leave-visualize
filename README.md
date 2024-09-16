# Leave Analysis Platform

## Overview

The Leave Analysis Platform automates the extraction, transformation, and loading (ETL) of leave and attendance data, offering real-time analytics and insights. It pulls data from external APIs, processes it into structured tables using Apache Airflow, and stores it in a MySQL database. The system supports scalable, secure, and robust operations with real-time data updates, customizable visualizations, and comprehensive reporting.

## Key Features

- **Data Upload & API Integration:** Supports bulk uploads and API-based data retrieval with authentication.
- **Employee Profile Management:** Extracts and manages employee profiles from raw data.
- **Leave Data Visualization:** Provides visualizations of leave trends, balances, and distributions.
- **Real-time Updates:** Ensures up-to-date information through scheduled ETL processes.
- **Custom Reporting:** Generates standard and custom reports, and offers insights into leave trends.

## System Architecture

- **Data Ingestion:** Uses parallel processing for efficient data retrieval and insertion.
- **Processing:** Applies threading for concurrent data transformation.
- **Storage:** Utilizes MySQL for raw and structured data management.

For deploying the Leave Analysis Platform, follow this step-by-step deployment process. The platform automates leave and attendance data ETL operations using Apache Airflow, MySQL, and a REST API. This guide covers how to set up, configure, and run the platform using Docker containers.
Prerequisites


Ensure you have the following installed:

    Docker
    Docker Compose
    Git

Deployment Process
1. Clone the Repository

First, clone the repository from your version control system:

bash

git clone https://github.com/lfbibek2024
cd leave-visualize

2. Configure the Environment

The repository includes a .env.example file for environment configuration. Copy it to a new .env file and fill in the necessary values:

bash

cp .env.example   .env

Update the following variables in the .env file:

    MYSQL_ROOT_PASSWORD
    MYSQL_DATABASE
    MYSQL_USER
    MYSQL_PASSWORD
    AIRFLOW_DATABASE

3. Build and Run the Application

The platform consists of multiple services defined in a docker-compose.yml file:

    Leave API: Runs on port 4448 to provide leave and attendance analytics.
    MySQL: Manages data storage.
    Airflow: Manages the ETL process via DAGs.

To build and start the services, use the following command:

bash

docker-compose up --build

This will:

    Build and start the Leave API on http://localhost:4448.
    Initialize MySQL with the environment variables from .env.
    Set up the Airflow webserver and scheduler.

4. Alembic Database Migrations

We use Alembic to handle database migrations. After starting the services, run the following command to apply all migrations and set up the database schema:

bash

docker exec -it leave-api alembic upgrade head

To downgrade the database to a previous version, use:

bash

docker exec -it leave-api alembic downgrade <revision_id>

You can view the migration history with:

bash

docker exec -it leave-api alembic history --verbose

5. Health Check

To verify that the Leave API is running, you can check the /health endpoint:

bash

curl http://localhost:4448/health

6. Access the Services

    Leave API: Accessible at http://localhost:4448.
    Airflow Web UI: Accessible at http://localhost:8080. Default credentials:
        Username: admin
        Password: admin
    MySQL: Accessible at localhost:3306 with the credentials defined in the .env file.

7. Logs and Monitoring

You can monitor real-time logs for all services with:

bash

docker-compose logs -f

8. Stopping and Cleaning Up

To stop the containers, use:

bash

docker-compose down

If you want to remove all associated volumes (such as the MySQL database), run:

bash

docker-compose down -v

9. Directory Structure

    docker_files/alembic/: Contains Alembic configuration files for managing database migrations.
    docker_files/sql/mysql_data/: Stores persistent MySQL data.
    docker_files/airflow/dags/: Location for Airflow DAGs to be executed.

Additional Information

    Airflow DAGs: Custom DAGs should be added in docker_files/airflow/dags/ to define your ETL workflows.
    API Documentation: Available via Swagger at http://localhost:4448/swagger.

## API Documentation

You can view the API documentation by following this link:

[Swagger Documentation](./docs/API_DOCUMENTS/swagger.pdf)

## Folder Structure

- `docs/`: Contains the Swagger documentation and other related resources.



