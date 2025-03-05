import json
from PIL import Image, ImageDraw, ImageFont

# Sample JSON input (as a string)
json_input = '''
{
    "*_background_color": "#FFFF00 (a bright, sunny yellow)",
    "*_image_theme_for_the_background": "Colorful Holi celebrations with gulal (powder) and thandai (drink)",
    "*_language_of_the_greeting": "Hindi",
    "*_recipient's-name": "Friends & Family",
    "*_sender's-name": "Unknown",
    "*_text_color": "#FF69B4 (a bright, festive pink)",
    "*_title_for_the_greeting_card": "\\"Vibrant Holi Wishes\\""
}
'''

# Parse JSON input
data = json.loads(json_input)

# Helper function to extract color code (e.g., "#FFFF00")
def extract_color(color_str):
    # Splitting at space and taking the first part
    return color_str.split()[0]

# Extract design parameters from the JSON
background_color = extract_color(data["*_background_color"])
text_color = extract_color(data["*_text_color"])
title_text = data["*_title_for_the_greeting_card"].strip('"')
language = data["*_language_of_the_greeting"]
recipient = data["*_recipient's-name"]
sender = data["*_sender's-name"]

# Create a new image with the specified background color
img_width, img_height = 800, 600  # dimensions can be adjusted
image = Image.new("RGB", (img_width, img_height), background_color)
draw = ImageDraw.Draw(image)

# Load fonts - adjust font paths and sizes as necessary
try:
    title_font = ImageFont.truetype("arialbd.ttf", 60)
    body_font = ImageFont.truetype("arial.ttf", 40)
except IOError:
    # Fallback to default font if custom fonts are not available
    title_font = ImageFont.load_default()
    body_font = ImageFont.load_default()

# Helper function to get text size using textbbox
def get_text_size(draw_obj, text, font):
    bbox = draw_obj.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    return width, height

# Center the title text at the top
title_width, title_height = get_text_size(draw, title_text, title_font)
title_position = ((img_width - title_width) // 2, 50)
draw.text(title_position, title_text, fill=text_color, font=title_font)

# Prepare the body greeting text in Hindi
greeting_text = (
    f"प्रिय {recipient},\n\n"
    "होली की ढेर सारी शुभकामनाएँ!\n"
    f"आपका शुभेच्छु,\n{sender}"
)

# Calculate position for the body text (for multi-line text, you might need extra spacing)
body_width, body_height = get_text_size(draw, greeting_text, body_font)
body_position = ((img_width - body_width) // 2, title_position[1] + title_height + 50)
draw.multiline_text(body_position, greeting_text, fill=text_color, font=body_font, align="center")

# Save the final image
output_file = "greeting_card.png"
image.save(output_file)
print(f"Greeting card generated and saved as {output_file}")
