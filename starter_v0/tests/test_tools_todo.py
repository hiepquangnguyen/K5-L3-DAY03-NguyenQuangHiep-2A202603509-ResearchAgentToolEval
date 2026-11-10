"""TODO(student): Tool Unit Test Challenge.

Each test below is a stub. Replace `pytest.skip(...)` with a real test.
Patterns to copy are in test_tools_examples.py. Fixtures are in conftest.py.

Rules:
- Offline only: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
- One behaviour per test. Name the test after the behaviour, not the function.
- Done = `pytest tests/ -v` shows 0 skipped, 0 failed.
"""
from __future__ import annotations

import pytest

from conftest import FakeResponse  # noqa: F401  (you will need it)
from tools import TOOL_FUNCTIONS  # noqa: F401

TODO = "TODO(student): implement this test"


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    clarify_func = TOOL_FUNCTIONS["clarify"]
    result = clarify_func(
        question="Chọn một tùy chọn:",
        response_type="choice",
        options=["Lựa chọn A", "Lựa chọn B"]
    )
    assert result["options"] == ["Lựa chọn A", "Lựa chọn B"]
    assert result["awaiting_user"] is True
    assert result["response_type"] == "choice"


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    format_func = TOOL_FUNCTIONS["format"]
    items = [
        {"title": "Tin 1", "section": "Công nghệ", "url": "https://example.com/1"},
        {"title": "Tin 2", "section": "Kinh tế", "url": "https://example.com/2"},
        {"title": "Tin 3", "section": "Công nghệ", "url": "https://example.com/3"},
    ]
    result = format_func(items=items, template="sections")
    
    assert result["markdown"].count("## Công nghệ") == 1
    assert result["markdown"].count("## Kinh tế") == 1
    assert result["item_count"] == 3


def test_format_thread_numbers_items() -> None:
    format_func = TOOL_FUNCTIONS["format"]
    items = [
        {"title": "Ý chính thứ nhất", "url": "https://example.com/1"},
        {"title": "Ý chính thứ hai", "url": "https://example.com/2"},
    ]
    result = format_func(items=items, template="thread")
    
    assert "1/ " in result["markdown"]
    assert "2/ " in result["markdown"]


def test_format_empty_items_does_not_crash() -> None:
    format_func = TOOL_FUNCTIONS["format"]
    
    res_none = format_func(items=None)
    assert res_none["item_count"] == 0
    assert res_none["markdown"] == ""

    res_empty = format_func(items=[])
    assert res_empty["item_count"] == 0
    assert res_empty["markdown"] == ""

# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    # Set TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID, mock HTTP.
    # Assert: exactly one POST, URL contains the token, json has chat_id + text, status == "sent".
    pytest.skip(TODO)


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    pytest.skip(TODO)


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    # timeframe=None -> request body has no "time_range" key.
    pytest.skip(TODO)


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    # Mock {"data": {"markdown": "...", "metadata": {"title": "T", "sourceURL": "https://..."}}}
    # Assert title/url/source/summary in result["items"][0].
    pytest.skip(TODO)


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    pytest.skip(TODO)


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    # Mock {"timeline": [...]} with 1 item missing tweet_id and 6 valid items, limit=3.
    # Assert 3 items, and each url looks like https://x.com/<handle>/status/<id>.
    pytest.skip(TODO)


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    # Assert the request params carry the query and search_type ("Top" / "Latest").
    pytest.skip(TODO)


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    pytest.skip(TODO)


def test_policy_area_filter_only_returns_that_area() -> None:
    # policy_area="data_privacy" -> every result has policy_area == "data_privacy".
    pytest.skip(TODO)


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    # One policy file contains a quoted line that tries to give the assistant orders.
    # Query that section (source_citation) and assert: that line is in untrusted_text, NOT in facts.
    pytest.skip(TODO)


# ---------------- YOUR NEW TOOL(S) ----------------
# Write at least 3 tests per tool your team adds:
#   1. happy path (mocked if it calls an API)
#   2. bad / missing input from the model (empty string, wrong type, out-of-enum value)
#   3. failure path (missing key, HTTP error, timeout) -> returns error dict, does not raise

def test_my_new_tool_happy_path(fake_http) -> None:
    """1. Happy path: mock HTTP thành công và kiểm tra dữ liệu trả về."""
    fake_data = {
        "title": "Alan Turing",
        "extract": "Alan Mathison Turing was an English mathematician and computer scientist.",
        "content_urls": {"desktop": {"page": "https://en.wikipedia.org/wiki/Alan_Turing"}}
    }
    calls = fake_http(FakeResponse(fake_data, status_code=200))
    
    wiki_func = TOOL_FUNCTIONS["wikipedia"]
    result = wiki_func(query="Alan Turing")
    
    assert len(calls) == 1
    assert "Alan_Turing" in calls[0]["url"]
    assert result["title"] == "Alan Turing"
    assert "mathematician" in result["summary"]
    assert result["url"] == "https://en.wikipedia.org/wiki/Alan_Turing"


def test_my_new_tool_bad_input_from_model(fake_http) -> None:
    """2. Bad input: query rỗng hoặc trang 404 không tồn tại."""
    wiki_func = TOOL_FUNCTIONS["wikipedia"]
    
    # Trường hợp query rỗng: không gọi mạng, báo nhắc nhở
    res_empty = wiki_func(query="")
    assert "Vui lòng cung cấp từ khóa" in res_empty["summary"]
    
    # Trường hợp HTTP 404 không tìm thấy
    fake_http(FakeResponse({}, status_code=404))
    res_404 = wiki_func(query="TrangKhongTonTai12345")
    assert "Không tìm thấy" in res_404["summary"]


def test_my_new_tool_failure_returns_error_dict(fake_http) -> None:
    """3. Failure path: lỗi server 500 trả về dict error, không raise crash."""
    fake_http(FakeResponse(status_code=500))
    
    wiki_func = TOOL_FUNCTIONS["wikipedia"]
    result = wiki_func(query="Test Error")
    
    assert "error" in result
    assert result["tool"] == "search_wikipedia"