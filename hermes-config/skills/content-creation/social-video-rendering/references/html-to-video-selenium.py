"""
HTML-to-Video renderer — HyperFrames-compatible fallback using Selenium + FFmpeg.
Use when HyperFrames CLI can't launch its bundled headless Chrome (e.g. Chrome 109 on
Windows Server 2012, or any platform where chrome-headless-shell download fails).

The HTML composition follows HyperFrames conventions:
  - data-start / data-duration / data-track-index on timed elements
  - class="clip" on every timed element
  - window.__timelines["main"] = gsap.timeline({ paused: true })

This script captures frames via Selenium's save_screenshot(), then encodes with FFmpeg.
GSAP timelines are seeked manually for each frame.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import subprocess, time, os, json

# --- Config ---
HTML_FILE = r"index.html"
OUTPUT_MP4 = r"renders/output.mp4"
FRAMES_DIR = r"frames"
DURATION = 10.0      # seconds — must match data-duration on root
FPS = 30
TOTAL_FRAMES = int(DURATION * FPS)

CHROME_BINARY = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
FFMPEG_BINARY = r"ffmpeg"  # or absolute path like r"C:\Users\Administrator\ffmpeg\bin\ffmpeg.exe"

COMPOSITION_WIDTH = 1080
COMPOSITION_HEIGHT = 1920
# --- End Config ---

os.makedirs(FRAMES_DIR, exist_ok=True)
os.makedirs(os.path.dirname(OUTPUT_MP4), exist_ok=True)

options = Options()
options.binary_location = CHROME_BINARY
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument(f"--window-size={COMPOSITION_WIDTH},{COMPOSITION_HEIGHT}")
options.add_argument("--force-device-scale-factor=1")

print(f"🚀 Launching Chrome from: {CHROME_BINARY}")
driver = webdriver.Chrome(options=options)

html_escaped = HTML_FILE.replace('\\', '/')
driver.get(f"file:///{html_escaped}")
time.sleep(2)

# Verify GSAP is loaded
has_gsap = driver.execute_script("return typeof gsap !== 'undefined'")
print(f"GSAP loaded: {has_gsap}")
if not has_gsap:
    print("⚠️  GSAP not found — check your <script> tag in index.html")

print(f"📸 Capturing {TOTAL_FRAMES} frames at {FPS}fps ({DURATION}s)...")
for frame in range(TOTAL_FRAMES):
    t = frame / FPS
    driver.execute_script(f"""
        if(window.__timelines && window.__timelines['main']) {{
            window.__timelines['main'].time({t});
        }}
    """)
    time.sleep(0.01)  # Let DOM paint

    frame_file = os.path.join(FRAMES_DIR, f"frame_{frame:05d}.png")
    driver.save_screenshot(frame_file)

    if frame % 30 == 0:
        print(f"  Frame {frame}/{TOTAL_FRAMES}")

driver.quit()
print("✅ Frames captured!")

# Encode video with FFmpeg
print("🎬 Encoding MP4...")
ffmpeg_cmd = [
    FFMPEG_BINARY, "-y",
    "-framerate", str(FPS),
    "-i", os.path.join(FRAMES_DIR, "frame_%05d.png"),
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-preset", "fast",
    "-crf", "23",
    OUTPUT_MP4,
]

result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
if result.returncode == 0:
    size_mb = os.path.getsize(OUTPUT_MP4) / (1024 * 1024)
    print(f"✅ DONE! Video: {OUTPUT_MP4} ({size_mb:.1f} MB)")
else:
    print(f"❌ FFmpeg error:\n{result.stderr[:500]}")
