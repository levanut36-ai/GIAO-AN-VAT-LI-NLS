import streamlit as st
import google.generativeai as genai

# Cấu hình giao diện ứng dụng chuyên nghiệp
st.set_page_config(page_title="Giáo Án Vật Lí 5512 & NLS", page_icon="⚛️", layout="wide")

st.markdown("<h2 style='text-align: center; color: #1E88E5;'>⚛️ ỨNG DỤNG SOẠN GIÁO ÁN VẬT LÍ 5512 (BẢN KHẮC PHỤC LỖI DỪNG HÌNH)</h2>", unsafe_allow_html=True)
st.write("---")

# Thanh cấu hình bên trái
st.sidebar.header("🔑 Cấu hình hệ thống")
api_key = st.sidebar.text_input("Nhập Gemini API Key của bạn:", type="password", help="Lấy mã này từ Google AI Studio")

st.sidebar.write("---")
st.sidebar.header("🧭 CHỌN PHẦN MUỐN SOẠN")
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
        "Miền VI: Ứng dụng Trí tuệ nhân tạo (AI) trong học tập Vật lí"
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

muc_tieu_rieng = st.text_area("Yêu cầu bổ sung đặc biệt (Nếu có):", placeholder="Ví dụ: Sử dụng thí nghiệm ảo PhET...")

if st.button(f"🚀 Bắt đầu soạn: {phan_soan}", type="primary", use_container_width=True):
    if not api_key:
        st.error("❌ Vui lòng nhập API Key ở thanh menu bên trái!")
    elif not ten_bai:
        st.warning("⚠️ Vui lòng nhập Tên bài dạy.")
    else:
        with st.spinner(f"⏳ Hệ thống đang dồn toàn bộ lực lượng soạn chi tiết {phan_soan}..."):
            try:
                genai.configure(api_key=api_key)
                model_config = genai.GenerationConfig(max_output_tokens=8192, temperature=0.3)
                model = genai.GenerativeModel('gemini-2.5-flash', generation_config=model_config)
                
                tong_thoi_gian = so_tiet * 45
                
                prompt_base = f"""
                Bạn là một chuyên gia giáo dục Vật lí xuất sắc. Hãy thiết kế một phần nội dung của kế hoạch bài dạy bám sát chương trình SGK KẾT NỐI TRI THỨC:
                - Bài dạy: {ten_bai} | Khối: {khoi_lop} | Số tiết: {so_tiet} tiết (Tổng {tong_thoi_gian} phút).
                - Định hướng tích hợp Năng lực số: {mien_nls} bám sát Thông tư 02/2025/TT-BGDĐT.
                - Yêu cầu khác: {muc_tieu_rieng}

                QUY TẮC CÔNG THỨC CHO MATHTYPE TRÊN WORD:
                Tất cả các công thức, phương trình Vật lí bắt buộc phải viết dưới dạng LaTeX trong cặp dấu $...$ (nếu nằm trên dòng) hoặc $$...$$ (nếu đứng riêng dòng). Ví dụ: $p = m \\cdot v$, $s = v_0 \\cdot t + \\frac{{1}}{{2}}at^2$. Tuyệt đối không dùng LaTeX cho chữ viết, tên hình, đơn vị đơn giản. Tiêu đề mục phải bọc trong hai dấu sao để IN ĐẬM.
                """

                prompt_ai_mienvidacbiet = ""
                if "Miền VI" in mien_nls:
                    prompt_ai_mienvidacbiet = """
                    BỞI VÌ người dùng chọn tích hợp Miền VI (Ứng dụng AI), bạn bắt buộc phải đưa vào các tình huống thực tế: Hướng dẫn học sinh biết cách đặt câu lệnh (Prompt) cho AI hỗ trợ học tập, nhưng phải có bước học sinh phản biện, rà soát đối chiếu thông tin AI cung cấp với SGK Kết nối tri thức để phát hiện lỗi sai, tuân thủ đạo đức học thuật.
                    """

                if "1. Khung đầu" in phan_soan:
                    prompt_loai = f"""
                    Nhiệm vụ: Hãy soạn hoàn chỉnh phần đầu giáo án hành chính Trường: {truong}, Tổ: {to_chuyen_mon}, Giáo viên: {giao_vien} và:
                    **I. Mục tiêu**
                      1. Kiến thức: Nêu ngắn gọn yêu cầu cần đạt bám sát chương trình.
                      2. Năng lực: Năng lực chung, đặc thù vật lí và chỉ rõ năng lực số thành phần của miền năng lực số đã chọn.
                      3. Phẩm chất tương ứng.
                    **II. Thiết bị dạy học và học liệu**
                    """
                else:
                    prompt_loai = f"""
                    Nhiệm vụ: Hãy soạn hoàn chỉnh duy nhất một hoạt động: **{phan_soan}** thuộc mục **III. Tiến trình dạy học**.
                    Yêu cầu bắt buộc viết đầy đủ, chi tiết, không dùng dấu ba chấm:
                      **a) Mục tiêu**: Phù hợp với hoạt động này (Ghi rõ số phút khuyến nghị dựa trên tổng thời gian bài học).
                      **b) Nội dung**: Nhiệm vụ cụ thể học sinh phải làm.
                      **c) Sản phẩm**: Kết quả học tập kì vọng gọn gàng.
                      **d) Tổ chức thực hiện**: 
                      QUY TẮC TUYỆT ĐỐI: KHÔNG ĐƯỢC VẼ BẢNG MARKDOWN (không dùng các ký tự gạch dọc |). 
                      Hãy trình bày phần Tổ chức thực hiện này bằng cách liệt kê rõ ràng theo đúng 4 bước của Công văn 5512 bằng định dạng văn bản in đậm và gạch đầu dòng như sau:
                      
                      - **Bước 1: Chuyển giao nhiệm vụ**: (Mô tả chi tiết hành động cụ thể của Giáo viên khi giao nhiệm vụ và Học sinh khi tiếp nhận nhiệm vụ. Có lồng ghép công nghệ hoặc AI nếu có yêu cầu).
                      - **Bước 2: Thực hiện nhiệm vụ**: (Mô tả hành động của Học sinh khi làm bài, tự học, thảo luận nhóm và hành động theo dõi, trợ giúp của Giáo viên).
                      - **Bước 3: Báo cáo, thảo luận**: (Mô tả hành động Học sinh đại diện trình bày, chia sẻ kết quả và các học sinh khác nhận xét, phản biện).
                      - **Bước 4: Kết luận, nhận định**: (Mô tả hành động Giáo viên chính xác hóa kiến thức Vật lí, nhận xét đánh giá chốt lại vấn đề).
                    """
                
                response = model.generate_content(prompt_base + prompt_ai_mienvidacbiet + prompt_loai)
                st.success(f"🎉 Đã soạn xong {phan_soan} thành công!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"🔴 Đã xảy ra lỗi hệ thống: {e}")
