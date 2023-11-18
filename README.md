# Log Ingestion System

The Log Ingestion System is a scalable solution for handling and querying log data efficiently. It includes features for log ingestion, real-time indexing, and a powerful query interface.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Advanced Features](#advanced-features)
- [Limitations](#limitations)

## Introduction

The Log Ingestion System is designed to efficiently handle log data, providing scalable log ingestion, real-time indexing, and a powerful query interface. Whether you need to store, search, or analyze logs, this system provides a robust solution.

## Features

- **Log Ingestion:** Ingest log entries in JSON format, storing them in a PostgreSQL database.
- **Scalability:** Implement database indexing, sharding, and consider distributed systems for large-scale deployments.
- **Query Interface:** Web-based or CLI interface with full-text search, field-based filtering, and support for date ranges.
- **Advanced Features (Bonus):** Real-time log ingestion, and searching, handles auto-push.

## Tech Stack

- Python
- Flask
- SQLAlchemy
- PostgreSQL

## Getting Started

### Prerequisites

Ensure you have the following prerequisites installed:

- Python
- PostgreSQL
- Check requirements.txt

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/ayush06092002/my_log_system
    cd my_log_system
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Set up PostgreSQL database:

    - Create a database named `log_ingestion_db`.
    - Configure database connection details in postgres cli
    -   CREATE DATABASE log_ingestion_db;
        CREATE USER log_user WITH PASSWORD 'ayush';
        ALTER ROLE log_user SET client_encoding TO 'utf8';
        ALTER ROLE log_user SET default_transaction_isolation TO 'read committed';
        ALTER ROLE log_user SET timezone TO 'UTC';
        GRANT ALL PRIVILEGES ON DATABASE log_ingestion_db TO log_user;
        GRANT USAGE, CREATE ON SCHEMA public TO log_user;


4. Run the application:

    ```bash
    python app.py
    ```
5. Push the logs from a file:

    - Run this script to push the data in log_data.json file
    - It pushes the logs at 'http://127.0.0.1:3000/ingest'
    ```bash
    python push.py
    ```

6. Auto generate logs and then push automatically:

    - It is a python script that generated random logs
    - Uses a python library 'faker' to generate random sentences
    ```bash
    python auto_push_generator.py
    ```


## Usage

1. Use a tool like Postman to send log entries to the `/ingest` endpoint.
2. Explore the query interface at `/query` for powerful log searching and filtering.
3. Use push.py to push logs from json file.
4. Use auto_push_generator.py to push auto generated logs.


## API Endpoints

- **Log Ingestion Endpoint:**
  - POST `/ingest`: Ingest log entries in JSON format.

- **Log Query Endpoint:**
  - GET `/query`: Query log entries.

- **Query Interface:**
  - GET `/query_ui`: Search and filter log entries based on various criteria.

## Advanced Features

- **Search within Date Ranges:** Utilize date range filtering for log entries.
- **Regular Expression Search:** Perform complex pattern matching on log messages.
- **Auto Push:** Included a script to push auto generated logs for testing.
- **Real-Time Log Ingestion and Searching:** Achieve up-to-date search results with real-time capabilities.

## Limitations

- **Wrong search results for '12:00:00 AM'** When entering 12:00:00 as the search time, it makes it 00:00:00