import random

sarcastic_lines = [
    "Oh, the weather? It’s sunny… just like your future. ☀️",
    "It’s raining sarcasm today. Better take an umbrella.",
    "Outside? It’s hotter than my WiFi router.",
    "The sky is crying… maybe because you asked.",
    "The weather? It’s perfect for a nap. Or two.",
    "Currently, 100% chance of you not going outside."
]

def get_sarcastic_reply():
    return random.choice(sarcastic_lines)
