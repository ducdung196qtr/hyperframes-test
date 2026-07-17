# OCR.space API Reference

## Endpoint
```
POST https://api.ocr.space/parse/image
```

## Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| `apikey` | `helloworld` | Free tier, 500 req/day. Shared key. |
| `base64Image` | `data:image/jpeg;base64,...` | Max ~1MB payload |
| `language` | `eng` | DO NOT use `vie` — returns error E201 |
| `isOverlayRequired` | `true` | Includes word-level bounding boxes |

## Supported Languages (confirmed working)
- `eng` — English, but also handles Unicode/Vietnamese diacritics fine
- `ara`, `chs`, `cht`, `fre`, `ger`, `ita`, `jpn`, `kor`, `por`, `rus`, `spa`, etc.

## Language Codes That FAIL
- `vie` → `E201: Value for parameter 'language' is invalid`

## Error Transcript (from session 2026-07-16)
```
Lỗi: ["E201: Value for parameter 'language' is invalid"]
{
  "OCRExitCode": 99,
  "IsErroredOnProcessing": true,
  "ErrorMessage": [
    "E201: Value for parameter 'language' is invalid"
  ],
  "ProcessingTimeInMilliseconds": "0"
}
```

## Response Shape (success)
```json
{
  "ParsedResults": [
    {
      "TextOverlay": { ... },
      "ParsedText": "Results for \"telegram\"\n\nMac AppS iPhone ...",
      "FileParseExitCode": 1,
      "ErrorMessage": "",
      "ErrorDetails": ""
    }
  ],
  "OCRExitCode": 1,
  "IsErroredOnProcessing": false,
  "ProcessingTimeInMilliseconds": "1234"
}
```

## Image Preparation
- Resize to max 1024px width before base64 encoding
- JPEG quality 85 is a good balance
- Pillow `Image.resize()` with proportional height
