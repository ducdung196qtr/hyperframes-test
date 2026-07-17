# HyperFrames Deep Dive

**Repo**: https://github.com/heygen-com/hyperframes
**Stars**: 35,676 | **Forks**: 3,345 | **License**: Apache 2.0
**Language**: TypeScript | **Requires**: Node.js 22+, FFmpeg

## Concept

"Write HTML. Render video. Built for agents."

HyperFrames turns HTML + CSS + GSAP into deterministic MP4 video. The core contract uses `data-*` attributes on `class="clip"` elements:

```html
<div id="title" class="clip"
     data-start="0" data-duration="5" data-track-index="1">
  Hello World
</div>
```

GSAP timelines must be registered on `window.__timelines`:

```js
window.__timelines = window.__timelines || {};
const tl = gsap.timeline({ paused: true });
tl.from("#title", { opacity: 0, y: 40, duration: 1 }, 0);
window.__timelines["main"] = tl;
```

## 19 Skills (agent workflows)

### Router
- `/hyperframes` — entry point, capability map, intent router

### Creation Workflows (pick one based on user intent)
- `/product-launch-video` — website → promo video (URL or brief, up to ~3 min, sweet spot 30-90s)
- `/faceless-explainer` — text → 60-90s explainer, no footage needed
- `/pr-to-video` — GitHub PR → changelog/feature reveal
- `/embedded-captions` — add captions to existing talking-head video
- `/talking-head-recut` — package interview/podcast with graphic overlays
- `/motion-graphics` — short (~10s) kinetic type / stat / logo, no narration
- `/music-to-video` — music track → beat-synced lyric/slideshow
- `/slideshow` — presentation/pitch deck (navigable, not rendered video)
- `/general-video` — fallback for anything else, companion mode
- `/remotion-to-hyperframes` — port Remotion (React) compositions

### Domain Skills (loaded on demand)
- `/hyperframes-core` — composition contract, `data-*` semantics
- `/hyperframes-animation` — GSAP, Lottie, Three.js, Anime.js, CSS, WAAPI, TypeGPU
- `/hyperframes-keyframes` — seek-safe keyframe authoring across all runtimes
- `/hyperframes-creative` — design specs, palettes, typography, narration, beat planning
- `/hyperframes-cli` — `init`, `lint`, `preview`, `render`, `publish`, `doctor`
- `/hyperframes-registry` — install catalog blocks via `hyperframes add`
- `/media-use` — **THE media OS**: `resolve --type voice|bgm|sfx|image|icon|logo|grade|lut`
- `/figma` — import Figma assets, tokens, animations

## Media-Use (TTS + Audio Engine)

The `media-use` skill is the single entry point for ALL media:

### Voice (TTS)
```bash
heygen auth login --oauth    # free credits via OAuth
node scripts/resolve.mjs --type voice --intent "Vietnamese female narrator" --project .
```

Two TTS paths:
- **HeyGen TTS** (cloud, free via OAuth)
- **Kokoro** (local, offline, free)

### Other media
```bash
resolve --type bgm --intent "upbeat tech background" 
resolve --type sfx --intent "whoosh transition"
resolve --type image --intent "city skyline at night"
resolve --type icon --intent "chart arrow up"
resolve --type logo --intent "github"          # cascade: svgl → simple-icons → org avatar → favicon
```

### Audio operations
- `transcribe.mjs` — Parakeet transcription (WER 6.05%, 5-10x faster than whisper)
- `transcript-cut.mjs` — compile word-timestamp edits into cut lists
- `audio-duck.mjs` — auto ducking + loudnorm

### Additional generation
- **mflux** — local FLUX image generation (RAM-graded)
- **HeyGen avatar video** — animate still image into talking clip
- **HeyGen image-to-video** — animate any image
- **LTX** — local video generation (opt-in)

## Animation Engines

HyperFrames supports: GSAP (primary), Lottie, Three.js, Anime.js, CSS keyframes, WAAPI, TypeGPU (shaders).

The `hyperframes-keyframes` skill provides seek-safe keyframe authoring across all runtimes — `hyperframes keyframes` diagnostics validates rendered motion.

## CLI Commands

```bash
npx hyperframes init <dir>              # scaffold new project
npx hyperframes preview                 # browser preview with live reload
npx hyperframes render                  # render to MP4
npx hyperframes check                   # lint + runtime + layout + motion
npx hyperframes publish                 # deploy + shareable link
npx hyperframes browser ensure          # download/verify Chrome headless-shell
npx hyperframes skills update           # refresh core skills
npx hyperframes docs <topic>            # offline reference
npx hyperframes upgrade --project       # bump pinned CLI version
```

## Determinism Rules

HyperFrames enforces deterministic rendering:
- No `Date.now()`, `Math.random()`, or network fetches in compositions
- Same HTML always produces the same MP4
- Fonts are cached locally with deterministic `@font-face` injection
- CDN scripts (like GSAP) are inlined at compile time
