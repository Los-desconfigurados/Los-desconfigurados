import random
import pytest
from nucleo.abb import ArbolBinarioBusqueda
from nucleo.dominio_v2 import Paciente
 
def P(documento):
    return Paciente(f"Paciente {documento}", str(documento), 30, "motivo")
 
def docs(pacientes):
    return [p.documento for p in pacientes]
 
def arbol_con(documentos):
    a = ArbolBinarioBusqueda()
    for d in documentos:
        a.insertar(d, P(d))
    return a
 
def arbol_conocido():
    return arbol_con([50, 30, 70, 20, 40, 60, 80])
 
def test_arbol_vacio():
    a = ArbolBinarioBusqueda()
    assert len(a) == 0 and a.esta_vacio() and a.altura() == 0
    assert a.buscar("123") is None and a.eliminar("123") is None
    assert list(a.inorden()) == [] and list(a.por_niveles()) == []
    assert a.preorden() == [] and a.postorden() == []
 
def test_insertar_y_buscar():
    a = ArbolBinarioBusqueda()
    paciente = P(123)
    a.insertar("123", paciente)
    a.insertar(456, P(456))              
    a.insertar(" 789 ", P(789))          
    assert a.buscar("123") is paciente
    assert a.buscar(456) is not None and a.buscar("789") is not None
    assert a.buscar("999") is None
    assert len(a) == 3
 
 
def test_rechaza_duplicados_y_documentos_invalidos():
    a = arbol_conocido()
    for malo in ("50", "", "   ", "abc", "12a", "-5", "1.5"):
        with pytest.raises(ValueError):
            a.insertar(malo, P(1))
    assert len(a) == 7                
 
def test_el_orden_es_numerico_y_no_alfabetico():
    assert docs(arbol_con(["9", "10", "100", "2", "33"]).inorden()) == ["2", "9", "10", "33", "100"]
 
def test_recorridos_y_altura():
    a = arbol_conocido()
    assert docs(a.inorden()) == ["20", "30", "40", "50", "60", "70", "80"]
    assert docs(a.preorden()) == ["50", "30", "20", "40", "70", "60", "80"]
    assert docs(a.postorden()) == ["20", "40", "30", "60", "80", "70", "50"]
    assert docs(a.por_niveles()) == ["50", "30", "70", "20", "40", "60", "80"]
    assert a.altura() == 3
    assert arbol_con(range(1, 101)).altura() == 100      
 
def test_eliminar_hoja_un_hijo_y_documento_inexistente():
    a = arbol_conocido()
    paciente = a.buscar("80")
    assert a.eliminar("80") is paciente                  
    assert a.eliminar("999") is None                     
    assert docs(a.preorden()) == ["50", "30", "20", "40", "70", "60"]
    assert len(a) == 6
 
    izq = arbol_con([50, 30, 70, 20])
    izq.eliminar("30")                                  
    assert docs(izq.preorden()) == ["50", "20", "70"]
 
    der = arbol_con([50, 30, 70, 40])
    der.eliminar("30")                                   
    assert docs(der.preorden()) == ["50", "40", "70"]
 
 
def test_eliminar_con_dos_hijos_usa_el_sucesor_inorden():
    a = arbol_conocido()
    a.eliminar("30")                                     
    assert docs(a.preorden()) == ["50", "40", "20", "70", "60", "80"]
 
    b = arbol_conocido()
    b.eliminar("50")                                     
    assert docs(b.preorden()) == ["60", "30", "20", "40", "70", "80"]
    assert docs(b.inorden()) == ["20", "30", "40", "60", "70", "80"]
 
def test_eliminar_al_azar_conserva_el_orden():
    azar = random.Random(7)
    todos = azar.sample(range(1000, 100000), 300)
    a = arbol_con(todos)
 
    borrados = azar.sample(todos, 150)
    for d in borrados:
        assert a.eliminar(str(d)) is not None
 
    restantes = sorted(set(todos) - set(borrados))
    assert [int(d) for d in docs(a.inorden())] == restantes
    assert len(a) == len(restantes)
    assert all(a.buscar(str(d)) is None for d in borrados)
 
def test_construir_balanceado():
    a = arbol_con([1, 2, 3])
    a.construir_balanceado(P(d) for d in (70, 20, 50, 80, 30, 60, 40))   # reemplaza, desordenado
    assert docs(a.inorden()) == ["20", "30", "40", "50", "60", "70", "80"]
    assert docs(a.preorden())[0] == "50" and a.altura() == 3 and len(a) == 7
 
    a.construir_balanceado(P(d) for d in ("100", "9", "33", "2", "10"))  # orden numerico
    assert docs(a.inorden()) == ["2", "9", "10", "33", "100"]
 
    for n, altura in ((1, 1), (1023, 10), (5000, 13)):
        b = ArbolBinarioBusqueda()
        b.construir_balanceado([P(1000 + i) for i in range(n)])
        assert b.altura() == altura and len(b) == n
 
    with pytest.raises(ValueError):                      
        a.construir_balanceado([P(5), P(5)])
    with pytest.raises(ValueError):                     
        a.construir_balanceado([P(5), P("")])
    assert docs(a.inorden()) == ["2", "9", "10", "33", "100"]   
 
def test_peor_caso_1500_documentos_ordenados():   
    n = 1500
    a = arbol_con(range(1000000001, 1000000001 + n))
    assert len(a) == n and a.altura() == n
    assert a.buscar(str(1000000001 + n - 1)) is not None
    assert len(list(a.inorden())) == len(a.preorden()) == len(a.postorden()) == n
    assert len(list(a.por_niveles())) == n
 
@pytest.mark.xfail(raises=RecursionError)
def test_eliminar_el_nodo_mas_profundo_de_un_arbol_degenerado():
    n = 1500
    a = arbol_con(range(1000000001, 1000000001 + n))
    assert a.eliminar(str(1000000001 + n - 1)) is not None
    assert len(a) == n - 1
 
def test_inorden_coincide_con_el_censo_ordenado():
    azar = random.Random(2026)
    censo = [str(d) for d in azar.sample(range(1000000000, 10000000000), 5000)]
    ordenado = sorted(censo, key=int)
 
    a = arbol_con(censo)
    assert docs(a.inorden()) == ordenado
    assert all(a.buscar(d) is not None for d in censo)
 
    b = ArbolBinarioBusqueda()
    b.construir_balanceado([P(d) for d in censo])
    assert docs(b.inorden()) == ordenado