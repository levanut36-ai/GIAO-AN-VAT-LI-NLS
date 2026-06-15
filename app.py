import streamlit as st
import google.generativeai as genai

# Cấu hình giao diện ứng dụng chuyên nghiệp
st.set_page_config(page_title="Giáo Án Vật Lí Tích Hợp NLS & AI", page_icon="⚛️", layout="wide")

st.markdown("<h2 style='text-align: center; color: #1E88E5;'>⚛️ ỨNG DỤNG SOẠN GIÁO ÁN VẬT LÍ TỰ ĐỘNG (KNTT - CV 5512 - TT 02/2025)</h2>", unsafe_allow_html=True)
st.write("---")

# Thanh cấu hình và menu bên trái
st.sidebar.header("🔑 Cấu hình hệ thống")
api_key = st.sidebar.text_input("Nhập Gemini API Key của bạn:", type="password", help="Lấy mã này từ Google AI Studio")

st.sidebar.write("---")
st.sidebar.header("📚 Lựa chọn Năng lực số (TT 02/2025)")

# Ô chọn nhanh 6 miền Năng lực số chính
mien_nls = st.sidebar.selectbox(
    "Chọn miền năng lực số chủ đạo cho bài học:",
    [
        "Miền I: Khai thác dữ liệu và thông tin",
        "Miền II: Giao tiếp và hợp tác trong môi trường số",
        "Miền III: Sáng tạo nội dung số",
        "Miền IV: An toàn",
        "Miền V: Giải quyết vấn đề",
        "Miền VI: Ứng dụng trí tuệ nhân tạo"
    ]
)

# Ô chọn nhanh 8 bậc năng lực
bac_nls = st.sidebar.select_slider(
    "Chọn Bậc thành thạo mục tiêu (Từ Bậc 1 đến Bậc 8):",
    options=["Bậc 1", "Bậc 2", "Bậc 3", "Bậc 4", "Bậc 5", "Bậc 6", "Bậc 7", "Bậc 8"],
    value="Bậc 3"
)

# Giao diện nhập liệu thông tin giáo án ở khung chính (Chia cột)
st.subheader("📝 Thông tin chung bài học")
col1, col2 = st.columns(2)

with col1:
    truong = st.text_input("Tên trường / Cơ sở giáo dục:", placeholder="Ví dụ: THPT Nguyễn Du...")
    giao_vien = st.text_input("Họ và tên giáo viên soạn:", placeholder="Ví dụ: Nguyễn Văn A...")
    khoi_lop = st.selectbox("Khối lớp (Môn Vật lí - Sách Kết nối tri thức):", ["Vật lí 10", "Vật lí 11", "Vật lí 12"])

with col2:
    to_chuyen_mon = st.text_input("Tổ / Nhóm chuyên môn:", placeholder="Ví dụ: Tổ Vật lí - Công nghệ...")
    ten_bai = st.text_input("Tên bài dạy chính xác:", placeholder="Ví dụ: Động lượng và Định luật bảo toàn động lượng...")
    so_tiet = st.number_input("Thời gian thực hiện (Số tiết):", min_value=1, max_value=6, value=2, step=1)

muc_tieu_rieng = st.text_area("Yêu cầu bổ sung hoặc lưu ý đặc biệt (Nếu có):", 
                              placeholder="Ví dụ: Tập trung vào thí nghiệm ảo, học sinh cần chuẩn bị điện thoại thông minh...")

# Xử lý sự kiện bấm nút kích hoạt AI soạn giáo án
if st.button("🚀 Bắt đầu soạn giáo án chuẩn Word", type="primary", use_container_width=True):
    if not api_key:
        st.error("❌ Vui lòng nhập API Key ở thanh menu bên trái trước khi bắt đầu!")
    elif not ten_bai:
        st.warning("⚠️ Vui lòng điền 'Tên bài dạy chính xác' để hệ thống lập trình.")
    else:
        with st.spinner("⏳ Hệ thống đang rà soát kiến thức Kết nối tri thức và thiết kế giáo án chia cột..."):
            try:
                genai.configure(api_key=api_key)
                # Sử dụng dòng mô hình mới ổn định lâu dài
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # Câu lệnh Prompt cực kỳ chi tiết, ép AI tuân thủ mọi quy tắc văn bản
                prompt = f"""
                Bạn là một chuyên gia giáo dục Vật lí xuất sắc cốt cán. Hãy thiết kế một kế hoạch bài dạy (Giáo án) chi tiết, khoa học bám sát chương trình sách giáo khoa KẾT NỐI TRI THỨC cho bài học sau:
                - Trường: {truong} | Tổ: {to_chuyen_mon} | Giáo viên: {giao_vien}
                - Tên bài dạy: {ten_bai}
                - Khối lớp: {khoi_lop} (Nguồn nội dung, đơn vị kiến thức, định luật phải lấy chính xác từ SGK Kết nối tri thức Vật lí khối này).
                - Thời gian thực hiện: {so_tiet} tiết (Hãy phân bổ phân phối thời gian cụ thể bằng số phút cho từng hoạt động sao cho tổng thời gian khớp với {so_tiet} tiết, mỗi tiết 45 phút).
                - Mục tiêu Năng lực số tích hợp: {mien_nls} ở trình độ thành thạo mục tiêu là {bac_nls} theo Thông tư 02/2025/TT-BGDĐT.
                - Yêu cầu bổ sung: {muc_tieu_rieng}

                QUY TẮC CẤU TRÚC (Bắt buộc tuân thủ Phụ lục IV Công văn 5512):
                Văn bản xuất ra phải được trình bày theo cấu trúc phân cấp nghiêm ngặt. Các tiêu đề mục phải được IN ĐẬM.
                I. Mục tiêu (Ghi rõ Kiến thức, Năng lực - đặc biệt là năng lực số thành phần của {mien_nls} đạt {bac_nls}, và Phẩm chất).
                II. Thiết bị dạy học và học liệu (Liệt kê cụ thể, bao gồm cả học liệu số hoặc công nghệ áp dụng).
                III. Tiến trình dạy học: Gồm 4 hoạt động bắt buộc.
                Trong MỖI hoạt động lớn (Hoạt động 1: Khởi động, Hoạt động 2: Hình thành kiến thức mới, Hoạt động 3: Luyện tập, Hoạt động 4: Vận dụng), phải trình bày đủ:
                  a) Mục tiêu
                  b) Nội dung
                  c) Sản phẩm (Bắt buộc phải viết chi tiết đáp án, lời giải bài tập, kết quả, định luật, không được bỏ trống hoặc ghi khái quát).
                  d) Tổ chức thực hiện: Phần này BẮT BUỘC phải dùng định dạng BẢNG chia thành 2 cột bằng Markdown Table:
                     - Cột 1: Tiến trình sư phạm (Gồm 4 bước: Bước 1: Chuyển giao nhiệm vụ; Bước 2: Thực hiện nhiệm vụ; Bước 3: Báo cáo, thảo luận; Bước 4: Kết luận, nhận định).
                     - Cột 2: Hoạt động cụ thể của Giáo viên và Học sinh (Mô tả chi tiết hành động tương tác của GV và HS. KHÔNG viết lời thoại dài như kịch bản, không dùng ký hiệu "GV:", "HS:". Tập trung vào hành động thực tế).

                QUY TẮC ĐỊNH DẠNG VÀ BIÊN SOẠN KHẮC KHÈO (VI PHẠM SẼ LÀM HỎNG FILE WORD):
                1. KÝ TỰ IN ĐẬM: Tất cả các tiêu đề đề mục lớn và nhỏ (ví dụ: **I. Mục tiêu**, **1. Kiến thức**, **a) Mục tiêu**, **Bước 1: Chuyển giao nhiệm vụ**) bắt buộc phải dùng cú pháp markdown cặp hai dấu sao để khi chuyển sang Word sẽ in đậm chuẩn xác.
                2. CÔNG THỨC TOÁN HỌC / VẬT LÍ: Sử dụng định dạng LaTeX chuẩn trong ký hiệu $...$ cho công thức nằm trong dòng (Inline) hoặc $$...$$ cho công thức nằm riêng một dòng độc lập (Block). Ví dụ: $p = m \\cdot v$, $s = v_0 \\cdot t + \\frac{{1}}{{2}}at^2$, $p_1 + p_2 = p$.
                3. TUYỆT ĐỐI KHÔNG DÙNG LATEX cho chữ viết thông thường, văn bản, tên hình (ví dụ: Hình 1), tên điểm (ví dụ: điểm A, điểm B), đơn vị đo đơn giản (ví dụ: m, s, kg, N, m/s). Chỉ dùng LaTeX cho các biểu thức toán học và phương trình vật lí phức tạp.
                4. KHÔNG DÙNG DẤU BA CHẤM (...) để bỏ lửng nội dung, viết tắt hay lười giải bài tập. Tất cả câu hỏi, phiếu học tập đề ra đều phải có đáp án chi tiết và sản phẩm mẫu trọn vẹn của học sinh tại mục c).
                5. RÀ SOÁT: Hãy tự đóng vai chuyên gia thẩm định rà soát lại toàn bộ hệ thống kiến thức vật lí, câu hỏi và đáp án để đảm bảo tính khoa học, chuẩn xác trước khi hoàn thành xuất văn bản.
                """
                
                response = model.generate_content(prompt)
                
                st.success("🎉 Đã thiết kế giáo án hoàn thành! Bạn có thể xem và copy nội dung bên dưới:")
                
                # Hiển thị trực tiếp trên giao diện trang web
                st.markdown(response.text)
                
                st.write("---")
                st.info("💡 Mẹo xuất file Word sạch: Hãy bôi đen toàn bộ nội dung giáo án ở trên, nhấn chuột phải chọn Sao chép (Copy), sau đó mở một file Microsoft Word trống trên máy tính của bạn ra và dán (Paste) vào. Các mục in đậm, bảng biểu chia cột và công thức toán học sẽ tự động được Word nhận diện hoàn hảo theo quy chuẩn văn bản hành chính.")
                
            except Exception as e:
                st.error(f"🔴 Đã xảy ra lỗi hệ thống: {e}. Vui lòng kiểm tra lại API Key hoặc liên hệ hỗ trợ.")
