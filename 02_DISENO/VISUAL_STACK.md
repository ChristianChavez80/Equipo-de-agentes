# 🎨 Visual Stack - Abelha Studio

## Sistema de Identidad Visual

Nuestro diseño dice: **"Tecnología Humana"**

---

## 🎭 Paleta de Colores

### Primarios

| Color | Hex | RGB | Uso |
|-------|-----|-----|-----|
| **Amarillo Abelha** | `#FFCC00` | (255, 204, 0) | Botones primarios, acentos destacados |
| **Verde Orgánico** | `#2D8C5E` | (45, 140, 94) | Secundarios, éxito, crecimiento |
| **Gris Oscuro (Dark Mode)** | `#1A1A1A` | (26, 26, 26) | Fondo primario |

### Secundarios

| Color | Hex | RGB | Uso |
|-------|-----|-----|-----|
| **Gris Claro** | `#E8E8E8` | (232, 232, 232) | Bordes, divisores en dark mode |
| **Verde Mint** | `#4ECD9B` | (78, 205, 155) | Estados de éxito, validación |
| **Rojo Suave** | `#E84C3D` | (232, 76, 61) | Errores, advertencias |

### Escala de Grises

```
Muy Oscuro:  #0D0D0D
Oscuro:      #1A1A1A  ← Fondo principal dark mode
Gris Medio:  #4A4A4A
Gris Claro:  #E8E8E8
Muy Claro:   #F5F5F5
```

---

## 🔤 Tipografía

### Fuentes Base

- **Sans-Serif Principal**: Inter o Montserrat
- **Fallback**: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto
- **Monoespaciada** (código): JetBrains Mono, Fira Code

### Escalas de Tamaño

**Principio**: Generoso en espaciado, mínimo 16px para cuerpo

| Elemento | Tamaño | Peso | Line Height |
|----------|--------|------|------------|
| H1 (Título) | 32-40px | 700 Bold | 1.2 |
| H2 (Subtítulo) | 24-28px | 600 Semi-Bold | 1.3 |
| H3 (Encabezado) | 20-24px | 600 Semi-Bold | 1.4 |
| Body (Cuerpo) | 16-18px | 400 Regular | 1.6 |
| Small (Pequeño) | 14px | 400 Regular | 1.5 |
| Micro (Muy pequeño) | 12px | 400 Regular | 1.4 |

---

## 🌓 Modo Dark Mode

**Implementación**: Native CSS `prefers-color-scheme: dark`

### Ratios de Contraste (WCAG AA+)

| Elemento | Foreground | Background | Ratio |
|----------|-----------|-----------|-------|
| Texto Normal | `#E8E8E8` | `#1A1A1A` | 10:1 ✓ |
| Enlaces | `#FFCC00` | `#1A1A1A` | 7.5:1 ✓ |
| Texto Botón | `#1A1A1A` | `#FFCC00` | 10:1 ✓ |

**Beneficio adicional**: Ahorro de energía en pantallas OLED/AMOLED

---

## 🎬 Micro-interacciones

### Principios

1. **Sutiles**: No distraen (TDAH-friendly)
2. **Rápidas**: 200-300ms máximo
3. **Propositivas**: Comunican estado o acción
4. **Accesibles**: Respetan `prefers-reduced-motion`

### Ejemplos

#### Hover en Botones
```css
transition: transform 200ms ease, box-shadow 200ms ease;
&:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 204, 0, 0.3);
}
@media (prefers-reduced-motion: reduce) {
  &:hover { transform: none; box-shadow: none; }
}
```

#### Focus State
```css
&:focus {
  outline: 2px solid #FFCC00;
  outline-offset: 2px;
}
```

#### Loading Spinner
- Rotación suave 1 segundo
- Color: Amarillo con 70% opacidad
- Respetar `prefers-reduced-motion`

---

## 📐 Espaciado

### Sistema de 8px

```
8px   = gap-1
16px  = gap-2
24px  = gap-3
32px  = gap-4
48px  = gap-6
64px  = gap-8
```

### Márgenes por Elemento

- **Sección**: 64px top/bottom
- **Componente**: 32px top/bottom
- **Elemento**: 16px top/bottom

---

## 🖼️ Imágenes & Medios

### Formatos Soportados

- **Fotografía**: WebP (principal), JPG (fallback)
- **Ilustración**: SVG (vectorial), PNG (si es raster)
- **Video**: MP4 (H.264), WebM (VP9) para soporte cross-browser

### Optimización

- Lazy loading en imágenes bajo el fold
- srcset para responsive images
- Compresión agresiva: 50-70% reducción de tamaño
- max-width: 100% en contenedores responsivos

---

## 📊 Componentes Base

### Botones

**Primario** (Amarillo)
- Background: `#FFCC00`
- Text: `#1A1A1A`
- Padding: 12px 24px
- Border radius: 4px

**Secundario** (Verde)
- Border: 2px `#2D8C5E`
- Text: `#2D8C5E`
- Background: transparent
- Padding: 10px 22px (ajustado por border)

**Terciario** (Ghost)
- Text: `#E8E8E8`
- Background: transparent
- Hover: fondo muy oscuro `#2A2A2A`

### Cards

- Background: `#262626` (dark mode)
- Border: 1px `#3A3A3A`
- Border-radius: 8px
- Padding: 24px
- Box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3)

### Input Fields

- Background: `#262626`
- Border: 1px `#4A4A4A`
- Text: `#E8E8E8`
- Focus: Border color `#FFCC00`, box-shadow `0 0 0 3px rgba(255, 204, 0, 0.1)`
- Padding: 12px 16px

---

## ♿ Accesibilidad en Diseño

- ✅ Todos los colores pasan WCAG AA (4.5:1 en texto)
- ✅ Sin dependencia de color para comunicar información
- ✅ Espaciado generoso en clickables (mínimo 48x48px)
- ✅ Focus visible en todos los elementos interactivos
- ✅ Respeto a `prefers-reduced-motion`

---

## 🚀 Implementación

Ver [02_DISENO/visual-stack/](.) para:
- `colores.md` - Paleta completa y uso específico
- `tipografia.md` - Detalles de fuentes y escalas
- `componentes.md` - Código de componentes reutilizables
