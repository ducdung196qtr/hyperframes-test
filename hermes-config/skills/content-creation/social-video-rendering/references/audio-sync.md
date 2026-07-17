# Audio-First Sync: TTS → Scene Timeline

**CRITICAL**: The user explicitly complained about out-of-sync audio ("audio đang bị lạch so vs text chạy thực tế"). Never estimate timing — extract it from the audio file first, then build the scene timeline around those timestamps.

## Step 1: Extract speech segments from TTS audio

```python
import subprocess, re

FFMPEG = r"C:\Users\Administrator\ffmpeg\bin\ffmpeg.exe"

# Get total duration
result = subprocess.run(
    [FFMPEG, "-i", AUDIO_PATH, "-f", "null", "-"],
    capture_output=True, text=True
)
match = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", result.stderr)
duration = int(match.group(1))*3600 + int(match.group(2))*60 + float(match.group(3))

# Detect silence gaps (pauses between sentences)
result = subprocess.run(
    [FFMPEG, "-i", AUDIO_PATH, 
     "-af", "silencedetect=noise=-25dB:d=0.25",
     "-f", "null", "-"],
    capture_output=True, text=True
)

# Parse into speech segments
times = []
for line in result.stderr.split("\n"):
    m_start = re.search(r"silence_start: ([\d.]+)", line)
    m_end = re.search(r"silence_end: ([\d.]+)", line)
    if m_start:
        times.append(("silence_start", float(m_start.group(1))))
    elif m_end:
        times.append(("silence_end", float(m_end.group(1))))

# Group: silence_start → silence_end = pause
# Everything else = speech
gaps = []
i = 0
while i < len(times):
    if times[i][0] == "silence_start":
        start = times[i][1]
        if i+1 < len(times) and times[i+1][0] == "silence_end":
            end = times[i+1][1]
            gaps.append((start, end))
            i += 2
        else:
            i += 1
    else:
        i += 1

# Speech segments
segments = []
prev_end = 0.0
for s, e in gaps:
    if s - prev_end > 0.1:  # meaningful speech
        segments.append((prev_end, s))
    prev_end = e
if duration - prev_end > 0.1:
    segments.append((prev_end, duration))

print("Speech segments:")
for i, (s, e) in enumerate(segments):
    print(f"  [{i}] {s:.2f}s → {e:.2f}s ({e-s:.2f}s)")
```

## Step 2: Map segments to scene content

Example output from a 15.84s TTS audio:
```
Speech segments:
  [0] 0.00s → 1.77s (1.77s) — "AI hứa sẽ giải phóng con người"
  [1] 2.71s → 6.00s (3.29s) — "Nhưng lập trình viên đang ngủ gục..."
  [2] 7.07s → 7.67s (0.60s) — short phrase
  [3] 7.93s → 10.15s (2.22s) — "Tỷ lệ phi lý đang bào mòn..."
  [4] 11.11s → 15.05s (3.94s) — quote + CTA
```

## Step 3: Build scene timeline from segments

Each speech segment = one scene. Text appears at segment start, fades out at segment end. Never assume uniform 2.5s or 3s per scene — follow the actual audio.

```javascript
// GSAP timeline synced to actual speech segments
const tl = gsap.timeline({ paused: true });

// Scene 1: 0.00s → 1.77s
tl.to(s1, { opacity: 1, duration: 0.3, ease: "back.out(2.5)" }, 0.00)
  .to(s1, { opacity: 0, duration: 0.3, ease: "power4.in" }, 1.47);

// Scene 2: 2.71s → 6.00s  
tl.to(s2, { opacity: 1, duration: 0.3, ease: "back.out(2.5)" }, 2.71)
  .to(s2, { opacity: 0, duration: 0.3, ease: "power4.in" }, 5.70);
// ... etc
```

## Pitfalls

- **Never use `ffprobe -show_format` on Windows** — stdout is often empty. Use `ffmpeg -i file -f null -` and parse stderr Duration line.
- **Silence threshold**: `-25dB` with `d=0.25s` works well for Vietnamese TTS. Adjust to `-20dB` if speech is too quiet or `-30dB` if pauses are being merged.
- **Segment floor**: ignore speech segments shorter than 0.1s (noise artifacts).
- **TTS must be generated FIRST**, before writing HTML. The HTML timeline depends on the actual audio timing, not the reverse.
