from pathlib import Path

from sqlalchemy.engine import Engine

from src.config import ROOT_DIR


SQL_DIR = ROOT_DIR / "sql"


def initialize_database(engine: Engine) -> None:
    """Создаёт таблицы, индексы и аналитические представления."""
    sql_files = [
        SQL_DIR / "01_create_tables.sql",
        SQL_DIR / "02_analytics_views.sql",
    ]

    for sql_file in sql_files:
        if not sql_file.exists():
            raise FileNotFoundError(f"Не найден SQL-файл: {sql_file}")

        sql_script = sql_file.read_text(encoding="utf-8")
        with engine.begin() as connection:
            connection.exec_driver_sql(sql_script)
        print(f"Выполнен SQL-скрипт: {sql_file.name}")
