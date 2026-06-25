import os
import joblib
import pandas as pd
import numpy as np


MODEL_PATH = "models/churn_model.pkl"
SCALER_PATH = "models/scaler.pkl"
COLUMNS_PATH = "models/model_columns.pkl"


def load_model_files():
    """
    Load trained model, scaler, and model column names.
    """

    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model file not found. Please run src/train_model.py first.")

    if not os.path.exists(SCALER_PATH):
        raise FileNotFoundError("Scaler file not found. Please run src/train_model.py first.")

    if not os.path.exists(COLUMNS_PATH):
        raise FileNotFoundError("Model columns file not found. Please run src/train_model.py first.")

    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    model_columns = joblib.load(COLUMNS_PATH)

    return model, scaler, model_columns


def create_customer_features(customer_data):
    """
    Create the same engineered features for a new customer
    that we created during training.
    """

    df = pd.DataFrame([customer_data])

    df["Transaction_Drop_Ratio"] = (
        (df["Previous_Month_Transactions"] - df["Current_Month_Transactions"])
        / (df["Previous_Month_Transactions"] + 1)
    )

    df["Transaction_Drop_Ratio"] = df["Transaction_Drop_Ratio"].apply(lambda x: max(x, 0))

    df["Digital_Engagement_Score"] = (
        df["Digital_Login_Frequency"] * 0.4
        + df["UPI_Transactions"] * 0.4
        + df["Card_Usage_Frequency"] * 0.2
    )

    df["Inactivity_Score"] = df["Days_Since_Last_Login"] / 120

    df["Complaint_Risk_Score"] = df["Complaint_Count"] / 8

    df["Product_Adoption_Score"] = (
        df["Loan_Active"]
        + df["Investment_Active"]
        + df["Salary_Account"]
        + df["Auto_Debit_Active"]
    )

    df["Balance_to_Income_Ratio"] = df["Account_Balance"] / (df["Monthly_Income"] + 1)

    df.replace([np.inf, -np.inf], 0, inplace=True)

    return df


def get_risk_category(churn_probability):
    """
    Convert churn probability into Low, Medium, or High risk.
    """

    if churn_probability >= 0.70:
        return "High Risk"
    elif churn_probability >= 0.40:
        return "Medium Risk"
    else:
        return "Low Risk"


def predict_customer_risk(customer_data):
    """
    Predict customer churn/engagement risk.
    """

    model, scaler, model_columns = load_model_files()

    df = create_customer_features(customer_data)

    df = df[model_columns]

    df_scaled = scaler.transform(df)

    prediction = model.predict(df_scaled)[0]
    churn_probability = model.predict_proba(df_scaled)[0][1]

    risk_category = get_risk_category(churn_probability)

    result = {
        "prediction": int(prediction),
        "churn_probability": round(churn_probability * 100, 2),
        "risk_category": risk_category,
        "status": "At Risk / Disengaged" if prediction == 1 else "Engaged"
    }

    return result


def get_user_input():
    """
    Take customer details from terminal input.
    """

    print("\nEnter Customer Details")
    print("----------------------")

    customer_data = {
        "Age": int(input("Age: ")),
        "Tenure_Months": int(input("Tenure in months: ")),
        "Account_Balance": float(input("Account balance: ")),
        "Monthly_Income": float(input("Monthly income: ")),
        "Previous_Month_Transactions": int(input("Previous month transactions: ")),
        "Current_Month_Transactions": int(input("Current month transactions: ")),
        "Digital_Login_Frequency": int(input("Digital login frequency per month: ")),
        "UPI_Transactions": int(input("UPI transactions per month: ")),
        "Card_Usage_Frequency": int(input("Card usage frequency per month: ")),
        "Loan_Active": int(input("Loan active? Enter 1 for Yes, 0 for No: ")),
        "Investment_Active": int(input("Investment active? Enter 1 for Yes, 0 for No: ")),
        "Complaint_Count": int(input("Complaint count: ")),
        "Days_Since_Last_Login": int(input("Days since last login: ")),
        "Salary_Account": int(input("Salary account? Enter 1 for Yes, 0 for No: ")),
        "Auto_Debit_Active": int(input("Auto debit active? Enter 1 for Yes, 0 for No: "))
    }

    return customer_data


if __name__ == "__main__":
    customer_data = get_user_input()

    result = predict_customer_risk(customer_data)

    print("\nCustomer Risk Prediction Result")
    print("-------------------------------")
    print("Customer Status:", result["status"])
    print("Churn Probability:", str(result["churn_probability"]) + "%")
    print("Risk Category:", result["risk_category"])