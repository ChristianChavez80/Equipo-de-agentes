# SKILL: UX/UI STRATEGIC FRAMEWORK & ACCESSIBILITY
Este archivo contiene la base de conocimiento extraída de fuentes clave (Nielsen, Krug, Norman, Sprint) para guiar el desarrollo de interfaces y lógica de negocio.

## 1. PRINCIPIOS DE DISEÑO (CRAP & PSICOLOGÍA)
Para cualquier componente o interfaz generada, aplicar:
- **Contraste:** Si dos elementos no son iguales, hazlos drásticamente distintos para marcar jerarquía.
- **Repetición:** Mantener consistencia visual en tokens, fuentes y espaciados.
- **Alineación:** Cada elemento debe tener una conexión visual con otro; evitar posicionamiento arbitrario.
- **Proximidad:** Agrupar elementos relacionados para reducir la carga cognitiva.
- **Affordance:** Los elementos interactivos deben indicar visualmente su función (ej. botones que parecen pulsables).
- **Modelos Mentales:** Respetar convenciones (Logo a la izquierda, carrito a la derecha) para no obligar al usuario a aprender de cero.

## 2. METODOLOGÍA SPRINT (Lógica de Implementación)
Al desarrollar flujos de usuario, seguir el orden de validación:
1. **Mapear:** Definir la meta y el mapa del desafío antes de codear.
2. **Esbozar:** Buscar inspiración en soluciones existentes.
3. **Decidir:** Priorizar la solución con mayor impacto.
4. **Prototipar:** Construir simulaciones realistas (foco en el MVP).
5. **Probar:** Diseñar para que sea validado por usuarios reales.

## 3. REGLAS TÉCNICAS Y ACCESSIBILITY (WCAG 2.1 AA)
- **Cero Fricción:** El usuario no debe "pensar". La navegación debe responder: ¿Dónde estoy? ¿De dónde vengo? ¿A dónde puedo ir?
- **Mobile-First:** Priorizar contenido esencial y simplificar formularios para pantallas táctiles.
- **Gestión de Errores:** Permitir deshacer acciones y proporcionar mensajes de error humanos y constructivos.
- **Jerarquía Semántica:** Estructura de encabezados (H1-H6) lógica para lectores de pantalla.
- **Contenido Escaneable:** Texto sucinto, uso de negritas y listas para lectura rápida.

## 4. ESTRATEGIA DE NEGOCIO (ROI & RETENCIÓN)
- La usabilidad es supervivencia: si el sitio es difícil, el usuario se va.
- El tiempo del usuario es la moneda principal (Economía de la Atención).
- Cada decisión de código debe estar respaldada por datos o principios de usabilidad, no por estética subjetiva.