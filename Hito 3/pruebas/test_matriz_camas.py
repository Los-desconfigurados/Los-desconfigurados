import pytest
 
from nucleo.matriz_camas import MatrizCamas, crear_matriz
 
@pytest.fixture
def matriz():
    return MatrizCamas(n_turnos=3, n_camas=4)

class TestConstruccion:
    def test_dimensiones_y_estado_inicial(self, matriz):
        assert matriz.n_turnos == 3
        assert matriz.n_camas == 4
        for turno in range(3):
            assert matriz.ocupacion(turno) == 0
 
    @pytest.mark.parametrize("turnos, camas", [(0, 4), (3, 0), (-1, 4), (3, -2), (0, 0)])
    def test_dimensiones_invalidas(self, turnos, camas):
        with pytest.raises(ValueError):
            MatrizCamas(turnos, camas)
 
    def test_crear_matriz_devuelve_matriz_camas(self):
        m = crear_matriz(2, 5)
        assert isinstance(m, MatrizCamas)
        assert (m.n_turnos, m.n_camas) == (2, 5)
 
    def test_repr_es_la_matriz_interna(self):
        m = MatrizCamas(2, 2)
        assert repr(m) == "[[0, 0], [0, 0]]"
        m.asignar(1, 0)
        assert repr(m) == "[[0, 1], [0, 0]]"
 

class TestAsignar:
    def test_asignar_ocupa_la_cama(self, matriz):
        matriz.asignar(2, 1)
        assert matriz.ocupacion(1) == 1
        assert 2 not in matriz.consultar_disponibilidad(1)
 
    def test_asignar_cama_ocupada_lanza_valueerror(self, matriz):
        matriz.asignar(0, 0)
        with pytest.raises(ValueError):
            matriz.asignar(0, 0)
 
    def test_doble_asignacion_no_altera_el_estado(self, matriz):
        matriz.asignar(0, 0)
        with pytest.raises(ValueError):
            matriz.asignar(0, 0)
        assert matriz.ocupacion(0) == 1
 
    def test_misma_cama_en_otro_turno_es_independiente(self, matriz):
        matriz.asignar(0, 0)
        matriz.asignar(0, 1)  # no debe fallar
        assert matriz.ocupacion(0) == 1
        assert matriz.ocupacion(1) == 1
        assert matriz.ocupacion(2) == 0
 
    def test_llenar_todas_las_camas_de_un_turno(self, matriz):
        for cama in range(matriz.n_camas):
            matriz.asignar(cama, 0)
        assert matriz.ocupacion(0) == matriz.n_camas
        assert matriz.consultar_disponibilidad(0) == []
        # con el turno lleno, cualquier asignacion adicional falla
        with pytest.raises(ValueError):
            matriz.asignar(0, 0)

class TestLiberar:
    def test_liberar_deja_la_cama_libre(self, matriz):
        matriz.asignar(1, 2)
        matriz.liberar(1, 2)
        assert matriz.ocupacion(2) == 0
        assert 1 in matriz.consultar_disponibilidad(2)
 
    def test_liberar_cama_libre_lanza_valueerror(self, matriz):
        with pytest.raises(ValueError):
            matriz.liberar(0, 0)
 
    def test_doble_liberacion_lanza_valueerror(self, matriz):
        matriz.asignar(0, 0)
        matriz.liberar(0, 0)
        with pytest.raises(ValueError):
            matriz.liberar(0, 0)
 
    def test_liberar_solo_afecta_su_turno(self, matriz):
        matriz.asignar(0, 0)
        matriz.asignar(0, 1)
        matriz.liberar(0, 0)
        assert matriz.ocupacion(0) == 0
        assert matriz.ocupacion(1) == 1
 
    def test_se_puede_reasignar_tras_liberar(self, matriz):
        matriz.asignar(3, 0)
        matriz.liberar(3, 0)
        matriz.asignar(3, 0)
        assert matriz.ocupacion(0) == 1
 
 
class TestValidacion:
    @pytest.mark.parametrize("cama, turno", [(0, -1), (0, 3), (0, 99)])
    def test_turno_fuera_de_rango(self, matriz, cama, turno):
        with pytest.raises(IndexError):
            matriz.asignar(cama, turno)
        with pytest.raises(IndexError):
            matriz.liberar(cama, turno)
 
    @pytest.mark.parametrize("cama, turno", [(-1, 0), (4, 0), (99, 0)])
    def test_cama_fuera_de_rango(self, matriz, cama, turno):
        with pytest.raises(IndexError):
            matriz.asignar(cama, turno)
        with pytest.raises(IndexError):
            matriz.liberar(cama, turno)
 
    @pytest.mark.parametrize("malo", [1.5, "1", None, [0]])
    def test_turno_de_tipo_invalido(self, matriz, malo):
        with pytest.raises(TypeError):
            matriz.asignar(0, malo)
        with pytest.raises(TypeError):
            matriz.ocupacion(malo)
        with pytest.raises(TypeError):
            matriz.consultar_disponibilidad(malo)
 
    @pytest.mark.parametrize("malo", [1.5, "1", None, [0]])
    def test_cama_de_tipo_invalido(self, matriz, malo):
        with pytest.raises(TypeError):
            matriz.asignar(malo, 0)
        with pytest.raises(TypeError):
            matriz.liberar(malo, 0)
 
    def test_ocupacion_turno_fuera_de_rango(self, matriz):
        with pytest.raises(IndexError):
            matriz.ocupacion(3)
        with pytest.raises(IndexError):
            matriz.ocupacion(-1)
 
    def test_disponibilidad_turno_fuera_de_rango(self, matriz):
        with pytest.raises(IndexError):
            matriz.consultar_disponibilidad(3)

class TestConsultas:
    def test_ocupacion_cuenta_las_asignadas(self, matriz):
        matriz.asignar(0, 0)
        matriz.asignar(2, 0)
        assert matriz.ocupacion(0) == 2
 
    def test_disponibilidad_devuelve_indices_libres_en_orden(self, matriz):
        matriz.asignar(1, 0)
        matriz.asignar(3, 0)
        assert matriz.consultar_disponibilidad(0) == [0, 2]
 
    def test_disponibilidad_turno_vacio(self, matriz):
        assert matriz.consultar_disponibilidad(1) == [0, 1, 2, 3]
 
    def test_reporte_ocupacion_inicial(self, matriz):
        reporte = matriz.reporte_ocupacion()
        assert len(reporte) == matriz.n_turnos
        for turno, fila in enumerate(reporte):
            assert fila == {"turno": turno, "ocupadas": 0, "libres": 4, "total": 4}
 
    def test_reporte_ocupacion_con_asignaciones(self, matriz):
        matriz.asignar(0, 0)
        matriz.asignar(1, 0)
        matriz.asignar(0, 2)
        reporte = matriz.reporte_ocupacion()
        assert reporte[0] == {"turno": 0, "ocupadas": 2, "libres": 2, "total": 4}
        assert reporte[1] == {"turno": 1, "ocupadas": 0, "libres": 4, "total": 4}
        assert reporte[2] == {"turno": 2, "ocupadas": 1, "libres": 3, "total": 4}
 
    def test_ocupadas_mas_libres_siempre_es_el_total(self, matriz):
        matriz.asignar(0, 1)
        matriz.asignar(3, 1)
        matriz.liberar(0, 1)
        for fila in matriz.reporte_ocupacion():
            assert fila["ocupadas"] + fila["libres"] == fila["total"]
 
