
import logging
import argparse
from PIL import Image, ImageDraw, ImageFont
import subprocess
import textwrap
import threading
from queue import Queue
import keyboard
# Initialize logging
logging.basicConfig(filename='your_log_file.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# CLI argument parsing
parser = argparse.ArgumentParser(description="Image Generation and Printing")
parser.add_argument('--threading', action='store_true', help="Use threading for print queue processing")
args = parser.parse_args()

def camera():
    print("cam")
    webcam_command = "fswebcam webcam.jpg ;  brother_ql -b pyusb -m QL-550 -p usb://0x04f9:0x2016 print -l 62 --dither webcam.jpg"
    print_queue.add_to_queue(webcam_command)
    subprocess.run(webcam_command, shell=True)

    logging.info("Arrow key pressed. Webcam photo command added to queue.")


# A Python function to map ASCII characters to their Hebrew counterparts
def map_to_hebrew(input_text):
    # Mapping of ASCII to Hebrew characters
    ascii_to_hebrew = {
        'a': 'א',
        'b': 'ב',
        'c': 'ג',
        'd': 'ד',
        'e': 'ה',
        'f': 'ו',
        'g': 'ז',
        'h': 'ח',
        'i': 'ט',
        'j': 'י',
        'k': 'כ',
        'l': 'ל',
        'm': 'מ',
        'n': 'נ',
        'o': 'ס',
        'p': 'ע',
        'q': 'פ',
        'r': 'צ',
        's': 'ק',
        't': 'ר',
        'u': 'ש',
        'v': 'ת',
        'w': 'ץ',
        'x': 'ך',
        'y': 'ן',
        'z': 'ם',
        # Add any other characters you want to map
    }
    
    # Convert the input text
    output_text = ''.join([ascii_to_hebrew.get(char, char) for char in input_text.lower()])
    
    return output_text

while True:
    user_input = input("Type something (or press Enter to generate image): ")
    logging.info(f"User input: {user_input}")
    if user_input =="+":
        camera()
    elif user_input != "":

        mapped_text = map_to_hebrew(user_input)

        logging.info("Generating image...")
        img_width = 696
        wrapped_text = textwrap.fill(mapped_text, width=8)
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
