import os
import random
from PIL import Image, ImageDraw, ImageFont
import textwrap



l = int(input("Enter no of images: "))



def generate_subtle_color():
    return random.randint(100, 155), random.randint(180, 255), random.randint(180, 255)




for i in range(l):
    i, j, k = generate_subtle_color()
    p = f"{i,j,k}"
    img = Image.new("RGB", (1080, 1080), color=(i, j, k))
    img.save(f"data\\backgrounds\\{p}.jpg")