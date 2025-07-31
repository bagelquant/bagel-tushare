from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

Base = declarative_base()

def create_all_tables(engine):
    Base.metadata.create_all(engine)

def get_engine(
    host: str,
    port: int,
    user: str,
    password: str,
    database: str
) -> Engine:
    return create_engine(
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}",
        pool_pre_ping=True
    )