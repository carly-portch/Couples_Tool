import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import date, datetime

# Set the page config to wide mode
st.set_page_config(page_title="Get Aligned as a Couple", layout="wide")

# Function to calculate age from birthday
def calculate_age(birthday):
    today = date.today()
    birthdate = pd.to_datetime(birthday)
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

# Function to calculate future account value considering principal and monthly contributions
def calculate_future_value(principal, annual_rate, years, monthly_contribution):
    if annual_rate == 0:
        future_value = principal + (monthly_contribution * years * 12)
    else:
        monthly_rate = annual_rate / 100 / 12
        months = years * 12
        try:
            future_value = principal * (1 + monthly_rate) ** months
            future_value += monthly_contribution * (((1 + monthly_rate) ** months - 1) / monthly_rate)
        except ZeroDivisionError:
            future_value = principal + (monthly_contribution * months)
    return future_value

# Function to calculate debt payback date based on fixed monthly payments
def calculate_payback_date(amount, interest_rate, monthly_payment):
    if monthly_payment <= 0:
        raise ValueError("Monthly payment must be greater than zero.")
    
    if interest_rate == 0:
        months = amount / monthly_payment
    else:
        monthly_rate = interest_rate / 100 / 12
        months = np.log(monthly_payment / (monthly_payment - amount * monthly_rate)) / np.log(1 + monthly_rate)

    payback_date = date.today() + pd.DateOffset(months=int(months))
    return payback_date.date()

# Function to display progress toward goals
def display_goal_progress(goals, selected_year, account_balances):
    st.subheader(f"Goal Progress in {selected_year}:")
    if not goals:
        st.write("No goals have been added.")
        return

    for goal in goals:
        goal_name = goal["name"]
        goal_cost = goal["cost"]
        goal_year = goal["target_year"]
        account_name = goal["account"]

        if account_name not in account_balances:
            st.write(f"Account {account_name} not found.")
            continue

        account_balance = account_balances[account_name]
        progress = min(account_balance / goal_cost, 1)
        progress_percentage = progress * 100

        st.write(f"**Goal: {goal_name}**")
        st.write(f"Cost: ${goal_cost:,.0f}, Target Year: {goal_year}")
        st.progress(progress)
        st.write(f"{progress_percentage:.0f}% of goal achieved.\n")

# Function to display the dashboard for both partners
def show_dashboard(responses_1, responses_2, joint_responses, selected_year):
    st.title("Couple's Financial Dashboard")

    def display_individual_dashboard(responses, title):
        st.subheader(title)
        st.write(f"**Monthly Take-Home Pay**: ${responses.get('paycheck', 0):,.0f}")
        st.write(f"**Monthly Expenses**: ${responses.get('total_expenses', 0):,.0f}")
        st.write(f"**Monthly Debt Payments**: ${responses.get('total_debt_payments', 0):,.0f}")

        remaining_funds = responses['paycheck'] - responses['total_expenses'] - responses['total_debt_payments']
        responses['remaining_funds'] = remaining_funds if remaining_funds > 0 else 0
        st.write(f"**Remaining Monthly Funds**: ${responses['remaining_funds']:,.0f}")

        st.subheader("Accounts Today:")
        if responses['accounts']:
            accounts_df = pd.DataFrame(responses['accounts'], columns=['Account Name', 'Type', 'Interest Rate (%)', 'Balance ($)'])
            st.write(accounts_df)
        else:
            st.write("No accounts added yet.")

    display_individual_dashboard(responses_1, "Partner 1's Financial Overview")
    display_individual_dashboard(responses_2, "Partner 2's Financial Overview")
    
    st.subheader("Joint Financial Overview")
    st.write(f"**Joint Monthly Income**: ${joint_responses.get('joint_income', 0):,.0f}")
    st.write(f"**Joint Monthly Expenses**: ${joint_responses.get('joint_expenses', 0):,.0f}")
    st.write(f"**Joint Monthly Debt Payments**: ${joint_responses.get('joint_debt_payments', 0):,.0f}")
    
    joint_remaining_funds = joint_responses['joint_income'] - joint_responses['joint_expenses'] - joint_responses['joint_debt_payments']
    joint_responses['joint_remaining_funds'] = joint_remaining_funds if joint_remaining_funds > 0 else 0
    st.write(f"**Joint Remaining Monthly Funds**: ${joint_responses['joint_remaining_funds']:,.0f}")

    st.subheader("Joint Accounts Today:")
    if joint_responses['joint_accounts']:
        joint_accounts_df = pd.DataFrame(joint_responses['joint_accounts'], columns=['Account Name', 'Type', 'Interest Rate (%)', 'Balance ($)'])
        st.write(joint_accounts_df)
    else:
        st.write("No joint accounts added yet.")
    
    # Joint goals, assets, and debts can also be added here similarly

    # Projections and assets visualization will follow the same pattern

# Main function to run the app
def main():
    if 'dashboard_run' not in st.session_state:
        st.session_state.dashboard_run = False

    # Partner 1 responses
    if 'responses_1' not in st.session_state:
        st.session_state.responses_1 = {
            'accounts': [],
            'allocations': {},
            'expenses': {},
            'total_expenses': 0,
            'remaining_funds': 0,
            'total_debt_payments': 0,
            'goals': [],
            'assets': [],
            'debts': []
        }

    # Partner 2 responses
    if 'responses_2' not in st.session_state:
        st.session_state.responses_2 = {
            'accounts': [],
            'allocations': {},
            'expenses': {},
            'total_expenses': 0,
            'remaining_funds': 0,
            'total_debt_payments': 0,
            'goals': [],
            'assets': [],
            'debts': []
        }

    # Joint responses
    if 'joint_responses' not in st.session_state:
        st.session_state.joint_responses = {
            'joint_income': 0,
            'joint_expenses': 0,
            'joint_remaining_funds': 0,
            'joint_total_debt_payments': 0,
            'joint_accounts': [],
            'joint_assets': [],
            'joint_debts': [],
            'joint_goals': []
        }

    responses_1 = st.session_state.responses_1
    responses_2 = st.session_state.responses_2
    joint_responses = st.session_state.joint_responses

    selected_year = st.number_input("Select the year to project your financial situation:", min_value=date.today().year, value=2055)

    col1, col2, col_joint = st.columns([1, 1, 1])

    with col1:
        st.header("Partner 1 Information")
        st.subheader("Personal Income")
        responses_1['paycheck'] = st.number_input("Partner 1: What is your monthly take-home pay after tax?", min_value=0.0)
        st.subheader("Expenses and Debts")
        responses_1['total_expenses'] = st.number_input("Partner 1: What are your total monthly expenses?", min_value=0.0)
        responses_1['total_debt_payments'] = st.number_input("Partner 1: Total Monthly Debt Payments", min_value=0.0)

    with col2:
        st.header("Partner 2 Information")
        st.subheader("Personal Income")
        responses_2['paycheck'] = st.number_input("Partner 2: What is your monthly take-home pay after tax?", min_value=0.0)
        st.subheader("Expenses and Debts")
        responses_2['total_expenses'] = st.number_input("Partner 2: What are your total monthly expenses?", min_value=0.0)
        responses_2['total_debt_payments'] = st.number_input("Partner 2: Total Monthly Debt Payments", min_value=0.0)

    with col_joint:
        st.header("Joint Information")
        joint_responses['joint_income'] = st.number_input("Joint Monthly Income (shared income)", min_value=0.0)
        joint_responses['joint_expenses'] = st.number_input("Joint Monthly Expenses (shared expenses)", min_value=0.0)
        joint_responses['joint_debt_payments'] = st.number_input("Joint Monthly Debt Payments (shared debts)", min_value=0.0)

    if st.button("Show Couples Dashboard"):
        show_dashboard(responses_1, responses_2, joint_responses, selected_year)

if __name__ == '__main__':
    main()
