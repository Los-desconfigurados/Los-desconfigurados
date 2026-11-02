import random 
from datetime import datetime, timedelta
from nucleo.dominio import Paciente, Nivel 

def generar_llegadas_poisson(n=5000, semilla=None):
    """Genera pacientes con intervalos entre llegadas
    siguiendo una distribución exponencial"""

    if n <= 0:
        raise ValueError("La cantidad de pacientes debe ser mayor que cero")

    generador = random.Random(semilla)
    pacientes = []
    tiempo_actual = datetime.now()

    for i in range(n):
        intervalo = generador.expovariate(1)
        tiempo_actual += timedelta(minutes=intervalo)

        paciente = Paciente(
            nombre=f"Paciente {i + 1}", 
            documento = str(1000000001 + i),
            edad = generador.randint(1, 100),
            motivo="Motivo de consulta",
            nivel=Nivel(generador.randint(1, 5)),
            hora_llegada=tiempo_actual
        )

        pacientes.append(paciente)
    return pacientes

def simular(sistema, n=5000, semilla=None, duracion_atencion=1):
    if duracion_atencion <= 0:
        raise ValueError("La duración de atención debe ser positiva")

    pacientes = generar_llegadas_poisson(n, semilla)
    pacientes.sort(key=lambda p: p.hora_llegada)

    #Guardar el nivel original de cada paciente
    niveles_originales = {}

    #Estadísticas por nivel
    esperas = {nivel: [] for nivel in range(1, 6)}
    orden_atencion = []
    indice = 0
    reloj = pacientes[0].hora_llegada
    inicio = reloj

    def hay_pacientes_esperando():
        return any(
            not cola.esta_vacia()
            for cola in sistema.cola_triage._colas.values()
        )
    while indice < len(pacientes) or hay_pacientes_esperando():

        #Registrar unicamente los pacientes que ya legaron
        while (
            indice < len(pacientes)
            and pacientes[indice].hora_llegada <= reloj
        ):
            paciente = pacientes[indice]

            registrado = sistema.registrar_paciente(
                nombre=paciente.nombre,
                documento=paciente.documento,
                edad=paciente.edad,
                motivo=paciente.motivo,
                nivel=paciente.nivel
            )

            #Conservar la hora de llegada simulada
            registrado.hora_llegada = paciente.hora_llegada

            #Guardar el nivel original antes del envejecimiento
            niveles_originales[registrado.documento] = int(registrado.nivel)

            indice += 1

        #Si no hay pacientes esperando, avanzar hasta la próxima llegada
        if not hay_pacientes_esperando():
            if indice < len(pacientes):
                reloj = pacientes[indice].hora_llegada
                continue
            break

        #Actualizar prioridades según el tiempo de espera
        sistema.cola_triage.envejecer(ahora=reloj)

        #Atender al siguiente paciente
        paciente_atendido = sistema.llamar_siguiente()

        if paciente_atendido is None:
            continue

        nivel_original = niveles_originales[
            paciente_atendido.documento
        ]

        espera = (
            reloj - paciente_atendido.hora_llegada
        ).total_seconds() / 60

        esperas[nivel_original].append(espera)
        orden_atencion.append(paciente_atendido.documento)

        #Durante la atención pueden llegar otros pacientes 
        reloj += timedelta(minutes=duracion_atencion)

    espera_media = {}
    espera_maxima = {}

    for nivel in range(1, 6):
        tiempos = esperas[nivel]
        espera_media[nivel] = sum(tiempos) / len(tiempos) if tiempos else 0
        espera_maxima[nivel] = max(tiempos) if tiempos else 0

    tiempo_total = (reloj - inicio).total_seconds() / 60

    return {
        "espera_media_por_nivel": espera_media,
        "espera_maxima_por_nivel": espera_maxima,
        "tiempo_total": tiempo_total,
        "orden_atencion": orden_atencion
    }