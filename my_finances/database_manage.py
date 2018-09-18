""" FUNCOES DO BANCO DE DADOS"""

import sqlite3


class DBcreator:
    def __init__(self, diretorio_database):
        self.conn = sqlite3.connect(diretorio_database)
        self.create_table()

    def create_table(self):
        """
        Cria a tabela deposito se nao existir
        """
        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            transaction_value REAL NOT NULL,
            barcode TEXT NOT NULL UNIQUE,
            transaction_date TEXT NOT NULL
        );
        """)

        self.conn.commit()
        cursor.close()


class Database:

    def __init__(self, name=str(), transaction_value=float(),
                 barcode=str(), transaction_date=str()):

        self.name = name
        self.transaction_value = transaction_value
        self.barcode = barcode
        self.transaction_date = transaction_date

    def insert(self, db_directory):
        """
        INSERCAO DE DADOS
        name, transaction_value, barcode, data do transaction_date

        """
        database = DBcreator(db_directory)
        cursor = database.conn.cursor()

        cursor.execute("""
        SELECT COUNT(*) AS bar_code_qt FROM transactions 
            WHERE barcode = ?;
        """, (self.barcode,))

        check_barcode_repeated = cursor.fetchone()

        if check_barcode_repeated[0] == 0:
            cursor = database.conn.cursor()

            cursor.execute("""
            INSERT INTO transactions (
                name, transaction_value, barcode, transaction_date)
                VALUES (?, ?, ?, ?);
            """, (self.name, self.transaction_value, self.barcode,
                  self.transaction_date))

            database.conn.commit()
            cursor.close()
            return "success"

        else:
            cursor.close()
            return "failed"

    def total_value(self, db_directory):
        """
        Mostrar o Valor total na conta
        """
        database = DBcreator(db_directory)
        cursor = database.conn.cursor()

        cursor.execute(
            """SELECT SUM(transaction_value) AS total_value FROM transactions"""
        )

        output = cursor.fetchone()[0]
        cursor.close()
        return float(output)

    def personal_value(self, db_directory):
        """ VALOR TOTAL DE CADA PESSOA """
        database = DBcreator(db_directory)
        cursor = database.conn.cursor()

        cursor.execute("""
        SELECT SUM(transaction_value) AS personal_value FROM transactions
            WHERE name = ?;
        """, (self.name,))

        output = cursor.fetchone()[0]
        cursor.close()
        return float(output)

    def latest_transactions(self, db_directory):
        """ 5 ULTIMAS TRANSACOES DE CADA PESSOA """
        database = DBcreator(db_directory)
        cursor = database.conn.cursor()

        cursor.execute("""
        SELECT name, transaction_value, transaction_date FROM transactions 
            WHERE name = ? ORDER BY id DESC LIMIT 5; 
        """, (self.name,))

        output = cursor.fetchall()
        cursor.close()
        return output
