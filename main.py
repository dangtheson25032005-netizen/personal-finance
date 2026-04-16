import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px

# 1. Cấu hình trang
st.set_page_config(page_title="Quản Lý Tài Sản Cá Nhân", layout="wide", page_icon="💰")

# Kết nối Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Hàm đọc dữ liệu (Tự động nhận diện tên trang tính)
def get_data():
    try:
        # Ưu tiên đọc "Trang tính1" vì máy bạn đang hiển thị tên này
        return conn.read(worksheet="Trang tính1", ttl=0)
    except:
        try:
            # Nếu không thấy, thử đọc "Sheet1"
            return conn.read(worksheet="Sheet1", ttl=0)
        except:
            # Cuối cùng là đọc trang tính đầu tiên bất kỳ
            return conn.read(ttl=0)

# Hàm định dạng số VN (1.000.000)
def format_vn(number):
    try:
        return "{:,.0f}".format(float(number)).replace(",", ".")
    except:
        return "0"

# 2. Hệ thống tài khoản
if 'user' not in st.session_state:
    st.session_state['user'] = None

def login():
    st.title("🔐 Đăng nhập / Đăng ký")
    tab1, tab2 = st.tabs(["Đăng nhập", "Đăng ký"])
    
    try:
        df = get_data()
        # Tạo các cột cần thiết nếu file Sheets còn trống
        for col in ['username', 'password', 'co_phieu', 'bac', 'tiet_kiem', 'tien_mat']:
            if col not in df.columns:
                df[col] = "" if col in ['username', 'password'] else 0
    except Exception as e:
        st.error(f"Lỗi kết nối: {e}. Hãy kiểm tra lại link trong Secrets!")
        return

    with tab1:
        u = st.text_input("Tên đăng nhập")
        p = st.text_input("Mật khẩu", type="password")
        if st.button("Vào App"):
            if not df.empty:
                user_row = df[(df['username'].astype(str) == u) & (df['password'].astype(str) == p)]
                if not user_row.empty:
                    st.session_state['user'] = u
                    st.rerun()
                else:
                    st.error("Sai tài khoản hoặc mật khẩu!")
            else:
                st.info("Chưa có tài khoản nào. Hãy sang tab Đăng ký!")

    with tab2:
        new_u = st.text_input("Tên đăng nhập mới")
        new_p = st.text_input("Mật khẩu mới", type="password")
        if st.button("Tạo tài khoản"):
            if new_u in df['username'].astype(str).values:
                st.warning("Tên này đã tồn tại!")
            elif new_u and new_p:
                new_row = pd.DataFrame([{"username": new_u, "password": new_p, "co_phieu": 0, "bac": 0, "tiet_kiem": 0, "tien_mat": 0}])
                updated_df = pd.concat([df, new_row], ignore_index=True)
                # Lưu vào đúng trang tính bạn đang mở
                conn.update(worksheet="Trang tính1", data=updated_df)
                st.success("Đã tạo tài khoản thành công! Hãy quay lại Đăng nhập.")
            else:
                st.error("Vui lòng điền đủ thông tin.")

# 3. Giao diện quản lý tài sản
def main_app():
    user = st.session_state['user']
    st.sidebar.write(f"👤 Tài khoản: **{user}**")
    if st.sidebar.button("Đăng xuất"):
        st.session_state['user'] = None
        st.rerun()

    st.title(f"💰 Tài Sản Cá Nhân")
    df = get_data()
    user_row = df[df['username'].astype(str) == user].iloc[0]

    # Nhập liệu
    col1, col2 = st.columns(2)
    with col1:
        cp = st.number_input("Cổ phiếu (VNĐ)", value=int(user_row['co_phieu']), step=1000000)
        ba = st.number_input("Bạc (VNĐ)", value=int(user_row['bac']), step=100000)
    with col2:
        tk = st.number_input("Tiết kiệm (VNĐ)", value=int(user_row['tiet_kiem']), step=1000000)
        tm = st.number_input("Tiền mặt (VNĐ)", value=int(user_row['tien_mat']), step=100000)

    tong = cp + ba + tk + tm
    st.divider()
    st.metric("TỔNG TÀI SẢN HIỆN TẠI", f"{format_vn(tong)} VNĐ")

    if st.button("💾 LƯU DỮ LIỆU VĨNH VIỄN"):
        df.loc[df['username'].astype(str) == user, ['co_phieu', 'bac', 'tiet_kiem', 'tien_mat']] = [cp, ba, tk, tm]
        conn.update(worksheet="Trang tính1", data=df)
        st.success("Đã cất dữ liệu vào Google Sheets thành công!")

    # Biểu đồ phân bổ
    if tong > 0:
        data = pd.DataFrame({'Loại': ['Cổ phiếu', 'Bạc', 'Tiết kiệm', 'Tiền mặt'], 'Giá trị': [cp, ba, tk, tm]})
        fig = px.pie(data, values='Giá trị', names='Loại', hole=0.4, title="Cơ cấu tài sản")
        st.plotly_chart(fig)

if st.session_state['user']:
    main_app()
else:
    login()
