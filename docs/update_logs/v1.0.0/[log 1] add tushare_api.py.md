# [log 1] Add tushare_api.py

add tushare_api.py to the project

## `tushare_api` module

This module provides a wrapper around the Tushare API, the function well receives:

- `token`: Tushare token for authentication
- `api_name`: The name of the Tushare API endpoint to call
- `params`: A dictionary of parameters to pass to the API endpoint
- `fields`: A list of fields to include in the API response

This function handles the API call, does not handle errors, and returns the response data.
