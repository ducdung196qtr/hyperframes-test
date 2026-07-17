"""Render HTML/CSS/GSAP composition to MP4 via Selenium + FFmpeg.

Usage:
    python scripts/render-html-to-video.py index.html output.mp4
    
The HTML file must:
    - Include GSAP via CDN: <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    - Register timelines: window.__timelines = {...}; window.__timelines["main"] = gsap.timeline({paused:true});
    - Use viewport matching output resolution in <meta name="viewport">
    - Not use Date.now(), Math.random(), or network fetches (determinism)

Resolution: auto-detected from <meta name="viewport" content="width=X, height=Y">.
Falls back to 1080x1920 (TikTok 9:16).

Requirements: selenium, Chrome, FFmpeg (on PATH or set FFMPEG_PATH env var).
"""
import os, sys, time, subprocess, json, argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# --- Config ---
FFMPEG = os.environ.get("FFMPEG_PATH", "ffmpeg")
CHROME_BINARY = os.environ.get(
    "CHROME_PATH",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
)
FPS = 30
CRF = 23  # H.264 quality (lower = better, 18-28 range)

def detect_resolution(html_path):
    """Extract viewport size from <meta name='viewport'> in HTML."""
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    import re
    match = re.search(r'content="width=(\d+),\s*height=(\d+)"', content)
    if match:
        return int(match.group(1)), int(match.group(2))
    # Fallback: TikTok 9:16
    return 1080, 1920


def render_html_to_video(html_path, output_path):
    html_path = os.path.abspath(html_path)
    output_path = os.path.abspath(output_path)

    W, H = detect_resolution(html_path)
    print(f"📐 Resolution: {W}×{H}")

    # Setup directories
    workdir = os.path.dirname(output_path) or "."
    frames_dir = os.path.join(workdir, ".frames_tmp")
    os.makedirs(frames_dir, exist_ok=True)

    # Open Chrome
    print("🚀 Launching Chrome...")
    options = Options()
    options.binary_location = CHROME_BINARY
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"--window-size={W},{H}")
    options.add_argument("--force-device-scale-factor=1")

    driver = webdriver.Chrome(options=options)
    file_url = f"file:///{html_path.replace(chr(92), '/')}"
    driver.get(file_url)
    time.sleep(2)

    # Validate GSAP
    has_gsap = driver.execute_script("return typeof gsap !== 'undefined'")
    if not has_gsap:
        driver.quit()
        raise RuntimeError("GSAP not loaded. Include: <script src='...gsap.min.js'></script>")

    # Read duration from composition
    duration = driver.execute_script("""
        const root = document.querySelector('[data-composition-id]');
        return root ? parseFloat(root.getAttribute('data-duration') || '10') : 10;
    """)
    total_frames = int(duration * FPS)
    print(f"⏱️  Duration: {duration}s → {total_frames} frames @ {FPS}fps")

    # Check for __timelines
    has_timelines = driver.execute_script("return window.__timelines && window.__timelines['main']")
    print(f"🎬 GSAP timelines registered: {has_timelines}")

    # Capture frames
    print(f"📸 Capturing {total_frames} frames...")
    for frame in range(total_frames):
        t = frame / FPS

        if has_timelines:
            driver.execute_script(f"window.__timelines['main'].time({t});")

        time.sleep(0.01)
        frame_file = os.path.join(frames_dir, f"frame_{frame:05d}.png")
        driver.save_screenshot(frame_file)

        if frame % max(1, total_frames // 10) == 0:
            pct = int(frame / total_frames * 100)
            print(f"  {pct}% — Frame {frame}/{total_frames}")

    driver.quit()
    print("✅ Frames captured!")

    # Encode with FFmpeg
    print("🎬 Encoding MP4...")
    ffmpeg_cmd = [
        FFMPEG, "-y",
        "-framerate", str(FPS),
        "-i", os.path.join(frames_dir, "frame_%05d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-crf", str(CRF),
        output_path,
    ]

    result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg failed:\n{result.stderr[:800]}")

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    frame_count = len(os.listdir(frames_dir))

    # Cleanup temp frames
    import shutil
    shutil.rmtree(frames_dir)

    print(f"✅ DONE!")
    print(f"   Output: {output_path}")
    print(f"   Size:   {size_mb:.1f} MB")
    print(f"   Frames: {frame_count}")
    print(f"   Res:    {W}×{H} @ {FPS}fps")

    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Render HTML to MP4 video")
    parser.add_argument("html", help="Path to index.html")
    parser.add_argument("output", nargs="?", default="output.mp4", help="Output MP4 path")
    args = parser.parse_args()

    render_html_to_video(args.html, args.output)
