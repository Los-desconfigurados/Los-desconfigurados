"""Pila dinámica implementada mediante nodos enlazados"""

class PilaDinamica:
    """Pila sin capacidad fija que sigue el principio de LIFO."""

    class _Nodo:
        """Nodo interno que almacena un elemento y apunta al anterior"""

        def __init__(self, dato, siguiente = None):
            self.dato = dato
            self.siguiente = siguiente

    def __init__(self):
        """Inicializa una pila vacía"""
        self._tope = None
        self._cantidad = 0

    def push(self, elemento):
        """Agrega un elemento al tope de la pila en O(1)"""
        nuevo = self._Nodo(elemento, self._tope)
        self._tope = nuevo
        self._cantidad += 1

    def pop(self):
        """Retira y devuelve el elemento del tope"""
        if self._tope is None:
            raise PilaVacia("La pila está vacía")

        elemento = self._tope.dato
        self._tope = self._tope.siguiente
        self._cantidad -= 1
        return elemento 


    def peek(self):
        """Consulta el elemento del tope sin retirarlo"""
        if self._tope is None:
            raise PilaVacia("La pila está vacía")
        return self._tope.dato

    def __len__(self):
        """Devuelve la cantidad de elementos almacenados"""
        return self._cantidad

    def esta_vacia(self):
        """Indica si la pila está vacía"""
        return self._tope is None

class PilaVacia(Exception):
    """Se ejecuta cuando se intenta consultar o retiraar de una pila vacía"""