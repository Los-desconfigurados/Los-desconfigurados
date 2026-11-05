import os
import platform
import sys
import time
from datetime import datetime
 
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)
 
from nucleo.simulacion import simular
from nucleo.sistema import SistemaUrgencias
 
N_ADMISIONES = 5000
SEMILLAS = (1, 2, 3, 4, 5)
LIMITE_SEGUNDOS = 2.0
DURACION_ATENCION = 1  # minutos simulados por paciente
 
 
class _ColaTriageCompatible:

 
    def __init__(self, cola_real):
        self._real = cola_real
        self._colas = {nivel: cola_real._colas[nivel] for nivel in range(1, 6)}
 
    def envejecer(self, ahora=None):
        return self._real.envejecer(ahora=ahora)
 
 
class _SistemaCompatible:
  
    def __init__(self, sistema):
        self._sistema = sistema
        self.cola_triage = _ColaTriageCompatible(sistema.cola_triage)
 
    def registrar_paciente(self, **datos):
        return self._sistema.registrar_paciente(**datos)
 
    def llamar_siguiente(self):
        return self._sistema.llamar_siguiente()
 
 
def correr_semilla(semilla):
    """Una simulacion completa con un sistema nuevo. Devuelve un dict."""
    sistema = _SistemaCompatible(SistemaUrgencias())
 
    inicio = time.perf_counter()
    resultado = simular(
        sistema,
        n=N_ADMISIONES,
        semilla=semilla,
        duracion_atencion=DURACION_ATENCION,
    )
    segundos = time.perf_counter() - inicio
 
    media = resultado["espera_media_por_nivel"]
    maxima = resultado["espera_maxima_por_nivel"]
 
    return {
        "semilla": semilla,
        "segundos": segundos,
        "atendidos": len(resultado["orden_atencion"]),
        "media_I": media[1],
        "media_II": media[2],
        "max_I": maxima[1],
        "max_II": maxima[2],
        "tiempo_ok": segundos < LIMITE_SEGUNDOS,
        "prioridad_ok": media[1] <= media[2],
        "completo": len(resultado["orden_atencion"]) == N_ADMISIONES,
    }
 
 
def si_no(valor):
    return "si" if valor else "NO"
 
 
def main():
    filas = [correr_semilla(semilla) for semilla in SEMILLAS]
 
    aprobado = all(
        f["tiempo_ok"] and f["prioridad_ok"] and f["completo"]
        for f in filas
    )
 
    lineas = [
        "DEMO DEL CRITERIO DE EXITO",
        f"Fecha: {datetime.now():%Y-%m-%d %H:%M}",
        f"Python {platform.python_version()} ({platform.system()})",
        f"Admisiones por simulacion: {N_ADMISIONES}",
        f"Semillas: {', '.join(str(s) for s in SEMILLAS)}",
        f"Limite de tiempo: {LIMITE_SEGUNDOS} s | "
        f"Duracion de atencion: {DURACION_ATENCION} min",
        "Espera medida por el nivel ORIGINAL (antes del envejecimiento), en minutos.",
        "",
        f"{'semilla':>7} {'tiempo (s)':>11} {'media I':>9} {'media II':>9} "
        f"{'max I':>8} {'max II':>8}  {'< 2 s':>6} {'I <= II':>8} {'completo':>9}",
        "-" * 88,
    ]
 
    for f in filas:
        lineas.append(
            f"{f['semilla']:>7} {f['segundos']:>11.3f} {f['media_I']:>9.2f} "
            f"{f['media_II']:>9.2f} {f['max_I']:>8.2f} {f['max_II']:>8.2f}  "
            f"{si_no(f['tiempo_ok']):>6} {si_no(f['prioridad_ok']):>8} "
            f"{si_no(f['completo']):>9}"
        )
 
    lineas.append("")
    lineas.append("RESULTADO: " + ("APROBADO" if aprobado else "FALLO"))
 
    texto = "\n".join(lineas)
    print(texto)
 
    carpeta = os.path.join(RAIZ, "informe")
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, "demo_criterio.txt")
 
    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write(texto + "\n")
 
    print(f"\nEvidencia guardada en {ruta}")
 
    # Codigo de salida: 0 si aprobado, 1 si fallo (sirve para el CI)
    sys.exit(0 if aprobado else 1)
 
 
if __name__ == "__main__":
    main()
 