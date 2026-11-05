import csv
import gc
import os
import platform
import random
import sys
import tracemalloc

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from nucleo.grafo import Grafo
from nucleo.lista_simple import ListaSimple

TAMANOS = (100, 250, 500, 1000)

DENSIDADES = (("disperso (grado 4)", None), ("5%", 0.05), ("25%", 0.25), ("50%", 0.50),)

SEMILLA = 7


def generar_aristas(n, probabilidad):
    
    azar = random.Random(SEMILLA)
    p = 4 / n if probabilidad is None else probabilidad

    return [
        (o, d, azar.randint(1, 30))
        for o in range(n)
        for d in range(n)
        if o != d and azar.random() < p
    ]


def construir_grafo(n, aristas):
   
    grafo = Grafo(list(range(n)), cargar_base=False)

    for origen, destino, minutos in aristas:
        grafo.agregar_arista(origen, destino, minutos)

    return grafo


def construir_lista(n, aristas):
    """Solo la lista de adyacencia, igual que en Grafo."""
    adyacencia = {v: ListaSimple() for v in range(n)}

    for origen, destino, minutos in aristas:
        adyacencia[origen].agregar_final((destino, minutos))

    return adyacencia


def construir_matriz(n, aristas):
    """Solo la matriz de adyacencia, igual que en Grafo."""
    matriz = [[None for _ in range(n)] for _ in range(n)]

    for origen, destino, minutos in aristas:
        matriz[origen][destino] = minutos

    return matriz


def medir(construir):
    
    gc.collect()
    tracemalloc.start()
    base = tracemalloc.get_traced_memory()[0]

    objeto = construir()

    actual = tracemalloc.get_traced_memory()[0]
    tracemalloc.stop()

    del objeto

    return actual - base


def main():
    encabezado = ["vertices", "densidad", "aristas", "lista_estimada", "lista_medida", "matriz_estimada", "matriz_medida", "menor_memoria",]
    filas = []

    print(f"Python {platform.python_version()} ({platform.system()})")
    print()
    print(
        f"{'V':>5}  {'densidad':<18}{'E':>8}  "
        f"{'lista est.':>13}{'lista med.':>13}  "
        f"{'matriz est.':>13}{'matriz med.':>13}  menor"
    )
    print("-" * 104)

    for n in TAMANOS:
        for nombre, probabilidad in DENSIDADES:
            aristas = generar_aristas(n, probabilidad)

            estimada = construir_grafo(n, aristas).memoria()
            lista_est = estimada["lista_adyacencia_bytes"]
            matriz_est = estimada["matriz_adyacencia_bytes"]

            lista_med = medir(lambda: construir_lista(n, aristas))
            matriz_med = medir(lambda: construir_matriz(n, aristas))

            menor = "lista" if lista_med < matriz_med else "matriz"

            fila = [n, nombre, len(aristas), lista_est, lista_med, matriz_est, matriz_med, menor,]
            filas.append(fila)

            print(
                f"{n:>5}  {nombre:<18}{len(aristas):>8,}  "
                f"{lista_est:>13,}{lista_med:>13,}  "
                f"{matriz_est:>13,}{matriz_med:>13,}  {menor}"
            )

    carpeta = os.path.join(RAIZ, "informe")
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, "bench_grafo.csv")

    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(encabezado)
        escritor.writerows(filas)

    print()
    print("Valores en bytes. 'est.' = Grafo.memoria() (superficial);")
    print("'med.' = memoria asignada medida con tracemalloc.")
    print(f"Tabla guardada en {ruta}")


if __name__ == "__main__":
    main()
