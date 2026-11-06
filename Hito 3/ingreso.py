#Pantalla 2
import streamlit as st
from triage import calcular_nivel, TIEMPOS
from estilos import NIVELES
from datetime import date, datetime
from componentes import tarjeta_resultado
import puente
from servicios import edad_de
from historiales import registrar_evento



PREGUNTAS = [
    ("disnea", ":material/pulmonology:",
     "¿Presenta dificultad para respirar?",
     "Incluye sensación de falta de aire o respiración muy rápida."),
    ("fiebre", ":material/thermostat:",
     "¿Tiene fiebre mayor o igual a 38°C?",
     "O sensación de escalofríos intensos."),
    ("dolor", ":material/bolt:",
     "¿El dolor es muy intenso?",
     "En el pecho, abdomen, cabeza u otra zona."),
    ("conciencia", ":material/psychology:",
     "¿Presenta alteración del estado de conciencia?",
     "Confusión, somnolencia o desorientación."),
    ("sangrado", ":material/water_drop:",
     "¿Ha presentado sangrado activo o incontrolable?",
     "En cualquier parte del cuerpo."),
]

def mostrar():
    st.markdown(
         "<h2 style='margin-bottom:0'>Ingreso y triage</h2>"
        "<p style='color:#5b7a90; margin-top:0'>"
        "Registro de pacientes y cuestionario de clasificación.</p>",
        unsafe_allow_html=True,
    )

    if st.session_state.pop("limpiar_form", False):
        for clave in ["nombre", "tipo_doc", "num_doc", "fecha_nac", "motivo",
                      "q_disnea", "q_fiebre", "q_dolor", "q_conciencia", "q_sangrado"]:
            st.session_state.pop(clave, None)

    mensaje = st.session_state.pop("mensaje_ok", None)
    if mensaje:
        st.success(mensaje)

    col_izq, col_der = st.columns([1, 1.5], gap="large")

    with col_izq:
         with st.container(border=True):
            st.markdown("### :material/person: Datos del paciente")

            nombre = st.text_input(
                "Nombre Completo *",
                placeholder="Nombres y apellidos",
                key="nombre",
            )
            col_tipo, col_num = st.columns([1, 2])
            tipo_doc = col_tipo.selectbox(
                "Documento *",
                ["CC", "TI", "CE", "RC", "PA"],
                key="tipo_doc",
            )
            num_doc = col_num.text_input(
                "Número de documento",
                placeholder="Documento de identidad",
                label_visibility="hidden",
                key="num_doc",
            )
            fecha_nac = st.date_input(
                "Fecha de nacimiento *",
                value=None,
                min_value=date(1900, 1, 1),
                max_value=date.today(),
                format="DD/MM/YYYY",
                key="fecha_nac",
            )
            motivo = st.text_area(
                "Motico de consulta *",
                placeholder="Describe brevemente el motivo de consulta...",
                max_chars=500,
                height=120,
                key="motivo",
            )
            iniciar = st.button(
                "Iniciar valoración",
                type="primary",
                icon=":material/play_arrow:",
                use_container_width=True,
            )

            if iniciar:
                faltantes = []
                if not nombre.strip():
                    faltantes.append("Nombre completo")
                if not num_doc.strip():
                    faltantes.append("Documento")
                if fecha_nac is None:
                    faltantes.append("Fecha de nacimiento")
                if not motivo.strip():
                    faltantes.append("Motivo de consulta")

                if faltantes:
                    st.error("Completa los campos obligatorios: " + ", ".join(faltantes))
                else:
                    st.session_state["paciente_en_curso"] = {
                        "nombre": nombre.strip(),
                        "doc": f"{tipo_doc}{num_doc.strip()}",
                        "fecha_nac": fecha_nac,
                        "motivo": motivo.strip(),
                    }
                    st.success("Datos registrados. Completa el cuestionario de triage.")


    with col_der:
         with st.container(border=True):
            st.markdown("#### :material/description: Cuestionario de triage")
            respuestas = {}
            for i, (clave, icono, pregunta, ayuda) in enumerate(PREGUNTAS):
                c_texto, c_resp = st.columns([3, 1.3], vertical_alignment="center")

                c_texto.markdown(f"{icono} **{pregunta}**")
                c_texto.caption(ayuda)

                respuestas[clave] = c_resp.radio(
                    pregunta,
                    ["Sí", "No"],
                    index=1,
                    horizontal=True,
                    label_visibility="collapsed",
                    key=f"q_{clave}",
                )

                if i < len(PREGUNTAS) - 1:
                    st.divider()

    nivel, razon = calcular_nivel(respuestas)
    st.session_state["Nivel_sugerido"] = nivel

    st.markdown(
        tarjeta_resultado(nivel, razon, TIEMPOS[nivel]),
        unsafe_allow_html=True,

    )

    st.write("")
    confirmar = st.button(
        "Confirmar ingreso",
        type="primary",
        icon=":material/check:",
        use_container_width=True,
        key="confirmar",
    )

    if confirmar:
        if "paciente_en_curso" not in st.session_state:
            st.warning("Primero completa los datos del paciente y presiona 'Iniciar valoración'.")
        else:
            paciente = st.session_state.pop("paciente_en_curso")

            try:
                puente.ingresar(
                    st.session_state["sistema"],
                    paciente["nombre"], paciente["doc"],
                    edad_de({"fecha_nac": paciente["fecha_nac"]}),
                    paciente["motivo"], nivel,
                    extras={"fecha_nac": paciente["fecha_nac"]},
                )
            except ValueError:
                # se devuelve para no obligar a llenar los datos otra vez
                st.session_state["paciente_en_curso"] = paciente
                st.error("Ya existe un paciente activo con ese documento.")
            else:
                registrar_evento(paciente["doc"], "Ingreso a urgencias",
                                 paciente["motivo"], nivel)

                st.session_state["actividad"].insert(0, (
                    NIVELES[nivel]["color"],
                    f"Paciente ingresó a triage (Nivel {nivel})",
                    f"{paciente['nombre']} - {paciente['doc']}",
                    datetime.now().strftime("%H:%M"),
                ))

                st.session_state["mensaje_ok"] = (
                    f"{paciente['nombre']} ingresó como Nivel {nivel} - {NIVELES[nivel]['nombre']}."
                )
                st.session_state["limpiar_form"] = True
                st.rerun()