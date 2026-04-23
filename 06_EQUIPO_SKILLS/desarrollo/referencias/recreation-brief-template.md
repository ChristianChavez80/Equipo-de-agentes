# 📋 Recreation Brief Template

**Propósito**: Documento puente entre análisis y construcción. Define exactamente QUÉ y CÓMO construir.

**Cuándo usar**: Después de completar análisis (capture + analyze + a11y audit + sustainability check).

**Quién lo usa**: El skill de diseño lo leerá para construir secciones de forma consistente.

---

## PLANTILLA COMPLETA

```markdown
# Recreation Brief: [SITIO NOMBRE]

**Original Site**: [URL]
**Recreation Date**: [YYYY-MM-DD]
**Auditor**: Abelha Studio

---

## 1. NARRATIVE MODEL

**Type**: [Vertical-Page / Scroll-Pinned Timeline]

**Rationale**: [Brief explanation of why this model]

**Example**:
- Vertical-Page: Sections stack naturally, scroll through them. Animations trigger per-section.
- Scroll-Pinned: Canvas pinned to viewport, scroll drives timeline (0% → 100% progress). Used for 3D/cinematic experiences.

---

## 2. STACK DECISION

### Framework
- Runtime: [Next.js 14 / Nuxt 3 / Astro / Plain React]
- Confidence: [High / Moderate / Low]

### Styling
- Tailwind v4 (via @tailwindcss/vite)
- Dark mode: [Yes / No / Both]

### 3D (if applicable)
- Library: [Three.js / Babylon.js / None]
- Renderer: [React Three Fiber / Plain Three.js / Babylon.js React]
- Effects: [Post-processing - Bloom, Depth of Field, etc.]

### Animation
- Motion library: [GSAP / Framer Motion / Lenis (scroll) / None]
- Scroll library: [Lenis for smooth scroll / Native scroll / Custom RAF]

### Build Tool
```
Vite 5 (NOT 7 — Node 20.18 compatibility issues)
@vitejs/plugin-react@^4
```

### Rationale
[Why this stack? Does it match the original? Is it performant?]

---

## 3. DESIGN TOKENS

### Color Palette

```
@theme {
  colors {
    background: #0A0A0A;           /* Dark background */
    surface: #1A1A1A;              /* Elevated surfaces */
    text-primary: #FFFFFF;         /* Primary text */
    text-secondary: #E0E0E0;       /* Secondary text */
    accent: #FFCC00;               /* Abelha yellow OR original brand color */
    success: #22C55E;
    error: #EF4444;
    warning: #F59E0B;
  }

  fontSize {
    xs: 12px;
    sm: 14px;
    base: 16px;
    lg: 18px;
    xl: 20px;
    2xl: 24px;
    3xl: 32px;
    4xl: 48px;
  }

  fontFamily {
    sans: ["Inter", "Montserrat", system-ui, sans-serif];
    serif: ["Playfair Display", serif];
    mono: ["IBM Plex Mono", monospace];
  }

  spacing {
    xs: 4px;
    sm: 8px;
    md: 12px;
    lg: 16px;
    xl: 24px;
    2xl: 32px;
    3xl: 48px;
  }

  borderRadius {
    sm: 4px;
    md: 8px;
    lg: 12px;
    full: 999px;
  }

  boxShadow {
    sm: 0 1px 2px rgba(0, 0, 0, 0.1);
    md: 0 4px 6px rgba(0, 0, 0, 0.15);
    lg: 0 10px 25px rgba(0, 0, 0, 0.2);
  }
}
```

### Contrast Validation
- Primary text (#FFFFFF) on background (#0A0A0A): **19.56:1** ✅ AAA
- Secondary text (#E0E0E0) on background (#0A0A0A): **13.2:1** ✅ AAA
- Accent (#FFCC00) on background (#0A0A0A): **19.56:1** ✅ AAA

---

## 4. SECTION LIST

### Overview
[Total viewport height on scroll, approximate sections, structure]

### Section 1: Hero
- **Purpose**: Brand intro, headline, CTA
- **Layout**: Full-width hero with headline + subheadline + CTA button
- **Viewport Height**: 100vh
- **Animation Entry**: Fade-in + subtle scale (scale 0.95 → 1.0) over 0.8s ease-out
- **Asset(s)**: 
  - Hero image (1920×1080) → replace with Unsplash equivalent
  - Brand logo → keep or replace with simplified SVG
- **Interactive Elements**: [CTA button, nav menu]
- **Notes**: [Any special considerations]

### Section 2: Features Grid
- **Purpose**: Showcase 3-4 features
- **Layout**: 3-column grid, 2 rows (desktop) / 2-column grid (tablet) / 1-column (mobile)
- **Viewport Height**: 80vh
- **Animation Entry**: Stagger in from bottom (cards appear one by one)
  - Each card: 0.5s ease-out, 100ms delay between cards
- **Asset(s)**: [3-4 feature images] → replace with icons or illustrations
- **Interactive Elements**: [Hover effects, cards clickable → modal?]
- **Notes**: [Any micro-interactions]

### Section 3: Testimonials / Social Proof
- **Purpose**: Build credibility
- **Layout**: Carousel or grid of testimonial cards
- **Viewport Height**: 60vh
- **Animation Entry**: Fade-in at 0.3s ease-out
- **Asset(s)**: [Avatar images] → replace with Unsplash headshots OR placeholders
- **Interactive Elements**: [Carousel arrows / pagination]
- **Notes**: [Any scroll-triggered reveals]

### Section 4: CTA / Footer
- **Purpose**: Call-to-action, secondary links, contact
- **Layout**: Centered CTA headline + form + footer links
- **Viewport Height**: 70vh
- **Animation Entry**: Fade-in + slide-up
- **Asset(s)**: [Footer logo, social icons]
- **Interactive Elements**: [Form submission, email input, social links]
- **Notes**: []

---

## 5. ANIMATION SPEC TABLE

| Section | Element | Trigger | Target Property | Duration | Easing | Stagger | Notes |
|---------|---------|---------|------------------|----------|--------|---------|-------|
| Hero | Headline | Page Load | opacity + transform | 0.8s | ease-out | — | Fade in + scale from 0.95 |
| Hero | Subheadline | Page Load | opacity | 0.8s | ease-out | 0.2s | Fade in after headline |
| Features | Cards | Scroll into view | opacity + transform | 0.5s | ease-out | 0.1s | Slide up from bottom |
| Features | Card hover | Hover | box-shadow + scale | 0.3s | ease-out | — | Lift effect on hover |
| Testimonials | Carousel | Manual (button click) | transform | 0.4s | ease-out | — | Slide left/right |
| CTA | Form submit button | Click | opacity + disabled | 0s | instant | — | Loading state appears |

### Optional: For Scroll-Pinned Timeline
```
Waypoint Table:

| Stage | Progress Range | Action | Camera Move | Objects | Opacity |
|-------|---|---|---|---|---|
| Intro | 0% - 28% | Setup | Pan left → center | Hero object rotates slowly | Intro fade in, other sections hidden |
| Feature 1 | 28% - 50% | Reveal | Move up | Feature 1 object scales up | Feature 1 fades in, Intro fades out |
| Feature 2 | 50% - 72% | Transition | Tilt | Feature 2 object rotates | Feature 2 fades in, Feature 1 fades out |
| CTA | 72% - 100% | Finale | Pull back | CTA object glows | CTA fades in |
```

---

## 6. ACCESSIBILITY SPECIFICATION ♿

### Color & Contrast
- Primary text: **4.5:1 minimum** (WCAG AA), target **7:1** (WCAG AAA)
- Validated palette:
  - ✅ Abelha palette meets AAA standards
  - Do NOT use colors alone to convey information (always add icon/text)

### Typography
- Body text: **minimum 16px** (18px preferred for inclusive reading)
- Line height: **1.5+ for body**, 1.3 for headings
- Letter spacing: normal (no tight letter-spacing)
- Font: Sans-serif with high x-height (Inter, Montserrat)

### Keyboard Navigation
- All interactive elements tabbable (buttons, links, form inputs, dropdowns)
- Focus order: logical (top-to-bottom, left-to-right)
- No focus traps (user can escape from any component)
- Focus indicator: **visible (2px outline, Abelha yellow #FFCC00)**

### ARIA & Semantic HTML
```html
<!-- ✅ Buttons are semantic -->
<button>Click me</button>

<!-- ✅ Links are semantic -->
<a href="/features">Learn more</a>

<!-- ✅ Images have alt text -->
<img src="hero.jpg" alt="Person holding coffee in morning sunlight" />

<!-- ✅ Forms have labels -->
<label for="email">Email:</label>
<input id="email" type="email" required />

<!-- ✅ Live regions for dynamic updates -->
<div aria-live="polite" aria-atomic="true">
  {{ formStatusMessage }}
</div>
```

### Motion
- All animations respect `prefers-reduced-motion: reduce`
- No animations > 5 seconds without user control
- No flashing content (> 3 flashes/sec)

### Testing
- [ ] Contrast check: All text meets WCAG AA minimum
- [ ] Keyboard test: Tab through all elements, no traps
- [ ] Focus test: Outline visible on every interactive element
- [ ] Screen reader test: Sections announced correctly
- [ ] Motion test: `prefers-reduced-motion` works

---

## 7. SUSTAINABILITY STRATEGY 🌱

### Current Baseline (Original Site)
- Page weight: [X] MB
- Core Web Vitals: [LCP, FID, CLS]
- Estimated CO₂ per visit: [X] grams

### Abelha Targets
- Page weight: **< 1.5 MB total** (from [X] MB)
- LCP: **< 2.5s**
- CLS: **< 0.1**
- Estimated CO₂: **< 1.5g per visit** (50% reduction)

### Asset Optimizations

| Asset | Original | Strategy | Target |
|-------|----------|----------|--------|
| Fonts | 500KB custom | Google Fonts 400/700 only | 45KB |
| Hero image | 2.1MB JPEG | WebP + lazy load | 480KB |
| Featured images (3×) | 1.5MB each | WebP + compress | 120KB each |
| Video (if any) | 10MB MP4 | WebM, 5s max, 720p | 1.8MB |
| 3D Model (if any) | 2.1MB GLB | Draco compression + mesh decimation | 580KB |
| Tracking scripts | 300KB | GA4 only, lazy load chat | 45KB |
| **Total Reduction** | **~17MB** | — | **~3.6MB** (**79% ↓**) |

### Monitoring
- Monthly page weight audit (target < 1.5 MB)
- Monthly Core Web Vitals report (via Web Vitals API)
- Monthly CO₂ footprint report (via websitecarbon.com)

---

## 8. COPY DIRECTION

**Tone**: [Punchy fintech / Editorial agency / Playful indie / Professional B2B / etc.]

**Voice**: [Formal / Casual / Witty / Empathetic / etc.]

**Original Copy Style**:
> "We're building the future of design. Every pixel counts."

**Abelha Recreation Copy Direction**:
> Generate copy in a **[tone]** voice that emphasizes **[key message]**. Examples:
> - "Your design, sustainably built."
> - "Accessibility isn't an afterthought—it's the standard."
> - "Performance that feels good to use."

**Brand Attributes to Preserve**:
- Original uses "futuristic" language → Abelha uses "responsible innovation"
- Original emphasizes speed → Abelha emphasizes **speed + sustainability**

---

## 9. ASSET SUBSTITUTION TABLE

| Original Asset | Type | Size | Replacement | Size | Savings | Notes |
|---|---|---|---|---|---|---|
| hero-brand-photo.jpg | Image | 2.1MB | Unsplash #12345 "Creative workspace" | 480KB | 77% | https://unsplash.com/photos/xxx |
| logo.svg | SVG | 15KB | Keep (already optimal) | 15KB | — | Brand asset, license-safe |
| Montserrat-all.woff2 | Font | 500KB | Google Fonts Montserrat 400/700 | 45KB | 91% | https://fonts.google.com/specimen/Montserrat |
| feature-1.jpg | Image | 850KB | Unsplash #67890 "Coffee" | 240KB | 72% | https://unsplash.com/photos/yyy |
| hero-video.mp4 | Video | 15MB | Custom WebM 5s @720p | 1.8MB | 88% | Shorten to 5s, reduce resolution |
| icon-pack.ttf | Font | 320KB | Heroicons SVG | 0KB (inline) | 100% | npm install heroicons |

---

## 10. DIFFICULTY FLAGS ⚠️

**What might take longer:**

- [ ] **Custom 3D scene** — If scroll-pinned 3D, budget 2-3 days for camera choreography
- [ ] **Complex scroll animations** — If many sections with staggered reveals, 1 day
- [ ] **Custom shader** — If original has custom WebGL shader, note this as high-risk
- [ ] **Physics simulation** — If objects have gravity/collision, much harder to recreate
- [ ] **Heavy interactivity** — If tons of hover states and micro-interactions, 1 day

**None of the above?** → Standard 2-3 day build.

---

## 11. SIGN-OFF

**Brief prepared by**: [Name]
**Date**: [YYYY-MM-DD]
**Confidence level**: [High / Moderate / Low]
**Ready for build?**: [ ] Yes [ ] Needs revision

---

## APPENDIX — Key References

1. **WCAG 2.1 AA Checklist**: `references/wcag-2.1-checklist.md`
2. **Asset Optimization**: `references/asset-substitution-ecoamigable.md`
3. **Scroll-Pinned Timeline** (if applicable): `references/scroll-pinned-timeline.md`

---

**This brief is your blueprint. The more specific it is, the faster and better the build.** 🐝
```

---

## NOTES FOR USAGE

### When to Write This
After Phase 2 (Analyze) completes, before invoking design skill.

### Who Writes This
The Abelha Clone-Study orchestrator reads the analysis outputs and fills this template. It becomes a "handoff document" to the design skill.

### What Happens Next
Design skill reads this brief and builds section-by-section, trusting that:
- Tokens are correct (uses the exact colors/typography/spacing)
- Animations match spec (durations, easing, stagger)
- A11y requirements are non-negotiable (WCAG AA or better)
- Sustainability targets are locked in (page weight, CO₂ footprint)

### Common Mistakes to Avoid
- ❌ Forgetting accessibility spec (design creates something inaccessible)
- ❌ Setting unrealistic page weight targets (< 500KB is unrealistic)
- ❌ Vague animation specs ("fade in smoothly") instead of precise timing
- ❌ Forgetting to swap assets (design uses original brand photography instead of substitutes)

---

**Templates win projects. Be specific.** 📋✨
