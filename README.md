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

## API Documentation

You can view the API documentation by following this link:

[Swagger Documentation](./templates/swagger.html)

## Folder Structure

- `docs/`: Contains the Swagger documentation and other related resources.

