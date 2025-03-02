import streamlit as st
import pandas as pd
from engine import UserDatabase

# ตัวเลือก dropdown
BANKS = ["SCB", "KBank", "BBL", "TMB", "Krungsri"]
CARD_TYPES = ["Platinum", "Gold", "Titanium", "Black Card"]
LIFESTYLES = ["Travel", "Shopping", "Dining", "Entertainment"]

db = UserDatabase("users.csv")  # กำหนด path ของ CSV

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
            st.session_state["registered"] = True  # ตั้งค่าตัวแปร session เพื่อแจ้งว่าลงทะเบียนแล้ว
        else:
            st.error(msg)

    # ถ้าลงทะเบียนเสร็จแล้ว ให้แสดงปุ่มกลับไปหน้า Login
    if st.session_state.get("registered", False):
        if st.button("🔙 Go to Login"):
            st.session_state["registered"] = False  # รีเซ็ตค่า
            st.experimental_set_query_params(page="Login")  # สลับหน้า

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

    # ดึงค่าหน้าปัจจุบันจาก query parameter
    query_params = st.experimental_get_query_params()
    current_page = query_params.get("page", ["Login"])[0]  # ค่า default คือ Login

    # สร้าง sidebar ให้เลือกหน้า
    page = st.sidebar.radio("📌 Select Page", ["Login", "Register"], index=0 if current_page == "Login" else 1)

    if page == "Register":
        register_page()
    else:
        login_page()

if __name__ == "__main__":
    main()
