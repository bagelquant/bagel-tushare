import json
from unittest import TestCase

from src.bageltushare import tushare_download


class TestTushareAPI(TestCase):

    def setUp(self):
        with open("tests/test_config.json") as f:
            self.token = json.load(f)["token"]

    def test_download(self):
        """Test downloading data with valid parameters."""
        api_name = "daily"
        params = {"ts_code": "000001.SZ", "trade_date": "20250325"}
        fields = ["ts_code", "trade_date", "open", "high", "low", "close", "vol"]
        df = tushare_download(self.token, api_name, params, fields)
        self.assertIsNotNone(df)
        self.assertEqual(df.shape[0], 1)  # type: ignore
        self.assertEqual(df.shape[1], 7)  # type: ignore

    def test_download_no_fields(self):
        """Test downloading data without specifying fields."""
        api_name = "daily"
        params = {"ts_code": "000001.SZ", "trade_date": "20250325"}
        df = tushare_download(self.token, api_name, params)
        self.assertIsNotNone(df)
        self.assertGreater(df.shape[1], 0)  # type: ignore

    def test_download_invalid_token(self):
        """Test downloading data with an invalid token."""
        api_name = "daily"
        params = {"ts_code": "000001.SZ", "trade_date": "20250325"}
        invalid_token = "INVALID_TOKEN"
        with self.assertRaises(Exception):
            tushare_download(invalid_token, api_name, params)
