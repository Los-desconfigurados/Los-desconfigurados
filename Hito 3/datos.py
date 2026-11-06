import streamlit as st
from puente import crear_sistema



# historial.py e historiales.py todavía importan DETALLES
DETALLES = {}


def iniciar_datos():
    if "sistema" not in st.session_state:
        st.session_state["sistema"] = crear_sistema()
    st.session_state.setdefault("actividad", [])