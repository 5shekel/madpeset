# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
import streamlit as st
import requests

from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("API_KEY")

# Specify the font size
font_size = 40
# Create an image
img_width = 696


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
    hebrew_text = st.text_area("Enter Hebrew Text:", "רסק שמופי טקסט", )

    # Button to send request
    if st.button("Process Text",):
        response = get_nakdan_response(hebrew_text, api_key)
        if not isinstance(response, dict):
            response = {'data': []}

        # st.json(response)
        # Extract words or newline from response
        words = []
        for item in response['data']:
            if 'nakdan' in item:
                if item['nakdan']['word'] == "\n":  # Check if the word is a newline
                    words.append("\n")
                else:
                    words.extend(
                        option['w'].replace("|", "")
                        for option in item['nakdan'].get('options', [])
                    )
        # st.text(" ".join(words))  # Print words, including newlines

        draw = Drawing()
        fontw = "fonts\\DejaVuSans.ttf"
        draw.font = fontw
        draw.text_antialias = True
        draw.text_encoding = 'utf-8'
        draw.font_size = font_size

        imgw = Image(width=696, height=400, background=Color('#ffffff'))

        spacing = 10
        line_width = 0
        y = font_size
        x = 0
        for word in words:
            if word == "\n":
                y += font_size
                line_width = 0
                continue
            
            # Create a dummy image to get the text metrics
            with Image(width=1, height=1) as img:
                metrics = draw.get_font_metrics(img, word)
                word_width = int(metrics.text_width)
                word_height = int(metrics.text_height)

            line_width += word_width + spacing
            # Position for the first word
            # Check if the word fits in the current line
            if line_width <= img_width - 20:
                x = img_width - (line_width) - 20
                # Render the word in the current line
                draw.text(x, y, word)
                x += word_width + spacing   # Add word width and spacing to x

            else:
                y += word_height
                line_width = 0
        # crop the image height to the text height
        imgw.crop(0, 0, img_width, y+spacing)
        
        draw(imgw)
        img_bytes = imgw.make_blob(format='png')
        st.image(img_bytes)
        # st.image(img)


if __name__ == "__main__":
    main()
