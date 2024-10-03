if 'responses' not in st.session_state:
    st.session_state.responses = {
        'yours': {  # Partner 1
            'accounts': [],
            'allocations': {},
            'expenses': {},
            'total_expenses': 0,
            'remaining_funds': 0,
            'total_debt_payments': 0,
            'goals': [],
            'assets': [],
            'debts': []
        },
        'mine': {  # Partner 2
            'accounts': [],
            'allocations': {},
            'expenses': {},
            'total_expenses': 0,
            'remaining_funds': 0,
            'total_debt_payments': 0,
            'goals': [],
            'assets': [],
            'debts': []
        },
        'ours': {  # Joint finances
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
    }
