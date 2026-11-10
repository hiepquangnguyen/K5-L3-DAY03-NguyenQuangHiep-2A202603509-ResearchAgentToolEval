# KẾ HOẠCH CÔNG VIỆC CÒN LẠI CỦA DỰ ÁN
**Dự án:** Day 03 Lab v2 — Research Agent Tool Eval  
**Trạng thái hiện tại:** Đã hoàn thành 100% phần Kỹ thuật cốt lõi (Prompt v3, Benchmark Base & Group đạt 100%, Tool Wikipedia API thật, Pytest 85/85 passed).  
**Mục tiêu tài liệu này:** Liệt kê chi tiết toàn bộ các đầu việc còn lại cần hoàn thiện để phục vụ nộp bài và buổi thuyết trình demo (Team Showdown).  
*(Lưu ý: Danh sách công việc thuần túy, chưa phân chia cụ thể cho thành viên nào).*

---

## 1. TỔNG QUAN HIỆN TRẠNG (NHỮNG GÌ ĐÃ HOÀN THÀNH 100%)

Trước khi triển khai các công việc còn lại, nhóm cần nắm rõ các thành quả kỹ thuật đã hoàn tất và đã được lưu trữ an toàn trên GitHub:
1. **System Prompt (`starter_v0/artifacts/system_prompt.md`):** Đã hoàn thiện phiên bản `v3`, loại bỏ hoàn toàn các lỗi đoán mò, ép 1 bước; bổ sung quy tắc định tuyến cho 11 công cụ; xử lý hội thoại đa lượt dứt khoát và khử hoàn toàn lỗi rò rỉ đề thi (Overfitting).
2. **Bộ Test Group chính thức (`starter_v0/data/eval_group.json`):** Đã chốt và đóng băng 10 test case thử thách nâng cao (5 single-turn, 5 multi-turn) bao phủ đủ các tình huống bẫy: đọc 2 URL song song, điều kiện giả Telegram, từ chối gửi tin, thực thể đa nghĩa Wikipedia.
3. **Dữ liệu thực nghiệm (`starter_v0/runs/` và `version_log.csv`):** Đã lưu vết đầy đủ 6 file log thực tế:
   - `v0` (Baseline Base): 0.80
   - `v1` (Core Routing Base): 1.00
   - `v2` (Thêm Wikipedia Base): 1.00
   - `v2-group` (Group Stress Test): 0.60 (bộc lộ 4 điểm yếu thật)
   - `v3-group` (Group Optimized): 1.00 (khắc phục trọn vẹn 4 điểm yếu)
   - `v3` (Base Re-check): 1.00 (chứng minh không bị hồi quy)
4. **Tool mới Wikipedia (`starter_v0/tools/wikipedia/`):** Code chạy thật với Wikipedia REST API, có tài liệu `TOOL.md`, đăng ký trong `__init__.py` và `tools.yaml`.
5. **Kiểm thử tự động (`pytest`):** Đạt 85/85 passed (0 failed, 0 skipped), đảm bảo hợp đồng Schema và Unit tests chuẩn xác.

---

## 2. DANH SÁCH CHI TIẾT CÁC CÔNG VIỆC CÒN LẠI CẦN LÀM

### HẠNG MỤC 1: CHẠY LIVE CHAT VÀ XUẤT FILE TRANSCRIPT (`chat.py`)
* **Mục tiêu:** Tạo ra file bằng chứng hội thoại thực tế giữa người dùng và Agent tại thư mục `starter_v0/transcripts/*.transcript.json` (bắt buộc phải có trong hồ sơ nộp bài).
* **Công việc cụ thể:**
  1. Chạy lệnh: `python chat.py --provider openrouter --version v3`
  2. Thực hiện tối thiểu 3 lượt chat tương tác thực tế với các tình huống:
     - **Lượt 1 (Tra cứu kiến thức bách khoa):** `"Tra cứu thông tin bách khoa toàn thư Wikipedia về Alan Turing giúp mình."` (Kiểm tra agent kích hoạt tool `wikipedia`).
     - **Lượt 2 (Xử lý thiếu thông tin):** User nhập: `"Tóm tắt các bài viết gần đây giúp mình"` ➔ Agent phải hỏi lại của ai (`clarify`) ➔ User nhập tiếp: `"Của tài khoản sama nhé"` ➔ Agent lấy tweet (`timeline`).
     - **Lượt 3 (Kiểm tra bảo vệ an toàn Telegram):** User nhập: `"Đăng bản tin này lên kênh Telegram giúp mình"` ➔ Agent phải kích hoạt `clarify(response_type="yes_no")` để xin xác nhận trước khi gửi.
  3. Gõ `/exit` để kết thúc phiên chat.
* **Kết quả cần đạt:** 
  - Xuất hiện file `starter_v0/transcripts/v3_openrouter_<timestamp>.transcript.json`.
  - Trích xuất các lượt chat này để điền vào mục **B4** của Báo cáo.

---

### HẠNG MỤC 2: HOÀN THIỆN FILE BÁO CÁO CHÍNH THỨC (`starter_v0/artifacts/REPORT.md`)
* **Mục tiêu:** Điền hoàn chỉnh 100% nội dung báo cáo nộp bài (gồm 2 phần: Phần A phục vụ Demo/Showdown và Phần B phục vụ chấm điểm kỹ thuật).
* **Nội dung cụ thể cần điền:**
  1. **Thông tin đầu trang:** Tên nhóm, danh sách thành viên, Provider/Model sử dụng (`openrouter / openai/gpt-4o-mini`).
  2. **PHẦN A — Giới thiệu Agent (Hoàn thành để phục vụ Demo):**
     - **Mục A1 (Agent này làm được gì):** Viết mô tả ngắn gọn 2–3 câu về năng lực tổng hợp của Agent (tìm tin tức web, lấy tweet theo tài khoản/chủ đề, đọc URL, tra cứu bách khoa Wikipedia, định dạng bản tin và bảo vệ an toàn gửi Telegram).
     - **Mục A1 (Link dùng thử):** Dán link public Web UI (từ Cloudflare Tunnel hoặc link local).
     - **Mục A2 (Bảng danh mục Tool):** Liệt kê đầy đủ 11 công cụ hiện có trong hệ thống (`clarify`, `timeline`, `social_search`, `lookup`, `fetch`, `format`, `send`, `policy`, `papers`, `paper_text`, `wikipedia`), nêu rõ chức năng từng tool và đánh dấu tool mới nhóm tự thêm (`wikipedia`).
     - **Mục A3 (Câu hỏi mẫu để thử):** Soạn sẵn 5 câu hỏi mẫu ấn tượng nhất để các nhóm khác có thể copy-paste dùng thử ngay trên giao diện web.
  3. **PHẦN B — Chi tiết & Bằng chứng kỹ thuật (Phục vụ nộp bài):**
     - **Mục B1 (Version Evidence):** Điền bảng tiến trình 6 phiên bản từ file `version_log.csv` (`v0`, `v1`, `v2`, `v2-group`, `v3-group`, `v3`).
     - **Mục B2 (Failure Analysis):** Lập bảng phân tích lỗi thực tế:
       - Phân tích 4 lỗi của `v0` (đoán mò handle `sama`, bịa URL `fetch`, tự ý gọi `send`, không từ chối bài toán tích phân).
       - Phân tích 4 lỗi của `v2-group` (thiếu timeframe year, gọi tool thừa khi user từ chối đăng tin, trích xuất từ khóa thừa trong `lookup`).
     - **Mục B3 (Team Eval Cases):** Lập bảng chi tiết 10 test cases trong `eval_group.json` (mô tả mục đích kiểm thử của từng case, tool mong đợi, kết quả thực tế đạt PASS 100%).
     - **Mục B4 (Live Chat Evidence):** Trích xuất bảng đối thoại thực tế từ file transcript đã chạy ở Hạng mục 1.
     - **Mục B5 (Bonus Evidence):** Trình bày bằng chứng về các điểm thưởng:
       - Giao diện Web UI Streamlit tương tác trực quan.
       - Bộ kiểm thử Unit Test đạt 85/85 passed (0 failed, 0 skipped), phân tích trường hợp lỗi mà unit test bắt được nhưng eval không bắt được (ví dụ: mock kiểm tra tham số request gửi đi).
       - Cơ chế bảo vệ xác nhận an toàn (Confirmation Guardrail) của tool `send` Telegram.
     - **Mục B6 (Reflection):** Trả lời 4 câu hỏi suy ngẫm kỹ thuật:
       - Sửa lỗi nào thuộc về `system_prompt.md`?
       - Sửa lỗi nào thuộc về `tools.yaml`?
       - Lỗi nào cần con người xem xét thủ công thay vì chấm tự động?
       - Nhóm sẽ cải tiến điều gì tiếp theo nếu có thêm thời gian?

---

### HẠNG MỤC 3: THIẾT KẾ POSTER TRÌNH CHIẾU SHOWDOWN (`starter_v0/artifacts/poster.html`)
* **Mục tiêu:** Tạo 1 trang HTML đơn lẻ, giao diện đồ họa đẹp mắt, trực quan để nhóm trình chiếu trên máy chiếu hoặc màn hình trong buổi Team Showdown (16:30).
* **Nội dung cần có trên Poster:**
  1. Tiêu đề nổi bật: Tên Agent, Slogan, Tên nhóm và thành viên.
  2. Khối tính năng cốt lõi: 11 công cụ được trực quan hóa theo nhóm (Web Research, X/Twitter, Wikipedia, Action Tool Telegram).
  3. Khối kết quả Benchmark ấn tượng:
     - Biểu đồ/bảng so sánh bước nhảy vọt: Base Eval (80% ➔ 100%), Group Eval (60% ➔ 100%).
     - Kết quả Pytest: 85/85 Tests Passed (100% xanh).
  4. Khối câu hỏi mẫu (Live Demo Prompts): 4–5 câu hỏi gợi ý để khán giả thử nghiệm ngay.
  5. Khu vực hiển thị Link truy cập hoặc mã QR kết nối vào giao diện Web Demo.

---

### HẠNG MỤC 4: TRIỂN KHAI VÀ VẬN HÀNH WEB UI STREAMLIT (`starter_v0/app.py`)
* **Mục tiêu:** Chạy ứng dụng web chat tương tác trực tiếp để cả lớp và giảng viên có thể dùng thử Agent.
* **Công việc cụ thể:**
  1. Khởi chạy ứng dụng Streamlit trên máy cục bộ:
     ```powershell
     cd starter_v0
     streamlit run app.py
     ```
  2. Mở cổng Public ra Internet bằng Cloudflare Tunnel (không cần đăng ký tài khoản, có link dùng ngay):
     ```powershell
     cloudflared tunnel --url http://localhost:8501
     ```
  3. Lấy URL public có dạng `https://<random-id>.trycloudflare.com` dán vào mục A1 của file `REPORT.md` và đưa lên Poster.
  4. Kiểm tra tính năng chuyển đổi phiên bản trên UI: Đảm bảo có thể chọn giữa `v0` (để thấy agent đoán mò/lỗi) và `v2/v3` (để thấy agent xử lý thông minh, hiển thị tool calls rõ ràng).

---

### HẠNG MỤC 5: CÁC ĐẦU VIỆC ĐIỂM THƯỞNG BONUS (TÙY CHỌN NÂNG CAO)
*(Thực hiện nếu nhóm muốn tối đa hóa điểm số và còn dư thời gian)*:

1. **Săn Điểm Thưởng Lớn (> 3 Tools mới + Web UI):**
   - Đề bài quy định: Nhóm nào có UI VÀ tự viết hơn 3 tool mới sẽ nhận điểm thưởng tối đa. Hiện nhóm đã có UI và 1 tool mới (`wikipedia`).
   - Có thể bổ sung thêm 3 tool mới:
     - Tool 2: `weather` (Lấy thời tiết qua Open-Meteo API, không cần key).
     - Tool 3: `calculator` (Hàm tính toán an toàn cho phân tích số liệu).
     - Tool 4: `duckduckgo_search` (Tìm kiếm web dự phòng).
   - Mỗi tool cần: thư mục riêng dưới `tools/`, file `tool.py`, file `TOOL.md`, đăng ký trong `__init__.py` và `tools.yaml`, kèm ≥ 3 unit test trong `tests/`.
2. **Small Local Model Challenge (Chạy mô hình nhỏ offline qua Ollama):**
   - Cài đặt Ollama, kéo model nhỏ (ví dụ: `qwen2.5:7b` hoặc `llama3.2:3b`).
   - Chạy lệnh benchmark local:
     ```powershell
     python run_eval.py --provider ollama --model qwen2.5:7b --version v3-qwen7b --suite base --eval-cases data/eval_base.json
     ```
   - Đo khoảng cách điểm số giữa Cloud vs Local Model, phân loại các lỗi đặc thù của model nhỏ (JSON hỏng, gọi lặp, bịa tên tool) và điền vào mục **B7** của `REPORT.md`.
3. **Bộ Đánh Giá Mở Rộng (`eval_research_extension.json`):**
   - Chạy benchmark đo lường công cụ tra cứu arXiv (`papers`, `paper_text`) và quy chế nội bộ (`policy`):
     ```powershell
     python run_eval.py --provider openrouter --version v3 --suite extension --eval-cases data/eval_research_extension.json
     ```

---

## 3. DANH MỤC HỒ SƠ NGHIỆM THU CUỐI CÙNG TRƯỚC KHI NỘP

Khi đến giờ nộp bài, nhóm cần rà soát lại đảm bảo repo có đầy đủ các file sau:
- [ ] `starter_v0/artifacts/system_prompt.md` (bản hoàn thiện v3).
- [ ] `starter_v0/artifacts/tools.yaml` (khai báo đủ schema 11 tool).
- [ ] `starter_v0/artifacts/version_log.csv` (ghi đủ 6 lượt chạy thực tế).
- [ ] `starter_v0/artifacts/REPORT.md` (hoàn thiện đủ cả Phần A và Phần B).
- [ ] `starter_v0/artifacts/poster.html` (trang poster trình chiếu).
- [ ] `starter_v0/data/eval_group.json` (bộ 10 case thử thách nâng cao).
- [ ] `starter_v0/runs/*.json` (chứa các file log thực tế của v0, v1, v2, v3).
- [ ] `starter_v0/transcripts/*.transcript.json` (chứa file lịch sử chat thực tế).
- [ ] `starter_v0/app.py` (chạy giao diện web mượt mà).
- [ ] File `.env` **KHÔNG ĐƯỢC COMMIT** lên GitHub.

---

## 4. QUY TẮC PHỐI HỢP TRÊN GIT & GITHUB (BẮT BUỘC ĐỌC KỸ TRƯỚC KHI BẮT ĐẦU)

Để tránh xung đột code (Merge Conflict) và bảo vệ dữ liệu thực nghiệm đã đạt điểm tuyệt đối:

### 1. Nguyên tắc "Bất khả xâm phạm" với Dữ liệu Benchmark:
* **TUYỆT ĐỐI KHÔNG tự ý chạy lại lệnh `run_eval.py` cho các version `v0`, `v1`, `v2`, `v3`** trên bộ `base` hoặc `group`. Toàn bộ 6 file log trong `runs/` và bảng kết quả trong `version_log.csv` đã được Lead chạy chuẩn xác (100%) và đóng băng. Việc chạy lại sẽ sinh ra file log rác và làm lệch timestamp/hash.
* **KHÔNG chỉnh sửa** file `data/eval_base.json` và `data/eval_group.json`.

### 2. Phân công độc lập theo từng File (File Ownership):
Ai nhận phần nào thì **chỉ chỉnh sửa đúng file của phần đó** để không bao giờ bị đụng nhau:
* Thành viên làm **Poster**: Chỉ làm việc trên file `starter_v0/artifacts/poster.html`.
* Thành viên làm **Báo cáo (Report)**: Chỉ chỉnh sửa file `starter_v0/artifacts/REPORT.md`.
* Thành viên làm **Transcript**: Chỉ tạo file trong thư mục `starter_v0/transcripts/`.
* Thành viên làm **Bonus (Tool mới/Local Model)**: Nên tạo branch riêng (ví dụ: `git checkout -b feature/bonus-tools`) để phát triển độc lập, không làm ảnh hưởng nhánh `main`.

### 3. Quy trình Pull / Push chuẩn để không bị đè code:
Mỗi khi bắt đầu làm và trước khi đẩy code lên, thành viên cần tuân thủ 3 bước:
1. **Trước khi bắt đầu làm:** Luôn cập nhật code mới nhất từ GitHub về máy:
   ```powershell
   git pull origin main
   ```
2. **Sau khi làm xong, chuẩn bị đẩy code:**
   ```powershell
   git add <tên_file_bạn_vừa_sửa>
   git commit -m "mô tả ngắn gọn việc bạn vừa làm"
   ```
3. **Kéo code mới nhất về trước khi Push (Tránh xung đột):**
   ```powershell
   git pull --rebase origin main
   git push origin main
   ```
   *(Lệnh `git pull --rebase` sẽ tự động đưa các commit mới nhất của nhóm lên đầu rồi mới xếp commit của bạn vào sau, giúp lịch sử Git luôn thẳng hàng và không bị sinh ra các commit merge rác).*

### 4. An toàn thông tin:
* Tuyệt đối **KHÔNG commit file `.env`** hoặc paste API Key cá nhân vào bất kỳ file tài liệu/mã nguồn nào (`.gitignore` đã cấu hình chặn file `.env`, hãy giữ nguyên như vậy).
