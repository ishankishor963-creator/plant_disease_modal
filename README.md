# Agro Edge — rebuilt for the field hardware station

## What changed from the old single-page app

- **Home.py** — pure AI diagnosis: upload or camera-capture a leaf photo, get
  the disease, confidence, treatment plan, and web references. This is your
  "AI model on the homepage."
- **Sidebar (Streamlit's built-in multipage nav, from `pages/`):**
  - 🎥 **Live Camera** — webcam feed today, drop-in ready for the ESP32-S3 +
    OV2640 board's stream URL later. Includes a "diagnose this frame" button
    that reuses the exact same AI model as Home.
  - 🌊 **Flood & Drought Alerts** — combines soil moisture + humidity +
    current rainfall condition (your requested logic) into one risk call,
    plus a water-level sensor slot for once that board is deployed.
  - 🌡️ **Temperature & Humidity** — live readings + a recent trend chart,
    with an ambient-weather fallback so the page is still useful before a
    board is wired up.
  - 🤖 **Ask AI Agent** — a chat-based plant-care assistant powered by the
    Anthropic API, separate from the diagnosis model.
- **config.py** — the one file to edit as your 4 ESP32 boards come online.
  Every sensor is looked up by name (`soil_moisture`, `temperature`,
  `humidity`, `water_level`) and only needs a `channel_id` / `read_api_key`
  / `field` filled in. Nothing else in the app needs to change.
- **theme.py / sensors.py / weather_utils.py / diagnosis.py** — shared code
  so the five pages don't duplicate logic or CSS.

## Before you run it

1. Copy your existing `recommendations.py` and `plant_model_v5.keras` into
   this folder (unchanged) — they aren't included here since they weren't
   part of what I was given.
2. `pip install -r requirements.txt`
3. Create `.streamlit/secrets.toml`:
   ```toml
   OPENWEATHER_API_KEY = "your_openweathermap_key"
   ANTHROPIC_API_KEY = "your_anthropic_key"
   ```
4. `streamlit run Home.py`

## Wiring up your 4 ESP32 boards

Open `config.py` and fill in `SENSOR_CHANNELS` for each sensor as its board
goes live — e.g. once your temperature/humidity ESP32 is pushing to a
ThingSpeak channel, set:
```python
"temperature": {"channel_id": "1234567", "read_api_key": "XXXX", "field": 1, "unit": "°C"},
"humidity":    {"channel_id": "1234567", "read_api_key": "XXXX", "field": 2, "unit": "%"},
```
(same channel, different fields, is the usual DHT/SHT sensor setup). The
soil moisture board is already wired to your existing channel `3467712`.

**LoRa nodes:** each field ESP32 talks LoRa to a single gateway (an ESP32 or
Raspberry Pi with a LoRa receiver); the gateway is what actually posts to
ThingSpeak over WiFi. This app only ever talks to ThingSpeak — it doesn't
need to know about LoRa at all, so the gateway can queue/retry independently
of whether this dashboard is open.

**Camera board (ESP32-S3 + OV2640):** once deployed, it can serve an MJPEG
stream (e.g. via the ESP32-CAM Arduino examples) at something like
`http://<device-ip>:81/stream`. Replace the webcam block in
`pages/1_🎥_Live_Camera.py` with an `st.image` loop reading that URL, or an
`<img src="...">` embed — the diagnosis button below it doesn't need to
change.

**Solar + battery + enclosure:** no code changes needed — these only affect
uptime of the ESP32 boards feeding ThingSpeak, which this app already treats
as "may go offline" (every sensor page shows a graceful "not configured /
no data" state rather than crashing).
