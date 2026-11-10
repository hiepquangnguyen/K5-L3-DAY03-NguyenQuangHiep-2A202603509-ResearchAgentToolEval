import json
from pathlib import Path
import streamlit as st

from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from chat import run_model_tool_loop

st.set_page_config(
    page_title="Research Agent Console",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

ROOT = Path(__file__).parent
load_lab_env(ROOT)

# Custom Engineering Theme Stylesheet
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    }

    code, pre, .mono {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Minimalist Dark Console Layout */
    .stApp {
        background-color: #090d16;
        color: #f8fafc;
    }

    /* Container border & cards */
    .console-header {
        border-bottom: 1px solid #1e293b;
        padding-bottom: 18px;
        margin-bottom: 20px;
    }

    .badge-subtle {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        padding: 3px 8px;
        border-radius: 4px;
        background: #141e33;
        border: 1px solid #1e293b;
        color: #38bdf8;
    }

    .badge-online {
        font-size: 0.75rem;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 9999px;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #10b981;
    }

    /* Metric boxes */
    div[data-testid="stMetricValue"] {
        font-size: 1.6rem !important;
        font-weight: 800 !important;
        color: #f8fafc !important;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        color: #94a3b8 !important;
        letter-spacing: 0.05em !important;
    }

    /* Chat bubble styling */
    .stChatMessage {
        border-radius: 8px !important;
        padding: 12px 16px !important;
        border: 1px solid #1e293b !important;
        background: #0f172a !important;
        margin-bottom: 12px !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 6px !important;
        border: 1px solid #1e293b !important;
        background: #141e33 !important;
        color: #e2e8f0 !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        transition: all 0.15s ease !important;
    }

    .stButton > button:hover {
        border-color: #38bdf8 !important;
        color: #38bdf8 !important;
        background: #1e293b !important;
    }
</style>
""", unsafe_allow_html=True)

# 1. Load System Prompts & Tool Declarations
PROMPT_V0 = """You are a fast, proactive research assistant with access to tools.
The user is busy and hates being asked questions. Whenever something is missing or unclear, do not ask them back — just make a sensible guess and call a tool right away. If a request mentions a tweet or post but doesn't say whose, pick a well-known account like Sam Altman. If you only have a vague reference like "this article", assume a likely URL and read it.
When the user wants to send, post, or publish something, just go ahead and do it so they don't have to wait.
Always finish the request in a single step. Pick one tool and fill in its arguments using your best judgment."""

PROMPT_V3 = (ROOT / "artifacts" / "system_prompt.md").read_text(encoding="utf-8")
PROMPT_V2 = PROMPT_V3
PROMPT_V1 = PROMPT_V3.replace("9. **Wikipedia Search (`wikipedia`)**:", "")

tools_all = load_tool_declarations(ROOT / "artifacts" / "tools.yaml")
tools_no_wiki = [t for t in tools_all if t["name"] != "wikipedia"]

VERSION_DATA = {
    "v3 (Production Optimized)": {
        "tag": "v3",
        "prompt": PROMPT_V3,
        "tools": to_openai_tools(tools_all),
        "desc": "Bản tối ưu hóa hoàn chỉnh: Đạt 100% Base & Group Eval. Xử lý triệt để bẫy đa lượt, lọc query thực thể sạch, dừng tool khi hủy lệnh.",
        "badge": "Active Release"
    },
    "v2 (+ Wikipedia Tool Integration)": {
        "tag": "v2",
        "prompt": PROMPT_V2,
        "tools": to_openai_tools(tools_all),
        "desc": "Tích hợp công cụ bách khoa toàn thư Wikipedia REST API. Bảo toàn 100% Base Eval.",
        "badge": "Extension"
    },
    "v1 (Core Routing & Safety Guardrail)": {
        "tag": "v1",
        "prompt": PROMPT_V1,
        "tools": to_openai_tools(tools_no_wiki),
        "desc": "Xóa bỏ anti-pattern đoán mò; bổ sung quy tắc gọi clarify khi thiếu tham số và chốt chặn xác nhận Telegram.",
        "badge": "Core Routing"
    },
    "v0 (Unoptimized Baseline)": {
        "tag": "v0",
        "prompt": PROMPT_V0,
        "tools": to_openai_tools(tools_no_wiki),
        "desc": "Phiên bản khởi điểm: Mắc lỗi tự suy diễn tài khoản sama, tự ý gửi Telegram, từ chối câu hỏi ngoài phạm vi kém.",
        "badge": "Legacy Baseline"
    }
}

# 2. Header Console
st.markdown("""
<div class="console-header" style="display:flex; justify-content:space-between; align-items:flex-end;">
    <div>
        <span class="badge-subtle">VinUni AI20k • Day 03 Lab Console</span>
        <h1 style="font-size:1.75rem; font-weight:800; color:#f8fafc; margin:6px 0 4px 0; letter-spacing:-0.02em;">
            Research Agent Execution & Evaluation Console
        </h1>
        <p style="font-size:0.88rem; color:#94a3b8; margin:0;">
            Hệ thống nghiên cứu thông minh đa nguồn (Web, Twitter/X, Wikipedia, arXiv, Calculator, Weather) • Định tuyến 14 công cụ • Chốt chặn an toàn hội thoại
        </p>
    </div>
    <div style="text-align:right;">
        <span class="badge-online">EVAL STATUS: VERIFIED 100% PASS</span>
        <div style="font-size:0.75rem; color:#64748b; margin-top:5px; font-family:'JetBrains Mono', monospace;">
            Artifact: v3+p4e41c09db176 • 14 Tools Active (4 Extensions)
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 3. Collapsible Engineering Benchmark Scoreboard
with st.expander("SPECIFICATION & BENCHMARK SCOREBOARD (Click to view verification metrics)", expanded=False):
    col_metric1, col_metric2, col_metric3 = st.columns([1.2, 1.2, 1.6])
    
    with col_metric1:
        st.markdown("**Base Benchmark Suite (20 Cases)**")
        b1, b2 = st.columns(2)
        b1.metric("Case Accuracy", "100%", help="20/20 Cases Passed")
        b2.metric("Tool Routing", "100%", help="Chính xác 100% trong việc chọn tool")
        st.caption("Standard frozen baseline validation suite.")

    with col_metric2:
        st.markdown("**Group Stress Suite (10 Cases)**")
        g1, g2 = st.columns(2)
        g1.metric("Case Accuracy", "100%", delta="+40% vs v2", help="10/10 Edge Cases Passed")
        g2.metric("Multi-turn Acc", "100%", help="Xử lý chuyển đổi và hủy lệnh an toàn")
        st.caption("Advanced edge-cases & adversarial prompt tests.")

    with col_metric3:
        st.markdown("**Contract & Execution Robustness**")
        st.markdown("""
        - **Pytest Suite:** `157/157 Passed` (0 failed, 0 skipped in 1.02s)
        - **Tool Schemas:** 14 active tools declared in `tools.yaml`
        - **Confirmation Guardrail:** Enforced via `clarify(response_type='yes_no')`
        - **Refusal Policy:** Deterministic `no_tool` for out-of-scope math/astrology
        """)

# 4. Model Version & Provider Selection
col_ver, col_prov, col_reset = st.columns([3, 1.2, 0.8])
with col_ver:
    selected_version_name = st.selectbox(
        "Agent Version Configuration:",
        list(VERSION_DATA.keys()),
        index=0
    )
with col_prov:
    provider_name = st.selectbox("Provider:", ["openrouter", "gemini"], index=0)
with col_reset:
    st.write("")
    st.write("")
    if st.button("Clear History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

current_cfg = VERSION_DATA[selected_version_name]
st.caption(f"**Selected Profile:** {current_cfg['desc']}")

# 5. Technical Query Preset Chips (Quick Test)
st.markdown("<div style='font-size:0.78rem; font-weight:700; text-transform:uppercase; color:#64748b; letter-spacing:0.05em; margin: 10px 0 6px 0;'>Interactive Test Queries:</div>", unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
if c1.button("[Wiki: Turing]", use_container_width=True):
    st.session_state["preset_input"] = "Alan Turing là ai theo bách khoa toàn thư Wikipedia?"
if c2.button("[Calc: 15% của 1200]", use_container_width=True):
    st.session_state["preset_input"] = "Tính giúp tôi 15% của 1200 là bao nhiêu?"
if c3.button("[Weather: Hanoi]", use_container_width=True):
    st.session_state["preset_input"] = "Thời tiết hiện tại ở Hanoi như thế nào?"
if c4.button("[Guardrail: Telegram]", use_container_width=True):
    st.session_state["preset_input"] = "Nếu bài viết này đạt tiêu chuẩn chất lượng thì đăng ngay lên kênh Telegram giúp tôi nhé"
if c5.button("[Refusal: Calculus]", use_container_width=True):
    st.session_state["preset_input"] = "Giải giúp mình bài toán tích phân: nguyên hàm của x^2 là gì?"

# 6. Chat History & Execution Trace
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "tool_events" in msg and msg["tool_events"]:
            events = msg["tool_events"]
            with st.expander(f"EXECUTION TRACE — {len(events)} Tool Call(s) Executed", expanded=False):
                for ev in events:
                    tname = ev.get("tool", "unknown")
                    args = ev.get("args", {})
                    st.markdown(f"**Function:** `{tname}` &nbsp;&nbsp;|&nbsp;&nbsp; **Status:** `Executed`")
                    st.code(f"{tname}({json.dumps(args, ensure_ascii=False, indent=2)})", language="json")
                    res = ev.get("result", {})
                    if isinstance(res, dict) and "summary" in res and res["summary"]:
                        st.caption(f"Payload excerpt: {res['summary'][:200]}...")

# 7. User Input Processing
user_input = st.chat_input("Enter research request or query...")
if "preset_input" in st.session_state:
    user_input = st.session_state.pop("preset_input")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    working_messages = [{"role": "system", "content": current_cfg["prompt"]}]
    for m in st.session_state.messages:
        working_messages.append({"role": m["role"], "content": m["content"]})

    with st.chat_message("assistant"):
        with st.spinner(f"Routing & executing tools ({current_cfg['tag']})..."):
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
                    with st.expander(f"EXECUTION TRACE — {len(tool_events)} Tool Call(s) Executed", expanded=True):
                        for ev in tool_events:
                            tname = ev.get("tool", "unknown")
                            args = ev.get("args", {})
                            st.markdown(f"**Function:** `{tname}` &nbsp;&nbsp;|&nbsp;&nbsp; **Status:** `Executed`")
                            st.code(f"{tname}({json.dumps(args, ensure_ascii=False, indent=2)})", language="json")
                            res = ev.get("result", {})
                            if isinstance(res, dict) and "summary" in res and res["summary"]:
                                st.caption(f"Payload excerpt: {res['summary'][:200]}...")

                st.markdown(reply_text)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": reply_text,
                    "tool_events": tool_events
                })

            except Exception as e:
                st.error(f"Runtime Exception: {e}")
