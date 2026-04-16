import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Cấu hình giao diện
st.set_page_config(page_title="Quản Lý Tài Sản Cá Nhân", layout="wide", page_icon="💰")

# Hàm định dạng số có dấu chấm phân cách hàng nghìn (kiểu VN)
def format_vn(number):
    return "{:,.0f}".format(number).replace(",", ".")

# 2. Tiêu đề chính
st.title("💰 Hệ Thống Quản Lý Tài Sản Cá Nhân")
st.markdown("---")

# 3. Thanh bên (Sidebar) - Quản lý tài khoản & Thiết lập
with st.sidebar:
    st.header("🔑 Đăng nhập")
    user = st.text_input("Tên đăng nhập", "Người dùng")
    password = st.text_input("Mật khẩu", type="password")
    st.info("App đang chạy chế độ lưu trữ vĩnh viễn trên GitHub.")

# 4. Bố cục nhập liệu (Chia làm 2 cột)
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Danh mục Đầu tư")
    cp_val = st.number_input("Tổng giá trị Cổ phiếu (VNĐ)", min_value=0, step=1000000, format="%d")
    bac_val = st.number_input("Tổng giá trị Bạc (VNĐ)", min_value=0, step=100000, format="%d")

with col2:
    st.subheader("🛡️ Danh mục An toàn")
    tk_goc = st.number_input("Tiền gửi Tiết kiệm (VNĐ)", min_value=0, step=1000000, format="%d")
    lai_suat = st.number_input("Lãi suất gửi tiết kiệm (%/năm)", min_value=0.0, max_value=20.0, value=5.0, step=0.1)
    tm_val = st.number_input("Tiền mặt hiện có (VNĐ)", min_value=0, step=100000, format="%d")
    tm_note = st.text_input("Ghi chú vị trí tiền mặt", placeholder="Ví dụ: Két sắt, ngăn kéo bàn...")

# 5. Tính toán các chỉ số
tien_lai_1_nam = tk_goc * (lai_suat / 100)
tk_tong_1_nam = tk_goc + tien_lai_1_nam
tong_hien_tai = cp_val + bac_val + tk_goc + tm_val

# 6. Hiển thị kết quả Tổng quát
st.markdown("---")
st.subheader("📊 Báo cáo Tài sản Tổng thể")

# Hiển thị số tổng lớn
st.metric(label="TỔNG TÀI SẢN HIỆN TẠI", value=f"{format_vn(tong_hien_tai)} VNĐ")

# Hiển thị dự báo tiết kiệm nếu có gửi tiền
if tk_goc > 0:
    st.success(f"📌 **Dự báo tiết kiệm:** Sau 1 năm, bạn sẽ nhận được khoảng **{format_vn(tk_tong_1_nam)} VNĐ** (Tiền lãi: {format_vn(tien_lai_1_nam)} VNĐ)")

# 7. Biểu đồ phân bổ tài sản
if tong_hien_tai > 0:
    data = pd.DataFrame({
        'Loại tài sản': ['Cổ phiếu', 'Bạc', 'Tiết kiệm', 'Tiền mặt'],
        'Giá trị (VNĐ)': [cp_val, bac_val, tk_goc, tm_val]
    })
    
    fig = px.pie(data, values='Giá trị (VNĐ)', names='Loại tài sản', 
                 title='Cơ cấu danh mục tài sản',
                 hole=0.4, # Tạo biểu đồ dạng vòng (Donut chart) cho hiện đại
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Vui lòng nhập số liệu để xem biểu đồ phân tích.")

# 8. Chân trang
st.markdown("---")
st.caption(f"Ứng dụng được thiết kế riêng cho {user}. Cập nhật lần cuối: 16/04/2026")
