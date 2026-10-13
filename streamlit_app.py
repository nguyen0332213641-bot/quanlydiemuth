import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cấu hình trang web rộng rãi và có tiêu đề
st.set_page_config(page_title="Quản lý điểm UTH", layout="wide")

# Hiển thị tiêu đề Web App
st.title("QUẢN LÝ ĐIỂM SINH VIÊN - UTH")

# 1. Khởi tạo dữ liệu
data = {
    'STT': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'Họ và tên': ['An', 'Tiến', 'Tiền', 'Hào', 'Dũng', 'Đô', 'Tuấn', 'Thành', 'Thư', 'Trung'],
    'Chuyên cần': [8, 9, 3, 10, 8, 6, 9, 8, 7, 10],
    'Giữa kỳ': [7, 8, 6, 3, 7, 5, 8, 7, 7, 9],
    'Cuối kỳ': [8, 8, 3, 6, 7, 6, 8, 6, 8, 9]
}
df = pd.DataFrame(data)
df.set_index('STT', inplace=True)

# 2. Xử lý tính toán (Điểm tổng kết & Xếp loại)
df['Tong_ket'] = df['Chuyên cần']*0.2 + df['Giữa kỳ']*0.3 + df['Cuối kỳ']*0.5

def xep_loai(diem):
    if diem >= 8.5: return 'Giỏi'
    elif diem >= 7.0: return 'Khá'
    elif diem >= 5.0: return 'Trung bình'
    else: return 'Yếu'
df['Xep_loai'] = df['Tong_ket'].apply(xep_loai)

# 3. Giao diện hiển thị
st.subheader("1. Bảng điểm chi tiết")
st.dataframe(df, use_container_width=True)

st.subheader("2. Thống kê tổng quan")
dtb_lop = df['Tong_ket'].mean()
sv_cao_nhat = df[df['Tong_ket'] == df['Tong_ket'].max()]['Họ và tên'].tolist()
sv_thap_nhat = df[df['Tong_ket'] == df['Tong_ket'].min()]['Họ và tên'].tolist()
so_sv_dat = len(df[df['Tong_ket'] >= 5.0])

# Hiển thị thống kê dạng cột cho đẹp
col1, col2, col3, col4 = st.columns(4)
col1.metric("Trung bình lớp", f"{dtb_lop:.2f}")
col2.metric("Điểm cao nhất", f"{df['Tong_ket'].max()}")
col3.metric("Điểm thấp nhất", f"{df['Tong_ket'].min()}")
col4.metric("Số SV đạt", f"{so_sv_dat}/10")

st.write(f"- **Sinh viên điểm cao nhất:** {', '.join(sv_cao_nhat)}")
st.write(f"- **Sinh viên điểm thấp nhất:** {', '.join(sv_thap_nhat)}")

st.subheader("3. Tra cứu điểm sinh viên")
selected_student = st.selectbox("Chọn một sinh viên:", df['Họ và tên'])
student_info = df[df['Họ và tên'] == selected_student].iloc[0]

st.info(f"""
**Họ và tên:** {student_info['Họ và tên']}  
**Chuyên cần:** {student_info['Chuyên cần']} | **Giữa kỳ:** {student_info['Giữa kỳ']} | **Cuối kỳ:** {student_info['Cuối kỳ']}  
**Điểm tổng kết:** {student_info['Tong_ket']} | **Xếp loại:** {student_info['Xep_loai']}
""")

st.subheader("4. Biểu đồ cột: Điểm tổng kết")
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(df['Họ và tên'], df['Tong_ket'], color='#2563eb', edgecolor='black', linewidth=0.5)
ax.set_title('Điểm tổng kết của 10 sinh viên', fontsize=12, fontweight='bold')
ax.set_xlabel('Sinh viên', fontsize=10)
ax.set_ylabel('Điểm', fontsize=10)
ax.set_ylim(0, 10) # Set trục Y từ 0 đến 10
plt.xticks(rotation=0) # Tên nằm ngang cho dễ đọc
plt.grid(axis='y', linestyle='--', alpha=0.6) # Thêm lưới ngang
st.pyplot(fig)

# Hiển thị họ tên và MSSV ở cuối trang
st.markdown("---")
st.markdown("""
<div style='text-align: center; font-size: 14px; background-color: #eff6ff; padding: 10px; border-radius: 10px; color: #1e3a8a;'>
    Sinh viên thực hiện: <b>Nguyễn Ngọc Nguyên</b> | MSSV: <b>060208009198</b>
</div>
""", unsafe_allow_html=True)
