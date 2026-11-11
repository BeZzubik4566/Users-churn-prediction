import json

import pandas as pd
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
from sqlalchemy import text
from sqlalchemy.engine import Engine

from src.config import (
    FEATURE_COLUMNS,
    CATEGORICAL_COLUMNS,
    MODEL_NAME,
    MODEL_PATH,
    MODEL_DIR,
    REPORTS_DIR,
    RANDOM_STATE,
    VALIDATION_SIZE,
    PREDICTION_THRESHOLD,
)


def train_model(engine: Engine) -> dict:
    query = """
        SELECT row_id, """ + ", ".join(FEATURE_COLUMNS) + """, churn
        FROM raw.customers_train
        ORDER BY row_id
    """
    data = pd.read_sql_query(text(query), con=engine)
    if data.empty:
        raise ValueError("Таблица raw.customers_train пуста. Сначала загрузите CSV.")

    X = data[FEATURE_COLUMNS]
    y = data["churn"].astype(int)

    X_train, X_valid, y_train, y_valid = train_test_split(
        X,
        y,
        test_size=VALIDATION_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    categorical_indices = [X.columns.get_loc(column) for column in CATEGORICAL_COLUMNS]
    model = CatBoostClassifier(
        iterations=700,
        depth=6,
        learning_rate=0.03,
        loss_function="Logloss",
        eval_metric="AUC",
        random_seed=RANDOM_STATE,
        auto_class_weights="Balanced",
        allow_writing_files=False,
        verbose=100,
    )

    model.fit(
        X_train,
        y_train,
        cat_features=categorical_indices,
        eval_set=(X_valid, y_valid),
        early_stopping_rounds=60,
        verbose=100,
    )

    probabilities = model.predict_proba(X_valid)[:, 1]
    predictions = (probabilities >= PREDICTION_THRESHOLD).astype(int)

    metrics = {
        "model_name": MODEL_NAME,
        "accuracy": float(accuracy_score(y_valid, predictions)),
        "precision_score": float(precision_score(y_valid, predictions, zero_division=0)),
        "recall_score": float(recall_score(y_valid, predictions, zero_division=0)),
        "f1_score": float(f1_score(y_valid, predictions, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_valid, probabilities)),
        "train_rows": int(len(X_train)),
        "validation_rows": int(len(X_valid)),
    }

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    model.save_model(str(MODEL_PATH))
    (REPORTS_DIR / "metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=4),
        encoding="utf-8",
    )

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                INSERT INTO ml.model_metrics (
                    model_name, accuracy, precision_score, recall_score,
                    f1_score, roc_auc, train_rows, validation_rows
                ) VALUES (
                    :model_name, :accuracy, :precision_score, :recall_score,
                    :f1_score, :roc_auc, :train_rows, :validation_rows
                )
                """
            ),
            metrics,
        )

    print("Метрики на валидационной выборке:")
    for metric, value in metrics.items():
        print(f"{metric}: {value}")
    print(f"Модель сохранена: {MODEL_PATH}")

    return metrics
