from PIL import Image, ImageDraw, ImageFont
import math

def generate_triangles_for_char(char, num_triangles=150):
    img = Image.new('L', (200, 200), color=0)
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 150)
    except:
        font = ImageFont.load_default()
    
    d.text((100, 100), char, fill=255, font=font, anchor="mm")
    
    pixels = img.load()
    valid_points = []
    for y in range(200):
        for x in range(200):
            if pixels[x, y] > 128:
                valid_points.append((x / 2.0, y / 2.0)) # scale to 100x100
                
    if not valid_points:
        return []
        
    import random
    random.seed(42)
    tris = []
    
    # We want num_triangles. We can pick a random valid point as center,
    # and create a triangle of size ~ 3-8 around it.
    for _ in range(num_triangles):
        cx, cy = random.choice(valid_points)
        size = random.uniform(3, 8)
        angle = random.uniform(0, 6.28)
        
        p1 = (cx + size * math.cos(angle), cy + size * math.sin(angle))
        p2 = (cx + size * math.cos(angle + 2.09), cy + size * math.sin(angle + 2.09))
        p3 = (cx + size * math.cos(angle + 4.18), cy + size * math.sin(angle + 4.18))
        
        tris.append([p1, p2, p3])
        
    return tris

print(len(generate_triangles_for_char("M")))
