from datetime import datetime
from nucleo.dominio import Paciente, Nivel, SignosVitales
from nucleo.registro import RegistroPacientes
from nucleo.cola_prioridad import ColaPrioridadTriage
from nucleo.cola_estatica import ColaCircularEstatica, ColaLlena
from nucleo.deshacer import GestorDeshacer
from nucleo.arbol_triage import (
    clasificar_iterativo,
    construir_arbol,
)

ARBOL_PREDETERMINADO_SPEC = {
    "pregunta": "¿El paciente presenta paro cardiorrespiratorio o alteración hemodinámica severa?",
    "si": {"nivel": "I"},
    "no": {
        "pregunta": "¿Presenta dolor torácico agudo, dificultad respiratoria grave o alteración del estado mental?",
        "si": {"nivel": "II"},
        "no": {
            "pregunta": "¿Presenta fiebre alta, dolor abdominal agudo o signos de infección moderada?",
            "si": {"nivel": "III"},
            "no": {
                "pregunta": "¿Presenta traumatismo menor o sintomatología leve de más de 24 horas?",
                "si": {"nivel": "IV"},
                "no": {"nivel": "V"},
            },
        },
    },
}

class SesionCuestionario:
    "Mantiene el estado actual de la navegacion por el arbol de triaje"

    def __init__(self, arbol):
        self.nodo_actual = arbol
        self.respuestas = []

class SistemaUrgencias:

    def __init__(self, capacidad_camillas: int = 10):
        """Inicializa el sistema de urgencias"""
        self.registro = RegistroPacientes()
        self.cola_triage = ColaPrioridadTriage()
        self.ambulancias = ColaCircularEstatica(capacidad_camillas)
        self.gestor_deshacer = GestorDeshacer()
        self.arbol_triage = construir_arbol(ARBOL_PREDETERMINADO_SPEC)
        self.paciente_en_atencion = None

    def _asegurar_id_paciente(self, paciente: Paciente):
        """Asegura que el paciente tenga un atributo "id" compatible con el registro"""
        if not hasattr(paciente, "id") or paciente.id is None:
            paciente.id = str(paciente.documento)

    def registrar_paciente(
        self,
        nombre: str,
        documento: str,
        edad: int,
        motivo: str,
        nivel=None,
        respuesta=None) -> Paciente:
        """
        Registra un paciente en el sistema
        
        Si no se proporciona nivel, puede
        utilizar las respuestas del cuestionario de triage

        Retorna: Paciente registrado
        """
        nivel_asignado = None

        if nivel is not None:
            if isinstance(nivel, Nivel):
                nivel_asignado = nivel
            else:
                nivel_asignado = Nivel(int(nivel))
        elif respuesta is not None and len(respuesta) > 0:
            nivel_asignado = clasificar_iterativo(self.arbol_triage, respuesta)
        else:
            nivel_asignado = Nivel.V

        paciente = Paciente(
            nombre=nombre, 
            documento=str(documento),
            edad=edad,
            motivo=motivo,
            nivel=nivel_asignado,
            hora_llegada=datetime.now(),
        )

        self._asegurar_id_paciente(paciente)
        self.registro.ingresar(paciente)
        self.cola_triage.encolar(paciente)
        paciente_id = paciente.id

        def accion_inversa():
            self.cola_triage.retirar(paciente_id)
            self.registro.dar_salida(paciente_id)
            return f"Se deshizo el registro del paciente {nombre}({paciente_id})"

        self.gestor_deshacer.registrar(accion_inversa)

        return paciente

    def iniciar_cuestionario(self):
        """
        Inicia el cuestionario de triage

        Retorna: Pregunta inicial
        """
        sesion = SesionCuestionario(self.arbol_triage)
        return sesion, sesion.nodo_actual.pregunta

    def responder(self, sesion: SesionCuestionario, si: bool):
        """
        Responde una pregunta del cuestionario

        Retorna: Siguiente pregunta o nivel de triage
        """
        sesion.respuestas.append(si)
        siguiente = sesion.nodo_actual.si if si else sesion.nodo_actual.no
        sesion.nodo_actual = siguiente

        if siguiente.nivel is not None:
            return siguiente.nivel

        return siguiente.pregunta

    def llamar_siguiente(self) -> Paciente | None:
        """
        Obtiene el siguiente paciente según la prioridad de triage

        Retorna: Paciente o None
        """
        paciente = self.cola_triage.desencolar_siguiente()

        if paciente is not None:
            anterior_en_atencion = self.paciente_en_atencion
            self.paciente_en_atencion = paciente

            def accion_inversa():
                self.paciente_en_atencion = anterior_en_atencion
                self.cola_triage.encolar(paciente)
                return f"Se reincorporó a la cola al paciente {paciente.nombre}"

            self.gestor_deshacer.registrar(accion_inversa)

        return paciente

    def dar_alta(self, id: str, motivo: str = "Alta médica") -> Paciente:
        """
        Da de alta, traslada o registra el abandono de un paciente
        """
        id_str = str(id)

        self.cola_triage.retirar(id_str)

        paciente = self.registro.dar_salida(id_str, motivo)

        if self.paciente_en_atencion and getattr(self.paciente_en_atencion, "id", None) == id_str:
            self.paciente_en_atencion = None

        def accion_inversa():
            self.registro.ingresar(paciente)
            self.cola_triage.encolar(paciente)
            return f"Se restauró el alta del paciente {paciente.nombre}"

        self.gestor_deshacer.registrar(accion_inversa)

        return paciente

    def reclasificar(self, id: str, nuevo_nivel, justificacion: str = "")-> bool:
        """
        Cambia el nivel de triage de un paciente
        """
        id_str = str(id)
        paciente = self.registro.obtener(id_str)

        if paciente is None:
            return False

        nivel_anterior = paciente.nivel
        nuevo_nivel_obj = Nivel(int(nuevo_nivel)) if not isinstance(nuevo_nivel, Nivel) else nuevo_nivel

        exito = self.cola_triage.reclasificar(id_str, nuevo_nivel_obj)

        if exito:
            paciente.nivel = nuevo_nivel_obj

            def accion_inversa():
                self.cola_triage.reclasificar(id_str, nivel_anterior)
                paciente.nivel = nivel_anterior
                mgs = f"se revirtió la reclasificacion de {paciente.nombre} a nivel {nivel_anterior.value}"
                if justificacion:
                    mgs += f" (Justificación previa: {justificacion})"
                return mgs

            self.gestor_deshacer.registrar(accion_inversa)

        return exito

    def registrar_signos(self, id: str, signos: SignosVitales):
        """
        Registra una medición de signos vitales
        """
        id_str = str(id)
        self.registro.registrar_signos(id_str, signos)

    def historial(self, id: str) -> list[SignosVitales]:
        """
        Retorna el historial de signos vitales del paciente
        """
        id_str = str(id)
        return list(self.registro.historial(id_str))

    def en_espera(self, nivel=None) -> list[Paciente]:
        """
        Retorna los pacientes que están en espera

        Si se proporciona nivel, filtra por dicho nivel
        """
        pacientes = self.cola_triage.en_orden()

        if nivel is not None:
            nivel_val = int(nivel) if isinstance(nivel, Nivel) else int(nivel)
            return [p for p in pacientes if int(p.nivel) == nivel_val]

        return pacientes

    def buscar(self, texto: str) -> list[Paciente]:
        """
        Busca pacientes utilizando un texto
        """
        texto_lower = str(texto).lower()
        resultado = []

        for paciente in self.registro.listar():
            if texto_lower in paciente.nombre.lower() or texto_lower in str(paciente.documento):
                resultado.append(paciente)

        return resultado

    def deshacer(self) -> str | None:
        """
        Deshace la última acción reversible

        Retorna: Descripción de la acción deshecha o None
        """
        if self.gestor_deshacer.esta_vacio():
            return None

        return self.gestor_deshacer.deshacer()

    def ingresar_ambulancia(self, datos: dict) -> bool:
        """
        Registra una ambulancia en la cola circular

        Retorna: False si la cola está llena
        """
        try:
            self.ambulancias.encolar(datos)
            return True
        except ColaLlena:
            return False

    def camillas(self) -> tuple [int, int]:
        """
        Retorna la cantidad de camillas ocupadas y el total

        Retorna: Tupla (ocupadas, total)
        """
        return len(self.ambulancias), self.ambulancias._capacidad

    def metricas(self) -> dict:
        """
        Retorna métricas generales del sistema

        Retorna: Diccionario con conteo por nivel, espera media y pacientes vencidos
        """
        self.cola_triage.envejecer()
        conteo = self.cola_triage.contar_por_nivel()

        pacientes_espera = self.en_espera()
        ahora = datetime.now()
        vencidos = 0
        tiempos_espera = []

        for p in pacientes_espera:
            if p.hora_llegada:
                minutos = (ahora - p.hora_llegada).total_seconds() / 60
                tiempos_espera.append(minutos)
                if minutos > p.nivel.tiempo_objetivo_min:
                    vencidos += 1

        espera_media = sum(tiempos_espera) / len(tiempos_espera) if tiempos_espera else 0.0

        return {
            "conteo_por_nivel": conteo,
            "espera_media_min": round(espera_media, 1),
            "pacientes_vencidos": vencidos,
            "total_en_espera": len(pacientes_espera),
        }

    def snapshot_estructuras(self) -> dict:
        """
        Retorna un resumen de las estructuras utilizadas
        por el sistema
        """
        return {
            "registro_lista_doble_tamano": len(self.registro),
            "cola_prioridad_conteos": self.cola_triage.contar_por_nivel(),
            "ambulancias_ocupadas": len(self.ambulancias),
            "ambulancias_capacidad": self.ambulancias._capacidad,
            "acciones_deshacer_pendientes": len(self.gestor_deshacer),
        }