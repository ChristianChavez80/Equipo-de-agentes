# 🚀 Abelha Clone-Study — QUICK START

Guía paso a paso para instalar y ejecutar tu primer **clone-study**.

---

## ⚙️ Paso 1: Instalación (5 minutos)

### 1.1 Verificar Python
```bash
python --version  # Must be 3.8+
python -m pip --version
```

### 1.2 Instalar dependencias
```bash
pip install playwright pillow beautifulsoup4 numpy
playwright install  # Instala browsers (chromium, firefox, webkit)
```

### 1.3 Copiar scripts a tu máquina
```bash
# En tu terminal (Windows, macOS, Linux):

# Crear directorio de trabajo
mkdir -p ~/abelha-clone-study/scripts
cd ~/abelha-clone-study

# Copiar scripts (ajusta la ruta según tu sistema)
cp "C:/Users/xzxgu/OneDrive/Área de Trabalho/Equipo de agentes/06_EQUIPO_SKILLS/desarrollo/scripts"/*.py scripts/

# Verificar
ls scripts/  # Deberías ver: capture.py, extract_tokens.py, a11y_audit.py, sustainability_audit.py
```

### 1.4 Crear carpeta de captures
```bash
mkdir -p captures
```

---

## 📸 Paso 2: Capturar un Sitio (10-15 minutos)

Vamos a capturar **Linear.app** como ejemplo (sitio público, fácil).

```bash
cd ~/abelha-clone-study

python scripts/capture.py https://linear.app captures/linear
```

**Qué pasa:**
- 📸 Captura 3 viewports (desktop, tablet, mobile)
- 📍 Captura scroll-states (cada 600px)
- 🎥 Graba video de 30 segundos
- 🗂️ Extrae red de requests, console logs, fonts

**Salida:**
```
captures/linear/
├── desktop-full.png
├── tablet-full.png
├── mobile-full.png
├── scroll-states/
│   ├── desktop-scroll-000-0px.png
│   ├── desktop-scroll-001-600px.png
│   └── ...
├── recording.webm
├── dom-snapshot.html
├── network-log.json
├── console-log.txt
├── fonts-detected.json
└── manual-notes.md          ← COMPLETA ESTO MANUALMENTE
```

---

## ♿ Paso 3: Auditoría de Accesibilidad (2 minutos)

```bash
python scripts/a11y_audit.py captures/linear

# Genera:
# - a11y-audit.json
# - a11y-audit.md
```

**Resultado esperado:**
- Identifica imágenes sin `alt` text
- Verifica elementos semánticos (<main>, <nav>, <header>)
- Cuenta inputs con labels
- Recomienda mejoras WCAG

---

## 🌱 Paso 4: Auditoría de Sostenibilidad (2 minutos)

```bash
python scripts/sustainability_audit.py captures/linear

# Genera:
# - sustainability-audit.json
# - sustainability-audit.md
```

**Resultado esperado:**
```
📊 SUSTAINABILITY SUMMARY
   Current Page Weight: 3.2MB
   Current CO₂: 2.6g per visit

   Potential Optimized Weight: 1.1MB
   Potential CO₂: 0.9g per visit
   Reduction: 66%

🎯 Meets Abelha Target (< 1.5MB): ✅ YES
```

---

## 🎨 Paso 5: Extraer Design Tokens (1 minuto)

```bash
python scripts/extract_tokens.py captures/linear

# Genera:
# - tokens.json (Tailwind @theme compatible)
```

**Resultado esperado:**
```json
{
  "tailwind_v4_theme": {
    "colors": {
      "background": "#0a0a0a",
      "text-primary": "#ffffff",
      "accent": "#ffcc00"
    },
    ...
  },
  "extracted_colors": [...]
}
```

---

## 📋 Paso 6: Completar Observaciones Manuales (5 minutos)

Abre el archivo generado:
```bash
open captures/linear/manual-notes.md
# o en Windows:
# notepad captures/linear/manual-notes.md
```

Completa:
- [ ] Keyboard navigation (Tab, Enter, Escape)
- [ ] Hover states (color changes, shadows)
- [ ] Animations on load, hover, scroll
- [ ] Audio cues (if any)
- [ ] Accessibility concerns

---

## 📊 Paso 7: Generar Recreation Brief (10 minutos)

Usa la plantilla en `referencias/recreation-brief-template.md`:

```bash
# Copia la plantilla
cp "referencias/recreation-brief-template.md" captures/linear/recreation-brief.md

# Edítala:
# - Llena "Narrative Model" (vertical-page vs scroll-pinned)
# - Añade "Stack Decision"
# - Completa "Design Tokens" (usa el JSON de extract_tokens.py)
# - Lista secciones con screenshots
# - Define animation spec
# - ✅ Añade "Accessibility Specification"
# - ✅ Añade "Sustainability Strategy"
```

**Tip**: Abre 3 ventanas lado a lado:
1. Screenshots originales (en captures/linear/)
2. Auditorías (a11y-audit.md, sustainability-audit.md)
3. Brief abierto en editor

---

## 🎬 Paso 8: Build (Futuro — cuando tengas la carpeta llena)

Una vez tengas el brief completo:

```bash
# En Claude Code, ejecuta:
# > design recreation-brief.md

# O:
# > scaffold my-linear-clone
```

El skill orquestará:
1. Scaffold → React project
2. Design → Construir secciones
3. Polish → Refinar
4. Verify → Comparar visual + a11y + sustainability
5. Iterate → Diff loop hasta perfección

---

## 📁 Estructura Final

```
~/abelha-clone-study/
├── scripts/
│   ├── capture.py
│   ├── extract_tokens.py
│   ├── a11y_audit.py
│   └── sustainability_audit.py
├── captures/
│   └── linear/
│       ├── raw-capture/  (screenshots, video, DOM)
│       ├── a11y-audit.json
│       ├── a11y-audit.md
│       ├── sustainability-audit.json
│       ├── sustainability-audit.md
│       ├── tokens.json
│       ├── manual-notes.md  (COMPLETADO)
│       └── recreation-brief.md  (COMPLETADO)
└── referencias/  (copiadas)
    ├── wcag-2.1-checklist.md
    ├── asset-substitution-ecoamigable.md
    ├── scroll-pinned-timeline.md
    └── recreation-brief-template.md
```

---

## 🐝 Siguiente Sitio

Cuando quieras capturar otro sitio:

```bash
python scripts/capture.py https://vercel.com captures/vercel

# Luego auditorías:
python scripts/a11y_audit.py captures/vercel
python scripts/sustainability_audit.py captures/vercel
python scripts/extract_tokens.py captures/vercel

# Luego brief:
cp referencias/recreation-brief-template.md captures/vercel/recreation-brief.md
# ... editar brief
```

---

## 🆘 Troubleshooting

### ❌ "ModuleNotFoundError: No module named 'playwright'"
```bash
pip install playwright
playwright install
```

### ❌ "Timed out waiting for navigation"
El sitio tarda mucho en cargar. Aumenta timeout:
```bash
# Edita capture.py, línea ~85:
# wait_until="networkidle", timeout=60000  # 60 segundos
```

### ❌ "Video recording failed"
Algunos sistemas no soportan video WebM. Es OK — los screenshots importan más.

### ❌ "No dom-snapshot.html found"
Capture.py falló. Revisa:
- ¿La URL es correcta?
- ¿Tienes internet?
- ¿El sitio tiene cloudflare/protección?

---

## ✅ Checklist — Listo para Usar

- [ ] Python 3.8+ instalado
- [ ] Playwright instalado
- [ ] Scripts copiados a `~/abelha-clone-study/scripts/`
- [ ] Primer sitio capturado sin errores
- [ ] a11y audit completado
- [ ] sustainability audit completado
- [ ] tokens.json generado
- [ ] manual-notes.md completado
- [ ] recreation-brief.md completado

---

## 🎯 Próximos Pasos Reales

1. **Test run completo** con un sitio pequeño (Linear, Vercel, o tu choice)
2. **Refina el brief** — ésta es la parte crítica
3. **Build en Claude Code** — copia el brief, invoca design skill
4. **Itera** — diff loop hasta que se parezca al original
5. **Certifica a11y** — genera accessibility-report.md
6. **Calcula CO₂ savings** — genera sustainability-scorecard.md

---

**¡Ahora tienes todo para clonar webs de forma ética! 🐝✨**

¿Dudas? Revisa:
- `referencias/wcag-2.1-checklist.md` — A11y detalles
- `referencias/asset-substitution-ecoamigable.md` — Cómo optimizar assets
- `ABELHA-CLONE-STUDY-SETUP.md` — Setup más detallado
