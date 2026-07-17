# 🐧 Hướng Dẫn Cài Đặt & Khôi Phục Hệ Thống
## Từ Windows Server 2012 → Ubuntu Server 24.04 LTS

> **Ngày backup cuối:** 17/07/2026
> **GitHub repos:** `ducdung196qtr/next-blog` + `ducdung196qtr/hyperframes-test`

---

## Bước 1: Cài Ubuntu Server 24.04 LTS

### 1.1 Tải ISO
```
https://releases.ubuntu.com/24.04/ubuntu-24.04.1-live-server-amd64.iso
```

### 1.2 Cài đặt (summary)
- Chọn **Minimal installation** (không cần GUI)
- Tạo user: tên gì cũng được (sẽ dùng để chạy Hermes)
- **QUAN TRỌNG:** Chọn **Install OpenSSH server** khi được hỏi
- RAM tối thiểu: 2GB (nên có swap 4GB)

### 1.3 Sau khi cài xong — SSH vào
```bash
ssh your-user@<địa-chỉ-IP>
```

---

## Bước 2: Cài Đặt Toolchain Cơ Bản

### 2.1 Update & cài package manager
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl wget unzip build-essential python3 python3-pip python3-venv nodejs npm
```

### 2.2 Cài FFmpeg
```bash
sudo apt install -y ffmpeg
ffmpeg -version   # Kiểm tra: phải thấy version 6.x hoặc 7.x
```

### 2.3 Cài Chrome + ChromeDriver (cho Selenium)
```bash
# Chrome stable
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update && sudo apt install -y google-chrome-stable

# Kiểm tra
google-chrome --version

# ChromeDriver (tự cài qua pip)
pip install selenium webdriver-manager
```

---

## Bước 3: Clone Repos Về

```bash
cd ~

# Next-blog
git clone https://github.com/ducdung196qtr/next-blog.git

# HyperFrames (có luôn Hermes config backup)
git clone https://github.com/ducdung196qtr/hyperframes-test.git
```

---

## Bước 4: Cài Hermes Agent

### 4.1 Cài Hermes
```bash
pip install hermes-agent
```

### 4.2 Khôi phục cấu hình
```bash
# Config
cp ~/hyperframes-test/hermes-config/config.yaml ~/.hermes/config.yaml

# Memory (giữ lại mọi thứ Hermes đã biết về bạn)
mkdir -p ~/.hermes/memories
cp ~/hyperframes-test/hermes-config/MEMORY.md ~/.hermes/memories/MEMORY.md
cp ~/hyperframes-test/hermes-config/USER.md ~/.hermes/memories/USER.md

# Skills (tất cả skill đã save)
mkdir -p ~/.hermes/skills
cp -r ~/hyperframes-test/hermes-config/skills/* ~/.hermes/skills/
```

### 4.3 Sửa API key & Token
Mở `~/.hermes/config.yaml`, sửa 2 chỗ:
```yaml
# Dòng model.api_key → thay YOUR_TOKEN bằng GitHub token thật
# Dòng custom_providers[0].api_key → thay YOUR_TOKEN bằng GitHub token thật
```

**Lấy token từ đâu?**: Vào https://github.com/settings/tokens → copy token `ghp_...`

### 4.4 Kiểm tra
```bash
hermes --version
hermes config show
hermes skills list
```

---

## Bước 5: Khôi Phục Next-Blog

### 5.1 Cài dependencies
```bash
cd ~/next-blog
npm install
```

### 5.2 Kiểm tra chạy local
```bash
npm run dev
# Mở browser: http://localhost:3000
# Phải thấy dark mode + bài viết tiếng Việt
```

### 5.3 Deploy lên Vercel (nếu cần)
```bash
npx vercel --token <VERCEL_TOKEN> --yes --prod
```

---

## Bước 6: Khôi Phục HyperFrames Pipeline

### 6.1 Cài dependencies Python
```bash
cd ~/hyperframes-test
pip install selenium pillow edge-tts gtts requests
```

### 6.2 Kiểm tra HTML render
```bash
python render_deconstructed.py
# Nếu báo lỗi Chrome/chromedriver → chạy lệnh này:
# sudo apt install -y chromium-chromedriver
# export PATH=$PATH:/usr/lib/chromium-browser/
```

### 6.3 Kiểm tra ảnh
Ảnh gốc không được backup (file nặng). Cần tải lại:
```bash
cd ~/hyperframes-test
# Tải ảnh mới từ Pexels/Unsplash (tự làm hoặc nhờ Hermes)
```

---

## Bước 7: Kết Nối Telegram

### 7.1 Lấy Hermes gateway token
```bash
hermes gateway start
# Sẽ hiện URL + token để kết nối Telegram
```

### 7.2 Kết nối bot Telegram
- Vào Telegram tìm bot Hermes của bạn
- Gửi `/start` + token từ bước trên
- Xác nhận kết nối

### 7.3 Kiểm tra
```bash
hermes status
# Phải thấy: Telegram ✅ connected
```

---

## Bước 8: Test Tổng Hợp

```bash
# 1. Blog chạy?
cd ~/next-blog && npm run build && echo "✅ Blog OK"

# 2. Hermes hoạt động?
hermes --version && echo "✅ Hermes OK"

# 3. TTS hoạt động?
python -c "
from edge_tts import Communicate
import asyncio
async def t(): 
    await Communicate('Xin chào','vi-VN-NamMinhNeural').save('/tmp/test.mp3')
asyncio.run(t())
" && echo "✅ TTS OK"

# 4. Chrome headless hoạt động?
python -c "
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
o=Options(); o.add_argument('--headless')
d=webdriver.Chrome(options=o); d.get('https://google.com')
print('✅ Chrome OK'); d.quit()
"

# 5. FFmpeg hoạt động?
ffmpeg -version && echo "✅ FFmpeg OK"
```

---

## Cấu Trúc File Sau Khi Khôi Phục

```
~/
├── next-blog/           ← Blog Next.js
│   ├── content/posts/   ← Bài viết Markdown
│   └── ...
├── hyperframes-test/    ← Pipeline TikTok
│   ├── index.html       ← Template video
│   ├── render_deconstructed.py
│   ├── assets/sfx/      ← 6 SFX files
│   └── hermes-config/   ← Backup cấu hình
└── .hermes/             ← Hermes config (đã khôi phục)
    ├── config.yaml
    ├── memories/
    │   ├── MEMORY.md    ← Những gì Hermes biết
    │   └── USER.md      ← Profile của Đức Dũng
    └── skills/          ← Tất cả skill
```

---

## Tóm Tắt Các Lệnh (Copy-Paste 1 Lần)

```bash
# === TOÀN BỘ CÀI ĐẶT ===
sudo apt update && sudo apt upgrade -y
sudo apt install -y git curl wget unzip python3 python3-pip python3-venv nodejs npm ffmpeg google-chrome-stable

# Hermes
pip install hermes-agent selenium pillow edge-tts gtts

# Clone
cd ~ && git clone https://github.com/ducdung196qtr/next-blog.git
cd ~ && git clone https://github.com/ducdung196qtr/hyperframes-test.git

# Restore config
mkdir -p ~/.hermes/memories ~/.hermes/skills
cp ~/hyperframes-test/hermes-config/config.yaml ~/.hermes/config.yaml
cp ~/hyperframes-test/hermes-config/MEMORY.md ~/.hermes/memories/
cp ~/hyperframes-test/hermes-config/USER.md ~/.hermes/memories/
cp -r ~/hyperframes-test/hermes-config/skills/* ~/.hermes/skills/

# Blog
cd ~/next-blog && npm install

echo "=== DONE === Đừng quên sửa token trong ~/.hermes/config.yaml!"
```

---

## ⚠️ Những Thứ KHÔNG ĐƯỢC Backup

| Thứ | Cần làm lại |
|-----|-------------|
| Ảnh video (`*.jpeg`, `*.jpg`) | Tải lại từ Pexels/Unsplash |
| File TTS audio (`script_audio_*.mp3`) | Tạo lại bằng edge-tts |
| Video đã render (`*.mp4`) | Render lại |
| Vercel token | Lấy từ Vercel dashboard |

---

## 🔧 Troubleshooting

| Lỗi | Fix |
|-----|-----|
| `chrome not found` | `sudo apt install -y google-chrome-stable` |
| `chromedriver not found` | `pip install webdriver-manager` |
| `hermes: command not found` | `export PATH=$PATH:~/.local/bin` hoặc `pip install --user hermes-agent` |
| `edge-tts NoAudioReceived` | Đợi vài phút (rate limit) hoặc dùng `text_to_speech` tool của Hermes |
| `git push bị lỗi auth` | Sửa token trong remote URL: `git remote set-url origin https://ducdung196qtr:TOKEN@github.com/...` |

---

*Backup tạo lúc 11:20 ngày 17/07/2026 — Hermes Agent sẽ nhớ mọi thứ từ MEMORY.md + USER.md*
