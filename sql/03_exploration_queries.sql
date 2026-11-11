-- 1. Общая доля оттока.
SELECT *
FROM analytics.v_churn_overview;

-- 2. Сравнение оттока по типу контракта.
SELECT *
FROM analytics.v_churn_by_contract
ORDER BY churn_rate_percent DESC;

-- 3. Отток по интернет-подключению.
SELECT *
FROM analytics.v_churn_by_internet
ORDER BY churn_rate_percent DESC;

-- 4. Способы оплаты с наибольшей долей оттока.
SELECT *
FROM analytics.v_churn_by_payment
ORDER BY churn_rate_percent DESC;

-- 5. Сегменты с коротким сроком обслуживания и высокой долей оттока.
SELECT
    CASE
        WHEN client_period <= 6 THEN '0-6 months'
        WHEN client_period <= 12 THEN '7-12 months'
        WHEN client_period <= 24 THEN '13-24 months'
        ELSE '25+ months'
    END AS tenure_group,
    COUNT(*) AS customers_total,
    COUNT(*) FILTER (WHERE churn = 1) AS churned_customers,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE churn = 1) / NULLIF(COUNT(*), 0),
        2
    ) AS churn_rate_percent
FROM raw.customers_train
GROUP BY tenure_group
ORDER BY MIN(client_period);

-- 6. Последние результаты оценки ML-модели.
SELECT
    model_name,
    accuracy,
    precision_score,
    recall_score,
    f1_score,
    roc_auc,
    train_rows,
    validation_rows,
    created_at
FROM ml.model_metrics
ORDER BY created_at DESC;

-- 7. Сколько клиентов модель отнесла к риску оттока.
SELECT
    predicted_churn,
    COUNT(*) AS customers_count,
    ROUND(AVG(churn_probability)::numeric, 4) AS avg_churn_probability
FROM ml.predictions
GROUP BY predicted_churn
ORDER BY predicted_churn DESC;
