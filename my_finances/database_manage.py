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
        CREATE TABLE IF NOT EXISTS deposito (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            pagamento REAL,
            codigo_boleto TEXT UNIQUE,
            data_pagamento TEXT
        );
        """)

        self.conn.commit()
        cursor.close()


class Database:

    def __init__(self, nome=str(), pagamento=float(),
                 codigo_boleto=str(), data_pagamento=str()):

        self.nome = nome
        self.pagamento = pagamento
        self.codigo_boleto = codigo_boleto
        self.data_pagamento = data_pagamento

    def insert(self, dir_bd):
        """
        INSERCAO DE DADOS
        nome, pagamento, codigo de barras, data do pagamento

        """
        database = DBcreator(dir_bd)

        try:
            cursor = database.conn.cursor()
            cursor.execute("""
            INSERT INTO deposito (
                nome, pagamento, codigo_boleto, data_pagamento)
                VALUES (?, ?, ?, ?);
            """, (self.nome, self.pagamento, self.codigo_boleto,
                  self.data_pagamento))

            database.conn.commit()
            cursor.close()
            return "Sucesso"

        except sqlite3.IntegrityError:
            return "Boleto ja existe"

            # cursor.commit()
            # situation = "#salvo"
        # else:
        #     situation = "#existe"
        #
        # self.connection.close()
        # return situation

    def saida_valor_total(self, bd_dir):
        """
        Mostrar o Valor total na conta
        """
        database = DBcreator(bd_dir)
        cursor = database.conn.cursor()
        cursor.execute("""SELECT SUM(pagamento) AS payments FROM deposito""")
        output = cursor.fetchone()[0]
        # output = "{:.2f}".format(output)
        cursor.close()
        return float(output)

    def saida_valor_pessoal(self, dir_bd):
        """ VALOR TOTAL DE CADA PESSOA """
        database = DBcreator(dir_bd)
        cursor = database.conn.cursor()
        cursor.execute("""
        SELECT SUM(pagamento) AS payments FROM deposito
            WHERE nome = ?;
        """, (self.nome,))
        output = cursor.fetchone()[0]
        # output = "{:.2f}".format(output)
        cursor.close()
        return float(output)

    def ultimas_movimentacoes(self, dir_bd):
        """ 5 ULTIMAS MOVIMENTACOES DE CADA PESSOA """
        database = DBcreator(dir_bd)
        cursor = database.conn.cursor()
        cursor.execute("""
        SELECT nome, pagamento, data_pagamento FROM deposito WHERE nome = ?
            ORDER BY id DESC LIMIT 5; 
        """, (self.nome,))

        output = cursor.fetchall()
        cursor.close()
        return output

#
# def save_in_db(name, pay, bcode, date):
#     db = Database(name, pay, bcode, date)
#     insert = db.insert()
#     return insert
#
# def valtotal(bd):
#     db = Database()
#     return db.saida_valor_total(bd)
#
# def valpeop(bd, name):
#     db = Database(nome=name)
#     return db.saida_valor_pessoal(bd, name)
#
# def val5movpeop(name):
#     db = Database(name=name)
#     return db.read3()
#
# save_in_db(1, 10.0, '1234567890', '31/08/18')
