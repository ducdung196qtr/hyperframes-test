
"""HyperFrames Deconstructed Render — 12s audio-synced"""
import os, time, subprocess

PROJ = r"C:\Users\Administrator\hyperframes-test"
FFMPEG = r"C:\Users\Administrator\ffmpeg\bin\ffmpeg.exe"
AUDIO_TTS = r"C:\Users\Administrator\script_audio_final.mp3"
SFX_DIR = os.path.join(PROJ, "assets", "sfx")
FRAMES_DIR = os.path.join(PROJ, "frames")
HTML_FILE = os.path.join(PROJ, "index.html")
VIDEO_NOSOUND = os.path.join(PROJ, "deconstructed_nosound.mp4")
VIDEO_FINAL = os.path.join(PROJ, "deconstructed_final.mp4")
AUDIO_TTS = r"C:\Users\Administrator\script_audio_final.mp3"
FPS = 30
DURATION = 34.0
TOTAL_FRAMES = 1020
W, H = 1080, 1920

os.makedirs(FRAMES_DIR, exist_ok=True)
for f in os.listdir(FRAMES_DIR):
    os.remove(os.path.join(FRAMES_DIR, f))

print(f"=== RENDER: {TOTAL_FRAMES} frames, {W}x{H}, 12.0s ===")

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument("--headless")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-gpu")
opts.add_argument(f"--window-size={W},{H}")
opts.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

driver = webdriver.Chrome(options=opts)
driver.set_window_size(W, H)
driver.get(f"file:///{HTML_FILE.replace(os.sep, '/')}")
time.sleep(5)

t0 = time.time()
for i in range(TOTAL_FRAMES):
    t = i / FPS
    driver.execute_script(f"window.seekTo({t});")
    png = driver.get_screenshot_as_png()
    with open(os.path.join(FRAMES_DIR, f"frame_{i:05d}.png"), "wb") as f:
        f.write(png)
    if i % (TOTAL_FRAMES // 10) == 0 or i == TOTAL_FRAMES - 1:
        el = time.time() - t0
        fps = (i+1)/el if el>0 else 0
        pct = (i+1)/TOTAL_FRAMES*100
        eta = (TOTAL_FRAMES-i-1)/fps if fps>0 else 0
        print(f"  [{i}/{TOTAL_FRAMES}] {pct:.0f}% | {fps:.1f}fps | ETA {eta:.0f}s")

driver.quit()
el = time.time()-t0
print(f"\n✅ {TOTAL_FRAMES} frames in {el:.0f}s ({TOTAL_FRAMES/el:.1f}fps)")

# Encode
print("\n[2/3] Encoding...")
subprocess.run([
    FFMPEG, "-y", "-framerate", str(FPS),
    "-i", os.path.join(FRAMES_DIR, "frame_%05d.png"),
    "-c:v", "libx264", "-preset", "ultrafast", "-crf", "22",
    "-pix_fmt", "yuv420p", VIDEO_NOSOUND
], check=True, timeout=300)
print(f"  {os.path.getsize(VIDEO_NOSOUND)/1024:.0f} KB")

# Mix audio + SFX (sync'd to 12s)
print("\n[3/3] Mixing TTS + SFX...")
# Updated SFX timing for 12s
sfx_cues = [
    ("impact-bass-1", 0.0, 0.35),    # Opening
    ("glitch-1", 2.7, 0.3),           # "NHƯNG" twist
    ("pop", 5.4, 0.35),               # BREAKING badge
    ("impact-bass-2", 6.8, 0.35),     # "20 AI" shock  
    ("whoosh-short", 8.4, 0.3),       # Quote transition
    ("chime", 11.0, 0.35),            # CTA ending
]

inputs = ["-i", VIDEO_NOSOUND, "-i", AUDIO_TTS]
filter_parts = ["[1:a]volume=1.0[tts]"]
mix_inputs = ["[tts]"]

for idx, (name, start_s, vol) in enumerate(sfx_cues):
    spath = os.path.join(SFX_DIR, f"{name}.mp3")
    if not os.path.exists(spath):
        print(f"  SKIP {name}: not found")
        continue
    inputs.extend(["-i", spath])
    pad = int(start_s * 1000)
    filter_parts.append(f"[{idx+2}:a]adelay={pad}|{pad},volume={vol}[sfx{idx}]")
    mix_inputs.append(f"[sfx{idx}]")

filter_parts.append(f"{''.join(mix_inputs)}amix=inputs={len(mix_inputs)}:duration=longest:dropout_transition=2[audio]")

cmd = [FFMPEG, "-y"] + inputs + [
    "-filter_complex", ";".join(filter_parts),
    "-map", "0:v:0", "-map", "[audio]",
    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
    "-shortest", VIDEO_FINAL
]
subprocess.run(cmd, check=True, timeout=120)

print(f"\n🎉 DONE: {os.path.getsize(VIDEO_FINAL)/1024:.0f} KB")
print(f"   {VIDEO_FINAL}")
