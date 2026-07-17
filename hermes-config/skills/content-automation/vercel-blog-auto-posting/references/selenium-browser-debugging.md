# Selenium Browser Debugging for Vercel Sites

Use this when the user reports visual bugs ("dark mode không hoạt động", "ảnh vỡ", "chữ sát hình") but you can't access browser tools. Deploy fixes, then verify with a headless browser that takes real screenshots and checks computed CSS values.

## Prerequisites

```bash
pip install selenium webdriver-manager
```

## Finding Chrome on the server

Windows Server 2012R2 may have Chrome installed even if it doesn't show up in PATH:

```bash
find /c/Program\ Files* -name "chrome.exe" 2>/dev/null
```

Common paths:
- `C:\Program Files (x86)\Google\Chrome\Application\chrome.exe`
- `C:\Program Files\Google\Chrome\Application\chrome.exe`

## Verification script template

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

chrome_path = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

options = Options()
options.binary_location = chrome_path
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1440,900")

driver = webdriver.Chrome(options=options)

# 1. Screenshot light mode
driver.get("https://next-blog-vert.vercel.app")
time.sleep(3)
driver.save_screenshot("web-light.png")

# 2. Toggle dark mode and verify
toggle = driver.find_element("css selector", ".dark-toggle")
toggle.click()
time.sleep(1)

has_dark = driver.execute_script(
    "return document.documentElement.classList.contains('dark')"
)
print(f"dark mode active: {has_dark}")

bg = driver.execute_script(
    "return getComputedStyle(document.body).backgroundColor"
)
print(f"body bg: {bg}")

driver.save_screenshot("web-dark.png")

# 3. Check spacing
cards = driver.find_elements("css selector", ".post-card")
if cards:
    img = cards[0].find_element("css selector", ".card-img")
    body = cards[0].find_element("css selector", ".card-body")
    img_rect = img.rect
    body_rect = body.rect
    gap = body_rect['y'] - (img_rect['y'] + img_rect['height'])
    print(f"card gap: {gap}px (should be > 0)")

# 4. Check hero image quality
hero_img = driver.find_element("css selector", ".hero-main-img img")
src = hero_img.get_attribute("src")
print(f"hero img: {src[:100]}...")

driver.quit()
```

## Key checks

| Check | Method | Expected |
|-------|--------|----------|
| Dark mode active | `documentElement.classList.contains('dark')` | `True` after click |
| Body background | `getComputedStyle(body).backgroundColor` | `rgb(15, 23, 42)` in dark |
| Image quality | `heroImg.getAttribute('src')` | Contains `w=1600` not `w=1200` |
| Card spacing | `bodyTop - imgBottom` | `> 2px` (not 0.25px) |
| Hero visible | `hero.rect.height` | `> 0` |

## Node.js alternative (when Selenium can't install)

If Selenium/Chrome fails, use a lightweight Node.js script to fetch and analyze deployed HTML/CSS:

```javascript
const https = require('https');
const html = await fetch('https://next-blog-vert.vercel.app');

// Check dark mode CSS selector
const cssUrl = html.match(/href="(\/_next\/static\/css\/[^"]+\.css)"/)[1];
const css = await fetch('https://next-blog-vert.vercel.app' + cssUrl);

console.log('html.dark in CSS:', css.includes('html.dark'));
console.log('1600px images:', (html.match(/w=1600/g) || []).length);
```

This approach confirms whether fixes are actually deployed to Vercel's CDN but can't verify visual rendering quality — for that, only a real browser screenshot will do.
