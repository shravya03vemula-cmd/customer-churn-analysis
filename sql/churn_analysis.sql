-- ============================================================
-- CUSTOMER CHURN ANALYSIS
-- Dataset: Telco Customer Churn
-- ============================================================

-- 1. OVERALL CHURN RATE
SELECT
    COUNT(*)                                                AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)         AS churned_customers,
    ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) /
          COUNT(*) * 100, 2)                                AS churn_rate_pct
FROM customers;

-- 2. CHURN BY CONTRACT TYPE
SELECT
    contract,
    COUNT(*)                                                AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)         AS churned,
    ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) /
          COUNT(*) * 100, 2)                                AS churn_rate_pct
FROM customers
GROUP BY contract
ORDER BY churn_rate_pct DESC;

-- 3. CHURN BY TENURE GROUP
SELECT
    CASE
        WHEN tenure BETWEEN 0  AND 12 THEN '0-12 months'
        WHEN tenure BETWEEN 13 AND 24 THEN '13-24 months'
        WHEN tenure BETWEEN 25 AND 48 THEN '25-48 months'
        ELSE '48+ months'
    END                                                     AS tenure_group,
    COUNT(*)                                                AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)         AS churned,
    ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) /
          COUNT(*) * 100, 2)                                AS churn_rate_pct
FROM customers
GROUP BY tenure_group
ORDER BY MIN(tenure);

-- 4. CHURN BY PAYMENT METHOD
SELECT
    payment_method,
    COUNT(*)                                                AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)         AS churned,
    ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) /
          COUNT(*) * 100, 2)                                AS churn_rate_pct
FROM customers
GROUP BY payment_method
ORDER BY churn_rate_pct DESC;

-- 5. CHURN BY INTERNET SERVICE
SELECT
    internet_service,
    COUNT(*)                                                AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)         AS churned,
    ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) /
          COUNT(*) * 100, 2)                                AS churn_rate_pct
FROM customers
GROUP BY internet_service
ORDER BY churn_rate_pct DESC;

-- 6. AVERAGE MONTHLY CHARGES — CHURNED VS RETAINED
SELECT
    churn,
    ROUND(AVG(monthly_charges), 2)                         AS avg_monthly_charges,
    ROUND(AVG(tenure), 1)                                  AS avg_tenure_months,
    ROUND(AVG(total_charges), 2)                           AS avg_total_charges,
    COUNT(*)                                               AS total_customers
FROM customers
GROUP BY churn;

-- 7. HIGH RISK CUSTOMERS — LIKELY TO CHURN
SELECT
    customer_id,
    tenure,
    contract,
    monthly_charges,
    payment_method,
    internet_service
FROM customers
WHERE churn = 'No'
  AND tenure < 12
  AND contract = 'Month-to-month'
  AND monthly_charges > 65
ORDER BY monthly_charges DESC
LIMIT 20;

-- 8. REVENUE AT RISK FROM CHURN
SELECT
    ROUND(SUM(monthly_charges), 2)                         AS monthly_revenue_at_risk,
    COUNT(*)                                               AS customers_at_risk
FROM customers
WHERE churn = 'Yes';

-- 9. CHURN BY SENIOR CITIZEN STATUS
SELECT
    CASE WHEN senior_citizen = 1 THEN 'Senior' ELSE 'Non-Senior' END AS customer_type,
    COUNT(*)                                                AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END)         AS churned,
    ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) /
          COUNT(*) * 100, 2)                                AS churn_rate_pct
FROM customers
GROUP BY senior_citizen;

-- 10. CHURN BY NUMBER OF SERVICES SUBSCRIBED
SELECT
    (CASE WHEN phone_service = 'Yes' THEN 1 ELSE 0 END +
     CASE WHEN internet_service != 'No' THEN 1 ELSE 0 END +
     CASE WHEN online_security = 'Yes' THEN 1 ELSE 0 END +
     CASE WHEN tech_support = 'Yes' THEN 1 ELSE 0 END +
     CASE WHEN streaming_tv = 'Yes' THEN 1 ELSE 0 END)     AS services_count,
    COUNT(*)                                               AS total_customers,
    ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) /
          COUNT(*) * 100, 2)                               AS churn_rate_pct
FROM customers
GROUP BY services_count
ORDER BY services_count;