# 🌱 Asset Substitution — Guía Eco-Amigable

**Propósito**: Playbook para reemplazar assets del sitio original con alternativas sustentables, libres de licencia, y optimizadas.

**Filosofía Abelha**: No copies bundles de JavaScript, no descargues fotografía de marca. Sustituye inteligentemente con activos que son:
- ✅ Libres de licencia (o bajo licencia permisiva)
- ✅ Optimizados para peso/tamaño
- ✅ Fáciles de obtener (Google Fonts, Unsplash, Pexels, etc.)
- ✅ Eticamente defensibles ("es un estudio de diseño, no plagiarismo")

---

## 1. FUENTES (Fonts) — Substitución Estándar

### Problema Original
Muchos sitios premium cargan **12-20 variantes de fuente custom** (todas las combinaciones de weight + style):

```
Montserrat-Light.woff2 (45KB)
Montserrat-Regular.woff2 (48KB)
Montserrat-Medium.woff2 (50KB)
Montserrat-SemiBold.woff2 (52KB)
Montserrat-Bold.woff2 (54KB)
... × 2 (italic versions) = 500KB+ total
```

### Solución Abelha
Usa **Google Fonts** con solo **2 variantes críticas** (400 regular, 700 bold):

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
```

**Resultado**: 45KB custom font → 12KB Google Fonts (73% reduction) 🎉

### Mapa de Substituciones Comunes

| Original (Custom) | Peso | Google Fonts Equivalente | Peso | Ahorro |
|---|---|---|---|---|
| Montserrat (all) | 500KB | Montserrat 400/700 | 12KB | **97%** |
| Inter (custom) | 480KB | Inter 400/700 | 11KB | **97%** |
| Poppins (custom) | 520KB | Poppins 400/700 | 13KB | **97%** |
| Playfair Display (custom) | 380KB | Playfair Display 700 | 8KB | **97%** |
| Raleway (custom) | 450KB | Raleway 400/700 | 10KB | **97%** |

### Proceso de Substitución

**1. Identifica la fuente original**
```
Inspecciona un elemento de texto:
DevTools → Computed → font-family: "Montserrat", sans-serif
```

**2. Encuentra el equivalente en Google Fonts**
- Visita [Google Fonts](https://fonts.google.com)
- Filtra por: Sans Serif, Serif, Display, Monospace
- Busca por apariencia/feel (alta x-height, generoso spacing, etc.)

**3. Carga solo lo necesario**
```html
<!-- ❌ Bad: todas las variantes -->
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@100;200;300;400;500;600;700;800;900&display=swap" rel="stylesheet">

<!-- ✅ Good: solo lo necesario -->
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap" rel="stylesheet">
```

**4. Reemplaza en CSS**
```css
/* Original (custom) */
@font-face {
  font-family: 'Montserrat';
  src: url('/fonts/montserrat-regular.woff2') format('woff2');
  font-weight: 400;
}

/* Abelha (Google Fonts) */
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
body {
  font-family: 'Montserrat', sans-serif;
}
```

---

## 2. IMÁGENES (Images) — Optimización Agresiva

### Problema Original
Fotografía de marca alta-calidad en JPEG/PNG no optimizado:

```
hero.jpg: 2.1MB (1920×1080)
feature-1.jpg: 1.8MB
feature-2.jpg: 1.6MB
testimonial-cards.png: 890KB
... total: 8-12MB en imágenes
```

### Solución Abelha
1. **Reemplaza con stock/royalty-free**
2. **Convierte a formatos modernos** (WebP, AVIF)
3. **Comprime agresivamente**
4. **Lazy load below-fold**

### Fuentes de Imágenes Libres

| Fuente | Calidad | Uso Comercial | Licencia |
|--------|---------|---------------|----------|
| [Unsplash](https://unsplash.com) | ⭐⭐⭐⭐⭐ Premium | Sí | Unsplash License |
| [Pexels](https://www.pexels.com) | ⭐⭐⭐⭐ Muy buena | Sí | Pexels License |
| [Pixabay](https://pixabay.com) | ⭐⭐⭐ Buena | Sí | Pixabay License |
| [Placeholder](https://placeholder.com) | ⭐ Básica | Sí | Public Domain |

### Proceso de Substitución

**1. Descarga imagen de stock** (formato original: JPG, PNG)
```bash
curl -o hero.jpg https://images.unsplash.com/photo-...
```

**2. Convierte a WebP**
```bash
# Requiere imagemagick o cwebp
cwebp -q 85 hero.jpg -o hero.webp
# Resultado: 2.1MB → 580KB (72% reduction)
```

**3. Genera AVIF (más nuevo, mejor compresión)**
```bash
# Requiere cavif o similar
cavif -o hero.avif hero.jpg
# Resultado: 2.1MB → 380KB (82% reduction)
```

**4. Implementa picture element con fallback**
```html
<!-- ✅ Good: WebP con fallback JPEG -->
<picture>
  <source srcset="/images/hero.avif" type="image/avif">
  <source srcset="/images/hero.webp" type="image/webp">
  <img src="/images/hero.jpg" alt="Hero: Person holding coffee in morning light" loading="lazy">
</picture>
```

**5. Compresión adicional**
```bash
# Comprime JPEG
jpegoptim --max=85 hero.jpg

# Comprime PNG
optipng -o2 feature.png

# O usa imagemin online: https://imagemin.online/
```

### Tamaños Recomendados por Contexto

| Contexto | Ancho | Altura | Max Size |
|----------|-------|--------|----------|
| Hero full-width (desktop) | 1920px | 1080px | 400KB WebP |
| Featured image (1/3 width) | 600px | 400px | 120KB WebP |
| Thumbnail (card) | 300px | 200px | 40KB WebP |
| Icon/illustration | 200px | 200px | 20KB SVG/PNG |

---

## 3. VIDEOS — Optimización Inteligente

### Problema Original
```
hero-video.mp4: 15-20MB (5-10 segundos)
background-loop.webm: 8MB
```

### Solución Abelha
**No incluyas video si es puramente decorativo.** Si es crítico:

1. **Acorta duración** → de 10s a 3-5s
2. **Reduce resolución** → 1080p → 720p
3. **Convierte a WebM/VP9** (mejor compresión que MP4)

```bash
# Extrae 5 segundos, reduce a 720p, convierte a WebM
ffmpeg -i original.mp4 -ss 0 -t 5 -vf scale=1280:720 -c:v libvpx-vp9 -crf 30 -b:v 500k output.webm
# Resultado: 15MB → 2MB (87% reduction)
```

**Mejor práctica**: Usa `<video>` con `autoplay muted playsinline` + lazy load
```html
<video autoplay muted playsinline loading="lazy" width="1280" height="720">
  <source src="/videos/hero.webm" type="video/webm">
  <source src="/videos/hero.mp4" type="video/mp4">
  Your browser doesn't support HTML5 video.
</video>
```

---

## 4. 3D ASSETS (GLB, GLTF) — Decimación & Compresión

### Problema Original
```
model.glb: 2.1MB (malla completa con alta resolución)
```

### Solución Abelha
1. **Decimación de malla** (reduce vertex count)
2. **Compresión gltf** (Draco compression)
3. **Baking de texturas** si es posible

**Herramientas**:
- [Babylon.js Inspector](https://doc.babylonjs.com/features/inspector) — Inspect & export
- [glTF Draco Compression](https://github.com/google/draco) — npm install draco3d
- [gltf-pipeline](https://github.com/CesiumGS/gltf-pipeline) — CLI tool

```bash
# Instala gltf-pipeline
npm install -g @gltf-transform/cli

# Decimación: reduce vertex count a 50%
gltf-transform quantize model.glb --quantize-position 16

# Draco compression
gltf-transform compress model.glb

# Resultado: 2.1MB → 580KB (72% reduction)
```

### Alternativa SVG para Logos/Marcas Simples
Si el 3D es un **logo o marca simple** (no geometría compleja):
```
modelo.glb (2.1MB) → logo.svg (15KB) con Three.js ExtrudeGeometry
// En build time, genera 3D desde SVG
```

---

## 5. ICONOS & ILLUSTRATIONS — SVG Inline

### Problema Original
```
icon-pack.ttf: 320KB (fuente de iconos)
sprite.png: 85KB
```

### Solución Abelha
1. **Usa SVG inline** para iconos críticos
2. **Usa Heroicons o Feather Icons** (gratuitas) para UI
3. **Comprime SVG con SVGO**

**Heroicons** (recomendado para Abelha):
```bash
npm install heroicons
```

```jsx
import { CheckIcon, ChevronRightIcon } from '@heroicons/react/24/solid';

export function Feature() {
  return (
    <>
      <CheckIcon className="w-6 h-6 text-green-600" />
      <ChevronRightIcon className="w-6 h-6" />
    </>
  );
}
```

**Compresión SVG**:
```bash
npm install -D svgo
npx svgo icons/*.svg --folder=icons-optimized
# Reduce SVG size típicamente 40-60%
```

---

## 6. LOTTIE ANIMATIONS — Substitución o Eliminación

### Problema Original
```
animation.json: 250KB (Lottie animation file)
```

### Solución Abelha
Opción 1: **Usa CSS animations** (mucho más ligero)
```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.element {
  animation: fadeInUp 0.6s ease-out;
}
```

Opción 2: **Simplifica Lottie** (remove layers, reduce frames)
```bash
# Abre en Figma → export optimized JSON
# O usa online tool: https://lottie.host/
```

---

## 7. TRACKING & ANALYTICS — Minimiza Scripts

### Problema Original
```
Google Analytics: 45KB
Segment: 55KB
Hotjar: 60KB
Crisp Chat: 85KB
... total: 300+KB de overhead
```

### Solución Abelha
**Prioriza**:
1. Google Analytics 4 (esencial, pero optimiza)
2. Uno máximo de tracking/heatmap (no todos)
3. Chat puede esperar o ser lazy-loaded

```html
<!-- ✅ Good: GA4 optimizado -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX', {
    anonymize_ip: true,
    cookie_flags: 'SameSite=None;Secure'
  });
</script>

<!-- ✅ Chat lazy-loaded: se carga 2s después de render -->
<script>
  setTimeout(() => {
    const script = document.createElement('script');
    script.src = 'https://crisp.chat/chat.js';
    document.body.appendChild(script);
  }, 2000);
</script>
```

---

## 8. QUICK REFERENCE — Asset Substitution Checklist

### Antes de Build
- [ ] **Fonts**: ¿Cuántas variantes? → Reduce a 2 (400, 700) via Google Fonts
- [ ] **Images**: ¿Formato? → Convierte a WebP/AVIF, comprime a < 300KB hero
- [ ] **Videos**: ¿Duración?¿Resolución? → Max 5s, 720p, WebM format
- [ ] **3D Models**: ¿Vertex count? → Decimación + Draco compression
- [ ] **Icons**: ¿Formato? → Usa Heroicons SVG, no font-based
- [ ] **Lottie**: ¿Necesario? → Reemplaza con CSS si es simple
- [ ] **Tracking**: ¿Cuántos scripts? → GA4 solo, lazy load chat

### Target Page Weights

| Asset Type | Original | Abelha Target | Reduction |
|---|---|---|---|
| Fonts | 500KB | 45KB | 91% |
| Images (hero + featured) | 4.5MB | 1.2MB | 73% |
| Videos | 10MB | 1.8MB | 82% |
| 3D Models | 2.1MB | 580KB | 72% |
| Scripts (tracking) | 300KB | 45KB | 85% |
| **TOTAL** | **~17MB** | **~3.6MB** | **79%** |

---

## 9. CO₂ IMPACT — Cálculo Simple

**Fórmula**: `Page Weight (KB) × 0.81g CO₂/MB ÷ 1000 = grams CO₂ per visit`

| Page Weight | CO₂ per Visit | Visitors/month (10k) | Total CO₂/month |
|---|---|---|---|
| 17MB (original) | 13.8g | 10,000 | 138kg |
| 3.6MB (Abelha) | 2.9g | 10,000 | 29kg |
| **Savings** | **79%** | — | **109kg CO₂** |

**Mensualmente, ahorras ~109kg CO₂ vs. original.** 🌱

---

## 10. TOOLS & REFERENCES

**Image Compression**:
- [cwebp](https://developers.google.com/speed/webp/docs/cwebp) — WebP CLI
- [ImageOptim](https://imageoptim.com/mac) — macOS GUI
- [TinyPNG Online](https://tinypng.com) — Online compression
- [Squoosh](https://squoosh.app) — Google's web tool

**3D Optimization**:
- [gltf-transform](https://www.npmjs.com/package/@gltf-transform/cli)
- [Babylon.js Inspector](https://doc.babylonjs.com/features/inspector)

**Fonts**:
- [Google Fonts](https://fonts.google.com)
- [Subset Font](https://www.fonttools.io/) — Reduce font to used characters only

**Icons**:
- [Heroicons](https://heroicons.com)
- [Feather Icons](https://feathericons.com)
- [SVGO](https://svgo.dev) — SVG compression

**Overall Page Weight**:
- [Web.dev Lighthouse](https://pagespeed.web.dev)
- [GTmetrix](https://gtmetrix.com)
- [Bundle Analyzer](https://www.npmjs.com/package/webpack-bundle-analyzer)

---

**Recuerda**: Cada KB ahorrado = usuario más rápido, mejor SEO, menos CO₂. 🌱💚
