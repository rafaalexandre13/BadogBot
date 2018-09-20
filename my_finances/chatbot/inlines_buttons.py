from telegram import InlineKeyboardButton as IlKbButton
from telegram import InlineKeyboardMarkup
from ..database_manage import Database

db_directory = "my_finances/FinancesDB.db"


class ButtonsInterface:
    @staticmethod
    def main_buttons():
        # TODO Documentar

        keyboard = [
            [IlKbButton("Depositar", callback_data="/deposit"),
             IlKbButton("Extrato", callback_data="/extract")],
            [IlKbButton("Sair", callback_data="/exit")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        return reply_markup

    @staticmethod
    def deposit_buttons():
        # TODO Documentar

        keyboard = [
            [IlKbButton("Banco do Brasil", callback_data="/bbrasil"),
             IlKbButton("Itau", callback_data="/itau")],
            [IlKbButton("Voltar", callback_data="/back"),
             IlKbButton("Sair", callback_data="/exit")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        return reply_markup

    @staticmethod
    def confirm_deposit_buttons(
            name, transaction_value, transaction_date, barcode
    ):
        # TODO Documentar
        db = Database(name, transaction_value, barcode, transaction_date)

        keyboard = [
            [IlKbButton("Continuar", callback_data=db.insert(db_directory))],
            [IlKbButton("Voltar", callback_data="/back"),
             IlKbButton("Cancelar", callback_data="/cancel")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        return reply_markup

    @staticmethod
    def extract_buttons():
        # TODO Documentar
        keyboard = [
            [IlKbButton("Valor total", callback_data="/total_value"),
             IlKbButton("Ultimas transações",
                        callback_data="/last_transactions")],
            [IlKbButton("Voltar", callback_data="/back"),
             IlKbButton("Sair", callback_data="/exit")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        return reply_markup
