import streamlit as st
import tempfile
import numpy as np
import cv2
from PIL import Image
import google.generativeai as genai
from mocking_responses import get_sarcastic_reply
from sunglass_detection import detect_sunglasses_from_frame
import json
import os

# ===== CONFIGURE GEMINI API =====

weather_keywords = [
    "weather", "rain", "sun", "sunny", "storm", "snow", "cloud", "cloudy",
    "wind", "windy", "temperature", "hot", "cold", "humidity", "forecast",
    "drizzle", "thunder", "lightning", "hail"
]

def ask_gemini(query):
    query_lower = query.lower()
    
    # Check if any weather keyword is in the query
    detected_keyword = None
    for kw in weather_keywords:
        if kw in query_lower:
            detected_keyword = kw
            break
    
    if detected_keyword:
        # Prepare a sarcastic reply based on detected_keyword
        if detected_keyword == "rain":
            reply = "Oh great, another rainy day to ruin your plans. Don't forget your umbrella... or better yet, just stay inside!"
        elif detected_keyword == "sun" or detected_keyword == "sunny":
            reply = "Ah yes, the sun is shining bright just to remind you how sweaty you’ll be outside."
        elif detected_keyword == "storm":
            reply = "Storm alert! Perfect weather to test if your roof leaks or not."
        elif detected_keyword == "snow":
            reply = "Snow again? Time to shovel and freeze your toes off!"
        else:
            reply = f"Yeah, the {detected_keyword} is just fabulous today. Couldn't be better!"
        
        return {"is_weather": True, "reply": reply}
    
    # If no weather keyword detected, normal reply
    return {"is_weather": False, "reply": "Hmm, not sure about that. But I'm here to chat!"}

def main():
    st.set_page_config(page_title="Sarcastic Weather App", page_icon="😏", layout="centered")
    st.title("😎 Sarcastic Weather App")

    # ===== SESSION STATE =====
    if "sunglasses_ok" not in st.session_state:
        st.session_state.sunglasses_ok = False

    # ===== STEP 1: Sunglass Detection =====
    if not st.session_state.sunglasses_ok:
        st.subheader("Step 1: Show me your sunglasses 😎")
        start = st.button("Start Detection")
        FRAME_WINDOW = st.image([])

        if start:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if not ret:
                st.error("🚫 Camera error")
            else:
                frame = cv2.flip(frame, 1)
                detected, annotated_frame = detect_sunglasses_from_frame(frame)
                FRAME_WINDOW.image(cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB))

                if detected:
                    st.success("✅ Sunglasses detected! Access granted.")
                    st.session_state.sunglasses_ok = True
                else:
                    st.error("🚫 No sunglasses detected! Go put them on if you want sarcastic weather.")
            cap.release()

    # ===== STEP 2: Query Box =====
    if st.session_state.sunglasses_ok:
        query = st.text_input("Ask me anything (weather or not)...")
        if query:
            result = ask_gemini(query)
            st.write("🤖:", result["reply"])


            # ===== STEP 3: Compel user to try again =====
            st.info("This time I promise I'll give you the accurate weather... trust me 😏")

            # ===== STEP 4: Upload outside image =====
            outside_img = st.file_uploader("Upload a picture outside your window", type=["jpg", "png", "jpeg"])
            if outside_img:
                img_out = Image.open(outside_img)
                st.image(img_out, caption="📸 This is the weather right now. You're welcome.")

if __name__ == "__main__":
    main()
