-- Сводная статистика по обучающей выборке.
CREATE OR REPLACE VIEW analytics.v_churn_overview AS
SELECT
    COUNT(*) AS customers_total,
    COUNT(*) FILTER (WHERE churn = 1) AS churned_customers,
    COUNT(*) FILTER (WHERE churn = 0) AS active_customers,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE churn = 1) / NULLIF(COUNT(*), 0),
        2
    ) AS churn_rate_percent,
    ROUND(AVG(monthly_spending), 2) AS avg_monthly_spending
FROM raw.customers_train;

-- Отток в зависимости от типа контракта.
CREATE OR REPLACE VIEW analytics.v_churn_by_contract AS
SELECT
    has_contract_phone AS contract_type,
    COUNT(*) AS customers_total,
    COUNT(*) FILTER (WHERE churn = 1) AS churned_customers,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE churn = 1) / NULLIF(COUNT(*), 0),
        2
    ) AS churn_rate_percent
FROM raw.customers_train
GROUP BY has_contract_phone;

-- Отток в зависимости от типа интернет-подключения.
CREATE OR REPLACE VIEW analytics.v_churn_by_internet AS
SELECT
    has_internet_service AS internet_type,
    COUNT(*) AS customers_total,
    COUNT(*) FILTER (WHERE churn = 1) AS churned_customers,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE churn = 1) / NULLIF(COUNT(*), 0),
        2
    ) AS churn_rate_percent
FROM raw.customers_train
GROUP BY has_internet_service;

-- Отток в зависимости от способа оплаты.
CREATE OR REPLACE VIEW analytics.v_churn_by_payment AS
SELECT
    payment_method,
    COUNT(*) AS customers_total,
    COUNT(*) FILTER (WHERE churn = 1) AS churned_customers,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE churn = 1) / NULLIF(COUNT(*), 0),
        2
    ) AS churn_rate_percent
FROM raw.customers_train
GROUP BY payment_method;
