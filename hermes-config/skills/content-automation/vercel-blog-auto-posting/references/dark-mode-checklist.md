# Dark Mode Setup Checklist (Next.js + Vercel Blog)

This is the proven pattern from the ducdung196qtr/next-blog session (2026-07-16).
**UPDATED 2026-07-16**: Added `html.dark` selector fix and `.dark`-inside-`:root` gotcha.

## 3 pieces you MUST have for dark mode to work without flash:

### 1. Anti-flash script (layout.js `<head>`)

```jsx
<script
  dangerouslySetInnerHTML={{
    __html: `
      (function(){
        try {
          var t = localStorage.getItem('theme');
          if (t === 'dark' || (!t && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
          }
        } catch(e){}
      })();
    `,
  }}
/>
```

This runs BEFORE paint — zero white flash. Targets `document.documentElement` (the `<html>` element).

### 2. CSS — `html.dark` block (globals.css)

This is the #1 source of dark-mode failures. **The `.dark` block MUST be a standalone selector `html.dark`, NOT nested inside `:root {}`.**

```css
/* ✅ CORRECT — standalone block */
:root {
  --bg: #ffffff;
  --text: #1e293b;
  /* ...all light vars... */
}

html.dark {
  --bg: #1a1f2e;              /* pastel dark — user rejected #0f172a as "xấu" */
  --bg-soft: #232839;
  --bg-card: #262b3a;
  --text: #c8cfda;
  --text-strong: #e8edf5;
  --text-soft: #8a94a6;
  --text-muted: #5a6478;
  --brand: #3b82f6;        /* slightly brighter in dark mode */
  --brand-hover: #60a5fa;
  --brand-light: #1e3a5f;
  --brand-subtle: #172033;
  --border: #353b4a;
  --border-soft: #2a2f3c;
}

html.dark .site-header { background: rgba(26,31,46,0.92); }
html.dark img { opacity: 0.92; }
html.dark .hero-main-overlay { 
  background: linear-gradient(to top,
    rgba(2,6,23,0.9) 0%, 
    rgba(2,6,23,0.3) 60%, 
    transparent 100%
  ); 
}
```

```css
/* ❌ WRONG — nesting .dark inside :root produces ":root .dark"
   which only matches <html>...</html> → <div class="dark"> inside root,
   NOT <html class="dark"> */
:root {
  --bg: #fff;
  .dark {
    --bg: #000;   /* NEVER fires! */
  }
}
```

**Use `html.dark` (not bare `.dark`) as the selector.** While `.dark` alone technically works, `html.dark` has higher specificity and is explicit about what element carries the class — matching the JS which uses `document.documentElement.classList`.

### 3. Toggle button (Header.js — client component)

```jsx
'use client';
const [dark, setDark] = useState(false);

useEffect(() => {
  const saved = localStorage.getItem('theme');
  if (saved === 'dark' || (!saved && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    setDark(true);
    document.documentElement.classList.add('dark');
  }
}, []);

const toggleDark = () => {
  const next = !dark;
  setDark(next);
  document.documentElement.classList.toggle('dark', next);
  localStorage.setItem('theme', next ? 'dark' : 'light');
};
```

### Button

```jsx
<button className="icon-btn" onClick={toggleDark} aria-label="Dark mode">
  {dark ? '☀️' : '🌙'}
</button>
```

## Common mistakes

- ❌ Only having the toggle JS without the anti-flash script → white flash on reload
- ❌ Nesting `.dark {}` inside `:root {}` → becomes `:root .dark` which never matches `<html class="dark">`
- ❌ Only having CSS `.dark` without JS → nothing toggles
- ❌ Using `prefers-color-scheme` in CSS media query instead of class toggle → can't override
- ❌ Forgetting to call `document.documentElement.classList.toggle()` in useEffect on mount → toggle out of sync
- ❌ Using `document.body` instead of `document.documentElement` → CSS on `html.dark` won't match
- ❌ Using `#0f172a` (slate-900) as the dark background — user rejected as "rất xấu" (very ugly). Use `#1a1f2e` (pastel dark blue-gray) — softer, more professional, easier on the eyes. The entire palette should shift to lighter tones: cards `#262b3a`, text `#c8cfda`, borders `#353b4a`.
