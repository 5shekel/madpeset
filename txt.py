# -*- coding: utf-8 -*-
import os
import argparse
from PIL import Image, ImageDraw, ImageFont
import subprocess

# Get the current user's username
username = os.getlogin()

# CLI argument parsing
parser = argparse.ArgumentParser(description="Image Generation and Printing")
args = parser.parse_args()


def camera():
    print("cam")
    webcam_command = (
        "fswebcam webcam.jpg ; "
        "/home/{username}/.local/bin/brother_ql -b pyusb -m QL-550 "
        "-p usb://0x04f9:0x2016 print -l 62 --dither webcam.jpg"
    )
    subprocess.run(webcam_command, shell=True)


def map_to_keyboard_hebrew(input_text):
    keyboard_to_hebrew = {
        't': 'א',
        'c': 'ב',
        'd': 'ג',
        's': 'ד',
        'v': 'ה',
        'u': 'ו',
        'z': 'ז',
        'j': 'ח',
        'y': 'ט',
        'h': 'י',
        'f': 'כ',
        'k': 'ל',
        'n': 'מ',
        'o': 'ם',
        'b': 'נ',
        'i': 'ן',
        'x': 'ס',
        'g': 'ע',
        'p': 'פ',
        'm': 'צ',
        '.': 'ץ',
        'e': 'ק',
        'r': 'ר',
        'a': 'ש',
        ',': 'ת',
        ';': 'ף',
        'i': 'ן',
        'l': 'ך',
        '/': '.',
        '\/': ',',
        '@': '"',
        # Add any other characters you want to map
    }
    
    output_text = ''.join([keyboard_to_hebrew.get(char, char) for char in input_text.lower()])    
    return output_text


def rtl_text_wrap(text, width):
    words = text.split()
    lines = []
    current_line = []
    current_line_length = 0

    for word in words:
        if current_line_length + len(word) <= width:
            current_line.insert(0, word)  # Insert word at the beginning of the current line
            current_line_length += len(word) + 1
        else:
            # When the line exceeds the width, finalize the current line
            lines.append(' '.join(current_line))
            current_line = [word]
            current_line_length = len(word) + 1

    # Add the last line to the lines list
    lines.append(' '.join(current_line))

    return '\n'.join(lines)


def print_label(image_path, printer_ql550="0x2016", printer_id1="000M6Z401370"):
    command = (
        f"/home/{username}/.local/bin/brother_ql -b pyusb --model QL-550 "
        f"-p usb://0x04f9:{printer_ql550}/{printer_id1} print -l 62 {image_path}"
    )
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if "The system cannot find the path specified." in process.stderr:
        print("printer not connected")


while True:
    user_input = input("Type something (or press + for camera): ")
    if user_input == "+":
        camera()
    elif user_input != "":
        img_width = 696

        # Step 1: Map to Hebrew
        mapped_text = map_to_keyboard_hebrew(user_input)
        print("mapped "+mapped_text)
        # Reverse characters within each word
        reversed_within_words = ' '.join([word[::-1] for word in mapped_text.split()])
        wrapped_text = rtl_text_wrap(reversed_within_words, 8)

        print("warp: "+wrapped_text)

        num_lines = wrapped_text.count('\n') + 1
        
        font_size = img_width // 6
        # ttfont = "5x5-Tami.ttf"
        # ttfont = "VarelaRound-Regular.ttf"
        ttfont = "fonts/xbmc-hebrew-fonts/Roboto-Bold-xbmc-il.ttf"
        font = ImageFont.truetype(ttfont, font_size)
        
        line_height = font_size + 10
        img_height = num_lines * line_height + 200
        image = Image.new('RGB', (img_width, img_height), 'white')
        d = ImageDraw.Draw(image)
        text_width, text_height = d.textsize(wrapped_text, font=font)
        x = (img_width - text_width) // 2
        y = (img_height - text_height) // 2

        d.text((x, y), wrapped_text, font=font, fill=(0, 0, 0))
        image.save("output.png")

        print_label("output.png")
