<<<<<<< HEAD
from nucleo.cola_dinamica import ColaDinamica
class _NodoABB:
    """Nodo que almacena un paciente y sus referencias de izquierda a derecha."""
    def __init__(self, documento, paciente):
        self.documento = documento
        self.paciente = paciente
        self.izquierdo = None
        self.derecho = None

class ArbolBinarioBusqueda:
    """(ABB) que organiza pacientes utilizando su número de documento como su clave"""
    def __init__(self):
        """Inicializa un árbol vacío"""
        self._raiz = None
        self._cantidad = 0

    @staticmethod
    def _obtener_documento(paciente):
        """Se obtiene y se valida el documento del paciente"""
        documento = getattr(paciente, "documento", None)

        if documento is None or str(documento).strip() == "":
            raise ValueError("El paciente debe tener un documento válido")
        return str(documento).strip()

    def insertar(self, documento, dato):
        """Insertar un paciente en el árbol según su documento"""
        documento = str(documento).strip()

        if documento == "":
            raise ValueError("El documento no puede estar vacío")

        if self._raiz is None:
            self._raiz = _NodoABB(documento, dato)
            self._cantidad += 1
            return

        actual = self._raiz

        while True:
            if documento == actual.documento:
                raise ValueError("Ya existe un paciente con ese documento")

            elif documento < actual.documento:
                if actual.izquierdo is None:
                    actual.izquierdo = _NodoABB(documento, dato)
                    self._cantidad += 1
                    return
                actual = actual.izquierdo

            else:
                if actual.derecho is None:
                    actual.derecho = _NodoABB(documento, dato)
                    self._cantidad += 1
                    return 
                actual = actual.derecho 


    def buscar(self, documento):
        """Busca un paciente por su número de documento, por el contrario, devuelve none si no existe"""
        documento = str(documento)
        actual =self._raiz

        while actual is not None:

            if documento == actual.documento:
                return actual.paciente

            elif documento < actual.documento:
                actual = actual.izquierdo

            else:
                actual = actual.derecho
        return None

    def eliminar(self, documento):
        """Elimina un paciente por documento y devuelve el paciente eliminado"""
        documento = str(documento)

        self._raiz, eliminado = self._eliminar_recursivo(
            self._raiz, documento
        )

        if eliminado is not None:
            self._cantidad -= 1
        return eliminado

    def _eliminar_recursivo(self, nodo, documento):
        """Realiza lla eliminación de un nodo conservando las reglas del ABB"""
        if nodo is None:
            return None, None

        if documento < nodo.documento:
            nodo.izquierdo, eliminado = self._eliminar_recursivo(
                nodo.izquierdo, documento
            )

        elif documento > nodo.documento:
            nodo.derecho, eliminado = self._eliminar_recursivo(
                nodo.derecho, documento 
            )

        else:
            eliminado = nodo.paciente

            #Caso 1 el nodo no tiene hijo izquierdo 
            if nodo.izquierdo is None:
                return nodo.derecho, eliminado 

            #Caso 2 el nodo no tiene hijo derecho
            if nodo.derecho is None:
                return nodo.izquierdo, eliminado

            #Caso 3 el nodo no tiene dos hijos 
            sucesor = self._buscar_minimo(nodo.derecho)

            nodo.documento = sucesor.documento
            nodo.paciente = sucesor.paciente

            nodo.derecho, _ = self._eliminar_recursivo(
                nodo.derecho, sucesor.documento
            )
        return nodo, eliminado 

    @staticmethod
    def _buscar_minimo(nodo):
        """Encuentra el nodo con el documento menor de un subárbol"""

        while nodo.izquierdo is not None:
            nodo = nodo.izquierdo 
        return nodo

    def inorden(self):
        """Devuelve los pacientes ordenados por documento de menor a mayor"""
    
        def recorrer(nodo):
            if nodo is not None:
                yield from recorrer(nodo.izquierdo)
                yield nodo.paciente
                yield from recorrer(nodo.derecho)

        yield from recorrer(self._raiz)

    def preorden(self):
        """Devuelve los pacientes recorriendo primero la raíz"""
        resultado = []

        def recorrer(nodo):
            if nodo is not None:
                resultado.append(nodo.paciente)
                recorrer(nodo.izquierdo)
                recorrer(nodo.derecho)

        recorrer(self._raiz)
        return resultado 

    def postorden(self):
        """Devuelve los pacientes recorriendo primeros los hijos"""
        resultado = []

        def recorrer(nodo):
            if nodo is not None:
                recorrer(nodo.izquierdo)
                recorrer(nodo.derecho)
                resultado.append(nodo.paciente)

        recorrer(self._raiz)
        return resultado

    def por_niveles(self):
        """Genera los pacientes recorriendo el árbol por niveles"""
        if self._raiz is None:
            return

        cola = ColaDinamica()
        cola.encolar(self._raiz)

        while not cola.esta_vacia():
            actual = cola.desencolar()
            yield actual.paciente

            if actual.izquierdo is not None:
                cola.encolar(actual.izquierdo)

            if actual.derecho is not None:
                cola.encolar(actual.derecho)
    
    def altura(self):
        """Devuelve la altura del árbol (un árbol vacío tiene altura 0"""

        def calcular(nodo):
            if nodo is None:
                return 0

            izquierda = calcular(nodo.izquierdo)
            derecha = calcular(nodo.derecho)

            return 1 + max(izquierda, derecha)
        return calcular(self._raiz)

    def construir_balanceado(self, pacientes):
        """Construye un ABB balanceado a partir de una colección de pacientes
        Reemplaza el contenido anterior"""

        pacientes = list(pacientes)

        registros = [
            (self._obtener_documento(paciente), paciente)
            for paciente in pacientes
        ]

        registros.sort(key=lambda registro: registro[0])

        for i in range(1, len(registros)):
            if registros[i][0] == registros[ i - 1][0]:
                raise ValueError("Hay documentos duplicados")

        def construir(inicio, fin):
            if inicio > fin: 
                return None

            medio = (inicio + fin) // 2
            documento, paciente = registros[medio]

            nodo = _NodoABB(documento, paciente)
            nodo.izquierdo = construir(inicio, medio - 1)
            nodo.derecho = construir(medio + 1, fin)
            return nodo

        self._raiz = construir(0, len(registros) -1)
        self._cantidad = len(registros)

    def esta_vacio(self):
        """Indica si el árbol está vacío"""
        return self._raiz is None 

    def __len__(self):
        """Devuelve la catidad de pacientes almacenados"""
=======
from nucleo.cola_dinamica import ColaDinamica
class _NodoABB:
    """Nodo que almacena un paciente y sus referencias de izquierda a derecha."""
    def __init__(self, documento, paciente):
        self.documento = documento
        self.paciente = paciente
        self.izquierdo = None
        self.derecho = None

class ArbolBinarioBusqueda:
    """(ABB) que organiza pacientes utilizando su número de documento como su clave"""
    def __init__(self):
        """Inicializa un árbol vacío"""
        self._raiz = None
        self._cantidad = 0

    @staticmethod
    def _obtener_documento(paciente):
        """Se obtiene y se valida el documento del paciente"""
        documento = getattr(paciente, "documento", None)

        if documento is None or str(documento).strip() == "":
            raise ValueError("El paciente debe tener un documento válido")
        return str(documento).strip()

    @staticmethod
    def _clave_documento(documento):
        documento = str(documento).strip()

        if not documento.isdigit():
            raise ValueError("El documento debe contener solo números")
        return int(documento)

    def insertar(self, documento, dato):
        """Insertar un paciente en el árbol según su documento"""
        documento = str(documento).strip()

        clave = self._clave_documento(documento)

        if self._raiz is None:
            self._raiz = _NodoABB(documento, dato)
            self._cantidad += 1
            return

        actual = self._raiz

        while True:
            clave_actual = self._clave_documento(actual.documento)
            if clave == clave_actual:
                raise ValueError("Ya existe un paciente con ese documento")
            
            elif clave < clave_actual:
                if actual.izquierdo is None:
                    actual.izquierdo = _NodoABB(documento, dato)
                    self._cantidad += 1
                    return
                actual = actual.izquierdo 

            else:
                if actual.derecho is None:
                    actual.derecho = _NodoABB(documento, dato)
                    self._cantidad += 1
                    return
                actual = actual.derecho


    def buscar(self, documento):
        """Busca un paciente por su número de documento, por el contrario, devuelve none si no existe"""
        
        clave = self._clave_documento(documento)
        actual =self._raiz

        while actual is not None:
            clave_actual = int(actual.documento)

            if clave == clave_actual:
                return actual.paciente

            elif clave < clave_actual:
                actual = actual.izquierdo

            else:
                actual = actual.derecho
        return None

    def eliminar(self, documento):
        """Elimina un paciente por documento y devuelve el paciente eliminado"""
        documento = self._clave_documento(documento)

        self._raiz, eliminado = self._eliminar_recursivo(
            self._raiz, documento
        )

        if eliminado is not None:
            self._cantidad -= 1
        return eliminado

    def _eliminar_recursivo(self, nodo, documento):
        """Realiza lla eliminación de un nodo conservando las reglas del ABB"""
        if nodo is None:
            return None, None

        clave = int(documento)
        clave_nodo = int(nodo.documento)


        if clave < clave_nodo:
            nodo.izquierdo, eliminado = self._eliminar_recursivo(
                nodo.izquierdo, documento
            )

        elif clave > clave_nodo:
            nodo.derecho, eliminado = self._eliminar_recursivo(
                nodo.derecho, documento 
            )

        else:
            eliminado = nodo.paciente

            #Caso 1 el nodo no tiene hijo izquierdo 
            if nodo.izquierdo is None:
                return nodo.derecho, eliminado 

            #Caso 2 el nodo no tiene hijo derecho
            if nodo.derecho is None:
                return nodo.izquierdo, eliminado

            #Caso 3 el nodo no tiene dos hijos 
            sucesor = self._buscar_minimo(nodo.derecho)

            nodo.documento = sucesor.documento
            nodo.paciente = sucesor.paciente

            nodo.derecho, _ = self._eliminar_recursivo(
                nodo.derecho, sucesor.documento
            )
        return nodo, eliminado 

    @staticmethod
    def _buscar_minimo(nodo):
        """Encuentra el nodo con el documento menor de un subárbol"""

        while nodo.izquierdo is not None:
            nodo = nodo.izquierdo 
        return nodo

    def inorden(self):
        """Devuelve los pacientes ordenados por documento de menor a mayor"""

        pila = []
        actual = self._raiz

        while actual is not None or pila:

            while actual is not None:
                pila.append(actual)
                actual = actual.izquierdo

            actual = pila.pop()
            yield actual.paciente
            actual = actual.derecho

    def preorden(self):
        """Devuelve los pacientes recorriendo primero la raíz"""
        resultado = []

        if self._raiz is None:
            return resultado

        pila = [self._raiz]

        while pila:
            actual = pila.pop()
            resultado.append(actual.paciente)

            if actual.derecho is not None:
                pila.append(actual.derecho)

            if actual.izquierdo is not None:
                pila.append(actual.izquierdo)

        return resultado

    def postorden(self):
        """Devuelve los pacientes recorriendo primeros los hijos"""
        resultado = []

        if self._raiz is None:
            return resultado

        pila = [(self._raiz, False)]

        while pila:
            actual, visitado = pila.pop()

            if visitado:
                resultado.append(actual.paciente)
            else:
                pila.append((actual, True))

                if actual.derecho is not None:
                    pila.append((actual.derecho, False))

                if actual.izquierdo is not None:
                    pila.append((actual.izquierdo, False))

        return resultado 

    def por_niveles(self):
        """Genera los pacientes recorriendo el árbol por niveles"""
        if self._raiz is None:
            return

        cola = ColaDinamica()
        cola.encolar(self._raiz)

        while not cola.esta_vacia():
            actual = cola.desencolar()
            yield actual.paciente

            if actual.izquierdo is not None:
                cola.encolar(actual.izquierdo)

            if actual.derecho is not None:
                cola.encolar(actual.derecho)
    
    def altura(self):
        """Devuelve la altura del árbol (un árbol vacío tiene altura 0"""

        if self._raiz is None:
            return 0

        altura = 0
        cola = ColaDinamica()
        cola.encolar(self._raiz)

        while not cola.esta_vacia():
            cantidad_nivel = 0

            nivel = []

            while not cola.esta_vacia():
                nivel.append(cola.desencolar())

            cantidad_nivel = len(nivel)
            altura += 1

            for nodo in nivel:
                if nodo.izquierdo is not None:
                    cola.encolar(nodo.izquierdo)

                if nodo.derecho is not None:
                    cola.encolar(nodo.derecho)

        return altura

    def construir_balanceado(self, pacientes):
        """Construye un ABB balanceado a partir de una colección de pacientes
        Reemplaza el contenido anterior"""

        pacientes = list(pacientes)

        registros = [
            (self._obtener_documento(paciente), paciente)
            for paciente in pacientes
        ]

        registros.sort(key=lambda registro: int(registro[0]))

        for i in range(1, len(registros)):
            if int(registros[i][0] == registros[ i - 1][0]):
                raise ValueError("Hay documentos duplicados")

        def construir(inicio, fin):
            if inicio > fin: 
                return None

            medio = (inicio + fin) // 2
            documento, paciente = registros[medio]

            nodo = _NodoABB(documento, paciente)
            nodo.izquierdo = construir(inicio, medio - 1)
            nodo.derecho = construir(medio + 1, fin)
            return nodo

        self._raiz = construir(0, len(registros) -1)
        self._cantidad = len(registros)

    def esta_vacio(self):
        """Indica si el árbol está vacío"""
        return self._raiz is None 

    def __len__(self):
        """Devuelve la catidad de pacientes almacenados"""
>>>>>>> 86509df (Corregir ABB: comparacion numerica y recorridos iterativos)
        return self._cantidad