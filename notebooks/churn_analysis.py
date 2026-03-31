import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (classification_report, confusion_matrix,
                             roc_auc_score, roc_curve)
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# Style
plt.rcParams.update({
    'figure.facecolor': '#FAFAFA',
    'axes.facecolor':   '#FAFAFA',
    'axes.spines.top':  False,
    'axes.spines.right':False,
    'font.family':      'sans-serif',
    'axes.grid':        True,
    'grid.alpha':       0.3,
})
PALETTE = ['#2563EB', '#DC2626', '#16A34A', '#D97706', '#7C3AED']

# ============================================================
# 1. LOAD DATA
# ============================================================
df = pd.read_csv('data/telco_churn.csv')

# Clean TotalCharges column
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)

# Binary churn column
df['Churn_Binary'] = (df['Churn'] == 'Yes').astype(int)

print("Dataset shape:", df.shape)
print("\nChurn distribution:")
print(df['Churn'].value_counts())
print(f"\nOverall churn rate: {df['Churn_Binary'].mean()*100:.1f}%")

# ============================================================
# 2. CHURN OVERVIEW
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Churn pie chart
churn_counts = df['Churn'].value_counts()
axes[0].pie(churn_counts, labels=['Retained', 'Churned'],
            colors=[PALETTE[0], PALETTE[1]],
            autopct='%1.1f%%', startangle=90,
            wedgeprops=dict(edgecolor='white', linewidth=2))
axes[0].set_title('Overall Churn Rate', fontweight='bold')

# Churn by contract type
contract_churn = df.groupby('Contract')['Churn_Binary'].mean() * 100
bars = axes[1].bar(contract_churn.index, contract_churn.values,
                   color=[PALETTE[1], PALETTE[2], PALETTE[0]])
axes[1].set_title('Churn Rate by Contract Type', fontweight='bold')
axes[1].set_ylabel('Churn Rate (%)')
for bar, val in zip(bars, contract_churn.values):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                 f'{val:.1f}%', ha='center', fontweight='bold', fontsize=10)

# Churn by internet service
internet_churn = df.groupby('InternetService')['Churn_Binary'].mean() * 100
bars2 = axes[2].bar(internet_churn.index, internet_churn.values,
                    color=PALETTE[:3])
axes[2].set_title('Churn Rate by Internet Service', fontweight='bold')
axes[2].set_ylabel('Churn Rate (%)')
for bar, val in zip(bars2, internet_churn.values):
    axes[2].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                 f'{val:.1f}%', ha='center', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig('outputs/01_churn_overview.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved: outputs/01_churn_overview.png")

# ============================================================
# 3. CHURN BY TENURE
# ============================================================
df['Tenure Group'] = pd.cut(df['tenure'],
    bins=[0, 12, 24, 48, 72],
    labels=['0-12 months', '13-24 months', '25-48 months', '48+ months'])

tenure_churn = df.groupby('Tenure Group', observed=True)['Churn_Binary'].mean() * 100

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

colors_t = [PALETTE[1] if v > 30 else PALETTE[0] for v in tenure_churn.values]
bars3 = axes[0].bar(tenure_churn.index, tenure_churn.values, color=colors_t)
axes[0].set_title('Churn Rate by Tenure Group', fontweight='bold')
axes[0].set_ylabel('Churn Rate (%)')
axes[0].set_xlabel('Tenure')
for bar, val in zip(bars3, tenure_churn.values):
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                 f'{val:.1f}%', ha='center', fontweight='bold', fontsize=10)

# Monthly charges distribution — churned vs retained
churned     = df[df['Churn'] == 'Yes']['MonthlyCharges']
retained    = df[df['Churn'] == 'No']['MonthlyCharges']
axes[1].hist(retained, bins=30, alpha=0.6, color=PALETTE[0], label='Retained')
axes[1].hist(churned,  bins=30, alpha=0.6, color=PALETTE[1], label='Churned')
axes[1].set_title('Monthly Charges — Churned vs Retained', fontweight='bold')
axes[1].set_xlabel('Monthly Charges ($)')
axes[1].set_ylabel('Number of Customers')
axes[1].legend(frameon=False)

plt.tight_layout()
plt.savefig('outputs/02_tenure_charges.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved: outputs/02_tenure_charges.png")

# ============================================================
# 4. CHURN BY KEY FACTORS
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Payment method
payment_churn = df.groupby('PaymentMethod')['Churn_Binary'].mean() * 100
payment_churn = payment_churn.sort_values(ascending=True)
axes[0,0].barh(payment_churn.index, payment_churn.values, color=PALETTE[0])
axes[0,0].set_title('Churn Rate by Payment Method', fontweight='bold')
axes[0,0].set_xlabel('Churn Rate (%)')

# Senior citizen
senior_churn = df.groupby('SeniorCitizen')['Churn_Binary'].mean() * 100
axes[0,1].bar(['Non-Senior', 'Senior'], senior_churn.values,
              color=[PALETTE[0], PALETTE[1]])
axes[0,1].set_title('Churn Rate by Senior Citizen Status', fontweight='bold')
axes[0,1].set_ylabel('Churn Rate (%)')
for i, val in enumerate(senior_churn.values):
    axes[0,1].text(i, val + 0.5, f'{val:.1f}%', ha='center',
                   fontweight='bold', fontsize=10)

# Online security
security_churn = df.groupby('OnlineSecurity')['Churn_Binary'].mean() * 100
axes[1,0].bar(security_churn.index, security_churn.values, color=PALETTE[:3])
axes[1,0].set_title('Churn Rate by Online Security', fontweight='bold')
axes[1,0].set_ylabel('Churn Rate (%)')

# Tech support
tech_churn = df.groupby('TechSupport')['Churn_Binary'].mean() * 100
axes[1,1].bar(tech_churn.index, tech_churn.values, color=PALETTE[:3])
axes[1,1].set_title('Churn Rate by Tech Support', fontweight='bold')
axes[1,1].set_ylabel('Churn Rate (%)')

plt.tight_layout()
plt.savefig('outputs/03_churn_factors.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved: outputs/03_churn_factors.png")

# ============================================================
# 5. CORRELATION HEATMAP
# ============================================================
numeric_cols = ['tenure', 'MonthlyCharges', 'TotalCharges', 'Churn_Binary']
corr = df[numeric_cols].corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdYlGn',
            center=0, ax=ax, linewidths=0.5,
            cbar_kws={'shrink': 0.8})
ax.set_title('Correlation Heatmap — Key Numeric Variables', fontweight='bold')
plt.tight_layout()
plt.savefig('outputs/04_correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved: outputs/04_correlation_heatmap.png")

# ============================================================
# 6. MACHINE LEARNING — CHURN PREDICTION
# ============================================================
print("\n── Building Churn Prediction Model ──────────────")

# Prepare features
ml_df = df.copy()
le = LabelEncoder()
categorical_cols = ml_df.select_dtypes(include='object').columns.tolist()
categorical_cols = [c for c in categorical_cols
                    if c not in ['customerID', 'Churn']]

for col in categorical_cols:
    ml_df[col] = le.fit_transform(ml_df[col].astype(str))

# Drop unused columns
ml_df = ml_df.drop(['customerID', 'Churn', 'Tenure Group'], axis=1)

X = ml_df.drop('Churn_Binary', axis=1)
y = ml_df['Churn_Binary']

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# Evaluate
y_pred  = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]
auc     = roc_auc_score(y_test, y_proba)

print(f"\nModel Accuracy:  {model.score(X_test, y_test)*100:.1f}%")
print(f"ROC-AUC Score:   {auc:.3f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Retained', 'Churned']))

# ============================================================
# 7. MODEL RESULTS — CONFUSION MATRIX + FEATURE IMPORTANCE
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0],
            xticklabels=['Retained', 'Churned'],
            yticklabels=['Retained', 'Churned'])
axes[0].set_title(f'Confusion Matrix\nROC-AUC: {auc:.3f}', fontweight='bold')
axes[0].set_ylabel('Actual')
axes[0].set_xlabel('Predicted')

# Feature importance
feat_imp = pd.Series(model.feature_importances_, index=X.columns)
feat_imp = feat_imp.nlargest(10).sort_values()
axes[1].barh(feat_imp.index, feat_imp.values, color=PALETTE[0])
axes[1].set_title('Top 10 Features Driving Churn', fontweight='bold')
axes[1].set_xlabel('Feature Importance Score')

plt.tight_layout()
plt.savefig('outputs/05_model_results.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved: outputs/05_model_results.png")

# ============================================================
# 8. ROC CURVE
# ============================================================
fpr, tpr, _ = roc_curve(y_test, y_proba)

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(fpr, tpr, color=PALETTE[0], linewidth=2.5,
        label=f'Random Forest (AUC = {auc:.3f})')
ax.plot([0, 1], [0, 1], color='gray', linewidth=1,
        linestyle='--', label='Random guess')
ax.fill_between(fpr, tpr, alpha=0.1, color=PALETTE[0])
ax.set_title('ROC Curve — Churn Prediction Model', fontweight='bold')
ax.set_xlabel('False Positive Rate')
ax.set_ylabel('True Positive Rate')
ax.legend(frameon=False)
plt.tight_layout()
plt.savefig('outputs/06_roc_curve.png', dpi=150, bbox_inches='tight')
plt.show()
print("Saved: outputs/06_roc_curve.png")

# ============================================================
# 9. HIGH RISK CUSTOMERS
# ============================================================
df['Churn_Probability'] = model.predict_proba(X)[:, 1]
high_risk = (df[df['Churn'] == 'No']
             .nlargest(10, 'Churn_Probability')
             [['customerID', 'tenure', 'Contract',
               'MonthlyCharges', 'Churn_Probability']])

print("\n── Top 10 High Risk Customers (likely to churn next) ──")
print(high_risk.to_string(index=False))

print("\n✅ All charts saved to outputs/ folder!")