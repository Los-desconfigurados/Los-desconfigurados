
from collections import deque

from nucleo.simulacion import simular


class ColaPrueba:
    def __init__(self):
        self.pacientes = deque()

    def esta_vacia(self):
        return len(self.pacientes) == 0

    def encolar(self, paciente):
        self.pacientes.append(paciente)

    def desencolar(self):
        if self.esta_vacia():
            return None
        return self.pacientes.popleft()


class ColaTriagePrueba:
    def __init__(self):
        self._colas = {
            nivel: ColaPrueba()
            for nivel in range(1, 6)
        }

    def envejecer(self, ahora=None):
        pass


class SistemaPrueba:
    def __init__(self):
        self.cola_triage = ColaTriagePrueba()
        self.pacientes = {}

    def registrar_paciente(
        self, nombre, documento, edad, motivo, nivel
    ):
        from nucleo.dominio import Paciente

        paciente = Paciente(
            nombre=nombre,
            documento=documento,
            edad=edad,
            motivo=motivo,
            nivel=nivel
        )

        self.pacientes[documento] = paciente
        self.cola_triage._colas[int(nivel)].encolar(paciente)

        return paciente

    def llamar_siguiente(self):
        for nivel in range(1, 6):
            cola = self.cola_triage._colas[nivel]

            if not cola.esta_vacia():
                return cola.desencolar()

        return None

def ejecutar_prueba():
    sistema = SistemaPrueba()

    resultado = simular(
        sistema,
        n=100,
        semilla=42,
        duracion_atencion=1
    )

    print("Pacientes atendidos:", len(resultado["orden_atencion"]))
    print("Tiempo total:", resultado["tiempo_total"])

    print("Espera media por nivel:")
    for nivel, tiempo in resultado["espera_media_por_nivel"].items():
        print(f"Nivel {nivel}: {tiempo:.2f} minutos")

    print("Espera máxima por nivel:")
    for nivel, tiempo in resultado["espera_maxima_por_nivel"].items():
        print(f"Nivel {nivel}: {tiempo:.2f} minutos")

    assert len(resultado["orden_atencion"]) == 100
    assert resultado["tiempo_total"] > 0

    print("PRUEBA SUPERADA")


if __name__ == "__main__":
    ejecutar_prueba()