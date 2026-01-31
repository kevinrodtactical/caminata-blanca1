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

# --- DATA TÁCTICA PARA EL MAPA ---
DATA = {
    "tambos": [
        {"name": "Tambo Arequipa-C19", "lat": -12.083672, "lon": -77.034785},
        {"name": "Tambo Arequipa-C25", "lat": -12.089616, "lon": -77.033552},
        {"name": "Tambo Risso", "lat": -12.086314, "lon": -77.035504}
    ],
    "salud": [
        {"name": "Clínica Javier Prado (Emergencias)", "lat": -12.091302, "lon": -77.028373, "color": "red"},
        {"name": "Hospital Rebagliati", "lat": -12.077935, "lon": -77.040427, "color": "orange"}
    ],
    "extraccion": [
        {"name": "EXTRACCIÓN A (J. Prado)", "lat": -12.091, "lon": -77.033},
        {"name": "EXTRACCIÓN B (Risso)", "lat": -12.086, "lon": -77.034},
        {"name": "EXTRACCIÓN C (Canevaro)", "lat": -12.079, "lon": -77.035}
    ]
}

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
    st.title("📜 MANUAL DE PROCEDIMIENTOS")
    with st.expander("🛡️ DISCIPLINA TÁCTICA", expanded=True):
        st.write("1. Mirada a la multitud, no a la marcha.\n2. Manos siempre libres.\n3. Mantener cápsula en Diamante.")
    with st.expander("🚨 PROTOCOLO DE EXTRACCIÓN"):
        st.error("CÓDIGO ROJO: El PM asegura al VIP. Flancos cubren. Retirada inmediata a la transversal roja hacia Petit Thouars.")
    

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
    st.write("Levante el móvil. Pantalla hacia Petit Thouars.")

elif opcion == "BITÁCORA":
    st.title("📝 REGISTRO")
    if 'log' not in st.session_state: st.session_state.log = []
    txt = st.text_input("Novedad:")
    if st.button("Guardar"): st.session_state.log.append(f"{datetime.now().strftime('%H:%M')} - {txt}")
    for i in reversed(st.session_state.log): st.write(i)