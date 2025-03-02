import streamlit as st
import pandas as pd
from engine import UserDatabase

# ตรวจสอบและกำหนดค่าเริ่มต้นของ session_state
def initialize_session_state():
    default_values = {
        "page": "Login",
        "logged_in": False,
        "registered": False,
        "username": "",
    }
    for key, value in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_session_state()  # เรียกใช้เพื่อกำหนดค่าเริ่มต้น

db = UserDatabase("users.csv")  # ใช้ database class

def register_page():
    st.title("🔐 Register")

    username = st.text_input("👤 Username", key="register_username")
    password = st.text_input("🔑 Password", type="password", key="register_password")
    bank = st.selectbox("🏦 Bank", ["SCB", "KBank", "BBL", "TMB", "Krungsri"], key="register_bank")
    card_type = st.selectbox("💳 Card Type", ["Platinum", "Gold", "Titanium", "Black Card"], key="register_card")
    lifestyle = st.selectbox("🎯 Lifestyle", ["Travel", "Shopping", "Dining", "Entertainment"], key="register_lifestyle")

    if st.button("✅ Register"):
        success, msg = db.register_user(username, password, bank, card_type, lifestyle)
        if success:
            st.success(msg)
            st.session_state["registered"] = True
            st.session_state["page"] = "Login"  # เปลี่ยนไปหน้า Login
            st.rerun()  # รีเฟรชหน้า
        else:
            st.error(msg)

def login_page():
    st.title("🔓 Login")

    username = st.text_input("👤 Username", key="login_username")
    password = st.text_input("🔑 Password", type="password", key="login_password")

    if st.button("🚀 Login"):
        if db.authenticate_user(username, password):
            st.success("✅ Login successful!")
            st.session_state["logged_in"] = True
            st.session_state["username"] = username  # บันทึก user ที่ล็อกอิน
            st.rerun()  # รีเฟรชเพื่อให้เข้าสู่ระบบ
        else:
            st.error("❌ Invalid username or password.")

def main():
    # ใช้ session_state["page"] เป็นตัวควบคุมหน้า
    if st.session_state["page"] == "Register":
        register_page()
    else:
        login_page()

    # Sidebar สำหรับเปลี่ยนหน้า
    page_selection = st.sidebar.radio("📌 Select Page", ["Login", "Register"])
    st.session_state["page"] = page_selection  # อัปเดต session_state

if __name__ == "__main__":
    main()
