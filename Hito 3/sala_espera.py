#3ra pantalla

import streamlit as st
from estilos import NIVELES
from componentes import tarjeta_nivel, tarjeta_total, badge
from datetime import datetime
from servicios import TIPOS_ALTA
import puente

#Filtro
OPCIONES_NIVEL = {"Todos": None}
for nivel, datos in NIVELES.items():
    OPCIONES_NIVEL[f"Nivel {nivel} - {datos['nombre']}"] = nivel

OPCIONES_NUEVO = {k: v for k, v in OPCIONES_NIVEL.items() if v is not None}


# Botón de Limpiar filtros 
def limpiar_filtros():
    st.session_state["buscar"] = ""
    st.session_state["filtro_nivel"] = "Todos"

ANCHOS = [0.4, 1.8, 1.7, 0.9, 2.0, 1.3, 1.4, 0.8]

def seleccionar(tipo, doc):
    st.session_state["accion"] = {"tipo": tipo, "doc": doc}

def encabezado():
    with st.container(key="cabecera"):
        cols = st.columns(ANCHOS, vertical_alignment="center")
        titulos = ["#", "Paciente", "Documento", "Nivel", "Motivo de consulta", "Estado", "Acciones", ""]

        for col, titulo in zip(cols, titulos):
            if titulo:
                col.markdown(f"**{titulo}**")


def fila(numero, idx, p):
    cols = st.columns(ANCHOS, vertical_alignment="center")
    cols[0].write(numero)
    cols[1].write(p["nombre"])
    cols[2].write(p["doc"])
    cols[3].markdown(badge(p["nivel"], p["nivel"]), unsafe_allow_html=True)
    cols[4].write(p.get("motivo", "-"))
    cols[5].markdown(badge("En espera", p["nivel"]), unsafe_allow_html=True)
    cols[6].button(
        "Reclasificar",
        key=f"rec_{p['doc']}",
        on_click=seleccionar,
        args=("reclasificar", p["doc"]),
        use_container_width=True,
    )   
    cols[7].button(
        "Alta",
        key=f"alta_{p['doc']}",
        on_click=seleccionar,
        args=("alta", p["doc"]),
        use_container_width=True,
    )
    st.markdown(
        "<hr style='margin:2px 0; border:none; border-top:1px solid #d5dde5;'>",
        unsafe_allow_html=True,
    )

def cancelar():
    st.session_state["accion"] = None


def panel_reclasificar(pacientes):
    accion = st.session_state.get("accion")

    with st.container(border=True):
        st.markdown("#### Reclasificar paciente")

        if (not accion or accion["tipo"] != "reclasificar"
                or accion["doc"] not in [p["doc"] for p in pacientes]):
            st.caption("Presiona 'Reclasificar' en la fila de un paciente para cambiar su nivel.")
            return

        p = next((paciente for paciente in pacientes if paciente["doc"] == accion["doc"]), None)
        etiquetas = list(OPCIONES_NUEVO.keys())
        actual = next((k for k, v in OPCIONES_NUEVO.items() if v == p["nivel"]),
              etiquetas[0])

        st.text_input(
            "Paciente",
            value=f"{p['nombre']} ({p['doc']})",
            disabled=True,
            key=f"panel_pac_{p['doc']}",
        )
        nuevo_label = st.selectbox(
            "Nuevo nivel de triage",
            etiquetas,
            index=etiquetas.index(actual),
            key=f"panel_nivel_{p['doc']}",
        )
        justificacion = st.text_area(
            "Justificación (obligatoria)",
            placeholder="Escriba la razón del cambio de nivel...",
            height=90,
            key=f"panel_just_{p['doc']}",
        )

        c_cancelar, c_confirmar = st.columns(2)
        c_cancelar.button(
            "Cancelar",
            on_click=cancelar,
            use_container_width=True,
            key="panel_cancelar",
        )
        confirmar = c_confirmar.button(
            "Reclasificar",
            type="primary",
            use_container_width=True,
            key="panel_confirmar",
        )

        if confirmar:
            nuevo = OPCIONES_NUEVO[nuevo_label]
            if nuevo == p["nivel"]:
                st.warning("Elige un nivel distinto al actual.")
            elif not justificacion.strip():
                st.error("La justificación es obligatoria.")
            else:
                anterior = p["nivel"]
                hora = datetime.now().strftime("%H:%M")

                puente.reclasificar(
                    st.session_state["sistema"],
                    p["doc"], nuevo, justificacion.strip(), hora,
                )
                st.session_state["actividad"].insert(0, (
                    NIVELES[nuevo]["color"],
                    f"Paciente reclasificado: Nivel {anterior} a Nivel {nuevo}",
                    f"{p['nombre']} - {p['doc']}",
                    hora,
                ))
                st.session_state["mensaje_sala"] = (
                    f"{p['nombre']} fue reclasificado de Nivel {anterior} a Nivel {nuevo}."
                )
                st.session_state["accion"] = None
                st.rerun()

def panel_alta(pacientes):
    accion = st.session_state.get("accion")

    with st.container(border=True):
         st.markdown("#### Registrar alta")

         if (not accion or accion["tipo"] != "alta"
                or accion["doc"] not in [p["doc"] for p in pacientes]):
            st.caption("Presiona 'Alta' en la fila de un paciente para registrar su salida.")
            return

         p = next((paciente for paciente in pacientes if paciente["doc"] == accion["doc"]), None)

         st.text_input(
            "Paciente",
            value=f"{p['nombre']} ({p['doc']})",
            disabled=True,
            key=f"panelalta_pac_{p['doc']}",
         )
         tipo = st.selectbox(
             "Tipo",
            list(TIPOS_ALTA.keys()),
            key=f"panelalta_tipo_{p['doc']}",
        )
         motivo_alta = st.selectbox(
            "Motivo",
            TIPOS_ALTA[tipo],
            key=f"panelalta_motivo_{p['doc']}_{tipo}",
        )

         c_cancelar, c_registrar = st.columns(2)
         c_cancelar.button(
            "Cancelar",
            on_click=cancelar,
            use_container_width=True,
            key="panelalta_cancelar",
        )
         registrar = c_registrar.button(
            "Registrar",
            type="primary",
            use_container_width=True,
            key="panelalta_registrar",
        )

         if registrar:
            hora = datetime.now().strftime("%H:%M")

            puente.dar_alta(
                st.session_state["sistema"],
                p["doc"], tipo, motivo_alta,
            )

            st.session_state["actividad"].insert(0, (
                NIVELES[p["nivel"]]["color"],
                f"Salida registrada: {tipo} ({motivo_alta})",
                f"{p['nombre']} - {p['doc']}",
                hora,
            ))
            st.session_state["mensaje_sala"] = (
                f"{p['nombre']} salió de la sala de espera: {tipo} ({motivo_alta})."
            )
            st.session_state["accion"] = None
            st.rerun()


def mostrar():
    pacientes = puente.en_espera(st.session_state["sistema"])

    conteo = {nivel: 0 for nivel in NIVELES}
    for p in pacientes:
        conteo[p["nivel"]] += 1


    mensaje = st.session_state.pop("mensaje_sala", None)
    if mensaje:
        st.success(mensaje)

    #Tarjetas resumen
    cols = st.columns(6)
    cols[0].markdown(tarjeta_total(len(pacientes)), unsafe_allow_html=True)
    for col, (nivel, cant) in zip(cols[1:], conteo.items()):
        col.markdown(tarjeta_nivel(nivel, cant), unsafe_allow_html=True)

    st.write("")

    #Panel lateral 
    col_main, col_side = st.columns([3, 1.1], gap="large")

    with col_main:
        with st.container(border=True):
            st.markdown("#### Pacientes en espera")

            #Buscador y filtros
            c_buscar, c_nivel, c_limpiar = st.columns([3, 1.8, 1.2],
                                                      vertical_alignment="bottom")
            texto = c_buscar.text_input(
                "Buscar",
                placeholder="Buscar por nombre, documento o ID...",
                label_visibility="collapsed",
                key="buscar",
            )
            filtro = c_nivel.selectbox(
                "Filtrar por nivel de triage",
                list(OPCIONES_NIVEL.keys()),
                key="filtro_nivel",
            )
            c_limpiar.button(
                "Limpiar filtros",
                on_click=limpiar_filtros,
                use_container_width=True,
            )

            
            texto_min = texto.strip().lower()
            nivel_elegido = OPCIONES_NIVEL[filtro]

            filtrados = []
            for idx, p in enumerate(pacientes):
                coincide_texto = (texto_min in p["nombre"].lower()
                                  or texto_min in p["doc"].lower())
                coincide_nivel = nivel_elegido is None or p["nivel"] == nivel_elegido
                if coincide_texto and coincide_nivel:
                    filtrados.append((idx, p))

            st.caption(f"Mostrando {len(filtrados)} de {len(pacientes)} pacientes")

            if not filtrados:
                st.info("No hay pacientes que coincidan con la búsqueda")

            else:
                encabezado()
                for n, (idx, p) in enumerate(filtrados, 1):
                    fila(n, idx, p) 


    with col_side:
        panel_reclasificar(pacientes)
        panel_alta(pacientes)
