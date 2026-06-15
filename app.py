import streamlit as st
import google.generativeai as genai

# Cấu hình giao diện ứng dụng chuyên nghiệp, giao diện rộng rãi
st.set_page_config(page_title="Giáo Án Vật Lí Tích Hợp NLS & AI", page_icon="⚛️", layout="wide")

st.markdown("<h2 style='text-align: center; color: #1E88E5;'>⚛️ ỨNG DỤNG SOẠN GIÁO ÁN VẬT LÍ TRỌN GÓI (CV 5512 TÍCH HỢP NLS & AI)</h2>", unsafe_allow_html=True)
st.write("---")

# Thanh cấu hình và menu bên trái
st.sidebar.header("🔑 Cấu hình hệ thống")
api_key = st.sidebar.text_input("Nhập Gemini API Key của bạn:", type="password", help="Lấy mã này từ Google AI Studio")

st.sidebar.write("---")
st.sidebar.header("📚 Tích hợp Năng lực số (TT 02/2025) & AI")

# Ô chọn nhanh miền Năng lực số chủ đạo cần lồng ghép
mien_nls = st.sidebar.selectbox(
    "Chọn miền năng lực số chủ đạo cho bài học:",
    [
        "Miền I: Khai thác dữ liệu và thông tin trong môi trường số",
        "Miền II: Giao tiếp và hợp tác trong môi trường số",
        "Miền III: Sáng tạo nội dung số (Làm sản phẩm, sơ đồ tư duy...)",
        "Miền IV: An toàn và bảo mật thông tin trên không gian mạng",
        "Miền V: Giải quyết sự cố kỹ thuật và vấn đề công nghệ",
        "Miền VI: Ứng dụng Trí tuệ nhân tạo (AI) trong học tập Vật lí"
    ]
)

# Giao diện nhập liệu thông tin giáo án ở khung chính (Chia cột)
st.subheader("📝 Thông tin chung kế hoạch bài dạy")
col1, col2 = st.columns(2)

with col1:
    truong = st.text_input("Tên trường / Cơ sở giáo dục:", placeholder="Ví dụ: THPT Nguyễn Du...")
    giao_vien = st.text_input("Họ và tên giáo viên soạn:", placeholder="Ví dụ: Nguyễn Văn A...")
    khoi_lop = st.selectbox("Khối lớp (Môn Vật lí - Sách Kết nối tri thức):", ["Vật lí 10", "Vật lí 11", "Vật lí 12"])

with col2:
    to_chuyen_mon = st.text_input("Tổ / Nhóm chuyên môn:", placeholder="Ví dụ: Tổ Vật lí - Công nghệ...")
    ten_bai = st.text_input("Tên bài dạy chính xác:", placeholder="Ví dụ: Động lượng và Định luật bảo toàn động lượng...")
    so_tiet = st.number_input("Thời gian thực hiện (Số tiết):", min_value=1, max_value=6, value=2, step=1)

muc_tieu_rieng = st.text_area("Yêu cầu bổ sung hoặc lưu ý sư phạm đặc biệt (Nếu có):", 
                              placeholder="Ví dụ: Sử dụng phần mềm thí nghiệm ảo PhET, học sinh chuẩn bị phiếu học tập số trên máy tính...")

# Xử lý sự kiện bấm nút kích hoạt AI soạn giáo án trọn gói
if st.button("🚀 Bắt đầu soạn giáo án trọn gói chuẩn Word", type="primary", use_container_width=True):
    if not api_key:
        st.error("❌ Vui lòng nhập API Key ở thanh menu bên trái trước khi bắt đầu!")
    elif not ten_bai:
        st.warning("⚠️ Vui lòng điền 'Tên bài dạy chính xác' để hệ thống làm việc.")
    else:
        with st.spinner("⏳ Hệ thống AI đang phân bổ cấu trúc Công văn 5512 và lồng ghép Năng lực số..."):
            try:
                genai.configure(api_key=api_key)
                
                # Cấu hình tối ưu để AI tập trung viết một mạch dài không đứt gãy
                model_config = genai.GenerationConfig(
                    max_output_tokens=8192,
                    temperature=0.3
                )
                
                model = genai.GenerativeModel('gemini-2.5-flash', generation_config=model_config)
                
                # Câu lệnh Prompt tinh giản, ép AI viết trọn vẹn cả giáo án từ I đến III
                prompt = f"""
                Bạn là một chuyên gia giáo dục Vật lí xuất sắc cốt cán. Hãy thiết kế một kế hoạch bài dạy (Giáo án) trọn vẹn, khoa học bám sát chương trình sách giáo khoa KẾT NỐI TRI THỨC cho bài học sau:
                - Trường: {truong} | Tổ: {to_chuyen_mon} | Giáo viên: {giao_vien}
                - Tên bài dạy: {ten_bai}
                - Khối lớp: {khoi_lop} (Nguồn nội dung kiến thức cốt lõi phải lấy chính xác từ SGK Kết nối tri thức Vật lí khối này).
                - Thời gian thực hiện: {so_tiet} tiết (Hãy phân bổ phân phối thời gian cụ thể bằng số phút cho từng hoạt động sao cho tổng thời gian khớp với số tiết quy định).
                - Năng lực số tích hợp chủ đạo: {mien_nls} theo tinh thần Thông tư 02/2025/TT-BGDĐT.
                - Yêu cầu bổ sung: {muc_tieu_rieng}

                QUY TẮC CẤU TRÚC (Bắt buộc tuân thủ Phụ lục IV Công văn 5512):
                Hãy viết một mạch trọn vẹn đầy đủ các mục lớn từ đầu đến cuối bài, không được bỏ lửng, không dừng lại giữa chừng. Toàn bộ các tiêu đề đề mục phải được IN ĐẬM. Cấu trúc gồm:
                **I. Mục tiêu**
                  1. Kiến thức: Nêu ngắn gọn các yêu cầu cần đạt về kiến thức bám sát chương trình.
                  2. Năng lực: Ghi rõ năng lực chung, năng lực đặc thù vật lí và chỉ rõ năng lực số thành phần của {mien_nls} mà học sinh sẽ phát triển được qua bài học.
                  3. Phẩm chất: Các phẩm chất tương ứng (Trách nhiệm, chăm chỉ...).
                **II. Thiết bị dạy học và học liệu**
                  Liệt kê thiết bị của giáo viên, học sinh (máy tính, máy chiếu, các học liệu số, phần mềm hỗ trợ hoặc mô hình thí nghiệm ảo nếu có).
                **III. Tiến trình dạy học**
                  Bắt buộc viết đủ cả 4 hoạt động lớn liên tục: Hoạt động 1: Khởi động; Hoạt động 2: Hình thành kiến thức mới; Hoạt động 3: Luyện tập; Hoạt động 4: Vận dụng.
                  Trong MỖI hoạt động lớn, phải trình bày đầy đủ 4 mục nhỏ:
                    a) Mục tiêu
                    b) Nội dung (Nhiệm vụ chung của học sinh)
                    c) Sản phẩm (Nêu rõ kết quả học tập kỳ vọng của học sinh một cách khái quát, không cần đưa đáp án giải bài tập chi tiết dài dòng để giáo án được nhẹ nhàng, liền mạch).
                    d) Tổ chức thực hiện: BẮT BUỘC trình bày dạng BẢNG chia thành 2 cột bằng Markdown Table:
                       - Cột 1: Tiến trình sư phạm (Gồm 4 bước: **Bước 1: Chuyển giao nhiệm vụ**; **Bước 2: Thực hiện nhiệm vụ**; **Bước 3: Báo cáo, thảo luận**; **Bước 4: Kết luận, nhận định**).
                       - Cột 2: Hoạt động cụ thể của Giáo viên và Học sinh (Mô tả hành động, lệnh tương tác dạy và học. Tập trung đan cài các hành động học sinh ứng dụng công nghệ, thiết bị số hoặc AI để làm bài tập, thảo luận nhóm nhằm phát triển năng lực số).

                QUY TẮC ĐỊNH DẠNG CÔNG THỨC ĐỂ TƯƠNG THÍCH MATHTYPE TRÊN WORD:
                1. MỌI CÔNG THỨC TOÁN HỌC VÀ BIỂU THỨC VẬT LÍ: Bắt buộc viết dưới dạng ký hiệu LaTeX trong cặp dấu $...$ (nếu nằm trên cùng dòng chữ) hoặc $$...$$ (nếu nằm riêng một dòng độc lập) để người dùng có thể mở Word ra và dùng tính năng "Toggle TeX" của phần mềm MathType chuyển đổi tự động sang công thức chỉnh sửa được. Ví dụ: $p = m \\cdot v$, $A = F \\cdot s \\cdot \\cos\\alpha$, $s = v_0 \\cdot t + \\frac{{1}}{{2}}at^2$.
                2. TUYỆT ĐỐI KHÔNG DÙNG KÝ HIỆU LATEX cho văn bản chữ viết thông thường, tên hình (ví dụ: Hình 1), tên điểm (ví dụ: điểm A, điểm B), đơn vị đo đơn giản (m, s, kg, N, m/s). Chỉ dùng LaTeX cho phương trình, hệ thức phức tạp cần gõ bằng toán học.
                3. Các tiêu đề lớn nhỏ bắt buộc bọc trong dấu hai sao để in đậm rõ ràng. Không sử dụng dấu ba chấm (...) để viết tắt hoặc bỏ lửng tiến trình sư phạm.
                """
                
                response = model.generate_content(prompt)
                
                st.success("🎉 Đã thiết kế giáo án trọn gói thành công! Bạn có thể xem nội dung bên dưới:")
                st.markdown(response.text)
                
                st.write("---")
                st.info("💡 HƯỚNG DẪN XUẤT WORD & CHUYỂN CÔNG THỨC MATHTYPE:\n1. Bạn dùng chuột bôi đen toàn bộ nội dung giáo án ở trên, bấm chuột phải chọn Copy (Sao chép).\n2. Mở một file Microsoft Word trống trên máy tính của bạn ra, bấm chuột phải chọn Paste (Dán) dạng Keep Source Formatting. Các tiêu đề sẽ tự in đậm và các bảng chia cột 5512 sẽ tự động hiển thị cực kỳ đẹp mắt.\n3. Đối với các công thức Vật lí dạng $...$: Bạn chỉ cần bôi đen toàn bộ văn bản trong Word, sau đó nhấn tổ hợp phím Alt + \\ (hoặc vào thanh menu MathType trên Word, bấm nút 'Toggle TeX'). Phần mềm MathType sẽ tự động biến đổi tất cả các ký hiệu $...$ thành công thức cấu trúc MathType chuẩn chỉnh để bạn bấm đúp chuột vào chỉnh sửa rất dễ dàng!")
                
            except Exception as e:
                st.error(f"🔴 Đã xảy ra lỗi hệ thống: {e}. Vui lòng kiểm tra lại API Key hoặc liên hệ hỗ trợ.")
