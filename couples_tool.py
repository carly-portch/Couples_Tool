import streamlit as st

# Define the list of questions and decision paths
questions = {
    "start": {
        "question": "What is your financial goal?",
        "options": ["Retirement", "Buying a home", "Travel", "Other"]
    },
    "retirement": {
        "question": "At what age do you plan to retire?",
        "options": ["60", "65", "70", "Other"]
    },
    "home": {
        "question": "When do you plan to buy a home?",
        "options": ["Within 1 year", "1-3 years", "3-5 years", "More than 5 years"]
    },
    "travel": {
        "question": "How often do you plan to travel?",
        "options": ["Once a year", "Twice a year", "Every few months", "Other"]
    },
    "other": {
        "question": "Please briefly describe your goal.",
        "options": None  # Open text input
    }
}

# Function to display the dashboard based on responses
def show_dashboard(responses):
    st.title("Your Customized Dashboard")

    st.subheader("Based on your inputs, here are some recommendations:")
    
    # Example: Responding based on the input
    if responses['goal'] == "Retirement":
        st.write(f"Since you plan to retire at age {responses['retirement']}, we recommend reviewing your investment strategy.")
    elif responses['goal'] == "Buying a home":
        st.write(f"Planning to buy a home in {responses['home']} gives you time to save and consider mortgage options.")
    elif responses['goal'] == "Travel":
        st.write(f"With {responses['travel']} travel plans, a budget allocation might help you stay financially balanced.")
    else:
        st.write(f"For your goal '{responses['other']}', here are some tailored suggestions...")
    
    # Visualization example (replace with real data visualizations)
    st.line_chart([1, 2, 3, 4, 5])

# Streamlit app logic
def main():
    st.title("Financial Planning Tool")

    # Store user responses in a dictionary
    responses = {}

    # Ask the first question
    goal = st.radio(
        questions["start"]["question"],
        questions["start"]["options"]
    )

    responses['goal'] = goal

    # Ask follow-up questions based on the first answer
    if goal == "Retirement":
        retirement_age = st.radio(
            questions["retirement"]["question"],
            questions["retirement"]["options"]
        )
        responses['retirement'] = retirement_age
    elif goal == "Buying a home":
        home_plan = st.radio(
            questions["home"]["question"],
            questions["home"]["options"]
        )
        responses['home'] = home_plan
    elif goal == "Travel":
        travel_freq = st.radio(
            questions["travel"]["question"],
            questions["travel"]["options"]
        )
        responses['travel'] = travel_freq
    else:
        other_goal = st.text_input(questions["other"]["question"])
        responses['other'] = other_goal

    # Button to submit and generate the dashboard
    if st.button("Submit"):
        show_dashboard(responses)

if __name__ == '__main__':
    main()
