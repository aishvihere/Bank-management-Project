import streamlit as st
from improved import Bank

# ---------- INITIAL SETUP ----------
bank = Bank()

st.set_page_config(page_title="Bank Management System", layout="centered")
st.title("🏦 Bank Management System")

# ---------- HELPER FUNCTION ----------
def authenticate_user():
    acc_no = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    return acc_no, pin


# ---------- SIDEBAR ----------
st.sidebar.title("📌 Menu")
menu = st.sidebar.radio(
    "Select an option",
    (
        "Create Account",
        "View Account Details",
        "Deposit Money",
        "Withdraw Money",
        "Update Account",
        "Delete Account"
    )
)

# ---------- CREATE ACCOUNT ----------
if menu == "Create Account":
    st.subheader("Create New Account")

    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    email = st.text_input("Email")
    pin = st.text_input("4 Digit PIN", type="password")

    if st.button("Create Account"):
        if not pin.isdigit():
            st.error("PIN must be numeric")
        else:
            success, result = bank.create_account(
                name, age, email, int(pin)
            )
            if success:
                st.success("Account created successfully 🎉")
                st.info(f"Your Account Number: {result['account_no']}")
            else:
                st.error(result)

# ---------- VIEW DETAILS ----------
elif menu == "View Account Details":
    st.subheader("Account Details")

    acc_no, pin = authenticate_user()

    if st.button("View Details"):
        if not pin.isdigit():
            st.error("Invalid PIN")
        else:
            user = bank.authenticate(acc_no, int(pin))
            if not user:
                st.error("Invalid credentials")
            else:
                st.json({
                    "Name": user["name"],
                    "Age": user["age"],
                    "Email": user["email"],
                    "Account Number": user["account_no"],
                    "Balance": user["balance"]
                })

# ---------- DEPOSIT ----------
elif menu == "Deposit Money":
    st.subheader("Deposit Money")

    acc_no, pin = authenticate_user()
    amount = st.number_input("Amount", min_value=1)

    if st.button("Deposit"):
        if not pin.isdigit():
            st.error("Invalid PIN")
        else:
            user = bank.authenticate(acc_no, int(pin))
            if not user:
                st.error("Account not found")
            else:
                success, msg = bank.deposit(user, amount)
                st.success(msg) if success else st.error(msg)

# ---------- WITHDRAW ----------
elif menu == "Withdraw Money":
    st.subheader("Withdraw Money")

    acc_no, pin = authenticate_user()
    amount = st.number_input("Amount", min_value=1)

    if st.button("Withdraw"):
        if not pin.isdigit():
            st.error("Invalid PIN")
        else:
            user = bank.authenticate(acc_no, int(pin))
            if not user:
                st.error("Account not found")
            else:
                success, msg = bank.withdraw(user, amount)
                st.success(msg) if success else st.error(msg)

# ---------- UPDATE ACCOUNT ----------
elif menu == "Update Account":
    st.subheader("Update Account Details")

    acc_no, pin = authenticate_user()
    new_name = st.text_input("New Name (optional)")
    new_email = st.text_input("New Email (optional)")
    new_pin = st.text_input("New PIN (optional)", type="password")

    if st.button("Update Details"):
        if not pin.isdigit():
            st.error("Invalid PIN")
        else:
            user = bank.authenticate(acc_no, int(pin))
            if not user:
                st.error("Invalid credentials")
            else:
                success, msg = bank.update_details(
                    user,
                    name=new_name or None,
                    email=new_email or None,
                    pin=int(new_pin) if new_pin.isdigit() else None
                )
                st.success("Account updated successfully ✏️") if success else st.error(msg)

# ---------- DELETE ACCOUNT ----------
elif menu == "Delete Account":
    st.subheader("Delete Account")

    acc_no, pin = authenticate_user()
    st.warning("⚠️ This action is irreversible!")

    if st.button("Delete Account"):
        if not pin.isdigit():
            st.error("Invalid PIN")
        else:
            user = bank.authenticate(acc_no, int(pin))
            if not user:
                st.error("Invalid credentials")
            else:
                bank.delete_account(user)
                st.warning("Account deleted successfully ❌")
