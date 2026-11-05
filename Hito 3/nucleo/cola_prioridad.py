"""Cola de prioridad parapacientes de triage"""
from datetime import datetime
from nucleo.cola_dinamica import ColaDinamica
from nucleo.dominio import Nivel

class ColaPrioridadTriage:
    """Gestiona cinco niveles de prioridad y conserva el orden FIFO"""
    def __init__(self):
        self._colas = [None] + [ColaDinamica() for _ in range(5)]

    @staticmethod
    def _obtener_nivel(paciente):
        """Valida y devuelve el nivel numérico del paciente"""
        nivel = getattr(paciente, "nivel", None)

        if nivel is None:
            raise ValueError("El paciente debe tener un nivel de triage")

        try:
            nivel = int(nivel)
        except (TypeError, ValueError):
            raise ValueError("El nivel debe estar entre I y V (1 a 5)")

        if nivel < 1 or nivel > 5:
            raise ValueError("El nivel debe estar entre I y V (1 a 5)")
        return nivel

    @staticmethod
    def _obtener_id(paciente):
        """Usa documento como identificador del paciente"""
        identificador = getattr(paciente, "documento", None)

        if identificador is None:
            identificador = getattr(paciente, "id", None)

        if identificador is None:
            raise ValueError("El paciente debe tener documento o id ")
        return str(identificador)

    def encolar(self, paciente):
        """Agrega un paciente al final de su nivel de prioridad"""
        nivel = self._obtener_nivel(paciente)
        identificador = self._obtener_id(paciente)

        if self._buscar(identificador) is not None:
            raise ValueError("Ya existe un paciente con ese identificador")
        self._colas[nivel].encolar(paciente)

    def desencolar_siguiente(self):
        """Retira el primer paciente del nivel más prioritario disponible"""
        for nivel in range(1, 6):
            if not self._colas[nivel].esta_vacia():
                return self._colas[nivel].desencolar()

        return None

    def _buscar(self, identificador):
        """Buscar un paciente y devuelve (nivel, paciente dek nivel)"""
        identificador = str(identificador)

        for nivel in range(1, 6):
            cola = self._colas[nivel]
            encontrados = []

            while not cola.esta_vacia():
                paciente = cola.desencolar()
                encontrados.append(paciente)
            encontrado = None 

            for paciente in encontrados:
                if self._obtener_id(paciente) == identificador:
                    encontrado = paciente 
                    break

            for paciente in encontrados:
                cola.encolar(paciente)

            if encontrado is not None:
                return nivel, encontrado
        return None

    def retirar(self, identificador):
        """Retira un paciente especifico. Complejidad O(n)"""
        identificador = str(identificador)

        for nivel in range(1, 6):
            cola = self._colas[nivel]
            cantidad_inicial = len(cola)
            retirado = None 

            for _ in range(cantidad_inicial):
                paciente = cola.desencolar()

                if self._obtener_id(paciente) == identificador:
                    retirado = paciente
                else:
                    cola.encolar(paciente)
            if retirado is not None:
                return retirado
        return None

    def reclasificar(self, identificador, nuevo_nivel):
        """Cambia una paciente de nivel conservando el FIFO de destino"""
        try:
            nuevo_nivel = int(nuevo_nivel)
        except (TypeError, ValueError):
            raise ValueError("El nuevo nivel debe estar entre 1 y 5")
        if nuevo_nivel < 1 or nuevo_nivel > 5:
            raise ValueError("El nuevo nivel debe estar entre 1 y 5")

        paciente = self.retirar(identificador)

        if paciente is None:
            return False

        paciente.nivel = nuevo_nivel
        self._colas[nuevo_nivel].encolar(paciente)
        return True

    def contar_por_nivel(self):
        """Devuelve la cantidad de paciente en cada nivel"""
        return {
            nivel: len(self._colas[nivel])
            for nivel in range(1,6)
        }

    def en_orden(self):
        """Devuelve una lista de pacientes por prioridad y orden FIFO"""
        resultado = []

        for nivel in range(1, 6):
            cola = self._colas[nivel]
            cantidad = len(cola)
            temporales = []

            for _ in range(cantidad): 
                paciente = cola.desencolar()
                temporales.append(paciente)
                resultado.append(paciente)

            for paciente in temporales:
                cola.encolar(paciente)
        return resultado

    def envejecer(self, ahora = None):
        """
        Reclasifica un nivel a los pacientes que superaron 
        el tiempo objetivo de espera de su nivel actual

        Devuelve la cantidad de pacientes reclasificados
        """
        if ahora is None:
            ahora = datetime.now()

        reclasificaciones = []
        for nivel in range(1, 6):
            cola = self._colas[nivel]
            cantidad = len(cola)

            for _ in range(cantidad):
                paciente = cola.desencolar()
                llegada = getattr(paciente, "hora_llegada", None)
                if llegada is None:

                    cola.encolar(paciente)
                    continue

                if llegada.tzinfo is not None and ahora.tzinfo is None:
                    tiempo_ahora = ahora.replace(tzinfo=llegada.tzinfo)
                elif llegada.tzinfo is None and ahora.tzinfo is not None:
                    tiempo_ahora = ahora.replace(tzinfo=None)
                else:
                    tiempo_ahora = ahora 

                espera_minutos = (tiempo_ahora - llegada).total_seconds() / 60
                minutos_objetivo = Nivel(nivel).tiempo_objetivo_min
             
                if nivel > 1 and espera_minutos > minutos_objetivo:
                    reclasificaciones.append((paciente, nivel - 1))
                else:
                    cola.encolar(paciente)
           
        for paciente, nuevo_nivel in reclasificaciones:
            paciente.nivel = nuevo_nivel
            self._colas[nuevo_nivel].encolar(paciente)
        return len(reclasificaciones)
