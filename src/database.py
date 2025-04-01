"""
Database connection and query execution module.
"""

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.sql import text
from sqlalchemy.exc import OperationalError


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


def create_index(engine: Engine,
                 table_name: str) -> None:
    """
    Creates an index on the specified table in the database.

    The function generates a SQL query to create an index on the table's
    columns listed in the `index_list`. The query is executed using the
    provided database engine within a transaction, ensuring changes only
    take effect if the execution succeeds.

    :param engine: A SQLAlchemy Engine object that connects to the database.
    :param table_name: The name of the table on which the index will be created.
    :return: None
    """
    index_list = ['trade_date', 'f_ann_date', 'end_date', 'ts_code']
    # get columns
    query_columns = f"""
    SELECT COLUMN_NAME 
    FROM INFORMATION_SCHEMA.COLUMNS 
    WHERE TABLE_NAME = '{table_name}'
    """

    # get existing indexes
    query_existing = f"""
    SHOW INDEX FROM {table_name}
    """

    with engine.begin() as conn:
        columns = conn.execute(text(query_columns)).fetchall()
        columns = [_[0] for _ in columns]

        existing_indexes = conn.execute(text(query_existing)).fetchall()
        existing_indexes = [_[2] for _ in existing_indexes]

        print(existing_indexes)

        # create index
        for index in index_list:
            if index in columns:
                # check existing
                if f"idx_{table_name}_{index}" in existing_indexes:
                    continue

                if index == 'ts_code':
                    # ts_code is TEXT not specify length
                    query_create_index = f"""
                    ALTER TABLE {table_name}
                    MODIFY COLUMN ts_code VARCHAR(20),
                    ADD INDEX idx_{table_name}_{index} (ts_code);
                    """
                else:
                    query_create_index = f"""
                    CREATE INDEX idx_{table_name}_{index} ON {table_name} ({index});
                    """
                conn.execute(text(query_create_index))
            else:
                continue
