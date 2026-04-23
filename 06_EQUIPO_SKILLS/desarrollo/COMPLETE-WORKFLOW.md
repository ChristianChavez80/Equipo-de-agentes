# 🐝 Abelha Clone-Study — COMPLETE WORKFLOW

**Your complete guide to ethically cloning premium websites while guaranteeing accessibility, sustainability, and inclusive design.**

---

## Overview: 8 Phases of Ethical Web Recreation

```
PHASE 1: CAPTURE          (Playwright automation)
    ↓
PHASE 2: ANALYZE          (Framework detection + design tokens)
    ↓
PHASE 3: BRIEF            (Recreation blueprint with a11y + eco specs)
    ↓
PHASE 4: BUILD            (React scaffold + design implementation)
    ↓
PHASE 5: DIFF LOOP        (Visual + accessibility + sustainability validation)
    ↓
PHASE 6: CERTIFICATION    (WCAG 2.1 AA compliance proof)
    ↓
PHASE 7: SCORECARD        (CO₂ reduction metrics)
    ↓
PHASE 8: TEARDOWN         (Educational documentation)
```

---

## Quick Start (10 minutes)

### Step 1: Install & Setup
```bash
cd ~/abelha-clone-study
python -m pip install playwright pillow beautifulsoup4
playwright install chromium
```

### Step 2: Capture Your Target Site
```bash
python scripts/capture.py https://your-target-site.com captures/mysite
```

### Step 3: Run All Audits
```bash
python scripts/a11y_audit.py captures/mysite
python scripts/sustainability_audit.py captures/mysite
python scripts/extract_tokens.py captures/mysite
```

### Step 4: Create Recreation Brief
Copy `referencias/recreation-brief-template.md` and fill it out using audit results.

### Step 5: Invoke Build Orchestrator
```bash
python scripts/build_orchestrator.py captures/mysite
```

This will:
- Generate scaffolding instructions
- (You complete design in Claude Code)
- Run accessibility certification
- Generate sustainability scorecard
- Create teardown documentation

---

## Detailed Phase Guide

### PHASE 1: CAPTURE 📸
**Purpose**: Systematically collect all visual and technical data about the target site.

**Command**:
```bash
python scripts/capture.py https://linear.app captures/linear
```

**Output**:
```
captures/linear/
├── desktop-full.png          (1920×1080 screenshot)
├── tablet-full.png           (768×1024 screenshot)
├── mobile-full.png           (390×844 screenshot)
├── scroll-states/
│   ├── desktop-scroll-000-0px.png
│   ├── desktop-scroll-001-600px.png
│   └── ... (every 600px)
├── dom-snapshot.html         (Full HTML after JS hydration)
├── network-log.json          (All requests + sizes)
├── console-log.txt           (Framework fingerprints)
├── fonts-detected.json       (Font families loaded)
├── recording.webm            (30-second scroll video)
└── manual-notes.md           (Complete this manually!)
```

**Manual Work Required**:
1. Open `manual-notes.md`
2. Test keyboard navigation with Tab key
3. Document hover states and animations
4. Record any audio cues
5. Note accessibility concerns

**Time**: 15-20 minutes (mostly manual)

---

### PHASE 2: ANALYZE 🔍
**Purpose**: Transform raw capture into structured understanding with accessibility and sustainability audits.

#### 2a. Accessibility Audit
```bash
python scripts/a11y_audit.py captures/linear
```

**Output**:
- `a11y-audit.json` — Semantic HTML, images, forms, buttons, ARIA, headings
- `a11y-audit.md` — Human-readable report

**What it checks**:
- ✓ Images with alt text
- ✓ Semantic elements (`<main>`, `<nav>`, `<header>`)
- ✓ Form labels
- ✓ Semantic buttons (not `<div role="button">`)
- ✓ Heading hierarchy
- ✓ ARIA attributes

#### 2b. Sustainability Audit
```bash
python scripts/sustainability_audit.py captures/linear
```

**Output**:
- `sustainability-audit.json` — Page weight breakdown, CO₂ estimate
- `sustainability-audit.md` — Optimization recommendations

**What it measures**:
- Total page weight (MB)
- Asset breakdown (images, fonts, scripts, CSS)
- Estimated CO₂ per visit (0.81g/MB)
- Optimization opportunities (fonts, images, scripts, videos)

#### 2c. Extract Design Tokens
```bash
python scripts/extract_tokens.py captures/linear
```

**Output**:
- `tokens.json` — Tailwind v4 compatible color palette

**What it extracts**:
- Top 10 dominant colors
- Typography scale
- Spacing system
- Ready to paste into Tailwind config

**Time**: 5 minutes (fully automated)

---

### PHASE 3: BRIEF 📋
**Purpose**: Create a detailed build blueprint that enforces accessibility and sustainability from day one.

**Template**: `referencias/recreation-brief-template.md`

**Mandatory Sections**:

1. **Narrative Model** — Is this a vertical-page site or scroll-pinned 3D timeline?
2. **Stack Decision** — React + Tailwind v4 (default), with framework-specific recommendations
3. **Design Tokens** — Paste Tailwind v4 `@theme` block from extracted tokens
4. **Section List** — List each page region with purpose, layout, and animation behavior
5. **Animation Spec Table** — Every animation: trigger, target, duration, easing, stagger
6. **Asset Substitution Table** — Original → eco-friendly replacement with savings %
7. **Copy Direction** — Tone/voice (original copy is off-limits)
8. **Accessibility Specification** ♿ NEW:
   - Color contrast requirements (4.5:1 minimum for body text)
   - Typography rules (16px minimum, 1.5+ line height)
   - Keyboard navigation expectations
   - ARIA & semantic HTML standards
   - Motion & animation constraints (respects `prefers-reduced-motion`)
9. **Sustainability Strategy** 🌱 NEW:
   - Page weight target (< 1.5MB)
   - Core Web Vitals targets (LCP < 2.5s, FID < 100ms, CLS < 0.1)
   - Specific asset optimizations with % reduction goals
   - Monitoring plan (monthly reports)
10. **Difficulty Flags** ⚠️ — Sections you're worried about
11. **Sign-off** — Confidence level and readiness for build

**Save as**: `captures/linear/recreation-brief.md`

**Time**: 20-30 minutes (requires reading audit reports and examining screenshots)

---

### PHASE 4: BUILD 🔨
**Purpose**: Scaffold React project and construct all sections according to the brief.

#### Step 1: Scaffold React Project
In Claude Code:
```
scaffold my-linear-clone --type react
```

#### Step 2: Configure Vite (Pin Version)
```bash
cd build/my-linear-clone
npm install -D vite@^5 @vitejs/plugin-react@^4
rm -rf node_modules package-lock.json
npm install
```

**Note**: We pin Vite 5, NOT 7, because Node 20.18 compatibility.

#### Step 3: Setup Dev Server
Add to `.claude/launch.json`:
```json
{
  "configurations": [
    {
      "name": "Clone-Study Dev",
      "type": "node",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev", "--prefix", "<absolute-path-to-build>"],
      "console": "integratedTerminal",
      "port": 5173
    }
  ]
}
```

#### Step 4: Invoke Design Skill
In Claude Code:
```
design recreation-brief.md
```

Paste the entire `recreation-brief.md` when prompted. The skill will:
- Build each section in order
- Enforce semantic HTML (`<button>` not `<div role="button">`)
- Add visible focus indicators
- Implement keyboard navigation
- Check color contrast via Tailwind sizing
- Respect `prefers-reduced-motion`

#### Step 5: Polish Phase
After design completes:
```
polish my-linear-clone
```

This refines spacing, colors, and micro-interactions.

**Time**: 4-8 hours (depending on site complexity)

---

### PHASE 5: DIFF LOOP 🔄
**Purpose**: Close the gap between "looks right" and "looks right + accessible + sustainable."

#### Step 5a: Capture Current Build
Take screenshots of your build at the same three viewports:
```bash
# In browser developer tools:
# Desktop: 1920×1080
# Tablet: 768×1024
# Mobile: 390×844

# Save screenshots to: build/desktop-full.png, etc.
```

#### Step 5b: Visual Diff
```bash
python scripts/visual_diff.py captures/linear build visual-diff.json
```

**Output**:
- `visual-diff.json` — Similarity scores per viewport
- `visual-diff.md` — Human-readable comparison

**Scoring**:
- ✓ 90%+ = Near pixel-perfect
- ✓ 80-90% = Strong match, minor refinements
- ⚠️  70-80% = Noticeable differences, priority fixes needed
- ✗ <70% = Significant work needed

#### Step 5c: Accessibility Audit (Build)
```bash
python scripts/a11y_audit.py build
```

This re-audits your build to ensure:
- ✓ Images have alt text
- ✓ Forms have labels
- ✓ Buttons are semantic
- ✓ Color contrast is correct
- ✓ Keyboard navigation works

#### Step 5d: Sustainability Audit (Build)
```bash
python scripts/sustainability_audit.py build
```

This audits your build's page weight and CO₂:
- ✓ < 1.5MB page weight
- ✓ < 1.2g CO₂ per visit
- Recommendations for further optimization

#### Step 5e: Fix Issues
- **Easy fixes** (contrast, labels) → use `polish` skill
- **Medium fixes** (focus, animations) → use `design` skill
- **Hard fixes** (custom components) → investigate manually

#### Step 5f: Re-test & Iterate
Repeat steps 5a-5e until:
- Visual similarity ≥ 85%
- A11y issues = 0 critical
- Page weight < 1.5MB

**Max iterations**: 5

**Time**: 2-4 hours (includes fixing issues)

---

### PHASE 6: CERTIFICATION ✅
**Purpose**: Generate formal WCAG 2.1 AA compliance proof.

```bash
python scripts/accessibility_certification.py build
```

**Output**:
- `accessibility-report.md` — Client-ready certification

**Contents**:
- Conformance claim (WCAG 2.1 AA or AAA)
- Detailed audit results by category
- Testing methodology
- Abelha Studio commitment statement
- Known limitations (if any)

**This document**:
- ✓ Is legally defensible
- ✓ Can be shared with clients
- ✓ Proves compliance to regulators
- ✓ Becomes part of your deliverable

**Time**: 1 minute (fully automated from existing audits)

---

### PHASE 7: SCORECARD 📊
**Purpose**: Prove the recreation is genuinely lower-carbon.

```bash
python scripts/sustainability_scorecard.py captures/linear build
```

**Output**:
- `sustainability-scorecard.md` — Client-ready metrics

**Contents**:
- Original vs. recreation comparison table
- Page weight reduction %
- CO₂ reduction %
- Annual carbon savings (at 100k visits/month)
- Asset optimization details
- Core Web Vitals progress

**Example**:
```
Original: 3.2MB, 2.4g CO₂
Recreation: 1.1MB, 0.8g CO₂
Reduction: 66% lighter, 67% less carbon
Annual savings at 100k visits/month: 18,240kg CO₂
Equivalent to: 867 tree seedlings grown for 10 years
```

**Time**: 1 minute (fully automated)

---

### PHASE 8: TEARDOWN 📚
**Purpose**: Create educational documentation explaining implementation techniques.

```bash
python scripts/build_orchestrator.py captures/mysite --phase 5
```

This generates `teardown.md` template. You complete it with:

**What to document**:

1. **Stack Used**
   - Original stack vs. what you built
   - Why you chose specific libraries

2. **Interesting Techniques** (2-3 sentences each)
   - "Hero text reveal uses GSAP SplitText with 30ms stagger and cubic-bezier(0.34, 1.56, 0.64, 1) easing"
   - "Scroll-pinned timeline uses sticky inner viewport (100vh) inside 600vh runway..."

3. **Accessibility Improvements**
   - Original contrast: 2.1:1 → Recreation: 4.5:1 (WCAG AA)
   - Added keyboard navigation, focus indicators, aria-labels
   - `prefers-reduced-motion` support

4. **Sustainability Wins**
   - Fonts: 320KB → 45KB (Google Fonts only, 86% reduction)
   - Images: 2.1MB → 580KB (WebP + lazy loading, 72% reduction)
   - Scripts: Deferred non-critical JS (40% reduction)

5. **What Was Hard**
   - Honest assessment of time-consuming problems
   - Workarounds for browser compatibility issues

6. **Final Scorecard**
   - Visual Fidelity: [%]
   - Accessibility: 100%
   - Sustainability: [% CO₂ ↓]
   - Performance: [Lighthouse score]

**Time**: 30 minutes (mostly writing, reflecting on implementation)

---

## Full Command Reference

### Phase 1: Capture
```bash
python scripts/capture.py https://target-site.com captures/mysite
# Then manually: edit captures/mysite/manual-notes.md
```

### Phase 2: Analyze
```bash
python scripts/a11y_audit.py captures/mysite
python scripts/sustainability_audit.py captures/mysite
python scripts/extract_tokens.py captures/mysite
```

### Phase 3: Brief
```bash
# Copy template
cp referencias/recreation-brief-template.md captures/mysite/recreation-brief.md
# Edit with your findings
```

### Phase 4: Build
```bash
# In Claude Code:
scaffold my-mysite --type react
design captures/mysite/recreation-brief.md
polish my-mysite
```

### Phase 5: Diff Loop
```bash
python scripts/visual_diff.py captures/mysite build
python scripts/a11y_audit.py build
python scripts/sustainability_audit.py build
# Fix issues and repeat
```

### Phase 6-8: Generate Reports
```bash
python scripts/accessibility_certification.py build
python scripts/sustainability_scorecard.py captures/mysite build
# Teardown: edit teardown.md template manually
```

---

## Output Structure (Final)

```
~/abelha-clone-study/mysite/
├── SCAFFOLD_INSTRUCTIONS.md          (How to scaffold)
├── SCAFFOLD_COMPLETE.log             (Scaffold completion)
│
├── raw-capture/
│   ├── desktop-full.png
│   ├── tablet-full.png
│   ├── mobile-full.png
│   ├── scroll-states/
│   ├── recording.webm
│   ├── dom-snapshot.html
│   ├── network-log.json
│   ├── manual-notes.md              (Completed)
│   └── ...
│
├── analysis.json
├── a11y-audit.json
├── sustainability-audit.json
├── tokens.json
│
├── recreation-brief.md              (Completed)
│
├── build/
│   ├── src/
│   ├── package.json
│   ├── a11y-audit.json             (Build audit)
│   ├── sustainability-audit.json    (Build audit)
│   └── ... (React project)
│
├── diff-iterations/
│   ├── iter-1/
│   │   ├── visual-diff.json
│   │   └── visual-diff.md
│   ├── iter-2/
│   └── ...
│
├── accessibility-report.md           (Final WCAG certification)
├── sustainability-scorecard.md        (Final CO₂ metrics)
├── teardown.md                        (Educational doc)
│
└── orchestrator.log                  (Complete workflow log)
```

---

## Troubleshooting

### "Playwright not installed"
```bash
pip install playwright
playwright install chromium
```

### "Vite 7 installed, need Vite 5"
```bash
npm uninstall vite
npm install -D vite@^5 @vitejs/plugin-react@^4
```

### "Can't reach the target site"
- Is the URL public (no login)?
- Do you have internet?
- Is Cloudflare blocking Playwright?

### "Screenshots don't match"
- Run more iterations of the diff loop
- Check if you're using the same viewport sizes
- Adjust font/spacing in `polish` phase

---

## Abelha Values in Action

Every recreation embodies Abelha Studio's mission:

### ✓ Accesibilidad como Mercado
- WCAG 2.1 AA certified
- Keyboard-navigable
- High color contrast
- Descriptive alt text

### ✓ Sostenibilidad como Velocidad
- 30%+ lighter than original
- Optimized assets (WebP, Google Fonts)
- Lower CO₂ footprint
- Better performance = better SEO

### ✓ Ética de Acceso
- No design exclusions
- Vision-friendly (dark mode)
- Motion-friendly (prefers-reduced-motion)
- Disability-friendly (semantic HTML)

---

## Next Steps

1. **Pick your first target**: Linear.app, Vercel, Stripe, or your choice
2. **Run Phase 1-3**: Capture, analyze, brief (30 minutes)
3. **Pause for review**: Let the brief sink in
4. **Run Phase 4-5**: Build and iterate (4-8 hours)
5. **Generate reports**: Certification, scorecard, teardown (2 hours)

**Total time**: 6-10 hours per site

---

**You now have everything to ethically clone premium websites while guaranteeing accessibility, sustainability, and inclusive design. 🐝✨**

Questions? Check:
- `referencias/wcag-2.1-checklist.md` — Accessibility details
- `referencias/asset-substitution-ecoamigable.md` — Sustainability strategy
- `referencias/scroll-pinned-timeline.md` — Advanced 3D techniques
- `abelha-clone-study.skill.md` — Full skill documentation
