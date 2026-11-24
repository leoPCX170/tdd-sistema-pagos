import unittest
from unittest.mock import MagicMock
from servicio_pagos import Orden, ServicioPagos


class TestServicioPagos(unittest.TestCase):
    def setUp(self):
        self.repo_mock = MagicMock()
        self.pasarela_mock = MagicMock()
        self.servicio = ServicioPagos(self.repo_mock, self.pasarela_mock)

    def test_pago_exitoso_actualiza_orden_a_pagada(self):
        orden = Orden(id="ORD-1", monto=250.0, token_pago="tok_abc")
        self.repo_mock.obtener_orden.return_value = orden
        self.pasarela_mock.cobrar.return_value = True

        estado = self.servicio.procesar_pago("ORD-1")

        self.assertEqual(estado, "PAGADA")
        self.assertEqual(orden.estado, "PAGADA")
        self.pasarela_mock.cobrar.assert_called_once_with(250.0, "tok_abc")
        self.repo_mock.guardar_orden.assert_called_once_with(orden)

    def test_orden_inexistente_lanza_error_y_no_cobra(self):
        self.repo_mock.obtener_orden.return_value = None

        with self.assertRaises(ValueError):
            self.servicio.procesar_pago("ORD-999")

        self.pasarela_mock.cobrar.assert_not_called()
        self.repo_mock.guardar_orden.assert_not_called()

    def test_pago_rechazado_marca_orden_como_fallida(self):
        orden = Orden(id="ORD-2", monto=100.0, token_pago="tok_rechazado")
        self.repo_mock.obtener_orden.return_value = orden
        self.pasarela_mock.cobrar.return_value = False

        estado = self.servicio.procesar_pago("ORD-2")

        self.assertEqual(estado, "FALLIDA")
        self.assertEqual(orden.estado, "FALLIDA")
        self.repo_mock.guardar_orden.assert_called_once_with(orden)


if __name__ == "__main__":
    unittest.main()

def test_regresion_recargo_cinco_porciento_mayor_a_mil(self):
        orden = Orden(id="ORD-3", monto=1200.0, token_pago="tok_alto")
        self.repo_mock.obtener_orden.return_value = orden
        self.pasarela_mock.cobrar.return_value = True

        estado = self.servicio.procesar_pago("ORD-3")

        self.assertEqual(estado, "PAGADA")
        self.pasarela_mock.cobrar.assert_called_once_with(1260.0, "tok_alto")
        self.repo_mock.guardar_orden.assert_called_once_with(orden)