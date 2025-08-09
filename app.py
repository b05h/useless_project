import streamlit as st
import cv2
from PIL import Image
from sunglass_detection import detect_sunglasses_from_frame  # Your detection function

# Dummy static weather data (fake & sarcastic)
current_weather = {
    "Temperature": "-10°C (But feels like emotionally drained)",
    "Condition": "Cloudy with a chance of sarcasm",
    "UV Index": "Very high — sunglasses recommended (obviously)",
    "AQI": "42 (Safe, unless you ask me!)"
}

hourly_forecast = [
    {"hour": "9 AM", "temp": "15°C", "cond": "Mostly meh"},
    {"hour": "12 PM", "temp": "18°C", "cond": "Slightly annoyed sun"},
    {"hour": "3 PM",  "temp": "17°C", "cond": "Clouds hiding, probably plotting"},
    {"hour": "6 PM", "temp": "14°C", "cond": "Getting cooler, like your mood"}
]

seven_day_forecast = [
    {"Day": "Maybe Tomorrow", "Condition": "Pizza rain", "High": "26°C", "Low": "18°C"},
    {"Day": "Not Today", "Condition": "Sunny-ish with sarcasm", "High": "27°C", "Low": "17°C"},
    {"Day": "Maybe Thursday", "Condition": "Storm of nonsense", "High": "25°C", "Low": "19°C"},
    {"Day": "Someday", "Condition": "Cloudy with weird vibes", "High": "24°C", "Low": "18°C"},
    {"Day": "Yesterday", "Condition": "Windy, like your ex’s attitude", "High": "23°C", "Low": "17°C"}
]

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
    
    if detected_keyword:
        if detected_keyword == "rain":
            reply = "Oh great, another rainy day to ruin your plans. Don't forget your umbrella... or better yet, just stay inside!"
        elif detected_keyword in ["sun", "sunny"]:
            reply = "Ah yes, the sun is shining bright just to remind you how sweaty you’ll be outside."
        elif detected_keyword == "storm":
            reply = "Storm alert! Perfect weather to test if your roof leaks or not."
        elif detected_keyword == "snow":
            reply = "Snow again? Time to shovel and freeze your toes off!"
        else:
            reply = f"Yeah, the {detected_keyword} is just fabulous today. Couldn't be better!"
        return {"is_weather": True, "reply": reply}
    return {"is_weather": False, "reply": "Hmm, not sure about that. But I'm here to chat!"}

def show_dashboard():
    st.header("🌦 Fake Weather Dashboard")

    st.subheader("Current Weather")
    for key, val in current_weather.items():
        st.write(f"**{key}:** {val}")

    st.subheader("Hourly Forecast")
    for hour in hourly_forecast:
        st.write(f"{hour['hour']}: {hour['temp']}, {hour['cond']}")

    st.subheader("7-Day Outlook")
    st.table(seven_day_forecast)

    st.subheader("Radar")
    pizza_img_url = "https://i.imgur.com/e9h8Bpy.png"  # Example pizza radar image
    st.image(pizza_img_url, caption="Radar? More like pizza delivery map!")

    st.subheader("Air Quality & UV Index")
    st.write(f"AQI: {current_weather['AQI']}")
    st.write(f"UV Index: {current_weather['UV Index']}")

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
                    st.rerun()
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
            if not st.session_state.awaiting_upload:
                query = st.text_input("Ask me anything (weather or not)...")
                if query:
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

if __name__ == "__main__":
    main()
