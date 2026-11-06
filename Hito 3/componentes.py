#Gráficos
import plotly.graph_objects as go
from estilos import NIVELES, FONDO, AZUL_OSCURO, AZUL_SIDEBAR
from html import escape
from plotly.subplots import make_subplots

def minify(fn):
    def wrapper(*args, **kwargs):
        return " ".join(linea.strip() for linea in fn(*args, **kwargs).splitlines())
    return wrapper

#Tarjeta de niveles de triage
@minify
def tarjeta_nivel(nivel, cantidad):
    n = NIVELES[nivel]
    return f"""
    <div style="background:{n['bg']}; border:1.5px solid {n['color']};
                border-radius:10px; padding:12px; text-align:center;">
        <div style="display:flex; align-items:center; justify-content:center;
                    gap:8px; color:{n['color']}; font-weight:700; font-size:16px;">
                <span style="background:{n['color']}; color:white; border-radius:50%;
                            width:24px; height:24px; display:inline-flex; align-items:center; justify-content:center;">!</span>
                Nivel {nivel}
        </div>
        <div style="font-size:30px; font-weight:700; margin:6px 0;">{cantidad}</div>
        <span style="background:{n['color']}33; color:{n['color']}; font-size:11px; font-weight:600; padding:2px 10px; border-radius:10px;">
            {n['nombre']}
        </span>
    </div>
    """

#Etiqueta de color
@minify
def badge(texto, nivel):
    n = NIVELES[nivel]
    return (
        f"<span style='background:{n['bg']}; color:{n['color']}; "
        f"font-size:12px; font-weight:600; padding:2px 14px; "
        f"border-radius:10px;'>{texto}</span>"
    )

#Tabla de sala de espera
@minify
def tabla_espera(lista_pacientes):
    filas = ""
    for p in lista_pacientes:
        filas += f"""
        <tr style="border-bottom:1px solid #d5dde5;">
            <td style="padding:14px 12px;">{p['nombre']}</td>
            <td>{p['doc']}</td>
            <td style="text-align:center;">{badge(p['nivel'], p['nivel'])}</td>
            <td style="text-align:center;">{p['espera']}min</td>
            <td style="text-align:center;">{badge('En espera', p['nivel'])}</td>
        </tr>"""
    return f"""
    <div class="card" style="margin-top:16px;">
        <h3 style="margin:0 0 12px 0;">Sala de espera</h3>
        <table style="width:100%; border-collapse:collapse; font-size:14px;">
            <thead>
                <tr style="background:{FONDO}; text-align:left;">
                    <th style="padding:14px 12px;">Paciente</th>
                    <th>Documento</th>
                    <th style="text-align:center;">Nivel</th>
                    <th style="text-align:center;">Tiempo de espera</th>
                    <th style="text-align:center;">Estado</th>
                </tr>
            </thead>
            <tbody>{filas}</tbody>
        </table>
    </div>
    """

#Dona de las camillas
def dona_camillas(ocupadas, total):
    fig = go.Figure(go.Pie(
        values=[ocupadas, total - ocupadas],
        hole=0.72,
        sort=False,
        textinfo="none",
        hoverinfo="skip",
        marker=dict(colors=[AZUL_SIDEBAR, "#9DB4C5"]),
    ))
    fig.update_layout(
        showlegend=False,
        height=170,
        margin=dict(l=0, r=0, t=0, b=0 ),
        paper_bgcolor="rgba(0,0,0,0)",
        annotations=[dict(
            text=f"<b>{ocupadas} de {total}</b><br><span style='font-size:11px'>ocupadas</span>",
            showarrow=False,
            font=dict(size=16, color=AZUL_OSCURO),
    )],
    )
    return fig

#Actividad reciente
@minify
def lista_actividad(items):
    html = ""
    for color,titulo, detalle, hora in items:
        html += f"""
        <div style="display:flex; gap:10px; padding:10px 0;
                    border-bottom:1px solid #e0e6ec;">
            <span style="background:{color}; width:12px; height:12px; 
                        border-radius:50%; margin-top:4px; flex-shrink:0;"></span>
            <div style="flex:1; font-size:12px;">
                <div style="font-weight:500;">{titulo}</div>
                <div style="font-size:10px; color:#7a93a5;">{detalle}</div>
            </div>
            <span style="font-size:10px; color:#7a93a5;">{hora}</span>
        </div>"""
    return f"""
    <div class="card" style="margin-top:16px;">
        <h4 style="text-align:center; margin:0 0 8px 0;">Actividad reciente</h4>
        {html}
    </div>
    """

# Tarjeta de resultado sugerido del triage
@minify
def tarjeta_resultado(nivel, razon, tiempo):
    n = NIVELES[nivel]
    return f"""
    <div style="background:{n['bg']}; border:1px solid {n['color']}; border-radius:10px;
                padding:16px 20px; margin-top:16px; display:flex;
                align-items:center; gap:16px;">
        <span style="background:{n['color']}; color:white; border-radius:50%;
                     width:44px; height:44px; display:inline-flex; align-items:center;
                     justify-content:center; font-size:24px; font-weight:700;
                     flex-shrink:0;">!</span>
        <div style="flex:1;">
            <div style="font-size:12px; font-weight:600;">Resultado sugerido</div>
            <div style="font-size:22px; font-weight:700; color:{n['color']};">
                Nivel {nivel} - {n['nombre']}
            </div>
            <div style="font-size:11px; color:#5b7a90;">Motivo: {razon}</div>
        </div>
        <div style="flex:1; font-size:12px; color:#5b7a90;">{tiempo}</div>
    </div>
    """
#Tarjeta del total de pacientes en espera
@minify
def tarjeta_total(total):
    return f"""
     <div style="background:white; border:1.5px solid {AZUL_OSCURO}; border-radius:10px;
                padding:12px; text-align:center;">
        <div style="display:flex; align-items:center; justify-content:center;
                    min-height:24px; font-size:16px; font-weight:700;
                    color:{AZUL_OSCURO};">Total en espera</div>
        <div style="font-size:30px; font-weight:700; margin:6px 0;">{total}</div>
        <span style="font-size:11px; font-weight:600; color:#5b7a90;">Pacientes</span>
    </div>
    """

# Avatar, nombre, documento, edad y sexo
@minify
def tarjeta_paciente(nombre, doc, edad, sexo):
    iniciales = "".join(w[0] for w in nombre.split()[:2]).upper()
    edad_txt = f"{edad} años" if edad is not None else "Edad sin registro"
    return f"""
    <div style="display:flex; align-items:center; gap:18px;">
        <div style="width:72px; height:72px; border-radius:50%; background:#CFE0EC;
                    color:{AZUL_SIDEBAR}; display:flex; align-items:center;
                    justify-content:center; font-size:26px; font-weight:700;
                    flex-shrink:0;">{escape(iniciales)}</div>
        <div>
            <div style="font-size:26px; font-weight:700; color:{AZUL_OSCURO};">
                {escape(nombre)}</div>
            <div style="font-size:13px; color:#5b7a90;">
                {escape(doc)} &nbsp;·&nbsp; {edad_txt} &nbsp;·&nbsp; {escape(sexo)}</div>
        </div>
    </div>
    """


# Franja azul con el motivo de consulta
@minify
def bloque_motivo(motivo):
    return f"""
    <div style="background:#CFE0EC; border-radius:8px; padding:12px 16px;
                margin-top:16px; font-weight:700; color:{AZUL_OSCURO};">
        Motivo de consulta</div>
    <div style="padding:12px 16px; color:#5b7a90; font-size:15px;">
        {escape(motivo)}</div>
    """


# Cuadro signos vitales
@minify
def signos_vitales(signos):
    items = [
        ("FC", "Frecuencia cardiaca", "fc", "lpm"),
        ("PA", "Presión arterial", "pa", "mmHg"),
        ("FR", "Frecuencia respiratoria", "fr", "rpm"),
        ("T", "Temperatura", "temp", "°C"),
        ("O2", "Saturación O2", "spo2", "%"),
    ]
    celdas = ""
    for sigla, etiqueta, clave, unidad in items:
        valor = signos.get(clave) if signos else None
        texto = f"{valor} {unidad}" if valor is not None else "Sin registro"
        celdas += f"""
        <div style="display:flex; align-items:center; gap:12px;">
            <div style="width:42px; height:42px; border-radius:50%; background:#DCE9F3;
                        color:{AZUL_SIDEBAR}; display:flex; align-items:center;
                        justify-content:center; font-size:12px; font-weight:700;
                        flex-shrink:0;">{sigla}</div>
            <div>
                <div style="font-size:11px; color:#7a93a5;">{etiqueta}</div>
                <div style="font-size:16px; font-weight:600;">{texto}</div>
            </div>
        </div>"""
    return f"""
    <div style="border:1px solid #d5dde5; border-radius:10px; padding:16px 18px;
                margin-top:8px;">
        <div style="font-weight:700; margin-bottom:14px;">Signos vitales
            <span style="font-weight:400; color:#7a93a5;">(último registro)</span></div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
            {celdas}</div>
    </div>
    """
# Nivel del paciente y minutos de espera
@minify
def cabecera_nivel(nivel, espera):
    n = NIVELES[nivel]
    return f"""
    <div style="display:flex; align-items:center; gap:12px;">
        <div style="flex:1; background:{n['bg']}; border-radius:10px;
                    padding:12px 16px; display:flex; align-items:center; gap:12px;">
            <span style="background:{n['color']}; color:white; border-radius:50%;
                         width:40px; height:40px; display:inline-flex;
                         align-items:center; justify-content:center;
                         font-size:22px; font-weight:700; flex-shrink:0;">!</span>
            <span style="font-size:20px; font-weight:700; color:{n['color']};">
                Nivel {nivel} - {n['nombre']}</span>
        </div>
        <div style="border:1px solid #d5dde5; border-radius:10px;
                    padding:10px 16px; text-align:center;">
            <div style="font-size:20px; font-weight:700;">{espera} min</div>
            <div style="font-size:12px; color:#7a93a5;">en espera</div>
        </div>
    </div>
    """


# Observaciones, alergias y antecedentes
@minify
def info_adicional(observaciones, alergias, antecedentes):
    filas = [("Observaciones", observaciones),
             ("Alergias", alergias),
             ("Antecedentes", antecedentes)]
    html = ""
    for i, (titulo, valor) in enumerate(filas):
        borde = "border-top:1px solid #d5dde5;" if i else ""
        html += f"""
        <div style="display:flex; gap:16px; padding:14px 0; {borde}">
            <div style="width:110px; font-weight:700; flex-shrink:0;">{titulo}</div>
            <div style="color:#5b7a90; font-size:14px;">{escape(valor)}</div>
        </div>"""
    return f"""
    <div style="font-size:20px; font-weight:700; margin:6px 0 4px 0;">
        Información adicional</div>
    {html}
    """

#Pantalla de historial

def _fecha(dt):
    return dt.strftime("%d/%m/%Y - %H:%M")

#Linea de tiempo 
@minify
def linea_tiempo(eventos):
    ordenados = sorted(eventos, key=lambda e: e["fecha"])
    html = ""
    for i, ev in enumerate(ordenados):
        if ev.get("nivel"):
            n = NIVELES[ev["nivel"]]
            texto_badge = f"Nivel {ev['nivel']} - {n['nombre']}"
            fondo, color = n["bg"], n["color"]
        elif ev.get("etiqueta"):
            texto_badge = ev["etiqueta"]
            fondo, color = "#C9EEEB", "#0E8F89"
        else:
            texto_badge = ""  
 
        badge = ""
        if texto_badge:
            badge = (f"<span style='background:{fondo}; color:{color}; font-size:11px; "
                     f"font-weight:600; padding:2px 10px; border-radius:10px; "
                     f"white-space:nowrap; height:fit-content;'>{escape(texto_badge)}</span>")
 
        detalle = ""
        if ev.get("detalle"):
            detalle = (f"<div style='font-size:12px; color:#7a93a5;'>"
                       f"{escape(ev['detalle'])}</div>")
 
        linea = "#14B0A8" if i < len(ordenados) - 1 else "transparent"
        html += f"""
        <div style="position:relative; padding:0 0 24px 26px; margin-left:8px;
                    border-left:2px solid {linea};">
            <span style="position:absolute; left:-9px; top:1px; width:16px; height:16px;
                         border-radius:50%; background:#14B0A8;"></span>
            <div style="display:flex; justify-content:space-between; gap:10px;">
                <div>
                    <div style="font-weight:700; font-size:13px;">{_fecha(ev['fecha'])}</div>
                    <div style="font-size:13px; color:#5b7a90;">{escape(ev['titulo'])}</div>
                    {detalle}
                </div>
                {badge}
            </div>
        </div>"""
    return f"<div style='padding-top:6px;'>{html}</div>"     

# Tabla de registros de signos vitales
@minify
def tabla_signos(registros):
    if not registros:
        return "<div style='color:#7a93a5; padding:12px 0;'>Sin registros de signos vitales.</div>"
 
    filas = ""
    for r in sorted(registros, key=lambda r: r["fecha"]):
        filas += f"""
        <tr style="border-bottom:1px solid #e0e6ec;">
            <td style="padding:12px 8px;">{_fecha(r['fecha'])}</td>
            <td style="text-align:center;">{r['fc']}</td>
            <td style="text-align:center;">{escape(str(r['pa']))}</td>
            <td style="text-align:center;">{r['fr']}</td>
            <td style="text-align:center;">{r['temp']}</td>
            <td style="text-align:center;">{r['spo2']}</td>
        </tr>"""
    return f"""
    <table style="width:100%; border-collapse:collapse; font-size:13px;">
        <thead>
            <tr style="background:{FONDO}; text-align:center;">
                <th style="padding:12px 8px; text-align:left;">Fecha y hora</th>
                <th>FC (lpm)</th><th>PA (mmHg)</th><th>FR (rpm)</th>
                <th>T° (°C)</th><th>SpO2 (%)</th>
            </tr>
        </thead>
        <tbody>{filas}</tbody>
    </table>
    """
 
 
# Gráfico de evolución: FC y PA a la izquierda, temperatura a la derecha
def grafica_signos(registros):
    regs = sorted(registros, key=lambda r: r["fecha"])
    mismo_dia = len({r["fecha"].date() for r in regs}) == 1
    formato = "%H:%M" if mismo_dia else "%d/%m %H:%M"
    etiquetas = [r["fecha"].strftime(formato) for r in regs]
 
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(
        x=etiquetas, y=[r["fc"] for r in regs], name="FC (lpm)",
        mode="lines+markers", line=dict(color="#14B0A8", width=3)),
        secondary_y=False)
    fig.add_trace(go.Scatter(
        x=etiquetas, y=[int(str(r["pa"]).split("/")[0]) for r in regs],
        name="PA sistólica (mmHg)", mode="lines+markers",
        line=dict(color="#F5B700", width=3)),
        secondary_y=False)
    fig.add_trace(go.Scatter(
        x=etiquetas, y=[r["temp"] for r in regs], name="T (°C)",
        mode="lines+markers", line=dict(color="#3B82F6", width=3)),
        secondary_y=True)
 
    fig.update_layout(
        height=270,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", y=1.18),
        font=dict(color=AZUL_OSCURO),
    )
    fig.update_xaxes(type="category")
    fig.update_yaxes(title_text="lpm / mmHg", secondary_y=False, gridcolor="#e0e6ec")
    fig.update_yaxes(title_text="°C", secondary_y=True, showgrid=False)
    return fig
