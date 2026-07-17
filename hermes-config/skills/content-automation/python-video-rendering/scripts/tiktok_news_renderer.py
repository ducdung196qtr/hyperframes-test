"""
Complete working example: TikTok news video renderer (1080x1920, 12s, 5 news items)
Generated on Windows Server 2012R2 with Python 3.11 + moviepy 2.2.1 + Pillow
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageSequenceClip, AudioArrayClip
import imageio_ffmpeg

# Config
W, H = 1080, 1920
FPS = 30
OUTPUT = os.path.expanduser("~/tiktok_news.mp4")

# News items — replace with your content
NEWS = [
    {"title": "Headline 1\nSubtitle line\nThird line", "subtitle": "Category"},
    {"title": "Headline 2\nSubtitle line\nThird line", "subtitle": "Category"},
]

# Font fallback
FONT_PATHS = [
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/arial.ttf",
]
FONT_TITLE = None
for fp in FONT_PATHS:
    try:
        FONT_TITLE = ImageFont.truetype(fp, 90)
        break
    except:
        continue
if FONT_TITLE is None:
    FONT_TITLE = ImageFont.load_default()


def create_gradient_background(w, h, color1, color2):
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    for y in range(h):
        ratio = y / h
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        arr[y, :] = [r, g, b]
    return Image.fromarray(arr)


def draw_text_centered(draw, text, font, y_start, max_width, fill_color, line_spacing=10):
    lines = text.split('\n')
    y = y_start
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        x = (W - tw) // 2
        draw.text((x, y), line, fill=fill_color, font=font)
        y += (bbox[3] - bbox[1]) + line_spacing
    return y


def create_frame(news_item, frame_num, total_frames):
    color_schemes = [
        ((20, 10, 40), (80, 20, 60)),
        ((10, 30, 50), (20, 60, 100)),
        ((30, 15, 20), (100, 30, 20)),
        ((15, 30, 20), (30, 80, 40)),
        ((40, 20, 10), (100, 60, 20)),
    ]
    idx = NEWS.index(news_item) % len(color_schemes)
    c1, c2 = color_schemes[idx]

    img = create_gradient_background(W, H, c1, c2)
    draw = ImageDraw.Draw(img)

    progress = frame_num / max(total_frames, 1)
    ease = 1 - (1 - progress) ** 3

    # Top accent bar
    draw.rectangle([0, 0, W, 8], fill='#FFD700')
    draw.rectangle([0, H - 8, W, H], fill='#FFD700')

    # Side accent bars
    bar_w = int(6 + ease * 30)
    draw.rectangle([0, 0, bar_w, H], fill='#FFD700')
    draw.rectangle([W - bar_w, 0, W, H], fill='#FFD700')

    # Title
    title_y = int(450 - (1 - ease) * 30)
    draw_text_centered(draw, news_item["title"], FONT_TITLE, title_y, W - 100, 'white', line_spacing=20)

    return np.array(img)


def generate_audio(duration, freq=440):
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    audio = 0.3 * np.sin(2 * np.pi * freq * t)
    fade = min(0.05, duration / 10)
    fade_samples = int(fade * sample_rate)
    if fade_samples > 0:
        audio[:fade_samples] *= np.linspace(0, 1, fade_samples)
        audio[-fade_samples:] *= np.linspace(1, 0, fade_samples)
    return audio


# Build frames
all_frames = []
segment_frames = 60  # 2s per segment
transition_frames = 15

for i, news in enumerate(NEWS):
    for f in range(segment_frames):
        frame = create_frame(news, f, segment_frames)
        all_frames.append(frame)
    if i < len(NEWS) - 1:
        last_frame = create_frame(news, segment_frames - 1, segment_frames)
        for f in range(transition_frames):
            alpha = 1 - (f / transition_frames)
            transition = (last_frame * alpha).astype(np.uint8)
            all_frames.append(transition)

# Assemble
clip = ImageSequenceClip(all_frames, fps=FPS)
total_duration = len(all_frames) / FPS

# Audio
audio_segments = []
base_freqs = [220, 262, 330, 277, 311]
for i in range(len(NEWS)):
    seg_dur = segment_frames / FPS
    freq = base_freqs[i % len(base_freqs)]
    audio_segments.append(generate_audio(seg_dur, freq))
    if i < len(NEWS) - 1:
        audio_segments.append(np.zeros(int(44100 * (transition_frames / FPS))))

full_audio = np.concatenate(audio_segments)
audio_clip = AudioArrayClip(np.column_stack([full_audio, full_audio]), fps=44100)
clip = clip.with_audio(audio_clip)

# Write
clip.write_videofile(
    OUTPUT, fps=FPS, codec='libx264', audio_codec='aac',
    preset='fast', bitrate='5000k', threads=2,
    ffmpeg_params=['-pix_fmt', 'yuv420p'],
)
clip.close()
print(f"Done: {OUTPUT} ({os.path.getsize(OUTPUT) / 1024 / 1024:.1f} MB)")
