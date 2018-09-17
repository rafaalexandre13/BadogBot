import os
from unittest import TestCase

from my_finances.database_manage import DBcreator, Database
from my_finances.ocr import ocr_itau, ocr_bbrasil

BANCOTESTE = 'TestFinanceDB.db'
BANK_SLIP_ITAU = 'test_bank_voucher/test_ocr_itau.jpg'
BANK_SLIP_BBRASIL = 'test_bank_voucher/test_ocr_bbrasil.jpg'


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
        self.assertEqual(self.database.insert(BANCOTESTE), "success")

    def test_3_inserir_valores_existente(self):
        """
        Teste de insersao de valores com o codigo de barras ja existente no
        banco de dados
        """
        self.assertEqual(
            self.database.insert(BANCOTESTE), "failed")

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
    # TODO Corrigir documentação

    def setUp(self):
        self.itauPay = 421.57
        self.itauPayDay = "05/07/2018"
        self.itauBarCode = "23793381286000847992919000063305375770000042157"

        self.bbrasilPay = 500.0
        self.bbrasilPayDay = "06/08/2018"
        self.bbrasilBarCode = "23793381286000918494072000063304176080000050000"

    def test_1_ocr_itau(self):
        """
        Teste de OCR em boleto gerado pelo banco Itau

        Insira os valores dos boletos que serao testados nas variaveis
        pagamento: valor pago,
        codigo_boleto: codigo de barras,
        data_pagamento: data em que foi realizado o pagamento
        """

        self.assertEqual(ocr_itau(BANK_SLIP_ITAU), (self.itauPay,
                                                    self.itauPayDay,
                                                    self.itauBarCode))

    def test_2_ocr_bbrasil(self):
        """
        Teste de OCR em boleto gerado pelo Banco do Brasil
        """

        self.assertEqual(ocr_bbrasil(BANK_SLIP_BBRASIL), (self.bbrasilPay,
                                                          self.bbrasilPayDay,
                                                          self.bbrasilBarCode))
