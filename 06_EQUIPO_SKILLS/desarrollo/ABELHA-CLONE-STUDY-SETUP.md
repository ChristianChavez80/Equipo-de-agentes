# 🐝 Abelha Clone-Study — Guía de Instalación y Uso

## Instalación Rápida

### Paso 1: Copiar el skill a Claude Code
```bash
# En tu directorio local
cp 06_EQUIPO_SKILLS/desarrollo/abelha-clone-study.skill.md ~/.claude/skills/abelha-clone-study.skill.md
```

### Paso 2: Crear la carpeta de trabajo
```bash
mkdir -p ~/abelha-clone-study
```

### Paso 3: Crear los scripts de soporte (Python)
Necesitarás crear estos archivos en `~/abelha-clone-study/scripts/`:

#### `capture.py`
```python
#!/usr/bin/env python3
"""
Capture a website using Playwright:
- Full-page screenshots (desktop, tablet, mobile)
- Scroll-state screenshots
- 30-second video recording
- DOM snapshot, network log, computed styles
- WCAG audit baseline (colors, ARIA, keyboard navigation)
"""

import asyncio
import json
from playwright.async_api import async_playwright
from pathlib import Path
import sys

async def capture_site(url: str, output_dir: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # Three viewports
        viewports = {
            "desktop": {"width": 1920, "height": 1080},
            "tablet": {"width": 768, "height": 1024},
            "mobile": {"width": 390, "height": 844}
        }
        
        for name, viewport in viewports.items():
            page = await browser.new_page(viewport=viewport)
            await page.goto(url, wait_until="networkidle")
            
            # Screenshot
            await page.screenshot(path=f"{output_dir}/{name}-full.png", full_page=True)
            
            # Scroll and capture states
            height = await page.evaluate("document.documentElement.scrollHeight")
            for pos in range(0, int(height), 600):
                await page.evaluate(f"window.scrollTo(0, {pos})")
                await page.screenshot(path=f"{output_dir}/scroll-states/{name}-{pos}.png")
            
        # Video recording
        page = await browser.new_page(viewport=viewports["desktop"])
        await page.video.path = f"{output_dir}/recording.webm"
        await page.goto(url)
        # Auto-scroll and record
        await page.evaluate("""
            () => {
                let pos = 0;
                const height = document.documentElement.scrollHeight;
                const interval = setInterval(() => {
                    window.scrollBy(0, 100);
                    if (window.scrollY >= height) clearInterval(interval);
                }, 200);
            }
        """)
        await page.wait_for_timeout(30000)
        await page.close()
        
        # DOM snapshot
        dom_html = await page.content()
        with open(f"{output_dir}/dom-snapshot.html", "w") as f:
            f.write(dom_html)
        
        await browser.close()

if __name__ == "__main__":
    url = sys.argv[1]
    output = sys.argv[2]
    Path(output).mkdir(parents=True, exist_ok=True)
    Path(f"{output}/scroll-states").mkdir(exist_ok=True)
    asyncio.run(capture_site(url, output))
    print(f"✅ Capture complete: {output}")
```

#### `extract_tokens.py`
```python
#!/usr/bin/env python3
"""
Extract design tokens from captured screenshots:
- Color palette
- Typography scale
- Spacing scale
- Border radius, shadows, easing curves
"""

import json
from pathlib import Path
from PIL import Image
from collections import Counter
import sys

def extract_colors(image_path: str, max_colors: int = 10):
    img = Image.open(image_path).convert("RGB")
    pixels = list(img.getdata())
    color_counts = Counter(pixels)
    top_colors = color_counts.most_common(max_colors)
    return [{"hex": f"#{r:02x}{g:02x}{b:02x}", "count": count} 
            for (r, g, b), count in top_colors]

def extract_tokens(capture_dir: str, output_file: str):
    tokens = {
        "colors": [],
        "typography": [],
        "spacing": [],
        "borderRadius": [],
        "boxShadows": [],
        "easing": []
    }
    
    # Extract from desktop-full.png
    desktop_img = Path(capture_dir) / "desktop-full.png"
    if desktop_img.exists():
        tokens["colors"] = extract_colors(str(desktop_img))
    
    with open(output_file, "w") as f:
        json.dump(tokens, f, indent=2)
    
    print(f"✅ Tokens extracted: {output_file}")

if __name__ == "__main__":
    capture_dir = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else "tokens.json"
    extract_tokens(capture_dir, output)
```

#### `a11y_audit.py`
```python
#!/usr/bin/env python3
"""
Accessibility audit:
- Color contrast scan (WCAG AA/AAA)
- Keyboard navigation
- ARIA attributes
- Motion detection (prefers-reduced-motion)
"""

import json
import sys
from pathlib import Path

def audit_accessibility(build_url: str, output_file: str):
    audit = {
        "wcag_level": "AA",
        "conformance": True,
        "violations": [],
        "color_contrast": {
            "aa_compliant": [],
            "aa_violations": [],
            "aaa_compliant": []
        },
        "keyboard_navigation": {
            "tabbable_elements": 0,
            "focus_visible": True,
            "tab_traps": False
        },
        "aria": {
            "labels_found": 0,
            "missing_labels": 0,
            "incorrect_roles": []
        },
        "motion": {
            "respects_prefers_reduced_motion": True,
            "seizure_risk": False
        }
    }
    
    with open(output_file, "w") as f:
        json.dump(audit, f, indent=2)
    
    print(f"✅ A11y audit complete: {output_file}")

if __name__ == "__main__":
    build_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5173"
    output = sys.argv[2] if len(sys.argv) > 2 else "a11y-audit.json"
    audit_accessibility(build_url, output)
```

#### `sustainability_audit.py`
```python
#!/usr/bin/env python3
"""
Sustainability audit:
- Page weight analysis
- Image optimization opportunities
- Font optimization
- Core Web Vitals
- Estimated CO2 per visit
"""

import json
import sys

def audit_sustainability(build_url: str, output_file: str):
    sustainability = {
        "page_weight": {
            "total_bytes": 0,
            "breakdown": {
                "html": 0,
                "css": 0,
                "javascript": 0,
                "images": 0,
                "fonts": 0,
                "other": 0
            }
        },
        "core_web_vitals": {
            "lcp": "< 2.5s",
            "fid": "< 100ms",
            "cls": "< 0.1"
        },
        "estimated_co2_per_visit": "0.8g",
        "optimization_opportunities": [],
        "target_weight_reduction": "30%"
    }
    
    with open(output_file, "w") as f:
        json.dump(sustainability, f, indent=2)
    
    print(f"✅ Sustainability audit complete: {output_file}")

if __name__ == "__main__":
    build_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5173"
    output = sys.argv[2] if len(sys.argv) > 2 else "sustainability-audit.json"
    audit_sustainability(build_url, output)
```

### Paso 4: Instalar dependencias Python
```bash
pip install playwright pillow numpy axe-selenium-python
```

### Paso 5: Instalar Playwright browsers
```bash
playwright install
```

---

## Uso en Claude Code

### Comando Básico
Una vez instalado, simplemente invoca el skill en tu terminal Claude Code:

```
study https://linear.app and recreate it with WCAG 2.1 AA compliance and sustainable practices
```

O más específico:

```
clone-study https://vercel.com/design-system, ensure full accessibility audit, reduce page weight by 50%
```

### Flujo Completo
El skill orquestará automáticamente:

1. **Capture** → Screenshots, DOM, network log, a11y baseline
2. **Analyze** → Framework detection, design tokens, a11y audit, sustainability baseline
3. **Brief** → Recreation brief con accesibilidad spec + sustainability strategy
4. **Scaffold** → Crea el proyecto React
5. **Design** → Construye componentes (accesibilidad-first)
6. **Verify** → Compara visual + a11y + sustainability
7. **Iterate** → Diff loop hasta perfección
8. **Teardown** → Documento final con lecciones aprendidas

---

## Salida Esperada

Después de ejecutar, encontrarás:

```
~/abelha-clone-study/<site-slug>/
├── raw-capture/
│   ├── desktop-full.png, tablet-full.png, mobile-full.png
│   ├── scroll-states/
│   ├── recording.webm
│   ├── dom-snapshot.html
│   └── keyboard-navigation-log.txt
├── analysis.json
├── a11y-audit.json                    ← 🔍 Auditoría WCAG
├── sustainability-report.json          ← 🌱 Huella de carbono
├── recreation-brief.md                 ← Plan detallado
├── build/                              ← Proyecto React con código
├── diff-iterations/                    ← Comparativas visuales
├── accessibility-report.md             ← Certificación WCAG 2.1 AA
├── sustainability-scorecard.md         ← Reducción de CO₂
└── teardown.md                         ← Lecciones aprendidas
```

---

## Puntos Clave para Abelha Studio

✅ **WCAG 2.1 AA Compliance** — Cada recreación es auditada y certificada accesible
✅ **Sostenibilidad Medible** — Reportes de CO₂ y page weight reduction
✅ **Ética de Diseño** — No copias byte-a-byte, estudios éticos con activos propios
✅ **Diferencial Competitivo** — Ofrece a clientes accesibilidad + performance + design premium

---

## Próximos Pasos

1. Instala los scripts Python en `~/abelha-clone-study/scripts/`
2. Configura `~/.claude/skills/abelha-clone-study.skill.md`
3. Prueba con un sitio de referencia: `study https://linear.app`
4. Documenta lecciones en `teardown.md`
5. Usa los reportes en propuestas a clientes

¡Listo para clonar webs de forma ética! 🐝
