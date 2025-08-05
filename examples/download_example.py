"""
Author: Yanzhong(Eric) Huang

Download and update data example
"""

import json
from bageltushare import download, update_by_date, update_by_code
from bageltushare import create_index, create_all_tables, get_engine


# configs
HOST = 'localhost'
PORT = 3306
USER = 'root'
PASSWORD = '<YOUR_PASSWORD>'
DB = '<DATABASE_NAME>'

ENGINE = get_engine(HOST, PORT, USER, PASSWORD, DB)
TOKEN = '<YOUR_TOKEN>'

# OR load from config file
with open('tests/test_config.json') as f:
    config = json.load(f)
    ENGINE = get_engine(**config['database'])
    TOKEN = config['tushare_token']


def main() -> None:
    by_date_apis = [
        'daily',
        'adj_factor',
    ]

    by_code_apis = [
        # 'balancesheet',
        # 'cashflow',
        # 'income',
        'fina_indicator',
    ]

    create_all_tables(ENGINE)

    # download and replace table
    download(engine=ENGINE, token=TOKEN, api_name='trade_cal')
    download(engine=ENGINE,
             token=TOKEN,
             api_name='stock_basic',
             params={'list_status': 'L, D, P'},
             fields=[       # Optional: specify fields to download
                 'ts_code',
                 'symbol',
                 'name',
                 'area',
                 'industry',
                 'cnspell',
                 'market',
                 'list_date',
                 'act_name',
                 'act_ent_type',
                 'fullname',
                 'enname',
                 'exchange',
                 'curr_type',
                 'list_status',
                 'delist_date',
                 'is_hs'
             ])

    # Suggestion: update daily
    for api in by_date_apis:
        update_by_date(engine=ENGINE, token=TOKEN, api_name=api)
        create_index(engine=ENGINE, table_name=api)

    # Suggestion: update monthly or quarterly, these tables normally do not change frequently
    # Example: update balancesheet, cashflow, income
    for api in by_code_apis:
        update_by_code(engine=ENGINE, token=TOKEN, api_name=api)
        create_index(engine=ENGINE, table_name=api)

if __name__ == "__main__":
    main()