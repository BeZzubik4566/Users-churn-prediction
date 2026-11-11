from src.database import get_engine
from src.init_db import initialize_database
from src.load_data import load_data_to_postgres
from src.train import train_model
from src.predict import predict_test_data


def main() -> None:
    engine = get_engine()
    try:
        initialize_database(engine)
        load_data_to_postgres(engine)
        train_model(engine)
        predict_test_data(engine)
        print("Готово: данные находятся в PostgreSQL, модель обучена, прогнозы сохранены.")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
