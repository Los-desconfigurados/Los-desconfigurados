import sys
from hito 2.nucleo.lista_simple import ListaSimple
from nucleo.dominio import Servicio


class Grafo:
   
    def __init__(self, servicios=None, cargar_base=True):
        
        if servicios is None:
            servicios = list(Servicio)

        self.vertices = list(servicios)

        if len(set(self.vertices)) != len(self.vertices):
            raise ValueError("No puede haber vertices duplicados")

        self.n = len(self.vertices)

        self.indices = {servicio: i  for i, servicio in enumerate(self.vertices)}

        # Lista de adyacencia
        self.adyacencia = {servicio: ListaSimple() for servicio in self.vertices}

        # Matriz de adyacencia
        self.matriz = [
            [None for _ in range(self.n)]
            for _ in range(self.n)
        ]

        # Cargar las conexiones iniciales
        if cargar_base:
            self._cargar_traslados_base()

    def _indice(self, servicio):
     

        if servicio not in self.indices:
            raise ValueError("El servicio no pertenece al grafo")

        return self.indices[servicio]

    def _validar_minutos(self, minutos):
        

        if isinstance(minutos, bool) or not isinstance(minutos, (int, float)):
            raise TypeError("Los minutos deben ser numericos")

        if minutos < 0:
            raise ValueError("Los minutos no pueden ser negativos")

    def _cargar_traslados_base(self):
        
        traslados = [
            (Servicio.URGENCIAS, Servicio.OBSERVACION, 5),
            (Servicio.URGENCIAS, Servicio.CIRUGIA, 10),
            (Servicio.URGENCIAS, Servicio.UCI, 8),
            (Servicio.URGENCIAS, Servicio.PEDIATRIA, 6),
            (Servicio.OBSERVACION, Servicio.HOSPITALIZACION, 6),
            (Servicio.OBSERVACION, Servicio.UCI, 7),
            (Servicio.CIRUGIA, Servicio.UCI, 4),
            (Servicio.CIRUGIA, Servicio.HOSPITALIZACION, 9),
            (Servicio.UCI, Servicio.HOSPITALIZACION, 8),
            (Servicio.PEDIATRIA, Servicio.HOSPITALIZACION, 7),
        ]

        for origen, destino, minutos in traslados:
            if origen in self.indices and destino in self.indices:
                self.agregar_arista(origen, destino, minutos)

    def agregar_arista(self, origen, destino, minutos):

        i = self._indice(origen)
        j = self._indice(destino)

        self._validar_minutos(minutos)

        if origen == destino:
            raise ValueError(
                "No se permiten conexiones de un servicio consigo mismo"
            )

        
        if self.matriz[i][j] is not None:

            nueva_lista = ListaSimple()

            for servicio, tiempo in self.adyacencia[origen]:

                if servicio == destino:
                    nueva_lista.agregar_final((destino, minutos))
                else:
                    nueva_lista.agregar_final((servicio, tiempo))

            self.adyacencia[origen] = nueva_lista

        else:
            self.adyacencia[origen].agregar_final(
                (destino, minutos)
            )

        
        self.matriz[i][j] = minutos

    def es_traslado_valido(self, origen, destino):
        
        i = self._indice(origen)
        j = self._indice(destino)

        return self.matriz[i][j] is not None

    def vecinos(self, origen):
      
        self._indice(origen)

        return list(self.adyacencia[origen])

    def bfs(self, origen):
        
        self._indice(origen)

        visitados = {origen}
        cola = [origen]
        recorrido = []
        frente = 0

        while frente < len(cola):

            actual = cola[frente]
            frente += 1

            recorrido.append(actual)

            for destino, minutos in self.adyacencia[actual]:

                if destino not in visitados:
                    visitados.add(destino)
                    cola.append(destino)

        return recorrido

    def camino_minimo(self, origen, destino):
        

        inicio = self._indice(origen)
        fin = self._indice(destino)

        distancias = [float("inf")] * self.n
        anteriores = [None] * self.n
        visitados = [False] * self.n

        distancias[inicio] = 0

        for _ in range(self.n):

            actual = None
            menor = float("inf")

            
            for i in range(self.n):

                if not visitados[i] and distancias[i] < menor:
                    menor = distancias[i]
                    actual = i

            if actual is None:
                break

            if actual == fin:
                break

            visitados[actual] = True

            # Revisar los vecinos usando la matriz
            for j in range(self.n):

                peso = self.matriz[actual][j]

                if peso is not None and not visitados[j]:

                    nueva_distancia = distancias[actual] + peso

                    if nueva_distancia < distancias[j]:
                        distancias[j] = nueva_distancia
                        anteriores[j] = actual

        
        if distancias[fin] == float("inf"):
            return None

        # Reconstruir el camino
        ruta_indices = []
        actual = fin

        while actual is not None:
            ruta_indices.append(actual)
            actual = anteriores[actual]

        ruta_indices.reverse()

        ruta = [self.vertices[i] for i in ruta_indices]

        return ruta, distancias[fin]

    def memoria(self):

        # Memoria de la lista de adyacencia
        memoria_lista = sys.getsizeof(self.adyacencia)

        for servicio, lista in self.adyacencia.items():

            memoria_lista += sys.getsizeof(lista)

            actual = lista.cabeza

            while actual is not None:

                memoria_lista += sys.getsizeof(actual)
                memoria_lista += sys.getsizeof(actual.dato)

                actual = actual.siguiente

        # Memoria de la matriz de adyacencia
        memoria_matriz = sys.getsizeof(self.matriz)

        for fila in self.matriz:
            memoria_matriz += sys.getsizeof(fila)

        return {"lista_adyacencia_bytes": memoria_lista, "matriz_adyacencia_bytes": memoria_matriz}
