# 📚 Sistema de Asesorías de Matemáticas

Aplicación web desarrollada con Streamlit para agendar asesorías de matemáticas gratuitas.

## ✨ Características

- 📅 **Calendario interactivo** para seleccionar fechas
- 🕐 **Gestión de horarios** disponibles y ocupados
- 📝 **Formulario de registro** con validación
- 📋 **Visualización de citas** agendadas
- 🔍 **Búsqueda y filtrado** de citas
- 🗑️ **Cancelación** de citas
- 💾 **Persistencia de datos** con JSON
- 🎨 **Interfaz amigable** y responsive

## 🚀 Instalación

1. Clona o descarga este repositorio

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## ▶️ Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📖 Uso

### Agendar una cita:
1. Ve a la pestaña "📅 Agendar Cita"
2. Selecciona una fecha disponible
3. Elige un horario libre
4. Completa el formulario con tus datos
5. Haz clic en "Confirmar Asesoría"

### Ver tus citas:
1. Ve a la pestaña "📋 Mis Citas"
2. Navega por las citas agendadas
3. Usa el buscador para filtrar por nombre o email
4. Cancela citas si es necesario

### Información:
- La pestaña "ℹ️ Información" contiene detalles sobre:
  - Qué ofrecemos
  - Temas cubiertos
  - Horarios disponibles
  - Cómo prepararte

## 📁 Archivos

- `app.py` - Aplicación principal de Streamlit
- `requirements.txt` - Dependencias del proyecto
- `citas.json` - Base de datos de citas (se crea automáticamente)

## 🛠️ Tecnologías

- **Streamlit** - Framework web para Python
- **JSON** - Almacenamiento de datos
- **Python 3.7+** - Lenguaje de programación

## 📝 Configuración

Puedes personalizar los horarios disponibles editando la lista `HORARIOS_DISPONIBLES` en `app.py`:

```python
HORARIOS_DISPONIBLES = [
    "09:00", "10:00", "11:00", "12:00", 
    "14:00", "15:00", "16:00", "17:00", "18:00"
]
```

## 🎯 Características futuras

- [ ] Notificaciones por email
- [ ] Integración con Google Calendar
- [ ] Sistema de recordatorios
- [ ] Autenticación de usuarios
- [ ] Base de datos más robusta (SQLite/PostgreSQL)
- [ ] Estadísticas y reportes

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Siéntete libre de abrir issues o pull requests.

---

**¡Hecho con ❤️ para ayudar a estudiantes!**
