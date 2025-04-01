import json
from unittest import TestCase

from src.database import get_engine, create_log_table, text, insert_log, create_index


class TestDatabase(TestCase):
    def setUp(self):
        with open("test_config.json") as f:
            self.config = json.load(f)["database"]

    def test_get_engine(self):
        engine = get_engine(**self.config)
        self.assertIsNotNone(engine)

        # drop log table
        with engine.begin() as conn:
            conn.execute(text("DROP TABLE IF EXISTS log"))

    def test_create_log_table(self):
        engine = get_engine(**self.config)
        create_log_table(engine)
        with engine.begin() as conn:
            result = conn.execute(text("SHOW TABLES LIKE 'log'")).fetchall()
            result = [r[0] for r in result]
            self.assertIn("log", result)

    def test_log_table_structure(self):
        """Test that the `log` table has the correct schema."""
        engine = get_engine(**self.config)
        create_log_table(engine)
        with engine.begin() as conn:
            result = conn.execute(
                text(
                    """
                    SELECT COLUMN_NAME, DATA_TYPE
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_NAME = 'log'
                    """
                )
            ).fetchall()
            columns = {row[0]: row[1] for row in result}
            self.assertIn("id", columns)
            self.assertEqual(columns["id"], "int")
            self.assertIn("update_table", columns)
            self.assertEqual(columns["update_table"], "varchar")
            self.assertIn("message", columns)
            self.assertEqual(columns["message"], "text")
            self.assertIn("created_at", columns)
            self.assertEqual(columns["created_at"], "timestamp")

    def test_insert_log(self):
        engine = get_engine(**self.config)
        create_log_table(engine)

        # test inserting a valid log entry
        insert_log(engine, "users", "Added a new user.")
        with engine.begin() as conn:
            logs = conn.execute(text("SELECT * FROM log WHERE update_table = 'users'")).fetchall()
            self.assertEqual(len(logs), 1)

        # test inserting multiple log entries
        insert_log(engine, "orders", "Order processed.")
        insert_log(engine, "inventory", "Stock updated.")
        with engine.begin() as conn:
            logs = conn.execute(text("SELECT * FROM log")).fetchall()
            self.assertEqual(len(logs), 3)


    def test_create_index(self):
        engine = get_engine(**self.config)
        create_index(engine, "daily")
