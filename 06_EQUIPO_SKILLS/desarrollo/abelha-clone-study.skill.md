---
name: Abelha Clone-Study
description: Studies and recreates high-end website designs (Awwwards, premium SaaS) from a URL while guaranteeing WCAG 2.1 AA accessibility, sustainable digital practices, and inclusive design. Captures structure, design tokens, animations, and asset inventory, then orchestrates scaffold + design + accessibility-validation + sustainability-check in a diff-driven loop. Use this whenever the user wants to clone, study, or recreate a website's design—but with ethical, accessible, and eco-friendly standards.
type: development
---

# 🐝 Abelha Clone-Study
## Recreate Premium Web Design with Ethical Standards

**Abelha Clone-Study** is a faithful study recreation system that clones the visual design of high-end websites (Awwwards, Site of the Day, premium SaaS) while enforcing **accessibility (WCAG 2.1 AA)**, **sustainable digital practices**, and **inclusive design**.

Unlike generic cloning, this skill does not produce byte-for-byte copies. It produces a **study recreation with a conscience**:
- Same layout, animations, design tokens, and feel
- Built from scratch with substituted assets and original copy
- **Audited for accessibility at every step**
- **Reduced carbon footprint** (lighter assets, optimized performance)
- **Designed for inclusion** (keyboard navigation, color contrast, readable typography)

---

## Core Philosophy: Ethical Study Over Copy

Abelha Studio's three pillars embedded in this skill:

1. **Accesibilidad como Mercado** — Accessible sites reach 15% more users and rank better in SEO. Every recreation must be WCAG 2.1 AA compliant.
2. **Sostenibilidad como Velocidad** — Lightweight, optimized sites load faster, consume less energy, and perform better. Sustainable = faster = more conversions.
3. **Automatización como Libertad** — Systematically capture, analyze, and rebuild—no guessing, no hallucinations. Data-driven recreation.

---

## When to Invoke This Skill

Use Abelha Clone-Study when the user:
- "Clone this site" / "Recreate this website" / "Study how this design works"
- "I want my site to look like X" / "Can we rebuild this design?"
- "Reverse engineer this layout" / "How would you build this?"
- **Shares a URL and wants a faithful recreation**
- Shares a URL and wants the same design **but accessible and sustainable**

---

## Workflow at a Glance

```
URL → capture → analyze (+ a11y audit + sustainability check) → brief (+ a11y spec + eco strategy) 
→ scaffold → design (+ accessibility-first) → polish → verify (+ a11y test) → diff → iterate → teardown
```

Each run produces a workspace at `~/abelha-clone-study/<site-slug>/` with intermediate artifacts, accessibility reports, and sustainability metrics.

---

## Phase 1: Capture
**Systematic data collection—foundation for everything that follows.**

Run `scripts/capture.py <url> <output-dir>`. This Playwright script captures:

- **Full-page screenshots** at three viewports: 1920×1080 (desktop), 768×1024 (tablet), 390×844 (mobile)
- **Scroll-state screenshots** every 600px (reveals scroll-triggered animations and lazy-loaded content)
- **30-second video recording** of an automated scroll-through (at 0.25× speed, you'll see timing details)
- **DOM snapshot** after JS hydration
- **Network requests** with content-type, size, and URL
- **Performance timeline** (paint events, animation start times)
- **Console logs** (framework fingerprints often hide here)
- **Computed styles** for all visible text and interactive elements
- **Font face declarations** actually loaded by the browser

**New for Abelha**: Also capture:
- **Keyboard navigation paths** — tab through the entire site, document interactive elements
- **Color contrast values** — for every text element, record computed foreground and background colors
- **ARIA attributes** — note any `aria-label`, `role`, `aria-live` declarations (or absence)
- **Viewport height for each section** — helps with accessible sizing later

**Manual supplement** (required):
1. Open the site in a regular browser. Hover, click, toggle dark mode if available.
2. Test keyboard navigation: Can you reach every button with Tab? Can you submit forms with Enter?
3. Note any audio cues or animations that might not be visible to keyboard users.
4. Save observations as `raw-capture/manual-notes.md`.

---

## Phase 2: Analyze
**Turn raw capture into structured understanding + accessibility audit + sustainability snapshot.**

Output: `analysis.json`, `analysis.md`, `a11y-audit.json`, `sustainability-report.json`.

### 2a. Framework & Library Fingerprinting
Detect the original stack using DOM snapshot, network bundles, window globals, CSS patterns.

Record confidence levels: "Definitely Next 14 + GSAP + Lenis" vs. "Probably Astro + Framer Motion".

### 2b. Design Token Extraction
Run `scripts/extract_tokens.py <capture-dir>`. Outputs:

- **Color palette** — grouped by role (background, surface, text-primary, text-muted, accent)
- **Typography scale** — font families, sizes, weights actually used (top ~5 are the system)
- **Spacing scale** — base unit (often 4px or 8px) and the derived scale
- **Border radius, shadows, easing curves**

### 2c. **NEW: Accessibility Audit** 🔍
For each section, evaluate:

| Aspect | Check |
|--------|-------|
| **Color Contrast** | Every text element: WCAG AA (4.5:1 body, 3:1 large text) or WCAG AAA (7:1)? |
| **Typography** | Minimum 16px body text? Generous line height (1.5+)? Dyslexia-friendly font? |
| **Keyboard Navigation** | Can you tab through all interactive elements? Is focus visible? |
| **ARIA & Semantics** | Are buttons semantic `<button>`, lists are `<ul>`, images have `alt`? |
| **Motion & Animations** | Do animations respect `prefers-reduced-motion`? Any seizure-risk flashes (>3/sec)? |
| **Images & Media** | Do images have descriptive `alt` text? Are videos captioned? |
| **Forms** | Are form labels explicit (`<label for="...">`)? Error messages clear? |
| **Focus Management** | After clicking, does focus move to the result (modal, new section)? |

**Output**: `a11y-audit.json` with scores per section and a severity list (critical, major, minor).

### 2d. **NEW: Sustainability Snapshot** 🌱
Measure the original site's digital footprint:

| Metric | Why It Matters |
|--------|-----------------|
| **Total Page Weight** | KB downloaded. Target: < 2 MB (ideally < 1 MB). Heavy = more energy. |
| **Image Bytes** | Largest asset category. WebP/AVIF used? Lazy loading? |
| **Font Bytes** | Custom fonts are heavy. Google Fonts equivalent available? |
| **Script Bytes** | Framework + libraries. Are there unnecessary bundles (tracking, ads)? |
| **Core Web Vitals** | LCP (paint speed), FID (interactivity), CLS (visual stability). |
| **Energy Estimate** | Using [websitecarbon.com](https://websitecarbon.com) or Lighthouse, estimate kgCO₂ per visit. |

**Output**: `sustainability-report.json` with current baseline and substitution targets.

### 2e. Animation & Scroll Behavior Inventory
Watch the 30-second video at 0.25× speed. For each animation, record:

- Trigger (load, scroll-position, hover, click, time-based)
- Target element
- Properties (opacity, transform, color)
- Duration, easing, stagger
- Does it respect `prefers-reduced-motion`?

### 2f. Narrative Model — Vertical Page vs. Scroll-Pinned Timeline
This determines architecture. See references below.

### 2g. Asset Inventory
For each asset, classify:

| Type | Example | Substitution Plan |
|------|---------|-------------------|
| **Bespoke** | Custom logo, brand photography, custom 3D model | Replace with equivalent free alternative (Unsplash, Pexels, Sketchfab) |
| **Licensable** | Adobe Fonts, stock photo, Lottie animation | Use Google Fonts, open-source library, or free equivalent |
| **Substitutable** | Heavy custom font → Google Fonts, PNG → WebP/AVIF, large video → optimized clip |

**Abelha requirement**: Prioritize eco-friendly alternatives (optimized formats, smaller file sizes).

### 2h. Section Breakdown
Walk the full-page screenshot. For each section, record:

- Purpose (hero, features, social proof, CTA, footer)
- Layout pattern (split, grid, stacked)
- Animation behavior
- Viewport height
- Accessibility notes (color contrast, text size, interactive elements)

---

## Phase 3: Recreation Brief
**The bridge between analysis and build. Without it, the design phase makes a thousand inconsistent decisions.**

Use template at `references/recreation-brief-template.md`. Save as `recreation-brief.md`.

### Mandatory sections:

**1. Narrative Model**
Vertical-page or scroll-pinned timeline. This is the most consequential choice.

**2. Stack Decision**
Based on framework detection + scaffold support. Defaults:
- Vite 5 (NOT 7 — Vite 7 requires Node 20.19+ and has native binding issues on Node 20.18)
- @vitejs/plugin-react@^4, Tailwind v4 via @tailwindcss/vite
- For 3D: three, @react-three/fiber, @react-three/drei, @react-three/postprocessing
- Optional: lenis (smooth scroll feel)

**3. Design Tokens**
Paste extracted Tailwind v4 `@theme` block ready for `index.css`.

**4. Section List**
One entry per page region with screenshot thumbnail inline.

**5. Animation Spec Table**
Every notable animation: trigger, target, timing. For pinned timelines, include waypoint table.

**6. Asset Substitution Table**
Original → Replacement (with sustainability rationale).

| Original Asset | Type | Size | Replacement | New Size | Savings |
|---|---|---|---|---|---|
| hero.jpg (JPEG) | Image | 850 KB | hero.webp (WebP) | 240 KB | 72% ↓ |
| Montserrat font family (all 12 weights) | Font | 320 KB | Montserrat 400/700 only via Google Fonts | 45 KB | 86% ↓ |
| canvas-animation.glb | 3D | 2.1 MB | optimized-model.glb (decimated mesh) | 580 KB | 72% ↓ |

**7. Copy Direction**
Original copy is off-limits. Provide tone: "punchy fintech," "editorial agency," "playful indie," etc.

### **NEW: Accessibility Specification** ♿
Add to brief:

**Color & Contrast**
- Primary text: minimum 4.5:1 (WCAG AA), target 7:1 (AAA)
- Large text (18px+ or 14px+ bold): minimum 3:1 (AA), target 4.5:1 (AAA)
- Interactive elements: minimum 3:1 contrast with adjacent colors
- Do not use color alone to convey information (always add icon/text)

**Typography**
- Body text: minimum 16px (18px preferred for inclusive reading)
- Line height: minimum 1.5 for body, 1.3 for headings
- Letter spacing: no tight letter-spacing on body text (dyslexia-friendly)
- Font choice: sans-serif, high x-height (Inter, Montserrat, Open Sans preferred)

**Keyboard Navigation**
- All interactive elements accessible via Tab (including custom buttons, dropdowns, modals)
- Focus indicator: visible, high-contrast, at least 2px outline
- Focus order: logical (top-to-bottom, left-to-right)
- Tab traps: none (focus must not get stuck)

**Motion**
- All animations must respect `prefers-reduced-motion: reduce` (instant or minimal motion)
- No animations > 5 seconds without user control
- No flashing content (> 3 flashes per second = seizure risk)

**ARIA & Semantics**
- Semantic HTML: `<button>` for buttons, `<a>` for links, `<ul>/<li>` for lists
- Form labels: explicit `<label for="...">` or `aria-label`
- Images: descriptive `alt` text (or `alt=""` if decorative)
- Live updates: `aria-live="polite"` or `aria-live="assertive"` as needed
- Custom components: correct `role` attribute

**Difficulty Flags** ⚠️
Sections you're worried about. Be specific: "custom scroll-pinned 3D — may need shadow DOM workaround for focus management."

### **NEW: Sustainability Strategy** 🌱
Add to brief:

**Page Weight Target**
- Baseline page weight: [X] KB (from original)
- Abelha target: < 1.5 MB total (including images)
- Strategy: [specific optimizations]

**Asset Optimizations**
- Images: Convert to WebP/AVIF, lazy load below-fold
- Fonts: Limit to essential weights (400, 700), use system fonts where possible
- Scripts: Defer non-critical JS, remove unused dependencies
- Monitoring: Core Web Vitals targets (LCP < 2.5s, FID < 100ms, CLS < 0.1)

**Energy Impact**
- Estimated CO₂ per visit (from original): [X] grams
- Target: [Y] grams (typically 50% reduction via optimization)
- Monitoring: Monthly carbon footprint report

---

## Phase 4: Build
**Hand the brief to the build skills.**

1. **Invoke scaffold** with project name and one-liner. When asked, paste stack decision from brief.
   - Immediately after, pin Vite: `npm install -D vite@^5 @vitejs/plugin-react@^4`
   - Clean install: `rm -rf node_modules package-lock.json && npm install`

2. **Register dev server** in `.claude/launch.json` with `runtimeExecutable: "npm"`, `runtimeArgs: ["run", "dev", "--prefix", "<absolute-path>"]`, `port: 5173`.

3. **Invoke design or premium-design** with full brief context. Build sections in order. **Enforce accessibility from the start**:
   - Every button is a semantic `<button>` with visible focus
   - Every image has descriptive `alt` text
   - Every form has explicit labels
   - Text contrast is checked (use Tailwind's `@apply` to enforce minimum sizes/weights)
   - Motion respects `prefers-reduced-motion`

4. **Invoke polish** for visual refinement.

5. **Do not do steps 6–7 yourself** — they have dedicated loops.

---

## Phase 5: Visual & Accessibility Diff Loop
**Close the gap between "looks right" and "looks AND performs AND is accessible like the original."**

Max 5 iterations. After each:

### 5a. Capture Current State
- Screenshot at same three viewports as original
- For pinned timelines, also screenshot at key waypoints (0.0, 0.28, 0.5, 0.72, 0.92)
- Sleep 1.5s between scroll and screenshot (camera lerps + React RAF latency)

### 5b. Visual Diff
Run `scripts/visual_diff.py <original-capture> <current-capture>` → side-by-side comparison + structured diff report.

### **5c. NEW: Accessibility Diff** ♿
Automated checks:

```bash
scripts/a11y_audit.py <build-dir>
```

Outputs:

- **axe-core violations** — flagged issues, severity, how to fix
- **Color contrast scan** — every text element vs. WCAG standards
- **Keyboard navigation test** — Tab through all elements, check focus order
- **ARIA scan** — missing labels, incorrect roles, orphaned live regions
- **Motion scan** — animations that don't respect `prefers-reduced-motion`

Categorize into: fixable (contrast, labels), medium (focus management), hard (custom component behavior).

### **5d. NEW: Sustainability Diff** 🌱
Compare current build against sustainability targets:

```bash
scripts/sustainability_audit.py <build-url>
```

Outputs:

- Page weight vs. target (KB breakdown: images, fonts, JS, CSS)
- Core Web Vitals vs. targets (LCP, FID, CLS)
- Estimated CO₂ per visit
- Optimization opportunities (e.g., "hero.jpg is 850KB, WebP would be 240KB; save 72%")

### 5e. Apply Fixes
Use **design** for structural/animation issues, **polish** for spacing/color/typography, **accessibility-first** skill (if available) for a11y issues.

Priority: Easy fixes first (contrast, labels) → medium (focus, animations) → hard (custom components).

### 5f. Re-test & Re-diff
Stop when:
- Visual diff score + a11y score + sustainability score all below threshold, OR
- No improvement for two iterations, OR
- Hit iteration 5

### 5g. Final Quality Gate
Invoke **design-review** as final gate. It's wired to flag UI issues the loop might miss.

---

## Phase 6: Accessibility Certification
**Abelha differentiator: prove the recreation is WCAG 2.1 AA compliant.**

Generate final report:

```
~/abelha-clone-study/<site-slug>/accessibility-report.md
```

Contents:

- **Conformance claim**: "This design is WCAG 2.1 Level AA compliant" or "Level AAA"
- **Test results by category**:
  - Perceivable (color, contrast, text alternatives)
  - Operable (keyboard, focus, timing)
  - Understandable (language, predictability, error prevention)
  - Robust (parsing, name-role-value for custom components)
- **Known limitations** (if any)
- **Monitoring plan** (automated checks, annual audit)

This becomes part of your client deliverable. Abelha Studio can claim: *"Your new site meets WCAG 2.1 AA standards—that's legally defensible accessibility."*

---

## Phase 7: Sustainability Report
**Prove the recreation is genuinely lower-carbon.**

Generate:

```
~/abelha-clone-study/<site-slug>/sustainability-report.md
```

Contents:

| Metric | Original | Recreation | Savings |
|--------|----------|------------|---------|
| Page Weight | 3.2 MB | 1.1 MB | **66% ↓** |
| LCP (desktop) | 3.8s | 1.9s | **50% ↓** |
| Est. CO₂/visit | 2.4g | 0.8g | **67% ↓** |
| Font Bytes | 320 KB | 45 KB | **86% ↓** (Google Fonts only) |
| Image Bytes | 2.1 MB | 580 KB | **72% ↓** (WebP/lazy load) |

---

## Phase 8: Teardown Document
**Video script raw material. Explain the build to a peer engineer.**

Write `teardown.md` covering:

**Stack Used**
What the original was vs. what you built.

**Interesting Techniques** (2–3 sentences each)
- "The hero text reveal uses GSAP SplitText with 30ms stagger and a clip-path mask animating bottom-to-top with cubic-bezier(0.34, 1.56, 0.64, 1) easing."
- "Scroll-pinned timeline uses a sticky inner viewport (height: 100vh, position: sticky) inside a tall runway (height: 600vh). RAF-throttled progress hook maps scroll position to camera waypoints and section opacity at key moments (0%, 28%, 50%, 72%, 92%)."

**Accessibility Improvements**
- "Original had 2.1:1 contrast on body text; we enforced 4.5:1 WCAG AA."
- "Added keyboard navigation to all interactive elements and focus indicators with `outline: 2px solid #FFCC00` (Abelha brand color)."
- "Implemented `prefers-reduced-motion: reduce` so animations become instant for users with vestibular disorders."

**Sustainability Wins**
- "Swapped custom Montserrat font (320 KB, 12 weights) for Google Fonts Montserrat 400/700 only (45 KB, 86% savings)."
- "Converted JPEG hero to WebP with lazy loading: 850 KB → 240 KB (72% savings)."
- "Optimized 3D model (GLB mesh decimation): 2.1 MB → 580 KB (72% savings)."
- "Final page weight: 3.2 MB → 1.1 MB (66% reduction). Estimated CO₂ per visit: 2.4g → 0.8g."

**What Was Hard**
Be honest. "Custom scroll-pinned 3D scene required careful RAF-throttling to keep animations smooth at 60fps while respecting keyboard focus. This took 1.5 days."

**What You Swapped**
Assets, fonts, copy tone.

**Final Scorecard**

| Category | Score | Status |
|----------|-------|--------|
| Visual Fidelity | 94% | ✅ Near pixel-perfect |
| Accessibility (WCAG 2.1 AA) | 100% | ✅ Fully compliant |
| Sustainability | 67% CO₂ ↓ | ✅ 66% lighter |
| Performance (Core Web Vitals) | 95+ Lighthouse | ✅ Excellent |

---

## Output Structure

```
~/abelha-clone-study/<site-slug>/
├── raw-capture/
│   ├── desktop-full.png, tablet-full.png, mobile-full.png
│   ├── scroll-states/
│   ├── recording.webm
│   ├── dom-snapshot.html
│   ├── network-log.json
│   ├── computed-styles.json
│   ├── console-log.txt
│   ├── keyboard-navigation-log.txt  [NEW]
│   └── manual-notes.md
├── analysis.json
├── analysis.md
├── a11y-audit.json                    [NEW]
├── a11y-audit.md                      [NEW]
├── sustainability-report.json          [NEW]
├── sustainability-report.md            [NEW]
├── recreation-brief.md
├── build/  (the scaffolded project)
├── diff-iterations/
│   ├── iter-1/  (screenshots + visual diff + a11y diff + sustainability diff)
│   ├── iter-2/
│   └── ...
├── accessibility-report.md             [NEW - final certification]
├── sustainability-scorecard.md          [NEW - final metrics]
└── teardown.md
```

---

## Boundaries — Read Carefully

1. **Never download and reship the target's bespoke assets.** Substitute. The asset-substitution doc is non-optional. Prioritize eco-friendly alternatives (smaller files, optimized formats).

2. **Never reuse the target's copy verbatim.** Generate replacement copy in the same tone.

3. **Do not republish the recreation as a commercial site without disclosing it's a study/parody/educational example.**

4. **If the target is open-source licensed**, cite the license.

5. **If the target requires login**, capture stops. Do not bypass auth.

6. **Accessibility is non-negotiable.** Every recreation must be WCAG 2.1 AA compliant (or note why not).

7. **Sustainability is non-negotiable.** Every recreation must reduce digital footprint vs. original by at least 30%.

---

## Tips for Picking Targets

Good targets:
- High visual interest, moderate technical complexity (Linear, Vercel, Stripe)
- Notable signature animation (Lusion, Active Theory, Resn piece)
- Clear section structure (avoid one-page WebGL experiences)
- Public-facing (no auth wall)

Avoid:
- 95% one bespoke 3D scene (can't recreate without weeks of work)
- 95% video content
- Open-source clones of other sites

---

## Abelha Studio Integration

This skill embodies **Abelha's mission: Tecnología Humana**.

Every recreation:
- ✅ **Accesibilidad como Mercado** — WCAG 2.1 AA certified, keyboard-navigable, high contrast
- ✅ **Sostenibilidad como Velocidad** — 30%+ lighter, optimized assets, lower CO₂ footprint
- ✅ **Ética de Acceso** — No design exclusions. Vision-friendly, motion-friendly, disability-friendly

When you finish, your client receives:
- A beautiful, faithful recreation of their inspiration
- A WCAG 2.1 AA accessibility certification
- A sustainability scorecard proving they're reducing digital carbon
- A teardown document explaining the techniques

This is how Abelha Studio wins: **not by copying, but by copying responsibly.**

---

## References

- `references/recreation-brief-template.md` — Brief template
- `references/scroll-pinned-timeline.md` — Architecture for pinned-scroll 3D sites
- `references/animation-detection.md` — Taxonomy of animations (load, scroll, hover, etc.)
- `references/asset-substitution.md` — Playbook for eco-friendly asset swaps
- `references/wcag-2.1-checklist.md` — WCAG 2.1 AA manual checklist
- `references/sustainability-toolkit.md` — Tools for measuring digital carbon footprint
