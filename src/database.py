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
    Creates and returns a SQLAlchemy engine using the provided database
    connection parameters. The engine allows interaction with the specified
    database using SQLAlchemy functionalities.

    :param host: Database server hostname or IP address.
    :param port: Port number on which the database server is listening.
    :param user: Username for database authentication.
    :param password: Password corresponding to the database user.
    :param database: Name of the database to connect to.
    :return: A SQLAlchemy Engine instance configured with the provided connection details.
    """
    connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    return create_engine(connection_string)


def create_log_table(engine: Engine) -> None:
    """
    Creates a `log` table in the database if it does not already exist. The `log` table
    contains information about updates, including the table name, a message,
    and a timestamp indicating when the log entry was created.

    :param engine: SQLAlchemy Engine instance used to connect to the database.
    :type engine: Engine
    :return: None
    """

    with engine.begin() as conn:
        conn.execute(text(
            """
            CREATE TABLE IF NOT EXISTS log (
                id INT AUTO_INCREMENT PRIMARY KEY,
                update_table VARCHAR(20) NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
        )


def insert_log(engine: Engine,
               table_name: str,
               message: str) -> None:
    """
    Inserts a log entry into the `log` table in the database.

    :param engine: SQLAlchemy Engine instance used to connect to the database.
    :param table_name: The name of the table being updated (logged entry).
    :param message: The log message describing the update.
    :return: None
    """
    with engine.begin() as conn:
        conn.execute(text(
            f"""
            INSERT INTO log (update_table, message)
            VALUES ('{table_name}', '{message}')
            """
        ))
