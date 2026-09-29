import json

# 30 Triangles defined by 19 vertices (V0 to V18)
# V0 = center
# V1-V6 = inner ring (clockwise)
# V7-V12 = middle ring (clockwise)
# V13-V18 = outer ring (clockwise)

triangles = [
    # Inner
    (0,1,2), (0,2,3), (0,3,4), (0,4,5), (0,5,6), (0,6,1),
    # Middle
    (1,7,2), (2,7,8), (2,8,3), (3,8,9), (3,9,4), (4,9,10), (4,10,5), (5,10,11), (5,11,6), (6,11,12), (6,12,1), (1,12,7),
    # Outer
    (7,13,8), (8,13,14), (8,14,9), (9,14,15), (9,15,10), (10,15,16), (10,16,11), (11,16,17), (11,17,12), (12,17,18), (12,18,7), (7,18,13)
]

def make_shape(name, points):
    # points is a list of 19 (x,y) tuples
    return {"name": name, "points": points}

# 1. Flexing Arm (Start) - Muscle, strength
# A stylized arm: Shoulder(20,70), Elbow(60,90), Fist(80,30)
p_arm = [
    (50,50), # 0: center of bicep
    (40,40), (60,40), (70,50), (60,60), (40,60), (30,50), # 1-6 inner bicep
    (30,30), (70,30), (85,45), (70,80), (30,80), (15,50), # 7-12 outer arm structure
    (20,20), (80,20), (95,40), (75,95), (20,95), (5,50)   # 13-18 background/edges
]

# 2. Flow/Dancer - Dynamic curve
p_dance = [
    (50,50), # 0: waist
    (45,35), (55,35), (60,50), (55,65), (45,65), (40,50), # 1-6 torso
    (40,15), (60,20), (75,55), (70,85), (40,90), (25,55), # 7-12 limbs
    (35,5),  (65,10), (90,60), (80,95), (30,95), (10,60)  # 13-18 extensions
]

# 3. Sun (Endurance/Beach)
p_sun = [
    (50,50), # 0
    (50,35), (65,50), (60,65), (50,65), (35,50), (40,35), # 1-6 inner circle
    (50,15), (85,50), (75,85), (50,85), (15,50), (25,15), # 7-12 middle rays
    (50,0),  (100,50), (85,100), (50,100), (0,50), (15,0)   # 13-18 outer rays
]

# 4. Crossed Swords/Bars (Battle)
p_battle = [
    (50,50), # 0
    (45,40), (55,40), (60,50), (55,60), (45,60), (40,50), # 1-6 center cross
    (25,25), (75,25), (75,50), (75,75), (25,75), (25,50), # 7-12 inner bars
    (10,10), (90,10), (90,50), (90,90), (10,90), (10,50)  # 13-18 outer bars
]

# 5. Lightning (Burpees)
p_lightning = [
    (50,50), # 0
    (55,40), (65,40), (55,50), (45,60), (35,60), (45,50), # 1-6 inner bolt
    (60,20), (80,20), (60,40), (40,80), (20,80), (40,60), # 7-12 middle bolt
    (65,0),  (95,0),  (70,45), (35,100), (5,100), (30,55) # 13-18 outer bolt
]

# 6. Brain/Pyramid (Mindset) -> Let's do a Brain (two hemispheres)
p_brain = [
    (50,50), # 0
    (40,40), (60,40), (70,55), (60,70), (40,70), (30,55), # 1-6 inner lobes
    (25,25), (75,25), (85,55), (75,85), (25,85), (15,55), # 7-12 middle lobes
    (15,10), (85,10), (95,60), (80,95), (20,95), (5,60)   # 13-18 outer lobes
]

# 7. Eye (Presence/Waltz)
p_eye = [
    (50,50), # 0: pupil
    (45,45), (55,45), (60,50), (55,55), (45,55), (40,50), # 1-6 iris
    (30,35), (70,35), (85,50), (70,65), (30,65), (15,50), # 7-12 inner eye
    (10,30), (90,30), (100,50), (90,70), (10,70), (0,50)  # 13-18 outer eye
]

shapes = [
    make_shape("start", p_arm),
    make_shape("flow", p_dance),
    make_shape("beach", p_sun),
    make_shape("battle", p_battle),
    make_shape("burpees", p_lightning),
    make_shape("mindset", p_brain),
    make_shape("presence", p_eye)
]

# Assign shades to the 30 triangles to create a 3D low-poly effect
# We use HSL. Base hue will be set by CSS. We just set Lightness.
# For example, Lightness varies from 30% to 70%
import random
random.seed(42)
shades = [random.randint(30, 70) for _ in range(30)]

# Write CSS variables
with open('scratch/mesh.css', 'w') as f:
    f.write(":root {\n")
    for shape in shapes:
        name = shape["name"]
        pts = shape["points"]
        for i, tri_indices in enumerate(triangles):
            pA = pts[tri_indices[0]]
            pB = pts[tri_indices[1]]
            pC = pts[tri_indices[2]]
            clip = f"polygon({pA[0]}% {pA[1]}%, {pB[0]}% {pB[1]}%, {pC[0]}% {pC[1]}%)"
            f.write(f"  --{name}-{i}: {clip};\n")
    
    # Also write the shades
    for i, l in enumerate(shades):
        f.write(f"  --shade-{i}: {l}%;\n")
        
    f.write("}\n")

