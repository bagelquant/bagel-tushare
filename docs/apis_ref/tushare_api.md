# Tushare API Wrapper Documentation

## Overview

This documentation provides a comprehensive guide for using the **Tushare API wrapper** and other related modules. The Tushare API is a financial data platform offering a wide range of data, including stock market data, fund flows, macroeconomic data, and industry data. The `tushare_api.py` module is a convenient wrapper for interacting with the Tushare API, providing functions for retrieving stock data effortlessly.

Additionally, related modules like `database.py` are included in this documentation to understand how to store, manage, and optimize the data retrieved from Tushare.

## Table of Contents

1. [Overview](#overview)
2. [Functions](#functions)
   - [tushare_download](#tushare_download)
   - [get_engine](#get_engine)
   - [create_log_table](#create_log_table)
   - [insert_log](#insert_log)
   - [create_index](#create_index)
3. [Important Topics](#important-topics)
   - [Connecting to Databases](#connecting-to-databases)
   - [Indexing and Optimization](#indexing-and-optimization)
   - [Error Handling in API Calls](#error-handling-in-api-calls)
   - [Extending Functionality](#extending-functionality)

---

## Functions

### `tushare_download`

Downloads financial data using the Tushare API.

#### Parameters:
- `token` (str): Authentication token to access the Tushare API.
- `api_name` (str): The name of the Tushare API endpoint to call.
- `params` (dict | None): (Optional) Dictionary of query parameters for the API.
- `fields` (list[str] | None): (Optional) List of fields to retrieve from the API.

#### Returns:
- `pandas.DataFrame | None`: A dataframe containing the retrieved data or `None` if no data is available.

#### Usage Example:
```python
from tushare_api import tushare_download

data = tushare_download(
    token="YOUR_TUSHARE_TOKEN",
    api_name="daily",
    params={"ts_code": "000001.SZ", "start_date": "20220101", "end_date": "20220131"},
    fields=["trade_date", "open", "high", "low", "close", "volume"]
)
print(data)
```

---

### `get_engine`

Establishes a connection to a database using SQLAlchemy.

#### Parameters:
- `host` (str): Database server hostname.
- `port` (int): Port number for the database connection.
- `user` (str): Database username.
- `password` (str): Database user password.
- `database` (str): Name of the database to connect to.

#### Returns:
- `Engine`: SQLAlchemy engine instance for connecting to the database.

#### Usage Example:
```python
from database import get_engine

engine = get_engine(
    host="127.0.0.1",
    port=3306,
    user="username",
    password="password",
    database="my_database"
)
```

---

### `create_log_table`

Creates a `log` table to store updates and logs related to operations.

#### Parameters:
- `engine` (Engine): SQLAlchemy engine instance.

#### Returns:
- `None`

#### Usage Example:
```python
from database import create_log_table

create_log_table(engine)
```

---

### `insert_log`

Logs an entry into the `log` table.

#### Parameters:
- `engine` (Engine): SQLAlchemy engine instance.
- `table_name` (str): The name of the table being logged.
- `message` (str): Log message.

#### Returns:
- `None`

#### Usage Example:
```python
from database import insert_log

insert_log(engine, table_name="daily_data", message="Data updated successfully.")
```

---

### `create_index`

Creates indices on specified columns of a table to optimize database queries.

#### Parameters:
- `engine` (Engine): SQLAlchemy engine instance.
- `table_name` (str): Name of the table to index.

#### Returns:
- `None`

#### Usage Example:
```python
from database import create_index

create_index(engine, table_name="daily_data")
```

---

## Important Topics

### Connecting to Databases

The `get_engine` function in the `database.py` module provides a simple way to establish a connection to a MySQL database using SQLAlchemy. Always store sensitive credentials securely (e.g., environment variables) when using this function.

### Indexing and Optimization

The `create_index` function ensures key columns are indexed in the database to improve query performance. It dynamically checks the table's structure and existing indices before creating new ones. This is particularly important for tables with large datasets, such as stock market data.

### Error Handling in API Calls

The `tushare_download` function should be wrapped in appropriate error handling mechanisms. For instance:
- Handle cases where the API quota is exhausted.
- Log errors for failed API calls using the `insert_log` function.
- Validate API responses to ensure data consistency.

Example of adding basic error handling:
```python
try:
    data = tushare_download(token=my_token, api_name="daily", params=my_params)
    if data is None:
        raise ValueError("No data returned from API.")
except Exception as e:
    print(f"Error: {e}")
    insert_log(engine, table_name="error_logs", message=str(e))
```

### Extending Functionality

The modules in this project are designed to be modular and extensible. You can add new APIs from Tushare by passing appropriate `api_name` and `params` to the `tushare_download` function.

For additional database operations, you can extend the `database.py` module by introducing functions for:
- Data cleanup.
- Table creation for custom datasets.
- Generating detailed reports.

---

## Conclusion

This documentation provides a comprehensive guide for integrating financial data from Tushare with database systems. By combining the functions in `tushare_api.py` and `database.py`, users can effectively retrieve, store, and optimize large volumes of market data for analysis and reporting.

Feel free to adapt the provided functions to suit your specific needs, and consult Tushare's official documentation for detailed information on available APIs and their parameters.