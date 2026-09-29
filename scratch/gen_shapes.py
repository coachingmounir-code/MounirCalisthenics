import math
import json
import random

# Number of triangles
N = 30

# We want 7 shapes:
# 1. "M" (Start)
# 2. "Diamond" (Flow)
# 3. "Sun" (Beach)
# 4. "X" (Battle)
# 5. "Lightning" (Burpees)
# 6. "Pyramid" (Mindset)
# 7. "Eye" (Präsenz)

# A function to generate N triangles that roughly fill a given bounding box list or function
def generate_triangles_for_shape(shape_func, bounds=(0,0,100,100)):
    # Very simple approach: generate random triangles, if their center is inside the shape, keep them.
    # To make it look "arranged", we can generate points inside the shape and triangulate, 
    # but since we need EXACTLY N triangles, independent generation is easier.
    triangles = []
    
    # We will generate N random triangles inside the bounding box that satisfy shape_func
    # To make them look like shards, we can pick random centers inside the shape,
    # and give them random orientations and sizes.
    
    random.seed(42) # repeatable
    while len(triangles) < N:
        cx = random.uniform(bounds[0], bounds[2])
        cy = random.uniform(bounds[1], bounds[3])
        if shape_func(cx, cy):
            # Generate a triangle around cx, cy
            size = random.uniform(5, 25)
            angle = random.uniform(0, math.pi * 2)
            
            p1 = (cx + size * math.cos(angle), cy + size * math.sin(angle))
            p2 = (cx + size * math.cos(angle + 2*math.pi/3), cy + size * math.sin(angle + 2*math.pi/3))
            p3 = (cx + size * math.cos(angle + 4*math.pi/3), cy + size * math.sin(angle + 4*math.pi/3))
            
            # Add some randomness to points to make them not perfectly equilateral
            p1 = (p1[0] + random.uniform(-5,5), p1[1] + random.uniform(-5,5))
            p2 = (p2[0] + random.uniform(-5,5), p2[1] + random.uniform(-5,5))
            p3 = (p3[0] + random.uniform(-5,5), p3[1] + random.uniform(-5,5))
            
            # clamp to 0-100
            p1 = (max(0,min(100,p1[0])), max(0,min(100,p1[1])))
            p2 = (max(0,min(100,p2[0])), max(0,min(100,p2[1])))
            p3 = (max(0,min(100,p3[0])), max(0,min(100,p3[1])))
            
            triangles.append([p1, p2, p3])
            
    return triangles

# Define shapes (return True if (x,y) is inside)
def shape_M(x, y):
    # Left leg
    if 20 <= x <= 35 and 20 <= y <= 80: return True
    # Right leg
    if 65 <= x <= 80 and 20 <= y <= 80: return True
    # Left diagonal
    if 35 <= x <= 50 and 20 <= y <= 60 and abs(y - (x * 1.5 - 20)) < 15: return True
    # Right diagonal
    if 50 <= x <= 65 and 20 <= y <= 60 and abs(y - ((100-x) * 1.5 - 20)) < 15: return True
    return False

def shape_diamond(x, y):
    # center 50,50
    return abs(x - 50) + abs(y - 50) < 35

def shape_sun(x, y):
    # circle
    r = math.hypot(x-50, y-50)
    if r < 20: return True
    # rays
    if 25 < r < 45:
        angle = math.atan2(y-50, x-50)
        if math.cos(angle * 8) > 0.8: return True
    return False

def shape_X(x, y):
    return abs(x - y) < 10 or abs(x - (100 - y)) < 10

def shape_lightning(x, y):
    if 30 <= x <= 60 and 10 <= y <= 50: return True
    if 40 <= x <= 70 and 50 <= y <= 90: return True
    return False

def shape_pyramid(x, y):
    if 10 <= y <= 90:
        width = (y - 10) * 0.6
        if 50 - width <= x <= 50 + width: return True
    return False

def shape_eye(x, y):
    dy = abs(y - 50)
    max_dy = 30 * (1 - ((x-50)/40)**2)
    if 10 <= x <= 90 and dy < max_dy:
        # cut out pupil
        if math.hypot(x-50, y-50) < 10: return False
        return True
    return False

shapes = {
    "start": generate_triangles_for_shape(shape_M),
    "flow": generate_triangles_for_shape(shape_diamond),
    "beach": generate_triangles_for_shape(shape_sun),
    "battle": generate_triangles_for_shape(shape_X),
    "burpees": generate_triangles_for_shape(shape_lightning),
    "mindset": generate_triangles_for_shape(shape_pyramid),
    "presence": generate_triangles_for_shape(shape_eye),
}

# Print CSS variables
print(":root {")
for s_name, s_tris in shapes.items():
    print(f"  /* {s_name} */")
    for i, tri in enumerate(s_tris):
        pts = f"{tri[0][0]:.2f}% {tri[0][1]:.2f}%, {tri[1][0]:.2f}% {tri[1][1]:.2f}%, {tri[2][0]:.2f}% {tri[2][1]:.2f}%"
        print(f"  --{s_name}-{i}: polygon({pts});")
print("}")
