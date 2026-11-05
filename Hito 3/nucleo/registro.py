from nucleo.lista_doble import ListaDoble
from nucleo.lista_simple import ListaSimple


class RegistroPacientes:

    def __init__(self):
        self._lista = ListaDoble()
        self._indice = {}
        self._historiales = {}

    def __len__(self):
       return len(self._lista)

    def ingresar(self, paciente):
       
        if paciente.id in self._indice:
            raise ValueError(f"Ya existe un paciente con ID {paciente.id}")

        nodo = self._lista.insertar_final(paciente)

        self._indice[paciente.id] = nodo
        self._historiales[paciente.id] = ListaSimple()

        return nodo

    def dar_salida(self, id, motivo=None):
        nodo = self._indice.get(id)

        if nodo is None:
            raise KeyError(f"No hay un paciente activo con ID {id}")

        paciente = self._lista.eliminar(nodo)
        del self._indice[id]

        return paciente

    def obtener(self, id):
        nodo = self._indice.get(id)

        if nodo is None:
            return None

        return nodo.dato

    def buscar(self, predicado):
        nodo = self._lista.buscar(predicado)

        if nodo is None:
            return None

        return nodo.dato

    def listar(self):
        return self._lista.recorrer_adelante()

    def registrar_signos(self, id, signos):
        if id not in self._indice:
            raise KeyError(f"No hay un paciente activo con ID {id}")

        self._historiales[id].agregar_final(signos)

    def historial(self, id):
        if id not in self._historiales:
            raise KeyError(f"No existe un historial para el paciente {id}")

        return iter(self._historiales[id])

    def reubicar_antes(self, id, id_referencia):
        nodo = self._indice.get(id)
        referencia = self._indice.get(id_referencia)

        if nodo is None or referencia is None:
            raise KeyError("Alguno de los pacientes no esta activo")

        if nodo is referencia or nodo.siguiente is referencia:
            return nodo

        paciente = self._lista.eliminar(nodo)
        self._indice[id] = self._lista.insertar_antes(referencia, paciente)

        return self._indice[id]
