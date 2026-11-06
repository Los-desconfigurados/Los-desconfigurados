"""Puente entre el front (Streamlit) y el backend (nucleo/).
Las pantallas solo hablan con este archivo, No importa streamlit."""
from datetime import datetime
from nucleo.sistema import SistemaUrgencias
from nucleo.dominio import Nivel, SignosVitales


def crear_sistema():
    s = SistemaUrgencias(capacidad_camillas=10)
    s.extras = {}     # datos que el back no guarda (sexo, alergias, reclasificaciones...), por documento
    s.altas = []      # salidas registradas (para el Historial)
    s.efectos = []    # efectos del front
    return s


# conversiones 
def romano(nivel):
    return Nivel(int(nivel)).name


def a_dict(sistema, p):
    """Paciente del back -> dict que esperan las pantallas."""
    espera = int((datetime.now() - p.hora_llegada).total_seconds() // 60) if p.hora_llegada else 0
    return {
        "nombre": p.nombre, "doc": p.documento, "nivel": romano(p.nivel),
        "espera": max(espera, 0), "motivo": p.motivo, "edad": p.edad,
        **sistema.extras.get(p.documento, {}),
    }


# lecturas 
def refrescar(sistema):
    """Envejecimiento: sube de nivel a quien supero su tiempo objetivo."""
    sistema.cola_triage.envejecer()


def en_espera(sistema, nivel=None):
    return [a_dict(sistema, p) for p in sistema.en_espera(nivel)]


def en_atencion(sistema):
    p = sistema.paciente_en_atencion
    return a_dict(sistema, p) if p else None


def siguiente(sistema):
    lista = en_espera(sistema)
    return lista[0] if lista else None


def conteo_por_nivel(sistema):
    return {romano(k): v for k, v in sistema.cola_triage.contar_por_nivel().items()}


def vencidos(sistema):
    return sistema.metricas()["pacientes_vencidos"]


def camillas(sistema):
    """Camillas ocupadas = pacientes activos (en espera + en atencion).
    Se liberan solas al dar el alta. Total = capacidad del sistema."""
    total = sistema.camillas()[1]
    return min(len(sistema.registro), total), total   # (ocupadas, total)


def hay_que_deshacer(sistema):
    return len(sistema.gestor_deshacer) > 0


# acciones 
def ingresar(sistema, nombre, doc, edad, motivo, nivel_romano, extras=None):
    p = sistema.registrar_paciente(nombre, doc, edad, motivo, nivel=Nivel[nivel_romano])
    sistema.extras[p.documento] = {**(extras or {}), "reclasificaciones": []}
    sistema.efectos.append(lambda: sistema.extras.pop(p.documento, None))
    return p


def llamar_siguiente(sistema):
    if sistema.paciente_en_atencion is not None:
        return None
    p = sistema.llamar_siguiente()
    if p is not None:
        sistema.efectos.append(None)
    return a_dict(sistema, p) if p else None


def reclasificar(sistema, doc, nuevo_romano, justificacion, hora):
    p = sistema.registro.obtener(str(doc))
    if p is None:
        return False
    anterior = romano(p.nivel)
    if not sistema.reclasificar(doc, Nivel[nuevo_romano], justificacion):
        return False
    lista = sistema.extras.setdefault(doc, {}).setdefault("reclasificaciones", [])
    lista.append({"de": anterior, "a": nuevo_romano, "justificacion": justificacion, "hora": hora})
    sistema.efectos.append(lambda: lista.pop())
    return True


def dar_alta(sistema, doc, tipo, motivo_alta):
    p = sistema.dar_alta(doc, f"{tipo}: {motivo_alta}")
    reg = {
        "nombre": p.nombre, "doc": p.documento, "nivel": romano(p.nivel),
        "motivo_consulta": p.motivo, "tipo": tipo, "motivo_alta": motivo_alta,
        "hora": datetime.now().strftime("%H:%M"),
        "reclasificaciones": sistema.extras.get(doc, {}).get("reclasificaciones", []),
    }
    sistema.altas.append(reg)
    sistema.efectos.append(lambda: sistema.altas.pop())
    return reg


def deshacer(sistema):
    """Deshace la ultima accion (ingreso, llamado, reclasificacion o alta)."""
    msg = sistema.deshacer()
    if msg is None:
        return None
    efecto = sistema.efectos.pop() if sistema.efectos else None
    if efecto:
        efecto()
    return msg


def registrar_signos(sistema, doc, fc, fr, temp, spo2):
    """El back no guarda presion arterial; esa queda en historiales.py del front."""
    try:
        sistema.registrar_signos(doc, SignosVitales(temp, fc, fr, spo2))
    except KeyError:
        pass   # paciente ya con salida: solo queda en el historial del front