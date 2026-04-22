# 🔗 Mapa de Relaciones entre Agentes Abelha

## Flujo de Comunicación Principal: Ciclo de Colmena

```
                    ┌─────────────────┐
                    │   ORQUESTRADOR  │ (Core)
                    │ (Sincronización)│
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
   ┌─────────┐         ┌─────────┐         ┌─────────┐
   │   CEO   │         │ PRODUCTO│         │DESARROLLO│
   │(Visión) │         │(Estrategia)       │(Tech)   │
   └────┬────┘         └────┬────┘         └────┬────┘
        │                   │                   │
   Semanal          Bi-semanal             Semanal
```

---

## 📊 Fases del Proyecto y Agentes Involucrados

### **FASE 1: DIAGNÓSTICO (Semana 1-2)**
```
Investigador ──→ Especialista ──→ Orquestador
    ↓               ↓                 ↓
  Research    Definir Oportunidades  Crear Plan
```

**Agentes Principales:**
- 🔍 **Investigador** (Research): Analiza nicho, pain points
- 💡 **Especialista** (Product): Define ofertas
- ⚙️ **Orquestador**: Crea plan de 12 semanas

**Entrada:** Cliente (brief)  
**Salida:** Proyecto Kickoff + Timeline

---

### **FASE 2: ARQUITECTURA (Semana 3-6)**
```
    UX/UI ──→ Copy Design ──→ Inclusive Design
      ↓            ↓              ↓
   Prototipo   Mensajería    Validación WCAG
      
      ↓            ↓              ↓
      └────→ Orquestador ←────┘
              (Aprobación)
```

**Agentes Principales:**
- 🎨 **UX/UI**: Wireframes → Mockups → Prototipos
- ✍️ **Copy Design**: UX writing, tone of voice
- ♿ **Inclusive Design**: Testing de accesibilidad
- ⚙️ **Orquestador**: Validar con cliente

**Entrada:** Proyecto Kickoff  
**Salida:** Design System + Prototipo clickable

---

### **FASE 3: CONSTRUCCIÓN (Semana 7-10)**
```
Backend ──→ Fullstack ──→ Ecology
  ↓           ↓             ↓
APIs      Estructura    Optimización
         de Datos      de Performance
         
  ↓           ↓             ↓
  └────→ Orquestador ←────┘
        (Integración)
```

**Agentes Principales:**
- 🔌 **Backend**: APIs, integraciones (Google Cal, n8n, CRM)
- 🏗️ **Fullstack**: Estructura de BD, flujos de datos
- 🌱 **Ecology**: Optimización WebP/AVIF, lazy loading
- ⚙️ **Orquestador**: Sincronización de entregas

**Entrada:** Design System  
**Salida:** Código production-ready

---

### **FASE 4: CERTIFICACIÓN (Semana 11)**
```
QA Testing ──→ Inclusive Audit ──→ Orquestador
     ↓              ↓                  ↓
  Bugs Check   Accesibilidad      Sign-off
                   Check           Final
```

**Agentes Principales:**
- 🧪 **QA**: Testing manual + automatizado
- ♿ **Inclusive**: Auditoría WCAG 2.1 AA final
- ⚙️ **Orquestador**: Aprobación para lanzamiento

**Entrada:** Código production  
**Salida:** Certificado de Calidad + Go Live

---

### **FASE 5: POLINIZACIÓN (Semana 12+, Mensual)**
```
SEO ──→ Copywriting ──→ Email Marketing
 ↓          ↓              ↓
GBP      Content      Lead Nurturing
Mgmt     Marketing     Sequences
 
 ↓          ↓              ↓
 └────→ Finanzas ←────┘
      (KPI Tracking)
```

**Agentes Principales:**
- 📍 **SEO**: Google Business Profile, citas locales
- ✍️ **Copywriting**: Blog, case studies, narrativa
- 📧 **Email**: Secuencias de nurturing
- 💰 **Finanzas**: Tracking de conversión, ROI

**Entrada:** Web en vivo  
**Salida:** Reporte mensual + nuevos clientes

---

## 🤝 Matiz de Comunicación: "Quién Habla con Quién"

### **COMUNICACIÓN CRÍTICA** (Diaria)
- Orquestador ↔ Todos los demás
- Desarrollo (Backend + Fullstack + Ecology)
- Diseño (UX/UI + Copy + Inclusive)

### **COMUNICACIÓN REGULAR** (Semanal)
- CEO ↔ Orquestador
- Marketing (SEO + Copywriting + Email)
- Financiero ↔ Orquestador

### **COMUNICACIÓN BIMENSUAL** (Bi-semanal)
- Producto ↔ Especialista Research
- UX/UI ↔ Backend (specs de interactividad)

### **COMUNICACIÓN MENSUAL** (1x/mes)
- CEO ↔ Finanzas (salud del negocio)
- Todos ↔ Orquestador (retrospectiva)

---

## 📈 Matriz de Responsabilidad: RACI

### RACI Legend
- **R** = Responsible (Hace el trabajo)
- **A** = Accountable (Aprueba)
- **C** = Consulted (Opinion importante)
- **I** = Informed (Notificado)

### Proyecto de Cliente (Setup + Fase Mensual)

| Tarea | Orq | CEO | Prod | UX | Inc | Back | Full | Eco | SEO | Copy | QA | Fin |
|-------|-----|-----|------|----|----|------|------|-----|-----|------|-----|-----|
| Kickoff | A | C | R | - | - | - | - | - | - | - | - | - |
| Diseño | - | - | C | R | C | - | - | - | - | C | - | - |
| Accesibilidad | - | - | - | C | R | - | - | - | - | - | C | - |
| Desarrollo | C | - | - | C | - | R | R | R | - | - | - | - |
| Testing | C | - | - | - | - | - | - | - | - | - | R | - |
| Lanzamiento | R | A | C | - | - | - | - | - | C | - | C | - |
| Reportes | - | - | - | - | - | - | - | - | R | C | - | R |

---

## 🎯 Señales de Salud: Indicadores Clave

### ✅ Relaciones Saludables
- Orquestador reporta progreso a CEO semanal
- UX/UI y Backend sincronizan sobre componentes
- QA y Inclusive coordinan testing

### ⚠️ Señales de Alerta
- Orquestador no reporta → retrasos no detectados
- Equipo de Diseño y Desarrollo sin comunicación → entregas desfasadas
- Finanzas sin visibilidad → presupuesto descontrolado

---

## 🔄 Flujo de Escalación

Si hay conflicto o bloqueo:

```
Agente A ↔ Agente B
    ↓ (sin resolver en 1 día)
Orquestador
    ↓ (sin resolver en 2 días)
CEO
    ↓ (decisión ejecutiva)
Implementación
```

---

## 💾 Herramientas de Comunicación Recomendadas

| Herramienta | Uso | Frecuencia |
|-------------|-----|-----------|
| **Tablero Kanban** | Estado de tareas | Diario |
| **Slack/Discord** | Comunicación rápida | Según necesidad |
| **Figma** | Feedback de diseño | Bi-semanal |
| **Spreadsheet** | Tracking de KPIs | Semanal |
| **Reunión Semanal** | Standup | Semanal |

---

**Última Actualización:** 2026-04-22  
**Creado por:** Abelha Studio Equipo de Agentes
