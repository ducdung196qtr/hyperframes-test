# Image + Text Split Layout (TikTok 1080×1920)

User rejected dim-overlay full-frame backgrounds — wants image and text as distinct visible zones for trust/credibility.

## CSS Pattern

```css
/* Scene container — full frame, flex column */
.scene {
  position: absolute; inset: 0;
  display: flex; flex-direction: column;
  opacity: 0;  /* controlled by GSAP */
}

/* IMAGE ZONE — top 62% */
.img-zone {
  width: 100%; height: 62%;
  position: relative; overflow: hidden;
}
.img-zone img {
  width: 100%; height: 100%;
  object-fit: cover; display: block;
}
/* Gradient mask fades image bottom into text zone */
.img-gradient {
  position: absolute; inset: 0;
  background: linear-gradient(180deg, 
    transparent 60%,
    rgba(10,15,26,0.6) 85%,
    #0a0f1a 100%
  );
}

/* TEXT ZONE — bottom 38%, solid dark background */
.text-zone {
  width: 100%; height: 38%;
  display: flex; flex-direction: column;
  align-items: center; justify-content: flex-start;
  padding: 25px 55px 30px;
  background: #0a0f1a;  /* matches body bg */
}

/* Scanlines + vignette OVERLAY everything */
.scanlines { /* repeating-linear-gradient, z-index: 996 */ }
.vignette  { /* radial-gradient, z-index: 995 */ }
```

## Font Sizes

- Headline: `82–100px` (Oswald 700)
- Subtext: `28–34px` (Inter/Helvetica 300)
- Badge: `26–30px` (Oswald 700, red bg)
- Stat big: `140–160px` (Oswald 700)
- Quote: `32–38px` (Inter 300 italic)
- CTA button: `34–38px` (Oswald 700, gold bg)

## Colors

| Token | Hex | Use |
|-------|-----|-----|
| Body bg | `#0a0f1a` | Background |
| Text white | `#ffffff` | Headlines |
| Gold accent | `#FFC300` | Key phrases, CTA |
| Red accent | `#E71D36` | Badge, twist text |
| Cyan accent | `#06b6d4` | Stat numbers |
| Muted subtext | `rgba(255,255,255,0.7)` | Descriptions |

## Image Requirements

- 1080×1920 or larger portrait orientation
- Copy to same directory as HTML for relative `<img src="...">` paths
- Use `<img>` tag (not CSS `background-image`) in `.img-zone`
