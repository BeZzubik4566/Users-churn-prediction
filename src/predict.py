import pandas as pd
from catboost import CatBoostClassifier
from sqlalchemy import text
from sqlalchemy.engine import Engine

from src.config import (
    FEATURE_COLUMNS,
    MODEL_NAME,
    MODEL_PATH,
    REPORTS_DIR,
    PREDICTION_THRESHOLD,
)


def predict_test_data(engine: Engine) -> pd.DataFrame:
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Файл модели не найден. Сначала выполните обучение.")

    query = """
        SELECT row_id, """ + ", ".join(FEATURE_COLUMNS) + """
        FROM raw.customers_test
        ORDER BY row_id
    """
    test_df = pd.read_sql_query(text(query), con=engine)
    if test_df.empty:
        raise ValueError("Таблица raw.customers_test пуста. Сначала загрузите CSV.")

    model = CatBoostClassifier()
    model.load_model(str(MODEL_PATH))

    X_test = test_df[FEATURE_COLUMNS]
    probabilities = model.predict_proba(X_test)[:, 1]
    predicted = (probabilities >= PREDICTION_THRESHOLD).astype(int)

    result = pd.DataFrame(
        {
            "test_row_id": test_df["row_id"].astype(int),
            "churn_probability": probabilities.astype(float),
            "predicted_churn": predicted.astype(int),
            "model_name": MODEL_NAME,
        }
    )

    # При повторном запуске заменяем прогнозы этой версии модели.
    with engine.begin() as connection:
        connection.execute(
            text("DELETE FROM ml.predictions WHERE model_name = :model_name"),
            {"model_name": MODEL_NAME},
        )
        result.to_sql(
            "predictions",
            con=connection,
            schema="ml",
            if_exists="append",
            index=False,
            method="multi",
            chunksize=1000,
        )

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    result.to_csv(REPORTS_DIR / "predictions.csv", index=False)
    print(f"Сохранено прогнозов: {len(result)}")
    print(f"Файл с прогнозами: {REPORTS_DIR / 'predictions.csv'}")
    return result
