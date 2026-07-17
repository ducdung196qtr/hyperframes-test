# TikTok News Video — Session Example (2026-07-16)

## Session Goal
User asked: "render 1 video về tin tức hot nhất hôm nay... định dạng chuẩn tiktok"

## Content Source
VnExpress RSS (`https://vnexpress.net/rss/tin-moi-nhat.rss`) → 5 top headlines:

1. Haaland gây sốt khi nhận lời mời ăn tối của Tom Holland
2. TSMC rót thêm 100 tỷ USD vào nước Mỹ
3. Bạn gái triệu phú Mỹ chi 2,6 triệu USD thí nghiệm trường thọ
4. Kế hoạch tuổi 28 bỏ việc kỹ sư về quê làm nông dân
5. Cuộc đua thuyết phục ông Trump bỏ ý định thu phí eo Hormuz

## Output
- Resolution: 1080×1920 (9:16 TikTok standard)
- Duration: 12 seconds (2s per card + 0.5s transitions)
- File: `tiktok_news.mp4`, 5.5 MB
- FPS: 30
- Codec: H.264 + AAC

## Key Implementation Details
- FFmpeg auto-resolved via `imageio_ffmpeg.get_ffmpeg_exe()` (no system install needed)
- Frames generated as PIL Images with gradient backgrounds, animated decorations
- Audio: simple sine-wave pad tones, varying frequency per card (220, 262, 330, 277, 311 Hz)
- Transition: 15-frame black fade between cards
- Fonts: Arial Bold / Tahoma from Windows system fonts
- Each card gets unique color scheme (purple, blue, red, green, orange gradients)

## Script Location
`C:\Users\Administrator\render_tiktok_news.py` — the full working script from this session.
