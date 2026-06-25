import numpy as np
import pandas as pd
import os

# For same output every time
np.random.seed(42)

# Number of customers
n_customers = 3000

# -------------------------------
# Generate customer basic details
# -------------------------------
customer_ids = [f"CUST{100000 + i}" for i in range(n_customers)]

age = np.random.randint(18, 70, n_customers)
tenure_months = np.random.randint(1, 180, n_customers)

monthly_income = np.random.randint(15000, 250000, n_customers)
account_balance = np.random.randint(1000, 1000000, n_customers)

previous_month_transactions = np.random.randint(5, 90, n_customers)
current_month_transactions = np.random.randint(0, 90, n_customers)

digital_login_frequency = np.random.randint(0, 35, n_customers)
upi_transactions = np.random.randint(0, 80, n_customers)
card_usage_frequency = np.random.randint(0, 50, n_customers)

loan_active = np.random.choice([0, 1], n_customers, p=[0.65, 0.35])
investment_active = np.random.choice([0, 1], n_customers, p=[0.60, 0.40])
salary_account = np.random.choice([0, 1], n_customers, p=[0.45, 0.55])
auto_debit_active = np.random.choice([0, 1], n_customers, p=[0.55, 0.45])

complaint_count = np.random.poisson(1.2, n_customers)
complaint_count = np.clip(complaint_count, 0, 8)

days_since_last_login = np.random.randint(0, 120, n_customers)

# -------------------------------
# Create risk logic for churn
# -------------------------------

transaction_drop_ratio = (
    (previous_month_transactions - current_month_transactions)
    / (previous_month_transactions + 1)
)

risk_score = (
    0.25 * (days_since_last_login / 120)
    + 0.20 * (1 - digital_login_frequency / 35)
    + 0.20 * np.maximum(transaction_drop_ratio, 0)
    + 0.15 * (complaint_count / 8)
    + 0.10 * (1 - upi_transactions / 80)
    + 0.05 * (1 - investment_active)
    + 0.05 * (1 - auto_debit_active)
)

# Add slight randomness
risk_score = risk_score + np.random.normal(0, 0.05, n_customers)

# Convert risk score into churn label
churn = (risk_score > 0.48).astype(int)

# -------------------------------
# Create DataFrame
# -------------------------------
df = pd.DataFrame({
    "Customer_ID": customer_ids,
    "Age": age,
    "Tenure_Months": tenure_months,
    "Account_Balance": account_balance,
    "Monthly_Income": monthly_income,
    "Previous_Month_Transactions": previous_month_transactions,
    "Current_Month_Transactions": current_month_transactions,
    "Digital_Login_Frequency": digital_login_frequency,
    "UPI_Transactions": upi_transactions,
    "Card_Usage_Frequency": card_usage_frequency,
    "Loan_Active": loan_active,
    "Investment_Active": investment_active,
    "Complaint_Count": complaint_count,
    "Days_Since_Last_Login": days_since_last_login,
    "Salary_Account": salary_account,
    "Auto_Debit_Active": auto_debit_active,
    "Churn": churn
})

# -------------------------------
# Save dataset
# -------------------------------
os.makedirs("data/raw", exist_ok=True)

df.to_csv("data/raw/customer_engagement_data.csv", index=False)

print("Dataset generated successfully!")
print("Shape:", df.shape)
print(df.head())
print("\nChurn distribution:")
print(df["Churn"].value_counts())