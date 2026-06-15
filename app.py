import streamlit as st
import google.generativeai as genai

# Cấu hình giao diện trang web rộng rãi, chuyên nghiệp
st.set_page_config(page_title="Giáo Án Vật Lí 5512 & NLS", page_icon="⚛️", layout="wide")

st.markdown("<h2 style='text-align: center; color: #1E88E5;'>⚛️ ỨNG DỤNG SOẠN GIÁO ÁN VẬT LÍ TRỌN GÓI MỘT MẠCH (CHUẨN 5512 & NLS)</h2>", unsafe_allow_html=True)
st.write("---")

# Thanh cấu hình bên trái
st.sidebar.header("🔑 Cấu hình hệ thống")
api_key = st.sidebar.text_input("Nhập Gemini API Key của bạn:", type="password", help="Lấy mã này từ Google AI Studio")

st.sidebar.write("---")
st.sidebar.header("📚 Năng lực số (TT 02/2025)")
mien_nls = st.sidebar.selectbox(
    "Chọn miền năng lực số lồng ghép chủ đạo:",
    [
        "Miền I: Khai thác dữ liệu và thông tin trong môi trường số",
        "Miền II: Giao tiếp và hợp tác trong môi trường số",
        "Miền III: Sáng tạo nội dung số",
        "Miền IV: An toàn và bảo mật thông tin",
        "Miền V: Giải quyết sự cố công nghệ và vấn đề kỹ thuật",
        "Miền VI: Ứng dụng Trí tuệ nhân tạo (AI) vào học tập"
    ]
)

# Khung nhập thông tin bài học Vật lí ở giao diện chính
st.subheader("📝 Thông tin chung bài học")
col1, col2 = st.columns(2)

with col1:
    truong = st.text_input("Tên trường / Cơ sở giáo dục:", placeholder="Ví dụ: THPT Nguyễn Du...")
    giao_vien = st.text_input("Họ và tên giáo viên:", placeholder="Ví dụ: Nguyễn Văn A...")
    khoi_lop = st.selectbox("Khối lớp (Môn Vật lí - Sách Kết nối tri thức):", ["Vật lí 10", "Vật lí 11", "Vật lí 12"])

with col2:
    to_chuyen_mon = st.text_input("Tổ / Nhóm chuyên môn:", placeholder="Ví dụ: Tổ Vật lí - Công nghệ...")
    ten_bai = st.text_input("Tên bài dạy chính xác:", placeholder="Ví dụ: Động lượng...")
    so_tiet = st.number_input("Thời gian thực hiện (Số tiết):", min_value=1, max_value=6, value=2)

muc_tieu_rieng = st.text_area("Yêu cầu bổ sung hoặc công cụ số muốn sử dụng (Nếu có):", 
                              placeholder="Ví dụ: Sử dụng thí nghiệm ảo PhET, điện thoại thông minh...")

if st.button("🚀 BẮT ĐẦU SOẠN GIÁO ÁN TRỌN GÓI MỘT MẠCH", type="primary", use_container_width=True):
    if not api_key:
        st.error("❌ Vui lòng nhập API Key ở thanh menu bên trái trước!")
    elif not ten_bai:
        st.warning("⚠️ Vui lòng nhập Tên bài dạy chính xác.")
    else:
        with st.spinner("⏳ Trợ lý AI đang áp dụng siêu dung lượng để soạn một mạch toàn bộ giáo án... Vui lòng đợi khoảng 30 giây!"):
            try:
                genai.configure(api_key=api_key)
                # Kích hoạt toàn bộ sức mạnh số từ đầu ra cho Gemini 2.5 Flash
                model_config = genai.GenerationConfig(max_output_tokens=65535, temperature=0.3)
                model = genai.GenerativeModel('gemini-2.5-flash', generation_config=model_config)
                
                tong_thoi_gian = so_tiet * 45
                
                # Truyền biến trực tiếp vào Prompt bằng cách gộp chuỗi an toàn nhất của Python
                prompt = (
                    "Bạn là một chuyên gia giáo dục Vật lí xuất sắc cốt cán. Hãy thiết kế một kế hoạch bài dạy (Giáo án) HOÀN CHỈNH, TRỌN GÓI TỪ ĐẦU ĐẾN CUỐI bám sát chương trình SGK KẾT NỐI TRI THỨC môn Vật lí.\n\n"
                    "Thông tin ngữ cảnh bài học:\n"
                    "- Trường: " + str(truong) + "\n"
                    "- Tổ chuyên môn: " + str(to_chuyen_mon) + "\n"
                    "- Giáo viên: " + str(giao_vien) + "\n"
                    "- Tên bài dạy: " + str(ten_bai) + "\n"
                    "- Khối lớp: " + str(khoi_lop) + "\n"
                    "- Số tiết thực hiện: " + str(so_tiet) + " tiết (Tổng cộng " + str(tong_thoi_gian) + " phút).\n"
                    "- Định hướng lồng ghép Năng lực số: " + str(mien_nls) + " bám sát Thông tư 02/2025/TT-BGDĐT.\n"
                    "- Lưu ý riêng: " + str(muc_tieu_rieng) + "\n\n"
                    "YÊU CẦU CẤU TRÚC VÀ ĐỊNH DẠNG (BẮT BUỘC TUÂN THỦ PHỤ LỤC IV CÔNG VĂN 5512):\n"
                    "Hãy soạn một mạch liên tục toàn bộ bài từ đầu đến cuối, không được bỏ lửng nội dung. Trình bày đẹp bằng Markdown, các tiêu đề mục lớn nhỏ phải được IN ĐẬM.\n"
                    "**I. MỤC TIÊU** (Ghi ngắn gọn Kiến thức; Năng lực đặc thù vật lí, Năng lực chung, Năng lực số thành phần cụ thể; Phẩm chất).\n"
                    "**II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU** (Thiết bị; Học liệu SGK Kết nối tri thức; Công cụ số áp dụng và Mục đích sử dụng).\n"
                    "**III. TIẾN TRÌNH DẠY HỌC**\n"
                    "Phải viết đủ cả 4 hoạt động liên tục, phân bổ rõ thời lượng số phút dự kiến cho mỗi hoạt động (Hoạt động 1: Mở đầu; Hoạt động 2: Hình thành kiến thức mới; Hoạt động 3: Luyện tập; Hoạt động 4: Vận dụng).\n"
                    "Trong MỖI hoạt động lớn, phải trình bày đầy đủ mục: a) Mục tiêu; b) Nội dung; c) Sản phẩm học tập.\n"
                    "Riêng mục d) Tổ chức thực hiện: BẮT BUỘC PHẢI VẼ BẢNG CHIA THÀNH 3 CỘT chuẩn bằng bảng Markdown. Cấu trúc bảng gồm:\n"
                    "  - Cột 1: Tiến trình sư phạm (Gồm đầy đủ 4 bước hành động bắt buộc: Bước 1: Chuyển giao nhiệm vụ; Bước 2: Thực hiện nhiệm vụ; Bước 3: Báo cáo, thảo luận; Bước 4: Kết luận, nhận định).\n"
                    "  - Cột 2: Hoạt động cụ thể của Giáo viên và Học sinh (Mô tả chi tiết hành động tương tác sư phạm thực tế dạy và học cho từng bước, không viết lời thoại dài dạng kịch bản, không dùng ký hiệu GV, HS).\n"
                    "  - Cột 3: Năng lực số (Ghi ngắn gọn năng lực số thành phần lồng ghép tại bước đó để phát triển kỹ năng công nghệ cho học sinh, nếu bước đó không dùng ghi Không tích hợp).\n"
                    "**IV. KIỂM TRA, ĐÁNH GIÁ** (Hình thức đánh giá các hoạt động học tập).\n\n"
                    "QUY TẮC CÔNG THỨC MATHTYPE TRÊN WORD:\n"
                    "Tất cả các công thức, biểu thức, phương trình Vật lí bắt buộc phải viết dưới dạng LaTeX trong cặp dấu $...$ (nếu nằm trên cùng dòng chữ) hoặc $$...$$ (nếu đứng riêng một dòng độc lập) để khi người dùng dán vào Word có thể dùng tính năng 'Toggle TeX' (Alt + \\) của MathType đổi sang công thức chỉnh sửa được một cách dễ dàng. Tuyệt đối không dùng LaTeX cho chữ viết thông thường, tên hình, tên điểm, đơn vị đo đơn giản (m, s, kg)."
                )

                response = model.generate_content(prompt)
                
                st.success("🎉 Trợ lý AI đã thiết kế xong toàn bộ giáo án trọn gói!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"🔴 Đã xảy ra lỗi hệ thống: {e}")
