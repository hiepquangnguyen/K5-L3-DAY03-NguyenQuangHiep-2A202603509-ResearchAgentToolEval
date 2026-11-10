---
name: wikipedia
track: bonus
kind: live_api
provider: Wikipedia REST API
requires_env: []
inputs: [query]
outputs: [title, summary, url]
side_effect: false
---

# Wikipedia Search Tool

Công cụ tra cứu bách khoa toàn thư, định nghĩa khái niệm khoa học, lịch sử, hoặc tiểu sử người nổi tiếng từ Wikipedia.

- **Khi nào dùng:** Khi người dùng muốn tìm hiểu khái niệm, kiến thức bách khoa, tiểu sử nhân vật lịch sử, khoa học.
- **Khi nào KHÔNG dùng:** Không dùng cho tin tức thời sự hôm nay (dùng `lookup`), không dùng tìm tweet (dùng `timeline`/`social_search`).