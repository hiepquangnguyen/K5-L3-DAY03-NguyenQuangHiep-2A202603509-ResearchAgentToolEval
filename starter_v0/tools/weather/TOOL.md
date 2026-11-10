---
name: weather
track: bonus
kind: live_api
provider: Open-Meteo
requires_env: []
inputs: [city]
outputs: [tool, city, country, latitude, longitude, temperature, unit, humidity, wind_speed, condition]
side_effect: false
---

# Weather Tool

Tra cứu thông tin thời tiết hiện tại và các chỉ số (nhiệt độ, độ ẩm, tốc độ gió, trạng thái) theo tên thành phố hoặc địa điểm thông qua Open-Meteo API (hoàn toàn miễn phí, không yêu cầu API key).

