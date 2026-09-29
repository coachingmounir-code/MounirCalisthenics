import math
import random

# Configuration
N = 45 # 45 shards for richer graphics

shapes_info = [
    # (id, title, bg_color, shard_color)
    ("start", "MOUNIR CALISTHENICS", "#1a1a2e", "#e94560"),
    ("flow", "FLOW & RHYTHMUS", "#16213e", "#0f3460"),
    ("beach", "ENDURANCE VIBES", "#f9a826", "#e15f41"),
    ("battle", "STREET BATTLE", "#2c3e50", "#e74c3c"),
    ("burpees", "BURPEES ENGINE", "#c0392b", "#f1c40f"),
    ("mindset", "MINDSET SÄULEN", "#00b894", "#ffeaa7"),
    ("presence", "PRÄSENZ & WIRKUNG", "#2d3436", "#00cec9")
]

# Shape functions (return True if point is inside the shape)
def shape_M(x, y):
    if 15 <= x <= 30 and 15 <= y <= 85: return True
    if 70 <= x <= 85 and 15 <= y <= 85: return True
    if 30 <= x <= 50 and 15 <= y <= 60 and abs(y - (x * 1.5 - 30)) < 15: return True
    if 50 <= x <= 70 and 15 <= y <= 60 and abs(y - ((100-x) * 1.5 - 30)) < 15: return True
    return False

def shape_diamond(x, y): return abs(x - 50) + abs(y - 50) < 40

def shape_sun(x, y):
    r = math.hypot(x-50, y-50)
    if r < 20: return True
    if 25 < r < 45 and math.cos(math.atan2(y-50, x-50) * 8) > 0.5: return True
    return False

def shape_X(x, y): return abs(x - y) < 15 or abs(x - (100 - y)) < 15

def shape_lightning(x, y):
    if 35 <= x <= 65 and 5 <= y <= 50: return True
    if 45 <= x <= 75 and 45 <= y <= 95: return True
    return False

def shape_pyramid(x, y):
    if 20 <= y <= 90:
        w = (y - 20) * 0.7
        if 50 - w <= x <= 50 + w: return True
    return False

def shape_eye(x, y):
    dy = abs(y - 50)
    max_dy = 28 * (1 - ((x-50)/45)**2)
    if 5 <= x <= 95 and dy < max_dy:
        if math.hypot(x-50, y-50) < 12: return False # pupil
        return True
    return False

funcs = [shape_M, shape_diamond, shape_sun, shape_X, shape_lightning, shape_pyramid, shape_eye]

random.seed(12345)
all_shapes = []
for f in funcs:
    tris = []
    # To get better coverage, we'll generate points on a grid and check
    # if they are in the shape.
    points_in_shape = []
    for x in range(0, 101, 5):
        for y in range(0, 101, 5):
            if f(x, y):
                points_in_shape.append((x,y))
                
    while len(tris) < N:
        if points_in_shape:
            cx, cy = random.choice(points_in_shape)
        else:
            cx, cy = random.uniform(20, 80), random.uniform(20, 80)
            
        size = random.uniform(10, 25)
        angle = random.uniform(0, 6.28)
        p1 = (cx + size * math.cos(angle), cy + size * math.sin(angle))
        p2 = (cx + size * math.cos(angle + 2.09), cy + size * math.sin(angle + 2.09))
        p3 = (cx + size * math.cos(angle + 4.18), cy + size * math.sin(angle + 4.18))
        
        p1 = (max(0,min(100,p1[0])), max(0,min(100,p1[1])))
        p2 = (max(0,min(100,p2[0])), max(0,min(100,p2[1])))
        p3 = (max(0,min(100,p3[0])), max(0,min(100,p3[1])))
        tris.append([p1, p2, p3])
    all_shapes.append(tris)

css_vars = []
for s_idx, (s_name, _, _, _) in enumerate(shapes_info):
    for i, tri in enumerate(all_shapes[s_idx]):
        pts = f"{tri[0][0]:.2f}% {tri[0][1]:.2f}%, {tri[1][0]:.2f}% {tri[1][1]:.2f}%, {tri[2][0]:.2f}% {tri[2][1]:.2f}%"
        css_vars.append(f"  --{s_name}-{i}: polygon({pts});")

css_rules = []
for s_idx, (s_name, _, bg_col, fg_col) in enumerate(shapes_info):
    css_rules.append(f"body[data-section='{s_idx}'] {{ background-color: {bg_col}; }}")
    # Using specific shard colors per section
    css_rules.append(f"body[data-section='{s_idx}'] .shard {{ background-color: {fg_col}; }}")
    for i in range(N):
        css_rules.append(f"body[data-section='{s_idx}'] .shard-{i} {{ clip-path: var(--{s_name}-{i}); }}")

html_content = f"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mounir Calisthenics</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
  <script src="https://unpkg.com/lucide@latest"></script>
  <style>
    :root {{
{chr(10).join(css_vars)}
    }}
    
    body {{
      margin: 0; padding: 0; overflow: hidden;
      font-family: 'Inter', sans-serif;
      transition: background-color 1.2s cubic-bezier(0.86, 0, 0.07, 1);
      color: #fff;
    }}

    h1, h2, h3, .oswald {{ font-family: 'Oswald', sans-serif; text-transform: uppercase; }}
    
    /* Graphic Container */
    #graphic-container {{
      position: absolute; top: 50%; left: calc(50% - 200px);
      transform: translate(-50%, -50%);
      width: 500px; height: 500px;
      pointer-events: none; z-index: 10;
      transition: left 0.8s cubic-bezier(0.86, 0, 0.07, 1);
    }}
    
    /* When drawer opens, shift graphic left */
    body.drawer-open #graphic-container {{
      left: calc(30%);
    }}
    
    .shard {{
      position: absolute; top: 0; left: 0;
      width: 100%; height: 100%;
      transition: clip-path 1.2s cubic-bezier(0.86, 0, 0.07, 1), background-color 1.2s ease;
      opacity: 0.85; mix-blend-mode: hard-light;
    }}
    
{chr(10).join(css_rules)}
    
    /* Navigation UI */
    #ui {{
      position: absolute; top: 0; left: 0; width: 100%; height: 100%;
      pointer-events: none; z-index: 20;
    }}
    
    .nav-dots {{
      position: absolute; left: 40px; top: 50%;
      transform: translateY(-50%);
      display: flex; flex-direction: column; gap: 20px;
      pointer-events: auto;
    }}
    .dot {{
      width: 10px; height: 10px; border-radius: 50%;
      background: rgba(255,255,255,0.2);
      cursor: pointer; transition: all 0.4s;
      position: relative;
    }}
    .dot::after {{
      content: attr(data-title);
      position: absolute; left: 25px; top: 50%; transform: translateY(-50%);
      white-space: nowrap; font-size: 11px; letter-spacing: 2px;
      opacity: 0; transition: opacity 0.3s; pointer-events: none;
      text-transform: uppercase; font-family: 'Oswald', sans-serif;
    }}
    .dot:hover::after {{ opacity: 1; }}
    .dot.active {{ background: #fff; transform: scale(1.5); }}
    .dot.active::after {{ opacity: 1; }}
    
    #title-display {{
      position: absolute; bottom: 80px; left: calc(50% - 200px);
      transform: translateX(-50%);
      font-size: 40px; font-weight: 700; letter-spacing: 6px;
      text-transform: uppercase; font-family: 'Oswald', sans-serif;
      opacity: 0; transition: opacity 0.5s, left 0.8s cubic-bezier(0.86, 0, 0.07, 1);
      white-space: nowrap;
    }}
    body.drawer-open #title-display {{ left: calc(30%); }}
    
    .btn-explore {{
      position: absolute; right: 0; top: 50%; transform: translateY(-50%);
      background: #fff; color: #111; padding: 25px 40px;
      font-size: 16px; font-weight: bold; cursor: pointer;
      pointer-events: auto; border: none; letter-spacing: 3px;
      text-transform: uppercase; font-family: 'Oswald', sans-serif;
      transition: background 0.3s, right 0.8s cubic-bezier(0.86, 0, 0.07, 1);
      clip-path: polygon(15px 0, 100% 0, 100% 100%, 0 100%);
    }}
    .btn-explore:hover {{ background: #f0f0f0; padding-right: 50px; }}
    
    /* Side Panel */
    #drawer {{
      position: absolute; top: 0; right: -700px;
      width: 700px; height: 100%;
      background: #ffffff; color: #111;
      transition: right 0.8s cubic-bezier(0.86, 0, 0.07, 1);
      z-index: 30; pointer-events: auto;
      overflow-y: auto;
      box-shadow: -15px 0 50px rgba(0,0,0,0.4);
    }}
    body.drawer-open #drawer {{ right: 0; }}
    body.drawer-open .btn-explore {{ right: 700px; }}
    
    .drawer-content {{ display: none; padding: 80px 60px; }}
    .drawer-content.active {{ display: block; animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; }}
    
    @keyframes slideUp {{
      from {{ opacity: 0; transform: translateY(40px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .close-btn {{
      position: absolute; top: 30px; right: 40px;
      background: none; border: none; cursor: pointer;
      color: #111; padding: 10px; z-index: 50;
    }}
    .close-btn:hover {{ opacity: 0.5; }}
  </style>
</head>
<body data-section="0">

  <div id="graphic-container">
"""
for i in range(N):
    html_content += f'    <div class="shard shard-{i}"></div>\n'
    
html_content += """  </div>
  
  <div id="ui">
    <div class="nav-dots" id="dots"></div>
    <div id="title-display">MOUNIR CALISTHENICS</div>
    <button class="btn-explore" onclick="toggleDrawer()">EXPLORE <i data-lucide="chevron-right" class="inline w-5 h-5 ml-2 -mt-1"></i></button>
  </div>
  
  <!-- Content Drawer -->
  <div id="drawer">
    <button class="close-btn" onclick="toggleDrawer()"><i data-lucide="x" class="w-8 h-8"></i></button>
    
    <!-- 0. Start -->
    <div class="drawer-content" data-idx="0">
      <div class="text-sm font-bold tracking-widest text-gray-400 mb-4 oswald">00. PROTOCOL</div>
      <h2 class="text-6xl font-bold mb-8 tracking-tighter">MOUNIR<br>CALISTHENICS</h2>
      <p class="text-xl text-gray-600 leading-relaxed mb-8">
        Kraft, Rhythmus, stählerne Disziplin und maximale Körperspannung.
        Dies ist dein offizieller Trainings-Leitfaden.
      </p>
      <div class="border-t border-gray-200 pt-8 mt-8">
        <h3 class="text-xl font-bold mb-4 oswald">Was dich erwartet:</h3>
        <ul class="space-y-4 text-gray-600">
          <li class="flex items-center gap-3"><i data-lucide="play-circle" class="w-5 h-5 text-black"></i> 3 Core Videos (Flow, Endurance, Battle)</li>
          <li class="flex items-center gap-3"><i data-lucide="timer" class="w-5 h-5 text-black"></i> 8x30s Burpees Intervall-Engine</li>
          <li class="flex items-center gap-3"><i data-lucide="brain" class="w-5 h-5 text-black"></i> Mindset & Sportleridentität (3 Säulen)</li>
          <li class="flex items-center gap-3"><i data-lucide="user" class="w-5 h-5 text-black"></i> Präsenz & Körpersprache</li>
        </ul>
      </div>
    </div>
    
    <!-- 1. Flow -->
    <div class="drawer-content" data-idx="1">
      <div class="text-sm font-bold tracking-widest text-gray-400 mb-4 oswald">01. STAGE MEDIA</div>
      <h2 class="text-5xl font-bold mb-6 tracking-tighter">FLOW & RHYTHMUS</h2>
      <p class="text-lg text-gray-600 mb-8">
        Das erste Video für Mounirs Ablauf: Starte mit Fokus auf Koordination, Rhythmusgefühl und fließende Bewegung.
      </p>
      <div class="aspect-video bg-black rounded-lg overflow-hidden shadow-2xl">
        <iframe width="100%" height="100%" src="https://www.youtube-nocookie.com/embed/g9FJhH9dOeU?rel=0" frameborder="0" allowfullscreen></iframe>
      </div>
      <p class="text-sm text-gray-400 mt-4 uppercase tracking-widest text-center">Mike Song • It Runs Through Me</p>
    </div>
    
    <!-- 2. Beach -->
    <div class="drawer-content" data-idx="2">
      <div class="text-sm font-bold tracking-widest text-gray-400 mb-4 oswald">02. STAGE MEDIA</div>
      <h2 class="text-5xl font-bold mb-6 tracking-tighter">ENDURANCE VIBES</h2>
      <p class="text-lg text-gray-600 mb-8">
        Zweites Video im Ablauf: Den richtigen Beat und die Leichtigkeit mitnehmen. Schaffe dir die ideale Trainingsatmosphäre.
      </p>
      <div class="aspect-video bg-black rounded-lg overflow-hidden shadow-2xl">
        <iframe width="100%" height="100%" src="https://www.youtube-nocookie.com/embed/ja2dGXXmFV4?rel=0" frameborder="0" allowfullscreen></iframe>
      </div>
      <p class="text-sm text-gray-400 mt-4 uppercase tracking-widest text-center">Chris Luno • Beach House</p>
    </div>
    
    <!-- 3. Battle -->
    <div class="drawer-content" data-idx="3">
      <div class="text-sm font-bold tracking-widest text-gray-400 mb-4 oswald">03. STAGE MEDIA</div>
      <h2 class="text-5xl font-bold mb-6 tracking-tighter">STREET BATTLE</h2>
      <p class="text-lg text-gray-600 mb-8">
        Die Essenz von reinem Calisthenics – Bars, Dips, Muscle-Ups und der unerbittliche Wettkampfgeist im Park.
      </p>
      <div class="aspect-video bg-black rounded-lg overflow-hidden shadow-2xl">
        <iframe width="100%" height="100%" src="https://www.youtube-nocookie.com/embed/UMYm2cBjZIY?rel=0" frameborder="0" allowfullscreen></iframe>
      </div>
      <p class="text-sm text-gray-400 mt-4 uppercase tracking-widest text-center">NYC Street Workout Showdown</p>
    </div>
    
    <!-- 4. Burpees -->
    <div class="drawer-content" data-idx="4">
      <div class="text-sm font-bold tracking-widest text-gray-400 mb-4 oswald">04. CORE ENGINE</div>
      <h2 class="text-6xl font-bold mb-2 tracking-tighter">BURPEES</h2>
      <p class="text-xl text-red-600 font-bold mb-8 oswald tracking-wide">8 RUNDEN × 30 SEKUNDEN</p>
      
      <div class="bg-gray-50 border border-gray-200 rounded-xl p-8 text-center shadow-lg">
        <div class="flex justify-between items-center mb-6 oswald text-gray-500 tracking-widest">
          <span id="timerStatus">READY</span>
          <span id="roundDisplay">ROUND 1/8</span>
        </div>
        
        <div id="timeRemaining" class="text-7xl font-bold tracking-tighter mb-8 oswald text-gray-900">
          00:30
        </div>
        
        <div class="w-full bg-gray-200 h-2 mb-8 rounded-full overflow-hidden">
          <div id="timerProgress" class="h-full bg-red-600 w-full transition-all duration-300"></div>
        </div>
        
        <div class="flex justify-center gap-4">
          <button id="startTimerBtn" onclick="toggleTimer()" class="bg-red-600 text-white px-8 py-4 rounded font-bold oswald tracking-widest hover:bg-red-700 transition-colors w-full">START</button>
          <button onclick="resetTimer()" class="bg-gray-200 text-gray-700 px-6 py-4 rounded hover:bg-gray-300 transition-colors"><i data-lucide="rotate-ccw"></i></button>
        </div>
      </div>
      
      <div class="mt-8 flex flex-col gap-4">
        <div class="flex items-center gap-3 text-gray-600 font-semibold"><i data-lucide="check-circle-2" class="text-green-500"></i> Brust berührt den Boden</div>
        <div class="flex items-center gap-3 text-gray-600 font-semibold"><i data-lucide="check-circle-2" class="text-green-500"></i> Voller Strecksprung oben</div>
      </div>
    </div>
    
    <!-- 5. Mindset -->
    <div class="drawer-content" data-idx="5">
      <div class="text-sm font-bold tracking-widest text-gray-400 mb-4 oswald">05. ATHLETE CORE</div>
      <h2 class="text-5xl font-bold mb-10 tracking-tighter">3 SÄULEN DER IDENTITÄT</h2>
      
      <div class="space-y-8">
        <div class="bg-gray-50 p-6 rounded-lg border-l-4 border-blue-500">
          <h3 class="text-2xl font-bold mb-2 oswald">1. Disziplin & Fokus</h3>
          <p class="text-gray-600">Kein Zaudern, keine Ausreden. Dein Geist lenkt deinen Körper. Jeder Moment gehört deinem Ziel.</p>
        </div>
        
        <div class="bg-gray-50 p-6 rounded-lg border-l-4 border-blue-500">
          <h3 class="text-2xl font-bold mb-2 oswald">2. Maximale Körperspannung</h3>
          <p class="text-gray-600">Jede Wiederholung in perfekter Ausführung. Calisthenics-Kontrolle von den Fingerspitzen bis zu den Zehen.</p>
        </div>
        
        <div class="bg-gray-50 p-6 rounded-lg border-l-4 border-blue-500">
          <h3 class="text-2xl font-bold mb-2 oswald">3. Unaufhaltsamer Wille</h3>
          <p class="text-gray-600">Wenn die Muskeln brennen, fängt der Satz erst an. Ein wahrer Athlet gibt niemals auf.</p>
        </div>
      </div>
      
      <button onclick="speakAllPillars()" class="mt-10 w-full bg-blue-600 text-white px-8 py-5 rounded font-bold oswald tracking-widest hover:bg-blue-700 transition-colors flex justify-center items-center gap-3">
        <i data-lucide="volume-2"></i> ALLE 3 LAUT AUFSAGEN
      </button>
    </div>
    
    <!-- 6. Presence -->
    <div class="drawer-content" data-idx="6">
      <div class="text-sm font-bold tracking-widest text-gray-400 mb-4 oswald">06. PRESENCE & FORM</div>
      <h2 class="text-5xl font-bold mb-6 tracking-tighter">KÖRPERSPRACHE</h2>
      <p class="text-lg text-gray-600 mb-8">
        Präsenz, Haltung, Mimik und Gestik – wie du dich trägst, definiert deine innere Stärke und Wirkung.
      </p>
      <div class="aspect-video bg-black rounded-lg overflow-hidden shadow-2xl">
        <iframe width="100%" height="100%" src="https://www.youtube-nocookie.com/embed/sBRbMvTlUok?rel=0" frameborder="0" allowfullscreen></iframe>
      </div>
      
      <div class="mt-8 space-y-4 text-gray-600 font-semibold">
        <div class="flex items-center gap-3"><div class="w-2 h-2 bg-black rounded-full"></div> Aufrechte Haltung, offene Brust</div>
        <div class="flex items-center gap-3"><div class="w-2 h-2 bg-black rounded-full"></div> Ruhiger Blickkontakt</div>
        <div class="flex items-center gap-3"><div class="w-2 h-2 bg-black rounded-full"></div> Souveräne, präzise Gestik</div>
      </div>
    </div>
    
  </div>

  <script>
    lucide.createIcons();
    
    const titles = [
      "MOUNIR CALISTHENICS",
      "FLOW & RHYTHMUS",
      "ENDURANCE VIBES",
      "STREET BATTLE",
      "BURPEES ENGINE",
      "MINDSET SÄULEN",
      "PRÄSENZ & WIRKUNG"
    ];
    let currentIdx = 0;
    
    const dotsContainer = document.getElementById('dots');
    for(let i=0; i<7; i++) {{
      let d = document.createElement('div');
      d.className = 'dot' + (i===0?' active':'');
      d.setAttribute('data-title', titles[i]);
      d.onclick = () => goTo(i);
      dotsContainer.appendChild(d);
    }}
    
    function goTo(idx) {{
      currentIdx = idx;
      document.body.setAttribute('data-section', idx);
      
      document.querySelectorAll('.dot').forEach((d, i) => {{
        d.className = 'dot' + (i===idx ? ' active' : '');
      }});
      
      const titleEl = document.getElementById('title-display');
      titleEl.style.opacity = 0;
      setTimeout(() => {{
        titleEl.textContent = titles[idx];
        titleEl.style.opacity = 1;
      }}, 400);
      
      document.querySelectorAll('.drawer-content').forEach(el => el.classList.remove('active'));
      document.querySelector(`.drawer-content[data-idx="${{idx}}"]`).classList.add('active');
    }}
    
    function toggleDrawer() {{
      document.body.classList.toggle('drawer-open');
    }}
    
    // Smooth scrolling
    let isScrolling = false;
    window.addEventListener('wheel', (e) => {{
      if(document.body.classList.contains('drawer-open')) return;
      if(isScrolling) return;
      if(Math.abs(e.deltaY) < 30) return; // threshold
      
      if(e.deltaY > 0 && currentIdx < 6) {{
        goTo(currentIdx + 1);
        isScrolling = true;
        setTimeout(() => isScrolling = false, 1200);
      }} else if (e.deltaY < 0 && currentIdx > 0) {{
        goTo(currentIdx - 1);
        isScrolling = true;
        setTimeout(() => isScrolling = false, 1200);
      }}
    }});
    
    // Key bindings
    window.addEventListener('keydown', (e) => {{
      if(document.body.classList.contains('drawer-open')) {{
        if(e.key === 'Escape') toggleDrawer();
        return;
      }}
      if(e.key === 'ArrowDown' || e.key === 'ArrowRight') {{
        if(currentIdx < 6) goTo(currentIdx + 1);
      }}
      if(e.key === 'ArrowUp' || e.key === 'ArrowLeft') {{
        if(currentIdx > 0) goTo(currentIdx - 1);
      }}
    }});

    // Timer Logic
    const TOTAL_ROUNDS = 8;
    const WORK_SECONDS = 30;
    const REST_SECONDS = 15;
    let currentRound = 1, isWorking = true, timeLeft = WORK_SECONDS, timerInterval = null, isRunning = false;
    
    const roundDisplay = document.getElementById('roundDisplay');
    const timeRemaining = document.getElementById('timeRemaining');
    const timerProgress = document.getElementById('timerProgress');
    const timerStatus = document.getElementById('timerStatus');
    const startTimerBtn = document.getElementById('startTimerBtn');
    
    function playBeep(freq, duration) {{
      const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'sine'; osc.frequency.value = freq;
      gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
      osc.connect(gain); gain.connect(audioCtx.destination);
      osc.start(); osc.stop(audioCtx.currentTime + duration);
    }}
    
    function updateDisplay() {{
      timeRemaining.textContent = `00:${{timeLeft.toString().padStart(2, '0')}}`;
      timerProgress.style.width = `${{(timeLeft / (isWorking ? WORK_SECONDS : REST_SECONDS)) * 100}}%`;
      if(isWorking) {{
        timerStatus.textContent = "WORK";
        timerStatus.className = "text-red-600 font-bold";
        timerProgress.className = "h-full bg-red-600 w-full transition-all duration-300";
      }} else {{
        timerStatus.textContent = "REST";
        timerStatus.className = "text-blue-500 font-bold";
        timerProgress.className = "h-full bg-blue-500 w-full transition-all duration-300";
      }}
      roundDisplay.textContent = `ROUND ${{currentRound}}/${{TOTAL_ROUNDS}}`;
    }}
    
    function toggleTimer() {{
      if(isRunning) {{
        clearInterval(timerInterval); isRunning = false; startTimerBtn.textContent = 'RESUME';
      }} else {{
        isRunning = true; startTimerBtn.textContent = 'PAUSE'; playBeep(880, 0.2);
        timerInterval = setInterval(() => {{
          if(timeLeft > 0) {{
            timeLeft--;
            if(timeLeft <= 3 && timeLeft > 0) playBeep(520, 0.1);
            updateDisplay();
          }} else {{
            if(isWorking) {{
              playBeep(1050, 0.35);
              if(currentRound >= TOTAL_ROUNDS) {{
                clearInterval(timerInterval); isRunning = false;
                startTimerBtn.textContent = 'DONE!'; timerStatus.textContent = "FINISHED";
                timeRemaining.textContent = "00:00"; return;
              }}
              isWorking = false; timeLeft = REST_SECONDS;
            }} else {{
              playBeep(920, 0.25);
              isWorking = true; currentRound++; timeLeft = WORK_SECONDS;
            }}
            updateDisplay();
          }}
        }}, 1000);
      }}
    }}
    
    function resetTimer() {{
      clearInterval(timerInterval); isRunning = false; isWorking = true;
      currentRound = 1; timeLeft = WORK_SECONDS; startTimerBtn.textContent = 'START';
      updateDisplay();
    }}
    
    // Speech Logic
    function speakAllPillars() {{
      const text = "Mounirs drei Säulen der Sportleridentität. Erstens: Eiserne Disziplin und Fokus. Zweitens: Maximale Körperspannung und perfekte Form. Drittens: Unaufhaltsamer Wille, keine Ausreden!";
      if ('speechSynthesis' in window) {{
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'de-DE';
        window.speechSynthesis.speak(utterance);
      }} else {{ alert(text); }}
    }}
    
    goTo(0);
  </script>
</body>
</html>
"""

with open('index.html', 'w') as f:
    f.write(html_content)

