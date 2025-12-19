import streamlit as st
import json
import os
from datetime import datetime, timedelta, date, time
from streamlit_calendar import calendar

# Configuración de la página
st.set_page_config(
    page_title="Asesorías de Matemáticas",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Archivo para almacenar las citas
CITAS_FILE = "citas.json"

# Niveles educativos
NIVELES = ["Primaria", "Secundaria", "Preparatoria", "Universidad", "Otro"]

# Horarios disponibles (24h format)
HORARIOS_DISPONIBLES = [
    "09:00", "10:00", "11:00", "12:00", 
    "14:00", "15:00", "16:00", "17:00", "18:00"
]

# Funciones para gestionar citas
def cargar_citas():
    """Carga las citas desde el archivo JSON"""
    if os.path.exists(CITAS_FILE):
        try:
            with open(CITAS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def guardar_citas(citas):
    """Guarda las citas en el archivo JSON"""
    with open(CITAS_FILE, 'w', encoding='utf-8') as f:
        json.dump(citas, f, ensure_ascii=False, indent=2)

def agendar_cita(fecha_str, hora, nombre, email, tema, nivel, comentarios=""):
    """Agenda una nueva cita"""
    citas = cargar_citas()
    
    if fecha_str not in citas:
        citas[fecha_str] = []
    
    cita = {
        "hora": hora,
        "nombre": nombre,
        "email": email,
        "tema": tema,
        "nivel": nivel,
        "comentarios": comentarios,
        "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    citas[fecha_str].append(cita)
    guardar_citas(citas)
    return cita

def cancelar_cita(fecha_str, hora):
    """Cancela una cita existente"""
    citas = cargar_citas()
    
    if fecha_str in citas:
        citas[fecha_str] = [c for c in citas[fecha_str] if c["hora"] != hora]
        
        if not citas[fecha_str]:
            del citas[fecha_str]
        
        guardar_citas(citas)
        return True
    return False

def generar_eventos_calendario():
    """Genera eventos para el calendario en formato FullCalendar"""
    eventos = []
    citas = cargar_citas()
    
    # Generar horarios disponibles para los próximos 60 días
    fecha_inicio = date.today()
    fecha_fin = fecha_inicio + timedelta(days=60)
    
    fecha_actual = fecha_inicio
    while fecha_actual <= fecha_fin:
        # Solo días laborables (lunes a viernes)
        if fecha_actual.weekday() < 5:
            fecha_str = fecha_actual.strftime("%Y-%m-%d")
            
            for hora in HORARIOS_DISPONIBLES:
                # Crear datetime completo
                hora_parts = hora.split(":")
                hora_inicio = datetime.combine(fecha_actual, time(int(hora_parts[0]), int(hora_parts[1])))
                hora_fin = hora_inicio + timedelta(hours=1)
                
                # Verificar si está ocupado
                ocupado = False
                titulo = "Disponible"
                color = "#28a745"  # Verde
                
                if fecha_str in citas:
                    for cita in citas[fecha_str]:
                        if cita["hora"] == hora:
                            ocupado = True
                            titulo = f"Ocupado - {cita['tema']}"
                            color = "#dc3545"  # Rojo
                            break
                
                evento = {
                    "title": titulo,
                    "start": hora_inicio.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": hora_fin.strftime("%Y-%m-%dT%H:%M:%S"),
                    "backgroundColor": color,
                    "borderColor": color,
                    "extendedProps": {
                        "disponible": not ocupado,
                        "fecha": fecha_str,
                        "hora": hora
                    }
                }
                eventos.append(evento)
        
        fecha_actual += timedelta(days=1)
    
    return eventos

# Estilo CSS personalizado
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        padding: 1rem 0;
        font-size: 2.5rem;
        font-weight: bold;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .info-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .legend {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 1rem 0;
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 0.5rem;
    }
    .legend-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .legend-color {
        width: 20px;
        height: 20px;
        border-radius: 4px;
    }
    .cita-card {
        background-color: #e8f4f8;
        padding: 1.2rem;
        border-radius: 0.8rem;
        margin: 0.8rem 0;
        border-left: 5px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Inicializar estado de sesión
if 'mostrar_formulario' not in st.session_state:
    st.session_state.mostrar_formulario = False
if 'fecha_seleccionada' not in st.session_state:
    st.session_state.fecha_seleccionada = None
if 'hora_seleccionada' not in st.session_state:
    st.session_state.hora_seleccionada = None
if 'cita_confirmada' not in st.session_state:
    st.session_state.cita_confirmada = None

# Encabezado
st.markdown("<h1 class='main-header'>📚 Asesorías de Matemáticas Gratuitas</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Selecciona un horario disponible en el calendario</p>", unsafe_allow_html=True)

# Banner informativo
st.markdown("""
<div class='info-banner'>
    <h3 style='color: white; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);'>✨ ¡Bienvenido a mi plataforma de asesorías!</h3>
    <p style='color: white; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);'>Matemáticas + Python 🐍 | Asesorías por Discord 🎧 | 100% Online</p>
    <p style='color: white; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);'>Selecciona cualquier horario <strong>verde</strong> en el calendario para agendar tu asesoría conmigo</p>
</div>
""", unsafe_allow_html=True)

# Buy Me a Coffee y Discord
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div style='text-align: center; padding: 1rem; background-color: #fff9e6; border-radius: 0.8rem; border: 2px solid #ffdd00; margin-bottom: 1rem;'>
        <p style='color: #333; margin: 0.5rem 0;'><strong>☕ ¿Te ayudé con tus matemáticas?</strong></p>
        <p style='color: #666; font-size: 0.9rem; margin: 0.5rem 0;'>Las asesorías son gratuitas, pero si quieres apoyarme con un café, ¡lo apreciaría mucho! 😊</p>
        <a href='https://buymeacoffee.com/ingjoma' target='_blank' style='display: inline-block; background-color: #FFDD00; color: #000; padding: 0.7rem 1.5rem; border-radius: 0.5rem; text-decoration: none; font-weight: bold; margin-top: 0.5rem;'>☕ Invítame un café</a>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='text-align: center; padding: 1rem; background-color: #e8f3ff; border-radius: 0.8rem; border: 2px solid #5865F2; margin-bottom: 1rem;'>
        <p style='color: #333; margin: 0.5rem 0;'><strong>💬 ¿Dudas rápidas?</strong></p>
        <p style='color: #666; font-size: 0.9rem; margin: 0.5rem 0;'>Únete a la comunidad de Discord. ¡Resuelvo dudas que no necesitan 1 hora completa!</p>
        <a href='https://discord.gg/sFsmx9krT7' target='_blank' style='display: inline-block; background-color: #5865F2; color: white; padding: 0.7rem 1.5rem; border-radius: 0.5rem; text-decoration: none; font-weight: bold; margin-top: 0.5rem;'>💬 Unirme a Discord</a>
    </div>
    """, unsafe_allow_html=True)

# Leyenda
st.markdown("""
<div class='legend'>
    <div class='legend-item'>
        <div class='legend-color' style='background-color: #28a745;'></div>
        <span style='color: #333;'><strong>Disponible</strong> - Haz clic para agendar</span>
    </div>
    <div class='legend-item'>
        <div class='legend-color' style='background-color: #dc3545;'></div>
        <span style='color: #333;'><strong>Ocupado</strong> - Horario no disponible</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Tabs principales
tab1, tab2, tab3 = st.tabs(["📅 Calendario", "❓ Preguntas Frecuentes", "ℹ️ Información"])

with tab1:
    # Generar eventos
    eventos = generar_eventos_calendario()
    
    # Configuración del calendario
    calendar_options = {
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek,timeGridDay"
        },
        "initialView": "timeGridWeek",
        "selectable": True,
        "selectMirror": True,
        "dayMaxEvents": True,
        "weekends": False,  # Solo días laborables
        "slotMinTime": "09:00:00",
        "slotMaxTime": "19:00:00",
        "allDaySlot": False,
        "height": 650,
        "locale": "es",
        "buttonText": {
            "today": "Hoy",
            "month": "Mes",
            "week": "Semana",
            "day": "Día"
        }
    }
    
    # Mostrar calendario
    calendar_component = calendar(
        events=eventos,
        options=calendar_options,
        custom_css=""
    )
    
    # Procesar clic en evento
    if calendar_component.get("eventClick"):
        evento_clickeado = calendar_component["eventClick"]["event"]
        props = evento_clickeado.get("extendedProps", {})
        
        if props.get("disponible"):
            # Solo actualizar si es un horario diferente al actual
            nueva_fecha = props.get("fecha")
            nueva_hora = props.get("hora")
            
            if (st.session_state.fecha_seleccionada != nueva_fecha or 
                st.session_state.hora_seleccionada != nueva_hora):
                st.session_state.mostrar_formulario = True
                st.session_state.fecha_seleccionada = nueva_fecha
                st.session_state.hora_seleccionada = nueva_hora
                st.session_state.cita_confirmada = None
                st.rerun()
    
    # Mostrar comprobante si hay una cita confirmada
    if st.session_state.cita_confirmada:
        st.success("🎉 ¡Asesoría reservada con éxito!")
        st.balloons()
        
        cita_info = st.session_state.cita_confirmada
        fecha_obj = datetime.strptime(cita_info['fecha'], "%Y-%m-%d")
        comprobante = f"""═══════════════════════════════════════
📚 COMPROBANTE DE ASESORÍA
═══════════════════════════════════════

👤 Estudiante: {cita_info['nombre']}
📧 Email: {cita_info['email']}
📅 Fecha: {fecha_obj.strftime('%d/%m/%Y')}
🕐 Hora: {cita_info['hora']} hs
📚 Tema: {cita_info['tema']}
🎓 Nivel: {cita_info['nivel']}
{f"💬 Comentarios: {cita_info['comentarios']}" if cita_info.get('comentarios') else ''}

🎮 DONDE NOS ENCONTRAMOS:
👉 Discord: discord.gg/sFsmx9krT7
🎧 Canal de voz: "Asesorías Matemáticas"

═══════════════════════════════════════
Te enviaré un recordatorio por email.
¡Te veo en Discord!
═══════════════════════════════════════
"""
        st.code(comprobante, language=None)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Entendido - Volver al calendario", use_container_width=True, type="primary"):
                st.session_state.cita_confirmada = None
                st.rerun()
        with col2:
            if st.button("➕ Agendar otra cita", use_container_width=True):
                st.session_state.cita_confirmada = None
                st.rerun()
    
    # Mostrar formulario de registro si se seleccionó un horario (y no hay cita confirmada)
    elif st.session_state.mostrar_formulario:
        st.divider()
        st.success(f"✅ Has seleccionado: {st.session_state.fecha_seleccionada} a las {st.session_state.hora_seleccionada} hs")
        
        with st.form("formulario_rapido", clear_on_submit=True):
            st.subheader("📝 Completa tus datos")
            
            col1, col2 = st.columns(2)
            
            with col1:
                nombre = st.text_input("Nombre completo *", placeholder="Ej: Juan Pérez")
                email = st.text_input("Correo electrónico *", placeholder="juan@ejemplo.com")
                nivel = st.selectbox(
                    "Nivel educativo *",
                    NIVELES,
                    index=2
                )
            
            with col2:
                tema = st.selectbox(
                    "Tema de la asesoría *",
                    ["Álgebra", "Cálculo", "Geometría", "Trigonometría", 
                     "Estadística", "Probabilidad", "Aritmética", 
                     "Ecuaciones Diferenciales", "Otro"]
                )
                
                comentarios = st.text_area(
                    "Comentarios o dudas específicas (opcional)",
                    placeholder="Ej: Necesito ayuda con derivadas",
                    height=100
                )
            
            col1, col2 = st.columns([1, 1])
            with col1:
                submitted = st.form_submit_button("✅ Confirmar Asesoría", use_container_width=True, type="primary")
            with col2:
                cancelar = st.form_submit_button("❌ Cancelar", use_container_width=True)
            
            if cancelar:
                st.session_state.mostrar_formulario = False
                st.session_state.fecha_seleccionada = None
                st.session_state.hora_seleccionada = None
                st.rerun()
            
            if submitted:
                if not nombre or not email or not tema:
                    st.error("❌ Por favor, completa todos los campos obligatorios.")
                elif "@" not in email:
                    st.error("❌ Por favor, ingresa un correo electrónico válido.")
                else:
                    cita = agendar_cita(
                        st.session_state.fecha_seleccionada,
                        st.session_state.hora_seleccionada,
                        nombre, email, tema, nivel, comentarios
                    )
                    
                    # Guardar info de la cita para mostrar comprobante
                    st.session_state.cita_confirmada = {
                        'fecha': st.session_state.fecha_seleccionada,
                        'hora': st.session_state.hora_seleccionada,
                        'nombre': nombre,
                        'email': email,
                        'tema': tema,
                        'nivel': nivel,
                        'comentarios': comentarios
                    }
                    
                    # Limpiar formulario
                    st.session_state.mostrar_formulario = False
                    st.session_state.fecha_seleccionada = None
                    st.session_state.hora_seleccionada = None
                    st.rerun()

with tab2:
    st.header("❓ Preguntas Frecuentes")
    
    with st.expander("🎬 ¿Cómo son las asesorías?"):
        st.write("""
Las asesorías son **100% online por Discord** 🎮

**Nos reunimos en el canal de voz:** 🎧 **"Asesorías Matemáticas"**

El canal es de **libre acceso** dentro del servidor. Una vez que te unas a Discord, solo tienes que:
1. Unirte al servidor: [discord.gg/sFsmx9krT7](https://discord.gg/sFsmx9krT7)
2. Buscar el canal de voz 🎧 "Asesorías Matemáticas"
3. Entrar a la hora acordada

Compartiré pantalla para explicar y programar en vivo. ¡Super fácil!
""")
    with st.expander("💬 ¿Y si tengo una duda pequeña?"):
        st.write("¡Únete a mi **comunidad de Discord**: [discord.gg/sFsmx9krT7](https://discord.gg/sFsmx9krT7)")
        st.write("")
        st.write("**Perfecto para:**")
        st.write("- Dudas rápidas que no necesitan 1 hora completa")
        st.write("- Preguntas específicas sobre un ejercicio")
        st.write("- Consultas sobre Python")
        st.write("- Cancelar o reprogramar citas")
        st.write("- Charlar con otros estudiantes")
        st.write("")
        st.write("¡Envíame un **mensaje directo** por Discord y te respondo! 🚀")    
    with st.expander("🕐 ¿Cuánto dura cada sesión?"):
        st.write("Cada asesoría tiene una duración de **1 hora**.")
    
    with st.expander("💰 ¿Realmente es gratis?"):
        st.write("Sí, las asesorías son **100% gratuitas**, sin ningún costo ni compromiso.")
        st.write("")
        st.write("Sin embargo, si te ayudé y quieres apoyarme con un café, puedes hacerlo de forma **voluntaria** en: [buymeacoffee.com/ingjoma](https://buymeacoffee.com/ingjoma) ☕")
        st.write("")
        st.write("¡Pero no es obligatorio en absoluto! Lo importante es que aprendas. 😊")
    with st.expander("🐍 ¿Necesito saber Python?"):
        st.write("**No es necesario**. Te enseño desde cero. Si ya sabes, mejor aún, profundizaremos más.")
    
    with st.expander("💻 ¿Qué necesito para la asesoría?"):
        st.write("""
        - **Cuenta de Discord** (gratis, fácil de crear)
        - **Conexión a internet estable**
        - **Computadora** (preferible) o tablet con Discord
        - Tus **dudas o ejercicios específicos**
        - Cuaderno para tomar notas (opcional)
        - Muchas ganas de aprender 🚀
        
        👉 Si no tienes Discord, descárgalo aquí: [discord.com](https://discord.com)
        """)
    
    with st.expander("� ¿Dónde nos encontramos?"):
        st.write("""
        **En el canal de voz de Discord: 🎧 "Asesorías Matemáticas"**
        
        Pasos para entrar:
        1. Únete al servidor: [discord.gg/sFsmx9krT7](https://discord.gg/sFsmx9krT7)
        2. Busca el canal de voz llamado **"Asesorías Matemáticas"**
        3. Haz clic para unirte a la hora de tu cita
        
        ¡Es un canal de libre acceso para todos! No necesitas permisos especiales.
        """)
    
    with st.expander("❌ ¿Cómo cancelo o reprogramo mi cita?"):
        st.write("""Contáctame con anticipación (al menos 2 horas antes):
        
**Opción 1 (Preferida):** Mándame un **mensaje directo por Discord**
- Únete al servidor: [discord.gg/sFsmx9krT7](https://discord.gg/sFsmx9krT7)
- Búscame y envíame un MD (Mensaje Directo)

**Opción 2:** Si no tienes Discord, envíame un email a:
- 📧 **josemariagarciamarquez2.72@gmail.com**
- Subject: **ASESORÍA**
        """)
    
    with st.expander("🎓 ¿Para qué niveles son las asesorías?"):
        st.write("Desde **primaria hasta universidad**. Cada sesión se adapta completamente a tu nivel y necesidades.")
    
    with st.expander("📅 ¿Con cuánta anticipación debo agendar?"):
        st.write("Puedes agendar hasta con **2 meses de anticipación**. Te recomiendo reservar con al menos **1 día** de antelación.")
    
    with st.expander("🔄 ¿Puedo agendar varias sesiones?"):
        st.write("¡Por supuesto! Puedes agendar tantas sesiones como necesites. Si necesitas un plan de estudio regular, podemos coordinarlo.")
    
    with st.expander("📧 ¿Cómo confirmo mi cita?"):
        st.write("""
Después de agendar:
1. Te enviaré un **email de confirmación** con todos los detalles
2. Te recordaré unirte al Discord: [discord.gg/sFsmx9krT7](https://discord.gg/sFsmx9krT7)
3. El día de la asesoría, solo entra al canal de voz 🎧 **"Asesorías Matemáticas"**

¡Nos vemos allí! 🚀
""")
    
    st.divider()
    
    st.info("💡 **¿Más preguntas?** Mándame un mensaje directo por Discord o email (ver sección de Información)")

with tab3:
    st.header("ℹ️ Información sobre las Asesorías")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📚 ¿Qué ofrezco?
        - Asesorías **100% online por Discord** 🎮
        - En el canal de voz 🎧 **"Asesorías Matemáticas"**
        - Personalizadas de matemáticas
        - **🐍 Todo explicado con código Python**
        - Aprende matemáticas + programación al mismo tiempo
        - Todos los niveles (primaria, secundaria, universidad)
        - Sesiones de 1 hora
        - Completamente **GRATIS** (aportes voluntarios)
        
        ### 📖 Temas que cubro
        - Álgebra básica y avanzada
        - Cálculo diferencial e integral
        - Geometría y trigonometría
        - Estadística y probabilidad
        - Ecuaciones diferenciales
        - Y mucho más...
        """)
    
    with col2:
        st.markdown("""
        ### 🕐 Mis Horarios
        **Estoy disponible de lunes a viernes**
        - Mañana: 09:00 - 12:00
        - Tarde: 14:00 - 18:00
        
        *Cada sesión dura 1 hora*
        
        ### 📝 Cómo prepararte
        1. Trae tus dudas o ejercicios específicos
        2. Cuaderno y lapicera para tomar notas
        3. Material del tema a tratar (opcional)
        4. Ganas de aprender 🚀
        """)
    
    st.divider()
    
    # Destacar Python
    st.markdown("""
    <div style='background: linear-gradient(135deg, #3776ab 0%, #ffd43b 100%); padding: 2rem; border-radius: 1rem; margin-bottom: 2rem;'>
        <h3 style='color: white; text-align: center; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>🐍 ¿Por qué Python?</h3>
        <p style='color: white; text-align: center; font-size: 1.1rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);'>
            Complemento todas las asesorías con <strong>código en Python</strong>.<br>
            Así no solo entiendes la teoría matemática, sino que también te vas <strong>forjando en programación</strong>.<br>
            📊 Visualizaciones | 🧮 Cálculos prácticos | 💻 Fundamentos de código
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background-color: #f0f8ff; border-radius: 1rem;'>
        <h3 style='color: #333;'>💬 Formas de contacto</h3>
        <p style='color: #555; font-size: 1.1rem; margin: 1rem 0;'><strong>🎮 Discord (Preferido):</strong></p>
        <p style='color: #555;'><a href='https://discord.gg/sFsmx9krT7' target='_blank' style='font-size: 1.1rem;'>discord.gg/sFsmx9krT7</a></p>
        <p style='color: #666; font-size: 0.9rem;'>Para dudas rápidas, cancelar/reprogramar citas, o cualquier consulta</p>
        <hr style='margin: 1.5rem 0; border: none; border-top: 1px solid #ddd;'>
        <p style='color: #555; margin-top: 1rem;'><strong>📧 Email (Si no tienes Discord):</strong></p>
        <p style='color: #555;'>josemariagarciamarquez2.72@gmail.com</p>
        <p style='color: #999; font-size: 0.85rem;'>Subject: <strong>ASESORÍA</strong></p>
    </div>
    """, unsafe_allow_html=True)

# Pie de página
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <small>Hecho con ❤️ para ayudar a estudiantes | © 2025 Asesorías de Matemáticas</small>
</div>
""", unsafe_allow_html=True)

# ============================================
# PANEL DE ADMINISTRACIÓN (SIDEBAR)
# ============================================
with st.sidebar:
    st.title("🔐 Panel de Administración")
    
    # Contraseña simple
    password = st.text_input("Contraseña:", type="password")
    
    if password == "admin123":  # Cambia esta contraseña
        st.success("✅ Acceso concedido")
        st.divider()
        
        st.header("📋 Gestión de Citas")
        
        citas = cargar_citas()
        
        if not citas:
            st.info("📭 No hay citas agendadas")
        else:
            # Filtros admin
            col1, col2 = st.columns(2)
            with col1:
                mostrar_pasadas = st.checkbox("Ver pasadas", value=False)
            with col2:
                buscar_admin = st.text_input("🔍 Buscar", "")
            
            # Estadísticas
            total_citas = sum(len(citas_dia) for citas_dia in citas.values())
            st.metric("Total de citas", total_citas)
            
            st.divider()
            
            # Listar citas
            fechas_ordenadas = sorted(citas.keys())
            
            for fecha_str in fechas_ordenadas:
                fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d").date()
                
                if not mostrar_pasadas and fecha_obj < date.today():
                    continue
                
                citas_dia = citas[fecha_str]
                citas_dia_ordenadas = sorted(citas_dia, key=lambda x: x["hora"])
                
                # Aplicar filtro de búsqueda
                if buscar_admin:
                    citas_dia_ordenadas = [
                        c for c in citas_dia_ordenadas 
                        if buscar_admin.lower() in c["nombre"].lower() or 
                           buscar_admin.lower() in c["email"].lower()
                    ]
                
                if not citas_dia_ordenadas:
                    continue
                
                st.subheader(fecha_obj.strftime('%d/%m/%Y'))
                
                for cita in citas_dia_ordenadas:
                    with st.container():
                        st.write(f"**🕐 {cita['hora']}**")
                        st.write(f"👤 {cita['nombre']}")
                        st.write(f"📧 {cita['email']}")
                        st.write(f"📚 {cita['tema']} ({cita.get('nivel', 'N/A')})")
                        if cita.get('comentarios'):
                            st.write(f"💬 {cita['comentarios']}")
                        
                        if st.button("🗑️ Eliminar", key=f"admin_del_{fecha_str}_{cita['hora']}"):
                            if cancelar_cita(fecha_str, cita['hora']):
                                st.success("Eliminada")
                                st.rerun()
                        
                        st.divider()
    
    elif password:
        st.error("❌ Contraseña incorrecta")
    else:
        st.info("👨‍💼 Solo para el administrador")
