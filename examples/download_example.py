"""
Author: Yanzhong(Eric) Huang

Download and update data example
"""

from bageltushare import download, update_by_date, update_by_code
from bageltushare import create_index, create_all_tables, get_engine


# configs
HOST = "localhost"
PORT = 3306
USER = "root"
PASSWORD = "<YOUR_PASSWORD>"
PASSWORD = "Hyz.js180518"
DB = "<DATABASE_NAME>"
DB = "tushare_test"

ENGINE = get_engine(HOST, PORT, USER, PASSWORD, DB)
TOKEN = "4f3059398b2c5fdb1b8d686be52cc6e7cb9bf4d61f75308821889c2f"

def main() -> None:
    by_date_apis = [
        "daily",
        "adj_factor",
    ]

    by_code_apis = [
        "balancesheet",
        "cashflow",
        "income",
    ]

    create_all_tables(ENGINE)

    # download and replace table
    download(engine=ENGINE, token=TOKEN, api_name="trade_cal")
    download(engine=ENGINE,
             token=TOKEN,
             api_name="stock_basic",
             params={"list_status": "L, D, P"},
             fields=[
                 "ts_code",
                 "symbol",
                 "name",
                 "area",
                 "industry",
                 "cnspell",
                 "market",
                 "list_date",
                 "act_name",
                 "act_ent_type",
                 "fullname",
                 "enname",
                 "exchange",
                 "curr_type",
                 "list_status",
                 "delist_date",
                 "is_hs"
             ])

    for api in by_date_apis:
        update_by_date(engine=ENGINE, token=TOKEN, api_name=api)
        create_index(engine=ENGINE, table_name=api)

    for api in by_code_apis:
        update_by_code(engine=ENGINE, token=TOKEN, api_name=api)
        create_index(engine=ENGINE, table_name=api)

if __name__ == "__main__":
    main()