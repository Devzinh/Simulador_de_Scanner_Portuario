import unittest

from motor import _clamp as clamp_motor, gerar_conteiner
from dados import _digito_verificador
from save import _sanitizar_nome


class CoreTests(unittest.TestCase):
    def test_clamp_motor(self):
        self.assertEqual(clamp_motor(10, 0, 5), 5)
        self.assertEqual(clamp_motor(-1, 0, 5), 0)
        self.assertEqual(clamp_motor(3, 0, 5), 3)

    def test_digito_verificador_intervalo(self):
        dig = _digito_verificador("MSCU", "123456")
        self.assertIsInstance(dig, int)
        self.assertGreaterEqual(dig, 0)
        self.assertLessEqual(dig, 9)

    def test_sanitizar_nome(self):
        self.assertEqual(_sanitizar_nome("\x1b[31mJoao\x1b[0m"), "Joao")
        self.assertEqual(_sanitizar_nome("***"), "Inspetor")

    def test_gerar_conteiner_campos(self):
        c = gerar_conteiner(risco_escala=1.1, suspeito_escala=1.2)
        for k in ("id", "peso_declarado", "tipo_carga", "pais", "porto", "iso", "risco_pais", "itens_escaneados"):
            self.assertIn(k, c)
        self.assertGreaterEqual(c["risco_pais"], 1)
        self.assertLessEqual(c["risco_pais"], 5)


if __name__ == "__main__":
    unittest.main()
