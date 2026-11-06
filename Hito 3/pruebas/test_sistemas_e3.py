import unittest
from puente import (crear_sistema, romano, a_dict, refrescar, en_espera, en_atencion,
                    siguiente, conteo_por_nivel, vencidos, camillas, hay_que_deshacer,
                    ingresar, llamar_siguiente, reclasificar, dar_alta, deshacer, registrar_signos,)

from nucleo.dominio import Nivel

class TestPuenteSistema(unittest.TestCase):
    def setUp(self):
        """Cada prueba comienza con un sistema nuevo"""
        self.sistema = crear_sistema()

    def ingresar_paciente(self, nombre="Paciente Prueba", doc="1001", edad=25, motivo="Dolor abdominal", 
                          nivel="III", extras=None,):
        return ingresar(self.sistema, nombre, doc, edad, motivo, nivel, extras,)

    def test_crear_sistema(self):
        self.assertIsNotNone(self.sistema)
        self.assertEqual(self.sistema.extras, {})
        self.assertEqual(self.sistema.altas, [])
        self.assertEqual(self.sistema.efectos, [])
        self.assertIsNone(self.sistema.paciente_en_atencion)

    def test_romano_convierte_todos_los_niveles(self):
        esperados = {
            1: "I",
            2: "II",
            3: "III",
            4: "IV",
            5: "V",
        }
        for numero, romano_esperado in esperados.items():
            with self.subTest(numero=numero):
                self.assertEqual(romano(numero), romano_esperado)

    def test_romano_acepta_enum_nivel(self):
        self.assertEqual(romano(Nivel.III), "III")

    def test_ingresar_paciente(self):
        paciente = self.ingresar_paciente()

        self.assertIsNotNone(paciente)
        self.assertEqual(paciente.nombre, "Paciente Prueba")
        self.assertEqual(paciente.documento, "1001")
        self.assertEqual(paciente.edad, 25)
        self.assertEqual(paciente.motivo, "Dolor abdominal")
        self.assertEqual(paciente.nivel, Nivel.III)

    def test_ingresar_guarda_extras(self):
        extras = {
            "alergias": "Penicilina",
            "observaciones": "Paciente consciente",
        }
        self.ingresar_paciente(extras=extras)
        self.assertIn("1001", self.sistema.extras)
        self.assertEqual(self.sistema.extras["1001"]["alergias"], "Penicilina",)
        self.assertEqual(self.sistema.extras["1001"]["observaciones"], "Paciente consciente",)
        self.assertEqual(self.sistema.extras["1001"]["reclasificaciones"], [],)

    def test_a_dict_devuelve_datos_del_paciente(self):
        self.ingresar_paciente(
            extras={"alergias": "Ninguna"}
        )

        paciente = self.sistema.registro.obtener("1001")
        resultado = a_dict(self.sistema, paciente)

        campos = [
            "nombre", "doc", "nivel", "espera", "motivo", "edad", "alergias",
        ]

        for campo in campos:
            self.assertIn(campo, resultado)

        self.assertEqual(resultado["nombre"], "Paciente Prueba")
        self.assertEqual(resultado["doc"], "1001")
        self.assertEqual(resultado["nivel"], "III")
        self.assertEqual(resultado["edad"], 25)
        self.assertEqual(resultado["alergias"], "Ninguna")
        self.assertGreaterEqual(resultado["espera"], 0)


    def test_en_espera_devuelve_pacientes(self):
        self.ingresar_paciente()

        pacientes = en_espera(self.sistema)

        self.assertEqual(len(pacientes), 1)
        self.assertEqual(pacientes[0]["doc"], "1001")

    def test_en_espera_filtra_por_nivel(self):
        self.ingresar_paciente(nombre="Paciente Uno", doc="1001", nivel="I",)

        self.ingresar_paciente(nombre="Paciente Dos", doc="1002", nivel="V",
        )

        pacientes = en_espera(self.sistema, Nivel.I)

        self.assertEqual(len(pacientes), 1)
        self.assertEqual(pacientes[0]["doc"], "1001")
        self.assertEqual(pacientes[0]["nivel"], "I")

    def test_siguiente_devuelve_el_primer_paciente(self):
        self.ingresar_paciente()

        paciente = siguiente(self.sistema)

        self.assertIsNotNone(paciente)
        self.assertEqual(paciente["doc"], "1001")

    def test_siguiente_devuelve_none_si_no_hay_pacientes(self):
        self.assertIsNone(siguiente(self.sistema))

    def test_conteo_por_nivel_devuelve_diccionario(self):
        self.ingresar_paciente(nivel="I")
        self.ingresar_paciente(nombre="Paciente Dos", doc="1002", nivel="III",)

        conteos = conteo_por_nivel(self.sistema)

        self.assertIsInstance(conteos, dict)
        self.assertEqual(conteos.get("I"), 1)
        self.assertEqual(conteos.get("III"), 1)

    def test_vencidos_devuelve_cantidad(self):
        resultado = vencidos(self.sistema)

        self.assertIsInstance(resultado, int)
        self.assertGreaterEqual(resultado, 0)

    def test_refrescar_ejecuta_actualizacion(self):
        resultado = refrescar(self.sistema)
        self.assertIsNone(resultado)

    def test_en_atencion_inicialmente_es_none(self):
        self.assertIsNone(en_atencion(self.sistema))

    def test_llamar_siguiente_paciente(self):
        self.ingresar_paciente()

        resultado = llamar_siguiente(self.sistema)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["doc"], "1001")
        self.assertEqual(self.sistema.paciente_en_atencion.documento,"1001",)

    def test_en_atencion_devuelve_paciente_llamado(self):
        self.ingresar_paciente()
        llamar_siguiente(self.sistema)

        paciente = en_atencion(self.sistema)

        self.assertIsNotNone(paciente)
        self.assertEqual(paciente["doc"], "1001")

    def test_no_llama_otro_paciente_si_ya_hay_uno_en_atencion(self):
        self.ingresar_paciente(nombre="Paciente Uno",doc="1001",)

        self.ingresar_paciente(nombre="Paciente Dos", doc="1002",)

        primero = llamar_siguiente(self.sistema)
        segundo = llamar_siguiente(self.sistema)

        self.assertIsNotNone(primero)
        self.assertIsNone(segundo)
        self.assertEqual(self.sistema.paciente_en_atencion.documento,"1001",)

    def test_reclasificar_paciente(self):
        self.ingresar_paciente(nivel="III")

        resultado = reclasificar(self.sistema,"1001","I","Empeoramiento de los síntomas","10:30",)

        self.assertTrue(resultado)
        paciente = self.sistema.registro.obtener("1001")
        self.assertEqual(romano(paciente.nivel), "I")

        historial = self.sistema.extras["1001"]["reclasificaciones"]

        self.assertEqual(len(historial), 1)
        self.assertEqual(historial[0]["de"], "III")
        self.assertEqual(historial[0]["a"], "I")
        self.assertEqual(historial[0]["justificacion"],"Empeoramiento de los síntomas",)
        self.assertEqual(historial[0]["hora"], "10:30")

    def test_reclasificar_documento_inexistente(self):
        resultado = reclasificar(self.sistema,"9999","I","Justificación","10:30",)
        self.assertFalse(resultado)

    def test_dar_alta_paciente(self):
        self.ingresar_paciente()

        resultado = dar_alta(self.sistema,"1001","Médica","Mejoría del paciente",)

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["doc"], "1001")
        self.assertEqual(resultado["tipo"], "Médica")
        self.assertEqual(resultado["motivo_alta"],"Mejoría del paciente",)
        self.assertEqual(len(self.sistema.altas), 1)

    def test_hay_que_deshacer_inicialmente_es_false(self):
        self.assertFalse(hay_que_deshacer(self.sistema))

    def test_hay_que_deshacer_es_true_despues_de_ingresar(self):
        self.ingresar_paciente()
        self.assertTrue(hay_que_deshacer(self.sistema))

    def test_deshacer_ingreso(self):
        self.ingresar_paciente()

        resultado = deshacer(self.sistema)

        self.assertIsNotNone(resultado)
        self.assertIsNone(self.sistema.registro.obtener("1001"))
        self.assertNotIn("1001", self.sistema.extras)
        self.assertEqual(len(en_espera(self.sistema)), 0)

    def test_deshacer_llamado(self):
        self.ingresar_paciente()
        llamar_siguiente(self.sistema)

        resultado = deshacer(self.sistema)

        self.assertIsNotNone(resultado)
        self.assertIsNone(self.sistema.paciente_en_atencion)
        self.assertEqual(len(en_espera(self.sistema)), 1)

    def test_deshacer_alta(self):
        self.ingresar_paciente()

        dar_alta(self.sistema,"1001","Médica","Mejoría",)
        self.assertEqual(len(self.sistema.altas), 1)

        resultado = deshacer(self.sistema)

        self.assertIsNotNone(resultado)
        self.assertEqual(len(self.sistema.altas), 0)
        self.assertIsNotNone(self.sistema.registro.obtener("1001"))

    def test_deshacer_sin_acciones_devuelve_none(self):
        resultado = deshacer(self.sistema)
        self.assertIsNone(resultado)

    def test_camillas_devuelve_ocupacion_y_capacidad(self):
        self.ingresar_paciente()
        ocupadas, total = camillas(self.sistema)

        self.assertEqual(ocupadas, 1)
        self.assertEqual(total, 10)

    def test_camillas_sin_pacientes(self):
        ocupadas, total = camillas(self.sistema)

        self.assertEqual(ocupadas, 0)
        self.assertEqual(total, 10)

    def test_registrar_signos_paciente_existente(self):
        self.ingresar_paciente()

        resultado = registrar_signos(self.sistema,"1001", 80, 18, 36.5, 98.0,)
        self.assertIsNone(resultado)

    def test_registrar_signos_documento_inexistente(self):
        # La fachada captura KeyError para documentos inexistentes.
        resultado = registrar_signos(self.sistema, "9999", 80, 18, 36.5, 98.0, )
        self.assertIsNone(resultado)
        

if __name__ == "__main__":
    unittest.main(verbosity=2)
