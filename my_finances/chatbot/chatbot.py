# TODO Documentar
from telegram import Bot
from telegram import ParseMode
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.ext import CallbackQueryHandler as CallbkQueHand
from telegram.ext import ConversationHandler as ConvHand
from decouple import config
from my_finances import ocr
from my_finances.database_manage import Database
from .inlines_buttons import ButtonsInterface

TOKEN = config('TOKEN')
bot = Bot(TOKEN)
updater = Updater(TOKEN)
dispatcher = updater.dispatcher

database = Database()
db_directory = "my_finances/FinancesDB.db_create"
voucher_directory = "my_finances/bank_voucher/ocr_me.jpg"

confirmation_message = "Valor depositado: R$ `{}`\n" \
                       "Data: `{}`\n" \
                       "Código de barras:\n`{}`"

# TODO Documentar
START, MAIN, DEPOSIT, CONFIRM, EXTRACT = range(5)


def start_interface(bot, update):
    """
    START

    Primeira interface a ser chamado pela aplicacao
    apresentara os botoes (Depositar, Extrato, Cancelar)
    """
    update.message.reply_text(
        "O que deseja?",
        reply_markup=ButtonsInterface.main_buttons()
    )
    return MAIN


def main_interface(bot, update):
    # TODO Documentar
    """
    MAIN

    """
    if update.callback_query.data == "/deposit":
        # TODO Documentar
        """
        Interface para escolha do Banco
        """
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Escolha o Banco em que foi gerado o comprovante",
            reply_markup=ButtonsInterface.deposit_buttons()
        )
        return DEPOSIT

    elif update.callback_query.data == "/extract":
        # TODO Documentar
        """
        Interface extrato
        """
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Extratos:",
            reply_markup=ButtonsInterface.extract_buttons()
        )
        return EXTRACT

    elif update.callback_query.data == "/cancel":
        # TODO Documentar
        """
        Cancelar
        """
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Até logo..."
        )


def deposit(bot, update):
    # TODO Documentar
    """
    DEPOSIT

    """
    if update.callback_query.data == '/bbrasil':
        def bbrasil(bot, update):
            # TODO Documentar
            """Banco do Brasil"""
            username = update.message.chat.username

            image = bot.getFile(update.message.photo[-1].file_id)
            image.download(voucher_directory)

            voucher = ocr.ocr_bbrasil(voucher_directory)

            bot.send_message(
                chat_id=update.message.chat_id,
                text=confirmation_message.format(
                    voucher[0], voucher[1], voucher[2]),
                parse_mode=ParseMode.MARKDOWN
            )

            confirm = ButtonsInterface.confirm_deposit_buttons(
                username, voucher[0], voucher[1], voucher[2])

            update.message.reply_text(
                "Confirme as informações",
                reply_markup=confirm)

            dispatcher.remove_handler(voucher_handler)

        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Envie o comprovante emitido pelo Banco do Brasil"
        )

        voucher_handler = MessageHandler(Filters.photo, bbrasil)
        dispatcher.add_handler(voucher_handler)

    elif update.callback_query.data == "/itau":
        # TODO Documentar
        """ Itau """
        def itau(bot, update):
            # TODO Documentar
            username = update.message.chat.username

            image = bot.getFile(update.message.photo[-1].file_id)
            image.download(voucher_directory)

            voucher = ocr.ocr_itau(voucher_directory)

            bot.send_message(
                chat_id=update.message.chat_id,
                text=confirmation_message.format(
                    voucher[0], voucher[1], voucher[2]),
                parse_mode=ParseMode.MARKDOWN
            )

            confirm = ButtonsInterface.confirm_deposit_buttons(
                username, voucher[0], voucher[1], voucher[2])

            update.message.reply_text(
                "Confirme as informações",
                reply_markup=confirm)

            dispatcher.remove_handler(voucher_handler)

        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Envie o comprovante emitido pelo Itau"
        )

        voucher_handler = MessageHandler(Filters.photo, itau)
        dispatcher.add_handler(voucher_handler)

    elif update.callback_query.data == "/back":
        # TODO Documentar
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="O que deseja?",
            reply_markup=ButtonsInterface.main_buttons()
        )
        return MAIN

    elif update.callback_query.data == "cancel":
        # TODO Documentar
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Até logo..."
        )
        return

    return CONFIRM


def confirm_information(bot, update):
    # TODO Documentar
    """
    CONFIRM

    """
    if update.callback_query.data == "success":
        # TODO Documentar
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Dados salvos com sucesso.",
        )

    elif update.callback_query.data == "failed":
        # TODO Documentar
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Já existe um comprovante com esse código de barras."
        )

    elif update.callback_query.data == "/back":
        # TODO Documentar
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Escolha o Banco em que foi gerado o comprovante",
            reply_markup=ButtonsInterface.deposit_buttons()
        )
        return MAIN

    elif update.callback_query.data == "/cancel":
        # TODO Documentar
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Até logo..."
        )


def extract(bot, update):
    # TODO Documentar
    """
    EXTRACT

    """
    if update.callback_query.data == "/total_value":
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Valor total: R${:.2f}".format(
                database.total_value(db_directory)
            )
        )

    elif update.callback_query.data == "/last_transactions":
        # TODO Documentar
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Aguardando..."
        )

    elif update.callback_query.data == "/back":
        # TODO Documentar
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="O que deseja?",
            reply_markup=ButtonsInterface.main_buttons()
        )

    elif update.callback_query.data == "/cancel":
        # TODO Documentar
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Até logo..."
        )


# TODO Documentar
manage_finances = ConvHand(
    [CommandHandler('finance', start_interface)],
    {
        START: [CallbkQueHand(start_interface)],
        MAIN: [CallbkQueHand(main_interface)],
        DEPOSIT: [CallbkQueHand(deposit)],
        CONFIRM: [CallbkQueHand(confirm_information)],
        EXTRACT: [CallbkQueHand(extract)]
    },
    [CommandHandler('finance', start_interface)]
)
