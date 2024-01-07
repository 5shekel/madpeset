
import logging
import argparse
from PIL import Image, ImageDraw, ImageFont
import subprocess
import textwrap
import threading
from queue import Queue

# Initialize logging
logging.basicConfig(filename='your_log_file.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# CLI argument parsing
parser = argparse.ArgumentParser(description="Image Generation and Printing")
parser.add_argument('--threading', action='store_true', help="Use threading for print queue processing")
args = parser.parse_args()

def camera():
    print("cam")
    webcam_command = "fswebcam webcam.jpg ;  brother_ql -b pyusb -m QL-550 -p usb://0x04f9:0x2016 print -l 62 --dither webcam.jpg"
    subprocess.run(webcam_command, shell=True)

    logging.info("Arrow key pressed. Webcam photo command added to queue.")


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
        'b': 'נ',
        'x': 'ס',
        'g': 'ע',
        'p': 'פ',
        'm': 'צ',
        'e': 'ק',
        'r': 'ר',
        'a': 'ש',
        ',': 'ת',
        ';': 'ף',
        'i': 'ן',
        'l': 'ך',
        # Add any other characters you want to map
    }
    
    output_text = ''.join([keyboard_to_hebrew.get(char, char) for char in input_text.lower()])    
    return output_text

def rtl_text_wrap(text, width):
    words = text.split()
    lines = []
    current_line = []
    current_line_length = 0

    for word in reversed(words):  # Reverse words for RTL
        if current_line_length + len(word) <= width:
            current_line.append(word)
            current_line_length += len(word) + 1  # +1 for the space
        else:
            lines.append(' '.join(reversed(current_line)))  # Reverse back to original
            current_line = [word]
            current_line_length = len(word) + 1  # +1 for the space

    lines.append(' '.join(reversed(current_line)))  # Add the last line
    return '\n'.join(lines)


while True:
    user_input = input("Type something (or press Enter to generate image): ")
    logging.info(f"User input: {user_input}")
    if user_input =="+":
        camera()
    elif user_input != "":
        img_width = 696
        
        # Step 1: Map to Hebrew
        mapped_text = map_to_keyboard_hebrew(user_input)
        print("mapped "+mapped_text)
        logging.info("Generating image...")
        # Reverse characters within each word
        reversed_within_words = ' '.join([word[::-1] for word in mapped_text.split()])
        wrapped_text = rtl_text_wrap(reversed_within_words, 8)

        # wrapped_text = textwrap.fill(reversed_within_words, width=8)
        print("warp: "+wrapped_text)

        num_lines = wrapped_text.count('\n') + 1
        font_size = img_width // 6
        ttfont="/home/tasmi/printme/5x5-Tami.ttf"
        ttfont="/home/tasmi/printme/VarelaRound-Regular.ttf"
        ttfont="/home/tasmi/printme/fonts/xbmc-hebrew-fonts/Roboto-Bold-xbmc-il.ttf"
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
        

        printer_ql550="0x2016"
        printer_id1="000M6Z401370"
        command = f"brother_ql -b pyusb --model QL-550 -p usb://0x04f9:{printer_ql550}/{printer_id1} print -l 62 output.png"
        subprocess.run(command, shell=True)

        logging.info("Image generated and print command added to queue. Returning to input.")
    
# Uncomment this line if you'd like to listen for arrow key events.
# keyboard.on_press_key("up", on_arrow_key)
