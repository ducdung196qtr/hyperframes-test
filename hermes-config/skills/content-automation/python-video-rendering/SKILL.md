---
name: python-video-rendering
description: Render videos programmatically with Python (Pillow + moviepy). TikTok, YouTube Shorts, news clips—any frame-based video generation. Covers FFmpeg setup via imageio_ffmpeg (no system install needed), frame creation patterns, audio generation, and common pitfalls.
---

# Python Video Rendering

Use Python to render videos from scratch: generate frames with Pillow, assemble with moviepy, and encode with FFmpeg. Ideal for automated content pipelines (TikTok, Shorts, news clips).

## When to use
- User asks to "render a video" or "create a TikTok/Short"
- Automated video generation from data (news, stats, charts)
- Any frame-by-frame animation without a GUI video editor

## Prerequisites

```bash
pip install pillow moviepy numpy
```

moviepy pulls `imageio_ffmpeg` which provides a **bundled FFmpeg binary** — no system install needed.

## Finding FFmpeg

```python
import imageio_ffmpeg
ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
# e.g. C:\...\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe
```

Use this path explicitly when moviepy asks, or let moviepy auto-detect it.

## Frame generation pattern

```python
from PIL import Image, ImageDraw, ImageFont
import numpy as np

W, H = 1080, 1920  # TikTok 9:16
FRAMES_PER_SEGMENT = 60  # 2s at 30fps
FPS = 30

all_frames = []
for f in range(FRAMES_PER_SEGMENT):
    img = Image.new('RGB', (W, H), '#1a1a2e')
    draw = ImageDraw.Draw(img)
    # ... draw text, shapes, gradients ...
    all_frames.append(np.array(img))
```

**Performance tip**: Use `Image.new('RGB', ...)` instead of RGBA unless you need alpha. Converting RGBA→RGB every frame is slow.

## Assembling the clip

```python
from moviepy import ImageSequenceClip

clip = ImageSequenceClip(all_frames, fps=FPS)
clip.write_videofile("output.mp4", fps=FPS, codec='libx264',
                     audio_codec='aac', preset='fast',
                     bitrate='5000k', ffmpeg_params=['-pix_fmt', 'yuv420p'])
clip.close()
```

## Audio

Generate a simple tone with numpy (or use a real audio file):

```python
sample_rate = 44100
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
audio = 0.3 * np.sin(2 * np.pi * freq * t)
# Apply fade envelope
fade_samples = int(0.05 * sample_rate)
audio[:fade_samples] *= np.linspace(0, 1, fade_samples)
audio[-fade_samples:] *= np.linspace(1, 0, fade_samples)

from moviepy import AudioArrayClip
audio_clip = AudioArrayClip(np.column_stack([audio, audio]), fps=sample_rate)
clip = clip.with_audio(audio_clip)
```

## TikTok standard dimensions

| Platform | Resolution | Aspect |
|----------|-----------|--------|
| TikTok / Reels / Shorts | 1080×1920 | 9:16 |
| YouTube | 1920×1080 | 16:9 |
| Square (Instagram) | 1080×1080 | 1:1 |

## Pitfalls

1. **`imageio_ffmpeg` not found after moviepy install**: Moviepy 2.x bundles it; check `pip show imageio_ffmpeg`. If missing, `pip install imageio_ffmpeg`.
2. **Out of memory on long videos**: Don't accumulate all frames in a list for >1-minute videos. Write frames as image files and use `ImageSequenceClip` with a file pattern instead.
3. **`pix_fmt` warning on upload**: Always include `ffmpeg_params=['-pix_fmt', 'yuv420p']` for maximum player compatibility.
4. **Font not found on Windows**: Fall back to `ImageFont.load_default()`. Try system fonts: `C:/Windows/Fonts/arialbd.ttf`, `tahomabd.ttf`.

## FFmpeg on PATH

For tools that expect `ffmpeg` on PATH (HyperFrames CLI, etc.), extract the bundled binary:

```bash
python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"
# Copy to a PATH location:
mkdir -p ~/ffmpeg/bin
cp <path> ~/ffmpeg/bin/ffmpeg.exe
cp ~/ffmpeg/bin/ffmpeg.exe ~/ffmpeg/bin/ffprobe.exe
export PATH="$HOME/ffmpeg/bin:$PATH"
```

## When HTML rendering is better

For videos needing rich typography, CSS gradients, GSAP animation, or kinetic text, use the **`html-video-rendering`** skill instead — it captures frames from a real browser (Chrome + Selenium) and encodes with FFmpeg, producing far richer visuals than Pillow can.

## References

- `scripts/tiktok_news_renderer.py` — complete, runnable TikTok news video script from this session
