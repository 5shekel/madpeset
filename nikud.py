# -*- coding: utf-8 -*-

import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
import os
from bidi.algorithm import get_display

# Load environment variables from .env file
load_dotenv()
# Read API key from .env file
api_key = os.getenv("API_KEY")

# Specify the font size
font_size = 80
# font = ImageFont.truetype("fonts/BonaNova-Regular.ttf", font_size, encoding='unic')
font = ImageFont.truetype("fonts/DejaVuSans.ttf", font_size)  # only one that works


# place the api_key in the .env file
# such as API_KEY=your_api_key
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
    try:
        response = requests.post(url, headers=headers, json=params)
        response.raise_for_status()  # Raises stored HTTPError, if one occurred.
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Something went wrong", err)
    else:
        return response.json()


def main():
    st.title('Dicta Nakdan API Interface')

    # Input fields for user
    hebrew_text = st.text_area("Enter Hebrew Text:", "טקסט טקסט טקסט")

    # Button to send request
    if st.button("Process Text"):
        response = get_nakdan_response(hebrew_text, api_key)
        if not isinstance(response, dict):
            response = {'data': []}
        # st.json(response)
        # Extract words
        words = [
            option['w'].replace("|", "")
            for item in response['data']
            if 'nakdan' in item
            for option in item['nakdan'].get('options', [])
        ]
        st.text(" ".join(words))  # printwords after each other

        # Create an image
        img_width = 696
        img_height = 400  # font_size * (len(words) // 10 + 2)  # Adjust the multiplier as needed
        img = Image.new('RGB', (img_width, img_height), color=(255, 255, 255))
        d = ImageDraw.Draw(img)

        # Position for the first word
        x, y = 10, 0

        max_width = img_width - 20  # Maximum width for each line
        line_width = 0  # Current line width

        for word in words:
            bidi_word = get_display(word)  # Convert word to RTL format
            word_width = font.getbbox(bidi_word)[2] - font.getbbox(bidi_word)[0]  # Width of the word

            # Check if the word fits in the current line
            if line_width + word_width <= img_width - 20:
                # Render the word in the current line
                d.text((img_width - (x + line_width + word_width), y), bidi_word, fill=(0, 0, 0), font=font)
                line_width += word_width + 10  # Add word width and spacing
            else:
                # Move to the next line
                y += font_size  # Move to the next line
                line_width = 0  # Reset line width

                # Check if the word fits in the new line
                if word_width <= img_width - 20:
                    # Render the word in the new line
                    d.text((img_width - (x + line_width + word_width), y), bidi_word, fill=(0, 0, 0), font=font)
                    line_width += word_width + 10  # Add word width and spacing
                else:
                    # Word is too long for a single line, truncate it
                    truncated_word = bidi_word[:max_width // font_size] + "..."
                    d.text((img_width - (x + line_width + font.getsize(truncated_word)[0]), y), truncated_word, fill=(0, 0, 0), font=font)
                    line_width += font.getsize(truncated_word)[0] + 10  # Add truncated word width and spacing

            # st.text(f"Word: '{bidi_word}', Position: (x={x + line_width - word_width}, y={y}), {len(bidi_word)} characters")

        st.image(img)


if __name__ == "__main__":
    main()
