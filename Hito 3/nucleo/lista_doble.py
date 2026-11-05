from nucleo.nodos import NodoDoble

class ListaDoble:

    def __init__(self):
        self.cabeza = None
        self.cola = None
        self._tamano = 0

    def esta_vacia(self):
        return self._tamano == 0

    def __len__(self):
        return self._tamano

    def _validar_nodo(self, nodo):
        if nodo is None or getattr(nodo, "lista", None) is not self:
            raise ValueError("El nodo no pertenece a esta lista")

    def insertar_final(self, dato):
        nuevo = NodoDoble(dato)
        nuevo.lista = self

        if self.esta_vacia():
            self.cabeza = nuevo
            self.cola = nuevo
        else:
            nuevo.anterior = self.cola
            self.cola.siguiente = nuevo
            self.cola = nuevo

        self._tamano += 1
        return nuevo

    def insertar_antes(self, nodo, dato):
        self._validar_nodo(nodo)

        nuevo = NodoDoble(dato)
        nuevo.lista = self
        nuevo.siguiente = nodo
        nuevo.anterior = nodo.anterior

        if nodo.anterior is None:
            self.cabeza = nuevo
        else:
            nodo.anterior.siguiente = nuevo

        nodo.anterior = nuevo
        self._tamano += 1
        return nuevo

    def insertar_despues(self, nodo, dato):
        self._validar_nodo(nodo)

        nuevo = NodoDoble(dato)
        nuevo.lista = self
        nuevo.anterior = nodo
        nuevo.siguiente = nodo.siguiente

        if nodo.siguiente is None:
            self.cola = nuevo
        else:
            nodo.siguiente.anterior = nuevo

        nodo.siguiente = nuevo
        self._tamano += 1
        return nuevo

    def eliminar(self, nodo):
        self._validar_nodo(nodo)

        if nodo.anterior is None:
            self.cabeza = nodo.siguiente
        else:
            nodo.anterior.siguiente = nodo.siguiente

        if nodo.siguiente is None:
            self.cola = nodo.anterior
        else:
            nodo.siguiente.anterior = nodo.anterior

        dato = nodo.dato

        nodo.anterior = None
        nodo.siguiente = None
        nodo.lista = None

        self._tamano -= 1
        return dato

    def buscar(self, predicado):
        actual = self.cabeza

        while actual is not None:
            if predicado(actual.dato):
                return actual
            actual = actual.siguiente

        return None

    def recorrer_adelante(self):
        actual = self.cabeza

        while actual is not None:
            siguiente = actual.siguiente
            yield actual.dato
            actual = siguiente

    def recorrer_atras(self):
        actual = self.cola

        while actual is not None:
            anterior = actual.anterior
            yield actual.dato
            actual = anterior

    def __iter__(self):
        return self.recorrer_adelante()
