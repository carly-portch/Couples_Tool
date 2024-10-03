import streamlit as st
from datetime import date

# Initialize session state for responses
if 'responses_1' not in st.session_state:
    st.session_state.responses_1 = {'accounts': [], 'debts': [], 'goals': []}
if 'responses_2' not in st.session_state:
    st.session_state.responses_2 = {'accounts': [], 'debts': [], 'goals': []}
if 'joint_responses' not in st.session_state:
    st.session_state.joint_responses = {'joint_accounts': [], 'joint_debts': [], 'joint_goals': []}

# Main function
def main():
    st.title("Couples Financial Planning Tool")
    
    # Partner 1 Input
    st.header("Partner 1 Input")
    partner_1_account_name = st.text_input("Account Name for Partner 1")
    partner_1_account_balance = st.number_input("Account Balance ($)", min_value=0.0)
    
    if st.button("Add this Account for Partner 1"):
        if partner_1_account_name:
            st.session_state.responses_1['accounts'].append((partner_1_account_name, partner_1_account_balance))
            st.success(f"Added Account for Partner 1: {partner_1_account_name}")
        else:
            st.error("Please enter an account name.")
    
    # Partner 2 Input
    st.header("Partner 2 Input")
    partner_2_account_name = st.text_input("Account Name for Partner 2")
    partner_2_account_balance = st.number_input("Account Balance ($)", min_value=0.0, key='partner_2_account_balance')
    
    if st.button("Add this Account for Partner 2"):
        if partner_2_account_name:
            st.session_state.responses_2['accounts'].append((partner_2_account_name, partner_2_account_balance))
            st.success(f"Added Account for Partner 2: {partner_2_account_name}")
        else:
            st.error("Please enter an account name.")

    # Joint Account Input
    st.header("Add Joint Account:")
    joint_account_name = st.text_input("Joint Account Name")
    joint_account_balance = st.number_input("Joint Account Balance ($)", min_value=0.0, key='joint_account_balance')
    
    if st.button("Add this Joint Account"):
        if joint_account_name:
            st.session_state.joint_responses['joint_accounts'].append((joint_account_name, joint_account_balance))
            st.success(f"Added Joint Account: {joint_account_name}")
        else:
            st.error("Please enter a joint account name.")

    # Partner 1 Debt Input
    st.header("Partner 1 Debt Input")
    partner_1_debt_name = st.text_input("Debt Name for Partner 1")
    partner_1_debt_amount = st.number_input("Debt Amount ($)", min_value=0.0, key='partner_1_debt_amount')
    partner_1_monthly_payment = st.number_input("Monthly Payment ($)", min_value=0.0, key='partner_1_monthly_payment')
    
    if st.button("Add this Debt for Partner 1"):
        if partner_1_debt_name:
            st.session_state.responses_1['debts'].append((partner_1_debt_name, partner_1_debt_amount, partner_1_monthly_payment))
            st.success(f"Added Debt for Partner 1: {partner_1_debt_name}")
        else:
            st.error("Please enter a debt name.")

    # Partner 2 Debt Input
    st.header("Partner 2 Debt Input")
    partner_2_debt_name = st.text_input("Debt Name for Partner 2")
    partner_2_debt_amount = st.number_input("Debt Amount ($)", min_value=0.0, key='partner_2_debt_amount')
    partner_2_monthly_payment = st.number_input("Monthly Payment ($)", min_value=0.0, key='partner_2_monthly_payment')
    
    if st.button("Add this Debt for Partner 2"):
        if partner_2_debt_name:
            st.session_state.responses_2['debts'].append((partner_2_debt_name, partner_2_debt_amount, partner_2_monthly_payment))
            st.success(f"Added Debt for Partner 2: {partner_2_debt_name}")
        else:
            st.error("Please enter a debt name.")

    # Joint Debt Input
    st.header("Add Joint Debt:")
    joint_debt_name = st.text_input("Joint Debt Name")
    joint_debt_amount = st.number_input("Joint Debt Amount ($)", min_value=0.0, key='joint_debt_amount')
    joint_monthly_payment = st.number_input("Joint Monthly Payment ($)", min_value=0.0, key='joint_monthly_payment')
    
    if st.button("Add this Joint Debt"):
        if joint_debt_name:
            st.session_state.joint_responses['joint_debts'].append((joint_debt_name, joint_debt_amount, joint_monthly_payment))
            st.success(f"Added Joint Debt: {joint_debt_name}")
        else:
            st.error("Please enter a joint debt name.")

    # Partner 1 Goal Input
    st.header("Partner 1 Goal Input")
    partner_1_goal_name = st.text_input("Goal Name for Partner 1")
    partner_1_goal_cost = st.number_input("Goal Cost ($)", min_value=0.0, key='partner_1_goal_cost')
    partner_1_target_year = st.number_input("Target Year for Goal", min_value=date.today().year, value=date.today().year, key='partner_1_target_year')
    
    # Include an account selection for the partner 1 goal
    account_for_goal_1 = st.selectbox("Account for Partner 1 Goal", options=[a[0] for a in st.session_state.responses_1['accounts']], key='partner_1_goal_account')
    if st.button("Add this Goal for Partner 1"):
        if partner_1_goal_name:
            st.session_state.responses_1['goals'].append({"name": partner_1_goal_name, "cost": partner_1_goal_cost, "target_year": partner_1_target_year, "account": account_for_goal_1})
            st.success(f"Added Goal for Partner 1: {partner_1_goal_name}")
        else:
            st.error("Please enter a goal name.")

    # Partner 2 Goal Input
    st.header("Partner 2 Goal Input")
    partner_2_goal_name = st.text_input("Goal Name for Partner 2")
    partner_2_goal_cost = st.number_input("Goal Cost ($)", min_value=0.0, key='partner_2_goal_cost')
    partner_2_target_year = st.number_input("Target Year for Goal", min_value=date.today().year, value=date.today().year, key='partner_2_target_year')
    
    # Include an account selection for the partner 2 goal
    account_for_goal_2 = st.selectbox("Account for Partner 2 Goal", options=[a[0] for a in st.session_state.responses_2['accounts']], key='partner_2_goal_account')
    if st.button("Add this Goal for Partner 2"):
        if partner_2_goal_name:
            st.session_state.responses_2['goals'].append({"name": partner_2_goal_name, "cost": partner_2_goal_cost, "target_year": partner_2_target_year, "account": account_for_goal_2})
            st.success(f"Added Goal for Partner 2: {partner_2_goal_name}")
        else:
            st.error("Please enter a goal name.")

    # Joint Goal Input
    st.header("Add Joint Goal:")
    joint_goal_name = st.text_input("Joint Goal Name")
    joint_goal_cost = st.number_input("Joint Goal Cost ($)", min_value=0.0, key='joint_goal_cost')
    joint_target_year = st.number_input("Joint Target Year", min_value=date.today().year, value=date.today().year, key='joint_target_year')
    
    # Include an account selection for the joint goal
    goal_account = st.selectbox("Account for Joint Goal", options=[a[0] for a in st.session_state.joint_responses['joint_accounts']], key='joint_goal_account')
    if st.button("Add this Joint Goal"):
        if joint_goal_name:
            st.session_state.joint_responses['joint_goals'].append({"name": joint_goal_name, "cost": joint_goal_cost, "target_year": joint_target_year, "account": goal_account})
            st.success(f"Added Joint Goal: {joint_goal_name}")
        else:
            st.error("Please enter a joint goal name.")

    # Display added accounts, debts, and goals
    st.subheader("Current Accounts, Debts, and Goals")
    
    # Partner 1 Accounts
    st.write("**Partner 1 Accounts:**")
    for account in st.session_state.responses_1['accounts']:
        st.write(f"Account Name: {account[0]}, Balance: ${account[1]:.2f}")
    
    # Partner 2 Accounts
    st.write("**Partner 2 Accounts:**")
    for account in st.session_state.responses_2['accounts']:
        st.write(f"Account Name: {account[0]}, Balance: ${account[1]:.2f}")

    # Joint Accounts
    st.write("**Joint Accounts:**")
    for account in st.session_state.joint_responses['joint_accounts']:
        st.write(f"Account Name: {account[0]}, Balance: ${account[1]:.2f}")

    # Partner 1 Debts
    st.write("**Partner 1 Debts:**")
    for debt in st.session_state.responses_1['debts']:
        st.write(f"Debt Name: {debt[0]}, Amount: ${debt[1]:.2f}, Monthly Payment: ${debt[2]:.2f}")
    
    # Partner 2 Debts
    st.write("**Partner 2 Debts:**")
    for debt in st.session_state.responses_2['debts']:
        st.write(f"Debt Name: {debt[0]}, Amount: ${debt[1]:.2f}, Monthly Payment: ${debt[2]:.2f}")

    # Joint Debts
    st.write("**Joint Debts:**")
    for debt in st.session_state.joint_responses['joint_debts']:
        st.write(f"Debt Name: {debt[0]}, Amount: ${debt[1]:.2f}, Monthly Payment: ${debt[2]:.2f}")

    # Partner 1 Goals
    st.write("**Partner 1 Goals:**")
    for goal in st.session_state.responses_1['goals']:
        st.write(f"Goal Name: {goal['name']}, Cost: ${goal['cost']:.2f}, Target Year: {goal['target_year']}, Account: {goal['account']}")

    # Partner 2 Goals
    st.write("**Partner 2 Goals:**")
    for goal in st.session_state.responses_2['goals']:
        st.write(f"Goal Name: {goal['name']}, Cost: ${goal['cost']:.2f}, Target Year: {goal['target_year']}, Account: {goal['account']}")

    # Joint Goals
    st.write("**Joint Goals:**")
    for goal in st.session_state.joint_responses['joint_goals']:
        st.write(f"Goal Name: {goal['name']}, Cost: ${goal['cost']:.2f}, Target Year: {goal['target_year']}, Account: {goal['account']}")

    # Dashboard Button
    if st.button("Show Dashboard"):
        selected_year = st.number_input("Select Year for Dashboard", min_value=date.today().year, value=date.today().year)
        show_dashboard(st.session_state.responses_1, st.session_state.responses_2, st.session_state.joint_responses, selected_year)

# Function to display dashboard
def show_dashboard(responses_1, responses_2, joint_responses, selected_year):
    st.title("Financial Dashboard")
    
    display_individual_dashboard(responses_1, "Partner 1's Financial Overview")
    display_individual_dashboard(responses_2, "Partner 2's Financial Overview")
    display_joint_dashboard(joint_responses, "Joint Financial Overview", selected_year)

def display_individual_dashboard(responses, title):
    st.subheader(title)
    
    st.write("**Accounts:**")
    for account in responses['accounts']:
        st.write(f"Account Name: {account[0]}, Balance: ${account[1]:.2f}")
    
    st.write("**Debts:**")
    for debt in responses['debts']:
        st.write(f"Debt Name: {debt[0]}, Amount: ${debt[1]:.2f}, Monthly Payment: ${debt[2]:.2f}")

    st.write("**Goals:**")
    display_goal_progress(responses['goals'], selected_year, {account[0]: account[1] for account in responses['accounts']})

def display_joint_dashboard(joint_responses, title, selected_year):
    st.subheader(title)
    
    st.write("**Joint Accounts:**")
    for account in joint_responses['joint_accounts']:
        st.write(f"Account Name: {account[0]}, Balance: ${account[1]:.2f}")

    st.write("**Joint Debts:**")
    for debt in joint_responses['joint_debts']:
        st.write(f"Debt Name: {debt[0]}, Amount: ${debt[1]:.2f}, Monthly Payment: ${debt[2]:.2f}")

    st.write("**Joint Goals:**")
    display_goal_progress(joint_responses['joint_goals'], selected_year, {account[0]: account[1] for account in joint_responses['joint_accounts']})

def display_goal_progress(goals, selected_year, accounts):
    for goal in goals:
        goal_cost = goal["cost"]
        target_year = goal["target_year"]
        account_name = goal["account"] if "account" in goal else None  # Safely get the account name

        # If account_name is specified, look it up; otherwise, set a default
        account_balance = accounts.get(account_name, 0)

        # Calculate the progress towards the goal
        if goal_cost > 0:
            progress = min(account_balance / goal_cost, 1)
        else:
            progress = 0  # Avoid division by zero

        st.write(f"Goal: {goal['name']}")
        st.write(f"Goal Cost: ${goal_cost:.2f}, Target Year: {target_year}, Account: {account_name}")
        st.write(f"Progress: {progress:.2%} towards this goal.")

if __name__ == "__main__":
    main()
