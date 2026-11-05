"""Cola dinámica FIFO implementada mediante nodos enlazados"""
class ColaVacia(Exception):
    """Se ejecuta cuando se intenta retirar o consultar una cola vacía"""

class ColaDinamica:
    """Cola sin capacidad fija con inserción y extracción O(1)"""

    class _Nodo:
        """Nodo que almacena un elemento y referencia al siguiente"""

        def __init__(self, dato, siguiente=None):
            self.dato = dato 
            self.siguiente = siguiente

    def __init__(self):
        self._frente = None
        self._final = None 
        self._cantidad = 0

    def encolar(self, elemento):
        """Agrega un elemento al final de la cola"""
        nuevo = self._Nodo(elemento)

        if self._final is None:
            self._frente = nuevo
            self._final = nuevo
        else:
            self._final.siguiente = nuevo 
            self._final = nuevo 

        self._cantidad += 1

    def desencolar(self):
        """Retira y devuelve el elemento que lleva"""
        if self._frente is None:
            raise ColaVacia("La cola está vacía")

        elemento = self._frente.dato
        self._frente = self._frente.siguiente
        self._cantidad -= 1

        if self._frente is None:
            self._final = None 
        return elemento

    def frente(self):
        """Devuelve el primer elemento sin retirarlo"""
        if self._frente is None:
            raise ColaVacia("La cola está vacía")
        return self._frente.dato

    def __len__(self):
        """Devuelve la cantidad de elementos"""
        return self._cantidad

    def esta_vacia(self):
        """Indica si la cola no contiene elementos"""
        return self._cantidad == 0