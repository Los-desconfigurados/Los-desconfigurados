import streamlit as st
from estilos import NIVELES
from servicios import (pasar_al_siguiente, deshacer, edad_de, abrir_alta, cerrar_alta, registrar_alta_actual, TIPOS_ALTA) 
from componentes import (tarjeta_paciente, bloque_motivo, signos_vitales, cabecera_nivel, info_adicional)
from historiales import obtener_historial
from layout import ir_a
import puente


def mostrar():
    sistema = st.session_state["sistema"]
    pacientes = puente.en_espera(sistema)
    actual = puente.en_atencion(sistema)
    mensaje = st.session_state.pop("mensaje_atencion", None)
    if mensaje:
        st.success(mensaje)

    c_sig, c_des = st.columns([2.2, 1])
    c_sig.button(
        "Pasar al siguiente paciente",
        type="primary",
        icon=":material/arrow_forward:",
        on_click=pasar_al_siguiente,
        disabled=(actual is not None or not pacientes),
        use_container_width=True,
        key="btn_siguiente",
    )
    c_des.button(
        "Deshacer",
        icon=":material/undo:",
        on_click=deshacer,
        disabled=not puente.hay_que_deshacer(sistema),
        use_container_width=True,
        key="btn_deshacer",
    )

    st.write("")

    if actual is None:
        with st.container(border=True):
            st.markdown("#### Sin paciente en atención")
            sig = puente.siguiente(sistema)
            if sig is None:
                st.caption("La sala de espera está vacía.")
            else:
                st.caption(
                    f"Siguiente en la cola: {sig['nombre']} - "
                    f"Nivel {sig['nivel']} - {NIVELES[sig['nivel']]['nombre']}, "
                    f"{sig['espera']} min de espera"
                )
        return

    col_izq, col_der = st.columns([1.5, 1], gap="large")
    historial_signos = obtener_historial(actual["doc"])["signos"]
    ultimos_signos = historial_signos[-1] if historial_signos else None

    with col_izq:
        with st.container(border=True):
            st.markdown(
                tarjeta_paciente(
                    actual["nombre"],
                    actual["doc"],
                    edad_de(actual),
                    actual.get("sexo", "Sin registro"),
                ),
                unsafe_allow_html=True,
            )
            st.markdown(
                bloque_motivo(actual.get("motivo", "Sin registro")),
                unsafe_allow_html=True,
            )
            st.markdown(
                signos_vitales(ultimos_signos),
                unsafe_allow_html=True,
            )

    with col_der:
        with st.container(border=True):
            st.markdown(
                cabecera_nivel(actual["nivel"], actual["espera"]),
                unsafe_allow_html=True,
            )


        with st.container(border=True):
            st.markdown("#### Acciones")

            if st.session_state.get("alta_abierta"):
                tipo = st.selectbox(
                    "Tipo",
                    list(TIPOS_ALTA.keys()),
                    key="atn_tipo",
                )
                motivo_alta = st.selectbox(
                    "Motivo",
                    TIPOS_ALTA[tipo],
                    key=f"atn_motivo_{tipo}",
                )
                c_can, c_reg = st.columns(2)
                c_can.button(
                    "Cancelar",
                    on_click=cerrar_alta,
                    use_container_width=True,
                    key="atn_cancelar_alta",
                )
                c_reg.button(
                    "Registrar",
                    type="primary",
                    on_click=registrar_alta_actual,
                    args=(tipo, motivo_alta),
                    use_container_width=True,
                    key="atn_registrar_alta",
                )
            else:
                c_alta, c_hist = st.columns(2)
                c_alta.button(
                    "Registrar alta",
                    type="primary",
                    on_click=abrir_alta,
                    use_container_width=True,
                    key="atn_abrir_alta",
                )
                c_hist.button(
                    "Ver historial",
                    on_click=ir_a,
                    args=("Historial", actual["doc"]),
                    use_container_width=True,
                    key="atn_historial",
                )

