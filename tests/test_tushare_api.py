import json
from unittest import TestCase
from src.tushare_api import download


class TestTushareAPI(TestCase):

    def setUp(self):
        with open("test_config.json", "r") as f:
            self.token = json.load(f)["token"]

    def test_download(self):
        api_name = "daily"
        params = {"ts_code": "000001.SZ", "trade_date": "20250325"}
        fields = ["ts_code", "trade_date", "open", "high", "low", "close", "vol"]
        df = download(self.token, api_name, params, fields)
        self.assertIsNotNone(df)
        self.assertEqual(df.shape[0], 1)
        self.assertEqual(df.shape[1], 7)
        print(df)
