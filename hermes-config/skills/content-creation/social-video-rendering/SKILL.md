---
name: social-video-rendering
description: Render short-form vertical videos (TikTok/Reels/Shorts format) with text overlays, gradient backgrounds, animated decorations, and audio using Python (Pillow + moviepy + FFmpeg).
triggers:
  - User asks to render, create, or make a TikTok, Reel, Shorts, or social video
  - User asks for video from news, text, or data
  - User says 'render video', 'make video', 'tạo video'
---

# Social Video Rendering (TikTok / Reels / Shorts)

Render professional 9:16 vertical videos programmatically from text content — news headlines, quotes, bullet lists, data cards.

## Prerequisites

```bash
pip install pillow moviepy numpy
```

FFmpeg is auto-provided by `imageio-ffmpeg` (bundled binary — no system install needed). Confirm with:

```python
import imageio_ffmpeg
print(imageio_ffmpeg.get_ffmpeg_exe())  # returns path to bundled ffmpeg
```

## Core workflow

1. **Gather content** — scrape or prepare the text payload (news RSS, data rows, quotes)
2. **Generate frames** — create each frame as a PIL Image with the text, gradient bg, and animated decoration
3. **Assemble video** — feed the frame list to `ImageSequenceClip` at 30fps
4. **Add audio** — generate a simple tone or attach a music file via `AudioArrayClip`
5. **Write MP4** — use `libx264` + `aac` with `yuv420p` pixel format for universal playback

## Frame generation pattern

For each "card" (news item, quote, data point), generate ~60 frames (2 seconds at 30fps) with an ease-in animation on text position:

```python
progress = frame_num / total_frames
ease = 1 - (1 - progress) ** 3  # ease-out cubic
y_offset = int(base_y - (1 - ease) * 30)
```

### Visual elements that look good on vertical video

- **Gradient background** — two colors blended vertically, different per card
- **Golden accent bars** — top/bottom edges, animated side bars
- **Decorative circle** — pulsing ring around center with small orbiting dots
- **Tag label** — category badge in golden pill shape at top
- **Title text** — large white multiline centered text
- **Subtitle** — smaller golden text with underline
- **Page indicator** — "1/5" at bottom
- **Diagonal pattern overlay** — subtle RGBA lines for texture

### Color schemes

Vary background gradient per card to create visual variety. Dark base with saturated accent works well:
- Purple → Magenta, Blue → Cyan, Dark Red → Red, Green → Emerald, Orange → Amber

## MoviePy output settings

```python
clip.write_videofile(
    path,
    fps=30,
    codec='libx264',
    audio_codec='aac',
    preset='fast',
    bitrate='5000k',
    ffmpeg_params=['-pix_fmt', 'yuv420p'],
)
```

## Font setup

### For HTML/CSS rendering (REQUIRED for Vietnamese)
**Google Fonts Roboto is mandatory for Vietnamese text.** Arial and system fonts do NOT render Vietnamese diacritics (ả, ạ, ệ, ố, etc.) correctly in headless Chrome. They appear as blank boxes or misaligned glyphs. User explicitly complained: "font chữ chưa oke với tiếng việt".

```html
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@700;900&display=swap" rel="stylesheet">
```

```css
body { font-family: 'Roboto', Arial, sans-serif; }
```

Use `font-weight: 700` for sub-text and `font-weight: 900` for headlines. Roboto handles all Vietnamese diacritics correctly.

### For Pillow/moviepy rendering (legacy — avoid for Vietnamese)
Only use Pillow fonts for English text. Vietnamese text rendered through Pillow with Arial/Tahoma will have broken/missing diacritics. Prefer the HTML approach above.

## Voiceover / TTS (Text-to-Speech)

### Voice availability (Vietnamese)

Only **2 free Vietnamese TTS voices** exist across all providers — there is no "Adam" or other male voice beyond NamMinh:

| Provider | Male | Female | Reliability | Notes |
|----------|------|--------|-------------|-------|
| **Hermes TTS tool** | Configurable | — | ✅ Most reliable | Uses Edge backend via different path. No voice/pitch params — text only. |
| **Edge TTS** | NamMinh | HoaiMy | ⚠️ Intermittent `NoAudioReceived` | Python library can die globally. |
| **gTTS (Google)** | 1 neutral | — | ✅ Stable | Fallback only — some users reject quality. |

No other free Vietnamese TTS voices exist (no free OpenAI/ElevenLabs/FPT tiers). If user asks for "Adam" or ElevenLabs-style voices, explain the limitation.

### gTTS (Google TTS) — FALLBACK ONLY

gTTS is a backup when Edge TTS is unavailable. Some users find its Vietnamese voice quality unacceptable. Always offer the user a choice between available TTS options; never assume gTTS is preferred.

```bash
pip install gtts
```

```python
from gtts import gTTS

TEXT = "AI hứa sẽ GIẢI PHÓNG con người! ..."
tts = gTTS(text=TEXT, lang='vi', slow=False)
tts.save('output.mp3')
```

- `lang='vi'` — Vietnamese (single neutral male voice)
- `slow=False` — normal speed, matches TikTok pacing
- **Auto-emphasis**: UPPERCASE words and `!` are naturally emphasized — no formatting tricks needed
- Duration for ~370 chars of Vietnamese: ~30s (9:16 TikTok sweet spot)
- Always send the `.mp3` file to the user for approval before proceeding

### Edge TTS (NamMinh / HoaiMy) — FALLBACK

Used as fallback when gTTS is unavailable. Only 2 voices exist for Vietnamese:

| Voice | Gender | Personality |
|-------|--------|-------------|
| `vi-VN-NamMinhNeural` | Male | Friendly, warm, authoritative — best for news/analysis |
| `vi-VN-HoaiMyNeural` | Female | Friendly, positive, gentle — best for lifestyle/emotional content |

```bash
pip install edge-tts
```

```python
import asyncio, edge_tts

async def gen_voice(text, voice="vi-VN-NamMinhNeural", out="voice.mp3"):
    comm = edge_tts.Communicate(text, voice, rate="+5%")
    await comm.save(out)

asyncio.run(gen_voice("Nội dung bài viết của bạn..."))
```

Speed control: `rate="+5%"` for fast-paced TikTok, `rate="+0%"` for calm explainer, `rate="-5%"` for dramatic/narrative delivery with more weight per word.

Pitch control: `pitch="+15Hz"` for brighter/more energetic voice, omit for natural pitch.

### TTS dramatic delivery (Vietnamese NamMinh — no style variants)

The `vi-VN-NamMinhNeural` voice has no built-in style tags, but **text formatting drives delivery**. User explicitly complained about flat delivery ("như đọc sớ vậy đó") and asked to "phân tích lại cách chấm, phẩy câu". The following techniques work:

| Technique | Effect | Example |
|-----------|--------|---------|
| **IN HOA** (UPPERCASE) | Natural emphasis, louder | `"AI HỨA sẽ giải phóng"` |
| `...` ellipsis | Dramatic pause, voice drops | `"NHƯNG... lập trình viên"` |
| `!` exclamation | Pitch rises at end | `"ngủ gục giữa ngày!"` |
| `,` comma | Light breath pause | `"20 AI Agent, 1 con người"` |
| `rate="-5%"` | Slower, weightier delivery | Good for dramatic/narrative |
| `pitch="+15Hz"` | Brighter, more energetic | Good for engaging content |

**MC-style dramatic recipe** (user-approved for news/analysis videos):
```
rate="-5%", pitch="+15Hz", IN HOA keywords, ... before punchlines, ! on shock statements
```

**Fast-paced TikTok recipe** for quick-hit content:
```
rate="+5%" to "+10%", fewer ... pauses, shorter sentences
```

### Edge TTS pitfalls

- **`edge-tts` Python library may suddenly fail globally**: The library can enter a state where ALL requests return `NoAudioReceived` — even trivial text with no SSML, pitch, or rate args. This is a service-side or rate-limit issue, not a code bug. When this happens:
  1. **DO NOT retry with the same library** — every attempt will fail.
  2. **Switch to the Hermes built-in `text_to_speech` tool** instead. It uses a different Edge backend path and is more reliable. The tool returns a `MEDIA:` path directly. Call it with the Vietnamese text and an `output_path` to `C:\Users\Administrator\script_audio.mp3`. The tool auto-picks the configured voice (typically NamMinh for this user) without voice/pitch/rate params — just the text.
  3. Only fall back to gTTS as a last resort (user may reject quality — some users find gTTS Vietnamese quality unacceptable).
- **`pitch` kwarg is unreliable and causes `NoAudioReceived`**: Passing `pitch="+15Hz"` or `pitch="+20Hz"` to `edge_tts.Communicate()` can trigger `NoAudioReceived` errors even when the same text works without it. Test without pitch first, add it only if the base audio succeeds.
- **`<emphasis>` tag fails on Vietnamese voices**: `edge_tts.Communicate(ssml_with_emphasis, "vi-VN-NamMinhNeural")` returns `NoAudioReceived`. Do NOT use `<emphasis>` in SSML for Vietnamese. Use IN HOA text instead.
- **`<prosody rate>` in SSML inflates duration dramatically**: A 209-char text that produces ~12s with the Python `rate` kwarg can balloon to 51s via `<prosody rate="1.05">`. Always use `rate="+N%"` on `Communicate()`, never `<prosody rate>` in SSML text.
- **SSML is unreliable for Vietnamese** — plain text with formatting (caps, punctuation) is more predictable. Stick to the text-formatting techniques above.

### TTS workflow

1. **Generate TTS** with plain text + formatting hints
2. **Send audio to user for approval** — always let them hear before proceeding. Send the `.mp3` file directly.
3. **User may iterate 3-4 times** on delivery quality. This is normal — expect it. Don't proceed to HTML/render until audio is approved.
4. **LOCK THE AUDIO once approved**: NEVER change its text, duration, or parameters silently. User got frustrated when a 51s-approved script was silently changed to 12s: "có biết phí time t chờ đợi lắm k". If a change is needed, propose it and wait for confirmation.

**When selecting a voice for the user (Đức Dũng)**:
- Default to **NamMinh** (male) — matches the authoritative "Đức Dũng" brand
- Let the user hear both samples before finalizing — always send audio files for approval
- The `+5%` rate works well for TikTok's fast pacing

## HTML-to-Video rendering (HyperFrames-compatible fallback)

When HyperFrames CLI can't use its built-in headless Chrome (e.g. Chrome 109 on Windows Server 2012), fall back to **Selenium + FFmpeg** — the same HTML/CSS/GSAP composition renders correctly:

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import subprocess, time, os

# Use existing Chrome 109
options = Options()
options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1080,1920")

driver = webdriver.Chrome(options=options)
driver.get(f"file:///{html_path.replace('\\', '/')}")

for frame in range(total_frames):
    t = frame / fps
    # Seek GSAP global timeline — works with standard CDN GSAP
    driver.execute_script(f"gsap.globalTimeline.time({t})")
    time.sleep(0.005)  # tiny wait for render
    driver.save_screenshot(f"frames/frame_{frame:05d}.png")

driver.quit()

# Encode with FFmpeg
subprocess.run([
    "ffmpeg", "-y", "-framerate", "30",
    "-i", "frames/frame_%05d.png",
    "-c:v", "libx264", "-pix_fmt", "yuv420p",
    "-preset", "fast", "-crf", "23",
    "output.mp4"
])
```

Full working script: `references/html-to-video-selenium.py`

## Video rendering workflow (user preference)

When the user asks to render a video from their blog articles:

1. **Find article** — present top 3-5 articles ranked by viral potential, let user pick. User may also request fresh content from news sources.
2. **Voice approval** — generate TTS samples, let user hear them before proceeding. For news/analysis content with the user's preference for dramatic delivery, use the MC-style recipe: `rate="-5%"`, `pitch="+15Hz"`, IN HOA keywords, `...` before punchlines, `!` on shock statements. Always send the `.mp3` file for approval. Expect 3-4 iterations on delivery quality — this is normal.
3. **Write a detailed plan file (MANDATORY)** — create a `video_plan.md` with:
   - Exact timing per scene (0.1s precision)
   - Every text overlay with exact wording, size, color, and animation style
   - Which background image per scene
   - Animation types (stagger, shake, bounce, typewriter, slide, zoom, pulse glow, fade, scale)
   - Color scheme (white headlines, gold #FFD700 highlights, red #ff4444 twist text)
   - User must **review and approve the plan** before any HTML/render work begins.
   - User explicitly said "thấy phong cách video chưa đúng ý tôi. text cần nhiều hơn. bạn cần chuẩn bị 1 files MD đi" — dense text is preferred, not sparse. Aim for 8-12 text segments in a 15s video.
4. **AUDIO-FIRST sync (MANDATORY — user rejected out-of-sync video):** Before writing a single line of HTML, extract the exact speech/silence timing from the TTS audio using FFmpeg silence detection. Then build the scene timeline to match those timestamps. Never eyeball timing or assume even pacing. See `references/audio-sync.md` for the exact procedure.
5. **IMAGE + TEXT split layout (MANDATORY — user rejected dark-only + overlay backgrounds):** User said "tôi muốn hình hiện lên vs text luôn. thay vì background như hiện tại" and "cái nền nó hơi đen quá. nên bỏ hình dưới text tăng sự tin cậy". Every scene MUST use a **62% image zone (top) + 38% text zone (bottom)** split with a CSS `linear-gradient` mask fading the bottom of the image into the text zone's solid `#0a0f1a` background. The image must be a visible, distinct zone alongside the text — NOT a dim background-image with text overlaid on top. User needs to see the photo clearly as a trust/credibility signal. See `references/image-text-layout.md` for the exact CSS pattern and `templates/tiktok-split-layout.html` for the working template.
6. **Preview screenshots BEFORE full render (MANDATORY):** User asked "trước khi render video cho tôi xem html trước dc k". After writing the HTML, capture 5-6 preview frames at key scene timestamps via Selenium (`driver.save_screenshot()` or `driver.get_screenshot_as_file()`), send the PNGs to the user, and **wait for approval** before running the full 480-frame render. This saves ~15 minutes of wasted render time when layout adjustments are needed. Use `gsap.globalTimeline.time(t)` to seek to exact timestamps for each preview.
7. **Only after preview is approved** — run the full Selenium + FFmpeg render with SFX audio mixing.
8. **NO "by Đức Dũng" in video** — user explicitly rejected this: "bỏ cái by duc dung gì đó trong video đi nghe". Brand identity goes on the blog/website, not in the video footer.
9. **HyperFrames creative styles** — when user asks for a specific visual style (e.g. "free-style-sfx", Deconstructed), adopt the design tokens from `hyperframes-creative` skill: palette, typography, motion energy, atmosphere (scan-lines, grain, glitch artifacts), transition shaders. The bundled SFX manifest in `media-use` skill provides 21 cue-able effects (impact-bass, glitch, pop, whoosh, chime, etc.) — mix them into the final video via FFmpeg amix filter. See `references/sfx-mixing.md` for the exact FFmpeg filter_complex command.

## Audio

Generate a simple pad tone if no music file is available:

```python
import numpy as np
def generate_tone(duration, freq=440, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    audio = 0.3 * np.sin(2 * np.pi * freq * t)
    # Soft fade in/out
    fade = min(0.05, duration / 10)
    fade_samples = int(fade * sample_rate)
    audio[:fade_samples] *= np.linspace(0, 1, fade_samples)
    audio[-fade_samples:] *= np.linspace(1, 0, fade_samples)
    return audio
```

Vary frequency per card for subtle progression. On TikTok, users typically add trending music in-app after upload.

## Transitions

Insert 15 black-fade frames between cards for a clean cut:

```python
alpha = 1 - (f / transition_frames)
transition = (last_frame * alpha).astype(np.uint8)
```

## Related skills

- **`python-video-rendering`** — Lower-level Python/Pillow frame generation (prefer this for simple static-card videos)
- **`html-video-rendering`** — HTML/CSS/GSAP → MP4 via browser capture. Vastly richer visuals (CSS gradients, Google Fonts, Lottie, Three.js) for any video with motion graphics or kinetic text. Use this instead of Pillow when you need professional-grade animation.

## Pitfalls

- **Font missing on Linux/macOS** — the script uses Windows font paths. On other OS, replace with system-appropriate paths or use Pillow's default font (ugly but works).
- **Memory with many frames** — for videos >30s, write frames to disk instead of holding all in RAM. Use `ImageSequenceClip` with a generator or temp files.
- **FFmpeg not found** — don't install system ffmpeg; `imageio_ffmpeg` bundles its own. Pass its path explicitly via `write_videofile(ffmpeg_params=...)`.
- **Pillow version conflict** — moviepy may downgrade Pillow. If rendering still works, ignore the pip warning.
- **Abstract gradients look disconnected from text (CRITICAL)**: User complained "có thấy liên quan đến đoạn text đang đọc k" when using abstract gradient backgrounds. Always use real stock photos that visually match the content — never default to synthetic gradients when a photo search is possible. Use Selenium Chrome to search Google Images, Pexels, or Unsplash for real photos. Fallback: specific Unsplash photo IDs (by subject) or download from known working URLs.
- **FFmpeg/ffprobe fails on Windows**: `ffprobe -show_entries format=duration` often returns empty stdout on Windows. Workaround: parse duration from `ffmpeg -i audio.mp3 -f null -` stderr with regex `Duration: (\d+):(\d+):(\d+\.\d+)`. Convert to seconds: `h*3600 + m*60 + s`.
- **Edge TTS SSML `<prosody rate>` inflates duration dramatically**: Wrapping text in `<speak><voice><prosody rate="1.05">...</prosody></voice></speak>` can make a 12s-worthy script balloon to 51s. The SSML parser interprets `rate` relative to a default that's already slower than the raw text path. **Always use the Python API `rate` parameter instead:** `edge_tts.Communicate(text, voice, rate="+10%")`. Never use `<prosody rate>` in SSML unless you have verified the output duration matches expectations. A 209-character Vietnamese text at `rate="+10%"` with `vi-VN-NamMinhNeural` produces ~12s — the perfect TikTok length.
- **Custom `seekTo()` more reliable than `gsap.globalTimeline.time()`**: The pattern `driver.execute_script(f"window.seekTo({t});")` where `seekTo` wraps `tl.progress(Math.min(t / DURATION, 1.0))` is more reliable than `gsap.globalTimeline.time(t)` which can desync from the paused timeline's actual state. Always define `window.seekTo` as part of the HTML. The render script at `scripts/render-tiktok-selenium.py` uses this pattern.
- **Progress reporting at 10% intervals (user mandate)**: When rendering frames, print progress every 10% — NEVER every N frames. User said "cứ 10% báo tôi 1 lần nha, sau này sẽ thế". Use `if i % (TOTAL_FRAMES // 10) == 0 or i == TOTAL_FRAMES - 1` and print `[i/TOTAL] {pct}% | {fps}fps | ETA {eta}s`. The render script at `scripts/render-tiktok-selenium.py` has this built in.
- **Stock image APIs blocked on server**: Pexels/Pixabay/Unsplash API keys may be rate-limited or blocked. Use Selenium Chrome to open Pexels.com directly and extract image URLs from page source (search for `images.pexels.com` in `page_source`). Unsplash direct photo URLs (`images.unsplash.com/photo-XXXXX?w=1080&h=1920&fit=crop`) can be tried as fallback — use specific known photo IDs by topic.
- **NEVER silently change approved audio duration/text (CRITICAL)**: User explicitly got frustrated: "có biết phí time t chờ đợi lắm k". If the user approved a 51s TTS, do NOT silently switch to a 12s version. If a change is needed, propose it and wait for explicit confirmation. Lock the audio file + duration once approved — treat it like a signed contract. Any deviation wastes the entire render cycle.

## Frame resolution fix (CRITICAL)

Selenium headless Chrome screenshots often come out at the wrong resolution (e.g. 1064×959 instead of the requested 1080×1920). Always resize + crop each frame to exact target dimensions in the capture loop:

```python
from PIL import Image

img = Image.open(io.BytesIO(screenshot))
w, h = img.size
target_ratio = 1080 / 1920  # 0.5625
current_ratio = w / h

if current_ratio > target_ratio:
    new_w = int(h * target_ratio)
    offset = (w - new_w) // 2
    img = img.crop((offset, 0, offset + new_w, h))
elif current_ratio < target_ratio:
    new_h = int(w / target_ratio)
    offset = (h - new_h) // 2
    img = img.crop((0, offset, w, offset + new_h))

img = img.resize((1080, 1920), Image.LANCZOS)
img.save(f"frames/frame_{i:05d}.png", "PNG")
```

Alternative post-hoc fix on already-captured frames: `ffmpeg -i input.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" output.mp4`

## HTML template for TikTok videos

The HTML must:
- Use **Google Fonts Roboto** — Arial does NOT render Vietnamese diacritics correctly in headless Chrome. Add `<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@700;900&display=swap" rel="stylesheet">` and set `font-family:'Roboto',Arial,sans-serif`
- Store background images as **relative paths** — copy images into the same directory as the HTML file, use `url('filename.jpg')` in CSS `background-image`. Absolute Windows paths (`C:\Users\...`) silently fail
- Structure as `<div class="scene">` containers with GSAP timeline for crossfade transitions
- Dark overlay gradient on images for text readability: `linear-gradient(180deg, rgba(0,0,0,0.35) 0%, rgba(0,0,0,0) 35%, rgba(0,0,0,0.75) 100%)`
- Gold (`#FFD700`) highlight color for key phrases on dark backgrounds
- Semi-transparent black CTA box at bottom with website URL
- NOT include "by Đức Dũng" branding — user explicitly rejected this

Full working template: `templates/tiktok-video.html`

## Image sourcing via Selenium Chrome

Stock photo APIs (Pexels, Pixabay, Unsplash) are often blocked or rate-limited on server environments. Working approaches:

1. **Selenium Chrome → Pexels.com**: Open `https://www.pexels.com/search/<query>/?orientation=portrait`, extract image URLs from `page_source` (search for `images.pexels.com`). Download with urllib + User-Agent header.
2. **Unsplash direct photo IDs** (no API key needed):
   - Sleeping programmer: `photo-1498050108023-c5249f4df085`, `photo-1531482615713-2afd69097998`
   - AI/robot: `photo-1677442136019-21780ecad995`, `photo-1620712943543-bcc4688e7485`
   - Office stress: `photo-1434030216411-0b793f4b4173`, `photo-1488190211105-8b0e65b80b4e`
   Format: `https://images.unsplash.com/{ID}?w=1080&h=1920&fit=crop`
3. **Copy to HTML directory**: After download, copy images into the render directory so relative CSS paths work

## Templates

- `templates/tiktok-split-layout.html` — 62/38 image+text split layout with Oswald font, scanlines, vignette, and GSAP seekable timeline scaffold.

## References

- `references/audio-sync.md` — zero-tolerance audio-first sync: extract TTS speech segment timestamps BEFORE writing HTML, build GSAP timeline from actual audio, not guesses
- `references/image-text-layout.md` — 62/38 split layout pattern: image zone on top, text zone on bottom with gradient mask
- `references/sfx-mixing.md` — FFmpeg amix filter_complex for mixing TTS + bundled SFX into final video
- `scripts/render-tiktok-selenium.py` — complete Selenium + FFmpeg pipeline for TikTok video from HTML/GSAP + Edge TTS audio
- `templates/tiktok-video.html` — working HTML template with Roboto font, 3-scene GSAP timeline, dark overlays
