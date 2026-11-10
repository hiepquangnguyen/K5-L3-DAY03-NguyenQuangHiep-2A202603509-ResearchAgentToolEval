import json
from pathlib import Path
import streamlit as st

from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from chat import run_model_tool_loop

st.set_page_config(page_title="Research Agent Demo", page_icon="🤖", layout="wide")

ROOT = Path(__file__).parent
load_lab_env(ROOT)

# 1. Định nghĩa System Prompt và Tools cho từng Version
PROMPT_V0 = """You are a fast, proactive research assistant with access to tools.
The user is busy and hates being asked questions. Whenever something is missing or unclear, do not ask them back — just make a sensible guess and call a tool right away. If a request mentions a tweet or post but doesn't say whose, pick a well-known account like Sam Altman. If you only have a vague reference like "this article", assume a likely URL and read it.
When the user wants to send, post, or publish something, just go ahead and do it so they don't have to wait.
Always finish the request in a single step. Pick one tool and fill in its arguments using your best judgment."""

PROMPT_V2 = (ROOT / "artifacts" / "system_prompt.md").read_text(encoding="utf-8")
PROMPT_V1 = PROMPT_V2.replace("9. **Wikipedia Search (`wikipedia`)**:", "")

tools_all = load_tool_declarations(ROOT / "artifacts" / "tools.yaml")
tools_no_wiki = [t for t in tools_all if t["name"] != "wikipedia"]

VERSION_DATA = {
    "v0 (Baseline - Chưa tối ưu)": {
        "tag": "v0",
        "prompt": PROMPT_V0,
        "tools": to_openai_tools(tools_no_wiki),
        "desc": "⚠️ Hay đoán mò tài khoản, tự ý gửi Telegram, từ chối kém, chưa có Wikipedia."
    },
    "v1 (Tối ưu Prompt)": {
        "tag": "v1",
        "prompt": PROMPT_V1,
        "tools": to_openai_tools(tools_no_wiki),
        "desc": "✅ Đã sửa prompt: Biết gọi clarify khi thiếu thông tin, bảo vệ an toàn Telegram."
    },
    "v2 (Tối ưu + Thêm Tool Wikipedia)": {
        "tag": "v2",
        "prompt": PROMPT_V2,
        "tools": to_openai_tools(tools_all),
        "desc": "🚀 Hoàn chỉnh nhất: Tích hợp thêm Tool mới Wikipedia để tra cứu bách khoa toàn thư."
    }
}

# 2. Sidebar cấu hình
st.sidebar.title("⚙️ Cấu hình Agent")

# CHỌN VERSION Ở ĐÂY
selected_version_name = st.sidebar.selectbox(
    "🎯 Chọn Version muốn trải nghiệm:",
    list(VERSION_DATA.keys()),
    index=2  # Mặc định chọn v2
)
current_cfg = VERSION_DATA[selected_version_name]
st.sidebar.info(current_cfg["desc"])

# Chọn Provider
provider_name = st.sidebar.selectbox("Model Provider:", ["openrouter", "gemini"], index=0)

# Nút xóa lịch sử chat khi muốn thử lại
if st.sidebar.button("🗑️ Xóa lịch sử hội thoại"):
    st.session_state.messages = []
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader("💡 Câu hỏi mẫu để test:")
sample_queries = [
    "Tóm tắt 5 tweet mới nhất giúp mình",
    "Đăng bản tin này lên Telegram giúp mình",
    "Alan Turing là ai theo bách khoa toàn thư Wikipedia?",
    "Tin tức AI hôm nay có gì nổi bật?",
    "Giải giúp mình bài toán tích phân: nguyên hàm của x^2"
]
for q in sample_queries:
    if st.sidebar.button(q, key=f"btn_{q}"):
        st.session_state["preset_input"] = q

# 3. Khu vực Chat chính
st.title("🤖 AI Research Agent — Interactive Demo")
st.caption(f"Đang tương tác với: **{selected_version_name}** | Provider: `{provider_name}`")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lịch sử chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "tool_events" in msg and msg["tool_events"]:
            with st.expander("🛠️ Chi tiết Tool Calls được kích hoạt:", expanded=False):
                for ev in msg["tool_events"]:
                    st.code(f"{ev.get('tool')}({json.dumps(ev.get('args', {}), ensure_ascii=False)})", language="python")
                st.json(msg["tool_events"])

# Nhận câu hỏi
user_input = st.chat_input("Nhập câu hỏi của bạn...")
if "preset_input" in st.session_state:
    user_input = st.session_state.pop("preset_input")

if user_input:
    # 1. Thêm câu hỏi user vào UI
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Xây dựng context hội thoại
    working_messages = [{"role": "system", "content": current_cfg["prompt"]}]
    for m in st.session_state.messages:
        working_messages.append({"role": m["role"], "content": m["content"]})

    # 3. Gọi Agent
    with st.chat_message("assistant"):
        with st.spinner(f"Agent ({current_cfg['tag']}) đang xử lý..."):
            try:
                provider = make_provider(provider_name)
                res = run_model_tool_loop(
                    provider=provider,
                    messages=working_messages,
                    tools=current_cfg["tools"],
                    model=None,
                    max_tool_rounds=3
                )
                
                reply_text = res.get("assistant_text", "")
                tool_events = res.get("tool_events", [])

                if tool_events:
                    with st.expander("🛠️ Chi tiết Tool Calls được kích hoạt:", expanded=True):
                        for ev in tool_events:
                            st.code(f"{ev.get('tool')}({json.dumps(ev.get('args', {}), ensure_ascii=False)})", language="python")
                        st.json(tool_events)

                st.markdown(reply_text)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply_text,
                    "tool_events": tool_events
                })

            except Exception as e:
                st.error(f"Lỗi: {e}")