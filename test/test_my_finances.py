import os
from unittest import TestCase

from my_finances.database_manage import DBcreator, Database
from my_finances.ocr import ocr_itau, ocr_bbrasil

TEST_DATABASE_DIRECTORY = 'TestFinanceDB.db_create'
ITAU_VOUCHER_TEST = 'test_bank_voucher/test_ocr_itau.jpg'
BBRASIL_VOUCHER_TEST = 'test_bank_voucher/test_ocr_bbrasil.jpg'


class TestDatabase(TestCase):
    """
    TESTE DE BANCO DE DADOS
    """
    def setUp(self):
        self.db_create = DBcreator(TEST_DATABASE_DIRECTORY)
        self.database = Database('Teste', 7000.31, '1234567890', '13/01/2020')

    def test_1_create_db(self):
        """
        Teste de criacao do banco de dados sqlite3
        """
        self.assertTrue(self.db_create)

    def test_2_enter_values(self):
        """
        Teste de insersao de valore no banco de dados
        """
        self.assertEqual(
            self.database.insert(TEST_DATABASE_DIRECTORY), "success"
        )

    def test_3_enter_existing_values(self):
        """
        Teste de insersao de valores com o codigo de barras ja existente no
        banco de dados
        """
        self.assertEqual(
            self.database.insert(TEST_DATABASE_DIRECTORY), "failed"
        )

    def test_4_total_value(self):
        """
        Teste de saida de valor total na conta
        """
        self.assertEqual(
            self.database.total_value(TEST_DATABASE_DIRECTORY), 7000.31
        )

    def test_5_personal_value(self):
        """
        Teste de saida de valor total de cada pessoa
        """
        self.assertEqual(
            self.database.personal_value(TEST_DATABASE_DIRECTORY), 7000.31
        )

    def test_6_latest_transactions(self):
        """
        Teste de saida dos ultimos 5 movimentos de cada pessoa
        """
        self.assertEqual(
            self.database.latest_transactions(TEST_DATABASE_DIRECTORY),
            [('Teste', 7000.31, '13/01/2020')]
        )

        # DEIXAR ESTA FUNCAO NO FINAL DO TESTE DE BANCO DE DADOS
        os.remove(TEST_DATABASE_DIRECTORY)


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
        transaction_value: valor pago,
        barcode: codigo de barras,
        transaction_date: data em que foi realizado o transaction_value
        """

        self.assertEqual(
            ocr_itau(ITAU_VOUCHER_TEST), (
                self.itauPay, self.itauPayDay, self.itauBarCode)
        )

    def test_2_ocr_bbrasil(self):
        """
        Teste de OCR em boleto gerado pelo Banco do Brasil
        """

        self.assertEqual(
            ocr_bbrasil(BBRASIL_VOUCHER_TEST), (
                self.bbrasilPay, self.bbrasilPayDay, self.bbrasilBarCode)
        )
