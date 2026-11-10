# KẾ HOẠCH PHÂN CHIA CÔNG VIỆC DỰ ÁN (MA TRẬN CÂN BẰNG 4 THÀNH VIÊN)
**Dự án:** Day 03 Lab v2 — Research Agent Tool Eval  
**Nguyên tắc cốt lõi:**  
1. **Phủ kín 100% yêu cầu đề bài** (Base, Testing, Demo, Report và toàn bộ mốc Điểm thưởng Bonus).  
2. **Công bằng & Bình đẳng học tập:** 100% thành viên đều được làm trọn vẹn cả 5 mảng: Tinh chỉnh Prompt, Viết Tool mới, Viết Unit Test, Viết Eval Cases và Viết Báo cáo.  
3. **Song song tuyệt đối (Zero-Blocking, Zero-Conflict):** Phân chia theo cơ chế cách ly file (File-level Isolation), không ai phải chờ ai và không bị xung đột Git.

---

## 1. BẢNG PHÂN CHIA TRÁCH NHIỆM TRỌN GÓI (EACH MEMBER END-TO-END)

Mỗi thành viên sở hữu một gói công việc cân bằng tuyệt đối:  
**1 Tool mới + 6-7 Unit Tests + 2-3 Eval Cases + 1 Version Prompt/Hypothesis + 1 Vai trò điều phối hạ tầng + 1 Phần trong REPORT.md**

```text
┌──────────────┬──────────────────┬───────────────────────┬─────────────────┬───────────────────┐
│ Thành viên   │ Tool mới tự viết │ Unit Test (Pytest)    │ Eval Cases      │ Vai trò điều phối │
├──────────────┼──────────────────┼───────────────────────┼─────────────────┼───────────────────┤
│ TV1 (Lead)   │ Wikipedia Search │ Clarify, Format, T1   │ 2-3 cases (T1)  │ Eval & Git Lead   │
│ TV2          │ Weather API      │ Send, Lookup, T2      │ 2-3 cases (T2)  │ API & Telegram    │
│ TV3          │ Calculator/Math  │ Fetch, Timeline, T3   │ 2-3 cases (T3)  │ QA & Pytest Lead  │
│ TV4          │ DuckDuckGo News  │ Social, Policy, T4    │ 2-3 cases (T4)  │ UI & Demo Lead    │
└──────────────┴──────────────────┴───────────────────────┴─────────────────┴───────────────────┘
```

---

### 👤 THÀNH VIÊN 1: Trưởng nhóm / Điều phối Benchmark & Git
* **Tool mới tự viết (Tool 1):** `wikipedia` (Tra cứu tóm tắt Wikipedia API cho bài toán tra cứu thực thể).
  - Tạo thư mục: `starter_v0/tools/wikipedia/` gồm `tool.py` và `TOOL.md`.
  - Đăng ký hàm trong `tools/__init__.py` và khai báo schema trong `tools.yaml`.
* **Phần Unit Test (`tests/test_member1.py`):**
  - Viết 3 unit tests cho tool `wikipedia` (happy path, entity rỗng, lỗi HTTP).
  - Hoàn thành các stub test có sẵn: `test_clarify_*` (1 test) và `test_format_*` (3 tests).
* **Phần Eval Cases (`eval_group.json`):**
  - Viết 2–3 test cases (kiểm tra model route đúng sang `wikipedia` khi hỏi khái niệm/tiểu sử).
* **Vòng lặp Prompt & Benchmark:**
  - Setup môi trường ban đầu, chạy lệnh Preflight.
  - Chạy **Baseline `v0`**, đọc log `runs/v0_*.json`, phân tích các case lỗi.
  - Chủ trì vòng **`v1`**: Xóa anti-pattern (đoán mò, ép 1 bước), bổ sung rule routing cơ bản.
* **Báo cáo `REPORT.md`:**
  - Viết mục **B1** (Version Evidence table v0–v3) và **B2** (Failure Analysis).

---

### 👤 THÀNH VIÊN 2: Chuyên viên Tích hợp API & Action Tool (Telegram)
* **Tool mới tự viết (Tool 2):** `weather` (Lấy thông tin thời tiết thực tế qua Open-Meteo API, không cần key).
  - Tạo thư mục: `starter_v0/tools/weather/` gồm `tool.py` và `TOOL.md`.
  - Đăng ký hàm trong `tools/__init__.py` và khai báo schema trong `tools.yaml`.
* **Phần Unit Test (`tests/test_member2.py`):**
  - Viết 3 unit tests cho tool `weather` (happy path, tọa độ/địa danh sai, lỗi API).
  - Hoàn thành các stub test có sẵn: `test_send_*` (2 tests: guardrail confirm) và `test_lookup_*` (1 test).
* **Phần Eval Cases (`eval_group.json`):**
  - Viết 2–3 test cases (kiểm tra routing sang `weather` và kiểm tra guardrail `send` không tự ý gửi).
* **Vòng lặp Prompt & Benchmark:**
  - Cấu hình Telegram Bot qua `@BotFather`, lấy Token & Chat ID để kích hoạt tool `send`.
  - Chủ trì đề xuất giả thuyết cho vòng **`v2`**: Tinh chỉnh ranh giới an toàn cho action tools và mô tả chi tiết *Khi nào dùng / Khi nào KHÔNG dùng* trong `tools.yaml`.
* **Báo cáo `REPORT.md`:**
  - Viết mục **A2** (Bảng tổng hợp tất cả các Tool) và **B5** (Bằng chứng Action tool Send Telegram).

---

### 👤 THÀNH VIÊN 3: Chuyên viên QA & Kiểm chuẩn Hợp đồng (Contract)
* **Tool mới tự viết (Tool 3):** `calculator` (Thực hiện phép tính toán, phân tích số liệu an toàn không dùng eval thô).
  - Tạo thư mục: `starter_v0/tools/calculator/` gồm `tool.py` và `TOOL.md`.
  - Đăng ký hàm trong `tools/__init__.py` và khai báo schema trong `tools.yaml`.
* **Phần Unit Test (`tests/test_member3.py`):**
  - Viết 3 unit tests cho tool `calculator` (phép tính chuẩn, biểu thức chia cho 0 hoặc lỗi cú pháp).
  - Hoàn thành các stub test có sẵn: `test_fetch_*` (2 tests: mapping Firecrawl, truncate 4000 ký tự) và `test_timeline_*` (1 test).
* **Phần Eval Cases (`eval_group.json`):**
  - Viết 2–3 test cases (kiểm tra model route sang `calculator` khi có bài toán tính toán, test multi-turn carryover).
* **Vòng lặp Prompt & Benchmark:**
  - Giữ cho bài test contract [`test_tool_contract.py`](file:///C:/Users/hiepq/VinUni/Day03-Prompt-Engineering-Tool-Calling-Labs-student/starter_v0/tests/test_tool_contract.py) luôn pass 100% khi nhóm thêm tool mới.
  - Chủ trì đề xuất giả thuyết cho vòng **`v3`**: Chuẩn hóa convention tham số (handle không có `@`, topic `news`, timeframe, search_type `Top`|`Latest`).
* **Báo cáo `REPORT.md`:**
  - Viết mục **B5** (Phần Unit Test: kết quả pytest 0 failed 0 skipped, phân tích bug tìm được) và mục **B6** (Reflection).

---

### 👤 THÀNH VIÊN 4: Chuyên viên Fullstack UI, Demo & Báo cáo viên
* **Tool mới tự viết (Tool 4):** `duckduckgo_search` (Tìm kiếm web dự phòng cho Tavily sử dụng duckduckgo API).
  - Tạo thư mục: `starter_v0/tools/duckduckgo_search/` gồm `tool.py` và `TOOL.md`.
  - Đăng ký hàm trong `tools/__init__.py` và khai báo schema trong `tools.yaml`.
* **Phần Unit Test (`tests/test_member4.py`):**
  - Viết 3 unit tests cho tool `duckduckgo_search` (happy path, query rỗng, lỗi kết nối).
  - Hoàn thành các stub test có sẵn: `test_social_search_*` (1 test) và `test_policy_*` (3 tests: security untrusted text).
* **Phần Eval Cases (`eval_group.json`):**
  - Viết 2–3 test cases (kiểm tra out-of-scope như từ chối code Python, giải toán ngoài phạm vi).
* **Dựng UI & Live Demo:**
  - Dựng ứng dụng Streamlit `starter_v0/app.py`: Giao diện chat trực quan, hiển thị Thought / Tool Calls / Tham số / Digest Markdown.
  - Cấu hình Cloudflare Tunnel (`cloudflared tunnel --url http://localhost:8501`) để lấy link public cho lớp dùng thử.
  - Chạy Live Chat ít nhất 3 lượt để tạo file transcript tại `transcripts/*.transcript.json`.
* **Báo cáo `REPORT.md` & Poster:**
  - Hoàn thành **PHẦN A của Report** trước 16:30.
  - Thiết kế Poster trình chiếu 1 trang tại `starter_v0/artifacts/poster.html`.
  - Viết mục **B4** (Live Chat Evidence) và tổng hợp toàn bộ bài nộp hoàn chỉnh.

---

## 2. GIẢI PHÁP CHỐNG XUNG ĐỘT GIT KHI LÀM SONG SONG 100%

1. **Cách ly Unit Test:**  
   Không cùng chỉnh sửa một file `test_tools_todo.py`. Mỗi bạn tạo một file test mang tên mình trong thư mục `tests/`:
   - `tests/test_member1.py`
   - `tests/test_member2.py`
   - `tests/test_member3.py`
   - `tests/test_member4.py`  
   *Lệnh `pytest` sẽ tự động chạy toàn bộ các file này cùng lúc! Khi tổng kết bài, TV3 chỉ cần gom lại vào `test_tools_todo.py` hoặc giữ nguyên đều hợp lệ.*

2. **Cách ly Tool mới:**  
   Mỗi người toàn quyền làm việc trong thư mục riêng của mình dưới `starter_v0/tools/`.

3. **Cách ly Eval Cases:**  
   Mỗi bạn viết các case của mình ra file nháp `data/cases_tvX.json`. Trước khi chạy eval group, TV1 gom lại thành mảng 10 phần tử trong `data/eval_group.json`.

---

## 3. LỘ TRÌNH THỰC HIỆN THEO MỐC THỜI GIAN

| Mốc giờ | TV1 (Lead & Eval) | TV2 (API & Telegram) | TV3 (QA & Contract) | TV4 (UI & Poster) | Điểm Đồng Bộ (Sync Point) |
|---|---|---|---|---|---|
| **09:30 – 10:15** | Cài env, preflight, chạy Baseline **`v0`**, ghi `version_log.csv` | Setup Bot Telegram, viết code Tool `weather` | Giữ contract test xanh, viết code Tool `calculator` | Khởi tạo Streamlit `app.py`, viết code Tool `duckduckgo` | **Sync 1:** Chốt số điểm `v0`, thống nhất 4 tool mới. |
| **10:15 – 11:00** | Xóa anti-pattern, viết prompt **`v1`**, viết Tool `wikipedia` | Viết 3 unit test cho `weather` + test `send`, `lookup` | Viết 3 unit test cho `calculator` + test `fetch`, `timeline` | Viết 3 unit test cho `duckduckgo` + test `social`, `policy` | **Sync 2:** Tích hợp 4 tool vào registry; `pytest` toàn nhóm xanh 100%. |
| **11:00 – 11:45** | Cùng TV2 cập nhật `tools.yaml`, chạy **`v2`** | Viết 2-3 eval cases, hỗ trợ tối ưu `v2` | Viết 2-3 eval cases, đề xuất convention args cho `v3` | Hoàn thiện UI Streamlit, mở Cloudflare Tunnel, viết 2-3 eval cases | **Sync 3:** Ghép đủ 10 cases vào `eval_group.json`. Chạy test group. |
| **11:45 – 12:15** | Chạy **`v3`** trên cả suite `base` và `group` | Kiểm thử tool `send` Telegram trên live chat | Kiểm tra toàn bộ `pytest`: **0 failed, 0 skipped** | Chạy live chat lưu transcript; hoàn thành **Phần A Report + Poster** | **Sync 4 (16:30): SHOWDOWN DEMO** (Show UI live + Poster HTML). |
| **Sau Showdown** | Tổng hợp bảng B1, B2 | Tổng hợp mục B5 | Tổng hợp mục B5, B6 | Hoàn thiện toàn bộ **Phần B REPORT.md** và nộp bài | **Sync 5:** Kiểm tra checklist nộp bài cuối cùng. |

---

## 4. CHIẾN LƯỢC ĐẠT ĐIỂM THƯỞNG TỐI ĐA (BONUS POINTS)

- **Điểm thưởng lớn (Bonus Point):** Nhóm đạt cả 2 điều kiện:
  1. Có UI tương tác Web (Streamlit) kèm link public Cloudflare Tunnel.
  2. Tự viết **4 tool mới** (vượt chỉ tiêu >3 tools của đề bài).
- **Tool hành động an toàn:** Tool `send` có xác nhận `confirmed=True` và có log transcript chứng minh.
- **Bonus Local Model:** TV4 có thể kéo model local qua Ollama (`qwen2.5:7b`) chạy thử nghiệm để lấy thêm dữ liệu điền vào mục B7.

---

## 5. CHECKLIST NGHIỆM THU TRƯỚC KHI NỘP BÀI

- [ ] File `.env` không bị commit lên Git.
- [ ] `artifacts/system_prompt.md` sạch các chỉ dẫn sai, có rule routing rõ ràng.
- [ ] `artifacts/tools.yaml` có mô tả đầy đủ điều kiện dùng/không dùng và schema 4 tool mới.
- [ ] `artifacts/version_log.csv` ghi đủ 4 phiên bản thực nghiệm (`v0`, `v1`, `v2`, `v3`).
- [ ] `data/eval_group.json` có đủ 10 test cases mới (5 single-turn, 5 multi-turn).
- [ ] Có đủ 4 tool mới trong `tools/` kèm `TOOL.md` chuẩn frontmatter.
- [ ] Chạy lệnh `pytest` báo **0 failed, 0 skipped**.
- [ ] Thư mục `transcripts/` có chứa file `*.transcript.json`.
- [ ] File giao diện `starter_v0/app.py` chạy mượt mà.
- [ ] File `artifacts/REPORT.md` hoàn thành đủ Phần A và Phần B.
- [ ] File trình chiếu `artifacts/poster.html` sẵn sàng.
