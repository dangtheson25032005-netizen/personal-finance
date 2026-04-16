import streamlit as st
import pandas as pd
from shspreadsheets import gsheets_connection # Thư viện kết nối Google Sheets

st.set_page_config(page_title="Quản Lý Tài Sản Cá Nhân", page_icon="🔒")

# --- QUẢN LÝ ĐĂNG NHẬP ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def login_page():
    st.title("🔐 Đăng nhập hệ thống")
    tab1, tab2 = st.tabs(["Đăng nhập", "Đăng ký tài khoản"])
    
    with tab1:
        user = st.text_input("Tên đăng nhập")
        pw = st.text_input("Mật khẩu", type="password")
        if st.button("Đăng nhập"):
            # Sau này code kết nối Google Sheets sẽ kiểm tra ở đây
            if user == "admin" and pw == "123": # Tài khoản tạm thời
                st.session_state['logged_in'] = True
                st.success("Đăng nhập thành công!")
                st.rerun()
            else:
                st.error("Sai tên đăng nhập hoặc mật khẩu")

    with tab2:
        st.subheader("Tạo tài khoản mới")
        new_user = st.text_input("Tên đăng nhập mới")
        new_pw = st.text_input("Mật khẩu mới", type="password")
        conf_pw = st.text_input("Xác nhận mật khẩu", type="password")
        if st.button("Xác nhận đăng ký"):
            st.info("Hệ thống đang gửi dữ liệu tới Google Sheets...")
            # Code lưu người dùng mới vào Google Sheets sẽ nằm ở đây

def main_app():
    st.title("💰 Quản Lý Tài Sản Cá Nhân")
    if st.sidebar.button("Đăng xuất"):
        st.session_state['logged_in'] = False
        st.rerun()
    
    # Tại đây dán lại phần code nhập liệu và biểu đồ tôi đã đưa hôm trước
    st.write(f"Chào mừng bạn quay trở lại!")

# Điều hướng
if st.session_state['logged_in']:
    main_app()
else:
    login_page()
