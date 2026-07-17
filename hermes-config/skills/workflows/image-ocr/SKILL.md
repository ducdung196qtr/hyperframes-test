---
name: image-ocr
description: "Extract text from images when native vision tools are unavailable. Multi-tier fallback chain: vision_analyze, local OCR (easyocr/tesseract), OCR.space API."
---

# Image OCR — Text Extraction from Images

## Trigger
Use this when:
- User sends an image and asks you to analyze/read it
- `vision_analyze` fails (model lacks vision, environment doesn't support it)
- You need to extract text from a screenshot, photo, or document image

## Fallback Chain (try in order)

### Tier 1: vision_analyze
Always try first — simplest when supported.
```
vision_analyze(image_url=..., question="Describe this image in detail...")
```
If it returns an error about vision not being supported, move to Tier 2.

### Tier 2: Local OCR (easyocr or tesseract)
Check what's available:
```bash
pip list | grep -iE "easyocr|pytesseract"
which tesseract
```

- **easyocr**: `pip install easyocr` — needs torch (DLL issues possible on Windows). Use `Reader(['vi', 'en'], gpu=False)`.
- **pytesseract**: `pip install pytesseract` — needs tesseract binary installed separately.

If either works, run OCR directly. If both fail (missing deps, DLL errors, no tesseract binary), move to Tier 3.

### Tier 3: OCR.space API (reliable fallback)
**Always works.** No local dependencies beyond Python stdlib + Pillow.

```python
from PIL import Image
import base64, urllib.request, urllib.parse, json
from io import BytesIO

img = Image.open(r'path/to/image.jpg')
w, h = img.size
if w > 1024:
    ratio = 1024 / w
    img = img.resize((1024, int(h * ratio)))

buffer = BytesIO()
img.save(buffer, format='JPEG', quality=85)
b64 = base64.b64encode(buffer.getvalue()).decode()

url = 'https://api.ocr.space/parse/image'
data = urllib.parse.urlencode({
    'apikey': 'helloworld',  # free tier — 500 req/day
    'base64Image': f'data:image/jpeg;base64,{b64}',
    'language': 'eng',       # use 'eng' even for Vietnamese text
    'isOverlayRequired': 'true',
}).encode()

req = urllib.request.Request(url, data=data)
resp = urllib.request.urlopen(req, timeout=30)
result = json.loads(resp.read())
if result.get('ParsedResults'):
    for r in result['ParsedResults']:
        print(r.get('ParsedText', ''))
```

### Critical: Language Code
OCR.space **rejects `language='vie'`** with error `E201: Value for parameter 'language' is invalid`. Always use `'eng'` — it still detects Vietnamese characters (with diacritics). The OCR engine handles Unicode text regardless of the language parameter.

## Pitfalls

- **easyocr + Windows**: torch DLL initialization errors (`c10.dll`) are common. Don't spend time debugging — jump straight to Tier 3.
- **tesseract**: Not pre-installed on most systems. Chocolatey might not be available. Downloading from GitHub releases can be slow/hang. Skip directly to Tier 3 if it's not already present.
- **OCR.space rate limits**: Free tier is 500 requests/day. The `helloworld` API key is public and shared across users. For heavy use, register for a personal key at ocr.space.
- **Image size limit**: OCR.space has a 1MB base64 payload limit. Always resize images to max 1024px width before encoding.
