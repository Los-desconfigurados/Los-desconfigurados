import sys
from nucleo.dominio import Nivel
from nucleo.pila_estatica import PilaEstatica

class NodoDesicion:
    """Nodo del arbool de desición para el triaje clinico"""
    def __init__(self, pregunta=None, si=None, no=None, nivel=None):
        self.pregunta = pregunta
        self.si = si
        self.no = no
        self.nivel = nivel

def clasificar(nodo, respuesta):
    """
    Clasificar un paciente utilizando recursión
    
    nodo: NodoDecision raiz o subarbol actual
    respuesta: lista de booleanos [True, False, ...]
    return: objetivo nivel designado.
    """
    if nodo.nivel is not None:
        return nodo.nivel

    if not respuesta:
        raise ValueError("Faltan respuestas para clasificar al paciente")

    respuesta = respuesta.pop(0)

    if respuesta:
        return clasificar(nodo.si, respuesta)

    else:
        return clasificar(nodo.no)

def construir_arbol(spec):
    """Construir el arbol de decision recursivamente desde un diccionario"""
    if "nivel" in spec:
        return NodoDesicion(nivel=Nivel[spec["nivel"]])

    return NodoDesicion(
        pregunta=spec["pregunta"],
        si=construir_arbol(spec["si"]),
        no=construir_arbol(spec["no"])
    )

def profundidad(nodo):
    """Calcula la profundidad maxima del arbol recursivamente"""
    if nodo is None or nodo.nivel is not None:
        return 0

    profundidad_si = profundidad(nodo.si)
    profundidad_no = profundidad(nodo.no)

    return 1 + max(profundidad_si, profundidad_no)

def contar_nodos(nodo):
    """Cuenta el numero total de nodos en el arbol"""
    if nodo is None:
        return 0

    if nodo.nivel is not None:
        return 1

    return 1 + contar_nodos(nodo.si) + contar_nodos(nodo.no)

def clasificar_iterativo(nodo, respuestas):
    """
    Clasificar al paciente de forma iterativa utilizando PilaEstatica
    Elimina el uso de la pila de llamadas de python (Call stack)

    nodo : NodoDecision raíz del árbol
    respuestas: Lista de booleanos [True, False, ...]
    return: Objeto Nivel asignado.
    """

    capacidad = profundidad(nodo) + 1
    pila = PilaEstatica(capacidad)

    respuestas_copia = list(respuestas)

    pila.push(nodo)

    while not pila.esta_vacia():
        actual = pila.pop()

        if actual.nivel is not None:
            return actual.nivel

        if not respuestas_copia:
            raise ValueError("Faltan respuestas para completar la clasificación iterativa")

        respuesta = respuestas_copia.pop(0)

        siguiente_nodo = actual.si if respuesta else actual.no

        if siguiente_nodo is None:
            raise ValueError("Arbol mal estructurado: referencia a nodo nulo")

        pila.push(siguiente_nodo)

def analizar_profundidad_limite():
    "compara el comportamiento del arbol real de triaje frente al limite de recursion de python"

    limite_actual = sys.getrecursionlimit()

    raiz_profunda = NodoDesicion(pregunta="Inicio")
    actual = raiz_profunda
    profundidad_prueba = limite_actual + 100

    for _ in range(profundidad_prueba):
        actual.no = NodoDesicion(pregunta="Continuar")
        actual = actual.no
    actual.nivel = Nivel.V

    respuestas_largas = [False] * (profundidad_prueba + 1)

    error_recursion = False
    try:
        clasificar(raiz_profunda, list(respuestas_largas))
    except RecursionError:
        error_recursion = True

    resultado_iterativo = clasificar_iterativo(raiz_profunda, respuestas_largas)

    return {
        "limite_python": limite_actual,
        "profundidad_probada": profundidad_prueba,
        "fallo_recursivo_con_recursion_error": error_recursion,
        "resultado_iterativo": resultado_iterativo
    }