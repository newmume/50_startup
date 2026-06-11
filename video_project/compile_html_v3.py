import os
import re
import mutagen.mp3

SCENE_IDS = [f"slide_{i}" for i in range(1, 12)]

# Get actual durations
scenes_data = []
current_start = 0

for sid in SCENE_IDS:
    mp3_path = f"app/assets_v2/{sid}.mp3"
    if not os.path.exists(mp3_path):
        print(f"Error: {mp3_path} does not exist!")
        exit(1)
    audio = mutagen.mp3.MP3(mp3_path)
    dur = audio.info.length
    scenes_data.append((sid, current_start, dur))
    current_start += dur

total_duration = current_start

def parse_vtt(vtt_path):
    subs = []
    if not os.path.exists(vtt_path):
        print(f"Warning: subtitle path {vtt_path} not found.")
        return subs
    with open(vtt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    current_time = None
    current_text = []
    
    time_regex = re.compile(r"(\d{2}:\d{2}:\d{2}[.,]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[.,]\d{3})")
    
    for line in lines:
        line = line.strip()
        match = time_regex.search(line)
        if match:
            if current_time and current_text:
                subs.append({
                    "start": current_time[0],
                    "end": current_time[1],
                    "text": " ".join(current_text)
                })
                current_text = []
            
            # Parse times
            start_str, end_str = match.groups()
            def time_to_sec(t):
                t = t.replace(',', '.')
                h, m, s = t.split(":")
                return int(h)*3600 + int(m)*60 + float(s)
            current_time = (time_to_sec(start_str), time_to_sec(end_str))
        elif line.isdigit():
            # Skip segment number
            continue
        elif line:
            # Accumulate text line
            current_text.append(line)
            
    # Append the last segment
    if current_time and current_text:
        subs.append({
            "start": current_time[0],
            "end": current_time[1],
            "text": " ".join(current_text)
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

# Setup time constants
time_vars = ""
for i, (sid, g_start, dur) in enumerate(scenes_data):
    time_vars += f"    const t_s{i+1} = {g_start:.2f};\n"
    time_vars += f"    const d_s{i+1} = {dur:.2f};\n"

html_content = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
  <style>
    body {{ margin: 0; background: #0f172a; color: white; font-family: 'Inter', sans-serif; overflow: hidden; }}
    #stage {{ width: 1920px; height: 1080px; position: relative; background: #000; overflow: hidden; }}
    .scene {{ position: absolute; top: 0; left: 0; width: 1920px; height: 1080px; opacity: 0; visibility: hidden; background-size: cover; background-position: center; background-repeat: no-repeat; }}
    #subtitle {{ position: absolute; bottom: 60px; left: 0; width: 1920px; text-align: center; font-size: 46px; font-weight: bold; color: #fbbf24; text-shadow: 0px 4px 10px rgba(0,0,0,0.9); z-index: 100; padding: 0 120px; box-sizing: border-box; line-height: 1.4; letter-spacing: 1px; }}
    
    /* Elegant Glowing Highlight Box */
    .highlight-overlay {{
      position: absolute;
      border: 5px solid #22c55e;
      border-radius: 20px;
      box-shadow: 0 0 25px rgba(34, 197, 94, 0.6), inset 0 0 15px rgba(34, 197, 94, 0.3);
      opacity: 0;
      transform: scale(0.96);
      pointer-events: none;
      box-sizing: border-box;
    }}
    
    /* Circular glow variant */
    .highlight-overlay.circle {{
      border-radius: 50%;
      border-color: #38bdf8;
      box-shadow: 0 0 25px rgba(56, 189, 248, 0.6), inset 0 0 15px rgba(56, 189, 248, 0.3);
    }}
    
    /* Cyan border variant */
    .highlight-overlay.cyan {{
      border-color: #06b6d4;
      box-shadow: 0 0 25px rgba(6, 182, 212, 0.6), inset 0 0 15px rgba(6, 182, 212, 0.3);
    }}

    /* Blue border variant */
    .highlight-overlay.blue {{
      border-color: #3b82f6;
      box-shadow: 0 0 25px rgba(59, 130, 246, 0.6), inset 0 0 15px rgba(59, 130, 246, 0.3);
    }}

    /* Red border variant */
    .highlight-overlay.red {{
      border-color: #ef4444;
      box-shadow: 0 0 25px rgba(239, 68, 68, 0.6), inset 0 0 15px rgba(239, 68, 68, 0.3);
    }}
  </style>
</head>
<body>
  <div id="stage" data-composition-id="50-startups-v3" data-start="0" data-duration="{total_duration:.2f}" data-width="1920" data-height="1080">
    
{audio_tags}
    <div id="subtitle"></div>

    <!-- Slide 1: Intro -->
    <div id="slide1" class="scene" style="background-image: url('assets_v2/slide_1.png');"></div>

    <!-- Slide 2: Background -->
    <div id="slide2" class="scene" style="background-image: url('assets_v2/slide_2.png');">
      <div id="s2-h1" class="highlight-overlay cyan" style="left: 10%; top: 32%; width: 25%; height: 57%; border-radius: 28px;"></div>
      <div id="s2-h2" class="highlight-overlay cyan" style="left: 36.5%; top: 32%; width: 27%; height: 57%; border-radius: 28px;"></div>
      <div id="s2-h3" class="highlight-overlay cyan" style="left: 65%; top: 32%; width: 25%; height: 57%; border-radius: 28px;"></div>
    </div>

    <!-- Slide 3: CRISP-DM Workflow -->
    <div id="slide3" class="scene" style="background-image: url('assets_v2/slide_3.png');">
      <div id="s3-h1" class="highlight-overlay blue" style="left: 14%; top: 48%; width: 22%; height: 16%; border-radius: 16px;"></div>
      <div id="s3-h2" class="highlight-overlay blue" style="left: 23%; top: 72%; width: 22%; height: 16%; border-radius: 16px;"></div>
      <div id="s3-h3" class="highlight-overlay blue" style="left: 36.5%; top: 48%; width: 22%; height: 16%; border-radius: 16px;"></div>
      <div id="s3-h4" class="highlight-overlay blue" style="left: 47%; top: 72%; width: 22%; height: 16%; border-radius: 16px;"></div>
      <div id="s3-h5" class="highlight-overlay blue" style="left: 59.5%; top: 48%; width: 22%; height: 16%; border-radius: 16px;"></div>
      <div id="s3-h6" class="highlight-overlay blue" style="left: 65.5%; top: 72%; width: 20%; height: 16%; border-radius: 16px;"></div>
    </div>

    <!-- Slide 4: Data Profiling (Gauges) -->
    <div id="slide4" class="scene" style="background-image: url('assets_v2/slide_4.png');">
      <div id="s4-h1" class="highlight-overlay circle" style="left: 15.5%; top: 58%; width: 21%; height: 37%;"></div>
      <div id="s4-h2" class="highlight-overlay circle" style="left: 39.5%; top: 58%; width: 21%; height: 37%;"></div>
      <div id="s4-h3" class="highlight-overlay circle" style="left: 63.5%; top: 58%; width: 21%; height: 37%;"></div>
    </div>

    <!-- Slide 5: Data Shape / Pipeline -->
    <div id="slide5" class="scene" style="background-image: url('assets_v2/slide_5.png');">
      <div id="s5-h1" class="highlight-overlay cyan" style="left: 15.5%; top: 67%; width: 22%; height: 26%; border-radius: 16px;"></div>
      <div id="s5-h2" class="highlight-overlay cyan" style="left: 39.5%; top: 67%; width: 22%; height: 26%; border-radius: 16px;"></div>
      <div id="s5-h3" class="highlight-overlay cyan" style="left: 63.5%; top: 67%; width: 22%; height: 26%; border-radius: 16px;"></div>
    </div>

    <!-- Slide 6: Models Comparison Table -->
    <div id="slide6" class="scene" style="background-image: url('assets_v2/slide_6.png');">
      <!-- Gradient Boosting Row Highlight -->
      <div id="s6-h1" class="highlight-overlay" style="left: 16%; top: 38%; width: 68%; height: 12%; border-radius: 12px; border-color: #22c55e;"></div>
      <!-- Random Forest Row -->
      <div id="s6-h2" class="highlight-overlay blue" style="left: 16%; top: 50.5%; width: 68%; height: 11%; border-radius: 12px;"></div>
      <!-- Linear Regression Row -->
      <div id="s6-h3" class="highlight-overlay blue" style="left: 16%; top: 62.0%; width: 68%; height: 11%; border-radius: 12px;"></div>
      <!-- Ridge Row -->
      <div id="s6-h4" class="highlight-overlay blue" style="left: 16%; top: 73.5%; width: 68%; height: 11%; border-radius: 12px;"></div>
    </div>

    <!-- Slide 7: Feature Importance Stacked Bar -->
    <div id="slide7" class="scene" style="background-image: url('assets_v2/slide_7.png');">
      <!-- R&D Spend Bar -->
      <div id="s7-h1" class="highlight-overlay" style="left: 17%; top: 18%; width: 60%; height: 24%; border-radius: 9999px; border-color: #22c55e;"></div>
      <!-- Marketing Spend Bar -->
      <div id="s7-h2" class="highlight-overlay circle" style="left: 77.2%; top: 18.5%; width: 4.8%; height: 23%; border-radius: 12px; border-color: #a855f7; box-shadow: 0 0 25px rgba(168, 85, 247, 0.6);"></div>
      <!-- Admin / State Negligible Bar -->
      <div id="s7-h3" class="highlight-overlay" style="left: 82.2%; top: 18.5%; width: 2.2%; height: 23%; border-radius: 12px; border-color: #94a3b8; box-shadow: 0 0 25px rgba(148, 163, 184, 0.6);"></div>
    </div>

    <!-- Slide 8: Web App / Laptop -->
    <div id="slide8" class="scene" style="background-image: url('assets_v2/slide_8.png');">
      <div id="slide8-h1" class="highlight-overlay cyan" style="left: 16.5%; top: 21.5%; width: 16.5%; height: 26%; border-radius: 20px;"></div>
      <div id="slide8-h2" class="highlight-overlay blue" style="left: 34.5%; top: 14%; width: 31%; height: 49%; border-radius: 16px;"></div>
      <div id="slide8-h3" class="highlight-overlay cyan" style="left: 67%; top: 21.5%; width: 16.5%; height: 26%; border-radius: 20px;"></div>
      <div id="slide8-h4" class="highlight-overlay" style="left: 33.5%; top: 66%; width: 33%; height: 11%; border-radius: 9999px; border-color: #22c55e;"></div>
    </div>

    <!-- Slide 9: Budget Recommendations 1 & 2 -->
    <div id="slide9" class="scene" style="background-image: url('assets_v2/slide_9.png');">
      <div id="s9-h1" class="highlight-overlay" style="left: 17.5%; top: 22.5%; width: 31.5%; height: 59%; border-radius: 36px; border-color: #22c55e;"></div>
      <div id="s9-h2" class="highlight-overlay circle" style="left: 51%; top: 22.5%; width: 31.5%; height: 59%; border-radius: 36px; border-color: #a855f7; box-shadow: 0 0 25px rgba(168, 85, 247, 0.6);"></div>
    </div>

    <!-- Slide 10: Operational Recommendations 3 & 4 -->
    <div id="slide10" class="scene" style="background-image: url('assets_v2/slide_10.png');">
      <div id="s10-h1" class="highlight-overlay blue" style="left: 17.5%; top: 22.5%; width: 31.5%; height: 59%; border-radius: 36px;"></div>
      <div id="s10-h2" class="highlight-overlay red" style="left: 51%; top: 22.5%; width: 31.5%; height: 59%; border-radius: 36px;"></div>
    </div>

    <!-- Slide 11: Growth Equation -->
    <div id="slide11" class="scene" style="background-image: url('assets_v2/slide_11.png');">
      <div id="s11-h1" class="highlight-overlay blue" style="left: 20.8%; top: 41.5%; width: 21.8%; height: 38%; border-radius: 28px;"></div>
      <div id="s11-h2" class="highlight-overlay" style="left: 57.5%; top: 41.5%; width: 21.8%; height: 38%; border-radius: 28px; border-color: #22c55e;"></div>
      <div id="s11-h3" class="highlight-overlay circle" style="left: 43.5%; top: 48%; width: 13%; height: 23%; border-color: #22c55e;"></div>
    </div>

  </div>

  <script>
    const tl = gsap.timeline({{ paused: true }});
    window.__timelines = window.__timelines || {{}};
    window.__timelines["50-startups-v3"] = tl;

    // --- TIMELINES VARIABLES ---
{time_vars}

    // --- SUBTITLES ---
    {"".join(gsap_sub_commands)}

    // --- SCENE 1 (Slide 1) ---
    tl.set("#slide1", {{ visibility: "visible" }}, t_s1);
    tl.fromTo("#slide1", {{ opacity: 0 }}, {{ opacity: 1, duration: 1.0 }}, t_s1);
    tl.to("#slide1", {{ opacity: 0, duration: 1.0 }}, t_s2 - 1.0);
    tl.set("#slide1", {{ visibility: "hidden" }}, t_s2);

    // --- SCENE 2 (Slide 2) ---
    tl.set("#slide2", {{ visibility: "visible" }}, t_s2);
    tl.fromTo("#slide2", {{ opacity: 0, scale: 1.05 }}, {{ opacity: 1, scale: 1.0, duration: 1.0, ease: "power2.out" }}, t_s2);
    // Card highlights matching narration
    // "在商業目標上，我們希望協助創投機構和創業團隊..."
    tl.to("#s2-h1", {{ opacity: 1, scale: 1.0, duration: 0.6 }}, t_s2 + 6.0);
    tl.to("#s2-h1", {{ opacity: 0.4, scale: 0.98, duration: 0.6, repeat: 3, yoyo: true }}, t_s2 + 6.6);
    // "透過深度分析，我們發現研發支出是決定新創公司獲利的絕對主導因素，影響權重達百分之九十三點八..."
    tl.to("#s2-h1", {{ opacity: 0, scale: 0.95, duration: 0.4 }}, t_s2 + 11.5);
    tl.to("#s2-h2", {{ opacity: 1, scale: 1.0, duration: 0.6 }}, t_s2 + 12.0);
    tl.to("#s2-h2", {{ opacity: 0.4, scale: 0.98, duration: 0.6, repeat: 3, yoyo: true }}, t_s2 + 12.6);
    // "最後，我們將這些模型封裝成即時互動的網頁應用，提供決策者進行模擬預測..."
    tl.to("#s2-h2", {{ opacity: 0, scale: 0.95, duration: 0.4 }}, t_s2 + 22.0);
    tl.to("#s2-h3", {{ opacity: 1, scale: 1.0, duration: 0.6 }}, t_s2 + 22.5);
    tl.to("#s2-h3", {{ opacity: 0.4, scale: 0.98, duration: 0.6, repeat: 2, yoyo: true }}, t_s2 + 23.1);
    tl.to("#s2-h3", {{ opacity: 0, scale: 0.95, duration: 0.5 }}, t_s3 - 1.2);
    
    tl.to("#slide2", {{ opacity: 0, duration: 1.0 }}, t_s3 - 1.0);
    tl.set("#slide2", {{ visibility: "hidden" }}, t_s3);

    // --- SCENE 3 (Slide 3) ---
    tl.set("#slide3", {{ visibility: "visible" }}, t_s3);
    tl.fromTo("#slide3", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 1.0, ease: "power2.out" }}, t_s3);
    // Step highlights matching narration:
    // "第一步，商業理解..."
    tl.to("#s3-h1", {{ opacity: 1, scale: 1.0, duration: 0.5 }}, t_s3 + 8.5);
    // "第二步，資料理解..."
    tl.to("#s3-h1", {{ opacity: 0, duration: 0.3 }}, t_s3 + 12.0);
    tl.to("#s3-h2", {{ opacity: 1, scale: 1.0, duration: 0.5 }}, t_s3 + 12.5);
    // "第三步，資料準備..."
    tl.to("#s3-h2", {{ opacity: 0, duration: 0.3 }}, t_s3 + 16.0);
    tl.to("#s3-h3", {{ opacity: 1, scale: 1.0, duration: 0.5 }}, t_s3 + 16.5);
    // "第四步，建模..."
    tl.to("#s3-h3", {{ opacity: 0, duration: 0.3 }}, t_s3 + 20.0);
    tl.to("#s3-h4", {{ opacity: 1, scale: 1.0, duration: 0.5 }}, t_s3 + 20.5);
    // "第五步，評估..."
    tl.to("#s3-h4", {{ opacity: 0, duration: 0.3 }}, t_s3 + 24.0);
    tl.to("#s3-h5", {{ opacity: 1, scale: 1.0, duration: 0.5 }}, t_s3 + 24.5);
    // "以及第六步，部署..."
    tl.to("#s3-h5", {{ opacity: 0, duration: 0.3 }}, t_s3 + 28.0);
    tl.to("#s3-h6", {{ opacity: 1, scale: 1.0, duration: 0.5 }}, t_s3 + 28.5);
    tl.to("#s3-h6", {{ opacity: 0, duration: 0.5 }}, t_s4 - 1.2);
    
    tl.to("#slide3", {{ opacity: 0, duration: 1.0 }}, t_s4 - 1.0);
    tl.set("#slide3", {{ visibility: "hidden" }}, t_s4);

    // --- SCENE 4 (Slide 4) ---
    tl.set("#slide4", {{ visibility: "visible" }}, t_s4);
    tl.fromTo("#slide4", {{ opacity: 0, scale: 0.95 }}, {{ opacity: 1, scale: 1.0, duration: 1.0, ease: "power2.out" }}, t_s4);
    // Gauge highlights:
    // "研發支出與利潤的相關係數高達零點九七三..."
    tl.to("#s4-h1", {{ opacity: 1, scale: 1.0, duration: 0.5 }}, t_s4 + 11.0);
    tl.to("#s4-h1", {{ opacity: 0.5, duration: 0.5, repeat: 2, yoyo: true }}, t_s4 + 11.5);
    // "行銷支出與利潤為零點七四八..."
    tl.to("#s4-h1", {{ opacity: 0, duration: 0.3 }}, t_s4 + 18.0);
    tl.to("#s4-h2", {{ opacity: 1, scale: 1.0, duration: 0.5 }}, t_s4 + 18.5);
    tl.to("#s4-h2", {{ opacity: 0.5, duration: 0.5, repeat: 2, yoyo: true }}, t_s4 + 19.0);
    // "而行政支出與利潤的相關係數僅有零點二零一..."
    tl.to("#s4-h2", {{ opacity: 0, duration: 0.3 }}, t_s4 + 23.5);
    tl.to("#s4-h3", {{ opacity: 1, scale: 1.0, duration: 0.5 }}, t_s4 + 24.0);
    tl.to("#s4-h3", {{ opacity: 0.5, duration: 0.5, repeat: 2, yoyo: true }}, t_s4 + 24.5);
    tl.to("#s4-h3", {{ opacity: 0, duration: 0.5 }}, t_s5 - 1.2);

    tl.to("#slide4", {{ opacity: 0, duration: 1.0 }}, t_s5 - 1.0);
    tl.set("#slide4", {{ visibility: "hidden" }}, t_s5);

    // --- SCENE 5 (Slide 5) ---
    tl.set("#slide5", {{ visibility: "visible" }}, t_s5);
    tl.fromTo("#slide5", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 1.0, ease: "power2.out" }}, t_s5);
    // Preprocessing step highlights:
    // "第一，對類別特徵「地區州別」進行獨熱編碼..."
    tl.to("#s5-h1", {{ opacity: 1, scale: 1.0, duration: 0.5 }}, t_s5 + 6.0);
    // "第二，使用標準化縮放對研發、行政與行銷支出進行標準化處理..."
    tl.to("#s5-h1", {{ opacity: 0, duration: 0.3 }}, t_s5 + 13.5);
    tl.to("#s5-h2", {{ opacity: 1, scale: 1.0, duration: 0.5 }}, t_s5 + 14.0);
    // "第三，以八比二的比例將數據隨機分割..."
    tl.to("#s5-h2", {{ opacity: 0, duration: 0.3 }}, t_s5 + 23.5);
    tl.to("#s5-h3", {{ opacity: 1, scale: 1.0, duration: 0.5 }}, t_s5 + 24.0);
    tl.to("#s5-h3", {{ opacity: 0, duration: 0.5 }}, t_s6 - 1.2);

    tl.to("#slide5", {{ opacity: 0, duration: 1.0 }}, t_s6 - 1.0);
    tl.set("#slide5", {{ visibility: "hidden" }}, t_s6);

    // --- SCENE 6 (Slide 6) ---
    tl.set("#slide6", {{ visibility: "visible" }}, t_s6);
    tl.fromTo("#slide6", {{ opacity: 0, y: -30 }}, {{ opacity: 1, y: 0, duration: 1.0, ease: "power2.out" }}, t_s6);
    // Highlight Gradient Boosting (Champion Row)
    // "評估結果顯示，梯度提升回歸模型以零點九三五四的決定係數奪下冠軍..."
    tl.to("#s6-h1", {{ opacity: 1, scale: 1.0, duration: 0.5 }}, t_s6 + 8.0);
    tl.to("#s6-h1", {{ opacity: 0.4, duration: 0.6, repeat: 3, yoyo: true }}, t_s6 + 8.5);
    // "隨機森林回歸次之..."
    tl.to("#s6-h1", {{ opacity: 0.8, duration: 0.3 }}, t_s6 + 18.0);
    tl.to("#s6-h2", {{ opacity: 1, scale: 1.0, duration: 0.5 }}, t_s6 + 18.5);
    // "而傳統的線性回歸與脊回歸表現稍遜..."
    tl.to("#s6-h2", {{ opacity: 0, duration: 0.3 }}, t_s6 + 21.0);
    tl.to(["#s6-h3", "#s6-h4"], {{ opacity: 1, scale: 1.0, duration: 0.5, stagger: 0.3 }}, t_s6 + 21.5);
    tl.to(["#s6-h3", "#s6-h4", "#s6-h1"], {{ opacity: 0, duration: 0.5 }}, t_s7 - 1.2);

    tl.to("#slide6", {{ opacity: 0, duration: 1.0 }}, t_s7 - 1.0);
    tl.set("#slide6", {{ visibility: "hidden" }}, t_s7);

    // --- SCENE 7 (Slide 7) ---
    tl.set("#slide7", {{ visibility: "visible" }}, t_s7);
    tl.fromTo("#slide7", {{ opacity: 0, scale: 1.05 }}, {{ opacity: 1, scale: 1.0, duration: 1.0, ease: "power2.out" }}, t_s7);
    // Horizontal Bar highlights:
    // "研發支出的影響權重高達百分之九十三點八..."
    tl.to("#s7-h1", {{ opacity: 1, scale: 1.0, duration: 0.5 }}, t_s7 + 7.5);
    tl.to("#s7-h1", {{ opacity: 0.4, duration: 0.6, repeat: 3, yoyo: true }}, t_s7 + 8.0);
    // "相較之下，行銷支出只佔了百分之五點零五..."
    tl.to("#s7-h1", {{ opacity: 0, duration: 0.3 }}, t_s7 + 16.0);
    tl.to("#s7-h2", {{ opacity: 1, scale: 1.0, duration: 0.5 }}, t_s7 + 16.5);
    // "行政管理費僅佔百分之零點五九，而地理州別的總權重更低於百分之零點五六..."
    tl.to("#s7-h2", {{ opacity: 0, duration: 0.3 }}, t_s7 + 19.5);
    tl.to("#s7-h3", {{ opacity: 1, scale: 1.0, duration: 0.5 }}, t_s7 + 20.0);
    tl.to("#s7-h3", {{ opacity: 0, duration: 0.5 }}, t_s8 - 1.2);

    tl.to("#slide7", {{ opacity: 0, duration: 1.0 }}, t_s8 - 1.0);
    tl.set("#slide7", {{ visibility: "hidden" }}, t_s8);

    // --- SCENE 8 (Slide 8) ---
    tl.set("#slide8", {{ visibility: "visible" }}, t_s8);
    tl.fromTo("#slide8", {{ opacity: 0, x: 30 }}, {{ opacity: 1, x: 0, duration: 1.0, ease: "power2.out" }}, t_s8);
    // Pipeline and Web App highlights:
    // "將整個機器學習流程與最佳模型封裝成 Pipeline，並序列化為 best model dot pkl..."
    tl.to("#slide8-h1", {{ opacity: 1, scale: 1.0, duration: 0.5 }}, t_s8 + 4.0);
    // "接著，我們結合 Streamlit 前端框架，開發出即時互動的預測網頁應用程式..."
    tl.to("#slide8-h1", {{ opacity: 0, duration: 0.3 }}, t_s8 + 9.5);
    tl.to("#slide8-h2", {{ opacity: 1, scale: 1.0, duration: 0.5 }}, t_s8 + 10.0);
    tl.to("#slide8-h3", {{ opacity: 1, scale: 1.0, duration: 0.5 }}, t_s8 + 12.0);
    // "用戶可以在介面上隨意拖動三大支出滑桿，即可即時獲得由梯度提升模型算出的獲利預測值..."
    tl.to(["#slide8-h2", "#slide8-h3"], {{ opacity: 0.3, duration: 0.4 }}, t_s8 + 16.0);
    tl.to("#slide8-h4", {{ opacity: 1, scale: 1.0, duration: 0.5 }}, t_s8 + 16.5);
    tl.to(["#slide8-h2", "#slide8-h3", "#slide8-h4"], {{ opacity: 0, duration: 0.5 }}, t_s9 - 1.2);

    tl.to("#slide8", {{ opacity: 0, duration: 1.0 }}, t_s9 - 1.0);
    tl.set("#slide8", {{ visibility: "hidden" }}, t_s9);

    // --- SCENE 9 (Slide 9) ---
    tl.set("#slide9", {{ visibility: "visible" }}, t_s9);
    tl.fromTo("#slide9", {{ opacity: 0, scale: 0.95 }}, {{ opacity: 1, scale: 1.0, duration: 1.0, ease: "power2.out" }}, t_s9);
    // Highlight Rec 1 and Rec 2:
    // "第一，極大化研發投入..."
    tl.to("#s9-h1", {{ opacity: 1, scale: 1.0, duration: 0.5 }}, t_s9 + 7.5);
    tl.to("#s9-h1", {{ opacity: 0.4, duration: 0.6, repeat: 3, yoyo: true }}, t_s9 + 8.0);
    // "第二，戰略性佈局行銷..."
    tl.to("#s9-h1", {{ opacity: 0, duration: 0.3 }}, t_s9 + 19.5);
    tl.to("#s9-h2", {{ opacity: 1, scale: 1.0, duration: 0.5 }}, t_s9 + 20.0);
    tl.to("#s9-h2", {{ opacity: 0.4, duration: 0.6, repeat: 2, yoyo: true }}, t_s9 + 20.5);
    tl.to("#s9-h2", {{ opacity: 0, duration: 0.5 }}, t_s10 - 1.2);

    tl.to("#slide9", {{ opacity: 0, duration: 1.0 }}, t_s10 - 1.0);
    tl.set("#slide9", {{ visibility: "hidden" }}, t_s10);

    // --- SCENE 10 (Slide 10) ---
    tl.set("#slide10", {{ visibility: "visible" }}, t_s10);
    tl.fromTo("#slide10", {{ opacity: 0, scale: 0.95 }}, {{ opacity: 1, scale: 1.0, duration: 1.0, ease: "power2.out" }}, t_s10);
    // Highlight Rec 3 and Rec 4:
    // "第三，精簡行政開銷..."
    tl.to("#s10-h1", {{ opacity: 1, scale: 1.0, duration: 0.5 }}, t_s10 + 4.5);
    tl.to("#s10-h1", {{ opacity: 0.4, duration: 0.6, repeat: 2, yoyo: true }}, t_s10 + 5.0);
    // "第四，忽略地點迷思..."
    tl.to("#s10-h1", {{ opacity: 0, duration: 0.3 }}, t_s10 + 13.0);
    tl.to("#s10-h2", {{ opacity: 1, scale: 1.0, duration: 0.5 }}, t_s10 + 13.5);
    tl.to("#s10-h2", {{ opacity: 0.4, duration: 0.6, repeat: 2, yoyo: true }}, t_s10 + 14.0);
    tl.to("#s10-h2", {{ opacity: 0, duration: 0.5 }}, t_s11 - 1.2);

    tl.to("#slide10", {{ opacity: 0, duration: 1.0 }}, t_s11 - 1.0);
    tl.set("#slide10", {{ visibility: "hidden" }}, t_s11);

    // --- SCENE 11 (Slide 11) ---
    tl.set("#slide11", {{ visibility: "visible" }}, t_s11);
    tl.fromTo("#slide11", {{ opacity: 0, scale: 1.05 }}, {{ opacity: 1, scale: 1.0, duration: 1.0, ease: "power2.out" }}, t_s11);
    // Highlight elements:
    // "解開不確定性轉化為精準的預測引擎..."
    tl.to("#s11-h1", {{ opacity: 1, scale: 1.0, duration: 0.6 }}, t_s11 + 6.0);
    tl.to("#s11-h3", {{ opacity: 1, scale: 1.0, duration: 0.6 }}, t_s11 + 10.0);
    tl.to("#s11-h2", {{ opacity: 1, scale: 1.0, duration: 0.6 }}, t_s11 + 12.0);
    
    tl.to(["#s11-h1", "#s11-h2", "#s11-h3"], {{ opacity: 0.5, duration: 1.0 }}, t_s11 + 20.0);
    tl.to("#slide11", {{ opacity: 0, duration: 2.0 }}, {total_duration:.2f} - 2.0);
    tl.set("#slide11", {{ visibility: "hidden" }}, {total_duration:.2f});

  </script>
</body>
</html>
"""

with open("app/index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"index.html successfully generated for V3! Total duration: {total_duration:.2f}s")
