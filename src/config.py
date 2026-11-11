from pathlib import Path
import os

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(ROOT_DIR / ".env")

DATA_DIR = ROOT_DIR / "data" / "raw"
TRAIN_CSV = DATA_DIR / "train.csv"
TEST_CSV = DATA_DIR / "test.csv"
MODEL_DIR = ROOT_DIR / "models"
MODEL_PATH = MODEL_DIR / "catboost_churn.cbm"
REPORTS_DIR = ROOT_DIR / "reports"

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "Не задан DATABASE_URL. Скопируйте .env.example в .env "
        "и укажите параметры подключения к PostgreSQL."
    )

MODEL_NAME = "catboost_churn_v1"
RANDOM_STATE = 42
VALIDATION_SIZE = 0.2
PREDICTION_THRESHOLD = 0.5

FEATURE_COLUMNS = [
    "client_period",
    "monthly_spending",
    "total_spent",
    "sex",
    "is_senior_citizen",
    "has_partner",
    "has_child",
    "has_phone_service",
    "has_multiple_phone_numbers",
    "has_internet_service",
    "has_online_security_service",
    "has_online_backup",
    "has_device_protection",
    "has_tech_support_access",
    "has_online_tv",
    "has_movie_subscription",
    "has_contract_phone",
    "is_billing_paperless",
    "payment_method",
]

CATEGORICAL_COLUMNS = [
    "sex",
    "has_partner",
    "has_child",
    "has_phone_service",
    "has_multiple_phone_numbers",
    "has_internet_service",
    "has_online_security_service",
    "has_online_backup",
    "has_device_protection",
    "has_tech_support_access",
    "has_online_tv",
    "has_movie_subscription",
    "has_contract_phone",
    "is_billing_paperless",
    "payment_method",
]
