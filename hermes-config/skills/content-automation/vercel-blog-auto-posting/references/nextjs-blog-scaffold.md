# Next.js Blog Scaffold — 2026-07-16 session (ducdung196qtr)

**Production URLs:**
- **Repo**: https://github.com/ducdung196qtr/next-blog
- **Vercel**: https://next-blog-vert.vercel.app
- **Vercel project**: ducdung196qtrs-projects/next-blog

Built for a user on Windows Server 2012R2 with 2GB RAM (insufficient for WordPress). 
The solution: Next.js 15 + React 19 blog hosted on Vercel (free), with Markdown content 
and a Python auto-post script.

**Final post count**: 13 articles (3 initial + 10 added after user feedback).

## Critical bugs fixed in this session

| Bug | Symptom | Root cause | Fix |
|-----|---------|------------|-----|
| Hero section blank | Hero not rendered at all | page.js used `className="hero-section"` but CSS only has `.hero` | Rename to `className="hero"` |
| Secondary hero images broken | Images blurry or missing | Used `<Image>` (next/image) without `remotePatterns` for Unsplash | Replace with plain `<img>` + correct CSS class names (`hero-side-img`) |
| Dark mode not toggling | No dark mode toggle visible | Header.js had no toggle button | Add `useState` + `localStorage` toggle with ☀️/🌙 button |
| Tight text-image spacing | "chữ với hình sát nhau" | Card body padding was 18px, hero side padding 20px | Increase to 22-24px |
| Images blurry | "image thì vỡ" | Unsplash URLs used `w=1200&q=80` | Upgrade to `w=1600&q=90` |
| Class name mismatch on secondary hero | Secondary hero cards unstyled | Used CSS class names like `hero-secondary`, `thumb`, `info`, `badge`, `meta` that didn't exist in stylesheet | Replace with `hero-side`, `hero-side-img`, `hero-side-body`, `category-tag`, `side-date` |

## File inventory

```
next-blog/
├── package.json
├── next.config.js
├── jsconfig.json
├── .gitignore
├── content/posts/
│   ├── haaland-tom-holland.md
│   ├── tsmc-dau-tu-my.md
│   └── ban-gai-trieu-phu-truong-tho.md
├── public/images/
├── scripts/
│   └── auto_post.py
└── src/
    ├── app/
    │   ├── layout.js
    │   ├── page.js
    │   ├── globals.css
    │   ├── about/page.js
    │   ├── trending/page.js
    │   ├── posts/[slug]/page.js
    │   └── category/[category]/page.js
    ├── components/
    │   ├── Header.js
    │   ├── Footer.js
    │   └── PostCard.js
    └── lib/
        └── posts.js
```

## Build output (Next.js 16.2.10 + Turbopack)

```
Route (app)
┌ ○ /
├ ○ /_not-found
├ ○ /about
├ ƒ /category/[category]
├ ● /posts/[slug]
│ ├ /posts/haaland-tom-holland
│ ├ /posts/tsmc-dau-tu-my
│ └ /posts/ban-gai-trieu-phu-truong-tho
└ ○ /trending

○  (Static)   prerendered as static content
●  (SSG)      prerendered as static HTML (uses generateStaticParams)
ƒ  (Dynamic)  server-rendered on demand
```

## Key decisions made in this session

1. **Vercel over WordPress** — user's server has only 2GB RAM and 30GB disk. Running
   XAMPP + WP would leave <200MB for the agent itself. Vercel is free and offloads
   all hosting.

2. **Markdown over database** — simpler, git-friendly, no migration headaches.
   The Python auto_post.py script creates .md files; git push triggers Vercel deploy.

3. **Custom Markdown converter** — no `react-markdown` or `remark` dependency.
   A simple regex converter in the post page component handles headings, bold,
   italic, code, links, and lists. Keeps the bundle tiny.

4. **CSS custom properties for dark mode** — `.dark` class swaps all variables.
   localStorage persistence + `prefers-color-scheme` for initial detection.

5. **No jQuery** — vanilla JS with `IntersectionObserver`, passive scroll listeners,
   CSS animations for everything visual.

## Vietnamese category slug mapping

```
tin-tuc    → Tin tức
doi-song   → Đời sống
cong-nghe  → Công nghệ
giai-tri   → Giải trí
the-thao   → Thể thao
```

## auto_post.py slugify function

```python
def slugify(title):
    slug = title.lower()
    slug = re.sub(r'[đĐ]', 'd', slug)
    slug = re.sub(r'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', slug)
    slug = re.sub(r'[èéẹẻẽêềếệểễ]', 'e', slug)
    slug = re.sub(r'[ìíịỉĩ]', 'i', slug)
    slug = re.sub(r'[òóọỏõôồốộổỗơờớợởỡ]', 'o', slug)
    slug = re.sub(r'[ùúụủũưừứựửữ]', 'u', slug)
    slug = re.sub(r'[ỳýỵỷỹ]', 'y', slug)
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug.strip())
    slug = re.sub(r'-+', '-', slug)
    return slug[:80]
```

## Responsive breakpoints used

- `900px` — hero collapses to single column, mobile menu appears
- `480px` — secondary hero cards stack vertically, font sizes reduce
