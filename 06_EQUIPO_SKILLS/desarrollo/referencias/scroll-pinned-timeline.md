# 📌 Scroll-Pinned Timeline — Architecture Reference

**Propósito**: Arquitectura completa para sitios "Awwwards-style" que usan scroll-pinned canvases con timeline controlada por scroll.

**Cuándo usar**: Cuando el sitio original tiene:
- Un canvas (3D, WebGL, animation) pegado al viewport
- Scroll position controla el timeline (camera move, object rotation, section reveal)
- Secciones que aparecen/desaparecen a posiciones específicas
- Efecto "cinemático" donde el usuario controla con scroll qué ve

**Ejemplos reales**: [Oryzo.com](https://oryzo.com), [Lusion.co](https://lusion.co), Apple's AirPods page.

---

## 1. DETECCIÓN — ¿Es scroll-pinned?

### Señales que el sitio usa scroll-pinned timeline:

```
✓ Full-page screenshot es mayormente negro/vacío (canvas content no pinta al DOM estático)
✓ Page height es mucho mayor que visible content (check: height: 600vh, 800vh, etc.)
✓ Scroll-state screenshots muestran el MISMO canvas pero con diferentes estados internos
  (cámara movida, objeto rotado, sección visible)
✓ Network log contiene .buf, .glb, .splat, o camera-animation.json (timeline data)
✓ Performance log muestra animaciones controladas por RAF + requestAnimationFrame
✓ DevTools → Elements: hay <canvas> or <div> con position: sticky / position: fixed
```

### Anti-señal: Es vertical-page, no pinned-timeline

```
✗ Cada viewport screenshot muestra SECCIÓN DIFERENTE
✗ Page height ~ viewport height (no tall runway)
✗ Scroll triggered animations pero distintas en cada sección
```

---

## 2. ARQUITECTURA CORE — La paciencia es clave

### DOM Structure
```html
<div class="runway" style="height: 600vh; /* tall but invisible */">
  <!-- This tall div provides scroll distance; content is elsewhere -->
</div>

<div class="viewport-container" style="position: sticky; height: 100vh; top: 0; overflow: hidden;">
  <!-- 
    THIS is what the user sees.
    - Position: sticky keeps it pinned to the top.
    - Height: 100vh fills the screen.
    - Overflow: hidden contains the canvas.
  -->
  <canvas ref={canvasRef}></canvas>
  <!-- OR for React Three Fiber: -->
  <Canvas>
    <MyScene />
  </Canvas>
</div>

<!-- Sections that fade in/out at scroll positions -->
<div class="section section-1" style="position: absolute; top: 0; ...">
  Section 1 content (will fade in at ~28% scroll)
</div>
<div class="section section-2" style="position: absolute; top: 0; ...">
  Section 2 content (will fade in at ~50% scroll)
</div>
```

### Scroll Progress Calculation
```typescript
// This is the HEART of the architecture.
// On every scroll event, calculate progress (0.0 to 1.0).

const [scrollProgress, setScrollProgress] = useState(0);

useEffect(() => {
  const handleScroll = () => {
    const runway = document.querySelector('.runway');
    const runwayHeight = runway.offsetHeight;
    const windowHeight = window.innerHeight;
    const maxScroll = runwayHeight - windowHeight;
    
    // Progress: 0.0 (start) to 1.0 (end)
    const progress = Math.max(0, Math.min(1, window.scrollY / maxScroll));
    setScrollProgress(progress);
  };
  
  // RAF-throttled for performance
  let rafId;
  const throttledScroll = () => {
    rafId = requestAnimationFrame(handleScroll);
  };
  
  window.addEventListener('scroll', throttledScroll, { passive: true });
  return () => {
    cancelAnimationFrame(rafId);
    window.removeEventListener('scroll', throttledScroll);
  };
}, []);

return scrollProgress; // 0.0 to 1.0
```

---

## 3. STAGE WAYPOINTS — Timeline Markers

Define cuando each section debe ser visible. Common pattern:

```typescript
const WAYPOINTS = {
  intro: { start: 0.0, end: 0.28 },      // Intro phase
  feature1: { start: 0.28, end: 0.5 },   // Feature reveal 1
  feature2: { start: 0.5, end: 0.72 },   // Feature reveal 2
  cta: { start: 0.72, end: 1.0 }         // Call-to-action
};

// For each section, calculate opacity
const getOpacity = (stage, progress) => {
  const { start, end } = WAYPOINTS[stage];
  if (progress < start) return 0;        // Before: invisible
  if (progress < start + 0.05) {
    // Fade in over 5% of scroll distance
    return (progress - start) / 0.05;
  }
  if (progress < end - 0.05) return 1;   // Middle: fully visible
  if (progress < end) {
    // Fade out over last 5%
    return 1 - ((progress - (end - 0.05)) / 0.05);
  }
  return 0; // After: invisible
};
```

---

## 4. THREE.JS / REACT THREE FIBER — Camera & Object Control

### Example: Camera Pan (reveal feature)

```typescript
useEffect(() => {
  if (!cameraRef.current) return;
  
  const camera = cameraRef.current;
  const progress = scrollProgress;
  
  // Camera moves horizontally as user scrolls
  // Start: camera.position.x = 0
  // End (at progress 0.5): camera.position.x = 10
  
  const easedProgress = easeInOutCubic(progress);
  camera.position.x = easedProgress * 10;
  camera.position.y = Math.sin(easedProgress * Math.PI) * 5;
  camera.lookAt(new THREE.Vector3(5, 0, 0));
}, [scrollProgress]);

// Easing function (smoother than linear)
const easeInOutCubic = (t) => {
  return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
};
```

### Example: Object Rotation

```typescript
useEffect(() => {
  if (!meshRef.current) return;
  
  const progress = scrollProgress;
  
  // Rotate object: full rotation every 0.5 scroll progress
  meshRef.current.rotation.x = progress * Math.PI * 4;
  meshRef.current.rotation.y = progress * Math.PI * 2;
}, [scrollProgress]);
```

### Example: Material Bloom/Glow (Premium Feel)

```typescript
// In your Three.js material setup
const material = new THREE.MeshStandardMaterial({
  color: 0xffcc00,       // Abelha yellow
  emissive: 0xffcc00,
  emissiveIntensity: scrollProgress * 0.8, // Glow increases with scroll
  metalness: 0.8,
  roughness: 0.2
});

// Optionally add bloom post-processing
useEffect(() => {
  bloomPass.strength = 0.5 + (scrollProgress * 0.5);
}, [scrollProgress]);
```

---

## 5. REACT THREE FIBER COMPLETE EXAMPLE

```typescript
// Scene.jsx
import React, { useEffect, useRef, useState } from 'react';
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { PerspectiveCamera, OrbitControls, Bloom, EffectComposer } from '@react-three/drei';
import * as THREE from 'three';

const ScrollProgressContext = React.createContext(0);

export function ScrollProgressProvider({ children }) {
  const [scrollProgress, setScrollProgress] = useState(0);
  
  useEffect(() => {
    const runway = document.querySelector('[data-runway]');
    if (!runway) return;
    
    const handleScroll = () => {
      const runwayHeight = runway.offsetHeight;
      const maxScroll = runwayHeight - window.innerHeight;
      const progress = Math.max(0, Math.min(1, window.scrollY / maxScroll));
      setScrollProgress(progress);
    };
    
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);
  
  return (
    <ScrollProgressContext.Provider value={scrollProgress}>
      {children}
    </ScrollProgressContext.Provider>
  );
}

function Hero3D() {
  const meshRef = useRef();
  const cameraRef = useRef();
  const scrollProgress = React.useContext(ScrollProgressContext);
  
  useFrame(() => {
    if (meshRef.current) {
      meshRef.current.rotation.y = scrollProgress * Math.PI * 2;
      meshRef.current.rotation.x = Math.sin(scrollProgress * Math.PI) * 0.5;
      
      // Glow intensity
      meshRef.current.material.emissiveIntensity = 0.3 + (scrollProgress * 0.7);
    }
    
    if (cameraRef.current) {
      cameraRef.current.position.z = 5 + (scrollProgress * 3);
    }
  });
  
  return (
    <>
      <PerspectiveCamera ref={cameraRef} position={[0, 0, 5]} makeDefault />
      <mesh ref={meshRef}>
        <boxGeometry args={[1, 1, 1]} />
        <meshStandardMaterial
          color={0xffcc00}
          emissive={0xffcc00}
          metalness={0.8}
          roughness={0.2}
        />
      </mesh>
      <pointLight position={[10, 10, 10]} intensity={1} />
      <ambientLight intensity={0.5} />
    </>
  );
}

export default function App() {
  return (
    <ScrollProgressProvider>
      <div data-runway style={{ height: '600vh' }} />
      <div
        style={{
          position: 'sticky',
          top: 0,
          height: '100vh',
          overflow: 'hidden'
        }}
      >
        <Canvas>
          <Hero3D />
          <EffectComposer>
            <Bloom luminanceThreshold={0.9} luminanceSmoothing={0.9} height={300} />
          </EffectComposer>
        </Canvas>
      </div>
    </ScrollProgressProvider>
  );
}
```

---

## 6. ACCESSIBILITY IN SCROLL-PINNED SITES — Critical

### Problem
Scroll-pinned sites are inherently hard to navigate with keyboard because:
- Focus gets lost in the sticky canvas
- Tab order is broken (canvas steals focus)
- Screen reader can't "see" the layered sections

### Solution

```typescript
// 1. Render sections in the DOM (off-screen), even though they're visually in the canvas
<div style={{ display: 'none' }} role="region" aria-label="Feature section 1">
  <h2>Feature 1</h2>
  <p>Description of feature 1...</p>
</div>

// 2. Make canvas non-interactive for keyboard
<canvas
  role="img"
  aria-label="Interactive 3D animation controlled by scroll"
  tabindex="-1"  // Not tabbable
/>

// 3. Provide keyboard navigation via hidden skip links
<a href="#feature-1" class="skip-link">Skip to Feature 1</a>
<a href="#feature-2" class="skip-link">Skip to Feature 2</a>

// 4. Respect prefers-reduced-motion
<style>
  @media (prefers-reduced-motion: reduce) {
    /* Instant scroll to final state instead of animated */
    canvas { display: none; }
    .sections { display: block; }
  }
</style>

// 5. Announce scroll position to screen readers
<div aria-live="polite" role="status" class="sr-only">
  {`Scroll progress: ${Math.round(scrollProgress * 100)}%`}
</div>
```

---

## 7. PERFORMANCE GOTCHAS — Half-Day of Debugging

### ❌ Gotcha 1: RAF Loop Thrashing
```typescript
// BAD: Updates camera every single RAF frame, even if scroll hasn't changed
useFrame(() => {
  camera.position.x = scrollProgress * 10; // scrollProgress hasn't changed!
});

// GOOD: Only update if scrollProgress actually changed
const prevProgressRef = useRef(0);
useFrame(() => {
  if (Math.abs(scrollProgress - prevProgressRef.current) > 0.001) {
    camera.position.x = scrollProgress * 10;
    prevProgressRef.current = scrollProgress;
  }
});
```

### ❌ Gotcha 2: Scroll Event Listener Not Throttled
```typescript
// BAD: Fires on every pixel scrolled (60+ times per second)
window.addEventListener('scroll', handleScroll);

// GOOD: Throttled via RAF
let rafId;
const handleScroll = () => {
  rafId = requestAnimationFrame(updateProgress);
};
window.addEventListener('scroll', handleScroll, { passive: true });
```

### ❌ Gotcha 3: Canvas Size Doesn't Match Window
```typescript
// BAD: Canvas is 1024x768 but window is 1920x1080
// Result: stretched, blurry render

// GOOD: Match canvas size to window
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
// Also update camera aspect ratio:
camera.aspect = window.innerWidth / window.innerHeight;
camera.updateProjectionMatrix();
```

### ❌ Gotcha 4: Three.js Scene Gets Laggy
```typescript
// BAD: 100k vertices, no frustum culling, no LOD
const geometry = new BoxGeometry(1, 1, 1);
for (let i = 0; i < 1000; i++) {
  mesh = new Mesh(geometry);
  scene.add(mesh);
}

// GOOD: Limit geometry complexity, use instances
const geometry = new BoxGeometry(1, 1, 1);
const material = new MeshStandardMaterial();
const instancedMesh = new InstancedMesh(geometry, material, 1000);
scene.add(instancedMesh);
```

### ❌ Gotcha 5: Opacity Fade Animation Looks Bad
```typescript
// BAD: Abrupt opacity change (looks choppy)
opacity = progress < 0.5 ? 0 : 1;

// GOOD: Smooth fade (cubic easing)
const easeInOutCubic = (t) => {
  return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
};
const fadeStart = 0.28, fadeDuration = 0.05;
opacity = Math.max(0, Math.min(1, (progress - fadeStart) / fadeDuration));
opacity = easeInOutCubic(opacity);
```

---

## 8. TESTING SCROLL-PINNED SITES

### Manual Testing
```
1. Scroll slowly from top to bottom (0% → 100%)
   - Do sections appear/disappear at the right times?
   - Is camera movement smooth?
   - Are there jumps or stuttering?

2. Scroll fast (fling scroll)
   - Does animation keep up?
   - Does scrolling feel responsive?

3. Test on mobile (slower devices)
   - Reduce mesh complexity or use LOD?
   - Is performance acceptable?

4. Keyboard navigation (TAB key)
   - Can you reach all interactive elements?
   - Is focus visible?
   - Does focus move logically through sections?

5. prefers-reduced-motion test
   - Disable animations in settings
   - Does site still work?
```

### Performance Measurement
```bash
# Lighthouse performance audit
npx lighthouse https://your-site.com --view

# Chrome DevTools Performance tab
# 1. Record 5-second scroll interaction
# 2. Check for:
#    - FPS drops below 60
#    - Long tasks (> 50ms)
#    - Layout thrashing (repeated forced layouts)
```

---

## 9. COMPLETE CHECKLIST — Before Launch

- [ ] **Scroll Progress** calculated and responsive (0.0 to 1.0)
- [ ] **Runway height** set correctly (visible height: 600vh+)
- [ ] **Viewport container** has `position: sticky; height: 100vh`
- [ ] **Canvas/Three.js** renders smoothly (60 FPS target)
- [ ] **Sections fade** at correct waypoints (28%, 50%, 72%, etc.)
- [ ] **Camera movement** matches original (pan, rotate, zoom)
- [ ] **Object animations** match (rotation, scale, material changes)
- [ ] **Bloom/glow effects** applied and performant
- [ ] **RAF throttling** in place (no frame drops on scroll)
- [ ] **Mobile responsiveness** tested (smaller device performance)
- [ ] **Keyboard navigation** works (Tab, Shift+Tab through sections)
- [ ] **Focus visible** indicators present (Abelha yellow outline)
- [ ] **prefers-reduced-motion** respected (animations disabled if set)
- [ ] **Screen reader** announces section progress
- [ ] **Core Web Vitals** pass (LCP < 2.5s, CLS < 0.1)

---

## References
- [React Three Fiber Docs](https://docs.pmnd.rs/react-three-fiber/getting-started/introduction)
- [Three.js Manual](https://threejs.org/manual/)
- [WebGL Fundamentals](https://webglfundamentals.org/)
- [WCAG 2.1 for Animation](https://www.w3.org/WAI/WCAG21/Understanding/animation-from-interactions.html)

---

**Remember**: Scroll-pinned sites are powerful but complex. The extra week of development pays off in user delight. 🎬✨
