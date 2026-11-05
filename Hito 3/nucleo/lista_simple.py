from nucleo.nodos import NodoSimple

class ListaSimple:

    def __init__(self):
        self.cabeza = None
        self.cola = None
        self._tamano = 0

    def esta_vacia(self):
        return self._tamano == 0

    def __len__(self):
        return self._tamano

    def agregar_final(self, dato):
        nuevo = NodoSimple(dato)

        if self.esta_vacia():
            self.cabeza = nuevo
            self.cola = nuevo
        else:
            self.cola.siguiente = nuevo
            self.cola = nuevo

        self._tamano += 1

    def agregar_inicio(self, dato):
        nuevo = NodoSimple(dato)
        nuevo.siguiente = self.cabeza
        self.cabeza = nuevo

        if self.cola is None:
            self.cola = nuevo

        self._tamano += 1

    def eliminar_inicio(self):
        
        if self.cabeza is None:
            raise IndexError("La lista está vacía")

        nodo = self.cabeza
        self.cabeza = nodo.siguiente

        if self.cabeza is None:
            self.cola = None

        self._tamano -= 1
        return nodo.dato

    def buscar(self, predicado):
        actual = self.cabeza

        while actual is not None:
            if predicado(actual.dato):
                return actual.dato
            actual = actual.siguiente

        return None

    def ultimos(self, n):
    
        if n <= 0:
            return

        saltar = self._tamano - n
        if saltar < 0:
            saltar = 0

        actual = self.cabeza

        while actual is not None:
            if saltar > 0:
                saltar -= 1
            else:
                yield actual.dato
            actual = actual.siguiente

    def __iter__(self):
        actual = self.cabeza

        while actual is not None:
            yield actual.dato
            actual = actual.siguiente
