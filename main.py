import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px

# 1. Cấu hình & Kết nối
st.set_page_config(page_title="Quản Lý Tài Sản Vĩnh Viễn", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

# Đọc dữ liệu từ Google Sheets
def get_data():
    # Lưu ý: "Trang tính1" phải khớp với tên sheet bên dưới file Google Sheets của bạn
    return conn.read(worksheet="Trang tính1", ttl=0)

# 2. Hệ thống Tài khoản
if 'user' not in st.session_state:
    st.session_state['user'] = None

def login():
    st.title("🔐 Đăng nhập / Đăng ký")
    tab1, tab2 = st.tabs(["Đăng nhập", "Đăng ký"])
    df = get_data()

    with tab1:
        u = st.text_input("Tên đăng nhập")
        p = st.text_input("Mật khẩu", type="password")
        if st.button("Vào App"):
            # Kiểm tra tài khoản trong Database
            user_row = df[(df['username'] == u) & (df['password'].astype(str) == p)]
            if not user_row.empty:
                st.session_state['user'] = u
                st.rerun()
            else:
                st.error("Sai tài khoản hoặc mật khẩu!")

    with tab2:
        new_u = st.text_input("Tên đăng nhập mới")
        new_p = st.text_input("Mật khẩu mới", type="password")
        if st.button("Tạo tài khoản"):
            if new_u in df['username'].values:
                st.warning("Tên này đã có người dùng!")
            else:
                # Tạo dòng dữ liệu mới
                new_data = pd.DataFrame([{"username": new_u, "password": new_p, "co_phieu": 0, "bac": 0, "tiet_kiem": 0, "tien_mat": 0}])
                updated_df = pd.concat([df, new_data], ignore_index=True)
                conn.update(worksheet="Trang tính1", data=updated_df)
                st.success("Đã tạo xong! Hãy qua tab Đăng nhập.")

# 3. Giao diện chính (Sau khi đăng nhập)
def main_app():
    user = st.session_state['user']
    st.sidebar.write(f"👤 Tài khoản: **{user}**")
    if st.sidebar.button("Đăng xuất"):
        st.session_state['user'] = None
        st.rerun()

    st.title(f"💰 Quản Lý Tài Sản")
    df = get_data()
    # Lấy dữ liệu của đúng người dùng đang đăng nhập
    user_row = df[df['username'] == user].iloc[0]

    # Nhập liệu
    col1, col2 = st.columns(2)
    with col1:
        cp = st.number_input("Cổ phiếu (VNĐ)", value=int(user_row['co_phieu']), step=1000000)
        ba = st.number_input("Bạc (VNĐ)", value=int(user_row['bac']), step=100000)
    with col2:
        tk = st.number_input("Tiết kiệm (VNĐ)", value=int(user_row['tiet_kiem']), step=1000000)
        tm = st.number_input("Tiền mặt (VNĐ)", value=int(user_row['tien_mat']), step=100000)

    if st.button("💾 LƯU VÀO KÉT SẮT VĨNH VIỄN"):
        df.loc[df['username'] == user, ['co_phieu', 'bac', 'tiet_kiem', 'tien_mat']] = [cp, ba, tk, tm]
        conn.update(worksheet="Trang tính1", data=df)
        st.success("Đã cất dữ liệu an toàn vào Google Sheets!")

if st.session_state['user']:
    main_app()
else:
    login()
