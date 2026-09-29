from PIL import Image, ImageDraw, ImageFont

img = Image.new('L', (200, 200), color=0)
d = ImageDraw.Draw(img)
try:
    font = ImageFont.truetype("/System/Library/Fonts/Apple Color Emoji.ttc", 100)
    d.text((100, 100), "⚡", fill=255, font=font, anchor="mm")
    
    pixels = img.load()
    count = sum(1 for y in range(200) for x in range(200) if pixels[x, y] > 0)
    print("Pixels found:", count)
except Exception as e:
    print("Error:", e)
