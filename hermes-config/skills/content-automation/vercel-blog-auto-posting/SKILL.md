---
name: vercel-blog-auto-posting
description: Build and auto-publish to a Next.js blog on Vercel using Markdown content and Git-push deployment. A lightweight, free alternative to WordPress for automated news blogs.
triggers:
  - User wants a blog but lacks server resources (low RAM, no hosting)
  - User asks about Vercel, Next.js, or static blog for auto-posting
  - User wants a free, fast blog with automated daily content
  - User mentions 'blog tĩnh', 'Vercel', 'Next.js blog', 'static blog'
  - WordPress is too heavy for the user's server
---

# Vercel Blog Auto-Posting

Build a free, fast news blog on Vercel with Next.js + Markdown. Content lives as `.md` files in Git; Vercel rebuilds on every push. An AI-powered Python script creates posts and commits them automatically.

**When to prefer this over WordPress:**
- Server has ≤2GB RAM (no room for Apache + MySQL)
- User wants free hosting (Vercel's free tier is generous)
- User prefers Nuxt/Next.js over PHP
- Speed matters (Vercel CDN is globally fast)
- User is comfortable with Git (or the agent manages it)

## Architecture

```
content/posts/*.md   ← Python auto_post.py creates these
     ↓ git push
Vercel detects push → npm run build → SSG pages deployed to CDN
     ↓
Users see the blog at https://your-domain.vercel.app
```

No database, no PHP, no ongoing server costs. Vercel's free tier covers:
- 100GB bandwidth/month
- 100 deployments/day
- Unlimited sites

## Project scaffold

```
next-blog/
  content/posts/         # Markdown posts (one .md per post)
  public/images/         # Static assets
  src/
    app/
      layout.js          # Root layout (Header + Footer + globals.css)
      page.js            # Homepage (hero + card grid)
      globals.css        # CSS variables, dark mode, responsive
      posts/[slug]/page.js  # Single post (SSG)
      category/[category]/page.js  # Category archive
      trending/page.js   # Trending posts
      about/page.js      # About page
    components/
      Header.js          # Sticky nav, dark mode toggle, mobile menu, search
      Footer.js          # 3-column footer + copyright
      PostCard.js        # Reusable card (hero + grid variants)
    lib/
      posts.js           # getAllPosts(), getPostBySlug(), gray-matter parsing
  scripts/
    auto_post.py         # Creates .md files from news data
  next.config.js
  package.json
  jsconfig.json          # @/ path alias
  .gitignore
```

## Key dependencies

```json
{
  "dependencies": {
    "next": "^15.0.0",
    "react": "^19.0.0",
    "react-dom": "^19.0.0",
    "gray-matter": "^4.0.3",
    "reading-time": "^1.5.0"
  }
}
```

No database, no ORM, no CMS. Just Markdown + gray-matter for frontmatter parsing.

## post.js library (src/lib/posts.js)

```javascript
import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

const CONTENT_DIR = path.join(process.cwd(), 'content/posts');

export function getAllPosts() {
  const files = fs.readdirSync(CONTENT_DIR).filter(f => f.endsWith('.md'));
  return files.map(f => {
    const raw = fs.readFileSync(path.join(CONTENT_DIR, f), 'utf8');
    const { data, content } = matter(raw);
    return { slug: f.replace('.md', ''), ...data, excerpt: content.slice(0, 200) };
  }).sort((a, b) => new Date(b.date) - new Date(a.date));
}

export function getPostBySlug(slug) {
  const raw = fs.readFileSync(path.join(CONTENT_DIR, `${slug}.md`), 'utf8');
  const { data, content } = matter(raw);
  return { slug, ...data, content };
}

export function getPostsByCategory(cat) {
  return getAllPosts().filter(p => p.category === cat);
}
```

## Markdown post format

```markdown
---
title: "Post title here"
date: "2026-07-16"
category: "Tin tức"
author: "Đức Dũng"
image: "https://example.com/hero.jpg"
---

## Section heading

Post content in standard Markdown...

> Blockquotes work

- Bullet lists work
- **Bold** and *italic* work
```

Date field is critical — it drives sort order and page metadata.

## Simple Markdown → HTML converter

For the single post page, use a lightweight converter (no external library needed):

```javascript
function convertMarkdown(md) {
  return md
    .replace(/^### (.+)$/gm, '<h3>$1</h3>')
    .replace(/^## (.+)$/gm, '<h2>$1</h2>')
    .replace(/^# (.+)$/gm, '<h1>$1</h1>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/`(.+?)`/g, '<code>$1</code>')
    .replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2">$1</a>')
    .replace(/^\- (.+)$/gm, '<li>$1</li>')
    .replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>')
    .replace(/\n\n/g, '</p><p>');
}
```

## CSS patterns

Use CSS custom properties (`:root`) with an `html.dark` override block. Never nest `.dark` inside `:root {}` — it silently becomes `:root .dark` which doesn't match `<html class="dark">`.

```css
/* Default: deep blue + white + gold accent (user preferred over red) */
:root {
  --brand: #1a56db;
  --brand-hover: #1e40af;
  --brand-light: #dbeafe;
  --brand-subtle: #eff6ff;
  --accent: #f59e0b;          /* gold — for category tags, highlights */
  --bg: #ffffff;
  --bg-soft: #f8fafc;
  --bg-card: #ffffff;
  --bg-footer: #0f172a;        /* dark navy footer — NEVER use Vercel/Next.js branding */
  --text: #1e293b;
  --text-strong: #0f172a;
  --text-soft: #64748b;
  --text-footer: #cbd5e1;
  --border: #e2e8f0;
  --border-soft: #f1f5f9;
  --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
  --font-serif: 'Lora', Georgia, 'Times New Roman', serif;  /* NOT Merriweather */
}
html.dark {
  --brand: #3b82f6;
  --brand-hover: #60a5fa;
  --brand-light: #1e3a5f;
  --brand-subtle: #172033;
  --accent: #fbbf24;
  --accent-subtle: #2d2110;
  --bg: #1e2433;              /* pastel dark — NOT #0f172a (user rejected as "xấu"), NOT #1a1f2e (also rejected) */
  --bg-soft: #242a3a;
  --bg-card: #282e3e;
  --bg-footer: #161b26;
  --text: #c8cfda;
  --text-strong: #e8edf5;
  --text-soft: #8a94a6;
  --text-muted: #5a6478;
  --border: #353b4a;
  --border-soft: #2a2f3c;
  --shadow-xs: 0 1px 2px rgba(0,0,0,0.3);
  --shadow-md: 0 8px 24px rgba(0,0,0,0.5);
  --shadow-lg: 0 16px 48px rgba(0,0,0,0.5);
}

/* Extra dark-mode overrides for elements not fully covered by variables */
html.dark .site-header { background: rgba(26,31,46,0.92); }
html.dark .hero-main-overlay { 
  background: linear-gradient(to top,
    rgba(2,6,23,0.9) 0%, 
    rgba(2,6,23,0.3) 60%, 
    transparent 100%
  ); 
}
html.dark img { opacity: 0.92; }
```

Dark mode persistence: localStorage + `prefers-color-scheme` media query for initial state.

## JS patterns (vanilla, no jQuery)

- Dark mode toggle saves to `localStorage`
- Mobile hamburger menu with CSS transitions on 3 `span` elements
- Sticky header with `scroll` event + `passive: true`
- Breaking news ticker with CSS `@keyframes ticker`

## Dark mode anti-flash pattern

To prevent white flash on page load before JS hydrates, inject an inline `<script>` in `<head>` (layout.js) that reads `localStorage` and sets the `dark` class on `<html>` synchronously — before any paint:

```jsx
// In layout.js <head>
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

The Header component (client-side) then reads the same state and toggles on click. The CSS must define a `.dark` class that overrides `:root` variables. This pattern eliminates the jarring white-to-dark transition on reload.

## Image quality requirements

User explicitly complained about blurry/broken images ("image thì vỡ"). Unsplash images must use:
- **Width**: minimum `w=1600` (not `w=1200` — too small for modern screens)
- **Quality**: `q=90` (not `q=80`)  
- **Format**: Use `?w=1600&q=90` suffix on all Unsplash URLs

Never use `w=1200&q=80` — images will appear blurry on retina/4K displays.

## Spacing guidelines

User complained "chữ với hình sát nhau" (text hugging images). Minimum spacing rules:

| Element | Min padding/margin |
|---------|-------------------|
| `.card-body` padding | `24px 20px 24px` (was 18px — too tight) |
| `.hero-side` padding | `24px 20px` (was 20px) |
| `.hero-side` inner gap | `16px` (was 14px) |
| `.card-img` to `.card-body` | zero gap OK (they abut naturally), but body needs internal top padding |
| `.post-content p` margin-bottom | `22px` minimum |

Cards must feel airy — tight spacing looks amateur.

## Header dark-toggle button pattern

```css
.header-actions { display: flex; align-items: center; gap: 6px; }
.icon-btn {
  width: 38px; height: 38px;
  display: flex; align-items: center; justify-content: center;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: var(--bg-card);
  cursor: pointer;
  font-size: 16px;
  transition: all var(--fast);
  color: var(--text);
}
.icon-btn:hover { background: var(--brand-subtle); border-color: var(--brand); }
```

```jsx
<button className="icon-btn" onClick={toggleDark} aria-label="Dark mode">
  {dark ? '☀️' : '🌙'}
</button>
```

Use emoji icons for the toggle — no external icon library needed.

## Vercel deployment

1. Push code to a **public GitHub repo**
2. Go to [vercel.com](https://vercel.com), sign up with GitHub
3. **Add New → Project** → select the repo
4. Vercel auto-detects Next.js — no config needed
5. Deploy → get a `*.vercel.app` URL instantly
6. Custom domain: Settings → Domains → add your domain

**Every `git push` triggers a rebuild.** Posts appear ~30 seconds after push.

## Python auto-post script pattern

```python
# scripts/auto_post.py
import os, re
from datetime import datetime

CONTENT_DIR = "content/posts"

def slugify(title):
    slug = title.lower()
    # Remove Vietnamese diacritics
    slug = re.sub(r'[đ]', 'd', slug)
    slug = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', slug)
    # ... other chars ...
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    return re.sub(r'\s+', '-', slug.strip())

def create_post(title, content, category="Tin tức", author="Đức Dũng", image=""):
    slug = slugify(title)
    date_str = datetime.now().strftime("%Y-%m-%d")
    filepath = f"{CONTENT_DIR}/{slug}.md"
    if os.path.exists(filepath):
        return  # Skip duplicates
    # Write frontmatter + content
```

## Cronjob pattern

```python
cronjob(action='create',
  schedule='0 7 * * *',
  name='daily-news-publish',
  prompt='Fetch 3-5 hot news articles from VnExpress RSS. For each,
          create a Markdown file in content/posts/ with proper
          Vietnamese titles, 2-3 paragraph content, and category tags.
          Then git add, commit, and push to origin main.',
  enabled_toolsets=['web', 'terminal'])
```

## Pitfalls

1. **`@/` import alias fails**: Must have `jsconfig.json` with `"baseUrl": "src"` and `"paths": {"@/*": ["./*"]}`. Without this, all `import X from '@/components/X'` will fail at build time.
2. **Build fails on Vercel but works locally**: Vercel uses Linux. `gray-matter` reads files with `fs.readFileSync` — ensure paths use `path.join(process.cwd(), ...)` not hard-coded Windows paths.
3. **Image component needs `remotePatterns`**: Next.js blocks external images by default. Add `remotePatterns: [{ protocol: 'https', hostname: '**' }]` to `next.config.js`.
4. **Posts not showing after push**: Vercel only rebuilds on commits to the **default branch**. Make sure you're pushing to `main` or `master`.
5. **Slug collision**: Two posts with the same title → same slug → second overwrites the first. The auto_post script should check for existing files.
6. **Markdown not rendering on Vercel**: The `convertMarkdown` function is called at build time (SSG). If using `dangerouslySetInnerHTML`, make sure the conversion runs in the server component, not the client.
7. **Domain DNS**: Point your domain's A record to `76.76.21.21` (Vercel). Wait for DNS propagation (up to 48 hours, usually 5-30 minutes).
8. **Git push with token on Windows git-bash**: Use URL-embedded auth: `git remote add origin "https://USERNAME:TOKEN@github.com/USERNAME/repo.git"`. This bypasses credential manager issues. Token must have `repo` scope (GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)).
9. **LF/CRLF warnings on Windows**: Git warns about line-ending conversions when files are created with Unix line endings. These are harmless — commit proceeds normally.
10. **Next.js version drift**: Current session used Next.js 16.2.10 (Turbopack). The API surface changed minimally between 15 and 16 for this workflow — check latest stable at install time.
11. **Footer must reflect user's brand, not infrastructure**: Do NOT credit Vercel, Next.js, or any platform in the footer. Use the user's brand name ("NewsPress"), the real author name ("Đức Dũng"), contact email, and social links. Copyright line should say "[Year] [Brand]. Tác giả: [Author]. Mọi quyền được bảo lưu." Dark navy (`--bg-footer: #0f172a`) background with light text. Include 3-4 footer columns: brand intro, categories, about, contact.
12. **Logo**: Minimal — a single letter in a colored block (`logo-icon` div), paired with the site name. No external image dependency.
13. **Vercel deploy requires GitHub**: The repo must exist on GitHub (public or private) before Vercel can import it. No direct upload.
14. **Direct Vercel CLI deploy with token**: Alternatively, install `vercel` globally (`npm install -g vercel`), then run `npx vercel --token <TOKEN> --yes --prod` from the project root. Vercel auto-detects Next.js and deploys. Get the token at https://vercel.com/account/tokens (Create Token → Full Account scope). First deployment also links the GitHub repo automatically for future auto-deploys. Token only appears once — copy immediately.
15. **Dark mode flash / missing dark mode (CRITICAL)**: User rejected the site with "dark mode đâu rồi" (where's dark mode?). Dark mode requires 3 pieces working together: (a) anti-flash inline `<script>` in layout.js `<head>` that adds class to `document.documentElement`, (b) `html.dark` CSS block overriding the same `:root` variables in globals.css **and placed OUTSIDE the `:root {}` block** — nesting `.dark` inside `:root` silently breaks because the inner block becomes `:root .dark` which only matches when `.dark` is a descendant of `:root`, not when it's ON the root element itself, (c) client-side toggle button in Header.js with `useState` + `localStorage` that toggles the class on `document.documentElement`. All three must call `document.documentElement` (the `<html>` element), not `document.body` or `window`. Missing any one = broken dark mode. See `references/dark-mode-checklist.md`.

   **Gotcha — `.dark` inside `:root`**: This is the most common failure mode. If globals.css has:
   ```css
   /* WRONG — .dark is inside :root's scope */
   :root {
     --bg: #fff;
     .dark {
       --bg: #000;   /* This becomes ":root .dark" — never matches <html class="dark"> */
     }
   }
   ```
   The fix: close `:root` first, then define `html.dark` as a standalone block:
   ```css
   /* CORRECT */
   :root { --bg: #fff; }
   html.dark { --bg: #000; }
   ```
16. **Blurry images (CRITICAL)**: User complained "image thì vỡ" (images broken/blurry). Unsplash images must use `?w=1600&q=90` suffix — NOT `w=1200&q=80`. The 1200px width is too small for retina/4K displays. Quality 90 prevents compression artifacts.
17. **Tight spacing between text and images (CRITICAL)**: User complained "chữ với hình sát nhau". Card body padding minimums: `22px 20px 24px`. Hero side padding: `24px 20px`. Gap between hero side elements: `16px`. Post content paragraph margin-bottom: `22px`. Airy spacing signals quality; tight spacing signals amateur work.
18. **Hero section CSS class mismatch + ảnh vỡ do next/image (CRITICAL)**: Two bugs that clobbered the hero: (a) The CSS defines `.hero` (not `.hero-section`). page.js must use `className="hero"`. Secondary hero elements use `hero-side`, `hero-side-img`, `hero-side-body` — NOT `hero-secondary`, `thumb`, `info`. Mismatched class names = elements render with zero layout. (b) Do NOT use `<Image>` (next/image) for secondary hero Unsplash URLs — Next.js blocks external images without `remotePatterns` config, and the fixed `width/height` props distort images with varying aspect ratios. Use plain `<img src={post.image} alt={post.title} />` everywhere for external images.

19. **Single-post featured image distorted**: Same next/image problem as above but on the detail page. UNSPLASH images have varying aspect ratios — fixed `width={800} height={450}` stretches or squishes them. Use plain `<img className="featured-img" />` with CSS `object-fit: cover` + `aspect-ratio: 16/9` on the container `.post-featured`. This keeps every image the right shape regardless of source dimensions.

20. **Hero feels flat / lacks impact**: User explicitly complained "thiếu ánh tượng" (lacks impact). Add 5 key animations: (a) `heroSlideIn` — hero card fades+slides up on load via CSS `animation` with staggered `animation-delay`, (b) `heroBodyIn` — text content fades up with 0.1s delay, (c) `pulse-glow` — category tag has animated `box-shadow` glowing pulse, (d) hover zoom — `.hero-main-img img` scales to 1.06x on hover with 0.8s cubic-bezier transition, (e) hover overlay darkens slightly. Side cards get a `translateX(6px)` hover effect + image zoom. All keyframes defined in globals.css, no JS needed.

21. **Verify deployed CSS with Python urllib**: When user reports a UI bug but you can't access browser tools (e.g. Windows Server 2012 without Playwright/browser support), verify what's actually deployed by fetching HTML and CSS from Vercel:

    ```python
    import urllib.request, re
    url = "https://next-blog-vert.vercel.app"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req, timeout=15)
    html = resp.read().decode('utf-8')
    css_urls = re.findall(r'href="(/_next/static/css/[^"]+\.css)"', html)
    if css_urls:
        req2 = urllib.request.Request(url + css_urls[0], headers={"User-Agent": "Mozilla/5.0"})
        css = urllib.request.urlopen(req2, timeout=15).read().decode('utf-8')
        if 'html.dark' in css:
            print("✅ Dark mode CSS deployed")
        else:
            print("❌ MISSING!")
        imgs = re.findall(r'images\.unsplash\.com[^"\']+', html)
        for img in imgs[:3]:
            print(f"  {'✅' if 'w=1600' in img else '❌'} {img}")
    ```

    This pattern caught that image URLs were still `w=1200` after a failed commit, and confirmed `html.dark` was correctly deployed.
    See `references/selenium-browser-debugging.md` for the full headless-Chrome verification script.

22. **Breaking bar — Marquee ticker (CORRECTED)**: User DOES want horizontal scrolling titles like a classic `<marquee>`. Must use CSS `@keyframes ticker` with duplicate title list for seamless looping. See `references/breaking-bar-pattern.md` for the full working pattern.

23. **Sidebar — 3 posts, not 2**: The hero grid needs `grid-row: span 3` and `allPosts.slice(1, 4)` (3 side cards). With only 2, the sidebar looks empty. With 3, it fills the hero height naturally.

24. **Sidebar heading colors — use `var(--text-strong)`**: The hero-side `<h4>` links must have `color: var(--text-strong)` explicitly set on the `<a>` tag. Without this, headings inherit the default link color or browser defaults, looking wrong in dark mode (too blue, not white-enough):
    ```css
    .hero-side-body h4 a { color: var(--text-strong); transition: color 0.2s; }
    .hero-side-body h4 a:hover { color: var(--brand); }
    ```

25. **Card body minimum padding updated**: After user feedback about spacing ("chữ với hình sát nhau"), the minimum card-body padding is now `24px 20px 24px` (was 22px). Category tag margin-bottom: `12px` (was 8px). These small bumps prevent the "dính sát" complaint.

26. **Card image touching text (0.2px gap)**: Even with padding fixes, Chrome measures the gap between `.card-img` and `.card-body` as ~0.2px — they visually touch. Add `border-bottom: 1px solid var(--border)` to `.card-img` for a visible separator. Without this, the card looks amateur even though CSS spacing is correct.

27. **Breaking bar — use a single solid color, never gradient**: User said "bg thì lấy 1 màu thôi màu nhạt nhạt là oke". Background must be one solid dark blue (`#1e3a5f`), NOT a multi-stop gradient. The gradient looks overly designed and the user prefers simplicity.

## CRITICAL: User approval workflow (MANDATORY)

**NEVER create blog posts, modify content, or deploy without explicit user approval.** The user has explicitly commanded this multiple times:

- "nào làm gì phải hỏi ý kiến tôi đã chứ"
- "từ từ. ai bảo mà làm"  
- "nhớ đấy. sau phải hỏi tôi"

This applies to EVERY action on the blog:
- Writing new `.md` posts → ask first (present topic, let user confirm)
- Deploying to Vercel → ask first
- Modifying existing posts → ask first
- Any UI/theme changes → ask first

The ONLY exception is when the user explicitly says "làm đi", "cứ làm", or gives a clear forward directive. When in doubt, present a plan with options and wait for approval. NEVER write a full blog post and push to Vercel in one motion without asking — even if the user just asked "is there an article about X?".

## User preferences for Đức Dũng (ducdung196qtr)

When building for this user, override the defaults:
- **Author**: Always `"Đức Dũng"` — never "NewsPress AI" or any AI-branded name. User explicitly rejected AI-authored attribution.
- **Color scheme**: Deep blue (`#1a56db`) + white + gold (`#f59e0b`) accent. Do NOT use red (`#e63946`) — user explicitly rejected it as "quá chói" (too glaring).
- **Layout**: Clean, structured, readable. Grid layout with clear separation between cards via borders and spacing. No clutter.
- **UI quality**: Premium polish — subtle borders on cards, stagger card animations with `animation-delay`, Lora serif font for body text (user replaced Merriweather with Lora), glassmorphism header with `backdrop-filter`, gradient background glow.
- **Footer**: Must be the user's own brand — dark navy background, brand name, author name (Đức Dũng), contact info, no mention of Vercel/Next.js/infrastructure. User explicitly rejected platform credit in footer.
- **Logo**: Simple text/icon combo — a single letter in a colored block (`logo-icon` div with border-radius) paired with the site name. No image dependency.
- **Content depth**: 2,000–3,500 words per article. Must include markdown tables, expert quotes (`> blockquote`), multi-angle analysis (e.g. "3 góc nhìn", "phân tích từ các phía"), and a "Góc nhìn Việt Nam" section where relevant. User explicitly asked for "chiều sâu" (depth).
- **Tone**: Professional but conversational Vietnamese. Use `##` and `###` headings heavily for structure. Use markdown tables for comparisons.
- **Code style**: Use markdown tables for comparisons, `**bold**` for emphasis, Unicode emoji sparingly in headings.
- **Deployment**: Prefer `vercel` CLI with token for direct deploy. If that fails, fall back to GitHub push + Vercel auto-deploy (user may not want to manually trigger deploy).

---

| | WordPress | Vercel Blog |
|---|---|---|
| Hosting cost | ~50–200k/month | Free |
| RAM needed | 500MB+ | 0 (serverless) |
| Setup time | 30 min + maintenance | 5 min + no maintenance |
| Content format | MySQL DB | Markdown files in Git |
| Auto-post | REST API POST | git commit + push |
| Speed | Medium | Very fast (CDN) |
| Best for | Non-devs, plugin ecosystem | Devs, AI-driven content, lean sites |

## References

- `references/nextjs-blog-scaffold.md` — Full file listing and code from the 2026-07-16 session
- `references/selenium-browser-debugging.md` — Verify deployed site visually with headless Chrome (screenshots, computed CSS, spacing)
- `references/breaking-bar-pattern.md` — Marquee ticker breaking bar with duplicate titles for seamless loop
