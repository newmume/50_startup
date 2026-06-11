import os
import re

SCENES = [
    ("scene1_intro", 0, 11.90),
    ("scene2_data", 12, 12.96),
    ("scene3_correlation", 25, 13.90),
    ("scene4_model", 39, 13.70),
    ("scene5_conclusion", 53, 15.34)
]

def parse_vtt(vtt_path):
    subs = []
    with open(vtt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 00:00:00.100 --> 00:00:00.600
    pattern = re.compile(r"(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})\n(.*?)\n", re.DOTALL)
    
    for match in pattern.finditer(content):
        start_str, end_str, text = match.groups()
        
        def time_to_sec(t):
            h, m, s = t.split(":")
            return int(h)*3600 + int(m)*60 + float(s)
            
        subs.append({
            "start": time_to_sec(start_str),
            "end": time_to_sec(end_str),
            "text": text.strip()
        })
    return subs

gsap_sub_commands = []
for scene_id, global_start, duration in SCENES:
    vtt_path = f"app/assets/{scene_id}.vtt"
    subs = parse_vtt(vtt_path)
    # The subtitles in VTT are relative to the audio file. We add global_start.
    for sub in subs:
        t_start = global_start + sub["start"]
        t_end = global_start + sub["end"]
        text = sub["text"].replace('\n', ' ').replace('"', '\\"')
        gsap_sub_commands.append(f"tl.set('#subtitle', {{innerHTML: \"{text}\"}}, {t_start});")
        gsap_sub_commands.append(f"tl.set('#subtitle', {{innerHTML: \"\"}}, {t_end});")

html_content = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
  <style>
    body {{ margin: 0; background: #0f172a; color: white; font-family: 'Inter', sans-serif; overflow: hidden; }}
    .scene {{ position: absolute; top: 0; left: 0; width: 1920px; height: 1080px; opacity: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
    #stage {{ width: 1920px; height: 1080px; position: relative; background: radial-gradient(circle at center, #1e293b 0%, #0f172a 100%); }}
    #subtitle {{ position: absolute; bottom: 80px; left: 0; width: 1920px; text-align: center; font-size: 56px; font-weight: bold; color: #fbbf24; text-shadow: 0px 4px 10px rgba(0,0,0,0.8); z-index: 100; }}
    
    .bar-container {{ display: flex; align-items: flex-end; gap: 40px; height: 400px; }}
    .bar-wrapper {{ display: flex; flex-direction: column; align-items: center; gap: 20px; }}
    .bar {{ width: 120px; background: linear-gradient(to top, #6366f1, #a855f7); border-radius: 10px 10px 0 0; height: 0px; }}
    .bar-label {{ font-size: 32px; font-weight: 600; color: #cbd5e1; }}
    
    .scatter {{ position: relative; width: 800px; height: 400px; border-left: 4px solid #475569; border-bottom: 4px solid #475569; }}
    .dot {{ position: absolute; width: 24px; height: 24px; background: #fbbf24; border-radius: 50%; opacity: 0; transform: scale(0); }}
    
    .model-card {{ background: rgba(255,255,255,0.05); padding: 40px; border-radius: 20px; border: 2px solid rgba(255,255,255,0.1); width: 400px; text-align: center; transform: translateY(50px); opacity: 0; }}
  </style>
</head>
<body>
  <div id="stage" data-composition-id="50-startups" data-start="0" data-duration="69" data-width="1920" data-height="1080">
    
    <!-- Audio tracks -->
    <audio id="audio0" data-start="0" data-duration="12" data-track-index="0" src="assets/scene1_intro.mp3"></audio>
    <audio id="audio1" data-start="12" data-duration="13" data-track-index="1" src="assets/scene2_data.mp3"></audio>
    <audio id="audio2" data-start="25" data-duration="14" data-track-index="2" src="assets/scene3_correlation.mp3"></audio>
    <audio id="audio3" data-start="39" data-duration="14" data-track-index="3" src="assets/scene4_model.mp3"></audio>
    <audio id="audio4" data-start="53" data-duration="16" data-track-index="4" src="assets/scene5_conclusion.mp3"></audio>

    <div id="subtitle"></div>

    <!-- Scene 1: Intro -->
    <div id="scene1" class="scene">
        <h1 id="s1-title" class="text-8xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500 mb-8" style="opacity:0;">50 Startups</h1>
        <h2 id="s1-subtitle" class="text-5xl text-slate-300" style="opacity:0;">獲利預測分析報告</h2>
    </div>

    <!-- Scene 2: Data Exploration -->
    <div id="scene2" class="scene">
        <h2 class="text-6xl font-bold mb-20 text-white">關鍵支出分佈</h2>
        <div class="bar-container">
            <div class="bar-wrapper"><div class="bar" id="bar1"></div><div class="bar-label">R&D</div></div>
            <div class="bar-wrapper"><div class="bar" id="bar2"></div><div class="bar-label">Admin</div></div>
            <div class="bar-wrapper"><div class="bar" id="bar3"></div><div class="bar-label">Marketing</div></div>
        </div>
    </div>

    <!-- Scene 3: Correlation -->
    <div id="scene3" class="scene">
        <h2 class="text-6xl font-bold mb-20 text-white">研發支出與獲利高度相關 (97%)</h2>
        <div class="scatter">
            <!-- Generate 20 dots using JS later -->
        </div>
    </div>

    <!-- Scene 4: Modeling -->
    <div id="scene4" class="scene" style="flex-direction: row; gap: 60px;">
        <div class="model-card" id="mcard1" style="opacity: 0;">
            <h3 class="text-4xl text-slate-300 mb-4">Linear Regression</h3>
            <div class="text-7xl font-bold text-green-400" id="mscore1">0%</div>
        </div>
        <div class="model-card" id="mcard2" style="opacity: 0;">
            <h3 class="text-4xl text-slate-300 mb-4">Ridge</h3>
            <div class="text-7xl font-bold text-green-400" id="mscore2">0%</div>
        </div>
        <div class="model-card" id="mcard3" style="opacity: 0;">
            <h3 class="text-4xl text-slate-300 mb-4">Random Forest</h3>
            <div class="text-7xl font-bold text-yellow-400" id="mscore3">0%</div>
        </div>
    </div>

    <!-- Scene 5: Conclusion -->
    <div id="scene5" class="scene">
        <h2 class="text-7xl font-bold mb-16 text-purple-400">行動建議</h2>
        <ul class="text-5xl space-y-12 text-left w-[1200px]">
            <li class="conc-item opacity-0 transform translate-x-10">✅ <strong>優先分配預算至 R&D</strong></li>
            <li class="conc-item opacity-0 transform translate-x-10">✅ <strong>精簡不必要的行政開銷</strong></li>
            <li class="conc-item opacity-0 transform translate-x-10">✅ <strong>將行銷作為良好產品的加速器</strong></li>
        </ul>
    </div>

  </div>

  <script>
    // Scatter Plot Dots
    const scatter = document.querySelector('.scatter');
    for(let i=0; i<20; i++) {{
        const dot = document.createElement('div');
        dot.className = 'dot';
        dot.style.left = (i * 38 + (i*13 % 20)) + 'px';
        dot.style.bottom = (i * 18 + (i*7 % 40)) + 'px';
        scatter.appendChild(dot);
    }}

    const tl = gsap.timeline({{ paused: true }});
    window.__timelines = window.__timelines || {{}};
    window.__timelines["50-startups"] = tl;

    // --- SUBTITLES ---
    {"".join(gsap_sub_commands)}

    // --- ANIMATIONS ---
    // Scene 1 (0 to 12s)
    tl.to("#scene1", {{ opacity: 1, duration: 1 }}, 0);
    tl.fromTo("#s1-title", {{ y: 50 }}, {{ opacity: 1, y: 0, duration: 1.5, ease: "power3.out" }}, 1);
    tl.to("#s1-subtitle", {{ opacity: 1, duration: 1 }}, 2.5);
    tl.to("#scene1", {{ opacity: 0, duration: 1 }}, 11);
    tl.set("#scene1", {{ visibility: "hidden" }}, 12);

    // Scene 2 (12s to 25s)
    tl.to("#scene2", {{ opacity: 1, duration: 1 }}, 12);
    // Animate bars growing
    tl.to("#bar1", {{ height: 350, duration: 1.5, ease: "power2.out" }}, 14);
    tl.to("#bar2", {{ height: 150, duration: 1.5, ease: "power2.out" }}, 14.5);
    tl.to("#bar3", {{ height: 250, duration: 1.5, ease: "power2.out" }}, 15);
    tl.to("#bar1", {{ backgroundColor: "#facc15", boxShadow: "0 0 30px #facc15", duration: 0.5 }}, 19); // Highlight R&D
    tl.to("#scene2", {{ opacity: 0, duration: 1 }}, 24);
    tl.set("#scene2", {{ visibility: "hidden" }}, 25);

    // Scene 3 (25s to 39s)
    tl.to("#scene3", {{ opacity: 1, duration: 1 }}, 25);
    tl.fromTo(".dot", {{ scale: 0 }}, {{ opacity: 1, scale: 1, duration: 0.5, stagger: 0.1, ease: "back.out(1.7)" }}, 27);
    tl.to("#scene3", {{ opacity: 0, duration: 1 }}, 38);
    tl.set("#scene3", {{ visibility: "hidden" }}, 39);

    // Scene 4 (39s to 53s)
    tl.to("#scene4", {{ opacity: 1, duration: 1 }}, 39);
    tl.fromTo(".model-card", {{ y: 50 }}, {{ opacity: 1, y: 0, duration: 0.8, stagger: 0.3 }}, 40);
    // Animate score counters
    tl.to({{val:0}}, {{ val: 95, duration: 2, onUpdate: function() {{ document.getElementById('mscore1').innerText = Math.round(this.targets()[0].val) + '%'; }} }}, 42);
    tl.to({{val:0}}, {{ val: 95, duration: 2, onUpdate: function() {{ document.getElementById('mscore2').innerText = Math.round(this.targets()[0].val) + '%'; }} }}, 42);
    tl.to({{val:0}}, {{ val: 89, duration: 2, onUpdate: function() {{ document.getElementById('mscore3').innerText = Math.round(this.targets()[0].val) + '%'; }} }}, 42);
    
    // Highlight best models
    tl.to(["#mcard1", "#mcard2"], {{ scale: 1.1, borderColor: "#4ade80", boxShadow: "0 0 40px rgba(74, 222, 128, 0.4)", duration: 0.5 }}, 45);
    tl.to("#scene4", {{ opacity: 0, duration: 1 }}, 52);
    tl.set("#scene4", {{ visibility: "hidden" }}, 53);

    // Scene 5 (53s to 69s)
    tl.to("#scene5", {{ opacity: 1, duration: 1 }}, 53);
    tl.to(".conc-item", {{ opacity: 1, x: 0, duration: 0.8, stagger: 2.5 }}, 54.5);
    tl.to("#scene5", {{ opacity: 0, duration: 2 }}, 67);
    tl.set("#scene5", {{ visibility: "hidden" }}, 69);

  </script>
</body>
</html>
"""

with open("app/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
print("index.html successfully generated with synced subtitles and GSAP timeline!")
