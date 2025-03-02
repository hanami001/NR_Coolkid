import streamlit as st
import pandas as pd
from engine import UserDatabase

# ตัวเลือก dropdown
BANKS = ["SCB", "KBank", "BBL", "TMB", "Krungsri"]
CARD_TYPES = ["Platinum", "Gold", "Titanium", "Black Card"]
LIFESTYLES = ["Travel", "Shopping", "Dining", "Entertainment"]

# ตรวจสอบและกำหนดค่าเริ่มต้นของ session_state
if "page" not in st.session_state:
    st.session_state["page"] = "Login"

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "registered" not in st.session_state:
    st.session_state["registered"] = False

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
            st.session_state["registered"] = True  # ตั้งค่าว่าลงทะเบียนแล้ว
            st.session_state["page"] = "Login"  # เปลี่ยนไปหน้า Login
            st.rerun()  # รีเฟรชหน้า

    # ถ้าลงทะเบียนเสร็จแล้ว ให้แสดงปุ่มกลับไปหน้า Login
    if st.session_state["registered"]:
        if st.button("🔙 Go to Login"):
            st.session_state["page"] = "Login"
            st.rerun()

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
    # ใช้ session_state ในการเปลี่ยนหน้า
    if st.session_state["page"] == "Register":
        register_page()
    else:
        login_page()

    # Sidebar สำหรับเปลี่ยนหน้า
    page_selection = st.sidebar.radio("📌 Select Page", ["Login", "Register"])
    st.session_state["page"] = page_selection  # อัปเดต session_state

if __name__ == "__main__":
    main()
