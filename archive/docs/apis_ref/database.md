# Database Module Documentation

## Overview

The `database` module is responsible for managing database connections, creating tables, indexes, and performing specific database operations like inserting logs. It utilizes SQLAlchemy to interact with the database, allowing for efficient and secure execution of SQL queries. This module provides functions essential for setting up the database schema and maintaining logs for updates or operations performed on the database tables.

## Table of Contents

1. [Overview](#overview)
2. [Functions](#functions)
   - [get_engine](#get_engine)
   - [create_log_table](#create_log_table)
   - [insert_log](#insert_log)
   - [create_index](#create_index)
3. [Other Important Topics](#other-important-topics)
   - [Dependencies](#dependencies)
   - [Usage Considerations](#usage-considerations)
4. [Related Information](#related-information)

---

## Functions

### `get_engine`

**Description:**
Creates and returns a SQLAlchemy engine instance configured with the provided database connection details.

**Parameters:**
- `host` (str): The hostname or IP address of the database server.
- `port` (int): Port number on which the database server is running.
- `user` (str): Username for database authentication.
- `password` (str): Password for the database user.
- `database` (str): Name of the database to connect to.

**Returns:**
- `Engine`: A SQLAlchemy Engine object used for interacting with the database.

---

### `create_log_table`

**Description:**
Creates a `log` table in the database if it does not already exist. This table stores update logs with details such as the table name, message, and timestamp.

**Parameters:**
- `engine` (Engine): A SQLAlchemy Engine instance used to connect to the database.

**Returns:**
- `None`

**Example Schema for `log` Table**:
```plaintext
id          INT           AUTO_INCREMENT PRIMARY KEY
update_table VARCHAR(20)  NOT NULL
message      TEXT          NOT NULL
created_at   TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
```

---

### `insert_log`

**Description:**
Inserts a new log entry into the `log` table. The log entry includes a message, the name of the table being updated, and a timestamp.

**Parameters:**
- `engine` (Engine): A SQLAlchemy Engine instance used to connect to the database.
- `table_name` (str): The name of the table being updated.
- `message` (str): A message describing the update.

**Returns:**
- `None`

---

### `create_index`

**Description:**
Creates indexes on specific columns of a specified table in the database. Ensures that indexes are only created if they do not already exist.

**Parameters:**
- `engine` (Engine): A SQLAlchemy Engine instance used to connect to the database.
- `table_name` (str): The name of the table on which indexes are to be created.

**Additional Details:**
- The function targets specific columns (`trade_date`, `f_ann_date`, `end_date`, `ts_code`) for indexing.
- It ensures unique index names (e.g., `idx_<table_name>_<column_name>`) are assigned.
- The function handles column constraints such as modifying the `ts_code` column to ensure compatibility for indexing.

**Returns:**
- `None`

---

## Other Important Topics

### Dependencies

This module makes use of the following packages:
- `SQLAlchemy`: A Python SQL toolkit and ORM for database interaction.
- `pymysql`: A pure-Python MySQL client for connecting to MySQL databases.

Install the dependencies using pip:
```bash
pip install sqlalchemy pymysql
```

---

### Usage Considerations

- **Database Configuration:** Ensure the host, port, user credentials, and database name are valid and accessible from the environment where the module is being used.
- **Error Handling:** Implement proper error handling mechanisms when invoking these functions, especially for `create_index` and `insert_log`, as improper usage may lead to SQL-related exceptions.
- **Security:** Avoid using string concatenation for SQL queries. The current version has examples like `f"INSERT INTO..."`. Instead, utilize parameterized queries to prevent SQL injection vulnerabilities.

---

## Related Information

This module is designed to work alongside other modules, such as `queries.py` (for executing database queries) and `download.py` (for data fetching and updating operations). According to the sibling `__init__.py`, the `database` module functions are integrated with:

- `download.download`
- `download.update_by_date`
- `download.update_by_code`

These integrations make it easier to set up a full workflow involving data storage and logging.

---

This concludes the documentation for the `database` module. For further details or troubleshooting, please refer to the repository's guidelines or reach out to your administrator.