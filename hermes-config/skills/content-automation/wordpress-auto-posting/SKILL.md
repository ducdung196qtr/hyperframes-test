---
name: wordpress-auto-posting
description: Automate WordPress content — theme development, REST API posting, cron-job scheduling for daily news auto-publish. Covers WP Application Password auth, REST API endpoints, and theme scaffolding.
---

# WordPress Auto-Posting

Build a WordPress-based automated content publishing pipeline. This skill covers:

1. **Theme development** — scaffolding a clean, modern WP theme from scratch
2. **REST API posting** — using Application Passwords to create posts via API
3. **Cron scheduling** — Hermes cronjob for daily auto-publish

## Theme structure (minimal)

```
wp-theme-name/
  style.css              # Theme header metadata
  functions.php          # Setup, enqueue, hooks, REST extensions
  header.php             # <head>, nav, search overlay
  footer.php             # Footer widgets, copyright
  index.php              # Homepage (hero + card grid)
  single.php             # Single post (breadcrumb, author box, related)
  archive.php            # Category/tag/author/date archives
  page.php               # Static pages
  sidebar.php            # Widget area
  search.php             # Search results
  404.php                # 404 page
  comments.php           # Minimal comment template
  assets/
    css/main.css         # Full stylesheet (CSS variables, dark mode, responsive)
    js/main.js           # Vanilla JS (no jQuery): dark mode toggle, search overlay,
                         #   mobile menu, sticky header, scroll-to-top, lazy loading
  template-parts/
    nav-fallback.php     # Fallback menu when no menu assigned
```

## Key functions.php patterns

### Register REST fields for auto-posting

```php
add_action('rest_api_init', function() {
    register_rest_field('post', 'views', [
        'get_callback' => fn($p) => (int) get_post_meta($p['id'], 'post_views', true),
        'schema' => ['type' => 'integer'],
    ]);
    register_rest_field('post', 'reading_time', [
        'get_callback' => fn($p) => {
            $c = get_post_field('post_content', $p['id']);
            return ceil(str_word_count(strip_tags($c)) / 200);
        },
        'schema' => ['type' => 'integer'],
    ]);
});
```

### Count post views

```php
function track_post_view() {
    if (!is_single()) return;
    $id = get_the_ID();
    $count = (int) get_post_meta($id, 'post_views', true);
    update_post_meta($id, 'post_views', $count + 1);
}
add_action('wp_head', 'track_post_view');
```

## REST API posting

### Authentication

Never use the main password. In WP Admin → Users → Profile → **Application Passwords**, create one named e.g. `hermes-bot`. This generates a password string shown only once.

### Create a post via curl

```bash
curl -X POST "https://example.com/wp-json/wp/v2/posts" \
  -H "Authorization: Basic $(echo -n 'username:app_password' | base64)" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Post Title",
    "content": "<p>HTML content here</p>",
    "status": "publish",
    "categories": [3],
    "tags": [7, 12],
    "featured_media": 456
  }'
```

### Upload featured image first

```bash
curl -X POST "https://example.com/wp-json/wp/v2/media" \
  -H "Authorization: Basic $(echo -n 'user:password' | base64)" \
  -H "Content-Disposition: attachment; filename=\"image.jpg\"" \
  -H "Content-Type: image/jpeg" \
  --data-binary @image.jpg
```

Note the returned `id` — use it as `featured_media`.

## Hermes cronjob for daily auto-post

Once the WP site is live, create a cronjob:

```
cronjob(action='create', 
  schedule='0 7 * * *',  # 7 AM daily
  name='daily-news-publish',
  prompt='Fetch hot news from VnExpress RSS, rewrite 3 articles in Vietnamese, 
          and post them to WordPress at https://example.com via REST API 
          with username X and app password Y.',
  enabled_toolsets=['web', 'terminal'])
```

## CSS conventions

- Use CSS custom properties (`:root`) for theming
- `[data-theme="dark"]` for dark mode (toggle via JS + cookie)
- `--primary`, `--bg`, `--text`, `--border` etc. for easy color swaps
- Mobile breakpoints: `1024px`, `768px`, `480px`

## JS conventions (no jQuery)

- `IntersectionObserver` for lazy loading
- `passive: true` on scroll listeners
- Cookie-based dark mode persistence: `document.cookie`
- Animate with CSS (`@keyframes`) not JS

## Theme Customizer hooks

```php
add_action('customize_register', function($wp_customize) {
    $wp_customize->add_section('my_section', ['title' => 'My Settings', 'priority' => 30]);
    $wp_customize->add_setting('my_setting', ['default' => true]);
    $wp_customize->add_control('my_setting', [
        'label' => 'Enable feature', 'section' => 'my_section', 'type' => 'checkbox'
    ]);
});
```

## Pitfalls

1. **Application Password vanishes**: It only appears once. Store it in memory or a secure note immediately.
2. **REST API 401**: Check that Application Passwords are enabled (Settings → Writing → "Enable application passwords").
3. **Categories not found**: Use category IDs, not slugs, in REST API. Get IDs from `/wp-json/wp/v2/categories`.
4. **featured_media requires prior upload**: Can't set `featured_media` in the same POST as content. Upload media first, get the ID, then create the post.
5. **Theme zip packaging**: Must preserve directory structure. `wp-theme-name/style.css` must be at `theme-name/style.css` inside the zip (one level of nesting).
6. **Low-RAM servers (≤2GB)**: WordPress + Apache + MySQL on a 2GB Windows Server is extremely tight — the OS alone uses ~800MB. MySQL is the biggest RAM consumer (200–500MB). Feasible only for personal blogs with <50 visitors/day and aggressive caching (WP Super Cache, limit `innodb_buffer_pool` to 256MB). Recommend upgrading to 4GB+ RAM or using shared WP hosting (~50–200k VNĐ/month). Linux (Ubuntu) saves ~700MB RAM vs Windows Server.

7. **Alternative: Vercel blog (preferred when RAM < 4GB)**: When server resources are too tight for WordPress, use Next.js + Vercel + Markdown instead (see `vercel-blog-auto-posting` skill for full scaffold). Vercel's free tier offers 100GB bandwidth and unlimited sites — zero RAM cost on the user's server. Auto-post via `git push` to GitHub (with Personal Access Token), Vercel rebuilds in ~30s. This approach was validated end-to-end in a session: Next.js 16 + React 19, 8 static pages, dark mode, responsive, Python auto_post.py helper, and GitHub token-based deploy. Much better fit for ≤2GB servers.
