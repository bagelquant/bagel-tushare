"""
Author: Yanzhong(Eric) Huang

This module is the queries used in downloading/update process

For "date loop update", the loop will loop through the trade_date 
from the latest date in the corresponding table to the current date.

For "code loop update", the loop will loop through the all the ts_code,
each ts_code we need to update from the latest date to current date.

In this module, we will have the queries for both of them.

- query_latest_trade_date_by_table_name
- query_latest_trade_date_by_ts_code
"""
from datetime import datetime
from sqlalchemy.engine import Engine
from sqlalchemy.sql import text
from sqlalchemy.exc import ProgrammingError


def query_latest_trade_date_by_table_name(engine: Engine,
                                          table_name: str) -> datetime | None:
    """
    Queries the latest trade_date from a given table.

    :param engine: SQLAlchemy Engine instance used to connect to the database.
    :param table_name: The name of the table to query.
    :return: The latest trade_date.
    """
    query = text(f'SELECT MAX(trade_date) as latest_date FROM {table_name}')
    try:
        with engine.connect() as conn:
            latest_date: datetime = conn.execute(query).fetchone()[0]  # type: ignore
            return latest_date if latest_date else None
    except ProgrammingError:
        # table not created yet
        return None


def query_latest_f_ann_date_by_ts_code(engine: Engine,
                            table_name: str,
                            ts_code: str) -> datetime | None:
    """
    Queries the latest financial announcement date from the specified table.
    This function connects to the database using the provided SQLAlchemy engine,
    runs a query to fetch the maximum value of the `f_ann_date` field from the
    given table, and returns the result as a datetime object. If the query fails
    or the result is None, the function returns None.

    :param ts_code:
    :param engine: The SQLAlchemy engine to use for connecting to the database.
    :param table_name: The name of the table from which to query the latest
        financial announcement date.
    :return: The latest financial announcement date as a datetime object, or None
        if no date is available or an error occurs.
    :raises ProgrammingError: If there is an issue executing the query.
    """
    query = text(f"""
    SELECT MAX(f_ann_date) as latest_date 
    FROM {table_name} 
    WHERE ts_code = "{ts_code}"
    """)
    try:
        with engine.connect() as conn:
            latest_date: datetime = conn.execute(query).fetchone()[0]  # type: ignore
            return latest_date if latest_date else None
    except ProgrammingError:
        return None


def query_latest_ann_date_by_ts_code(engine: Engine,
                                     table_name: str,
                                     ts_code: str) -> datetime | None:
    """
    Queries the latest announcement date (ann_date) for a given ts_code from a specified table.

    :param engine: SQLAlchemy Engine instance used to connect to the database.
    :param table_name: The name of the table to query.
    :param ts_code: The ts_code to filter the query.
    :return: The latest ann_date for the given ts_code, or None if not found or error.
    """
    query = text(f"""
    SELECT MAX(ann_date) as latest_date
    FROM {table_name}
    WHERE ts_code = :ts_code
    """)
    try:
        with engine.connect() as conn:
            latest_date: datetime = conn.execute(query, {"ts_code": ts_code}).fetchone()[0]  # type: ignore
            return latest_date if latest_date else None
    except ProgrammingError:
        return None

def query_latest_trade_date_by_ts_code(engine: Engine,
                                       table_name: str,
                                       ts_code: str) -> datetime | None:
    """
    Queries the latest trade_date for a given ts_code from a specified table.

    :param engine: SQLAlchemy Engine instance used to connect to the database.
    :param table_name: The name of the table to query.
    :param ts_code: The ts_code to filter the query.
    :return: The latest trade_date for the given ts_code.
    """
    query = text(f"SELECT MAX(trade_date) as latest_date FROM {table_name} WHERE ts_code = {ts_code}")
    try:
        with engine.connect() as conn:
            latest_date: datetime = conn.execute(query, {"ts_code": ts_code}).fetchone()[0]  # type: ignore
            print(f'Latest trade date for {ts_code}: {latest_date}, table: {table_name}, ts_code: {ts_code}')
            return latest_date if latest_date else None
    except ProgrammingError:
        return None


def query_trade_cal(engine: Engine,
                    start_date: datetime,
                    end_date: datetime) -> list[datetime]:
    """
    Query trade calendar dates from the database.

    This function retrieves financial trading calendar dates from a database
    using the provided SQLAlchemy engine. The returned dates indicate the
    specific calendar days of trading activities.

    :param engine: SQLAlchemy database engine used to connect to the database.
    :param start_date: The starting date for the calendar query.
    :param end_date: The ending date for the calendar query.
    :return: A list of datetime objects representing trading calendar dates.
    """
    query = text(f"""
    SELECT cal_date FROM trade_cal 
    WHERE is_open = 1 
    AND cal_date BETWEEN "{start_date.strftime('%Y-%m-%d')}" AND "{end_date.strftime('%Y-%m-%d')}"
    ORDER BY cal_date
    """)
    with engine.connect() as conn:
        cal_dates = conn.execute(query).fetchall()
        return [_[0] for _ in cal_dates] if cal_dates else []


def query_code_list(engine: Engine) -> list[str]:
    """
    Fetches a list of stock codes from the stock_basic table using the provided database engine.

    The function performs a SQL query to extract the `ts_code` column values from
    the `stock_basic` table. It establishes a connection to the database using the
    provided engine, executes the query, retrieves the results, and returns the
    list of stock codes. If no results are found, it returns an empty list.

    :param engine: The SQLAlchemy Engine instance for connecting to the database.
    :return: A list of stock codes extracted from the `stock_basic` table.
    """
    query = text('SELECT ts_code FROM stock_basic')
    with engine.connect() as conn:
        ts_codes = conn.execute(query).fetchall()
        return [_[0] for _ in ts_codes] if ts_codes else []
