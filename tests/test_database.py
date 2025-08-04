import json
from unittest import TestCase

from src.bageltushare.database import get_engine, create_all_tables, text, insert_log, create_index


class TestDatabase(TestCase):
    def setUp(self):
        with open("tests/test_config.json") as f:
            self.config = json.load(f)["database"]

    def test_get_engine(self):
        engine = get_engine(**self.config)
        self.assertIsNotNone(engine)

        # drop log table
        with engine.begin() as conn:
            conn.execute(text("DROP TABLE IF EXISTS log"))
