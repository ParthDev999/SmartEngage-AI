from predict import predict_customer_risk, get_user_input


def analyze_customer_behavior(customer_data):
    """
    Analyze customer behavior and generate risk reasons.
    """

    reasons = []

    previous_txn = customer_data["Previous_Month_Transactions"]
    current_txn = customer_data["Current_Month_Transactions"]

    transaction_drop_ratio = (previous_txn - current_txn) / (previous_txn + 1)

    if transaction_drop_ratio >= 0.50:
        reasons.append("Major drop in monthly transaction activity")
    elif transaction_drop_ratio >= 0.25:
        reasons.append("Moderate drop in monthly transaction activity")

    if customer_data["Digital_Login_Frequency"] <= 5:
        reasons.append("Low digital banking login frequency")

    if customer_data["UPI_Transactions"] <= 5:
        reasons.append("Low UPI transaction usage")

    if customer_data["Card_Usage_Frequency"] <= 5:
        reasons.append("Low card usage activity")

    if customer_data["Complaint_Count"] >= 4:
        reasons.append("High complaint count indicates dissatisfaction")
    elif customer_data["Complaint_Count"] >= 2:
        reasons.append("Customer has raised multiple complaints")

    if customer_data["Days_Since_Last_Login"] >= 60:
        reasons.append("Customer has been inactive for a long time")
    elif customer_data["Days_Since_Last_Login"] >= 30:
        reasons.append("Customer has not logged in recently")

    if customer_data["Investment_Active"] == 0:
        reasons.append("Customer is not using investment products")

    if customer_data["Auto_Debit_Active"] == 0:
        reasons.append("Customer is not using auto-debit services")

    if customer_data["Loan_Active"] == 0 and customer_data["Investment_Active"] == 0:
        reasons.append("Low product adoption with the bank")

    if len(reasons) == 0:
        reasons.append("Customer shows healthy engagement behavior")

    return reasons


def generate_recommended_actions(customer_data, risk_category):
    """
    Generate personalized banking engagement actions.
    """

    actions = []

    if risk_category == "High Risk":
        actions.append("Assign relationship manager follow-up within 24-48 hours")
        actions.append("Send personalized retention offer or digital banking benefit")

    elif risk_category == "Medium Risk":
        actions.append("Send personalized digital engagement nudge")
        actions.append("Monitor customer activity for the next 30 days")

    else:
        actions.append("Send loyalty message and cross-sell relevant banking products")

    if customer_data["Digital_Login_Frequency"] <= 5:
        actions.append("Recommend SBI YONO/mobile banking usage tutorial")

    if customer_data["UPI_Transactions"] <= 5:
        actions.append("Offer UPI cashback or digital payment reward campaign")

    if customer_data["Complaint_Count"] >= 2:
        actions.append("Prioritize complaint resolution and service recovery call")

    if customer_data["Investment_Active"] == 0:
        actions.append("Suggest SIP, mutual fund, or fixed deposit awareness campaign")

    if customer_data["Auto_Debit_Active"] == 0:
        actions.append("Promote auto-debit setup for bills, EMI, and subscriptions")

    if customer_data["Days_Since_Last_Login"] >= 30:
        actions.append("Send reactivation reminder through SMS, email, or app notification")

    # Remove duplicate actions
    unique_actions = []
    for action in actions:
        if action not in unique_actions:
            unique_actions.append(action)

    return unique_actions


def generate_customer_message(risk_category):
    """
    Generate a simple personalized customer engagement message.
    """

    if risk_category == "High Risk":
        return (
            "Dear Customer, we noticed reduced activity in your digital banking usage. "
            "Explore SBI YONO, UPI rewards, and personalized banking benefits designed for you."
        )

    elif risk_category == "Medium Risk":
        return (
            "Dear Customer, make your banking easier with SBI digital services. "
            "Use mobile banking, UPI payments, and auto-debit features for a smoother experience."
        )

    else:
        return (
            "Dear Customer, thank you for actively banking with us. "
            "Explore more SBI digital services and personalized financial products."
        )


def create_engagement_plan(customer_data):
    """
    Combine ML prediction and recommendation logic.
    """

    prediction_result = predict_customer_risk(customer_data)

    reasons = analyze_customer_behavior(customer_data)

    actions = generate_recommended_actions(
        customer_data,
        prediction_result["risk_category"]
    )

    customer_message = generate_customer_message(
        prediction_result["risk_category"]
    )

    engagement_plan = {
        "status": prediction_result["status"],
        "churn_probability": prediction_result["churn_probability"],
        "risk_category": prediction_result["risk_category"],
        "risk_reasons": reasons,
        "recommended_actions": actions,
        "customer_message": customer_message
    }

    return engagement_plan


if __name__ == "__main__":
    customer_data = get_user_input()

    engagement_plan = create_engagement_plan(customer_data)

    print("\nSmartEngage AI Recommendation Report")
    print("------------------------------------")
    print("Customer Status:", engagement_plan["status"])
    print("Churn Probability:", str(engagement_plan["churn_probability"]) + "%")
    print("Risk Category:", engagement_plan["risk_category"])

    print("\nKey Risk Reasons:")
    for reason in engagement_plan["risk_reasons"]:
        print("-", reason)

    print("\nRecommended Bank Actions:")
    for action in engagement_plan["recommended_actions"]:
        print("-", action)

    print("\nSuggested Customer Message:")
    print(engagement_plan["customer_message"])