# for_download Module Documentation

## Overview
The `for_download` module provides utility functions for database queries, specifically designed to facilitate data updates from financial datasets. It handles two main scenarios:
1. Looping through trade dates (e.g., "date loop update") to process data sequentially from the last recorded date in the database to the most recent date.
2. Looping through unique codes (e.g., `ts_code`) to perform updates per code for a specified time range.

The module makes use of SQLAlchemy to connect to and query a database. The provided functions are robust against missing tables or missing data in database tables, returning consistent outputs (e.g., `None` or empty lists) when no data is found.

## Table of Contents
1. [Functions](#functions)
   - [query_latest_trade_date_by_table_name](#query_latest_trade_date_by_table_name)
   - [query_latest_trade_date_by_ts_code](#query_latest_trade_date_by_ts_code)
   - [query_latest_f_ann_date_by_ts_code](#query_latest_f_ann_date_by_ts_code)
   - [query_trade_cal](#query_trade_cal)
   - [query_code_list](#query_code_list)
2. [Error Handling](#error-handling)
3. [Dependencies and Prerequisites](#dependencies-and-prerequisites)
4. [Examples of Usage](#examples-of-usage)

---

## Functions

### query_latest_trade_date_by_table_name
**Definition:**
```python
def query_latest_trade_date_by_table_name(engine: Engine, table_name: str) -> datetime | None:
```

Queries the latest trade date from a specific table.

- **Parameters:**
  - `engine`: An SQLAlchemy `Engine` instance for database connection.
  - `table_name` (`str`): The name of the database table.
  
- **Returns:** A `datetime` object representing the latest trade date, or `None` if the table is not found or contains no data.

---

### query_latest_trade_date_by_ts_code
**Definition:**
```python
def query_latest_trade_date_by_ts_code(engine: Engine, table_name: str, ts_code: str) -> datetime | None:
```

Fetches the latest trade date for a given `ts_code` from the specified table.

- **Parameters:**
  - `engine`: An SQLAlchemy `Engine` instance for database connection.
  - `table_name` (`str`): The name of the database table.
  - `ts_code` (`str`): The unique stock code to filter the query.

- **Returns:** A `datetime` object representing the latest trade date for the code, or `None` if no data is found.

---

### query_latest_f_ann_date_by_ts_code
**Definition:**
```python
def query_latest_f_ann_date_by_ts_code(engine: Engine, table_name: str, ts_code: str) -> datetime | None:
```

Queries the latest financial announcement date for a specific `ts_code` from a given table.

- **Parameters:**
  - `engine`: An SQLAlchemy `Engine` instance for database connection.
  - `table_name` (`str`): The name of the table to query.
  - `ts_code` (`str`): The unique stock code.

- **Returns:** A `datetime` object representing the latest financial announcement date or `None` if no relevant data is found.

---

### query_trade_cal
**Definition:**
```python
def query_trade_cal(engine: Engine, start_date: datetime, end_date: datetime) -> list[datetime]:
```

Fetches the list of trading calendar dates within a specified range.

- **Parameters:**
  - `engine`: An SQLAlchemy `Engine` instance for database connection.
  - `start_date` (`datetime`): Start of the date range.
  - `end_date` (`datetime`): End of the date range.

- **Returns:** A `list` of `datetime` objects representing the trading dates, or an empty list if no dates fall within the range.

---

### query_code_list
**Definition:**
```python
def query_code_list(engine: Engine) -> list[str]:
```

Retrieves a list of stock codes (`ts_code`) from the `stock_basic` table.

- **Parameters:**
  - `engine`: An SQLAlchemy `Engine` instance for database connection.

- **Returns:** A `list` of strings representing stock codes, or an empty list if the table contains no data.

---

## Error Handling
- If an SQL query encounters a missing table or invalid filters (e.g., non-existent `ts_code`, invalid `table_name`), the functions return `None` or an empty list, depending on context.
- The `query_latest_trade_date_by_table_name` and `query_latest_f_ann_date_by_ts_code` handle SQL exceptions (e.g., `ProgrammingError`) gracefully, preventing application crashes.

---

## Dependencies and Prerequisites
- **Python Version:** Requires Python 3.12 or newer.
- **Installed Packages:**
  - `SQLAlchemy`: For database connections and query execution.
  - `datetime`: For handling date and time-related data.

Ensure that an SQL database is accessible with the required tables (`stock_basic`, `trade_cal`, etc.) for the functions to work. Example configuration for connecting to a database is provided in the `test_config.json` file.

---

## Examples of Usage

### Query Latest Trade Date from Table
```python
from for_download import query_latest_trade_date_by_table_name
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://user:password@host/database")
latest_date = query_latest_trade_date_by_table_name(engine, "daily")
print(f"Latest Trade Date: {latest_date}")
```

### Query Trade Calendar
```python
from for_download import query_trade_cal
from sqlalchemy import create_engine
from datetime import datetime

engine = create_engine("mysql+pymysql://user:password@host/database")
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)
trade_dates = query_trade_cal(engine, start_date, end_date)

print("Trade Dates:")
for date in trade_dates:
    print(date)
```

---

## Other Important Topics

### Database Configuration
- The module expects a database connection string or an SQLAlchemy `Engine` instance.
- Example configuration in `test_config.json`:
  ```json
  {
    "database": {
      "host": "localhost",
      "port": 3306,
      "user": "root",
      "password": "password",
      "database": "test_tushare"
    }
  }
  ```

### Testing
Test cases for database-related functionality can be created using Python's `unittest` module, as demonstrated in the `test_database.py` file.

Example test for inserting logs:
```python
def test_insert_log(self):
    engine = get_engine(**self.config)
    create_log_table(engine)
    
    insert_log(engine, "table_name", "Log message")
    logs = query_log_entries(engine, "table_name")
    self.assertGreater(len(logs), 0)
```