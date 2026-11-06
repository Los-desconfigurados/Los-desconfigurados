#Pantalla 1
import streamlit as st
from estilos import NIVELES
from componentes import (tarjeta_nivel, tabla_espera, dona_camillas, lista_actividad)
import puente


def mostrar():
    sistema = st.session_state["sistema"]
    pacientes = puente.en_espera(sistema)
    actividad = st.session_state["actividad"]

    conteo_niveles = puente.conteo_por_nivel(sistema)
    fuera_de_tiempo = puente.vencidos(sistema)
    ocupadas, total_camillas = puente.camillas(sistema)

    col_main, col_side = st.columns([3, 1.1], gap="large")

    # Columna izquierda
    with col_main:
        st.markdown(
            "<h2 style='margin-bottom:0'>Tablero de Urgencias</h2>"
            "<p style='color:#5b7a90; margin-top:0'>Estado actual del servicio </p>",
            unsafe_allow_html=True
        )

        cols = st.columns(5)
        for col, (nivel, cant) in zip(cols, conteo_niveles.items()):
            col.markdown(tarjeta_nivel(nivel, cant), unsafe_allow_html=True)

        # Alerta roja
        if fuera_de_tiempo > 0:
            texto = ("1 paciente ha excedido" if fuera_de_tiempo == 1
                     else f"{fuera_de_tiempo} pacientes han excedido")
            st.markdown(f"""
            <div style="background:#F8D7DA; border:1px solid #E53935; border-radius:8px;
                        padding:10px 16px; margin-top:16px; color:#E53935;
                        font-weight:600; font-size:14px;">
                {texto} el tiempo de espera recomendado.
                Por favor, priorice su atención.
            </div>
            """, unsafe_allow_html=True)

        # Tabla (fuera del if)
        st.markdown(tabla_espera(pacientes), unsafe_allow_html=True)

    # Columna derecha (fuera de col_main)
    with col_side:
        # Camillas
        with st.container(border=True):
            st.markdown("<h2 style='margin:0;'>Camillas</h2>", unsafe_allow_html=True)
            st.plotly_chart(
                dona_camillas(ocupadas, total_camillas),
                use_container_width=True,
                config={"displayModeBar": False},
            )
            st.caption(
                f"🔵 Ocupadas: {ocupadas}  ·  ⚪ Disponibles: {total_camillas - ocupadas}"
                f"  ·  Total: {total_camillas}"
            )

        # Actividad reciente
        st.markdown(lista_actividad(actividad), unsafe_allow_html=True)

        # Botón
        st.write("")
        if st.button("Ver historial del día", use_container_width=True, type="primary"):
            st.toast("Aquí iremos al Historial")