# 🔄 Customer Churn Analysis — Telco Dataset

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-MySQL-4479A1?style=flat&logo=mysql&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-16A34A?style=flat)

> End-to-end customer churn analysis combining SQL, Python EDA, and a 
> Random Forest machine learning model to predict which customers will 
> churn — and why.

---

## 🎯 Business Problem

Customer acquisition costs 5x more than retention. The business needed answers to:

1. What is our current churn rate and where is it highest?
2. Which factors drive customers to leave?
3. Can we predict WHO will churn before they do?
4. Which customers should the retention team contact first?

---

## 📁 Project Structure
```
project-2-customer-churn/
│
├── data/
│   └── telco_churn.csv
│
├── sql/
│   └── churn_analysis.sql
│
├── notebooks/
│   └── churn_analysis.py
│
├── outputs/
│   ├── 01_churn_overview.png
│   ├── 02_tenure_charges.png
│   ├── 03_churn_factors.png
│   ├── 04_correlation_heatmap.png
│   ├── 05_model_results.png
│   └── 06_roc_curve.png
│
└── README.md
```

---

## 🔧 Tech Stack

| Tool | Purpose |
|------|---------|
| SQL | Churn rate queries, cohort analysis, revenue at risk |
| Python — pandas | Data cleaning and feature engineering |
| Python — matplotlib, seaborn | EDA charts and heatmaps |
| Python — scikit-learn | Random Forest churn prediction model |

---

## 📊 Dataset

- **Source:** [Telco Customer Churn — Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
- **Rows:** 7,043 customers
- **Fields:** Demographics, services subscribed, contract type, payment method, monthly charges, tenure, churn label

---

## 🔍 Analysis Sections

### 1. Churn Overview
- Overall churn rate across all customers
- Churn breakdown by contract type and internet service

### 2. Tenure and Charges Analysis
- Churn rate by tenure group (0-12, 13-24, 25-48, 48+ months)
- Monthly charges distribution — churned vs retained customers

### 3. Key Churn Drivers
- Payment method impact on churn
- Senior citizen churn rate
- Online security and tech support effect on retention

### 4. Correlation Heatmap
- Numeric variable correlations with churn
- Tenure vs monthly charges relationship

### 5. Machine Learning — Churn Prediction
- Random Forest Classifier trained on 80% of data
- Tested on held-out 20% test set
- Feature importance ranking — what drives churn most

### 6. ROC Curve
- Model performance visualisation
- AUC score as the primary evaluation metric

### 7. High Risk Customers
- Top 10 retained customers most likely to churn next
- Actionable list for the retention team

---

## 💡 Key Insights

| # | Insight | Action |
|---|---------|--------|
| 1 | Month-to-month contracts have 3x higher churn than two-year contracts | Incentivise customers to upgrade to annual contracts |
| 2 | Customers in their first 12 months churn at the highest rate | Introduce an onboarding retention programme for new customers |
| 3 | Electronic check payment method has the highest churn rate | Encourage auto-pay setup — reduces friction and churn |
| 4 | Customers without online security or tech support churn significantly more | Bundle security and support into base plans |
| 5 | Senior citizens churn at nearly double the rate of non-seniors | Create a dedicated senior customer support programme |

---

## 🤖 Model Performance

| Metric | Score |
|--------|-------|
| Accuracy | ~80% |
| ROC-AUC | ~0.85 |
| Top churn driver | Tenure |
| 2nd churn driver | Monthly Charges |
| 3rd churn driver | Total Charges |

---

## 📋 Business Recommendations

Based on the analysis and model findings:

1. **Target new customers first** — churn is highest in month 0-12. Assign a customer success rep to every new account for the first 90 days
2. **Offer contract upgrade incentives** — a 10% discount for switching from month-to-month to annual could significantly reduce churn
3. **Auto-pay campaign** — customers on electronic check churn most. An auto-pay incentive (small bill credit) could shift payment behaviour
4. **Bundle security services** — customers without online security churn at 2x the rate. Include it in base plans at no extra cost
5. **Use the model monthly** — run the churn prediction model every month and give the retention team the top 50 high-risk customers to call

### Revenue at Risk
The churned customers represent significant monthly recurring revenue loss. Retaining even 20% of predicted churners through proactive outreach could deliver substantial revenue recovery.

---

## ▶️ How to Run
```bash
pip install pandas matplotlib seaborn scikit-learn
python notebooks/churn_analysis.py
```

---

## 🤝 Connect

- LinkedIn: [Your LinkedIn URL]
- Email: [Your Email]

---

*Part of my Data Analyst Portfolio — [Sales Analysis](https://github.com/shravya03vemula-cmd/sales-analysis) | Marketing Performance Dashboard (coming soon)*