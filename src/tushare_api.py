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


def download(token: str,
             api_name: str,
             params: dict | None = None,
             fields: list[str] | None = None) -> DataFrame | None:
    """
    Download data from Tushare API.

    :param token: Tushare token for authentication.
    :param params: A dictionary of parameters to pass to the API endpoint.
    :param fields: A list of fields to retrieve from the API.
    :return: A DataFrame containing the data retrieved from the API.
    """
    pro = pro_api(token)
    if params is None:
        params = {}
    if fields is not None:
        params["fields"] = ",".join(fields)
    return pro.query(api_name, **params)

