import streamlit as st
import google.generativeai as genai

# Cấu hình giao diện ứng dụng rộng rãi, chuyên nghiệp
st.set_page_config(page_title="Giáo Án Vật Lí 5512 & NLS", page_icon="⚛️", layout="wide")

st.markdown("<h2 style='text-align: center; color: #1E88E5;'>⚛️ ỨNG DỤNG SOẠN GIÁO ÁN VẬT LÍ THEO MẪU CHUẨN ĐÓN ĐẦU (CV 5512 & TT 02/2025)</h2>", unsafe_allow_html=True)
st.write("---")

# Thanh cấu hình và lựa chọn bên trái
st.sidebar.header("🔑 Cấu hình hệ thống")
api_key = st.sidebar.text_input("Nhập Gemini API Key của bạn:", type="password", help="Lấy mã này từ Google AI Studio")

st.sidebar.write("---")
st.sidebar.header("🧭 PHẦN CẦN SOẠN (CUỐN CHIẾU)")
phan_soan = st.sidebar.radio(
    "Chọn phân đoạn soạn để AI tập trung viết sâu nhất:",
    [
        "1. Khung đầu + Mục I (Mục tiêu) + Mục II (Thiết bị)",
        "2. Mục III - Hoạt động 1: Mở đầu / Xác định vấn đề",
        "3. Mục III - Hoạt động 2: Hình thành kiến thức mới",
        "4. Mục III - Hoạt động 3: Luyện tập",
        "5. Mục III - Hoạt động 4: Vận dụng",
        "6. Mục IV: Kiểm tra, đánh giá (Kèm Rubric tiêu chí)"
    ]
)

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

# Khung nhập thông tin bài học Vật lí ở giữa
st.subheader("📝 Thông tin chung kế hoạch bài dạy")
col1, col2 = st.columns(2)

with col1:
    truong = st.text_input("Tên trường / Cơ sở giáo dục:", placeholder="Ví dụ: THPT Nguyễn Du...")
    giao_vien = st.text_input("Họ và tên giáo viên:", placeholder="Ví dụ: Nguyễn Văn A...")
    khoi_lop = st.selectbox("Khối lớp (Môn Vật lí - Sách Kết nối tri thức):", ["Vật lí 10", "Vật lí 11", "Vật lí 12"])

with col2:
    to_chuyen_mon = st.text_input("Tổ / Nhóm chuyên môn:", placeholder="Ví dụ: Tổ Vật lí - Công nghệ...")
    ten_bai = st.text_input("Tên bài dạy chính xác:", placeholder="Ví dụ: Động lượng và định luật bảo toàn động lượng...")
    so_tiet = st.number_input("Thời gian thực hiện (Số tiết):", min_value=1, max_value=6, value=2)

muc_tieu_rieng = st.text_area("Yêu cầu bổ sung hoặc công cụ số muốn sử dụng (Nếu có):", 
                              placeholder="Ví dụ: Sử dụng thí nghiệm ảo PhET, sử dụng máy tính cầm tay, điện thoại thông minh...")

if st.button(f"🚀 Kích hoạt AI soạn: {phan_soan}", type="primary", use_container_width=True):
    if not api_key:
        st.error("❌ Vui lòng nhập API Key ở thanh menu bên trái trước!")
    elif not ten_bai:
        st.warning("⚠️ Vui lòng nhập Tên bài dạy chính xác.")
    else:
        with st.spinner(f"⏳ Trợ lý AI đang áp dụng mẫu chuẩn 5512 cải tiến để soạn {phan_soan}..."):
            try:
                genai.configure(api_key=api_key)
                # Cấu hình tối ưu độ chính xác và chiều dài văn bản
                model_config = genai.GenerationConfig(max_output_tokens=8192, temperature=0.3)
                model = genai.GenerativeModel('gemini-2.5-flash', generation_config=model_config)
                
                tong_thoi_gian = so_tiet * 45
                
                # Khung promt nền tảng thiết lập luật MathType và phân bổ thời gian
                prompt_base = f"""
                Bạn là một chuyên gia giáo dục Vật lí xuất sắc cốt cán. Hãy thiết kế một phần nội dung của kế hoạch bài dạy (Giáo án) bám sát chương trình SGK KẾT NỐI TRI THỨC môn Vật lí.
                - Bài dạy: {ten_bai} | Khối: {khoi_lop} | Số tiết: {so_tiet} tiết (Tổng cộng {tong_thoi_gian} phút).
                - Trường: {truong} | Giáo viên: {giao_vien} | Tổ: {to_chuyen_mon}
                - Định hướng lồng ghép Năng lực số: {mien_nls} bám sát Thông tư 02/2025/TT-BGDĐT.
                - Yêu cầu riêng: {muc_tieu_rieng}

                QUY TẮC PHÂN BỔ THỜI GIAN THEO SỐ TIẾT:
                Tổng thời gian bài học là {tong_thoi_gian} phút. Phải phân bổ phân chia thời lượng thực hiện (số phút) chi tiết cho hoạt động hoặc nội dung đang viết ngay tại tiêu đề mục.

                QUY TẮC ĐỊNH DẠNG CÔNG THỨC MATHTYPE TRÊN WORD:
                Tất cả các công thức, biểu thức, phương trình Vật lí hoặc Toán học bắt buộc phải viết dưới dạng ký hiệu LaTeX nằm trong cặp dấu $...$ (nếu nằm trên cùng dòng chữ) hoặc $$...$$ (nếu đứng độc lập riêng một dòng). Ví dụ: $p = m \\cdot v$, $A = F \\cdot s \\cdot \\cos\\alpha$, $s = v_0 \\cdot t + \\frac{{1}}{{2}}at^2$. 
                TUYỆT ĐỐI KHÔNG DÙNG LATEX cho chữ viết thông thường, văn bản tiếng Việt, tên hình (ví dụ: Hình 1), tên điểm (ví dụ: điểm A, điểm B), đơn vị đo đơn giản (m, s, kg, N, m/s). Tiêu đề mục phải bọc trong cặp hai dấu sao để IN ĐẬM.
                """

                # Các kịch bản prompt động theo mẫu file giáo án của bạn gửi
                if "1. Khung đầu" in phan_soan:
                    prompt_loai = f"""
                    Nhiệm vụ: Hãy soạn hoàn chỉnh phần đầu giáo án hành chính gồm Trường, Tổ, Giáo viên, Tên bài, Môn, Lớp, Số tiết, Đối tượng học sinh, Phân chia thời lượng thực hiện chi tiết cho từng tiết (Mỗi tiết 45 phút) bám sát thời lượng {so_tiet} tiết. Sau đó soạn tiếp:
                    **I. MỤC TIÊU**
                      1. Kiến thức: Nêu cụ thể các yêu cầu cần đạt về kiến thức cốt lõi Vật lí dựa theo SGK Kết nối tri thức.
                      2. Năng lực: Ghi rõ Năng lực đặc thù vật lí, Năng lực chung (Tự chủ và tự học, Giao tiếp và hợp tác). Đặc biệt thiết lập riêng một mục **Năng lực số**: Gọi tên chính xác tên Miền và Năng lực thành phần tương ứng của {mien_nls} (Ví dụ: Miền V, Năng lực thành phần 5.2...). Mô tả rõ học sinh biết sử dụng công cụ số gì để giải quyết vấn đề bài học Vật lí này.
                      3. Phẩm chất: Nêu cụ thể biểu hiện phẩm chất Chăm chỉ, Trung thực, Trách nhiệm gắn với hoạt động bài học.
                    **II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU**
                      Tách rõ thành 3 gạch đầu dòng lớn:
                      - Thiết bị dạy học: (Máy chiếu, màn chiếu, thiết bị thí nghiệm...).
                      - Học liệu: Ghi rõ Sách giáo khoa Vật lí khối {khoi_lop} (Kết nối tri thức).
                      - Công cụ số: Liệt kê rõ tên phần mềm, máy tính, mô hình thí nghiệm ảo muốn áp dụng và nêu rõ *Mục đích sử dụng* công cụ số này để giải quyết việc gì.
                    """
                elif "6. Mục IV" in phan_soan:
                    prompt_loai = """
                    Nhiệm vụ: Hãy soạn hoàn chỉnh mục **IV. KIỂM TRA, ĐÁNH GIÁ** bám sát nội dung bài dạy Vật lí trên bao gồm:
                    - Hình thức đánh giá: Nêu rõ phương pháp đánh giá tương ứng cho từng Hoạt động 1, 2, 3, 4 (Ví dụ: đánh giá qua câu trả lời, qua chấm tập, qua quan sát thao tác máy tính...).
                    - BẢNG TIÊU CHÍ (RUBRIC) ĐÁNH GIÁ NĂNG LỰC SỐ VÀ GIẢI QUYẾT VẤN ĐỀ VẬT LÍ: Hãy thiết kế một bảng tiêu chí đánh giá chia làm các cột: Tiêu chí, Mức 4, Mức 3, Mức 2, Mức 1 bằng định dạng bảng Markdown Table. Các tiêu chí phải xoay quanh: Nhận diện và thiết lập công thức vật lí, Sử dụng công cụ số hỗ trợ, Trình bày lời giải bài tập.
                    """
                else:
                    # Các hoạt động tiến trình dạy học mục III
                    prompt_loai = f"""
                    Nhiệm vụ: Hãy soạn hoàn chỉnh duy nhất mục **III. TIẾN TRÌNH DẠY HỌC** cho hoạt động: **{phan_soan}**.
                    Yêu cầu bắt buộc viết trọn vẹn đầy đủ 4 mục nhỏ, không viết tắt, không dùng dấu ba chấm:
                      **a) Mục tiêu**: Phù hợp với tính chất của hoạt động này và ghi kèm thời lượng số phút dự kiến.
                      **b) Nội dung**: Nhiệm vụ, câu hỏi hiện tượng Vật lí hoặc phiếu học tập cụ thể giáo viên giao cho học sinh thực hiện.
                      **c) Sản phẩm**: Nêu kết quả học tập kỳ vọng của học sinh một cách tổng quát, gọn gàng, định thức công thức Vật lí chuẩn chỉnh.
                      **d) Tổ chức thực hiện**: 
                      QUY TẮC TUYỆT ĐỐI: KHÔNG ĐƯỢC VẼ BẢNG MARKDOWN TRONG MỤC NÀY. Hãy trình bày Tổ chức thực hiện dưới dạng văn bản cấu trúc in đậm và gạch đầu dòng chi tiết mô tả chuỗi hành động tương tác sư phạm phối hợp nhịp nhàng giữa Giáo viên và Học sinh, ghi rõ cả năng lực số có tích hợp hay không tích hợp tại từng bước. Trình bày chính xác theo biểu mẫu sau:
                      
                      - **Chuyển giao nhiệm vụ**: (Giáo viên trình chiếu, giao lệnh, phát phiếu học tập hay yêu cầu học sinh mở công cụ số/AI. Học sinh quan sát, lắng nghe và tiếp nhận nhiệm vụ).
                      - **Thực hiện nhiệm vụ**: (Học sinh thực hiện tự học, thảo luận cặp đôi hoặc làm việc nhóm để giải quyết hiện tượng Vật lí hay tính toán công thức. Giáo viên đi vòng quanh theo dõi. BẮT BUỘC ghi rõ mục: *Khó khăn thường gặp của học sinh* và *Biện pháp hỗ trợ của giáo viên* là gì).
                      - **Báo cáo, thảo luận**: (Giáo viên gọi đại diện học sinh báo cáo kết quả, giơ sản phẩm hoặc công cụ số. Học sinh nhóm khác lắng nghe, nhận xét, phản biện, thảo luận).
                      - **Kết luận, nhận định**: (Giáo viên tiến hành đánh giá tính đúng đắn, chính xác hóa kiến thức Vật lí, chốt định luật, đóng khung công thức và hướng dẫn học sinh ghi bài vào vở).
                    """

                # Kết hợp câu lệnh và gửi cho mô hình AI
                prompt_final = prompt_base + prompt_loai
                response = model.generate_content(prompt_final)
                
                st.success(f"🎉 Đã soạn xong {phan_soan} theo biểu mẫu mẫu chuẩn thành công!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"🔴 Đã xảy ra lỗi hệ thống: {e}")
