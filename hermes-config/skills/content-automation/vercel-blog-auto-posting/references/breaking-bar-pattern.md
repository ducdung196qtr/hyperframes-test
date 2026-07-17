# Breaking Bar — Marquee Ticker Pattern (CORRECTED)

User DOES want horizontal scrolling titles — a classic `<marquee>` style ticker that runs continuously. This session the user said "cho nó chạy đường ngang màn hình đi. và chạy liên tục như ver 1 ấy". The static list version was a misunderstanding from an earlier session.

## CSS (globals.css)

```css
.breaking-bar { background: #1e3a5f; padding: 14px 0; overflow: hidden; }
.breaking-bar .container { display: flex; align-items: center; gap: 16px; }
.breaking-label {
  flex-shrink: 0;
  display: inline-flex; align-items: center; gap: 6px;
  background: #ef4444; color: #fff;
  padding: 6px 16px; font-size: 11px; font-weight: 800;
  border-radius: 4px; letter-spacing: 0.08em;
  box-shadow: 0 2px 12px rgba(239,68,68,0.5);
  animation: breakingPulse 2s ease-in-out infinite;
}
@keyframes breakingPulse {
  0%, 100% { box-shadow: 0 2px 12px rgba(239,68,68,0.5); }
  50% { box-shadow: 0 4px 24px rgba(239,68,68,0.7); }
}

.breaking-text { overflow: hidden; flex: 1; position: relative; height: 22px; }
.breaking-text-track {
  display: flex; gap: 48px;
  position: absolute; white-space: nowrap;
  animation: ticker 22s linear infinite;
}
.breaking-text-track:hover { animation-play-state: paused; }
.breaking-text-track a {
  color: rgba(255,255,255,0.95); font-size: 14px; font-weight: 500;
  flex-shrink: 0; transition: color 0.2s;
}
.breaking-text-track a:hover { color: #fff; text-decoration: underline; }

@keyframes ticker {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
```

## HTML (page.js)

**CRITICAL**: Must duplicate the title list twice — `[...titles, ...titles]` — so that when the first copy scrolls off-screen, the second copy enters from the right. Without duplication there's a visible gap.

```jsx
<div className="breaking-bar">
  <div className="container">
    <span className="breaking-label">BREAKING</span>
    <div className="breaking-text">
      <div className="breaking-text-track">
        {[...allPosts.slice(0, 5), ...allPosts.slice(0, 5)].map((p, i) => (
          <Link key={`${p.slug}-${i}`} href={`/posts/${p.slug}`}>
            {p.title}
          </Link>
        ))}
      </div>
    </div>
  </div>
</div>
```

## Why this works

- `translateX(0)` → `translateX(-50%)`: because we have 2 copies of the list, shifting left by 50% reveals the second copy seamlessly
- `gap: 48px` between titles — visual separation
- `flex-shrink: 0` on links — prevents titles from wrapping
- Hover pauses animation — user can read a specific title
- Each title is a clickable `<Link>` to the post

## Key points

- Background: **solid `#1e3a5f`** (NOT gradient — user said "bg thì lấy 1 màu thôi màu nhạt nhạt là oke")
- BREAKING badge: red `#ef4444` with pulsing glow
- Animation: `translateX(0)` → `translateX(-50%)` — NOT `translateX(100%)` → `translateX(-100%)` (that needs a reference point that doesn't exist)
- Each title is a clickable `<Link>` to the post
- Hover pauses the animation
