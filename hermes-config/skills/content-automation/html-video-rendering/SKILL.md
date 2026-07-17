---
name: html-video-rendering
description: Render video from HTML/CSS/GSAP — professional animations via browser screenshot capture + FFmpeg. Covers HyperFrames (HeyGen's 35K★ framework) and the Selenium fallback pipeline for legacy Windows hosts.
triggers:
  - User asks to render video with animations, motion graphics, kinetic text
  - User mentions HyperFrames, HTML-to-video, or GSAP video
  - User wants richer visuals than Python/Pillow can produce
  - User asks to "make a video like a website"
---

# HTML Video Rendering (HyperFrames + Selenium fallback)

Render professional MP4 videos from HTML/CSS/GSAP by screenshot-capturing each frame from a headless browser and encoding with FFmpeg. This approach unlocks rich typography, CSS gradients, GSAP animation, Lottie, and Three.js — vastly more powerful than Python/Pillow for motion graphics.

## Two pipelines (pick based on host)

### Path A: HyperFrames (HeyGen) — preferred

[HyperFrames](https://github.com/heygen-com/hyperframes) (Apache 2.0, 35K+ stars) is HeyGen's open-source framework for turning HTML into deterministic MP4. It ships **19 AI-agent skills** covering product launches, faceless explainers, PR-to-video, embedded captions, talking-head recuts, motion graphics, music-to-video, slideshows, and more.

```bash
npx hyperframes init my-video --example blank
cd my-video
# Write index.html with GSAP + data-* attributes
npm run check   # lint + runtime validation
npm run render  # encode MP4
```

The framework uses `data-start`, `data-duration`, `data-track-index` attributes on `class="clip"` elements, plus `window.__timelines` GSAP registration for animation.

**TTS + media**: Skill `media-use` provides `resolve --type voice` (HeyGen TTS free via OAuth, or local Kokoro), `resolve --type bgm/sfx/image/icon`, transcription (Parakeet, WER 6.05%), auto-duck, and avatar video generation.

**Requirements**: Node.js 22+, Chrome headless-shell ≥ v152 (bundled), FFmpeg on PATH.

### Path B: Selenium fallback — for legacy / Win Server 2012 hosts

When HyperFrames' bundled Chrome headless-shell won't run (Windows Server 2012R2, Chrome 109), use the direct Selenium + FFmpeg pipeline:

1. Write the composition as pure `index.html` with inline GSAP (CDN)
2. Launch Chrome via Selenium in headless mode
3. Loop through frames: `gsap.timeline.time(t)`, `driver.save_screenshot(frame_N.png)`
4. Encode with FFmpeg: `ffmpeg -framerate 30 -i frame_%05d.png -c:v libx264 ... output.mp4`

```python
# Key pattern — define seekTo in HTML, call from Python
# In HTML <script>:  window.seekTo = t => tl.progress(Math.min(t / DURATION, 1.0));
# In render loop:
for frame in range(total_frames):
    t = frame / fps
    driver.execute_script(f"window.seekTo({t})")
    time.sleep(0.005)   # tiny wait for browser render
    driver.save_screenshot(f"frames/frame_{frame:05d}.png")
```

**Resolution tip**: Set `--window-size=1080,1920` and `--force-device-scale-factor=1` in Chrome options for TikTok 9:16. For landscape, use `1920,1080`.

## FFmpeg setup (both paths)

HyperFrames and the Selenium pipeline both need `ffmpeg` on PATH. On Windows hosts without a system install, copy the bundled binary from Python's `imageio_ffmpeg`:

```bash
# imageio_ffmpeg bundles ffmpeg — extract it to a known PATH location
python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"
# → C:\...\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe

mkdir -p ~/ffmpeg/bin
cp <that-path> ~/ffmpeg/bin/ffmpeg.exe
cp ~/ffmpeg/bin/ffmpeg.exe ~/ffmpeg/bin/ffprobe.exe
export PATH="$HOME/ffmpeg/bin:$PATH"
```

## When to use HTML vs Python/Pillow

| Criterion | HTML/GSAP (this skill) | Python/Pillow |
|-----------|----------------------|---------------|
| Rich typography | ✅ Native CSS fonts, Google Fonts | ⚠️ PIL font handling is limited |
| Animations | ✅ GSAP, CSS keyframes, Lottie, Three.js | ❌ Manual frame math |
| Gradient backgrounds | ✅ CSS `linear-gradient` | ⚠️ Manual draw per frame |
| Text wrapping | ✅ CSS layout engine | ❌ Manual word-wrap logic |
| Development speed | ✅ Live-preview in browser | ⚠️ Render-to-see |
| Host requirements | Chrome + FFmpeg | Python + Pillow only |
| Legacy Win Server 2012 | ✅ Via Selenium fallback | ✅ |

**Rule**: default to HTML/GSAP for any video with motion graphics, kinetic text, or rich visuals. Fall back to Python/Pillow only for simple static-card videos where the HTML overhead isn't justified.

## Pitfalls

1. **HyperFrames init path on Windows Git Bash**: `npx hyperframes init /c/Users/.../project` creates the project at a doubled path (`/c/c/Users/.../` → actually `C:\c\Users\...\project`). The init says "Created" but the directory appears empty/unfindable. **Always `cd` into the target directory first, then `npx hyperframes init .`**.
2. **HyperFrames browser ensure extraction fails silently on Win Server 2012**: `npx hyperframes browser ensure` downloads the 115MB Chrome headless-shell zip but extraction leaves an empty directory with no `.exe`. Workaround: `npx hyperframes browser ensure --force` to retry (also fails), or symlink/copy Chrome 109 from `C:\Program Files (x86)\Google\Chrome\Application\chrome.exe` to the expected cache path. Even then, Chrome 109 causes `spawn UNKNOWN` at render time — **use Path B (Selenium fallback) on Win Server 2012**.
3. **FFmpeg not found**: HyperFrames and the Python pipeline both need `ffmpeg` + `ffprobe` on PATH. See FFmpeg setup above. On Windows hosts, `imageio_ffmpeg` bundles a working `ffmpeg-win-x86_64-v7.1.exe` — copy to `~/ffmpeg/bin/ffmpeg.exe` and `ffprobe.exe`, then `export PATH`.
4. **GSAP timeline not advancing**: The most reliable way to seek a GSAP timeline in Selenium is `window.seekTo(t)` wrapping `tl.progress(Math.min(t / DURATION, 1.0))` — define it in the HTML `<script>` tag and call `driver.execute_script(f"window.seekTo({t})")` in the render loop. `gsap.globalTimeline.time(t)` can desync from the paused timeline's actual state, producing identical frames. Do NOT use `window.__timelines['main'].time(t)` — that pattern is HyperFrames-specific. Also set `--window-size=1080,1920` with `--force-device-scale-factor=1` for TikTok 9:16 — mismatch causes blurry frames.
5. **Chrome scale factor mismatch**: Always set `--window-size` to the exact output resolution with `--force-device-scale-factor=1`. A mismatch causes blurry or cropped frames.
6. **Low memory on 2GB hosts**: HyperFrames auto-detects low memory and pins to 1 worker. For Selenium pipeline, keep frame PNGs on disk (don't accumulate in RAM). Each 1080×1920 PNG is ~200KB; 240 frames = ~50MB.

## References

- `references/hyperframes-deep-dive.md` — full capability map, 19 skills breakdown, TTS/media details
- `scripts/render-html-to-video.py` — runnable Selenium + FFmpeg pipeline script
