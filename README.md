# SmartEngage AI

**Agentic Banking Engagement & Churn Prevention System**

Live Demo: https://smartengage-ai-sbi.streamlit.app/

## Overview

SmartEngage AI is a machine learning based banking engagement system designed to identify customers who may become digitally inactive or disengaged. The system analyzes customer behavior such as transaction activity, digital login frequency, UPI usage, card usage, complaint count, product adoption, and days since last login to predict customer churn or disengagement risk.

The project classifies customers into **Low Risk**, **Medium Risk**, and **High Risk** categories. It also provides AI-style personalized recommendations to help banks take proactive engagement actions.

This project was built as a prototype for the **SBI Hackathon** under the theme **Agentic AI & Emerging Tech for Banking and Financial Services**, focusing on **Digital Engagement**.

## Problem Statement

Banks often face the challenge of customers slowly becoming inactive on digital banking platforms. Customers may reduce their transactions, stop using mobile banking, avoid UPI payments, ignore financial products, or become dissatisfied due to unresolved complaints.

Traditional generic campaigns are not always effective because each customer has different behavior and needs. SmartEngage AI solves this by predicting disengagement risk and recommending personalized actions for each customer.

## Key Features

* Customer churn and disengagement risk prediction
* Low, Medium, and High risk classification
* Personalized AI-style banking recommendations
* Key risk reason generation
* Single customer prediction dashboard
* Batch CSV-based customer analysis
* Risk distribution charts
* Churn probability visualization
* Downloadable prediction report
* Professional Streamlit dashboard

## Tech Stack

* Python
* Pandas
* NumPy
* Scikit-learn
* Joblib
* Streamlit
* Plotly

## Machine Learning Workflow

1. Generate simulated banking-style customer data
2. Preprocess and clean the dataset
3. Create feature engineering columns such as:

   * Transaction Drop Ratio
   * Digital Engagement Score
   * Inactivity Score
   * Complaint Risk Score
   * Product Adoption Score
   * Balance to Income Ratio
4. Train multiple ML models
5. Compare model performance
6. Save the best model
7. Use the trained model inside the Streamlit dashboard
8. Generate risk reasons and recommended actions

## Project Structure

```bash
SmartEngage-AI/
│
├── app/
│   └── streamlit_app.py
│
├── data/
│   ├── raw/
│   │   ├── customer_engagement_data.csv
│   │   └── sample_batch_customers.csv
│   │
│   └── processed/
│       └── processed_customer_data.csv
│
├── models/
│   ├── churn_model.pkl
│   ├── scaler.pkl
│   ├── model_columns.pkl
│   └── model_comparison.csv
│
├── src/
│   ├── generate_dataset.py
│   ├── data_preprocessing.py
│   ├── train_model.py
│   ├── predict.py
│   ├── recommendation_agent.py
│   └── create_sample_batch.py
│
├── requirements.txt
└── README.md
```

## How to Run Locally

### 1. Clone the repository

```bash
git clone <https://github.com/ParthDev999/SmartEngage-AI>
cd SmartEngage-AI
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Generate dataset

```bash
python src/generate_dataset.py
```

### 4. Preprocess data

```bash
python src/data_preprocessing.py
```

### 5. Train model

```bash
python src/train_model.py
```

### 6. Run Streamlit app

```bash
streamlit run app/streamlit_app.py
```

## Dashboard Pages

### Home

Displays the project overview, problem statement, solution, and key features.

### Single Customer Prediction

Allows users to enter customer banking details and predicts:

* Customer status
* Churn probability
* Risk category
* Key risk reasons
* Recommended banking actions
* Suggested customer message

### Batch Customer Analysis

Allows users to upload a CSV file and analyze multiple customers together. It also provides charts and a downloadable prediction report.

### Project Architecture

Shows the end-to-end flow of the system, technology stack, and business impact.

## Example Recommendations

SmartEngage AI can recommend actions such as:

* Assign relationship manager follow-up
* Send UPI cashback offer
* Recommend SBI YONO/mobile banking tutorial
* Prioritize complaint resolution
* Suggest SIP, mutual fund, or fixed deposit awareness
* Promote auto-debit setup
* Send reactivation reminder

## Business Impact

SmartEngage AI can help banks:

* Improve customer retention
* Increase digital banking adoption
* Reduce customer disengagement
* Improve campaign targeting
* Personalize customer communication
* Identify high-risk customers early
* Improve customer satisfaction

## Dataset Note

This project uses simulated banking-style customer data for prototype demonstration. No real customer or banking data is used.

## Future Scope

* Real-time customer engagement monitoring
* Integration with banking CRM systems
* Multilingual customer communication
* Advanced LLM-based recommendation generation
* Campaign performance tracking
* Customer segmentation dashboard
* Integration with mobile banking platforms

## Author

**Parth Sawaria**
MNIT Jaipur
GitHub: ParthDev999

## Disclaimer

This project is a prototype created for educational and hackathon purposes. It does not use real SBI customer data and is not connected to any real banking system.
