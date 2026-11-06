import streamlit as st
import puente   
from datos import DETALLES
from servicios import edad_de
from componentes import tarjeta_paciente, linea_tiempo, tabla_signos, grafica_signos
from historiales import obtener_historial, registrar_signos, pacientes_conocidos

@st.dialog("Registrar signos vitales")
def dialogo_signos(doc):
    c1, c2 = st.columns(2)
    fc = c1.number_input("Frecuencia cardiaca (lpm)", min_value=20, max_value=250,
                         value=80, key=f"d_fc_{doc}")
    fr = c2.number_input("Frecuencia respiratoria (rpm)", min_value=5, max_value=60,
                         value=16, key=f"d_fr_{doc}")
    c3, c4 = st.columns(2)
    sis = c3.number_input("Presión sistólica (mmHg)", min_value=50, max_value=250,
                          value=120, key=f"d_sis_{doc}")
    dia = c4.number_input("Presión diastólica (mmHg)", min_value=30, max_value=150,
                          value=80, key=f"d_dia_{doc}")
    c5, c6 = st.columns(2)
    temp = c5.number_input("Temperatura (°C)", min_value=30.0, max_value=45.0,
                           value=36.5, step=0.1, format="%.1f", key=f"d_temp_{doc}")
    spo2 = c6.number_input("Saturación O2 (%)", min_value=50, max_value=100,
                           value=97, key=f"d_spo2_{doc}")
 
    if st.button("Guardar", type="primary", use_container_width=True,
                 key=f"d_guardar_{doc}"):
        if sis <= dia:
            st.error("La presión sistólica debe ser mayor que la diastólica.")
        else:
            registrar_signos(doc, int(fc), f"{int(sis)}/{int(dia)}",
                             int(fr), float(temp), int(spo2))
            st.session_state["mensaje_historial"] = "Signos vitales registrados."
            st.rerun()
 
 
def mostrar():
    conocidos = pacientes_conocidos()
    if not conocidos:
        st.info("Todavía no hay pacientes registrados.")
        return
 
    mensaje = st.session_state.pop("mensaje_historial", None)
    if mensaje:
        st.success(mensaje)
 
    # Elegir paciente
    docs = [p["doc"] for p in conocidos]
    por_doc = {p["doc"]: p for p in conocidos}
 
    en_atencion = puente.en_atencion(st.session_state["sistema"])
    inicial = en_atencion["doc"] if en_atencion and en_atencion["doc"] in docs else docs[0]
    guardado = st.session_state.get("hist_doc")
    if guardado not in docs:
        guardado = inicial
 
    doc = st.selectbox(
        "Paciente",
        docs,
        index=docs.index(guardado),
        format_func=lambda d: f"{por_doc[d]['nombre']} ({d}) - {por_doc[d]['estado']}",
    )
    st.session_state["hist_doc"] = doc
 
    p = por_doc[doc]
    datos = {**DETALLES.get(doc, {}), **p}
    historial = obtener_historial(doc)
    signos = sorted(historial["signos"], key=lambda r: r["fecha"])
 
    #Cabecera del paciente
    with st.container(border=True):
        st.markdown(
            tarjeta_paciente(p["nombre"], doc, edad_de(datos),
                             datos.get("sexo", "Sin registro")),
            unsafe_allow_html=True,
        )
 
    #Pestañas
    t_res, t_sig, t_con = st.tabs(["Resumen", "Signos vitales", "Consultas"])
 
    with t_res:
        c_izq, c_der = st.columns([1, 1.5], gap="large")
 
        with c_izq:
            with st.container(border=True):
                st.markdown("#### Línea de tiempo")
                if historial["eventos"]:
                    st.markdown(linea_tiempo(historial["eventos"]),
                                unsafe_allow_html=True)
                else:
                    st.caption("Sin eventos registrados.")
 
        with c_der:
            with st.container(border=True):
                c_tit, c_btn = st.columns([2, 1], vertical_alignment="center")
                c_tit.markdown("#### Últimos signos vitales")
                if c_btn.button("Registrar nuevos", use_container_width=True,
                                key=f"btn_signos_{doc}"):
                    dialogo_signos(doc)
                st.markdown(tabla_signos(signos[-5:]), unsafe_allow_html=True)
 
            with st.container(border=True):
                st.markdown("#### Evolución de signos vitales")
                if len(signos) >= 2:
                    st.plotly_chart(grafica_signos(signos),
                                    use_container_width=True,
                                    config={"displayModeBar": False})
                else:
                    st.caption("Se necesitan al menos 2 registros para mostrar la evolución.")
 
    with t_sig:
        with st.container(border=True):
            st.markdown("#### Todos los registros de signos vitales")
            st.markdown(tabla_signos(signos), unsafe_allow_html=True)
 
    with t_con:
        with st.container(border=True):
            st.markdown("#### Consultas")
            st.write(f"**Motivo de consulta:** {datos.get('motivo', 'Sin registro')}")
            cambios = datos.get("reclasificaciones", [])
            if cambios:
                st.markdown("**Reclasificaciones**")
                for c in cambios:
                    st.write(f"- {c['hora']}: de Nivel {c['de']} a Nivel {c['a']}. "
                             f"Justificación: {c['justificacion']}")
            else:
                st.caption("Sin reclasificaciones.")