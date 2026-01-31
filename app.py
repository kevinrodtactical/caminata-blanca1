import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime

# --- CONFIGURACIÓN E INTERFAZ ---
st.set_page_config(page_title="OPS: CAMINATA BLANCA V3.0", layout="wide")

# --- VARIABLES OPERATIVAS ---
LINK_GRUPO = "https://chat.whatsapp.com/D40mfH1s3DyAiTGEs8ykL1"
NUM_SOMBRA = "+51931382247"
FECHA_OP = "01-FEB-2026"

# --- DATA TÁCTICA CON COORDENADAS PRECISAS ---
DATA = {
    "tambos": [
        {"name": "Tambo Arequipa-C25", "lat": -12.08945, "lon": -77.03360},
        {"name": "Tambo Risso (Arequipa 19)", "lat": -12.08375, "lon": -77.03485},
        {"name": "Tambo Teleticket (Arequipa 13)", "lat": -12.07820, "lon": -77.03580}
    ],
    "salud": [
        {"name": "Clínica Javier Prado", "lat": -12.09135, "lon": -77.02845, "color": "red"},
        {"name": "Hospital Rebagliati", "lat": -12.07795, "lon": -77.04045, "color": "orange"}
    ],
    "extraccion": [
        {"name": "EXTRACCIÓN RISSO", "lat": -12.08380, "lon": -77.03310},
        {"name": "EXTRACCIÓN CANEVARO", "lat": -12.07920, "lon": -77.03410}
    ]
}

# --- TRAYECTORIAS EXACTAS ---
# Av. Arequipa (San Isidro a Lima)
RUTA_AREQUIPA = [
    [-12.09245, -77.03300], # Cruce Javier Prado
    [-12.08375, -77.03480], # Risso
    [-12.07915, -77.03575], # Canevaro
    [-12.07085, -77.03730]  # Parque Cervantes (Llegada)
]

# Av. Petit Thouars (Ruta Sombra - Sentido Sur a Norte)
RUTA_PETIT_THOUARS = [
    [-12.09210, -77.03135], # Inicio paralela J. Prado
    [-12.08345, -77.03315], # Altura Risso
    [-12.07885, -77.03410], # Altura Canevaro
    [-12.07035, -77.03565]  # Altura Parque Cervantes
]

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    .wsp-btn { display: block; width: 100%; padding: 15px; background-color: #25D366; color: white; text-align: center; border-radius: 10px; text-decoration: none; font-weight: bold; font-size: 20px; }
    .call-btn { display: block; width: 100%; padding: 12px; background-color: #007bff; color: white; text-align: center; border-radius: 10px; text-decoration: none; margin-bottom: 10px; font-weight: bold; }
    .sos-blink { background-color: #ff0000; color: white; padding: 30px; text-align: center; border-radius: 15px; font-weight: bold; font-size: 30px; animation: blinker 0.8s linear infinite; }
    @keyframes blinker { 50% { opacity: 0.2; } }
    </style>
""", unsafe_allow_html=True)

# --- NAVEGACIÓN ---
opcion = st.sidebar.radio("CENTRO DE MANDO", ["MAPA TÁCTICO", "MANUAL SOP", "COMMS", "SOS", "BITÁCORA"])

if opcion == "MAPA TÁCTICO":
    st.title("📍 MAPA TÁCTICO OPERATIVO")
    m = folium.Map(location=[-12.084, -77.034], zoom_start=15)
    
    # Rutas
    folium.PolyLine([[-12.092, -77.033], [-12.071, -77.035]], color="blue", weight=5, tooltip="Ruta Peatonal").add_to(m)
    folium.PolyLine([[-12.092, -77.031], [-12.071, -77.033]], color="black", weight=3, dash_array='5, 10', tooltip="Unidad Sombra").add_to(m)

    # Marcadores
    for s in DATA["salud"]: folium.Marker([s["lat"], s["lon"]], popup=s["name"], icon=folium.Icon(color=s["color"], icon="plus")).add_to(m)
    for t in DATA["tambos"]: folium.Marker([t["lat"], t["lon"]], popup=t["name"], icon=folium.Icon(color="green", icon="shopping-cart")).add_to(m)
    for e in DATA["extraccion"]: folium.Marker([e["lat"], e["lon"]], popup=e["name"], icon=folium.Icon(color="darkred", icon="warning-sign")).add_to(m)

    folium_static(m, width=1000)
    st.markdown("🔵 **Azul**: Ruta Marcha | 🏁 **Punteada**: Ruta Sombra | 🏥 **Rojo**: Salud | 🛒 **Verde**: Tambos")

elif opcion == "MANUAL SOP":
    st.title("📜 MANUAL DE PROCEDIMIENTOS EXPANDIDO")
    
    st.markdown('<div class="sop-header">1. VIGILANCIA: MIRADA A LA MULTITUD</div>', unsafe_allow_html=True)
    st.write("""
    - **Sectores de Responsabilidad:** No mire al VIP. Su sector es el público. Divida su visión en sectores: S-2 Izquierda, S-3 Derecha.
    - **Detección Temprana:** Identifique manos ocultas, ropa inusual para el clima (27°C) o trayectorias de interceptación.
    - **Barrido Visual:** Use visión periférica para movimiento y focal para identificar objetos sospechosos.
    """)
    

    st.markdown('<div class="sop-header">2. DISPONIBILIDAD: MANOS SIEMPRE LIBRES</div>', unsafe_allow_html=True)
    st.write("""
    - **Guardia Pasiva:** Manos entrelazadas al frente o sueltas sobre la cintura. Nunca en bolsillos o cruzadas.
    - **Prohibición de Cargas:** No cargue maletas, paraguas ni celulares. El móvil solo se usa para reportes rápidos o SOP.
    - **Gestión de Ciclistas:** Use las manos libres para hacer señales preventivas y apartar obstáculos suavemente.
    """)

    st.markdown('<div class="sop-header">3. FORMACIÓN: CÁPSULA EN DIAMANTE</div>', unsafe_allow_html=True)
    st.write("""
    - **S-1 (Puntero):** Rompehielos. Avisa sobre obstáculos y abre el flujo.
    - **Flancos (S-2/S-3):** Muros laterales. Mantienen el espacio vital del VIP.
    - **S-4 (Retaguardia):** Vigilancia 180° hacia atrás. Evita seguimientos.
    - **Líder (PM):** Responsable de la integridad física directa del VIP (Fuerza de cobertura).
    """)

elif opcion == "COMMS":
    st.title("📲 COMUNICACIONES")
    st.markdown(f'<a class="wsp-btn" href="{LINK_GRUPO}">📢 WHATSAPP DEL GRUPO</a>', unsafe_allow_html=True)
    st.markdown(f'<a class="call-btn" href="tel:{NUM_SOMBRA}">📞 LLAMAR A SOMBRA</a>', unsafe_allow_html=True)
    st.divider()
    st.subheader("REPORTE RÁPIDO")
    loc = st.selectbox("Lugar", ["J. Prado", "Risso", "Canevaro", "Llegada"])
    stat = st.selectbox("Estado", ["🟢 Despejado", "🟡 Sospechoso", "🔴 Emergencia"])
    st.code(f"REPORTE {datetime.now().strftime('%H:%M')} | {loc} | {stat}")

elif opcion == "SOS":
    st.markdown('<div class="sos-blink">CÓDIGO ROJO<br>EXTRACCIÓN</div>', unsafe_allow_html=True)
    st.write("Levante el móvil. Pantalla hacia Petit Thouars, llame al vehiculo sombra y dirijase al este")

elif opcion == "BITÁCORA":
    st.title("📝 REGISTRO")
    if 'log' not in st.session_state: st.session_state.log = []
    txt = st.text_input("Novedad:")
    if st.button("Guardar"): st.session_state.log.append(f"{datetime.now().strftime('%H:%M')} - {txt}")

    for i in reversed(st.session_state.log): st.write(i)

