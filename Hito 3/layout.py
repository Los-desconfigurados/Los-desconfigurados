#Header superior y menú lateral

import streamlit as st

#Menú lateral
OPCIONES = ["Tablero", "Ingreso y triage", "Sala de espera", "Atención", "Historial"]

ICONOS = {
    "Tablero": ":material/home:",
    "Ingreso y triage": ":material/person:",
    "Sala de espera": ":material/monitoring:",
    "Atención": ":material/stethoscope:",
    "Historial": ":material/description:",
}
#Header superior
def mostrar_header():
   st.markdown("""
<div style="background-color:white; padding:14px 32px; margin:0 -2rem 1rem -2rem;
            display:flex; align-items:center; gap:16px;">
    <span style="font-size:28px; font-weight:700; letter-spacing:3px;">
        SAN<span style="color:#14B0A8;">IQ</span>
    </span>
    <span style="border-left:1px solid #ccc; padding-left:16px;
                 font-weight:600; font-size:18px;">
        Gestión de Urgencias
    </span>
</div>
""", unsafe_allow_html=True)

def ir_a(pagina, doc=None):
    """Cambia de pantalla desde cualquier botón (usar con on_click)."""
    st.session_state["pagina"] = pagina
    if doc is not None:
        st.session_state["hist_doc"] = doc

def mostrar_menu():
    with st.sidebar:
        st.write("")
        pagina = st.radio(
            "Navegación",
            OPCIONES,
            format_func=lambda opcion: f"{ICONOS[opcion]} {opcion}",
            label_visibility="collapsed",
            key="pagina",
        )
    return pagina

        