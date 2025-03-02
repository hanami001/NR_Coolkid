import streamlit as st
import pandas as pd
from engine import UserDatabase

# ตัวเลือก dropdown
BANKS = ["SCB", "KBank", "BBL", "TMB", "Krungsri"]
CARD_TYPES = ["Platinum", "Gold", "Titanium", "Black Card"]
LIFESTYLES = ["Travel", "Shopping", "Dining", "Entertainment"]

db = UserDatabase()

def register_page():
    st.title("Register")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    bank = st.selectbox("Bank", BANKS)
    card_type = st.selectbox("Card Type", CARD_TYPES)
    lifestyle = st.selectbox("Lifestyle", LIFESTYLES)
    
    if st.button("Register"):
        success, msg = db.register_user(username, password, bank, card_type, lifestyle)
        if success:
            st.success(msg)
            st.switch_page("app.py")  # กลับไปหน้า Login
        else:
            st.error(msg)

def login_page():
    st.title("Login")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if db.authenticate_user(username, password):
            st.success("Login successful!")
        else:
            st.error("Invalid username or password.")

def main():
    page = st.sidebar.selectbox("Choose Page", ["Login", "Register"])
    if page == "Register":
        register_page()
    else:
        login_page()

if __name__ == "__main__":
    main()
