#Lógica de atención

from datetime import datetime
import streamlit as st
from estilos import NIVELES
from datetime import date, datetime
import puente

ORDEN_NIVELES = list(NIVELES.keys())


def _s():
    return st.session_state["sistema"]

def _log(color, titulo, detalle):
    st.session_state["actividad"].insert(0, (color, titulo, detalle, datetime.now().strftime("%H:%M")))

def pasar_al_siguiente():
    p = puente.llamar_siguiente(_s())
    if p is None:
        return
    st.session_state["accion"] = None
    st.session_state["alta_abierta"] = False
    _log(NIVELES[p["nivel"]]["color"], "Paciente pasó a atención", f"{p['nombre']} - {p['doc']}")

def deshacer():
    msg = puente.deshacer(_s())
    if msg:
        st.session_state["accion"] = None
        st.session_state["alta_abierta"] = False
        _log("#14B0A8", msg, "")

def edad_de(p):
    if p.get("edad") is not None:
        return p["edad"]
    nacimiento = p.get("fecha_nac")
    if nacimiento is None:
        return None
    hoy = date.today()
    cumplio = (hoy.month, hoy.day) >= (nacimiento.month, nacimiento.day)
    return hoy.year - nacimiento.year - (0 if cumplio else 1)

TIPOS_ALTA = {
    "Alta": ["Mejora", "Tratamiento completado", "Remisión a consulta externa"],
    "Traslado": ["A otra institución", "A hospitalización", "A cuidados intensivos"],
    "Alta voluntaria": ["Solicitud del paciente", "Solicitud de familiares"],
    "Abandono": ["Se retiró sin ser atendido"],
}


def abrir_alta():
    st.session_state["alta_abierta"] = True


def cerrar_alta():
    st.session_state["alta_abierta"] = False


def registrar_alta_actual(tipo, motivo_alta):
    p = puente.en_atencion(_s())
    if p is None:
        return
    puente.dar_alta(_s(), p["doc"], tipo, motivo_alta)
    _log(NIVELES[p["nivel"]]["color"], f"Salida registrada: {tipo} ({motivo_alta})", f"{p['nombre']} - {p['doc']}")
    st.session_state["mensaje_atencion"] = f"{p['nombre']} salió de atención: {tipo} ({motivo_alta})."
    st.session_state["alta_abierta"] = False


