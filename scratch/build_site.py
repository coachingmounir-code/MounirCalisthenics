import math
import random

# Generate shapes
N = 30
shapes_info = [
    ("start", "Mounir Calisthenics", "#2c3e50", "#e74c3c"),
    ("flow", "Flow & Rhythmus", "#16a085", "#f1c40f"),
    ("beach", "Endurance Vibes", "#f39c12", "#8e44ad"),
    ("battle", "Street Battle", "#8e44ad", "#3498db"),
    ("burpees", "8x30s Burpees", "#c0392b", "#f1c40f"),
    ("mindset", "3 Säulen Identität", "#2980b9", "#2ecc71"),
    ("presence", "Körpersprache", "#27ae60", "#ecf0f1")
]

def shape_M(x, y):
    if 25 <= x <= 35 and 25 <= y <= 75: return True
    if 65 <= x <= 75 and 25 <= y <= 75: return True
    if 35 <= x <= 50 and 25 <= y <= 60 and abs(y - (x * 1.5 - 20)) < 15: return True
    if 50 <= x <= 65 and 25 <= y <= 60 and abs(y - ((100-x) * 1.5 - 20)) < 15: return True
    return False

def shape_diamond(x, y): return abs(x - 50) + abs(y - 50) < 35
def shape_sun(x, y):
    r = math.hypot(x-50, y-50)
    if r < 20: return True
    if 25 < r < 40 and math.cos(math.atan2(y-50, x-50) * 8) > 0.6: return True
    return False

def shape_X(x, y): return abs(x - y) < 12 or abs(x - (100 - y)) < 12
def shape_lightning(x, y):
    if 35 <= x <= 65 and 15 <= y <= 55: return True
    if 45 <= x <= 75 and 45 <= y <= 85: return True
    return False

def shape_pyramid(x, y):
    if 20 <= y <= 80:
        if 50 - (y - 20) * 0.6 <= x <= 50 + (y - 20) * 0.6: return True
    return False

def shape_eye(x, y):
    dy = abs(y - 50)
    max_dy = 25 * (1 - ((x-50)/40)**2)
    if 10 <= x <= 90 and dy < max_dy:
        if math.hypot(x-50, y-50) < 10: return False
        return True
    return False

funcs = [shape_M, shape_diamond, shape_sun, shape_X, shape_lightning, shape_pyramid, shape_eye]

random.seed(99)
all_shapes = []
for f in funcs:
    tris = []
    while len(tris) < N:
        cx, cy = random.uniform(10, 90), random.uniform(10, 90)
        if f(cx, cy):
            size = random.uniform(10, 20)
            angle = random.uniform(0, 6.28)
            p1 = (cx + size * math.cos(angle), cy + size * math.sin(angle))
            p2 = (cx + size * math.cos(angle + 2.09), cy + size * math.sin(angle + 2.09))
            p3 = (cx + size * math.cos(angle + 4.18), cy + size * math.sin(angle + 4.18))
            # clamp
            p1 = (max(0,min(100,p1[0])), max(0,min(100,p1[1])))
            p2 = (max(0,min(100,p2[0])), max(0,min(100,p2[1])))
            p3 = (max(0,min(100,p3[0])), max(0,min(100,p3[1])))
            tris.append([p1, p2, p3])
    all_shapes.append(tris)

# Build CSS
css_vars = []
for s_idx, (s_name, _, _, _) in enumerate(shapes_info):
    for i, tri in enumerate(all_shapes[s_idx]):
        pts = f"{tri[0][0]:.2f}% {tri[0][1]:.2f}%, {tri[1][0]:.2f}% {tri[1][1]:.2f}%, {tri[2][0]:.2f}% {tri[2][1]:.2f}%"
        css_vars.append(f"  --{s_name}-{i}: polygon({pts});")

css_rules = []
for s_idx, (s_name, _, bg_col, fg_col) in enumerate(shapes_info):
    css_rules.append(f"body[data-section='{s_idx}'] {{ background-color: {bg_col}; color: #fff; }}")
    css_rules.append(f"body[data-section='{s_idx}'] .shard {{ background-color: {fg_col}; }}")
    for i in range(N):
        css_rules.append(f"body[data-section='{s_idx}'] .shard-{i} {{ clip-path: var(--{s_name}-{i}); }}")

with open('scratch/template.html', 'w') as f:
    f.write("""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <title>Species in Pieces Inspiration</title>
  <style>
    :root {
""" + "\n".join(css_vars) + """
    }
    body {
      margin: 0; padding: 0; overflow: hidden;
      font-family: 'Helvetica Neue', Arial, sans-serif;
      transition: background-color 1.2s cubic-bezier(0.86, 0, 0.07, 1);
    }
    
    /* Center Graphic Container */
    #graphic-container {
      position: absolute; top: 50%; left: 50%;
      transform: translate(-50%, -50%);
      width: 400px; height: 400px;
      pointer-events: none;
      z-index: 10;
    }
    
    .shard {
      position: absolute; top: 0; left: 0;
      width: 100%; height: 100%;
      transition: clip-path 1.2s cubic-bezier(0.86, 0, 0.07, 1), background-color 1.2s ease;
      opacity: 0.9;
      mix-blend-mode: screen;
    }
    
""" + "\n".join(css_rules) + """
    
    /* UI Overlay */
    #ui {
      position: absolute; top: 0; left: 0; width: 100%; height: 100%;
      pointer-events: none; z-index: 20;
    }
    
    .nav-dots {
      position: absolute; left: 40px; top: 50%;
      transform: translateY(-50%);
      display: flex; flex-direction: column; gap: 15px;
      pointer-events: auto;
    }
    .dot {
      width: 12px; height: 12px; border-radius: 50%;
      background: rgba(255,255,255,0.3);
      cursor: pointer; transition: all 0.3s;
    }
    .dot.active { background: #fff; transform: scale(1.3); }
    
    #title-display {
      position: absolute; bottom: 60px; left: 50%;
      transform: translateX(-50%);
      font-size: 24px; font-weight: bold; letter-spacing: 4px;
      text-transform: uppercase;
      opacity: 0; transition: opacity 0.5s;
    }
    
    .btn-explore {
      position: absolute; right: 0; top: 50%; transform: translateY(-50%);
      background: #111; color: #fff; padding: 20px 30px;
      font-size: 14px; font-weight: bold; cursor: pointer;
      pointer-events: auto; border: none; letter-spacing: 2px;
      text-transform: uppercase;
      transition: background 0.3s, right 0.6s cubic-bezier(0.86, 0, 0.07, 1);
      clip-path: polygon(10px 0, 100% 0, 100% 100%, 0 100%);
    }
    .btn-explore:hover { background: #333; }
    
    /* Side Panel */
    #drawer {
      position: absolute; top: 0; right: -600px;
      width: 600px; height: 100%;
      background: #fff; color: #111;
      transition: right 0.6s cubic-bezier(0.86, 0, 0.07, 1);
      z-index: 30; pointer-events: auto;
      overflow-y: auto;
      box-shadow: -10px 0 30px rgba(0,0,0,0.2);
    }
    body.drawer-open #drawer { right: 0; }
    body.drawer-open .btn-explore { right: 600px; }
    
    .drawer-content { display: none; padding: 60px; }
    .drawer-content.active { display: block; animation: fadeIn 0.5s forwards; }
    
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }
    
    h2 { font-size: 36px; margin-top: 0; }
    p { font-size: 16px; line-height: 1.6; color: #555; }
    
    .close-btn {
      position: absolute; top: 20px; right: 20px;
      background: none; border: none; font-size: 30px; cursor: pointer;
    }
    
  </style>
</head>
<body data-section="0">

  <div id="graphic-container">
""")
    for i in range(N):
        f.write(f'    <div class="shard shard-{i}"></div>\n')
    f.write("""  </div>
  
  <div id="ui">
    <div class="nav-dots" id="dots"></div>
    <div id="title-display">Mounir Calisthenics</div>
    <button class="btn-explore" onclick="toggleDrawer()">Inhalt ansehen ➔</button>
  </div>
  
  <div id="drawer">
    <button class="close-btn" onclick="toggleDrawer()">×</button>
    
    <div class="drawer-content" data-idx="0">
      <h2>Mounir Calisthenics</h2>
      <p>Willkommen zum offiziellen Trainings-Leitfaden. Kraft, Rhythmus, stählerne Disziplin und maximale Körperspannung.</p>
    </div>
    
    <div class="drawer-content" data-idx="1">
      <h2>Flow & Rhythmus</h2>
      <p>Mike Song Choreography. Starte mit Fokus auf Koordination und fließende Bewegung.</p>
      <iframe width="100%" height="250" src="https://www.youtube-nocookie.com/embed/g9FJhH9dOeU?rel=0" frameborder="0" allowfullscreen></iframe>
    </div>
    
    <div class="drawer-content" data-idx="2">
      <h2>Endurance Vibes</h2>
      <p>Chris Luno Beach House. Den richtigen Beat und die Leichtigkeit mitnehmen.</p>
      <iframe width="100%" height="250" src="https://www.youtube-nocookie.com/embed/ja2dGXXmFV4?rel=0" frameborder="0" allowfullscreen></iframe>
    </div>
    
    <div class="drawer-content" data-idx="3">
      <h2>Street Battle</h2>
      <p>Die Essenz von reinem Calisthenics – Bars, Dips, Muscle-Ups und Wettkampfgeist.</p>
      <iframe width="100%" height="250" src="https://www.youtube-nocookie.com/embed/UMYm2cBjZIY?rel=0" frameborder="0" allowfullscreen></iframe>
    </div>
    
    <div class="drawer-content" data-idx="4">
      <h2>8x30s Burpees</h2>
      <p>Das Kernstück: 8 Runden à 30 Sekunden Burpees. Maximale Intensität.</p>
      <button style="padding:15px;background:#c0392b;color:#fff;border:none;font-weight:bold;cursor:pointer;">Start Timer</button>
    </div>
    
    <div class="drawer-content" data-idx="5">
      <h2>Mindset: 3 Säulen</h2>
      <p>1. Disziplin & Fokus<br>2. Maximale Körperspannung<br>3. Unaufhaltsamer Wille</p>
    </div>
    
    <div class="drawer-content" data-idx="6">
      <h2>Präsenz & Wirkung</h2>
      <p>Christoph Waltz über Körpersprache, Dominanz und Ausstrahlung.</p>
      <iframe width="100%" height="250" src="https://www.youtube-nocookie.com/embed/sBRbMvTlUok?rel=0" frameborder="0" allowfullscreen></iframe>
    </div>
    
  </div>

  <script>
    const titles = [
      "Mounir Calisthenics",
      "Flow & Rhythmus",
      "Endurance Vibes",
      "Street Battle",
      "8x30s Burpees Engine",
      "Mindset & 3 Säulen",
      "Präsenz & Körpersprache"
    ];
    let currentIdx = 0;
    
    const dotsContainer = document.getElementById('dots');
    for(let i=0; i<7; i++) {
      let d = document.createElement('div');
      d.className = 'dot' + (i===0?' active':'');
      d.onclick = () => goTo(i);
      dotsContainer.appendChild(d);
    }
    
    function goTo(idx) {
      currentIdx = idx;
      document.body.setAttribute('data-section', idx);
      
      // Update dots
      document.querySelectorAll('.dot').forEach((d, i) => {
        d.className = 'dot' + (i===idx ? ' active' : '');
      });
      
      // Update Title
      const titleEl = document.getElementById('title-display');
      titleEl.style.opacity = 0;
      setTimeout(() => {
        titleEl.textContent = titles[idx];
        titleEl.style.opacity = 1;
      }, 500);
      
      // Update drawer
      document.querySelectorAll('.drawer-content').forEach(el => el.classList.remove('active'));
      document.querySelector(`.drawer-content[data-idx="${idx}"]`).classList.add('active');
    }
    
    function toggleDrawer() {
      document.body.classList.toggle('drawer-open');
    }
    
    // Mouse wheel scrolling
    let isScrolling = false;
    window.addEventListener('wheel', (e) => {
      if(document.body.classList.contains('drawer-open')) return;
      if(isScrolling) return;
      
      if(e.deltaY > 0 && currentIdx < 6) {
        goTo(currentIdx + 1);
        isScrolling = true;
        setTimeout(() => isScrolling = false, 1200);
      } else if (e.deltaY < 0 && currentIdx > 0) {
        goTo(currentIdx - 1);
        isScrolling = true;
        setTimeout(() => isScrolling = false, 1200);
      }
    });
    
    goTo(0);
  </script>
</body>
</html>
""")
