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

## Introduction

The Log Ingestion System is designed to efficiently handle log data, providing scalable log ingestion, real-time indexing, and a powerful query interface. Whether you need to store, search, or analyze logs, this system provides a robust solution.

## Features

- **Log Ingestion:** Ingest log entries in JSON format, storing them in a PostgreSQL database.
- **Scalability:** Implement database indexing, sharding, and consider distributed systems for large-scale deployments.
- **Query Interface:** Web-based or CLI interface with full-text search, field-based filtering, and support for date ranges.
- **Advanced Features (Bonus):** Regular expression search, role-based access control, real-time log ingestion, and searching.

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

## Usage

1. Use a tool like Postman to send log entries to the `/ingest` endpoint.
2. Explore the query interface at `/query` for powerful log searching and filtering.

## API Endpoints

- **Log Ingestion Endpoint:**
  - POST `/ingest`: Ingest log entries in JSON format.

- **Query Interface:**
  - GET `/query`: Search and filter log entries based on various criteria.

## Advanced Features

- **Search within Date Ranges:** Utilize date range filtering for log entries.
- **Regular Expression Search:** Perform complex pattern matching on log messages.
- **Role-Based Access Control (RBAC):** Implement user authentication and authorization.
- **Real-Time Log Ingestion and Searching:** Achieve up-to-date search results with real-time capabilities.

