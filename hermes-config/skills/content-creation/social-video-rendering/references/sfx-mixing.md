# SFX Mixing for TikTok Videos (FFmpeg amix)

Mix TTS voiceover + bundled SFX cues into final video using FFmpeg `amix` filter.

## Prerequisites

Copy the needed SFX from `media-use` bundled library:

```bash
SFX_SRC="path/to/skills/media-use/audio/assets/sfx"
cp "$SFX_SRC/impact-bass-1.mp3" ./assets/sfx/
cp "$SFX_SRC/glitch-1.mp3"      ./assets/sfx/
cp "$SFX_SRC/pop.mp3"           ./assets/sfx/
# etc.
```

## SFX Bundled Library (21 files)

| Name | Duration | Use |
|------|----------|-----|
| `impact-bass-1` | 2.12s | Opening slam, hero reveal |
| `impact-bass-2` | 2.59s | Major shock, second impact |
| `glitch-1` | 2.64s | Twist moment, glitch transition |
| `glitch-2` | 3.50s | Harsh chaotic transition |
| `glitch-3` | 3.10s | Subtle digital shift |
| `pop` | 0.72s | Badge/icon appear, spawn |
| `whoosh` | 0.57s | Fast reveal, hard transition |
| `whoosh-short` | 0.57s | Quick swipe/slide |
| `whoosh-cinematic` | 5.54s | Sweeping scene transition |
| `chime` | 2.50s | Success, positive ending |
| `click` | 0.37s | UI tap, selection |
| `click-soft` | 0.37s | Quiet tap |
| `error` | 1.62s | Failure state |
| `key-press` | 0.40s | Keystroke |
| `notification` | 2.46s | Alert/message |
| `ping` | 1.32s | Sharp accent on reveal |
| `riser` | 10.03s | Long cinematic build |
| `sparkle` | 1.80s | Magical reveal highlight |
| `typing` | 1.50s | Code typing beat |

## FFmpeg Command

```python
import subprocess

sfx_cues = [
    # (filename, start_time_s, volume)
    ("impact-bass-1", 0.0, 0.35),
    ("glitch-1", 2.5, 0.3),
    ("pop", 5.0, 0.35),
    ("impact-bass-2", 7.5, 0.35),
    ("whoosh-short", 10.5, 0.3),
    ("chime", 13.0, 0.3),
]

inputs = ["-i", video_nosound, "-i", tts_audio]
filter_parts = ["[1:a]volume=1.0[tts]"]
mix_inputs = ["[tts]"]

for idx, (sfx_name, start_s, vol) in enumerate(sfx_cues):
    sfx_path = f"assets/sfx/{sfx_name}.mp3"
    inputs.extend(["-i", sfx_path])
    pad_ms = int(start_s * 1000)
    filter_parts.append(f"[{idx+2}:a]adelay={pad_ms}|{pad_ms},volume={vol}[sfx{idx}]")
    mix_inputs.append(f"[sfx{idx}]")

mix_count = len(mix_inputs)
filter_parts.append(f"{''.join(mix_inputs)}amix=inputs={mix_count}:duration=longest:dropout_transition=2[audio]")
filter_complex = ";".join(filter_parts)

cmd = ["ffmpeg", "-y"] + inputs + [
    "-filter_complex", filter_complex,
    "-map", "0:v:0", "-map", "[audio]",
    "-c:v", "copy",
    "-c:a", "aac", "-b:a", "192k",
    "-shortest",
    video_final
]
subprocess.run(cmd, check=True, timeout=120)
```

## Volume Rules

- TTS voiceover: `volume=1.0` (baseline)
- SFX: `volume=0.30–0.35` (sit under voice, never fight it)
- No BGM by default unless user requests it

## Timing Rules

- SFX start time = scene start time ± 0.1s tolerance
- SFX durations are known from manifest — check before choosing (impact-bass-1 is 2.12s, glitch-1 is 2.64s)
- Don't overlap two heavy SFX (impact + glitch = jarring)
- End on `chime` for positive closure
