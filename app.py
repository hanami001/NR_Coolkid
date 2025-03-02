import streamlit as st
from engine import UserManager, BANKS, CARD_TYPES, LIFESTYLES

# Initialize UserManager
user_manager = UserManager()

def init_session_state():
    """Initialize session state variables if they don't exist"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'show_register' not in st.session_state:
        st.session_state.show_register = False

def login_page():
    """Render login page"""
    st.title("เข้าสู่ระบบ")
    
    with st.form("login_form"):
        username = st.text_input("ชื่อผู้ใช้", key="login_username")
        password = st.text_input("รหัสผ่าน", type="password", key="login_password")
        
        col1, col2 = st.columns(2)
        with col1:
            login_button = st.form_submit_button("เข้าสู่ระบบ")
        with col2:
            register_button = st.form_submit_button("ลงทะเบียน")
    
    if login_button:
        if user_manager.authenticate_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("เข้าสู่ระบบสำเร็จ!")
            st.rerun()
        else:
            st.error("ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง")
    
    if register_button:
        st.session_state.show_register = True
        st.rerun()

def register_page():
    """Render registration page"""
    st.title("ลงทะเบียน")
    
    with st.form("register_form"):
        username = st.text_input("ชื่อผู้ใช้", key="register_username")
        password = st.text_input("รหัสผ่าน", type="password", key="register_password")
        confirm_password = st.text_input("ยืนยันรหัสผ่าน", type="password", key="confirm_password")
        
        bank = st.selectbox("ธนาคารที่ถือบัตรเครดิต", options=BANKS)
        card_type = st.selectbox("ประเภทบัตรเครดิตที่ถือ", options=CARD_TYPES)
        lifestyle = st.selectbox("ไลฟ์สไตล์ของคุณ", options=LIFESTYLES)
        
        col1, col2 = st.columns(2)
        with col1:
            submit_button = st.form_submit_button("ลงทะเบียน")
        with col2:
            back_button = st.form_submit_button("กลับ")
    
    if submit_button:
        if password != confirm_password:
            st.error("รหัสผ่านไม่ตรงกัน")
        elif not username or not password:
            st.error("กรุณากรอกชื่อผู้ใช้และรหัสผ่าน")
        else:
            success, message = user_manager.register_user(username, password, bank, card_type, lifestyle)
            if success:
                st.success(message)
                st.session_state.show_register = False
                st.rerun()
            else:
                st.error(message)
    
    if back_button:
        st.session_state.show_register = False
        st.rerun()

def main_app():
    """Render main application after login"""
    st.title(f"ยินดีต้อนรับ, {st.session_state.username}!")
    
    # Get user data
    user_data = user_manager.get_user_data(st.session_state.username)
    
    st.write("## ข้อมูลของคุณ")
    st.write(f"**ธนาคาร:** {user_data['bank']}")
    st.write(f"**ประเภทบัตรเครดิต:** {user_data['card_type']}")
    st.write(f"**ไลฟ์สไตล์:** {user_data['lifestyle']}")
    
    # Logout button
    if st.button("ออกจากระบบ"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()

def main():
    """Main function to run the app"""
    init_session_state()
    
    if st.session_state.logged_in:
        main_app()
    else:
        if st.session_state.show_register:
            register_page()
        else:
            login_page()

if __name__ == "__main__":
    main()
