import json
import unittest

import pandas as pd
from sqlalchemy import text
from src.database import get_engine
from src.queries.for_download import (query_latest_trade_date_by_table_name,
                                      query_latest_trade_date_by_ts_code,
                                      query_trade_cal)
from src.tushare_api import tushare_download


class TestForDownload(unittest.TestCase):

    def setUp(self):
        # database connection
        with open("test_config.json") as f:
            config = json.load(f)
            self.config = config["database"]
            self.token = config["token"]
        self.engine = get_engine(**self.config)

        # download test data
        self.code = "000001.SZ"
        self.table_name = "daily"
        self.download_df = tushare_download(self.token,
                                            self.table_name,
                                            {"ts_code": self.code,
                                     "start_date": "20200101",
                                     "end_date": "20250101"})
        self.download_df["trade_date"] = pd.to_datetime(self.download_df["trade_date"])
        self.latest_trade_date = self.download_df["trade_date"].max()


    def test_query_latest_trade_date_by_table_name(self):
        """Test querying the latest trade date from a table."""
        # save to database
        self.download_df.to_sql(self.table_name, self.engine, if_exists="replace", index=False)

        # query
        latest_trade_date = query_latest_trade_date_by_table_name(self.engine, self.table_name)
        self.assertEqual(latest_trade_date, self.latest_trade_date)

        # drop table
        with self.engine.begin() as conn:
            conn.execute(text(f"DROP TABLE {self.table_name}"))

    def test_query_latest_trade_date_by_ts_code(self):
        """Test querying the latest trade date for a given ts_code."""
        # save to database
        self.download_df.to_sql(self.table_name, self.engine, if_exists="replace", index=False)

        # query
        latest_trade_date = query_latest_trade_date_by_ts_code(self.engine, self.table_name, self.code)
        self.assertEqual(latest_trade_date, self.latest_trade_date)

        # drop table
        with self.engine.begin() as conn:
            conn.execute(text(f"DROP TABLE {self.table_name}"))

    def test_query_trade_cal(self):
        """Test querying the trade calendar from the database."""
        # Create sample trade calendar data
        trade_cal_data = pd.DataFrame({"cal_date": ["2020-01-01", "2020-01-02", "2020-01-03"]})
        trade_cal_data["cal_date"] = pd.to_datetime(trade_cal_data["cal_date"])

        # Save to database
        trade_cal_data.to_sql("trade_cal", self.engine, if_exists="replace", index=False)

        # Query trade calendar
        cal_dates = query_trade_cal(self.engine)

        # Convert results to datetime
        expected_dates = trade_cal_data["cal_date"].to_list()

        self.assertEqual(cal_dates, expected_dates)

        # Drop table
        with self.engine.begin() as conn:
            conn.execute(text("DROP TABLE trade_cal"))
