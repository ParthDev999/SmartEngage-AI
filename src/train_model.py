import os
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix
)


PROCESSED_DATA_PATH = "data/processed/processed_customer_data.csv"

MODEL_PATH = "models/churn_model.pkl"
SCALER_PATH = "models/scaler.pkl"
COLUMNS_PATH = "models/model_columns.pkl"
MODEL_COMPARISON_PATH = "models/model_comparison.csv"
FEATURE_IMPORTANCE_PATH = "models/feature_importance.csv"


def load_processed_data(file_path):
    """
    Load the processed customer dataset.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Processed dataset not found at {file_path}. Please run src/data_preprocessing.py first."
        )

    df = pd.read_csv(file_path)
    return df


def prepare_features_and_target(df):
    """
    Separate input features and target column.
    """

    # We do not use Customer_ID for prediction because it is only an identifier.
    X = df.drop(columns=["Customer_ID", "Churn"])
    y = df["Churn"]

    return X, y


def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    """
    Train multiple ML models and compare their performance.
    """

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
        "Random Forest": RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            random_state=42,
            class_weight="balanced"
        ),
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=3,
            random_state=42
        )
    }

    results = []
    trained_models = {}

    for model_name, model in models.items():
        print(f"\nTraining {model_name}...")

        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        if hasattr(model, "predict_proba"):
            y_prob = model.predict_proba(X_test)[:, 1]
            roc_auc = roc_auc_score(y_test, y_prob)
        else:
            roc_auc = 0

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        results.append({
            "Model": model_name,
            "Accuracy": accuracy,
            "Precision": precision,
            "Recall": recall,
            "F1_Score": f1,
            "ROC_AUC": roc_auc
        })

        trained_models[model_name] = model

        print(f"{model_name} Results:")
        print("Accuracy:", round(accuracy, 4))
        print("Precision:", round(precision, 4))
        print("Recall:", round(recall, 4))
        print("F1 Score:", round(f1, 4))
        print("ROC AUC:", round(roc_auc, 4))

        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))

        print("Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))

    results_df = pd.DataFrame(results)

    # Select best model based on F1 score
    best_model_name = results_df.sort_values(by="F1_Score", ascending=False).iloc[0]["Model"]
    best_model = trained_models[best_model_name]

    return best_model_name, best_model, results_df


def save_feature_importance(model, feature_names):
    """
    Save feature importance if the model supports it.
    """

    if hasattr(model, "feature_importances_"):
        importance_df = pd.DataFrame({
            "Feature": feature_names,
            "Importance": model.feature_importances_
        })

        importance_df = importance_df.sort_values(by="Importance", ascending=False)

        importance_df.to_csv(FEATURE_IMPORTANCE_PATH, index=False)

        print("\nFeature importance saved at:", FEATURE_IMPORTANCE_PATH)
        print("\nTop 10 Important Features:")
        print(importance_df.head(10))

    else:
        print("\nSelected model does not support feature importance directly.")


def main():
    print("Loading processed dataset...")
    df = load_processed_data(PROCESSED_DATA_PATH)

    print("Dataset shape:", df.shape)

    print("\nPreparing features and target...")
    X, y = prepare_features_and_target(df)

    print("Feature columns:")
    print(list(X.columns))

    print("\nTarget distribution:")
    print(y.value_counts())

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # Scaling features
    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Convert scaled arrays back to DataFrame
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X.columns)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X.columns)

    print("\nTraining and evaluating models...")
    best_model_name, best_model, results_df = train_and_evaluate_models(
        X_train_scaled,
        X_test_scaled,
        y_train,
        y_test
    )

    print("\nModel Comparison:")
    print(results_df)

    print("\nBest Model Selected:", best_model_name)

    # Create models folder
    os.makedirs("models", exist_ok=True)

    # Save best model, scaler, and columns
    joblib.dump(best_model, MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(list(X.columns), COLUMNS_PATH)

    # Save model comparison
    results_df.to_csv(MODEL_COMPARISON_PATH, index=False)

    print("\nSaved files:")
    print("-", MODEL_PATH)
    print("-", SCALER_PATH)
    print("-", COLUMNS_PATH)
    print("-", MODEL_COMPARISON_PATH)

    # Save feature importance
    save_feature_importance(best_model, X.columns)

    print("\nModel training completed successfully!")


if __name__ == "__main__":
    main()