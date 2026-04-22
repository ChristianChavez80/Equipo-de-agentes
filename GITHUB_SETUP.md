# 🚀 Configuración para GitHub - Abelha Studio

Tu repositorio local está listo. Aquí está cómo subirlo a GitHub:

## Opción 1: Crear Repositorio Nuevo en GitHub

### Paso 1: Crear repositorio en GitHub
1. Ve a https://github.com/new
2. Nombre: `abelha-studio-team`
3. Descripción: "Abelha Studio - Team of 20 specialized AI agents for Tecnología Humana"
4. Visibilidad: **Public** (para que sea accesible)
5. **NO** inicialices con README (ya tenemos uno)
6. Click "Create repository"

### Paso 2: Conectar repo local con GitHub

```bash
cd "C:\Users\xzxgu\OneDrive\Área de Trabalho\Equipo de agentes"

# Agregar remote (reemplaza USER con tu usuario de GitHub)
git remote add origin https://github.com/USER/abelha-studio-team.git

# Cambiar rama a main
git branch -M main

# Hacer push
git push -u origin main
```

## Opción 2: Si ya tienes repositorio en GitHub

```bash
cd "C:\Users\xzxgu\OneDrive\Área de Trabalho\Equipo de agentes"

# Reemplaza con tu URL de GitHub
git remote add origin https://github.com/USER/REPO.git
git branch -M main
git push -u origin main
```

---

## ✅ Estado Actual del Repositorio

```
Repositorio Local: LISTO ✅
├── 36 archivos
├── 20 skills (agentes)
├── Documentación completa
└── Commit inicial: d09f78c
```

---

## 📋 Checklist

- [ ] Crear repositorio en GitHub
- [ ] Copiar URL (HTTPS o SSH)
- [ ] Ejecutar `git remote add origin [URL]`
- [ ] Ejecutar `git push -u origin main`
- [ ] Verificar en GitHub que todo está subido

---

## 🔐 Nota sobre SSH vs HTTPS

**HTTPS (Más fácil):**
```bash
git remote add origin https://github.com/USER/abelha-studio-team.git
```
Te pedirá credenciales (usuario + token)

**SSH (Más seguro):**
```bash
git remote add origin git@github.com:USER/abelha-studio-team.git
```
Requiere configuración de claves SSH

---

## 📞 ¿Necesitas ayuda?

1. Crea el repo en GitHub
2. Copia la URL (HTTPS)
3. Ejecuta en terminal:
   ```bash
   cd "C:\Users\xzxgu\OneDrive\Área de Trabalho\Equipo de agentes"
   git remote add origin https://github.com/TU_USUARIO/abelha-studio-team.git
   git push -u origin main
   ```

---

**Estado:** ✅ Listo para GitHub  
**Fecha:** 2026-04-22
