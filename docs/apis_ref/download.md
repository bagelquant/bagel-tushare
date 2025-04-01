# Download and Update Module Documentation

## Overview

This module provides functionalities for downloading and updating database tables from external APIs, particularly focusing on Tushare-based financial data. The module handles downloading new data, converting date fields, updating records by specific criteria (e.g., dates or codes), and logging errors encountered during these operations. 

The module also supports multiprocessing to improve performance when updating large datasets.

---

## Table of Contents

1. [Overview](#overview)
2. [Functions](#functions)
   - [_convert_date_column](#_convert_date_column)
   - [download](#download)
   - [_single_date_update](#_single_date_update)
   - [update_by_date](#update_by_date)
3. [Other Important Topics](#other-important-topics)
   - Error Logging
   - Multiprocessing Parallelism
   - Retry Mechanism

---

## Functions

### `_convert_date_column`

**Description**:  
Converts specific columns in a pandas DataFrame to datetime format. Handles columns like `trade_date`, `cal_date`, `pretrade_date`, etc.

**Signature**:
```python
def _convert_date_column(df: pd.DataFrame) -> pd.DataFrame:
```

**Parameters**:
- `df` (`pd.DataFrame`): Input DataFrame containing columns that need datetime conversion.

**Returns**:
- `pd.DataFrame`: The modified DataFrame with date columns set to pandas datetime format.

**Example**:
```python
df = _convert_date_column(dataframe)
```

---

### `download`

**Description**:  
Downloads data from an API and replaces the database table with the new data.

**Signature**:
```python
def download(engine: Engine, token: str, api_name: str, params: dict | None = None, fields: list[str] | None = None, retry: int = 3) -> None:
```

**Parameters**:
- `engine` (`Engine`): SQLAlchemy database engine.
- `token` (`str`): API token for authentication.
- `api_name` (`str`): API name to fetch data from.
- `params` (`dict` or `None`): Additional parameters for the API request.
- `fields` (`list[str]` or `None`): Specific fields to fetch from the API.
- `retry` (`int`): Number of retry attempts for failed operations (default: 3).

**Returns**:
- `None`

**Example**:
```python
download(engine, token="YOUR_API_TOKEN", api_name="stock_daily", params={"trade_date": "20231025"})
```

---

### `_single_date_update`

**Description**:  
Updates the database for a specific date by downloading data from the API and appending it to the database.

**Signature**:
```python
def _single_date_update(engine_url: str, token: str, api_name: str, trade_date: datetime, params: dict | None = None, fields: list[str] | None = None, retry: int = 3) -> None:
```

**Parameters**:
- `engine_url` (`str`): Database engine URL.
- `token` (`str`): Authentication token for accessing the API.
- `api_name` (`str`): API name to download data from.
- `trade_date` (`datetime`): Target date for updating data.
- `params` (`dict` or `None`): Optional query parameters.
- `fields` (`list[str]` or `None`): Optional fields to retrieve.
- `retry` (`int`): Retry attempts for failed downloads (default: 3).

**Returns**:
- `None`

**Example**:
```python
_single_date_update(engine.url, token, "stock_daily", trade_date=datetime(2023, 10, 25))
```

---

### `update_by_date`

**Description**:  
Bulk updates the database by iterating through trade dates and processing data in parallel.

**Signature**:
```python
def update_by_date(engine: Engine, token: str, api_name: str, params: dict | None = None, fields: list[str] | None = None, end_date: datetime = datetime.now(), max_workers: int = 10, retry: int = 3) -> None:
```

**Parameters**:
- `engine` (`Engine`): Database engine for querying and updates.
- `token` (`str`): API authentication token.
- `api_name` (`str`): API name for fetching data.
- `params` (`dict` or `None`): Additional API query parameters.
- `fields` (`list[str]` or `None`): API response fields to fetch.
- `end_date` (`datetime`): The end date for the updates (default: `datetime.now()`).
- `max_workers` (`int`): Maximum parallel workers for multiprocessing (default: 10).
- `retry` (`int`): Maximum retries for failed API calls (default: 3).

**Returns**:
- `None`

**Example**:
```python
update_by_date(engine, token, "stock_daily", end_date=datetime(2023, 10, 31))
```

---

## Other Important Topics

### Error Logging

The module logs errors encountered during API requests and database updates to ensure traceability. It uses the `insert_log` function to record errors in a specific table for debugging purposes.

### Multiprocessing Parallelism

Functions like `update_by_date` use Python's `ProcessPoolExecutor` to utilize multiple processor cores for handling large datasets efficiently. Each process creates a separate database connection to avoid concurrency issues.

### Retry Mechanism

Wherever applicable, the module implements retry mechanisms to attempt failed operations (e.g., API requests) up to a specified number (`retry` argument). Between retries, the function waits (e.g., 60 seconds) before retrying.

---

## Conclusion

This module is a powerful tool for managing financial data from Tushare APIs and updating databases efficiently. Features such as automated error logging, date-based updates, and multiprocessing make it highly effective for financial data pipelines.