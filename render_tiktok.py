"""Render TikTok video: Selenium frames + FFmpeg video + merge audio."""
import os, time, subprocess, re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import io

# Config
FPS = 30
AUDIO = r"C:\Users\Administrator\script_audio.mp3"
HTML = r"C:\Users\Administrator\hyperframes-test\tiktok_video.html"
FFMPEG = r"C:\Users\Administrator\ffmpeg\bin\ffmpeg.exe"
FRAMES_DIR = r"C:\Users\Administrator\hyperframes-test\frames"
OUTPUT_VIDEO = r"C:\Users\Administrator\hyperframes-test\tiktok_nosound.mp4"
OUTPUT_FINAL = r"C:\Users\Administrator\hyperframes-test\tiktok_final.mp4"

# Get audio duration from ffmpeg
result = subprocess.run(
    [r"C:\Users\Administrator\ffmpeg\bin\ffmpeg.exe", "-i", AUDIO, "-f", "null", "-"],
    capture_output=True, text=True
)
match = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", result.stderr)
if match:
    h, m, s = int(match.group(1)), int(match.group(2)), float(match.group(3))
    duration = h*3600 + m*60 + s
else:
    duration = 15.84  # fallback from earlier measurement
total_frames = int(duration * FPS)
print(f"🎵 Audio: {duration:.2f}s → {total_frames} frames at {FPS}fps")

# Clean frames dir
os.makedirs(FRAMES_DIR, exist_ok=True)
for f in os.listdir(FRAMES_DIR):
    os.remove(os.path.join(FRAMES_DIR, f))

# Chrome
opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--window-size=1080,1920")
opts.add_argument("--disable-gpu")
opts.add_argument("--no-sandbox")
opts.add_argument("--force-device-scale-factor=1")
opts.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

print("🚀 Starting Chrome...")
driver = webdriver.Chrome(options=opts)
driver.get(f"file:///{HTML}")
print("📄 HTML loaded, waiting for GSAP...")
time.sleep(2)

# Capture frames
print(f"📸 Capturing {total_frames} frames...")
capture_start = time.time()

for i in range(total_frames):
    t = i / FPS
    # Advance GSAP to exact time
    driver.execute_script(f"gsap.globalTimeline.time({t})")
    time.sleep(0.005)  # tiny wait for render
    
    # Screenshot → resize to 1080x1920
    screenshot = driver.get_screenshot_as_png()
    img = Image.open(io.BytesIO(screenshot))
    
    # Resize and crop to 1080x1920 (9:16)
    w, h = img.size
    target_ratio = 1080 / 1920  # 0.5625
    current_ratio = w / h
    
    if current_ratio > target_ratio:
        # Too wide — crop width
        new_w = int(h * target_ratio)
        offset = (w - new_w) // 2
        img = img.crop((offset, 0, offset + new_w, h))
    elif current_ratio < target_ratio:
        # Too tall — crop height
        new_h = int(w / target_ratio)
        offset = (h - new_h) // 2
        img = img.crop((0, offset, w, offset + new_h))
    
    img = img.resize((1080, 1920), Image.LANCZOS)
    img.save(os.path.join(FRAMES_DIR, f"frame_{i:05d}.png"), "PNG")
    
    if i % 30 == 0:
        elapsed = time.time() - capture_start
        pct = (i+1) / total_frames * 100
        eta = elapsed / (i+1) * (total_frames - i - 1) if i > 0 else 0
        print(f"  Frame {i+1}/{total_frames} ({pct:.0f}%) — ETA {eta:.0f}s")

driver.quit()
capture_elapsed = time.time() - capture_start
print(f"✅ Frames done in {capture_elapsed:.0f}s ({total_frames/capture_elapsed:.1f} fps)")

# FFmpeg: frames → video
print("🎬 Encoding video (frames → MP4)...")
subprocess.run([
    FFMPEG, "-y",
    "-framerate", str(FPS),
    "-i", os.path.join(FRAMES_DIR, "frame_%05d.png"),
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-preset", "fast",
    "-crf", "23",
    "-vf", "scale=1080:1920",
    OUTPUT_VIDEO
], check=True)
print(f"✅ Video: {OUTPUT_VIDEO}")

# Merge audio + video
print("🔊 Merging audio + video...")
subprocess.run([
    FFMPEG, "-y",
    "-i", OUTPUT_VIDEO,
    "-i", AUDIO,
    "-c:v", "copy",
    "-c:a", "aac",
    "-shortest",
    "-map", "0:v:0",
    "-map", "1:a:0",
    OUTPUT_FINAL
], check=True)

size = os.path.getsize(OUTPUT_FINAL)
print(f"🎉 FINAL: {OUTPUT_FINAL} ({size/1024:.0f} KB)")
