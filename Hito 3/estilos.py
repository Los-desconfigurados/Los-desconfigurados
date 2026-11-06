#Paleta de colores y CSS 

import streamlit as st

#Aqui se defina la paleta de colores
AZUL_OSCURO = "#0D3A56"
AZUL_SIDEBAR = "#1B5A7D"
FONDO = "#EAF1F8"

#Se define un diccionario 
NIVELES = {
    "I":   {"nombre": "Crítico",      "color": "#E53935", "bg": "#F8D7DA"},
    "II":  {"nombre": "Muy urgente",  "color": "#F57C00", "bg": "#FFE0C2"},
    "III": {"nombre": "Urgente",      "color": "#D9A400", "bg": "#FFF1C2"},
    "IV":  {"nombre": "Poco urgente", "color": "#14B0A8", "bg": "#C9EEEB"},
    "V":   {"nombre": "No urgente",   "color": "#3B82F6", "bg": "#D3E3FA"},
}

def aplicar_estilos():
    st.markdown(f""" 
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Montserrat' , sans-serif;
    color: {AZUL_OSCURO};
}}

.stApp {{ background-color: {FONDO}; }}
header[data-testid="stHeader"] {{ display : none;}}

[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapsedControl"] {{ display: none; }}

footer {{ visibility: hidden; }}

.block-container {{
   padding-top: 0rem;
   padding-left: 2rem;
   padding-right: 2rem;
   max-width: 100%;
}}

.card {{
   background: white;
   border-radius: 12px;
   padding: 20px 24px;
}}

div[data-testid="stVerticalBlockBorderWrapper"] {{
   background: white;
   border: none;
   border-radius: 12px;
}}

.stButton > button[kind="primary"] {{
    background-color: {AZUL_SIDEBAR};
    border: none;
    border-radius: 8px;
    padding: 14px;
    font-weight: 700;
    color: white;
}}

/* Estilos del menú lateral */
section[data-testid="stSidebar"] {{
    background-color: {AZUL_SIDEBAR};
}}
section[data-testid="stSidebar"] * {{
    color: white;
}}
section[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {{
    display: none;
}}
section[data-testid="stSidebar"] div[role="radiogroup"] label {{
    padding: 12px 16px;
    border-radius: 8px;
    width: 100%;
    cursor: pointer;
}}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {{
    background: white;
}}
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {{
    color: {AZUL_OSCURO} !important;
    font-weight: 600;
}}  

/* Tabla de sala de espera */
.st-key-cabecera {{
    background: #D6E6F2;
    border-radius: 8px;
    padding: 6px 12px;
}}
/* Botón Reclasificar */
[class*="st-key-rec_"] button {{
    background: white;
    border: 1.5px solid #14B0A8;
    border-radius: 6px;
    min-height: 0;
    padding: 2px 8px;
}}
[class*="st-key-rec_"] button p {{
    color: #14B0A8 !important;
    font-size: 12px;
    font-weight: 600;
}}

/* Botón Alta */
[class*="st-key-alta_"] button {{
    background: #CCE0F0;
    border: none;
    border-radius: 6px;
    min-height: 0;
    padding: 2px 8px;
}}
[class*="st-key-alta_"] button p {{
    color: {AZUL_OSCURO} !important;
    font-size: 12px;
    font-weight: 600;
}}
</style>

""", unsafe_allow_html=True)