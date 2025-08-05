"""
Download and update module
Author: Yanzhong(Eric) Huang

The entry point of the download and update process.

- `_convert_date_column` will convert the date column to datetime, including:
    - `trade_date`
    - `cal_date`
    - `pretrade_date`
    - `ann_date`
    - `f_ann_date`
    - `end_date`
- `download` function will replace the table
- `update_by_date` function will append to the table
    - `_update_single_date` will update a single date
    - it will multiprocess the `_update_single_date`
- `update_by_code function will append to the table
    - `_update_single_code` will update a single code
    - it will multiprocess the `_update_single_code`
"""


import pandas as pd
from time import sleep
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine, text
from datetime import datetime

from .tushare_api import tushare_download
from .database import insert_log
from .queries import (query_trade_cal,
                      query_latest_f_ann_date_by_ts_code,
                      query_latest_ann_date_by_ts_code,
                      query_latest_trade_date_by_table_name,
                      query_code_list)
from concurrent.futures import ProcessPoolExecutor


START_DATE = '20000101'  # default start date for data download


def _convert_date_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts specific columns in the provided DataFrame to datetime format.

    This function checks for the presence of specific date-related columns in
    the input DataFrame and converts them to pandas datetime format. The columns
    considered for conversion include "trade_date", "cal_date",
    "pretrade_date", "ann_date", "f_ann_date", and "end_date".

    :param df: The input DataFrame containing the columns to be converted to
        datetime format.
    :return: A DataFrame with the specified columns converted to datetime format.
    """
    date_columns = ['trade_date', 'cal_date', 'pretrade_date', 'ann_date', 'f_ann_date', 'end_date']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])
    return df


def download(engine: Engine,
             token: str,
             api_name: str,
             params: dict | None = None,
             fields: list[str] | None = None,
             retry: int = 3) -> None:
    """
    Downloads data from a specified API endpoint, processes the resulting data,
    and stores it in a database table. It handles errors gracefully by logging
    any issues encountered during the download or data processing steps.

    :param engine: A SQLAlchemy engine instance used for connecting to the database.
    :param token: The API authentication token required for accessing the API.
    :param api_name: The name of the API endpoint from which data is to be downloaded.
    :param params: A dictionary of optional parameters to be passed to the API request.
    :param fields: A list of fields to be fetched from the API response.
    :param retry: Retry times if download failed. Default is 3.
    :return: None.
    """
    try_count = 1
    try:
        df_new = tushare_download(token, api_name, params, fields)
        df_new = _convert_date_column(df_new)  # type: ignore

        # Read existing data from database
        try:
            df_existing = pd.read_sql_table(api_name, engine)
        except Exception:
            df_existing = pd.DataFrame()


        # Compare columns for new rows
        if api_name == 'stock_basic':
            compare_cols = ['ts_code']
        elif 'ts_code' in df_new.columns and 'trade_date' in df_new.columns:
            compare_cols = ['ts_code', 'trade_date']
        elif 'ts_code' in df_new.columns:
            compare_cols = ['ts_code']
        else:
            compare_cols = df_new.columns.tolist()

        if not df_existing.empty:
            merged = df_new.merge(df_existing, on=compare_cols, how='left', indicator=True, suffixes=('', '_dup'))
            df_to_insert = merged[merged['_merge'] == 'left_only']
            # Only keep columns from df_new (original columns, not _dup)
            df_to_insert = df_to_insert[df_new.columns]
        else:
            df_to_insert = df_new

        if not df_to_insert.empty:
            df_to_insert.to_sql(api_name, engine, if_exists='append', index=False)
            print(f'Inserted {len(df_to_insert)} new rows into {api_name}')
        else:
            print(f'No new rows to insert for {api_name}')
    except Exception as e:
        error_msg = f'Error downloading {api_name}: {e}'
        insert_log(engine, table_name=api_name, message=error_msg)

        # retry in 60s
        if try_count < retry:
            sleep(60)
            download(engine, token, api_name, params, fields, retry)
        else:
            print(f'Error downloading {api_name}, retry {retry} times, stop retrying')


def _single_date_update(engine_url: str,
                        token: str,
                        api_name: str,
                        trade_date: datetime,
                        params: dict | None = None,
                        fields: list[str] | None = None,
                        retry: int = 3) -> None:
    """
    Updates a single date entry for a given API by downloading the associated
    data and saving it to the database. It retries the operation in case of failure
    up to a specified number of times, logging errors as they occur.

    :param engine_url: URL of the database engine used to connect to the database.
    :param token: Authentication token required to access the API.
    :param api_name: Name of the API to fetch data from.
    :param trade_date: Date for which the data needs to be updated.
    :param params: Additional parameters to pass to the API request. Defaults to None.
    :param fields: Specific fields to fetch in the API response. Defaults to None.
    :param retry: Number of retry attempts in case of failure. Defaults to 3.
    :return: None
    """
    print(f'Updating {api_name} for {trade_date}')
    # create a new engine using existing engine (multiprocess needs separate engine)
    engine = create_engine(engine_url)

    if params is None:
        params = {}
    params['trade_date'] = trade_date.strftime('%Y%m%d')

    try_count = 0
    while try_count < retry:
        try:
            df = tushare_download(token, api_name, params, fields)
            df = _convert_date_column(df)  # type: ignore
            df.to_sql(api_name, engine, if_exists='append', index=False)
            break
        except Exception as e:
            print(f'Error downloading {api_name} for {trade_date}: {e}, retrying...')
            try_count += 1
            if try_count < retry:
                sleep(60)
            else:
                error_msg = f'Error downloading {api_name} for {trade_date}: {e}'
                insert_log(engine, table_name=api_name, message=error_msg)
                print(f'Error downloading {api_name} for {trade_date}, retried {retry} times, giving up.')
        finally:
            engine.dispose()


def update_by_date(engine: Engine,
                   token: str,
                   api_name: str,
                   params: dict | None = None,
                   fields: list[str] | None = None,
                   end_date: datetime = datetime.now(),
                   max_workers: int = 10,
                   retry: int = 3) -> None:
    """
    Updates data from an API by iterating through trade dates and processing them in parallel.

    This function updates data from a given API in the database by finding trade dates
    between the latest database entry and the provided end date. It uses a
    `ProcessPoolExecutor` to process the dates in parallel for performance optimization.

    :param engine: The database engine used to execute queries and perform updates.
    :param token: The authentication token required to access the API.
    :param api_name: The name of the API from which the data is being fetched.
    :param params: Optional dictionary of additional parameters to be sent in the query.
    :param fields: Optional list of specific fields to retrieve from the API.
    :param end_date: The ending date for the data update. Defaults to the current datetime.
    :param max_workers: The maximum number of parallel workers to process trade dates. Defaults to 10.
    :param retry: Number of retry attempts for failed API calls. Defaults to 3.
    :return: This function returns nothing.
    """
    # latest date in database
    latest_date = query_latest_trade_date_by_table_name(engine, api_name)

    # Ensure latest_date and end_date are pandas Timestamps for comparison and arithmetic
    latest_date = pd.to_datetime(latest_date) if latest_date is not None else pd.to_datetime(START_DATE)
    latest_date = latest_date + pd.Timedelta(days=1)

    end_date = pd.to_datetime(end_date)

    if end_date < latest_date:
        print(f'{api_name} already up to date')
        return

    # trade_cal
    trade_cal = query_trade_cal(engine, start_date=latest_date, end_date=end_date)

    print(f'Start updating {api_name} from {latest_date} to {end_date}')
    # multiprocess loop
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        engine_urls = [engine.url for _ in trade_cal]
        tokens = [token for _ in trade_cal]
        api_names = [api_name for _ in trade_cal]
        params_list = [params for _ in trade_cal]
        fields_list = [fields for _ in trade_cal]
        retries = [retry for _ in trade_cal]

        list(executor.map(_single_date_update,
                               engine_urls,
                               tokens,
                               api_names,
                               trade_cal,
                               params_list,
                               fields_list,
                               retries))


    print(f'Finished updating {api_name} from {latest_date} to {end_date}')


def _single_update_by_code(engine_url: str,
                           token: str,
                           api_name: str,
                           ts_code: str,
                           end_date: datetime,
                           params: dict | None = None,
                           fields: list[str] | None = None,
                           retry: int = 3,
                           date_field: str | None = None) -> None:
    """
    Updates a single stock code entry for a given API by downloading the associated
    data and saving it to the database. Retries the operation in case of failure
    up to a specified number of times, logging errors as they occur.

    :param engine_url: URL of the database engine used to connect to the database.
    :param token: Authentication token required to access the API.
    :param api_name: Name of the API to fetch data from.
    :param ts_code: Stock code for which the data needs to be updated.
    :param params: Additional parameters to pass to the API request. Defaults to None.
    :param fields: Specific fields to fetch in the API response. Defaults to None.
    :param retry: Number of retry attempts in case of failure. Defaults to 3.
    :return: None
    """
    # Create a new engine using existing engine_url (multiprocess requires separate engine)
    engine = create_engine(engine_url)

    # Determine latest date for this code using the selected date_field
    if date_field == 'f_ann_date':
        latest_date = query_latest_f_ann_date_by_ts_code(engine, table_name=api_name, ts_code=ts_code)
    elif date_field == 'ann_date':
        latest_date = query_latest_ann_date_by_ts_code(engine, table_name=api_name, ts_code=ts_code)
    elif date_field == 'trade_date':
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT MAX(trade_date) FROM {api_name} WHERE ts_code = :ts_code"), {"ts_code": ts_code})
            latest_date = result.scalar()
    else:
        latest_date = None

    if latest_date is None:
        start_date = START_DATE
    else:
        latest_date = pd.to_datetime(latest_date)
        start_date = (latest_date + pd.Timedelta(days=1)).strftime("%Y%m%d")

    print(f'Updating {api_name} for {ts_code} from {start_date} to {end_date.strftime('%Y%m%d')} (using {date_field})')
    try_count = 0
    if params is None:
        params = {}
    params['ts_code'] = ts_code
    params['start_date'] = start_date
    params['end_date'] = end_date.strftime('%Y%m%d')

    while try_count <= retry:
        try:
            df = tushare_download(token, api_name, params, fields)
            df = _convert_date_column(df)  # type: ignore
            df.to_sql(api_name, engine, if_exists='append', index=False)
            break
        except Exception as e:
            print(f'Error downloading {api_name} for {ts_code}: {e}, retrying...')
            try_count += 1
            if try_count < retry:
                sleep(60)
            else:
                error_msg = f'Error downloading {api_name} for {ts_code}: {e}'
                insert_log(engine, api_name, error_msg)
                print(f'Error downloading {api_name} for {ts_code}, retried {retry} times, giving up.')
        finally:
            engine.dispose()


def update_by_code(engine: Engine,
                   token: str,
                   api_name: str,
                   params: dict | None = None,
                   fields: list[str] | None = None,
                   end_date: datetime = datetime.now(),
                   max_workers: int = 10,
                   retry: int = 3) -> None:
    """
    Updates data for stock codes from an API by processing them in parallel.

    This function retrieves stock codes from the database with the latest trading date 
    and processes updates using a `ProcessPoolExecutor` to optimize performance.

    :param engine: The database engine used to execute queries and perform updates.
    :param token: The authentication token required to access the API.
    :param api_name: The name of the API from which the data is being fetched.
    :param params: Optional dictionary of additional parameters to be sent in the query.
    :param fields: Optional list of specific fields to retrieve from the API.
    :param end_date: The ending date for the data update. Defaults to the current datetime.
    :param max_workers: The maximum number of parallel workers to process trade dates.
        Defaults to 10.
    :param retry: Number of retry attempts for failed API calls. Defaults to 3.
    :return: This function returns nothing.
    """
    # get codes from database
    codes = query_code_list(engine)

    # Determine which date field to use for incremental update (once per table)
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM {api_name} LIMIT 1"))
        row = result.fetchone()
        if row is not None:
            columns = result.keys()
        else:
            columns = []

        # Priority: f_ann_date > ann_date > trade_date
        if 'f_ann_date' in columns:
            date_field = 'f_ann_date'
        elif 'ann_date' in columns:
            date_field = 'ann_date'
        elif 'trade_date' in columns:
            date_field = 'trade_date'
        else:
            date_field = None

    print(f'Start updating {api_name} to {end_date} (using {date_field})')

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        engine_urls = [engine.url for _ in codes]
        tokens = [token for _ in codes]
        api_names = [api_name for _ in codes]
        params_list = [params for _ in codes]
        fields_list = [fields for _ in codes]
        retries = [retry for _ in codes]
        date_fields = [date_field for _ in codes]

        results = list(executor.map(_single_update_by_code,
                                   engine_urls,
                                   tokens,
                                   api_names,
                                   codes,
                                   [end_date for _ in codes],
                                   params_list,
                                   fields_list,
                                   retries,
                                   date_fields
        ))

    print(f'Finished updating {api_name} to {end_date}')
