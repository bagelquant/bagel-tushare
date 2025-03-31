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

from sqlalchemy.engine import Engine
from sqlalchemy.sql import text
from datetime import datetime


def query_latest_trade_date_by_table_name(engine: Engine,
                                          table_name: str) -> datetime | None:
    """
    Queries the latest trade_date from a given table.

    :param engine: SQLAlchemy Engine instance used to connect to the database.
    :param table_name: The name of the table to query.
    :return: The latest trade_date.
    """
    query = text(f"SELECT MAX(trade_date) as latest_date FROM {table_name}")
    with engine.connect() as conn:
        latest_date: datetime = conn.execute(query).fetchone()[0]
        return latest_date if latest_date else None


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
    query = text(f"SELECT MAX(trade_date) as latest_date FROM {table_name} WHERE ts_code = :ts_code")
    with engine.connect() as conn:
        latest_date: datetime = conn.execute(query, {"ts_code": ts_code}).fetchone()[0]
        return latest_date if latest_date else None


def query_trade_cal(engine: Engine) -> list[datetime]:
    """
    Query trade calendar dates from the database.

    This function retrieves financial trading calendar dates from a database
    using the provided SQLAlchemy engine. The returned dates indicate the
    specific calendar days of trading activities.

    :param engine: SQLAlchemy database engine used to connect to the database.
    :return: A list of datetime objects representing trading calendar dates.
    """
    query = text("SELECT cal_date FROM trade_cal")
    with engine.connect() as conn:
        cal_dates = conn.execute(query).fetchall()
        return sorted([_[0] for _ in cal_dates] if cal_dates else [])
