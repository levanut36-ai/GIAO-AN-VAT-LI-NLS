import streamlit as st
import google.generativeai as genai

# Cấu hình giao diện rộng để bảng chia cột hiển thị đẹp mắt
st.set_page_config(page_title="Giáo Án Vật Lí 5512 & NLS", page_icon="⚛️", layout="wide")

st.markdown("<h2 style='text-align: center; color: #1E88E5;'>⚛️ ỨNG DỤNG SOẠN GIÁO ÁN VẬT LÍ CHUẨN 5512 (SOẠN CUỐN CHIẾU)</h2>", unsafe_allow_html=True)
st.write("---")

# Thanh cấu hình bên trái
st.sidebar.header("🔑 Cấu hình hệ thống")
api_key = st.sidebar.text_input("Nhập Gemini API Key của bạn:", type="password", help="Lấy mã này từ Google AI Studio")

st.sidebar.write("---")
st.sidebar.header("🧭 CHỌN PHẦN MUỐN SOẠN")
# Thanh chọn này giúp giải quyết triệt để lỗi dừng giữa chừng của AI
phan_soan = st.sidebar.radio(
    "Bạn muốn AI tập trung soạn phần nào?",
    [
        "1. Khung đầu + Mục I (Mục tiêu) + Mục II (Học liệu)",
        "2. Mục III - Hoạt động 1: Khởi động",
        "3. Mục III - Hoạt động 2: Hình thành kiến thức",
        "4. Mục III - Hoạt động 3: Luyện tập",
        "5. Mục III - Hoạt động 4: Vận dụng"
    ]
)

st.sidebar.write("---")
st.sidebar.header("📚 Năng lực số (TT 02/2025)")
mien_nls = st.sidebar.selectbox(
    "Chọn miền năng lực số lồng ghép:",
    [
        "Miền I: Khai thác dữ liệu và thông tin trong môi trường số",
        "Miền II: Giao tiếp và hợp tác trong môi trường số",
        "Miền III: Sáng tạo nội dung số",
        "Miền IV: An toàn và bảo mật thông tin",
        "Miền V: Giải quyết sự cố công nghệ",
        "Miền VI: Ứng dụng Trí tuệ nhân tạo (AI)"
    ]
)

# Khung nhập thông tin bài học ở giữa
st.subheader("📝 Thông tin chung bài học")
col1, col2 = st.columns(2)

with col1:
    truong = st.text_input("Tên trường / Cơ sở giáo dục:", placeholder="Ví dụ: THPT Nguyễn Du...")
    giao_vien = st.text_input("Họ và tên giáo viên:", placeholder="Ví dụ: Nguyễn Văn A...")
    khoi_lop = st.selectbox("Khối lớp (Sách Kết nối tri thức):", ["Vật lí 10", "Vật lí 11", "Vật lí 12"])

with col2:
    to_chuyen_mon = st.text_input("Tổ / Nhóm chuyên môn:", placeholder="Ví dụ: Tổ Vật lí...")
    ten_bai = st.text_input("Tên bài dạy chính xác:", placeholder="Ví dụ: Động lượng...")
    so_tiet = st.number_input("Thời gian thực hiện (Số tiết):", min_value=1, max_value=6, value=2)

muc_tieu_rieng = st.text_area("Yêu cầu bổ sung đặc biệt (Nếu có):", placeholder="Ví dụ: Sử dụng thí nghiệm ảo...")

if st.button(f"🚀 Bắt đầu soạn: {phan_soan}", type="primary", use_container_width=True):
    if not api_key:
        st.error("❌ Vui lòng nhập API Key ở thanh menu bên trái!")
    elif not ten_bai:
        st.warning("⚠️ Vui lòng nhập Tên bài dạy.")
    else:
        with st.spinner(f"⏳ AI đang tập trung toàn bộ dung lượng để soạn chi tiết {phan_soan}..."):
            try:
                genai.configure(api_key=api_key)
                model_config = genai.GenerationConfig(max_output_tokens=8192, temperature=0.3)
                model = genai.GenerativeModel('gemini-2.5-flash', generation_config=model_config)
                
                # Khung lệnh cơ bản
                prompt_base = f"""
                Bạn là một chuyên gia giáo dục Vật lí xuất sắc. Hãy thiết kế một phần nội dung của kế hoạch bài dạy bám sát chương trình SGK KẾT NỐI TRI THỨC:
                - Bài dạy: {ten_bai} | Khối: {khoi_lop} | Số tiết: {so_tiet} tiết.
                - Trường: {truong} | Giáo viên: {giao_vien} | Tổ: {to_chuyen_mon}
                - Định hướng tích hợp Năng lực số: {mien_nls} theo Thông tư 02/2025/TT-BGDĐT.
                - Lưu ý: {muc_tieu_rieng}

                QUY TẮC CÔNG THỨC CHO MATHTYPE TRÊN WORD:
                Tất cả các công thức, phương trình Vật lí bắt buộc phải viết dưới dạng LaTeX trong cặp dấu $...$ (nếu nằm trên dòng) hoặc $$...$$ (nếu đứng riêng dòng). Ví dụ: $p = m \\cdot v$, $s = v_0 \\cdot t + \\frac{{1}}{{2}}at^2$. Tuyệt đối không dùng LaTeX cho chữ viết, tên hình, đơn vị đơn giản (m, s, kg). Tiêu đề mục phải bọc trong hai dấu sao để IN ĐẬM.
                """

                # Lệnh động theo từng phân đoạn
                if "1. Khung đầu" in phan_soan:
                    prompt_loai = """
                    Nhiệm vụ: Hãy soạn hoàn chỉnh phần đầu giáo án hành chính và:
                    **I. Mục tiêu**
                      1. Kiến thức: Nêu ngắn gọn yêu cầu cần đạt.
                      2. Năng lực: Ghi rõ năng lực chung, năng lực đặc thù vật lí và chỉ rõ năng lực số thành phần của miền năng lực số đã chọn.
                      3. Phẩm chất tương ứng.
                    **II. Thiết bị dạy học và học liệu** (Liệt kê thiết bị công nghệ, học liệu số sử dụng).
                    """
                else:
                    prompt_loai = f"""
                    Nhiệm vụ: Hãy soạn hoàn chỉnh duy nhất một hoạt động: **{phan_soan}** thuộc mục **III. Tiến trình dạy học**.
                    Yêu cầu bắt buộc viết đầy đủ, chi tiết, không được viết tắt, không dùng dấu ba chấm:
                      **a) Mục tiêu**: Phù hợp với hoạt động này.
                      **b) Nội dung**: Nhiệm vụ cụ thể học sinh phải làm.
                      **c) Sản phẩm**: Kết quả học tập kì vọng của học sinh một cách tổng quát, gọn gàng.
                      **d) Tổ chức thực hiện**: BẮT BUỘC phải dùng định dạng BẢNG chia thành 2 cột bằng Markdown Table:
                         - Cột 1: Tiến trình sư phạm (Gồm đầy đủ 4 bước hành động bắt buộc: **Bước 1: Chuyển giao nhiệm vụ**; **Bước 2: Thực hiện nhiệm vụ**; **Bước 3: Báo cáo, thảo luận**; **Bước 4: Kết luận, nhận định**).
                         - Cột 2: Hoạt động cụ thể của Giáo viên và Học sinh (Mô tả chi tiết hành động tương tác sư phạm dạy học, tập trung đan cài các hành động học sinh ứng dụng công nghệ/thiết bị số để phát triển năng lực số, viết rõ ràng hành động, không viết lời thoại dài).
                    """
                
                response = model.generate_content(prompt_base + prompt_loai)
                st.success("🎉 Đã soạn xong đoạn giáo án thành công!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"🔴 Đã xảy ra lỗi hệ thống: {e}")
