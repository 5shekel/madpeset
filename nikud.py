# -*- coding: utf-8 -*-

import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()
# Read API key from .env file
api_key = os.getenv("API_KEY")

def get_nakdan_response(hebrew_text, api_key):
    url = "https://nakdan-5-3.loadbalancer.dicta.org.il/addnikud"
    headers = {'Content-Type': 'text/plain;charset=utf-8'}
    params = {
        "task": "nakdan",
        "useTokenization": True,
        "genre": "modern",  # or "rabbinic" or "premodern" based on user's need
        "data": hebrew_text,
        "addmorph": True,
        "matchpartial": True, 
        "keepmetagim": False,
        "keepqq": False,
        "apiKey": api_key
    }
    response = requests.post(url, headers=headers, json=params)
    return response.json()


# Create an image
img = Image.new('RGB', (300, 100), color = (255, 255, 255))
d = ImageDraw.Draw(img)
ttfont = "fonts/xbmc-hebrew-fonts/Roboto-Bold-xbmc-il.ttf"
ttfont = "fonts/BonaNova-Regular.ttf"
font = ImageFont.truetype(ttfont, 10)


def main():
    st.title('Dicta Nakdan API Interface')

    # Input fields for user
    hebrew_text = st.text_area("Enter Hebrew Text:", "טקסט טקסט טקסט")

    # Button to send request
    if st.button("Process Text"):
        response = get_nakdan_response(hebrew_text, api_key)
        # st.json(response)
        # Extract words
        words = [option['w'] for item in response['data'] if 'nakdan' in item for option in item['nakdan'].get('options', [])]
        st.text(words)
        # Create an image
        img = Image.new('RGB', (300, 100), color=(255, 255, 255))
        d = ImageDraw.Draw(img)

        # Position for the first word
        x, y = 10, 40

        # Write words on the image
        for word in words:
            d.text((x, y), word, fill=(0, 0, 0), font=font)
            y += 15  # Move to the next line
        st.image(img)




if __name__ == "__main__":
    main()
