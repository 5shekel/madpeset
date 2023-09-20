
from PIL import Image, ImageDraw, ImageFont
import subprocess
import textwrap
import keyboard

def on_arrow_key(e):
    subprocess.run("fswebcam webcam.jpg ;  brother_ql -b pyusb -m QL-550 -p usb://0x04f9:0x2016 print -l 62 --dither webcam.jpg", shell=True)
    print("Arrow key pressed. Webcam photo taken and printed.")

while True:
    user_input = input("Type something (or press Enter to generate image): ")
    print(user_input)

    if user_input != "":
        print("Generating image...")
        
        img_width = 696
        
        # Wrap text if a word is longer than 8 letters
        wrapped_text = textwrap.fill(user_input, width=8)
        num_lines = wrapped_text.count('\n') + 1
        
        # Calculate font size to fit the width of the image
        font_size = img_width // 6  # Adjust as needed
        ttfont="/home/tasmi/printme/5x5-Tami.ttf"
        ttfont="/home/tasmi/printme/VarelaRound-Regular.ttf"
        font = ImageFont.truetype(ttfont, font_size)
        
        # Calculate image height based on the number of lines and font size
        line_height = font_size + 10  # Include some padding, adjust as needed
        img_height = num_lines * line_height + 200
        
        image = Image.new('RGB', (img_width, img_height), 'white')
        d = ImageDraw.Draw(image)
        
        # Calculate position to center-align the text
        text_width, text_height = d.textsize(wrapped_text, font=font)
        x = (img_width - text_width) // 2
        y = (img_height - text_height) // 2
        
        print(wrapped_text)
        
        d.text((x, y), wrapped_text, font=font, fill=(0, 0, 0))
        
        image.save("output.png")

        printer_ql550="0x2016"
        printer_id1="000M6Z401370"
        command = f"brother_ql -b pyusb --model QL-550 -p usb://0x04f9:{printer_ql550}/{printer_id1} print -l 62 output.png"
        subprocess.run(command, shell=True)

        print("Image generated. Returning to input.")
