import os
import re
import mutagen.mp3

SCENE_IDS = [
    "scene1_intro",
    "scene2_workflow",
    "scene3_data",
    "scene4_correlation",
    "scene5_model",
    "scene6_conclusion"
]

# Get actual durations
scenes_data = []
current_start = 0

for sid in SCENE_IDS:
    mp3_path = f"app/assets_v2/{sid}.mp3"
    audio = mutagen.mp3.MP3(mp3_path)
    dur = audio.info.length
    scenes_data.append((sid, current_start, dur))
    current_start += dur

total_duration = current_start

def parse_vtt(vtt_path):
    subs = []
    with open(vtt_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
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
audio_tags = ""

# Track index mapping
for i, (sid, g_start, dur) in enumerate(scenes_data):
    # Audio tag
    audio_tags += f'    <audio id="audio{i}" data-start="{g_start:.2f}" data-duration="{dur:.2f}" data-track-index="{i}" src="assets_v2/{sid}.mp3"></audio>\n'
    
    # Subtitles
    vtt_path = f"app/assets_v2/{sid}.vtt"
    subs = parse_vtt(vtt_path)
    for sub in subs:
        t_start = g_start + sub["start"]
        t_end = g_start + sub["end"]
        text = sub["text"].replace('\n', ' ').replace('"', '\\"')
        gsap_sub_commands.append(f"tl.set('#subtitle', {{innerHTML: \"{text}\"}}, {t_start:.3f});")
        gsap_sub_commands.append(f"tl.set('#subtitle', {{innerHTML: \"\"}}, {t_end:.3f});")


html_content = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
  <style>
    body {{ margin: 0; background: #0f172a; color: white; font-family: 'Inter', sans-serif; overflow: hidden; }}
    .scene {{ position: absolute; top: 0; left: 0; width: 1920px; height: 1080px; opacity: 0; visibility: hidden; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
    #stage {{ width: 1920px; height: 1080px; position: relative; background: radial-gradient(circle at center, #1e293b 0%, #0f172a 100%); }}
    #subtitle {{ position: absolute; bottom: 80px; left: 0; width: 1920px; text-align: center; font-size: 56px; font-weight: bold; color: #fbbf24; text-shadow: 0px 4px 10px rgba(0,0,0,0.8); z-index: 100; padding: 0 100px; box-sizing: border-box; line-height: 1.4; }}
    
    .bar-container {{ display: flex; align-items: flex-end; gap: 40px; height: 400px; }}
    .bar-wrapper {{ display: flex; flex-direction: column; align-items: center; gap: 20px; }}
    .bar {{ width: 120px; background: linear-gradient(to top, #6366f1, #a855f7); border-radius: 10px 10px 0 0; height: 0px; }}
    .bar-label {{ font-size: 32px; font-weight: 600; color: #cbd5e1; }}
    
    .scatter {{ position: relative; width: 800px; height: 400px; border-left: 4px solid #475569; border-bottom: 4px solid #475569; }}
    .dot {{ position: absolute; width: 24px; height: 24px; background: #fbbf24; border-radius: 50%; opacity: 0; transform: scale(0); }}
    
    .model-card {{ background: rgba(255,255,255,0.05); padding: 40px; border-radius: 20px; border: 2px solid rgba(255,255,255,0.1); width: 400px; text-align: center; transform: translateY(50px); opacity: 0; }}

    .workflow-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 60px; padding: 40px; }}
    .wf-block {{ background: #1e293b; border: 4px solid #334155; border-radius: 16px; padding: 40px; text-align: center; opacity: 0; transform: scale(0.8); position: relative; width: 350px; }}
    .wf-title {{ font-size: 36px; font-weight: bold; color: #38bdf8; margin-bottom: 20px; }}
    .wf-desc {{ font-size: 24px; color: #94a3b8; }}
    .arrow {{ position: absolute; right: -50px; top: 50%; transform: translateY(-50%); font-size: 40px; color: #475569; opacity: 0; }}
  </style>
</head>
<body>
  <div id="stage" data-composition-id="50-startups-v2" data-start="0" data-duration="{total_duration:.2f}" data-width="1920" data-height="1080">
    
{audio_tags}
    <div id="subtitle"></div>

    <!-- Scene 1: Intro -->
    <div id="scene1" class="scene">
        <h1 id="s1-title" class="text-8xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500 mb-8" style="opacity:0;">50 Startups V2</h1>
        <h2 id="s1-subtitle" class="text-5xl text-slate-300" style="opacity:0;">獲利預測深度分析報告</h2>
    </div>

    <!-- Scene 2: Workflow -->
    <div id="scene2" class="scene">
        <h2 class="text-6xl font-bold mb-16 text-white">CRISP-DM 跨產業資料探勘流程</h2>
        <div class="workflow-grid">
            <div class="wf-block" id="wf1"><div class="wf-title">1. 商業理解</div><div class="wf-desc">定義獲利預測目標</div><div class="arrow" id="arr1">➔</div></div>
            <div class="wf-block" id="wf2"><div class="wf-title">2. 資料理解</div><div class="wf-desc">收集三大支出數據</div><div class="arrow" id="arr2">➔</div></div>
            <div class="wf-block" id="wf3"><div class="wf-title">3. 資料準備</div><div class="wf-desc">清理缺失與獨熱編碼</div></div>
            <div class="wf-block" id="wf4"><div class="wf-title">4. 模型建立</div><div class="wf-desc">訓練多種機器學習</div><div class="arrow" id="arr4">➔</div></div>
            <div class="wf-block" id="wf5"><div class="wf-title">5. 模型評估</div><div class="wf-desc">挑選 R² 最佳模型</div><div class="arrow" id="arr5">➔</div></div>
            <div class="wf-block" id="wf6"><div class="wf-title">6. 模型部署</div><div class="wf-desc">應用於商業決策</div></div>
        </div>
    </div>

    <!-- Scene 3: Data Exploration -->
    <div id="scene3" class="scene">
        <h2 class="text-6xl font-bold mb-20 text-white">關鍵支出分佈</h2>
        <div class="bar-container">
            <div class="bar-wrapper"><div class="bar" id="bar1"></div><div class="bar-label">R&D</div></div>
            <div class="bar-wrapper"><div class="bar" id="bar2"></div><div class="bar-label">Admin</div></div>
            <div class="bar-wrapper"><div class="bar" id="bar3"></div><div class="bar-label">Marketing</div></div>
        </div>
    </div>

    <!-- Scene 4: Correlation -->
    <div id="scene4" class="scene">
        <h2 class="text-6xl font-bold mb-20 text-white">研發支出與獲利高度相關 (97%)</h2>
        <div class="scatter">
            <!-- Generate 40 dots using JS later -->
        </div>
    </div>

    <!-- Scene 5: Modeling -->
    <div id="scene5" class="scene" style="flex-direction: row; gap: 60px;">
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

    <!-- Scene 6: Conclusion -->
    <div id="scene6" class="scene">
        <h2 class="text-7xl font-bold mb-16 text-purple-400">行動建議</h2>
        <ul class="text-5xl space-y-12 text-left w-[1400px]">
            <li class="conc-item opacity-0 transform translate-x-10">✅ <strong>優先分配核心預算至產品研發部門</strong></li>
            <li class="conc-item opacity-0 transform translate-x-10">✅ <strong>盡可能精簡不必要的行政與管理開銷</strong></li>
            <li class="conc-item opacity-0 transform translate-x-10">✅ <strong>行銷費用需建立在優秀產品基礎上發揮乘數效應</strong></li>
        </ul>
    </div>

  </div>

  <script>
    // Scatter Plot Dots
    const scatter = document.querySelector('.scatter');
    for(let i=0; i<40; i++) {{
        const dot = document.createElement('div');
        dot.className = 'dot';
        dot.style.left = (i * 18 + (i*13 % 20)) + 'px';
        dot.style.bottom = (i * 9 + (i*7 % 40)) + 'px';
        scatter.appendChild(dot);
    }}

    const tl = gsap.timeline({{ paused: true }});
    window.__timelines = window.__timelines || {{}};
    window.__timelines["50-startups-v2"] = tl;

    // --- SUBTITLES ---
    {"".join(gsap_sub_commands)}

    // Define scene start times
    const t_s1 = {scenes_data[0][1]};
    const t_s2 = {scenes_data[1][1]};
    const t_s3 = {scenes_data[2][1]};
    const t_s4 = {scenes_data[3][1]};
    const t_s5 = {scenes_data[4][1]};
    const t_s6 = {scenes_data[5][1]};

    // --- ANIMATIONS ---
    
    // Scene 1: Intro
    tl.set("#scene1", {{ visibility: "visible" }}, t_s1);
    tl.to("#scene1", {{ opacity: 1, duration: 1 }}, t_s1);
    tl.fromTo("#s1-title", {{ y: 50 }}, {{ opacity: 1, y: 0, duration: 1.5, ease: "power3.out" }}, t_s1 + 1);
    tl.to("#s1-subtitle", {{ opacity: 1, duration: 1 }}, t_s1 + 2.5);
    tl.to("#scene1", {{ opacity: 0, duration: 1 }}, t_s2 - 1);
    tl.set("#scene1", {{ visibility: "hidden" }}, t_s2);

    // Scene 2: Workflow
    tl.set("#scene2", {{ visibility: "visible" }}, t_s2);
    tl.to("#scene2", {{ opacity: 1, duration: 1 }}, t_s2);
    // Block appearances synced vaguely to duration
    tl.to("#wf1", {{ opacity: 1, scale: 1, borderColor: "#0ea5e9", duration: 0.5 }}, t_s2 + 6);
    tl.to("#arr1", {{ opacity: 1, duration: 0.2 }}, t_s2 + 7.5);
    tl.to("#wf2", {{ opacity: 1, scale: 1, borderColor: "#0ea5e9", duration: 0.5 }}, t_s2 + 8.5);
    tl.to("#arr2", {{ opacity: 1, duration: 0.2 }}, t_s2 + 10);
    tl.to("#wf3", {{ opacity: 1, scale: 1, borderColor: "#0ea5e9", duration: 0.5 }}, t_s2 + 12.5);
    
    tl.to("#wf4", {{ opacity: 1, scale: 1, borderColor: "#0ea5e9", duration: 0.5 }}, t_s2 + 17);
    tl.to("#arr4", {{ opacity: 1, duration: 0.2 }}, t_s2 + 18.5);
    tl.to("#wf5", {{ opacity: 1, scale: 1, borderColor: "#0ea5e9", duration: 0.5 }}, t_s2 + 20.5);
    tl.to("#arr5", {{ opacity: 1, duration: 0.2 }}, t_s2 + 22.5);
    tl.to("#wf6", {{ opacity: 1, scale: 1, borderColor: "#0ea5e9", duration: 0.5 }}, t_s2 + 25.5);
    
    tl.to("#scene2", {{ opacity: 0, scale: 1.2, duration: 1.5, ease: "power2.inOut" }}, t_s3 - 1.5);
    tl.set("#scene2", {{ visibility: "hidden" }}, t_s3);

    // Scene 3: Data
    tl.set("#scene3", {{ visibility: "visible" }}, t_s3);
    tl.to("#scene3", {{ opacity: 1, duration: 1 }}, t_s3);
    tl.to("#bar1", {{ height: 350, duration: 1.5, ease: "power2.out" }}, t_s3 + 12);
    tl.to("#bar2", {{ height: 150, duration: 1.5, ease: "power2.out" }}, t_s3 + 12.5);
    tl.to("#bar3", {{ height: 250, duration: 1.5, ease: "power2.out" }}, t_s3 + 13);
    tl.to("#bar1", {{ backgroundColor: "#facc15", boxShadow: "0 0 40px #facc15", duration: 0.5 }}, t_s3 + 20); // Highlight R&D
    tl.to("#scene3", {{ opacity: 0, duration: 1 }}, t_s4 - 1);
    tl.set("#scene3", {{ visibility: "hidden" }}, t_s4);

    // Scene 4: Correlation
    tl.set("#scene4", {{ visibility: "visible" }}, t_s4);
    tl.fromTo("#scene4", {{ x: 200, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 1.5, ease: "power3.out" }}, t_s4);
    tl.fromTo(".dot", {{ scale: 0 }}, {{ opacity: 1, scale: 1, duration: 0.5, stagger: 0.05, ease: "back.out(1.7)" }}, t_s4 + 8);
    tl.to("#scene4", {{ opacity: 0, y: -200, duration: 1.5, ease: "power3.in" }}, t_s5 - 1.5);
    tl.set("#scene4", {{ visibility: "hidden" }}, t_s5);

    // Scene 5: Modeling
    tl.set("#scene5", {{ visibility: "visible" }}, t_s5);
    tl.to("#scene5", {{ opacity: 1, duration: 1 }}, t_s5);
    tl.fromTo(".model-card", {{ y: 50 }}, {{ opacity: 1, y: 0, duration: 0.8, stagger: 0.3 }}, t_s5 + 4);
    tl.to({{val:0}}, {{ val: 95, duration: 2, onUpdate: function() {{ document.getElementById('mscore1').innerText = Math.round(this.targets()[0].val) + '%'; }} }}, t_s5 + 7);
    tl.to({{val:0}}, {{ val: 95, duration: 2, onUpdate: function() {{ document.getElementById('mscore2').innerText = Math.round(this.targets()[0].val) + '%'; }} }}, t_s5 + 7);
    tl.to({{val:0}}, {{ val: 89, duration: 2, onUpdate: function() {{ document.getElementById('mscore3').innerText = Math.round(this.targets()[0].val) + '%'; }} }}, t_s5 + 7);
    tl.to(["#mcard1", "#mcard2"], {{ scale: 1.1, borderColor: "#4ade80", boxShadow: "0 0 40px rgba(74, 222, 128, 0.4)", duration: 0.5 }}, t_s5 + 13);
    tl.to("#scene5", {{ opacity: 0, duration: 1 }}, t_s6 - 1);
    tl.set("#scene5", {{ visibility: "hidden" }}, t_s6);

    // Scene 6: Conclusion
    tl.set("#scene6", {{ visibility: "visible" }}, t_s6);
    tl.to("#scene6", {{ opacity: 1, duration: 1 }}, t_s6);
    tl.to(".conc-item", {{ opacity: 1, x: 0, duration: 0.8, stagger: 5.5 }}, t_s6 + 4);
    tl.to("#scene6", {{ opacity: 0, duration: 2 }}, {total_duration:.2f} - 2);
    tl.set("#scene6", {{ visibility: "hidden" }}, {total_duration:.2f});

  </script>
</body>
</html>
"""

with open("app/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"index.html successfully generated for V2! Total duration: {total_duration:.2f}s")
