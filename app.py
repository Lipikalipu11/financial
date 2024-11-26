import streamlit as st
import pandas as pd
import pickle

# Load the family scores pickle file
with open('family_scores.pkl', 'rb') as file:
    family_scores = pickle.load(file)

# Title of the app
st.title("Family Financial Score Tracker")

# Sidebar for user input
st.sidebar.header("Input Your Financial Data")

# Input fields for user data
savings = st.sidebar.number_input("Savings", min_value=0.0, step=0.1)
income = st.sidebar.number_input("Income", min_value=0.0, step=0.1)
monthly_expenses = st.sidebar.number_input("Monthly Expenses", min_value=0.0, step=0.1)
loan_payments = st.sidebar.number_input("Loan Payments", min_value=0.0, step=0.1)
credit_card_spending = st.sidebar.number_input("Credit Card Spending", min_value=0.0, step=0.1)
financial_goals_met = st.sidebar.slider("Financial Goals Met (%)", 0, 100, 50)
category = st.sidebar.selectbox("Spending Category", ['Travel', 'Entertainment', 'Other'])

# Calculating Financial Metrics
savings_to_income = (savings / income) * 100 if income > 0 else 0
monthly_expenses_ratio = (monthly_expenses / income) * 100 if income > 0 else 0
loan_payments_ratio = (loan_payments / income) * 100 if income > 0 else 0
credit_card_spending_ratio = (credit_card_spending / income) * 100 if income > 0 else 0

# Scoring Function
def calculate_financial_scores():
    savings_score = min(20, savings_to_income / 5)
    expenses_score = max(0, 15 - monthly_expenses_ratio / 10)
    loan_score = max(0, 10 - loan_payments_ratio / 5)
    credit_card_score = max(0, 10 - credit_card_spending_ratio / 5)
    category_score = 20 if category not in ['Travel', 'Entertainment'] else 10
    goals_score = min(25, financial_goals_met)
    total_score = savings_score + expenses_score + loan_score + credit_card_score + category_score + goals_score
    return total_score

# Compute the financial score
if st.sidebar.button("Calculate Financial Score"):
    financial_score = calculate_financial_scores()
    st.write(f"Your Financial Score: **{financial_score:.2f}**")
    if financial_score < 50:
        st.warning("Consider reducing discretionary spending or increasing savings to improve your score.")
    elif financial_score < 75:
        st.info("Good job! Improving savings further can enhance your score.")
    else:
        st.success("Excellent! You have a healthy financial score.")

# Display family scores
st.header("Family Financial Scores")
st.write(family_scores)
