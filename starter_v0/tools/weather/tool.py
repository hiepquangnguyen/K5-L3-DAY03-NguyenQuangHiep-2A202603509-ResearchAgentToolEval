from __future__ import annotations

from typing import Any
import requests

from tools._shared import TIMEOUT, err

WMO_WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
}


def get_weather(city: str = "") -> dict[str, Any]:
    """Fetch current weather for a city using the Open-Meteo free API."""
    if not city or not city.strip():
        return {
            "tool": "weather",
            "error": "ValueError",
            "message": "City name must not be empty.",
        }

    city_name = city.strip()
    try:
        # Step 1: Geocode city name to latitude/longitude
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo_resp = requests.get(
            geo_url,
            params={"name": city_name, "count": 1, "language": "en", "format": "json"},
            timeout=TIMEOUT,
        )
        geo_resp.raise_for_status()
        geo_data = geo_resp.json()

        results = geo_data.get("results")
        if not results:
            return {
                "tool": "weather",
                "error": "NotFoundError",
                "message": f"City '{city_name}' not found.",
            }

        location = results[0]
        lat = location.get("latitude")
        lon = location.get("longitude")
        matched_city = location.get("name", city_name)
        country = location.get("country", "")

        # Step 2: Fetch current weather for coordinates
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_resp = requests.get(
            weather_url,
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
            },
            timeout=TIMEOUT,
        )
        weather_resp.raise_for_status()
        weather_data = weather_resp.json()

        current = weather_data.get("current", {})
        temp = current.get("temperature_2m")
        humidity = current.get("relative_humidity_2m")
        code = current.get("weather_code", 0)
        wind_speed = current.get("wind_speed_10m")
        condition = WMO_WEATHER_CODES.get(code, "Unknown")

        return {
            "tool": "weather",
            "city": matched_city,
            "country": country,
            "latitude": lat,
            "longitude": lon,
            "temperature": temp,
            "unit": "°C",
            "humidity": humidity,
            "wind_speed": wind_speed,
            "condition": condition,
        }
    except Exception as exc:
        return err("weather", exc)

