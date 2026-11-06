import streamlit as st
import puente
from datos import iniciar_datos
from estilos import aplicar_estilos
from layout import mostrar_header, mostrar_menu
from pantallas import tablero, ingreso, sala_espera, atencion
from historiales import iniciar_historiales


st.set_page_config(
    page_title="SANIQ",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

iniciar_datos()
puente.refrescar(st.session_state["sistema"])
iniciar_historiales()
aplicar_estilos()
mostrar_header()
pagina = mostrar_menu()

#Enrutador
if pagina == "Tablero":
    tablero.mostrar()
elif pagina == "Ingreso y triage":
    ingreso.mostrar()
elif pagina == "Sala de espera":
    sala_espera.mostrar()
elif pagina == "Atención":
    atencion.mostrar()
elif pagina == "Historial":
    from pantallas import historial
    historial.mostrar()

