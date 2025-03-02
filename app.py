import streamlit as st
import pandas as pd
from engine import UserDatabase

# ตัวเลือก dropdown
BANKS = ["SCB", "KBank", "BBL", "TMB", "Krungsri"]
CARD_TYPES = ["Platinum", "Gold", "Titanium", "Black Card"]
LIFESTYLES = ["Travel", "Shopping", "Dining", "Entertainment"]

db = UserDatabase("users.csv")  # ต้องกำหนด path ให้ตรง

def register_page():
    st.title("🔐 Register")

    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")
    bank = st.selectbox("🏦 Bank", BANKS)
    card_type = st.selectbox("💳 Card Type", CARD_TYPES)
    lifestyle = st.selectbox("🎯 Lifestyle", LIFESTYLES)

    if st.button("✅ Register"):
        success, msg = db.register_user(username, password, bank, card_type, lifestyle)
        if success:
            st.success(msg)
            st.experimental_rerun()  # รีเฟรชหน้าให้กลับไป login
        else:
            st.error(msg)

def login_page():
    st.title("🔓 Login")

    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    if st.button("🚀 Login"):
        if db.authenticate_user(username, password):
            st.success("✅ Login successful!")
            st.session_state["logged_in"] = True
        else:
            st.error("❌ Invalid username or password.")

def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    page = st.sidebar.radio("📌 Select Page", ["Login", "Register"])

    if page == "Register":
        register_page()
    else:
        login_page()

if __name__ == "__main__":
    main()
