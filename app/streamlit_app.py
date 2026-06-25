import os
import sys
import html
import pandas as pd
import streamlit as st
import plotly.express as px

# Add src folder to Python path
sys.path.append(os.path.abspath("src"))

from recommendation_agent import create_engagement_plan


st.set_page_config(
    page_title="SmartEngage AI",
    page_icon="🏦",
    layout="wide"
)


# -------------------------------------------------
# Custom CSS
# -------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #111827 50%, #020617 100%);
        color: #e5e7eb;
    }

    .main-title {
        font-size: 46px;
        font-weight: 900;
        color: #f8fafc;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 19px;
        color: #cbd5e1;
        margin-top: 4px;
        margin-bottom: 22px;
    }

    .section-card {
        background: rgba(15, 23, 42, 0.92);
        padding: 24px;
        border-radius: 18px;
        border: 1px solid rgba(148, 163, 184, 0.25);
        box-shadow: 0 12px 30px rgba(0,0,0,0.25);
        margin-bottom: 18px;
    }

    .feature-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        padding: 22px;
        border-radius: 16px;
        border: 1px solid rgba(96, 165, 250, 0.25);
        box-shadow: 0 8px 20px rgba(0,0,0,0.20);
        min-height: 135px;
    }

    .feature-title {
        color: #93c5fd;
        font-size: 20px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .feature-text {
        color: #d1d5db;
        font-size: 15px;
        line-height: 1.6;
    }

    .risk-card {
        padding: 24px;
        border-radius: 18px;
        color: white;
        box-shadow: 0 14px 35px rgba(0,0,0,0.35);
        margin-top: 18px;
        margin-bottom: 20px;
    }

    .risk-high {
        background: linear-gradient(135deg, #7f1d1d, #dc2626);
        border: 1px solid #fca5a5;
    }

    .risk-medium {
        background: linear-gradient(135deg, #92400e, #f59e0b);
        border: 1px solid #fde68a;
    }

    .risk-low {
        background: linear-gradient(135deg, #065f46, #10b981);
        border: 1px solid #a7f3d0;
    }

    .risk-title {
        font-size: 32px;
        font-weight: 900;
        margin-bottom: 12px;
        color: #ffffff;
    }

    .risk-text {
        font-size: 17px;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 6px;
    }

    .compact-card {
        background: #0f172a;
        border: 1px solid rgba(148, 163, 184, 0.28);
        border-radius: 16px;
        padding: 20px 22px;
        box-shadow: 0 8px 22px rgba(0,0,0,0.22);
        margin-bottom: 16px;
    }

    .compact-card-title {
        font-size: 21px;
        font-weight: 850;
        color: #bfdbfe;
        margin-bottom: 12px;
    }

    .compact-card ul {
        margin-top: 8px;
        margin-bottom: 4px;
        padding-left: 22px;
    }

    .compact-card li {
        color: #e5e7eb;
        font-size: 15.5px;
        line-height: 1.55;
        margin-bottom: 7px;
    }

    .message-box {
        background: linear-gradient(135deg, #172554, #1e3a8a);
        border: 1px solid #60a5fa;
        padding: 20px;
        border-radius: 16px;
        color: #ffffff;
        font-size: 16.5px;
        line-height: 1.7;
        box-shadow: 0 8px 22px rgba(0,0,0,0.25);
        margin-bottom: 16px;
    }

    .metric-box {
        background: linear-gradient(135deg, #1e293b, #111827);
        border: 1px solid rgba(96, 165, 250, 0.35);
        padding: 18px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 8px 18px rgba(0,0,0,0.22);
    }

    .metric-number {
        color: #60a5fa;
        font-size: 30px;
        font-weight: 900;
    }

    .metric-label {
        color: #cbd5e1;
        font-size: 14px;
        font-weight: 600;
    }

    div[data-testid="stSidebar"] {
        background: #020617;
        border-right: 1px solid rgba(148, 163, 184, 0.2);
    }

    div[data-testid="stMetricValue"] {
        color: #60a5fa;
    }

    .stButton > button {
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1.5rem;
        font-weight: 800;
        font-size: 16px;
        box-shadow: 0 8px 18px rgba(37, 99, 235, 0.35);
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8, #6d28d9);
        color: white;
        border: none;
    }

    h1, h2, h3 {
        color: #f8fafc;
    }

    p, li, label {
        color: #e5e7eb;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# -------------------------------------------------
# Helper functions
# -------------------------------------------------
def html_list(items):
    """
    Convert Python list into safe HTML bullet list.
    """
    if not items:
        return "<ul><li>No major risk found.</li></ul>"

    list_items = "".join([f"<li>{html.escape(str(item))}</li>" for item in items])
    return f"<ul>{list_items}</ul>"


def display_risk_box(risk_category, status, probability):
    if risk_category == "High Risk":
        css_class = "risk-high"
        icon = "🚨"
    elif risk_category == "Medium Risk":
        css_class = "risk-medium"
        icon = "⚠️"
    else:
        css_class = "risk-low"
        icon = "✅"

    st.markdown(
        f"""
        <div class="risk-card {css_class}">
            <div class="risk-title">{icon} {risk_category}</div>
            <div class="risk-text">Customer Status: {html.escape(str(status))}</div>
            <div class="risk-text">Churn / Disengagement Probability: {probability}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def collect_customer_input():
    st.markdown("### Enter Customer Banking Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input("Age", min_value=18, max_value=80, value=35)
        tenure_months = st.number_input("Tenure in Months", min_value=1, max_value=240, value=48)
        account_balance = st.number_input("Account Balance", min_value=0.0, value=85000.0)
        monthly_income = st.number_input("Monthly Income", min_value=0.0, value=60000.0)
        previous_month_transactions = st.number_input(
            "Previous Month Transactions",
            min_value=0,
            max_value=150,
            value=45
        )

    with col2:
        current_month_transactions = st.number_input(
            "Current Month Transactions",
            min_value=0,
            max_value=150,
            value=12
        )
        digital_login_frequency = st.number_input(
            "Digital Login Frequency / Month",
            min_value=0,
            max_value=60,
            value=3
        )
        upi_transactions = st.number_input(
            "UPI Transactions / Month",
            min_value=0,
            max_value=150,
            value=2
        )
        card_usage_frequency = st.number_input(
            "Card Usage Frequency / Month",
            min_value=0,
            max_value=100,
            value=5
        )
        complaint_count = st.number_input(
            "Complaint Count",
            min_value=0,
            max_value=20,
            value=4
        )

    with col3:
        days_since_last_login = st.number_input(
            "Days Since Last Login",
            min_value=0,
            max_value=365,
            value=65
        )

        loan_active = st.selectbox("Loan Active?", ["No", "Yes"])
        investment_active = st.selectbox("Investment Active?", ["No", "Yes"])
        salary_account = st.selectbox("Salary Account?", ["Yes", "No"])
        auto_debit_active = st.selectbox("Auto Debit Active?", ["No", "Yes"])

    customer_data = {
        "Age": age,
        "Tenure_Months": tenure_months,
        "Account_Balance": account_balance,
        "Monthly_Income": monthly_income,
        "Previous_Month_Transactions": previous_month_transactions,
        "Current_Month_Transactions": current_month_transactions,
        "Digital_Login_Frequency": digital_login_frequency,
        "UPI_Transactions": upi_transactions,
        "Card_Usage_Frequency": card_usage_frequency,
        "Loan_Active": 1 if loan_active == "Yes" else 0,
        "Investment_Active": 1 if investment_active == "Yes" else 0,
        "Complaint_Count": complaint_count,
        "Days_Since_Last_Login": days_since_last_login,
        "Salary_Account": 1 if salary_account == "Yes" else 0,
        "Auto_Debit_Active": 1 if auto_debit_active == "Yes" else 0
    }

    return customer_data


def predict_batch_data(df):
    results = []

    for _, row in df.iterrows():
        customer_data = row.to_dict()

        try:
            plan = create_engagement_plan(customer_data)

            results.append({
                "Customer_ID": customer_data.get("Customer_ID", "Unknown"),
                "Risk_Category": plan["risk_category"],
                "Status": plan["status"],
                "Churn_Probability": plan["churn_probability"],
                "Top_Risk_Reason": plan["risk_reasons"][0] if plan["risk_reasons"] else "No major risk",
                "Recommended_Action": plan["recommended_actions"][0] if plan["recommended_actions"] else "No action required"
            })

        except Exception as e:
            results.append({
                "Customer_ID": customer_data.get("Customer_ID", "Unknown"),
                "Risk_Category": "Error",
                "Status": "Error",
                "Churn_Probability": 0,
                "Top_Risk_Reason": str(e),
                "Recommended_Action": "Check input data"
            })

    return pd.DataFrame(results)


def section_header(title, subtitle=None):
    st.markdown(f"## {title}")
    if subtitle:
        st.markdown(f"<p class='subtitle'>{subtitle}</p>", unsafe_allow_html=True)


# -------------------------------------------------
# Sidebar
# -------------------------------------------------
st.sidebar.markdown("## 🏦 SmartEngage AI")
st.sidebar.markdown("Agentic Banking Engagement System")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Single Customer Prediction",
        "Batch Customer Analysis",
        "Project Architecture"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "SBI Hackathon @ GFF 2026\n\n"
    "Theme: Agentic AI & Emerging Tech\n\n"
    "Problem Statement: Digital Engagement"
)


# -------------------------------------------------
# Home Page
# -------------------------------------------------
if page == "Home":
    st.markdown('<p class="main-title">SmartEngage AI</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Agentic Banking Engagement & Churn Prevention System</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-card">
            <h3>Problem Statement</h3>
            <p>
            Banks often face the challenge of customers becoming digitally inactive over time.
            Customers may reduce transactions, stop using mobile banking, avoid UPI payments,
            ignore financial products, or become dissatisfied due to unresolved complaints.
            Generic campaigns are not enough because every customer has different behavior.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-card">
            <h3>Proposed Solution</h3>
            <p>
            SmartEngage AI predicts customer disengagement risk using machine learning and
            generates personalized engagement actions through an AI-style recommendation agent.
            The system helps banking teams identify high-risk customers early and take proactive action.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-title">ML Risk Engine</div>
                <div class="feature-text">
                Predicts customer churn or disengagement probability using banking behavior signals.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-title">AI Recommendation Agent</div>
                <div class="feature-text">
                Generates reasons, suggested actions, and customer engagement messages.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-title">Banking Dashboard</div>
                <div class="feature-text">
                Helps bank teams monitor risk levels and take targeted engagement actions.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    section_header("Key Features")

    st.markdown(
        """
        - Customer churn / disengagement risk prediction  
        - Low, Medium, and High risk classification  
        - Behavioral risk reason generation  
        - Personalized banking engagement recommendations  
        - Single customer prediction  
        - CSV-based batch customer analysis  
        - Downloadable prediction report  
        """
    )


# -------------------------------------------------
# Single Customer Prediction Page
# -------------------------------------------------
elif page == "Single Customer Prediction":
    section_header(
        "Single Customer Risk Prediction",
        "Enter banking behavior details and generate a personalized engagement plan."
    )

    customer_data = collect_customer_input()

    st.markdown("---")

    if st.button("Predict Customer Risk"):
        engagement_plan = create_engagement_plan(customer_data)

        display_risk_box(
            engagement_plan["risk_category"],
            engagement_plan["status"],
            engagement_plan["churn_probability"]
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                f"""
                <div class="compact-card">
                    <div class="compact-card-title">Key Risk Reasons</div>
                    {html_list(engagement_plan["risk_reasons"])}
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div class="compact-card">
                    <div class="compact-card-title">Recommended Bank Actions</div>
                    {html_list(engagement_plan["recommended_actions"])}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("### Suggested Customer Message")
        st.markdown(
            f"""
            <div class="message-box">
                {html.escape(str(engagement_plan["customer_message"]))}
            </div>
            """,
            unsafe_allow_html=True
        )


# -------------------------------------------------
# Batch Customer Analysis Page
# -------------------------------------------------
elif page == "Batch Customer Analysis":
    section_header(
        "Batch Customer Risk Analysis",
        "Upload a CSV file and analyze risk category for multiple customers."
    )

    uploaded_file = st.file_uploader("Upload Customer CSV File", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

        st.markdown("### Uploaded Data Preview")
        st.dataframe(df.head(), use_container_width=True)

        required_columns = [
            "Age",
            "Tenure_Months",
            "Account_Balance",
            "Monthly_Income",
            "Previous_Month_Transactions",
            "Current_Month_Transactions",
            "Digital_Login_Frequency",
            "UPI_Transactions",
            "Card_Usage_Frequency",
            "Loan_Active",
            "Investment_Active",
            "Complaint_Count",
            "Days_Since_Last_Login",
            "Salary_Account",
            "Auto_Debit_Active"
        ]

        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            st.error("Missing required columns:")
            st.write(missing_columns)

        else:
            if st.button("Analyze Customers"):
                result_df = predict_batch_data(df)

                st.markdown("### Prediction Results")
                st.dataframe(result_df, use_container_width=True)

                high_risk_count = (result_df["Risk_Category"] == "High Risk").sum()
                medium_risk_count = (result_df["Risk_Category"] == "Medium Risk").sum()
                low_risk_count = (result_df["Risk_Category"] == "Low Risk").sum()

                total_customers = len(result_df)

                st.markdown("---")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.markdown(
                        f"""
                        <div class="metric-box">
                            <div class="metric-number">{total_customers}</div>
                            <div class="metric-label">Total Customers</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col2:
                    st.markdown(
                        f"""
                        <div class="metric-box">
                            <div class="metric-number" style="color:#f87171;">{high_risk_count}</div>
                            <div class="metric-label">High Risk</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col3:
                    st.markdown(
                        f"""
                        <div class="metric-box">
                            <div class="metric-number" style="color:#fbbf24;">{medium_risk_count}</div>
                            <div class="metric-label">Medium Risk</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col4:
                    st.markdown(
                        f"""
                        <div class="metric-box">
                            <div class="metric-number" style="color:#34d399;">{low_risk_count}</div>
                            <div class="metric-label">Low Risk</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st.markdown("---")

                risk_count_df = result_df["Risk_Category"].value_counts().reset_index()
                risk_count_df.columns = ["Risk Category", "Count"]

                fig = px.pie(
                    risk_count_df,
                    names="Risk Category",
                    values="Count",
                    title="Customer Risk Distribution",
                    color="Risk Category",
                    color_discrete_map={
                        "High Risk": "#ef4444",
                        "Medium Risk": "#f59e0b",
                        "Low Risk": "#10b981"
                    }
                )

                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#e5e7eb"
                )

                st.plotly_chart(fig, use_container_width=True)

                fig2 = px.histogram(
                    result_df,
                    x="Churn_Probability",
                    nbins=20,
                    title="Churn Probability Distribution",
                    color_discrete_sequence=["#60a5fa"]
                )

                fig2.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#e5e7eb"
                )

                st.plotly_chart(fig2, use_container_width=True)

                csv = result_df.to_csv(index=False).encode("utf-8")

                st.download_button(
                    label="Download Prediction Report",
                    data=csv,
                    file_name="smartengage_prediction_report.csv",
                    mime="text/csv"
                )

    else:
        st.info("Upload your customer CSV file to start batch analysis.")


# -------------------------------------------------
# Project Architecture Page
# -------------------------------------------------
elif page == "Project Architecture":
    section_header(
        "Project Architecture",
        "End-to-end flow of SmartEngage AI."
    )

    st.markdown(
        """
        <div class="section-card">
            <h3>System Flow</h3>
            <p>
            Customer Banking Data → Data Preprocessing → Feature Engineering → ML Risk Prediction →
            Risk Classification → AI Recommendation Agent → Dashboard + Engagement Action
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.code(
        """
Customer Banking Data
        ↓
Data Preprocessing
        ↓
Feature Engineering
        ↓
ML-Based Churn / Engagement Risk Prediction
        ↓
Risk Category Classification
        ↓
AI Recommendation Agent
        ↓
Banking Dashboard + Suggested Engagement Action
        """,
        language="text"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="section-card">
                <h3>Technology Stack</h3>
                <p>
                Python, Pandas, NumPy, Scikit-learn, Machine Learning Classification Models,
                Streamlit Dashboard, Plotly Visualizations, and Joblib for model saving.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="section-card">
                <h3>Business Impact</h3>
                <p>
                SmartEngage AI can help banks improve customer retention, increase digital banking adoption,
                reduce disengagement, improve campaign targeting, and personalize customer communication.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )