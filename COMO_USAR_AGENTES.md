# 🐝 Cómo Usar los Agentes - Guía Rápida

## Visión General

**Equipo-de-agentes** es tu biblioteca centralizada de 21 especialistas. Desde cualquier proyecto, puedes invocar estos agentes sin duplicar archivos.

---

## 📍 Configuración en tu Proyecto Cliente

### 1. Copia la estructura base

Cuando creas un nuevo proyecto cliente:

```
Mi-Proyecto-Cliente/
├── CLAUDE.md              ← Hereda de Abelha Studio
├── .claude/
│   └── settings.local.json
└── ...
```

### 2. Configura el CLAUDE.md

Tu `CLAUDE.md` debe apuntar a la biblioteca central:

```markdown
# Mi Proyecto Cliente

Este proyecto usa los **21 agentes especializados de Abelha Studio**.
Ruta base: `../../Equipo-de-agentes/06_EQUIPO_SKILLS/`

## Cómo invocar agentes

### Para SEO
```/seo-strategic-master```

### Para Diseño Accesible  
```/inclusive-design-accessibility```

### Para Arquitectura Backend
```/backend-api-design```

[Ver índice completo](../../Equipo-de-agentes/06_EQUIPO_SKILLS/INDICE_SKILLS.md)
```

### 3. Configura settings.local.json

En `.claude/settings.local.json` de tu proyecto:

```json
{
  "claude-code.skillsPath": "../../Equipo-de-agentes/06_EQUIPO_SKILLS/",
  "claude-code.contextInclusion": {
    "CLAUDE.md": true,
    "MEMORY.md": true
  }
}
```

---

## 🎯 Cómo Invocar Agentes

### Opción A: Desde la conversación

```
Quiero que actúes como /seo-strategic-master y me ayudes a 
encontrar palabras clave para esta tienda local
```

### Opción B: Referencia en tu CLAUDE.md

Cuando necesites un agente específico, agrega una sección:

```markdown
## Consultar Especialistas

### Necesito SEO Local
Consulta: `06_EQUIPO_SKILLS/marketing/seo-strategic-master.skill.md`
Pregunta: "Actúa como SEO Master y dame palabras clave para [negocio]"

### Necesito Auditoría de Accesibilidad  
Consulta: `06_EQUIPO_SKILLS/producto/inclusive-design-accessibility.skill.md`
Pregunta: "Audita esta web según WCAG 2.1 AA"
```

---

## 📋 Lista de Agentes Disponibles

### 🎯 Liderazgo (2)
- `/orchestrator` - Director de orquestación
- `/ceo-vision-strategy` - Visión estratégica

### 🎨 Producto & Diseño (4)
- `/product-design-strategy` - Estrategia de producto
- `/ux-ui-master` - UX/UI
- `/inclusive-design-accessibility` - Accesibilidad WCAG
- `/copy-design-master` - Copywriting

### 💻 Desarrollo (3)
- `/fullstack-architecture` - Arquitectura full-stack
- `/backend-api-design` - APIs backend
- `/digital-ecology-sustainability` - Sostenibilidad digital

### 📊 Marketing & Ventas (6)
- `/seo-strategic-master` - SEO estratégico
- `/copywriting-sales-master` - Copy persuasivo
- `/sales-funnel-logic` - Embudo de ventas
- `/digital-marketing-growth` - Growth marketing
- `/inbound-marketing-email` - Email marketing
- `/outbound-prospecting-sales` - Prospección

### 👥 Comunidad (2)
- `/community-management-strategy` - Gestión de comunidad
- `/storytelling-narrative` - Storytelling

### 🔬 Investigación (1)
- `/niche-specialist-research` - Research especializada

### ✅ Operaciones (2)
- `/qa-testing-protocol` - Testing & QA
- `/business-finances-ops` - Finanzas

---

## 🚀 Ejemplo: Crear un Proyecto Cliente

```bash
# 1. Crea tu carpeta
mkdir Mi-Cliente-X
cd Mi-Cliente-X

# 2. Copia la estructura base (con CLAUDE.md template)
cp ../../Equipo-de-agentes/CLAUDE_TEMPLATE.md ./CLAUDE.md

# 3. Personaliza CLAUDE.md con datos del cliente
# Edita: nombre, ruta del equipo, servicios, etc.

# 4. Crea settings.local.json
mkdir -p .claude
# Agrega la configuración de skillsPath
```

---

## 💡 Tips

1. **Los skills están en Equipo-de-agentes**, no duplicados
2. **Usa `/` para invocar skills** en Claude Code
3. **CLAUDE.md es tu guía local**, Equipo-de-agentes es la biblioteca
4. **MEMORY.md local** para tracking del cliente específico

---

## 📚 Más Info

- [Índice de Skills](./06_EQUIPO_SKILLS/INDICE_SKILLS.md)
- [CLAUDE.md principal](./CLAUDE.md)
- [Abelha Studio - Contexto](./01_ESTRATEGIA/mision-vision-valores.md)
