from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from src.config import DATABASE_URL


def get_engine() -> Engine:
    """Создаёт подключение к PostgreSQL."""
    return create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        future=True,
    )
