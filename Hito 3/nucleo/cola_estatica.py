"""Cola circular estática implementada mediante un arreglo fijo """

class ColaLlena(Exception):
    """Se ejecuta cuando se intenta agregar a una cola llena"""

class ColaVacia(Exception):
    """Se ejecuta cuando se intenta agregar a una cola llena."""

class ColaCircularEstatica:
    """Cola FIFO circular con capacidad fija y con operaciones O(1)"""
    def __init__(self, capacidad):
        """Inicializa la cola con una capacidad determinada"""
        if not isinstance(capacidad, int) or isinstance(capacidad, bool):
            raise TypeError("La capacidad debe ser un número entero.")
        if capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor que cero.")

        self._datos = [None] * capacidad 
        self._capacidad = capacidad 
        self._frente = 0
        self._final = -1
        self._cantidad = 0

    def encolar(self, elemento):
        """Agrega un elemento al final de la cola en O(1)"""
        if self._cantidad == self._capacidad:
            raise ColaLlena("La cola está llena")

        self._final = (self._final +1) % self._capacidad
        self._datos[self._final] = elemento 
        self._cantidad += 1

    def desencolar(self):
        """Retira y devuelve el elemento más antiguo de la cola"""
        if self._cantidad == 0:
            raise ColaVacia("La cola está vacía")

        elemento = self._datos[self._frente]
        self._datos[self._frente] = None
        self._frente = (self._frente +1) % self._capacidad
        self._cantidad -= 1
        return elemento 

    def frente(self):
        """Devuelve el primer elemento sin retirarlo"""
        if self._cantidad == 0:
            raise ColaVacia("La cola está vacía")
        return self._datos[self._frente]

    def __len__(self):
        """Devuelve la cantidad de elementos de la cola"""
        return self._cantidad

    def esta_vacia(self):
        """Indica si la cola está vacía"""
        return self._cantidad == 0

    def esta_llena(self):
        """Indica si la cola alcanzó su capacidad máxima"""
        return self._cantidad == self._capacidad