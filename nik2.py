import streamlit as st
from wand.image import Image as wImage
from wand.drawing import Drawing
from wand.color import Color

draw = Drawing()
font = "fonts\\DejaVuSans.ttf"
draw.font = font
img = wImage(width=696, height=100, background=Color('#ffffff'))
# draw.fill_color(Color('#000000'))
draw.text_alignment = 'right'
draw.text_antialias = True
draw.text_encoding = 'utf-8'
# draw.text_interline_spacing = 1
# draw.text_interword_spacing = 15.0
# draw.text_kerning = 0.0
draw.font_size = 40

draw.text(
    int(img.width / 2), 
    int(img.height / 2), 
    u'יֵשׁ לְךָ חָבֵר חָדָשׁ'
    )

draw(img)
img_bytes = img.make_blob(format='png')
st.image(img_bytes)
