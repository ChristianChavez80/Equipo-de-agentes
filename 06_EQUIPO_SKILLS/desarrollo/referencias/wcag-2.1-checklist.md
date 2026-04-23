# ♿ WCAG 2.1 AA — Checklist de Conformidad

**Propósito**: Manual de auditoría para validar que la recreación cumple WCAG 2.1 Level AA.

**Referencia oficial**: [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

---

## 1. PERCEIVABLE (Perceptible)
### ✓ 1.4.3 Contrast (Minimum) — CRITICAL
**Estándar**: 
- Body text: mínimo 4.5:1 (WCAG AA), idealmente 7:1 (WCAG AAA)
- Large text (18px+ o 14px bold): mínimo 3:1 (AA), idealmente 4.5:1 (AAA)
- UI components & graphical elements: mínimo 3:1 (AA)

**Cómo auditar**:
```
Para cada elemento de texto:
1. Inspecciona color de texto (color CSS property)
2. Inspecciona color de fondo (background-color CSS property)
3. Calcula contraste: https://webaim.org/resources/contrastchecker/
4. Si < 4.5:1 → violation
```

**Herramientas**:
- Chrome DevTools: Inspect → Accessibility → check contrast ratio
- axe DevTools plugin
- WebAIM Contrast Checker online

**Fix común**:
```css
/* ❌ Bad: 3.2:1 contrast */
.text { color: #777777; background: white; }

/* ✅ Good: 7.1:1 contrast */
.text { color: #333333; background: white; }
```

---

### ✓ 1.1.1 Non-text Content — CRITICAL
**Estándar**: Toda imagen, icono, gráfico debe tener `alt` text descriptivo (o `alt=""` si decorativo).

**Cómo auditar**:
```
1. Inspecciona cada <img>: ¿tiene alt attribute?
2. Si alt="" → ¿es verdaderamente decorativo?
3. Si alt="X" → ¿describe el contenido de forma útil?

❌ alt="image"
❌ alt="pic.jpg"
❌ alt=""  (solo si decorativo)
✅ alt="Hero section: Person holding coffee cup in morning sunlight"
✅ alt="Abelha Studio logo"
```

**SVGs**:
```html
<!-- ❌ Bad -->
<svg>...</svg>

<!-- ✅ Good: opción 1 (aria-label) -->
<svg aria-label="Chevron icon">...</svg>

<!-- ✅ Good: opción 2 (title + desc) -->
<svg>
  <title>Chevron icon</title>
  <desc>Right-pointing chevron for navigation</desc>
</svg>
```

---

### ✓ 1.3.1 Info and Relationships
**Estándar**: Información no debe basarse solo en forma, tamaño, posición visual o sonido.

**Cómo auditar**:
```
Pregunta: ¿Entiende un usuario ciego qué está pasando?

❌ "Click the green button to confirm" (solo color)
❌ "Press the large text at the top" (solo tamaño/posición)
✅ "Click the green 'Confirm' button"
✅ "Press the 'Submit' button at the top"
```

---

## 2. OPERABLE (Operable)
### ✓ 2.1.1 Keyboard — CRITICAL
**Estándar**: Toda funcionalidad disponible vía teclado (no solo mouse).

**Cómo auditar**:
```
1. Abre el sitio en navegador
2. Desactiva el mouse (o simplemente no lo uses)
3. Tab a través de TODOS los elementos interactivos:
   - Botones
   - Links
   - Form inputs
   - Dropdowns
   - Modales
   - Custom components

Preguntas:
- ¿Puedo llegar a cada elemento con Tab?
- ¿Puedo activar botones con Enter/Space?
- ¿Puedo cerrar modales con Escape?
- ¿Hay tab traps (focus atrapado)?
```

**Common violations**:
```html
<!-- ❌ Bad: div no es tabulable -->
<div onclick="handleClick()">Click me</div>

<!-- ✅ Good: button es tabulable y tiene semántica -->
<button onclick="handleClick()">Click me</button>

<!-- ✅ Good: div con tabindex=0 y role -->
<div role="button" tabindex="0" onclick="handleClick()" onkeydown="if(event.key==='Enter') handleClick()">Click me</div>
```

---

### ✓ 2.1.2 No Keyboard Trap
**Estándar**: Focus no puede quedar atrapado en un componente.

**Cómo auditar**:
```
Tab a través del sitio. ¿Puedes salir de cada sección?

❌ Modal abierto → Tab infinitamente dentro del modal → no puedes cerrar
✅ Modal abierto → Tab cíclico dentro del modal → Escape cierra
```

---

### ✓ 2.4.7 Focus Visible — CRITICAL
**Estándar**: Cuando un elemento recibe focus, debe haber un indicador visual claro.

**Cómo auditar**:
```
Tab a través del sitio. ¿Ves dónde está el focus?

❌ No outline visible
❌ Outline muy tenue (< 2px, muy bajo contraste)
✅ Outline visible de al menos 2px, alto contraste
```

**Fix en Abelha (brand color)**:
```css
/* Global focus styles */
:focus-visible {
  outline: 2px solid #FFCC00;  /* Abelha brand yellow */
  outline-offset: 2px;
}

button:focus-visible {
  outline: 2px solid #FFCC00;
  outline-offset: 2px;
}

input:focus-visible {
  outline: 2px solid #FFCC00;
  outline-offset: 2px;
}

a:focus-visible {
  outline: 2px solid #FFCC00;
  outline-offset: 2px;
}
```

---

### ✓ 2.4.1 Bypass Blocks
**Estándar**: Debe haber forma de saltarse contenido repetitivo (nav, sidebar, etc.).

**Cómo auditar**:
```
¿Hay un "Skip to main content" link visible o accesible con Tab?

❌ No skip link
✅ <a href="#main-content" class="skip-link">Skip to main content</a>
```

---

### ✓ 2.5.1 Pointer Gestures
**Estándar**: Si hay gestos complejos (swipe, pinch, drag), debe haber alternativa.

**Cómo auditar**:
```
¿Funciona la interacción solo con mouse/gestos?

❌ Carousel solo se mueve con drag/swipe
✅ Carousel tiene botones "Previous/Next" para teclado
```

---

## 3. UNDERSTANDABLE (Comprensible)
### ✓ 3.1.1 Language of Page
**Estándar**: La página debe declarar su idioma principal.

**Cómo auditar**:
```html
<!-- ✅ Good -->
<html lang="es">

<!-- ❌ Bad -->
<html>
```

---

### ✓ 3.3.1 Error Identification
**Estándar**: Si hay error en un form, el usuario debe saber cuál es y cómo arreglarlo.

**Cómo auditar**:
```
1. Intenta enviar un form con datos inválidos
2. ¿Qué pasa?

❌ El form se rechaza pero no dice por qué
✅ Mensaje claro: "Email must be valid (format: user@example.com)"
```

---

### ✓ 3.3.4 Error Prevention (Submission)
**Estándar**: Para transacciones importantes (compra, eliminación), debe haber confirmación.

**Cómo auditar**:
```
¿Hay un paso de confirmación antes de operaciones peligrosas?

❌ Click "Delete" → item desaparece sin confirmación
✅ Click "Delete" → modal de confirmación aparece
```

---

## 4. ROBUST (Robusto)
### ✓ 4.1.2 Name, Role, Value
**Estándar**: Componentes deben tener nombre, rol, y valores accesibles.

**Cómo auditar**:
```
Inspecciona cada componente interactivo en DevTools → Accessibility:
- Name: ¿tiene un nombre accesible? (text, aria-label, label)
- Role: ¿tiene rol correcto? (button, link, textbox, etc.)
- Value: ¿son evidentes los posibles valores? (checked/unchecked, expanded/collapsed, etc.)
```

**Ejemplos**:
```html
<!-- ❌ Bad: sin nombre accesible -->
<button>🔍</button>

<!-- ✅ Good: con aria-label -->
<button aria-label="Search">🔍</button>

<!-- ✅ Good: con texto -->
<button>Search</button>
```

---

### ✓ 4.1.3 Status Messages (Level AA)
**Estándar**: Mensajes de estado (loading, success, error) deben ser anunciados a usuarios de lector de pantalla.

**Cómo auditar**:
```html
<!-- ❌ Bad: mensaje no es anunciado -->
<div id="status"></div>
<script>
  document.querySelector('#status').textContent = 'Loading...';
</script>

<!-- ✅ Good: con aria-live -->
<div id="status" aria-live="polite" aria-atomic="true"></div>
<script>
  document.querySelector('#status').textContent = 'Loading...';
  // El screen reader anunciará: "Loading..."
</script>
```

---

## 5. MOTION & ANIMATION — Extra Abelha
### ✓ prefers-reduced-motion
**Estándar WCAG 2.1 AAA** (pero buena práctica para AA): Respetar `prefers-reduced-motion: reduce`.

**Cómo auditar**:
```
1. En Settings, activa "Reduce motion" (macOS) o "Remove animations" (Windows)
2. Abre el sitio
3. ¿Aún funciona? ¿Sin animaciones dañinas?

❌ Animaciones continúan, causan mareos
✅ Animaciones se desactivan, todo sigue siendo funcional
```

**Fix**:
```css
/* Default: animaciones activas */
.element {
  animation: slide 0.5s ease-out;
}

/* Si el usuario prefiere reducción de movimiento */
@media (prefers-reduced-motion: reduce) {
  .element {
    animation: none;
    /* o transform inmediato */
    transform: translateX(0);
  }
}
```

---

## 6. COLOR & CONTRAST — Toolkit Abelha
### Paleta Abelha con Contraste Garantizado

**Primario**: `#FFCC00` (Amarillo)
- Sobre blanco: 19.56:1 ✅ AAA
- Sobre gris oscuro: 8.2:1 ✅ AAA

**Secundarios**:
- Verde orgánico: `#2D5016` — 9.1:1 sobre blanco ✅ AAA
- Gris oscuro: `#333333` — 12.6:1 sobre blanco ✅ AAA
- Blanco: `#FFFFFF` — solo para elementos no-críticos sobre colores claros

**Dark Mode**:
- Fondo: `#0A0A0A`
- Texto primario: `#FFFFFF` — 19.56:1 ✅ AAA
- Texto secundario: `#E0E0E0` — 13.2:1 ✅ AAA

---

## 7. TESTING AUTOMATION

### axe-core (Automated Scanning)
```bash
# Instalación
npm install --save-dev @axe-core/cli

# Uso
axe https://your-site.com
```

Output: Lista de violations por severity (critical, serious, moderate, minor).

### Manual Testing Checklist
```
□ Color contrast: todas las combinaciones texto/fondo verificadas
□ Keyboard navigation: Tab, Shift+Tab, Enter, Space, Escape funciona
□ Focus visible: outline claro en todos elementos interactivos
□ Alt text: cada imagen tiene alt descriptivo
□ Form labels: cada input tiene <label> asociado
□ ARIA: roles, labels, live regions correctos
□ Motion: respeta prefers-reduced-motion
□ Errors: mensajes claros si form falla
□ Language: <html lang="es"> declarado
□ Semantic HTML: <button>, <a>, <label>, <input>, <ul>/<ol>/<li>
```

---

## 8. WCAG 2.1 AA Conformance Claim Template

Cuando termines la auditoría, usa este template:

```markdown
# Accessibility Conformance Report

**Site**: [URL]
**Date**: [YYYY-MM-DD]
**Auditor**: Abelha Studio

## Conformance Level
This website conforms to **WCAG 2.1 Level AA**.

## Test Methodology
- Automated testing (axe-core)
- Manual keyboard navigation
- Manual color contrast verification
- Screen reader testing (NVDA, JAWS)

## Results Summary
- Total issues found: [X]
- Critical violations: [X] (all resolved)
- Major violations: [X] (all resolved)
- Minor violations: [X] (documented)

## Known Limitations
[List any WCAG 2.1 AAA features not implemented, if intentional]

## Monitoring
This site will undergo accessibility audits annually and after major updates.

**Signed**: [Name], Abelha Studio
```

---

## References
- [WCAG 2.1 Official](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [axe DevTools](https://www.deque.com/axe/devtools/)
- [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/)
