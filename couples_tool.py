import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

# Set the page config to wide mode
st.set_page_config(page_title="Get Aligned as a Couple", layout="wide")

# Function to calculate future account value considering principal and monthly contributions
def calculate_future_value(principal, annual_rate, years, monthly_contribution):
    if annual_rate == 0:
        future_value = principal + (monthly_contribution * years * 12)
    else:
        monthly_rate = annual_rate / 100 / 12
        months = years * 12
        future_value = principal * (1 + monthly_rate) ** months
        future_value += monthly_contribution * (((1 + monthly_rate) ** months - 1) / monthly_rate)
    return future_value

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

        st.subheader("Debts:")
        if responses['debts']:
            debts_df = pd.DataFrame(responses['debts'], columns=['Debt Name', 'Amount ($)', 'Interest Rate (%)', 'Monthly Payment ($)'])
            st.write(debts_df)
        else:
            st.write("No debts added yet.")

        st.subheader("Goals:")
        if responses['goals']:
            goals_df = pd.DataFrame(responses['goals'], columns=['Goal Name', 'Cost ($)', 'Target Year', 'Account'])
            st.write(goals_df)
            display_goal_progress(responses['goals'], selected_year, {account[0]: account[3] for account in responses['accounts']})
        else:
            st.write("No goals added yet.")

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

    st.subheader("Joint Goals:")
    if joint_responses['joint_goals']:
        joint_goals_df = pd.DataFrame(joint_responses['joint_goals'], columns=['Goal Name', 'Cost ($)', 'Target Year'])
        st.write(joint_goals_df)
        display_goal_progress(joint_responses['joint_goals'], selected_year, {account[0]: account[3] for account in joint_responses['joint_accounts']})
    else:
        st.write("No joint goals added yet.")

# Main function to run the app
def main():
    if 'dashboard_run' not in st.session_state:
        st.session_state.dashboard_run = False

    # Partner 1 responses
    if 'responses_1' not in st.session_state:
        st.session_state.responses_1 = {
            'accounts': [],
            'total_expenses': 0,
            'remaining_funds': 0,
            'total_debt_payments': 0,
            'goals': [],
            'debts': []
        }

    # Partner 2 responses
    if 'responses_2' not in st.session_state:
        st.session_state.responses_2 = {
            'accounts': [],
            'total_expenses': 0,
            'remaining_funds': 0,
            'total_debt_payments': 0,
            'goals': [],
            'debts': []
        }

    # Joint responses
    if 'joint_responses' not in st.session_state:
        st.session_state.joint_responses = {
            'joint_income': 0,
            'joint_expenses': 0,
            'joint_remaining_funds': 0,
            'joint_debt_payments': 0,
            'joint_accounts': [],
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
        st.subheader("Expenses")
        responses_1['total_expenses'] = st.number_input("Partner 1: What are your total monthly expenses?", min_value=0.0)

        st.subheader("Account:")
        account_name = st.text_input("Account Name", key='account_1')
        account_type = st.selectbox("Account Type", options=["Checking", "Savings", "Investment"], key='account_type_1')
        interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, key='interest_rate_1')
        balance = st.number_input("Account Balance ($)", min_value=0.0, key='balance_1')
        if account_name:
            responses_1['accounts'].append([account_name, account_type, interest_rate, balance])

        st.subheader("Debt:")
        debt_name = st.text_input("Debt Name", key='debt_1')
        debt_amount = st.number_input("Amount ($)", min_value=0.0, key='debt_amount_1')
        debt_interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, key='debt_interest_rate_1')
        monthly_payment = st.number_input("Monthly Payment ($)", min_value=0.0, key='monthly_payment_1')
        if debt_name:
            responses_1['debts'].append([debt_name, debt_amount, debt_interest_rate, monthly_payment])

        st.subheader("Goal:")
        goal_name = st.text_input("Goal Name", key='goal_1')
        goal_cost = st.number_input("Goal Cost ($)", min_value=0.0, key='goal_cost_1')
        target_year = st.number_input("Target Year", min_value=date.today().year, value=date.today().year, key='target_year_1')
        goal_account = st.selectbox("Account for Goal", options=[a[0] for a in responses_1['accounts']], key='goal_account_1')
        if goal_name:
            responses_1['goals'].append({"name": goal_name, "cost": goal_cost, "target_year": target_year, "account": goal_account})

        if st.button("Add Another Account for Partner 1"):
            responses_1['accounts'].append([])  # Add an empty list for another account
        if st.button("Add Another Debt for Partner 1"):
            responses_1['debts'].append([])  # Add an empty list for another debt
        if st.button("Add Another Goal for Partner 1"):
            responses_1['goals'].append({"name": "", "cost": 0, "target_year": date.today().year, "account": ""})  # Add an empty dict for another goal

    with col2:
        st.header("Partner 2 Information")
        st.subheader("Personal Income")
        responses_2['paycheck'] = st.number_input("Partner 2: What is your monthly take-home pay after tax?", min_value=0.0)
        st.subheader("Expenses")
        responses_2['total_expenses'] = st.number_input("Partner 2: What are your total monthly expenses?", min_value=0.0)

        st.subheader("Account:")
        account_name = st.text_input("Account Name", key='account_2')
        account_type = st.selectbox("Account Type", options=["Checking", "Savings", "Investment"], key='account_type_2')
        interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, key='interest_rate_2')
        balance = st.number_input("Account Balance ($)", min_value=0.0, key='balance_2')
        if account_name:
            responses_2['accounts'].append([account_name, account_type, interest_rate, balance])

        st.subheader("Debt:")
        debt_name = st.text_input("Debt Name", key='debt_2')
        debt_amount = st.number_input("Amount ($)", min_value=0.0, key='debt_amount_2')
        debt_interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, key='debt_interest_rate_2')
        monthly_payment = st.number_input("Monthly Payment ($)", min_value=0.0, key='monthly_payment_2')
        if debt_name:
            responses_2['debts'].append([debt_name, debt_amount, debt_interest_rate, monthly_payment])

        st.subheader("Goal:")
        goal_name = st.text_input("Goal Name", key='goal_2')
        goal_cost = st.number_input("Goal Cost ($)", min_value=0.0, key='goal_cost_2')
        target_year = st.number_input("Target Year", min_value=date.today().year, value=date.today().year, key='target_year_2')
        goal_account = st.selectbox("Account for Goal", options=[a[0] for a in responses_2['accounts']], key='goal_account_2')
        if goal_name:
            responses_2['goals'].append({"name": goal_name, "cost": goal_cost, "target_year": target_year, "account": goal_account})

        if st.button("Add Another Account for Partner 2"):
            responses_2['accounts'].append([])  # Add an empty list for another account
        if st.button("Add Another Debt for Partner 2"):
            responses_2['debts'].append([])  # Add an empty list for another debt
        if st.button("Add Another Goal for Partner 2"):
            responses_2['goals'].append({"name": "", "cost": 0, "target_year": date.today().year, "account": ""})  # Add an empty dict for another goal

    with col_joint:
        st.header("Joint Information")
        st.subheader("Joint Income")
        joint_responses['joint_income'] = st.number_input("What is your joint monthly income?", min_value=0.0)
        st.subheader("Joint Expenses")
        joint_responses['joint_expenses'] = st.number_input("What are your joint monthly expenses?", min_value=0.0)
        joint_responses['joint_debt_payments'] = st.number_input("Joint Monthly Debt Payments (shared debts)", min_value=0.0)

        st.subheader("Joint Account:")
        account_name = st.text_input("Joint Account Name", key='joint_account')
        account_type = st.selectbox("Joint Account Type", options=["Checking", "Savings", "Investment"], key='joint_account_type')
        interest_rate = st.number_input("Joint Interest Rate (%)", min_value=0.0, key='joint_interest_rate')
        balance = st.number_input("Joint Account Balance ($)", min_value=0.0, key='joint_balance')
        if account_name:
            joint_responses['joint_accounts'].append([account_name, account_type, interest_rate, balance])

        st.subheader("Joint Goal:")
        goal_name = st.text_input("Joint Goal Name", key='joint_goal')
        goal_cost = st.number_input("Joint Goal Cost ($)", min_value=0.0, key='joint_goal_cost')
        target_year = st.number_input("Joint Target Year", min_value=date.today().year, value=date.today().year, key='joint_target_year')
        if goal_name:
            joint_responses['joint_goals'].append({"name": goal_name, "cost": goal_cost, "target_year": target_year})  # Add another joint goal

        if st.button("Add Another Joint Account"):
            joint_responses['joint_accounts'].append([])  # Add an empty list for another joint account
        if st.button("Add Another Joint Goal"):
            joint_responses['joint_goals'].append({"name": "", "cost": 0, "target_year": date.today().year})  # Add another empty dict for a joint goal

    if st.button("Show Couples Dashboard"):
        show_dashboard(responses_1, responses_2, joint_responses, selected_year)

if __name__ == '__main__':
    main()
