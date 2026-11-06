#Historial de cada paciente

from datetime import datetime, timedelta
import streamlit as st
import puente

#Historial de cada paciente

SIGNOS_EXTRA = {
    "CC1032456789": [
        (25, {"fc": 102, "pa": "110/70", "fr": 20, "temp": 37.8, "spo2": 96}),
        (40, {"fc": 96, "pa": "120/80", "fr": 18, "temp": 36.9, "spo2": 98}),
    ],
}
    
def iniciar_historiales():
    st.session_state.setdefault("historiales", {})


def obtener_historial(doc):
    return st.session_state["historiales"].setdefault(
        doc, {"eventos": [], "signos": []}
    )


def registrar_evento(doc, titulo, detalle="", nivel=None, etiqueta=None):
    obtener_historial(doc)["eventos"].append({
        "fecha": datetime.now(),
        "titulo": titulo,
        "detalle": detalle,
        "nivel": nivel,
        "etiqueta": etiqueta,
    })


def registrar_signos(doc, fc, pa, fr, temp, spo2):
    obtener_historial(doc)["signos"].append({
        "fecha": datetime.now(),
        "fc": fc, "pa": pa, "fr": fr, "temp": temp, "spo2": spo2,
    })
    registrar_evento(
        doc,
        "Registro de signos vitales",
        f"FC {fc} | PA {pa} | T {temp} °C | SpO2 {spo2} %",
    )
    # El back guarda fc, fr, temp y spo2 (la presión arterial solo queda aquí)
    puente.registrar_signos(st.session_state["sistema"], doc, fc, fr, temp, spo2)


def pacientes_conocidos():
    """Une pacientes en espera, en atención y dados de alta, sin repetir documentos."""
    sistema = st.session_state["sistema"]
    vistos = {}

    for p in puente.en_espera(sistema):
        vistos[p["doc"]] = {**p, "estado": "En espera"}

    atencion = puente.en_atencion(sistema)
    if atencion:
        vistos[atencion["doc"]] = {**atencion, "estado": "En atención"}

    for a in sistema.altas:
        if a["doc"] not in vistos:
            vistos[a["doc"]] = {
                **sistema.extras.get(a["doc"], {}),
                "nombre": a["nombre"],
                "doc": a["doc"],
                "nivel": a["nivel"],
                "motivo": a.get("motivo_consulta", "-"),
                "reclasificaciones": a.get("reclasificaciones", []),
                "estado": "Salida registrada",
            }
    return list(vistos.values())