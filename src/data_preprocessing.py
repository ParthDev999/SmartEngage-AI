import os
import pandas as pd
import numpy as np


RAW_DATA_PATH = "data/raw/customer_engagement_data.csv"
PROCESSED_DATA_PATH = "data/processed/processed_customer_data.csv"


def load_data(file_path):
    """
    Load raw customer engagement dataset.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Dataset not found at {file_path}. Please run src/generate_dataset.py first."
        )

    df = pd.read_csv(file_path)
    return df


def handle_missing_values(df):
    """
    Handle missing values in numeric and categorical columns.
    """

    # Fill numeric missing values with median
    numeric_columns = df.select_dtypes(include=["int64", "float64"]).columns

    for col in numeric_columns:
        df[col] = df[col].fillna(df[col].median())

    # Fill text/object missing values with mode
    object_columns = df.select_dtypes(include=["object"]).columns

    for col in object_columns:
        df[col] = df[col].fillna(df[col].mode()[0])

    return df


def create_features(df):
    """
    Create professional banking engagement features.
    """

    # 1. Transaction Drop Ratio
    # It checks how much the customer's transaction activity has dropped.
    df["Transaction_Drop_Ratio"] = (
        (df["Previous_Month_Transactions"] - df["Current_Month_Transactions"])
        / (df["Previous_Month_Transactions"] + 1)
    )

    # If transaction increased, drop should not be negative.
    df["Transaction_Drop_Ratio"] = df["Transaction_Drop_Ratio"].apply(
        lambda x: max(x, 0)
    )

    # 2. Digital Engagement Score
    # Higher score means customer is more digitally active.
    df["Digital_Engagement_Score"] = (
        df["Digital_Login_Frequency"] * 0.4
        + df["UPI_Transactions"] * 0.4
        + df["Card_Usage_Frequency"] * 0.2
    )

    # 3. Inactivity Score
    # Higher value means customer has been inactive for longer.
    df["Inactivity_Score"] = df["Days_Since_Last_Login"] / 120

    # 4. Complaint Risk Score
    # More complaints means higher dissatisfaction risk.
    df["Complaint_Risk_Score"] = df["Complaint_Count"] / 8

    # 5. Product Adoption Score
    # Checks whether customer uses banking products.
    df["Product_Adoption_Score"] = (
        df["Loan_Active"]
        + df["Investment_Active"]
        + df["Salary_Account"]
        + df["Auto_Debit_Active"]
    )

    # 6. Balance to Income Ratio
    # Gives an idea of customer financial behavior.
    df["Balance_to_Income_Ratio"] = df["Account_Balance"] / (
        df["Monthly_Income"] + 1
    )

    # Remove infinite values if any
    df.replace([np.inf, -np.inf], 0, inplace=True)

    return df


def save_processed_data(df, file_path):
    """
    Save processed dataset.
    """
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(file_path, index=False)


def main():
    print("Loading raw dataset...")
    df = load_data(RAW_DATA_PATH)

    print("Raw dataset shape:", df.shape)

    print("Handling missing values...")
    df = handle_missing_values(df)

    print("Creating new banking engagement features...")
    df = create_features(df)

    print("Saving processed dataset...")
    save_processed_data(df, PROCESSED_DATA_PATH)

    print("Data preprocessing and feature engineering completed successfully!")
    print("Processed dataset saved at:", PROCESSED_DATA_PATH)
    print("Processed dataset shape:", df.shape)

    print("\nNew columns created:")
    new_columns = [
        "Transaction_Drop_Ratio",
        "Digital_Engagement_Score",
        "Inactivity_Score",
        "Complaint_Risk_Score",
        "Product_Adoption_Score",
        "Balance_to_Income_Ratio",
    ]

    for col in new_columns:
        print("-", col)

    print("\nFirst 5 rows:")
    print(df.head())


if __name__ == "__main__":
    main()