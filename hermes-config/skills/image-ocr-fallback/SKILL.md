---
name: image-ocr-fallback
description: OCR approaches for reading text from images when vision models are unavailable or fail. Use when vision_analyze returns "not supported" and local OCR tools (tesseract, easyocr) are not installed or fail.
---

## Trigger
- User sends an image expecting analysis but `vision_analyze` returns "not supported" or fails
- Need to extract text from screenshots, memes, or document photos without vision capability

## Workflow

### Step 1: Confirm the image exists and inspect metadata
```bash
ls -la "<image_path>"
file "<image_path>"
python -c "from PIL import Image; img=Image.open('<path>'); print(img.size, img.mode, img.format)"
```

### Step 2: Try local OCR tools (fast path)
```bash
# Check availability
which tesseract
pip list | grep -iE "pytesseract|easyocr|pillow"

# If tesseract available:
tesseract "<image_path>" stdout -l vie+eng

# If easyocr available:
python -c "import easyocr; r=easyocr.Reader(['vi','en'],gpu=False); print(r.readtext('<image_path>'))"
```

### Step 3: OCR.space free API (reliable fallback)
When local tools fail or are missing, use OCR.space free tier. **Language codes**: `eng` for English, `vie` for Vietnamese. Only one language at a time. Best results usually come from `eng` even for Vietnamese screenshots, as it catches Latin characters in mixed text.

```python
from PIL import Image
import base64, urllib.request, urllib.parse, json, io

img = Image.open(r'<image_path>')
w, h = img.size
if w > 1024:
    img = img.resize((1024, int(h * w / 1024)))

buf = io.BytesIO()
img.save(buf, format='JPEG', quality=85)
b64 = base64.b64encode(buf.getvalue()).decode()

url = 'https://api.ocr.space/parse/image'
data = urllib.parse.urlencode({
    'apikey': 'helloworld',  # free tier, limited rate
    'base64Image': f'data:image/jpeg;base64,{b64}',
    'language': 'eng',
    'isOverlayRequired': 'true',
}).encode()

req = urllib.request.Request(url, data=data)
resp = urllib.request.urlopen(req, timeout=30)
result = json.loads(resp.read())
for r in result.get('ParsedResults', []):
    print(r.get('ParsedText', ''))
```

### Step 4: ASCII art preview (last resort)
When OCR returns nothing useful, generate an ASCII art preview to see the image structure:
```python
from PIL import Image
img = Image.open(r'<image_path>')
gray = img.convert('L')
w, h = img.size
scale = 8
for y in range(0, h, scale):
    line = ''
    for x in range(0, w, scale//2):
        px = gray.getpixel((x, y))
        line += '#' if px < 40 else '8' if px < 80 else 'o' if px < 120 else '.' if px < 180 else ' '
    if line.strip():
        print(line)
```

## Pitfalls

- **easyocr on Windows Server**: frequently fails with `OSError: [WinError 1114] DLL initialization routine failed` due to PyTorch DLL issues on older Windows. Don't spend time debugging — fall back to OCR.space immediately.
- **OCR.space language codes**: `'vie'` and `'vi'` return `"E201: Value for parameter 'language' is invalid"`. Use `'eng'` which captures Latin chars well enough for Vietnamese in screenshots.
- **Tesseract Windows install**: `choco install tesseract` fails without Chocolatey. Manual download from UB-Mannheim GitHub releases is unreliable via curl. Skip and use OCR.space.
- **OCR.space free tier**: limited rate, use sparingly. Results may be truncated.
