from enum import Enum, IntEnum
from dataclasses import dataclass
from datetime import datetime


class Nivel(IntEnum):
    I = 1
    II = 2
    III = 3
    IV = 4
    V = 5

    @property
    def tiempo_objetivo_min(self):
        tiempos = {
            Nivel.I: 2,
            Nivel.II: 5,
            Nivel.III: 8,
            Nivel.IV: 12,
            Nivel.V: 15
        }
        return tiempos[self]

    @property
    def color(self):
        colores = {
            Nivel.I: "rojo",
            Nivel.II: "naranja",
            Nivel.III: "amarillo",
            Nivel.IV: "verde",
            Nivel.V: "azul"
        }
        return colores[self]


class Servicio(Enum):
   
    URGENCIAS = 0
    OBSERVACION = 1
    CIRUGIA = 2
    UCI = 3
    HOSPITALIZACION = 4
    PEDIATRIA = 5

    @property
    def etiqueta(self):
        etiquetas = {
            Servicio.URGENCIAS: "Urgencias",
            Servicio.OBSERVACION: "Observacion",
            Servicio.CIRUGIA: "Cirugia",
            Servicio.UCI: "UCI",
            Servicio.HOSPITALIZACION: "Hospitalizacion",
            Servicio.PEDIATRIA: "Pediatria"
        }
        return etiquetas[self]


@dataclass
class Paciente:
    nombre: str
    documento: str
    edad: int
    motivo: str
    nivel: Nivel | None = None
    hora_llegada: datetime | None = None
    servicio: Servicio = Servicio.URGENCIAS


@dataclass
class SignosVitales:
    temperatura: float
    frecuencia_cardiaca: int
    frecuencia_respiratoria: int
    saturacion_oxigeno: float


TRASLADO = "traslado"


@dataclass
class Accion:
    tipo: str
    paciente_id: str
    datos: dict

    def inversa(self):
       
        if self.tipo != TRASLADO:
            raise ValueError("Solo se puede invertir una accion de traslado")

        return Accion(
            tipo=TRASLADO,
            paciente_id=self.paciente_id,
            datos={"origen": self.datos["destino"], "destino": self.datos["origen"], "minutos": self.datos.get("minutos")}
        )


def crear_traslado(paciente_id, origen, destino, minutos=None):
    """Crea una accion de traslado validando sus datos."""

    if not isinstance(origen, Servicio):
        raise TypeError("El origen debe ser un Servicio valido")

    if not isinstance(destino, Servicio):
        raise TypeError("El destino debe ser un Servicio valido")

    if origen == destino:
        raise ValueError("El origen y el destino deben ser diferentes")

    if minutos is not None:
        if isinstance(minutos, bool) or not isinstance(minutos, (int, float)):
            raise TypeError("Los minutos deben ser un numero")

        if minutos < 0:
            raise ValueError("Los minutos no pueden ser negativos")

    return Accion(
        tipo=TRASLADO,
        paciente_id=str(paciente_id),
        datos={"origen": origen, "destino": destino, "minutos": minutos}
    )
