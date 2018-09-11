import os
from unittest import TestCase

from my_finances.database_manage import DBcreator, Database

BANCOTESTE = 'TestFinanceDB.db'


class TestDatabase(TestCase):
    """
    TESTE DE BANCO DE DADOS
    """
    def setUp(self):
        self.db = DBcreator(BANCOTESTE)
        self.database = Database('Teste', 7000.31, '1234567890', '13/01/2020')

    def test_1_create_db(self):
        """
        Teste de criacao do banco de dados sqlite3
        """
        self.assertTrue(self.db)

    def test_2_inserir_valores(self):
        """
        Teste de insersao de valore no banco de dados
        """
        self.assertEqual(self.database.insert(BANCOTESTE), "Sucesso")

    def test_3_inserir_valores_existente(self):
        """
        Teste de insersao de valores com o codigo de barras ja existente no
        banco de dados
        """
        self.assertEqual(
            self.database.insert(BANCOTESTE), "Boleto ja existe")

    def test_4_valor_total(self):
        """
        Teste de saida de valor total na conta
        """
        self.assertEqual(self.database.saida_valor_total(BANCOTESTE), 7000.31)

    def test_5_valor_pessoal(self):
        """
        Teste de saida de valor total de cada pessoa
        """
        self.assertEqual(
            self.database.saida_valor_pessoal(BANCOTESTE), 7000.31)

    def test_6_ultimas_movimentacoes(self):
        """
        Teste de saida dos ultimos 5 movimentos de cada pessoa
        """
        self.assertEqual(
            self.database.ultimas_movimentacoes(BANCOTESTE),
            [('Teste', 7000.31, '13/01/2020')])

        # DEIXAR ESTA FUNCAO NO FINAL DO TESTE DE BANCO DE DADOS
        os.remove(BANCOTESTE)


class TestOCR(TestCase):
    """
    Teste de OCR dos boletos
    """

    def setUp(self):
        pass

    def test_1_ocr_itau(self):
        pass
