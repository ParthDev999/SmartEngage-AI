import pandas as pd
import os

sample_data = [
    {
        "Customer_ID": "CUST_DEMO_001",
        "Age": 35,
        "Tenure_Months": 48,
        "Account_Balance": 85000,
        "Monthly_Income": 60000,
        "Previous_Month_Transactions": 45,
        "Current_Month_Transactions": 12,
        "Digital_Login_Frequency": 3,
        "UPI_Transactions": 2,
        "Card_Usage_Frequency": 5,
        "Loan_Active": 0,
        "Investment_Active": 0,
        "Complaint_Count": 4,
        "Days_Since_Last_Login": 65,
        "Salary_Account": 1,
        "Auto_Debit_Active": 0
    },
    {
        "Customer_ID": "CUST_DEMO_002",
        "Age": 29,
        "Tenure_Months": 24,
        "Account_Balance": 145000,
        "Monthly_Income": 75000,
        "Previous_Month_Transactions": 38,
        "Current_Month_Transactions": 32,
        "Digital_Login_Frequency": 14,
        "UPI_Transactions": 20,
        "Card_Usage_Frequency": 12,
        "Loan_Active": 1,
        "Investment_Active": 0,
        "Complaint_Count": 1,
        "Days_Since_Last_Login": 18,
        "Salary_Account": 1,
        "Auto_Debit_Active": 1
    },
    {
        "Customer_ID": "CUST_DEMO_003",
        "Age": 42,
        "Tenure_Months": 96,
        "Account_Balance": 350000,
        "Monthly_Income": 110000,
        "Previous_Month_Transactions": 55,
        "Current_Month_Transactions": 58,
        "Digital_Login_Frequency": 25,
        "UPI_Transactions": 45,
        "Card_Usage_Frequency": 30,
        "Loan_Active": 1,
        "Investment_Active": 1,
        "Complaint_Count": 0,
        "Days_Since_Last_Login": 4,
        "Salary_Account": 1,
        "Auto_Debit_Active": 1
    },
    {
        "Customer_ID": "CUST_DEMO_004",
        "Age": 51,
        "Tenure_Months": 132,
        "Account_Balance": 60000,
        "Monthly_Income": 45000,
        "Previous_Month_Transactions": 30,
        "Current_Month_Transactions": 8,
        "Digital_Login_Frequency": 2,
        "UPI_Transactions": 1,
        "Card_Usage_Frequency": 3,
        "Loan_Active": 0,
        "Investment_Active": 0,
        "Complaint_Count": 5,
        "Days_Since_Last_Login": 90,
        "Salary_Account": 0,
        "Auto_Debit_Active": 0
    },
    {
        "Customer_ID": "CUST_DEMO_005",
        "Age": 24,
        "Tenure_Months": 10,
        "Account_Balance": 40000,
        "Monthly_Income": 35000,
        "Previous_Month_Transactions": 22,
        "Current_Month_Transactions": 18,
        "Digital_Login_Frequency": 12,
        "UPI_Transactions": 18,
        "Card_Usage_Frequency": 7,
        "Loan_Active": 0,
        "Investment_Active": 0,
        "Complaint_Count": 1,
        "Days_Since_Last_Login": 15,
        "Salary_Account": 0,
        "Auto_Debit_Active": 1
    }
]

df = pd.DataFrame(sample_data)

os.makedirs("data/raw", exist_ok=True)

file_path = "data/raw/sample_batch_customers.csv"
df.to_csv(file_path, index=False)

print("Sample batch CSV created successfully!")
print("Saved at:", file_path)
print(df)