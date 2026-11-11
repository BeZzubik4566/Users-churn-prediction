import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

from src.config import TRAIN_CSV, TEST_CSV, FEATURE_COLUMNS


COLUMN_MAP = {
    "ClientPeriod": "client_period",
    "MonthlySpending": "monthly_spending",
    "TotalSpent": "total_spent",
    "Sex": "sex",
    "IsSeniorCitizen": "is_senior_citizen",
    "HasPartner": "has_partner",
    "HasChild": "has_child",
    "HasPhoneService": "has_phone_service",
    "HasMultiplePhoneNumbers": "has_multiple_phone_numbers",
    "HasInternetService": "has_internet_service",
    "HasOnlineSecurityService": "has_online_security_service",
    "HasOnlineBackup": "has_online_backup",
    "HasDeviceProtection": "has_device_protection",
    "HasTechSupportAccess": "has_tech_support_access",
    "HasOnlineTV": "has_online_tv",
    "HasMovieSubscription": "has_movie_subscription",
    "HasContractPhone": "has_contract_phone",
    "IsBillingPaperless": "is_billing_paperless",
    "PaymentMethod": "payment_method",
    "Churn": "churn",
}

NUMERIC_COLUMNS = [
    "client_period",
    "monthly_spending",
    "total_spent",
    "is_senior_citizen",
]
CATEGORICAL_COLUMNS = [column for column in FEATURE_COLUMNS if column not in NUMERIC_COLUMNS]


def prepare_dataframe(file_path, is_train: bool) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(
            f"Не найден файл {file_path}. Поместите train.csv и test.csv в data/raw/."
        )

    df = pd.read_csv(file_path)
    df = df.rename(columns=COLUMN_MAP)

    required_columns = FEATURE_COLUMNS + (["churn"] if is_train else [])
    missing_columns = sorted(set(required_columns) - set(df.columns))
    if missing_columns:
        raise ValueError(
            f"В {file_path.name} отсутствуют обязательные столбцы: {missing_columns}"
        )

    # В исходном Telco-датасете пустой TotalSpent означает отсутствие накопленных трат.
    for column in NUMERIC_COLUMNS + (["churn"] if is_train else []):
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df["total_spent"] = df["total_spent"].fillna(0)

    for column in NUMERIC_COLUMNS + (["churn"] if is_train else []):
        if df[column].isna().any():
            raise ValueError(
                f"В столбце {column} файла {file_path.name} остались пропуски "
                "или нечисловые значения. Проверьте исходный CSV."
            )

    df["client_period"] = df["client_period"].astype(int)
    df["is_senior_citizen"] = df["is_senior_citizen"].astype(int)
    if is_train:
        df["churn"] = df["churn"].astype(int)
        if not set(df["churn"].unique()).issubset({0, 1}):
            raise ValueError("В столбце Churn допускаются только значения 0 и 1.")

    for column in CATEGORICAL_COLUMNS:
        df[column] = df[column].fillna("Unknown").astype(str)

    selected_columns = FEATURE_COLUMNS + (["churn"] if is_train else [])
    return df[selected_columns]


def load_data_to_postgres(engine: Engine) -> None:
    train_df = prepare_dataframe(TRAIN_CSV, is_train=True)
    test_df = prepare_dataframe(TEST_CSV, is_train=False)

    # Обе таблицы очищаются в одной транзакции, чтобы повторный запуск
    # не дублировал строки и не оставлял частично загруженные данные.
    with engine.begin() as connection:
        connection.execute(
            text(
                "TRUNCATE TABLE raw.customers_train, raw.customers_test "
                "RESTART IDENTITY CASCADE"
            )
        )
        train_df.to_sql(
            "customers_train",
            con=connection,
            schema="raw",
            if_exists="append",
            index=False,
            method="multi",
            chunksize=1000,
        )
        test_df.to_sql(
            "customers_test",
            con=connection,
            schema="raw",
            if_exists="append",
            index=False,
            method="multi",
            chunksize=1000,
        )

    print(f"Загружено строк train: {len(train_df)}")
    print(f"Загружено строк test: {len(test_df)}")
