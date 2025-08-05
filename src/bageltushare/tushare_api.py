"""
Tushare api wrapper for stock data retrieval.

This module provides a wrapper around the Tushare API, the function well receives:

- `token`: Tushare token for authentication
- `api_name`: The name of the Tushare API endpoint to call
- `params`: A dictionary of parameters to pass to the API endpoint
- `fields`: A comma-separated string of fields to retrieve from the API

"""

from pandas import DataFrame
from tushare import pro_api


def tushare_download(token: str,
                     api_name: str,
                     params: dict | None = None,
                     fields: list[str] | None = None) -> DataFrame | None:
    """
    Downloads data by querying an API using the specified token and parameters.

    :param token: The authentication token for accessing the API.
    :param api_name: The name of the API to query data from.
    :param params: Optional dictionary of query parameters to include in the API call.
    :param fields: Optional list of field names to explicitly retrieve from the API.
    :return: A DataFrame containing data from the query, or None if no data is
        available.
    """
    pro = pro_api(token)
    if params is None:
        params = {}
    if fields is not None:
        params['fields'] = ','.join(fields)
    return pro.query(api_name, **params)
