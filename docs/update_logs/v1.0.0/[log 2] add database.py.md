# [log 2] Add database.py

Module responsibility:

- Connect to mysql database
- query the database
- close the connection

Adding: 

- `get_engine` function, returns a SQLAlchemy engine object.
- `create_log_table` function, creates a log in the database.
