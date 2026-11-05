import random
import time
from bisect import bisect_left
from dataclasses import dataclass
from nucleo.abb import ArbolBinarioBusqueda

@dataclass
class Registro:
    documento: str

def medir(tamaño=5000, consultas=1000, semilla=42):
    generador = random.Random(semilla)

    documentos = [str(i) for i in range(tamaño)]
    generador.shuffle(documentos)

    buscados = generador.sample(documentos, min(consultas, tamaño))

    registros = {
        documento: Registro(documento)
        for documento in documentos
    }

    #1. ABB
    arbol = ArbolBinarioBusqueda()

    inicio = time.perf_counter()
    for documento in documentos:
        arbol.insertar(documento, documento)
    tiempo_insertar_abb = time.perf_counter() - inicio

    inicio = time.perf_counter()
    for documento in buscados:
        arbol.buscar(documento)
    tiempo_buscar_abb = time.perf_counter() - inicio

    #2. Diccionario: inserción y búsqueda
    diccionario = {}

    inicio = time.perf_counter()
    for documento in documentos:
        diccionario[documento] = documento
    tiempo_insertar_dict = time.perf_counter() - inicio

    inicio = time.perf_counter()
    for documento in buscados:
        diccionario.get(documento)
    tiempo_buscar_dict = time.perf_counter() - inicio

    #3 Lista ordenada y búsqueda binaria 
    inicio = time.perf_counter()
    lista_ordenada = sorted(documentos)
    tiempo_ordenar_lista = time.perf_counter() - inicio

    inicio = time.perf_counter()
    for documento in buscados:
        posicion = bisect_left(lista_ordenada, documento)
        if posicion < len(lista_ordenada) and lista_ordenada[posicion] == documento:
            pass
    tiempo_buscar_binaria = time.perf_counter() - inicio

    print(f"\nBENCHMARK con {tamaño} documentos")
    print(f"Consultas realizadas: {len(buscados)}")

    print("\nABB")
    print(f"Insercción: {tiempo_insertar_abb:.6f} segundos")
    print(f"Búsqueda: {tiempo_buscar_abb:.6f} segundos")

    print("\nDICCIONARIO")
    print(f"Inserción: {tiempo_insertar_dict:.6f} segundos")
    print(f"Búsqueda: {tiempo_buscar_dict:.6f} segundos")

    print("\nBÚSQUEDA BINARIA")
    print(f"Ordenamiento previo: {tiempo_ordenar_lista:.6f} segundos")
    print(f"Búsqueda: {tiempo_buscar_binaria:.6f} segundos")

if __name__ == "__main__":
    medir()
