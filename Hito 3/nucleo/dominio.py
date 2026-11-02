from enum import IntEnum
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
            Nivel.III: 8,    #Consultar tiempos con liz
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

@dataclass
class Paciente:
    nombre: str
    documento: str
    edad: int
    motivo: str
    nivel: Nivel | None = None
    hora_llegada: datetime | None = None

@dataclass
class SignosVitales:
    temperatura: float
    frecuencia_cardiaca: int
    frecuencia_respiratoria: int
    saturacion_oxigeno: float

@dataclass
class Accion:
    tipo: str
    paciente_id: str
    datos: dict