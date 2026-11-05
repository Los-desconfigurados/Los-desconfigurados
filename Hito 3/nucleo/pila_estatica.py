class PilaLlena(Exception):
    """Se ejecuta cuando se intenta agregar un elemento a la pila llena"""

class PilaVacia(Exception):
    """Se ejecuta cuando se intenta consultar o retirar un elemento de una pila vacía"""

class PilaEstatica:
    """Pila de capacidad fija con operaciones push, pop y peek"""

    def __init__(self, capacidad):
        """Crea una pila vacía con la capacidad indicada."""
        if not isinstance(capacidad, int) or isinstance(capacidad, bool):
            raise TypeError("La capacidad debe ser un número entero.")
        if capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor que cero.")

        self._datos = [None] * capacidad
        self._capacidad = capacidad
        self._tope = -1

    def push(self, elemento):
        """Agrega un elemento al tope. Lanza pilaLlena si no hay espacio."""
        if self._tope == self._capacidad - 1:
            raise PilaLlena("La pila está llena.")
        self._tope += 1
        self._datos[self._tope] = elemento
            
    def pop(self):
        """Retira y devuelve el elemento del tope"""
        if self._tope == - 1:
            raise PilaVacia("La pila está vacía.")

        elemento =self._datos[self._tope]
        self._datos[self._tope] = None
        self._tope -= 1
        return elemento 

    def peek(self):
        """Devuelve el elemento del tope sin retirarlo"""
        if self._tope == -1:
            raise PilaVacia("La pila está vacía.")
        return self._datos[self._tope]

    def __len__(self):
        """Devuelve la cantidad de elementos almacenados"""
        return self._tope + 1

    def esta_vacia(self):
        """Indica si la pila está vacía"""
        return self._tope == -1

    def esta_llena(self):
        """Indica si la pila alcanzó su capacidad máxima"""
        return self._tope == self._capacidad - 1






