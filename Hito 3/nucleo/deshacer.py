"""Gestión de acciones reversibles mediante una pila dinámica"""
from nucleo.pila_dinamica import PilaDinamica,  PilaVacia

class GestorDeshacer:
    """Registra y ejecuta acciones inversas en orden LIFO"""
    def __init__(self):
        """Inicializa la pila de acciones inversas"""
        self._acciones = PilaDinamica()

    def registrar(self, accion):
        """
        Registra una acción inversa.
        La acción debe ser una funcióon ejecutable o un objeto
        que implemente el método ejecutar()
        """
        if not callable(accion) and not callable(getattr(accion, "ejecutar", None)):
            raise TypeError("La acción debe ser ejecutable o tener un método ejecutar()")
        self._acciones.push(accion)

    def deshacer(self):
        """
        Extrae y ejecuta la última acción registrada.
        Devuelve el resultado de la acción, si lo hay. Ejecuta
        PilaVacia cuando no hay acciones pendientes
        """

        accion = self._acciones.pop()

        if callable(accion):
            return accion()
        return accion.ejecutar()

    def esta_vacio(self):
        """Indica si no quedan acciones por deshacer"""
        return self._acciones.esta_vacia()

    def __len__(self):
        """Devuelve la cantidad de acciones pendientes"""
        return len(self._acciones)