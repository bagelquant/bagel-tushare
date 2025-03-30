import json
from unittest import TestCase
from src.database import get_engine, create_log_table, text


class TestDatabase(TestCase):

    def setUp(self):
        with open("test_config.json", "r") as f:
            self.config = json.load(f)["database"]

    def test_get_engine(self):
        engine = get_engine(**self.config)
        self.assertIsNotNone(engine)

    def test_create_log_table(self):
        engine = get_engine(**self.config)
        create_log_table(engine)
        with engine.begin() as conn:
            result = conn.execute(text("SHOW TABLES LIKE 'log'")).fetchall()
            result = [r[0] for r in result]
            self.assertIn("log", result)
