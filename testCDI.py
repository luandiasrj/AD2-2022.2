# !/usr/bin/env python
# coding: UTF-8
#
## @package AD2_Test_Unit_for_CDI
#
#  Class for testing the CDI taxes.
#
#  @author Luan Bernardo Dias
#  @since 06/10/2022
#  @see https://docs.python.org/2/library/unittest.html
#


""" Importa módulos do arquivo a ser testado (cdi.py) e faz o teste das funções """
from cdi import *
import unittest


## 
# Classe para testar se os montantes, porcentagens e rendimentos estão corretos.
# 
class TestCDI(unittest.TestCase):

    ##
    # setUp é chamado automaticamente antes de qualquer teste ser executado.
    #
    def setUp(self):
        pass

    ## 
    # Testa se a conversão de meses para dias está correta.
    #
    # @param m meses
    # @param d dias
    # 
    def test_month2day(self):
        self.assertEqual(round(month2day(0.1315), 6), 0.049037)
        self.assertEqual(round(month2day(0.1365), 6), 0.050788)

    ## Testa se a conversão de taxa para percentual está correta.
    #
    # @param t taxa de juros.
    # 
    def test_toPercent(self):
        self.assertEqual(to_percent(0.05), 5.0)
        self.assertEqual(to_percent(0.1315), 13.15)
        self.assertEqual(to_percent(0.084), 8.4)

    ## Testa se o juros de poupança está correto.
    #
    # @param t taxa de juros.
    # @param r taxa de juros nominal.
    # 
    def test_jurospoupanca(self):
        self.assertEqual(jurospoupanca(0.1315), 0.061675)
        self.assertEqual(jurospoupanca(0.084), (0.084 * 0.7))

    ## Testa se o valor futuro está correto.
    #
    # @param capital capital inicial.
    # @param taxa taxa de juros.
    # @param periodo período de tempo.
    #
    def test_valorfuturo(self):
        self.assertEqual(round(valorfuturo(1000, 0.005, 1), 2), 1005.00)
        self.assertEqual(round(valorfuturo(1000, 0.005, 2), 2), 1010.02)
        self.assertEqual(round(valorfuturo(1000, 0.005, 3), 2), 1015.08)

    ## Testa se o imposto está correto.
    #
    # @param valorfuturo valor futuro.
    # @param capital capital inicial.
    # @param taxa taxa de juros.
    #
    def test_imposto(self):
        valorfut = valorfuturo(1000, year2month(0.93 * 0.1315) / 100, 1)
        self.assertEqual(round(imposto(valorfut, 1000, 22.5), 4), 2.1737)
        self.assertEqual(round(imposto(1032.505467, 1000, 20), 4), 6.5011)


if __name__ == '__main__':
    unittest.main()
