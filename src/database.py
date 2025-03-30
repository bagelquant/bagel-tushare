"""
Database connection and query execution module.
"""

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.sql import text


def get_engine(host: str,
               port: int,
               user: str,
               password: str,
               database: str) -> Engine:
    """
    Create a SQLAlchemy engine for connecting to a MySQL database.

    :param host: Hostname of the database server.
    :param port: Port number of the database server.
    :param user: Username for authentication.
    :param password: Password for authentication.
    :param database: Name of the database to connect to.
    :return: SQLAlchemy engine object.
    """
    connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    return create_engine(connection_string)


def create_log_table(engine: Engine) -> None:
    """
    Create a log table in the database if it doesn't exist.

    :param engine: SQLAlchemy engine object.
    :return: None
    """

    with engine.begin() as conn:
        conn.execute(text(
            """
            CREATE TABLE IF NOT EXISTS log (
                id INT AUTO_INCREMENT PRIMARY KEY,
                update_table VARCHAR(20) NOT NULL,
                message TEXT NOT NULL,
                trade_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
        )
