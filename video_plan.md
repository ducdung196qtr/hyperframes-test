# 🎬 Kế hoạch TikTok Video: "AI Agent Đang Bào Mòn Lập Trình Viên"
## 1080×1920 | 15.8 giây | Giọng NamMinh | 30fps

---

### Tổng quan
- **Nguồn**: The Atlantic — "America Is Headed Toward the Infinite Workweek" (18/6/2026)
- **Phong cách**: Faceless explainer, text-heavy, giật màn hình kiểu TikTok viral
- **Font**: Roboto (Google Fonts — hỗ trợ đầy đủ dấu tiếng Việt)
- **Ảnh**: Pexels / Unsplash (ảnh thật, đã tải về)
- **Animation**: GSAP stagger, fade, scale, slide
- **Màu chính**: Trắng (#fff), Vàng gold (#FFD700), Đỏ cảnh báo (#ff4444)

---

### Timeline chi tiết

| Thời gian | Scene | Ảnh nền | Text trên màn hình | Animation | Giọng đọc |
|-----------|-------|---------|-------------------|-----------|-----------|
| **0.0-1.5s** | Hook | `ai_burnout_1.jpeg` | **AI HỨA SẼ** | Fade in từ dưới, scale 0→1, back.out | "AI hứa sẽ..." |
| **1.5-3.0s** | Hook cont. | `ai_burnout_1.jpeg` | **GIẢI PHÓNG CON NGƯỜI** | Text vàng đậm, stagger chữ "GIẢI PHÓNG", pulse glow | *(continuation)* "giải phóng con người." |
| **3.0-4.0s** | Twist | `ai_burnout_1.jpeg` | **NHƯNG...** | Chữ đỏ to, giật màn hình, zoom in nhanh 1.2x | *(pause 0.5s)* "Nhưng..." |
| **4.0-5.5s** | Reality | `sleeping_dev_1.jpg` | **SỰ THẬT LÀ** | Cross-fade ảnh sang sleeping_dev, chữ trắng fade in, slide từ phải | "sự thật là..." |
| **5.5-6.5s** | Reveal | `sleeping_dev_1.jpg` | 🔴 **BREAKING** | Badge đỏ pulsing ở góc phải, chữ nhỏ "07/2026" bên dưới | "lập trình viên..." |
| **6.5-8.5s** | Shock | `sleeping_dev_1.jpg` | **LẬP TRÌNH VIÊN** | Chữ to fade in từ giữa, scale 0.5→1.05, bounce nhẹ | "lập trình viên đang ngủ gục..." |
| **8.5-10.0s** | Hook 2 | `sleeping_dev_1.jpg` | **NGỦ GỤC GIỮA NGÀY** | Chữ đỏ, stagger từng chữ rơi xuống, shake nhẹ | "ngủ gục giữa ngày..." |
| **10.0-11.0s** | Bối cảnh | `ai_burnout_2.jpeg` | **VÌ KIỆT SỨC** | Cross-fade ảnh mới, chữ vàng cam nóng | "vì kiệt sức..." |
| **11.0-12.5s** | Cause | `ai_burnout_2.jpeg` | **QUẢN LÝ AI AGENT** | Chữ trắng, typewriter effect từng chữ xuất hiện nhanh | "quản lý AI Agent." |
| **12.5-14.0s** | Quote | `multitask_1.jpg` | *"Nếu bạn ngủ, bạn sẽ không ở bên 20 AI agent"* | Chữ nghiêng trắng, border mờ, fade in từ dưới | "Nếu bạn ngủ, bạn sẽ không ở bên 20 AI agent của mình." |
| **14.0-15.0s** | CTA | `multitask_1.jpg` | 📖 **ĐỌC FULL PHÂN TÍCH** | Box đen mờ, chữ vàng, slide up từ dưới | "Đọc phân tích đầy đủ trên..." |
| **15.0-15.8s** | Link | `multitask_1.jpg` | **next-blog-vert.vercel.app** | Link nhỏ ở dưới, fade out cùng audio kết thúc | "next-blog-vert.vercel.app" |

---

### Chi tiết animation mỗi scene

#### Scene 1: AI hứa (0-3s)
```
0.0s: Ảnh bg scale 1.25→1.08 (zoom out chậm)
0.2s: "AI HỨA SẼ" slide up 80px, opacity 0→1, ease back.out(1.5)
1.0s: "GIẢI PHÓNG" text vàng, scale 0.5→1.05→1.0, stagger 0.1s/chữ
2.0s: "CON NGƯỜI" fade in nhẹ bên dưới
```

#### Scene 2: Twist "NHƯNG..." (3-5.5s)
```
3.0s: "NHƯNG..." chữ đỏ #ff4444, size 80px, zoom in từ 0.3→1.2→1.0
3.8s: 3 dấu chấm xuất hiện từng cái, stagger 0.3s
4.5s: Cross-fade ảnh sang sleeping_dev
5.0s: "SỰ THẬT LÀ" fade in từ phải sang
```

#### Scene 3: BREAKING + LTV ngủ gục (5.5-10s)
```
5.5s: Badge "🔴 BREAKING" slide in từ phải, pulse dot animation
6.8s: "LẬP TRÌNH VIÊN" chữ trắng to 72px, từ giữa bung ra
8.5s: "NGỦ GỤC GIỮA NGÀY" chữ đỏ, stagger rơi từ trên xuống
9.0s: Hiệu ứng shake nhẹ cả màn hình (2px, 0.1s)
```

#### Scene 4: Nguyên nhân (10-12.5s)
```
10.0s: Cross-fade sang ảnh ai_burnout_2
10.3s: "VÌ KIỆT SỨC" text vàng cam, glow effect
11.2s: "QUẢN LÝ AI AGENT" typewriter effect, mỗi chữ 0.05s
```

#### Scene 5: Quote + CTA (12.5-15.8s)
```
12.5s: Cross-fade sang ảnh multitask
13.0s: Quote fade in, border mờ 2px, nền đen 60% opacity
14.2s: CTA box slide up: "📖 ĐỌC FULL PHÂN TÍCH" (vàng)
15.0s: Link blog hiện dưới cùng, text nhỏ trắng mờ
15.8s: Fade out toàn bộ
```

---

### Text overlay style

| Loại text | Font | Size | Màu | Hiệu ứng |
|-----------|------|------|-----|----------|
| Headline shock | Roboto 900 | 72px | #fff | text-shadow lớn |
| Highlight keyword | Roboto 900 | 80px | #FFD700 (vàng) | glow + scale pulse |
| Twist text | Roboto 900 | 80px | #ff4444 (đỏ) | zoom + shake |
| Sub-text | Roboto 700 | 36px | rgba(255,255,255,0.9) | fade in |
| Quote italic | Roboto 700 italic | 34px | rgba(255,255,255,0.95) | border box |
| CTA | Roboto 900 | 38px | #FFD700 | slide up |
| Link URL | Roboto 700 | 26px | #FFD700 | static |

---

### Ảnh sử dụng

| File | Mô tả | Scene |
|------|-------|-------|
| `ai_burnout_1.jpeg` (3.4MB) | AI/robot dark, dramatic | Scene 1,2 |
| `sleeping_dev_1.jpg` (288KB) | Người ngủ gục trên bàn | Scene 3 |
| `ai_burnout_2.jpeg` (2.5MB) | AI burnout concept | Scene 4 |
| `multitask_1.jpg` (249KB) | Stress, nhiều màn hình | Scene 5 |

---

### Âm thanh
- Giọng: **vi-VN-NamMinhNeural** (Edge TTS)
- Tốc độ: +10%
- File: `script_audio.mp3` (15.84s, 48kbps mono)

---

### Checklist trước khi render
- [ ] Font Roboto load được từ Google Fonts CDN
- [ ] Ảnh copy vào cùng thư mục HTML (path relative)
- [ ] GSAP CDN load được
- [ ] Resolution 1080×1920 (crop/resize trong script)
- [ ] Audio sync đúng timing từng cảnh

---

## 📝 Script giọng đọc

> AI hứa sẽ giải phóng con người. Nhưng sự thật là... lập trình viên đang ngủ gục giữa ngày vì kiệt sức quản lý AI Agent. Nếu bạn ngủ, bạn sẽ không ở bên 20 AI agent của mình. Đọc phân tích đầy đủ trên next-blog-vert.vercel.app.
