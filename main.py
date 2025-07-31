"""
Main entry point for bagel-tushare: create all tables if not exist.
"""

import json
from time import perf_counter
from sqlalchemy.engine import Engine
from src.bagel_tushare.database import get_engine, create_all_tables


def connect_and_create_tables() -> Engine:
    # Example connection config, replace with your actual DB credentials
    with open('tests/test_config.json', 'r') as f:
        config = json.load(f)
    
    engine = get_engine(
        host=config['host'],
        port=config['port'],
        user=config['user'],
        password=config['password'],
        database=config['database']
    )
    create_all_tables(engine)
    print("All tables created (if not exist).")
    return engine

def main():
    connect_and_create_tables()

if __name__ == "__main__":
    start_time = perf_counter()
    main()
    time_elapsed = perf_counter() - start_time
    print(f"Time taken: {time_elapsed:.2f} seconds \n or {time_elapsed / 60:.2f} minutes")
