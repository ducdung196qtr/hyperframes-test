"""HTML-to-video renderer using Selenium + FFmpeg — HyperFrames-inspired pipeline."""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import subprocess, time, os, json

FRAMES_DIR = r"C:\Users\Administrator\hyperframes-test\frames"
VIDEO_OUT = r"C:\Users\Administrator\hyperframes-test\renders\demo.mp4"

os.makedirs(FRAMES_DIR, exist_ok=True)
os.makedirs(os.path.dirname(VIDEO_OUT), exist_ok=True)

# Use file:// protocol — no server needed
html_file = r"C:\Users\Administrator\hyperframes-test\index.html"

options = Options()
options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1080,1920")
options.add_argument("--force-device-scale-factor=1")

FFMPEG = r"C:\Users\Administrator\ffmpeg\bin\ffmpeg.exe"

print("🚀 Launching Chrome...")
driver = webdriver.Chrome(options=options)
driver.get(f"file:///{html_file.replace(chr(92), '/')}")
time.sleep(2)

# Check GSAP loaded
has_gsap = driver.execute_script("return typeof gsap !== 'undefined'")
print(f"GSAP loaded: {has_gsap}")

# Advance timeline manually
duration = 8.0
fps = 30
total_frames = int(duration * fps)

print(f"📸 Capturing {total_frames} frames...")
for frame in range(total_frames):
    t = frame / fps
    # Set GSAP timeline to time t
    driver.execute_script(f"""
        if(window.__timelines && window.__timelines['main']) {{
            window.__timelines['main'].time({t});
        }}
    """)
    time.sleep(0.01)  # Let DOM update
    
    frame_file = os.path.join(FRAMES_DIR, f"frame_{frame:05d}.png")
    driver.save_screenshot(frame_file)
    
    if frame % 30 == 0:
        print(f"  Frame {frame}/{total_frames}")

driver.quit()
print("✅ Frames captured!")

# Encode video with FFmpeg
print("🎬 Encoding MP4...")
ffmpeg_cmd = [
    FFMPEG, "-y",
    "-framerate", str(fps),
    "-i", os.path.join(FRAMES_DIR, "frame_%05d.png"),
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-preset", "fast",
    "-crf", "23",
    VIDEO_OUT
]

result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
if result.returncode == 0:
    size_mb = os.path.getsize(VIDEO_OUT) / (1024*1024)
    print(f"✅ DONE! Video: {VIDEO_OUT} ({size_mb:.1f} MB)")
else:
    print(f"FFmpeg error:\n{result.stderr[:500]}")

# Cleanup frames (optional — keep for debugging)
# import shutil; shutil.rmtree(FRAMES_DIR)
