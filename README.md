# Customer Churn Prediction: PostgreSQL + CatBoost

Учебный end-to-end ML-проект: исходные CSV загружаются в PostgreSQL, SQL используется для хранения и анализа данных, CatBoost обучается на данных из БД, а прогнозы и метрики возвращаются в PostgreSQL.

> В текущем исходном репозитории фактическая задача — прогнозирование оттока клиентов (`Churn`), хотя название репозитория говорит об оценках студентов. Этот проект соответствует содержимому `train.csv`, `test.csv` и `ottock sub.py`.

## Структура

```text
churn_sql_ml_project/
├── data/
│   └── raw/                  # сюда положить train.csv и test.csv
├── models/                   # здесь появится файл CatBoost-модели
├── reports/                  # метрики и CSV с прогнозами
├── sql/
│   ├── 01_create_tables.sql  # схемы и таблицы PostgreSQL
│   ├── 02_analytics_views.sql# аналитические VIEW
│   └── 03_exploration_queries.sql # полезные SQL-запросы
├── src/
│   ├── config.py             # пути, параметры, список признаков
│   ├── database.py           # подключение к PostgreSQL
│   ├── init_db.py            # создание таблиц и VIEW
│   ├── load_data.py          # загрузка CSV в raw
│   ├── train.py               # обучение и оценка модели
│   ├── predict.py             # прогнозирование и запись в ml.predictions
│   └── run_pipeline.py        # запуск всего процесса
├── .env.example               # пример настроек подключения
├── docker-compose.yml         # PostgreSQL в Docker (опционально)
└── requirements.txt           # Python-зависимости
