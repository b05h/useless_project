import streamlit as st
import cv2
from PIL import Image
import random
from sunglass_detection import detect_sunglasses_from_frame  # Your detection function

# Define variables needed in current_weather dict
current_condition = random.choice(["Sunny", "Cloudy", "Rainy"])
location_name = "Somewhere in the Northern Hemisphere"

# Dummy static weather data (fake & sarcastic)
current_weather = {
    "Temperature": "-10°C",
    "Feels Like": "Emotionally drained",
    "Humidity": "Soggy vibes",
    "Condition": current_condition,
    "Location": location_name,
    "Sunrise": "Whenever you wake up",
    "Sunset": "When you stop caring",
    "Wind": f"{random.randint(5, 20)} km/h {random.choice(['NW', 'SE', '🐸', '🌪️', '🦄'])}",
    "AQI": random.randint(1, 500),
    "UV Index": random.randint(0, 11),
}

hourly_forecast = [
    {"hour": "9 AM", "temp": "15°C", "cond": "Mostly meh"},
    {"hour": "12 PM", "temp": "18°C", "cond": "Slightly annoyed sun"},
    {"hour": "3 PM",  "temp": "17°C", "cond": "Clouds hiding, probably plotting"},
    {"hour": "6 PM", "temp": "14°C", "cond": "Getting cooler, like your mood"},
    {"hour": "9 PM", "temp": "12°C", "cond": "Chilly with attitude"},
    {"hour": "12 AM", "temp": "10°C", "cond": "Nighttime gloom"}
]

seven_day_forecast = [
    {"Day": day, "Condition": cond, "High": f"{random.randint(20, 30)}°C", "Low": f"{random.randint(10, 19)}°C"}
    for day, cond in zip(
        ["Someday", "Not Today", "Maybe Thursday", "Yesterday", "Ask Later", "Tomorrow-ish", "Whenever"],
        ["Pizza rain", "Sunny-ish with sarcasm", "Storm of nonsense", "Cloudy with weird vibes",
         "Windy, like your ex’s attitude", "Fog of confusion", "Sunburn chance high"]
    )
]

weather_alerts = [
    "⚠️ Severe nap conditions expected this afternoon.",
    "⚠️ Warning: clouds may judge you.",
    "⚠️ Alert: excessive sarcasm levels detected.",
]

pro_mode_message = "Subscribe to Pro to get exactly the same weather but with more sarcasm."

weather_keywords = [
    "weather", "rain", "sun", "sunny", "storm", "snow", "cloud", "cloudy",
    "wind", "windy", "temperature", "hot", "cold", "humidity", "forecast",
    "drizzle", "thunder", "lightning", "hail"
]

def ask_gemini(query):
    query_lower = query.lower()
    detected_keyword = None
    for kw in weather_keywords:
        if kw in query_lower:
            detected_keyword = kw
            break

    sarcastic_replies = {
        "rain": [
            "Oh great, another rainy day to ruin your plans. Don't forget your umbrella... or better yet, just stay inside!",
            "Yes. It’s raining wisdom. But not weather data.",
            "Rain check on your plans? Maybe check outside first next time.",
            "Umbrella sales are booming thanks to your curiosity.",
            "If you want a weather update, try looking out a window instead."
        ],
        "sun": [
            "Ah yes, the sun is shining bright just to remind you how sweaty you’ll be outside.",
            "Why don’t you open a window and find out like the good old days?",
            "Newsflash: the weather doesn’t text back.",
            "Go outside and stop bothering me with basic questions."
        ],
        "sunny": [
            "Ah yes, the sun is shining bright just to remind you how sweaty you’ll be outside.",
            "Why don’t you open a window and find out like the good old days?",
            "Newsflash: the weather doesn’t text back.",
            "Go outside and stop bothering me with basic questions."
        ],
        "storm": [
            "Storm alert! Perfect weather to test if your roof leaks or not.",
            "Storm’s brewing, just like your patience running out.",
            "Thunder’s just the sky clapping for your curiosity.",
            "Stormy questions..!! Too much to handle.",
            "Go watch the storm show live if it's storming instead of texting me."
        ],
        "snow": [
            "Snow again? Time to shovel and freeze your toes off!",
            "Cold enough outside to freeze that question in your brain.",
            "If you’re waiting for a snow day, maybe wait outside instead.",
            "Snow joke, this is basic stuff you can check yourself.",
            "Snowflakes aren’t the only things falling—your common sense too."
        ],
        "temperature": [
            "Why ask me when you can just feel the heat yourself?"
        ],
        "hot": [
            "It’s hot outside, just like this conversation.",
            "Hot enough to fry an egg, or just your brain cells?",
            "Sweating the small stuff? Go outside and cool off.",
            "Hot take: check the weather before pestering me.",
            "Feeling the heat? Maybe it’s your bad questions."
        ],
        "cold": [
            "Cold enough to freeze that question in your brain?"
        ],
        "humidity": [
            "If you want dry facts, check outside instead of asking.",
            "Humidity’s a pain, like repeating yourself to me."
        ],
        "cloud": [
            "Clouds outside, clouded judgment inside.",
            "Too cloudy for your brain to work?",
            "Cloudy skies, clearer excuses not to go outside.",
            "Clouds blocking the sun, and your common sense.",
            "Don’t blame the clouds for your dull questions."
        ],
        "lightning": [
            "Lightning fast questions, but slow answers.",
            "Hope lightning strikes before you ask that again.",
            "Bright flashes outside, dim thoughts inside.",
            "Lightning’s scary, your questions are scarier.",
            "Go watch the lightning show, I’m done here."
        ],
        "wind": [
            "The wind’s talking—too bad you’re not listening.",
            "Windy enough to blow your questions away.",
            "If you want a breeze, open a window, not your mouth.",
            "Your curiosity’s like the wind—always changing direction.",
            "Stop blowing hot air and check outside."
        ]
    }

    if detected_keyword:
        key = detected_keyword.lower()
        if key in sarcastic_replies:
            reply = random.choice(sarcastic_replies[key])
        else:
            reply = f"Yeah, the {detected_keyword} is just fabulous today. Couldn't be better!"
        return {"is_weather": True, "reply": reply}

    return {"is_weather": False, "reply": "Hmm, not sure about that. But I'm here to chat!"}

def show_dashboard():
    st.header("🌦 Convincing but Useless Weather Dashboard")

    # 1. Current Weather Card
    st.subheader("Current Weather")
    st.markdown(f"### {current_weather['Temperature']}")
    icon_map = {
        "Sunny": "☀️",
        "Cloudy": "☁️",
        "Rainy": "🌧️"
    }
    st.markdown(f"**{icon_map.get(current_weather['Condition'], '')} {current_weather['Condition']}**")
    st.markdown(f"Location: *{current_weather['Location']}*")
    st.markdown(f"Feels like: *{current_weather['Feels Like']}*")
    st.markdown(f"Humidity: *{current_weather['Humidity']}*")

    # 2. Hourly Forecast (horizontal scroll simulation)
    st.subheader("Hourly Forecast")
    cols = st.columns(6)
    for idx, hour in enumerate(hourly_forecast[:6]):
        with cols[idx]:
            st.write(hour["hour"])
            st.write(hour["temp"])
            st.write(hour["cond"])

    # 3. 7-Day Outlook
    st.subheader("7-Day Outlook")
    st.table(seven_day_forecast)

    # 4. Weather Radar (pizza image)
    st.subheader("Weather Radar")
    pizza_img_url = "https://i.imgur.com/e9h8Bpy.png"
    st.image(pizza_img_url, caption="Analyzing precipitation patterns... Done: Looks delicious.")

    # 5. Air Quality Index
    st.subheader("Air Quality Index")
    aqi_val = current_weather["AQI"]
    aqi_status = "Good"
    if aqi_val > 300:
        aqi_status = "Hazardous (like your ex)"
    elif aqi_val > 150:
        aqi_status = "Unhealthy"
    elif aqi_val > 100:
        aqi_status = "Moderate but suspicious"
    st.write(f"AQI: {aqi_val} — Status: {aqi_status}")

    # 6. UV Index with colored scale
    st.subheader("UV Index")
    uv = current_weather["UV Index"]
    uv_color = "green"
    if uv >= 8:
        uv_color = "red"
    elif uv >= 5:
        uv_color = "orange"
    st.markdown(f"<span style='color:{uv_color}; font-weight:bold;'>UV Index: {uv} (Best time to sunbathe… if you’re into that.)</span>", unsafe_allow_html=True)

    # 7. Sunrise / Sunset Times
    st.subheader("Sunrise / Sunset Times")
    st.write(f"Sunrise: {current_weather['Sunrise']}")
    st.write(f"Sunset: {current_weather['Sunset']}")

    # 8. Wind Speed with random emoji direction
    st.subheader("Wind Speed")
    st.write(current_weather["Wind"])

    # 9. Weather Alerts (banner style)
    st.subheader("Weather Alerts")
    for alert in weather_alerts:
        st.warning(alert)

    # 10. Location Search (fake)
    st.subheader("Location Search")
    location = st.text_input("Search location")
    if location:
        st.info("That’s the only place I care about.")

    # 11. Background Changes (simulate with color + emoji)
    st.subheader("Background")
    bg_condition = random.choice(["Sunny ☀️", "Rainy 🌧️", "Snowy ❄️", "Cloudy ☁️"])
    st.markdown(f"Background set to: **{bg_condition}** (But it doesn’t match the data, obviously)")

    # 12. Pro Mode (locked feature)
    st.subheader("Pro Mode")
    st.error(pro_mode_message)

def main():
    st.set_page_config(page_title="Sarcastic Weather App", page_icon="😏", layout="centered")

    if "sunglasses_ok" not in st.session_state:
        st.session_state.sunglasses_ok = False
    if "awaiting_upload" not in st.session_state:
        st.session_state.awaiting_upload = False

    if not st.session_state.sunglasses_ok:
        st.subheader("Step 1: Show me your sunglasses 😎")
        start = st.button("Start Detection")
        frame_window = st.image([])

        if start:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if not ret:
                st.error("🚫 Camera error")
            else:
                frame = cv2.flip(frame, 1)
                detected, annotated_frame = detect_sunglasses_from_frame(frame)
                frame_window.image(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB))
                if detected:
                    st.success("✅ Sunglasses detected! Access granted.")
                    st.session_state.sunglasses_ok = True
                    st.rerun()  # rerun app to show dashboard
                else:
                    st.error("🚫 No sunglasses detected! Go put them on if you want sarcastic weather.")
            cap.release()
    else:
        # Sunglasses detected → show dashboard + query tabs immediately
        st.header("Welcome to your sarcastic weather dashboard!")

        tab1, tab2 = st.tabs(["Dashboard", "Query Bot"])

        with tab1:
            show_dashboard()

        with tab2:
            if "query" not in st.session_state:
                st.session_state.query = ""

            if not st.session_state.awaiting_upload:
                query = st.text_input("Ask me anything (weather or not)...", value=st.session_state.query, key="query_input")
                if query and query != st.session_state.query:
                    st.session_state.query = query
                    result = ask_gemini(query)
                    st.write("🤖:", result["reply"])
                    st.info("This time I promise I'll give you the accurate weather... trust me 😏")
                    st.session_state.awaiting_upload = True

            else:
                outside_img = st.file_uploader("Upload a picture outside your window", type=["jpg", "png", "jpeg"])
                if outside_img:
                    img_out = Image.open(outside_img)
                    st.image(img_out, caption="📸 This is the weather right now. You're welcome.")
                    st.session_state.awaiting_upload = False
                    st.session_state.query = ""  # Clear previous query so input box resets

if __name__ == "__main__":
    main()
