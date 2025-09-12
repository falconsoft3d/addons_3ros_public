# MuK Web Theme Addons

Este repositorio contiene un conjunto de módulos de Odoo diseñados para mejorar la experiencia de usuario del backend de Odoo con un tema moderno y funcionalidades adicionales de personalización.

## 📦 Módulos Incluidos

### 🎨 muk_web_theme
**Tema Principal del Backend**
- Diseño moderno y responsive para Odoo Community
- Compatible con dispositivos móviles
- Preferencias de diseño personalizables
- Depende de todos los otros módulos para funcionalidad completa

### 📱 muk_web_appsbar
**Barra Lateral de Aplicaciones**
- Añade una barra lateral con navegación rápida de apps
- Lista de todas las aplicaciones instaladas
- Configuraciones de tamaño: invisible, pequeña, grande
- Imagen personalizable por empresa

### 💬 muk_web_chatter
**Mejoras del Chatter**
- Diseño mejorado del chatter
- Opciones de posición personalizable en vista formulario
- Toggle para mostrar/ocultar información de seguimiento
- Estado persistente en localStorage

### 🎨 muk_web_colors
**Personalización de Colores**
- Esquemas de colores personalizables
- Soporte para temas claro y oscuro
- Colores configurables: brand, primary, success, info, warning, danger
- Reset a valores por defecto

### 🖼️ muk_web_dialog
**Configuración de Diálogos**
- Preferencias de tamaño de diálogos
- Opciones: minimizar, maximizar
- Configuración por usuario

## 🚀 Instalación

1. Clona este repositorio en tu directorio de addons de Odoo:
```bash
git clone https://github.com/falconsoft3d/addons_3ros_public.git
```

2. Actualiza la lista de aplicaciones en Odoo

3. Instala el módulo principal `muk_web_theme` que automáticamente instalará las dependencias

## 🛠️ Dependencias

- **Odoo 17.0+**
- Módulos base: `base_setup`, `web`, `mail`
- Los módulos están interrelacionados según el siguiente orden:
  - `muk_web_appsbar`, `muk_web_colors`, `muk_web_dialog`, `muk_web_chatter` → `muk_web_theme`

## ⚙️ Configuración

### Personalización de Colores
1. Ve a **Configuración → Configuración General**
2. Busca la sección "Web Colors"
3. Personaliza los colores para temas claro y oscuro
4. Guarda los cambios

### Preferencias de Usuario
- **Barra Lateral**: Usuario → Preferencias → Tipo de Barra Lateral
- **Diálogos**: Usuario → Preferencias → Tamaño de Diálogo
- **Chatter**: Se configura automáticamente por vista

## 🎯 Características Principales

- ✅ **Responsive Design**: Adaptado para dispositivos móviles
- ✅ **Temas Claro/Oscuro**: Soporte completo con personalización
- ✅ **Configuración por Usuario**: Cada usuario puede personalizar su experiencia
- ✅ **Estado Persistente**: Las preferencias se guardan automáticamente
- ✅ **Fácil Personalización**: Interfaz intuitiva para cambios de diseño

## 🔧 Desarrollo

### Estructura del Código
- **Python**: Modelos y configuraciones en `/models/`
- **JavaScript**: Componentes OWL en `/static/src/`
- **SCSS**: Estilos y variables en `/static/src/scss/`
- **XML**: Vistas y templates en `/views/` y `/templates/`

### Mejoras Recientes
- ✅ Documentación mejorada en código Python y JavaScript
- ✅ Consistencia en formato y estilo de código
- ✅ Constantes centralizadas para reducir duplicación
- ✅ Validaciones de entrada mejoradas
- ✅ Manejo de errores más robusto

## 📄 Licencia

LGPL-3 - Ver archivos de manifiesto individuales para detalles específicos

## 👥 Autores

- **MuK IT** - Desarrollo original
- **Mathias Markl** - Contribuidor principal
- Sitio web: [http://www.mukit.at](http://www.mukit.at)
- Demo: [https://mukit.at/demo](https://mukit.at/demo)

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request
