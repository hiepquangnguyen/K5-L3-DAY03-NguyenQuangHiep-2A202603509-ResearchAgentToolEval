"""Unit tests for Member 2 (TV2: Weather Tool & Send Guardrail).

Tests are 100% offline and do not make real network calls.
"""
from __future__ import annotations

import pytest
import requests

from conftest import FakeResponse
from tools import TOOL_FUNCTIONS

weather_tool = TOOL_FUNCTIONS["weather"]
send_tool = TOOL_FUNCTIONS["send"]
lookup_tool = TOOL_FUNCTIONS["lookup"]


# ============================================================================
# 1. WEATHER TOOL UNIT TESTS (3 tests)
# ============================================================================

def test_weather_happy_path(fake_http) -> None:
    """Happy path: Mock Open-Meteo geocoding and forecast responses."""
    mock_payload = {
        "results": [
            {
                "name": "Hanoi",
                "latitude": 21.0285,
                "longitude": 105.8542,
                "country": "Vietnam",
            }
        ],
        "current": {
            "temperature_2m": 28.5,
            "relative_humidity_2m": 65,
            "weather_code": 0,
            "wind_speed_10m": 12.0,
        },
    }
    calls = fake_http(FakeResponse(mock_payload))

    result = weather_tool(city="Hanoi")

    assert len(calls) == 2
    assert "geocoding-api.open-meteo.com" in calls[0]["url"]
    assert "api.open-meteo.com" in calls[1]["url"]

    assert result["tool"] == "weather"
    assert result["city"] == "Hanoi"
    assert result["country"] == "Vietnam"
    assert result["temperature"] == 28.5
    assert result["unit"] == "°C"
    assert result["humidity"] == 65
    assert result["wind_speed"] == 12.0
    assert result["condition"] == "Clear sky"


def test_weather_empty_city_returns_error_dict() -> None:
    """Bad input: Empty or whitespace city must return an error dict and not raise."""
    result_empty = weather_tool(city="")
    assert result_empty["tool"] == "weather"
    assert result_empty["error"] == "ValueError"
    assert "empty" in result_empty["message"].lower()

    result_spaces = weather_tool(city="   ")
    assert result_spaces["tool"] == "weather"
    assert result_spaces["error"] == "ValueError"


def test_weather_network_failure_returns_error_dict(fake_http) -> None:
    """Failure path: Network timeout or HTTP error returns an error dict without raising."""
    fake_http(requests.RequestException("Connection timed out"))

    result = weather_tool(city="Tokyo")
    assert result["tool"] == "weather"
    assert result["error"] == "RequestException"
    assert "timed out" in result["message"]


# ============================================================================
# 2. ASSIGNED STUB TESTS (send guardrail & lookup)
# ============================================================================

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    """When confirmed=True and env vars are set, post to Telegram."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "fake_bot_token_123")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "fake_chat_456")

    calls = fake_http(FakeResponse({"ok": True}))

    result = send_tool(text="Bản tin nghiên cứu", confirmed=True)

    assert result["status"] == "sent"
    assert len(calls) == 1
    assert calls[0]["method"] == "POST"
    assert "fake_bot_token_123" in calls[0]["url"]
    assert calls[0]["json"]["chat_id"] == "fake_chat_456"
    assert calls[0]["json"]["text"] == "Bản tin nghiên cứu"


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    """When confirmed=True but env vars are missing, return error dict and do not call network."""
    calls = fake_http(FakeResponse({"ok": True}))

    result = send_tool(text="Bản tin", confirmed=True)

    assert result["error"] == "RuntimeError"
    assert "TELEGRAM_BOT_TOKEN" in result["message"]
    assert calls == []


def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    """When timeframe=None, the Tavily request body must omit the time_range key."""
    monkeypatch.setenv("TAVILY_API_KEY", "test-key")
    calls = fake_http(FakeResponse({"results": []}))

    result = lookup_tool(query="AI research", timeframe=None)

    assert len(calls) == 1
    assert "time_range" not in calls[0]["json"]
    assert calls[0]["json"]["query"] == "AI research"

