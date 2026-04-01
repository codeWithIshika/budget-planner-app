import streamlit as st

# Page config
st.set_page_config(page_title="Budget Planner", layout="centered")

st.title("💰 Budget Planner")
st.markdown("Track your income and expenses easily 😎")
st.divider()

# ---------------- SESSION STATE ----------------
if "balance" not in st.session_state:
    st.session_state.balance = 0

if "transactions" not in st.session_state:
    st.session_state.transactions = []

# ---------------- SIDEBAR ----------------
st.sidebar.title("📌 Menu")
option = st.sidebar.radio(
    "Select Option",
    ["Add Income", "Add Expense", "View Summary"]
)

# ---------------- ADD INCOME ----------------
if option == "Add Income":
    st.subheader("💰 Add Income")

    income = st.number_input("Enter income amount", min_value=0.0)

    if st.button("Add Income"):
        st.session_state.balance += income
        st.session_state.transactions.append(f"Income: +{income}")
        st.success("Income added!")

# ---------------- ADD EXPENSE ----------------
elif option == "Add Expense":
    st.subheader("🧾 Add Expense")

    expense = st.number_input("Enter expense amount", min_value=0.0)

    category = st.selectbox(
        "Select Category",
        ["Food", "Shopping", "Travel", "Bills", "Other"]
    )

    payment = st.radio(
        "Payment Method",
        ["UPI", "Cash"]
    )

    if st.button("Add Expense"):
        st.session_state.balance -= expense
        st.session_state.transactions.append(
            f"Expense: -{expense} | {category} | {payment}"
        )
        st.warning("Expense added!")

# ---------------- SUMMARY ----------------
elif option == "View Summary":
    st.subheader("📊 Dashboard Overview")

    # Metrics
    col1, col2 = st.columns(2)

    with col1:
        st.metric("💰 Balance", st.session_state.balance)

    with col2:
        st.metric("📋 Transactions", len(st.session_state.transactions))

    st.divider()

    # Calculate totals
    total_income = 0
    total_expense = 0

    for t in st.session_state.transactions:
        if "Income" in t:
            amount = t.split("+")[1].split("|")[0]
            total_income += float(amount)
        elif "Expense" in t:
            amount = t.split("-")[1].split("|")[0]
            total_expense += float(amount)

    # Graph
    st.subheader("📊 Income vs Expense")
    data = {
        "Income": total_income,
        "Expense": total_expense
    }
    st.bar_chart(data)

    st.divider()

    # Transactions
    st.subheader("🧾 Transactions")

    if len(st.session_state.transactions) == 0:
        st.info("No transactions yet!")
    else:
        for t in st.session_state.transactions:
            if "Income" in t:
                st.success(t)
            else:
                st.error(t)

    # ---------------- DELETE FEATURE ----------------
    if st.button("🗑️ Delete Last Transaction"):
        if len(st.session_state.transactions) > 0:
            last = st.session_state.transactions.pop()

            if "Income" in last:
                amount = float(last.split("+")[1].split("|")[0])
                st.session_state.balance -= amount
            elif "Expense" in last:
                amount = float(last.split("-")[1].split("|")[0])
                st.session_state.balance += amount

            st.warning("Last transaction deleted!")
        else:
            st.info("No transactions to delete!")
