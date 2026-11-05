class MatrizCamas:
    def __init__(self, n_turnos, n_camas):
        """
        Administra la disponibilidad de camas por turnos.
        - Filas: turno.
        - Columnas: camas.
        """
        if n_turnos <= 0 or n_camas <= 0:
            raise ValueError("El numero de turnos y camas deben ser mayores que 0")
            
        self.n_turnos = n_turnos
        self.n_camas = n_camas
        self._matriz = [[0 for _ in range(n_camas)] for _ in range(n_turnos)]

    def _validar_turno(self, turno):
        if not isinstance(turno, int):
            raise TypeError("El turno debe ser un entero")

        if turno < 0 or turno >= self.n_turnos:
            raise IndexError("Turno fuera del limite")

    def _validar_cama(self, cama):
        if not isinstance(cama, int):
            raise TypeError("La Cama debe ser un entero")

        if cama< 0 or cama >= self.n_camas:
            raise IndexError("Cama fuera del limite")
        
    def asignar(self, cama, turno):
        """Asigna una cama a un turno"""
        self._validar_turno(turno)
        self._validar_cama(cama)

        if self._matriz[turno][cama] == 1:
            raise ValueError(f"La cama {cama} ya se encunentra ocupada en el turno {turno}")
        self._matriz[turno][cama] = 1

    def liberar(self, cama, turno):
        """
        Libera una cama en un turno determinado.
        Usa los condicionales de la funcion _validar_indices con los paramnetros:
        - Cama: indice de la cama.
        - Turno: indice del turno.
        """
        self._validar_turno(turno)
        self._validar_cama(cama)

        if self._matriz[turno][cama] == 0:
            raise ValueError(f"La cama {cama} ya se encuentra libre en el turno {turno}")
        self._matriz[turno][cama] = 0

    def ocupacion(self, turno):
        """Devuelve la cantidad de camas ocupadas en un turno"""
        self._validar_turno(turno)
        return sum(self._matriz[turno])

    def consultar_disponibilidad(self, turno):
        """
        Devuelve una lista con los indices de la cama libres en el turno indicado.
        """
        self._validar_turno(turno)

        return [
            cama
            for cama in range(self.n_camas)
            if self._matriz[turno][cama] == 0
        ]

    def reporte_ocupacion(self):
        """
       Genera un reporte de ocupación por turno
        """
        return [
            {
                "turno": turno, 
                "ocupadas": self.ocupacion(turno), 
                "libres": self.n_camas - self.ocupacion(turno),
                "total": self.n_camas
            }
            for turno in range(self.n_turnos)
        ]

    def __repr__(self):
        """Representación de la matriz"""
        return repr(self._matriz)

def crear_matriz(n_turnos, n_camas):
    """ 
    Crea y devuelve una matriz de camas 
    """
    return MatrizCamas(n_turnos, n_camas)
