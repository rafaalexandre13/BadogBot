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

BOTTOKEN = config('TOKEN')
bot = Bot(BOTTOKEN)
updater = Updater(BOTTOKEN)
dispatcher = updater.dispatcher

database = Database()
bd_dir = "my_finances/FinancesDB.db"
img_dir = "my_finances/bank_voucher/ocr_me.jpg"

confirmation_message = "Valor depositado: R$ `{}`\n" \
                       "Data: `{}`\n" \
                       "Código de barras:\n`{}`"

# TODO Documentar
A, B, C, D, E = range(5)


def start_interface(bot, update):
    """
    Primeira interface a ser chamado pela aplicacao
    apresentara os botoes (Depositar, Extrato, Cancelar)
    """
    update.message.reply_text(
        "O que deseja?",
        reply_markup=ButtonsInterface.main_buttons())

    return B


def main_interface(bot, update):
    # TODO Documentar
    if update.callback_query.data == "/deposit":
        # TODO Documentar
        """
        Interface para escolha do Banco
        """
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Escolha o Banco em que foi gerado o comprovante",
            reply_markup=ButtonsInterface.deposit_buttons())

        return C

    elif update.callback_query.data == "/extract":
        # TODO Documentar
        """
        Interface extrato
        """
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Extratos:",
            reply_markup=ButtonsInterface.extract_buttons())

        return E

    elif update.callback_query.data == "/cancel":
        # TODO Documentar
        """
        Cancelar
        """
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Até logo...")


def deposit(bot, update):
    # TODO Documentar
    if update.callback_query.data == '/bbrasil':
        def bbrasil(bot, update):
            # TODO Documentar
            """Banco do Brasil"""
            username = update.message.chat.username

            image = bot.getFile(update.message.photo[-1].file_id)
            image.download(img_dir)

            voucher = ocr.ocr_bbrasil(img_dir)

            bot.send_message(
                chat_id=update.message.chat_id,
                text=confirmation_message.format(
                    voucher[0], voucher[1], voucher[2]),
                parse_mode=ParseMode.MARKDOWN)

            confirm = ButtonsInterface.confirm_deposit_buttons(
                username, voucher[0], voucher[1], voucher[2])

            update.message.reply_text(
                "Confirme as informações",
                reply_markup=confirm)

            dispatcher.remove_handler(voucher_handler)

        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Envie o comprovante emitido pelo Banco do Brasil")

        voucher_handler = MessageHandler(Filters.photo, bbrasil)
        dispatcher.add_handler(voucher_handler)

    elif update.callback_query.data == "/itau":
        # TODO Documentar
        """ Itau """
        def itau(bot, update):
            # TODO Documentar
            username = update.message.chat.username

            image = bot.getFile(update.message.photo[-1].file_id)
            image.download(img_dir)

            voucher = ocr.ocr_itau(img_dir)

            bot.send_message(
                chat_id=update.message.chat_id,
                text=confirmation_message.format(
                    voucher[0], voucher[1], voucher[2]),
                parse_mode=ParseMode.MARKDOWN)

            confirm = ButtonsInterface.confirm_deposit_buttons(
                username, voucher[0], voucher[1], voucher[2])

            update.message.reply_text(
                "Confirme as informações",
                reply_markup=confirm)

            dispatcher.remove_handler(voucher_handler)

        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Envie o comprovante emitido pelo Itau")

        voucher_handler = MessageHandler(Filters.photo, itau)
        dispatcher.add_handler(voucher_handler)

    elif update.callback_query.data == "/back":
        # TODO Documentar
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="O que deseja?",
            reply_markup=ButtonsInterface.main_buttons())

        return B

    elif update.callback_query.data == "cancel":
        # TODO Documentar
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Até logo...")
        return

    return D


def confirm_information(bot, update):
    # TODO Documentar
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
        return B

    elif update.callback_query.data == "/cancel":
        # TODO Documentar
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Até logo..."
        )


def extract(bot, update):
    # TODO Documentar
    if update.callback_query.data == "/amount":
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Valor total: R${:.2f}".format(
                database.saida_valor_total(bd_dir)
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
        A: [CallbkQueHand(start_interface)],
        B: [CallbkQueHand(main_interface)],
        C: [CallbkQueHand(deposit)],
        D: [CallbkQueHand(confirm_information)],
        E: [CallbkQueHand(extract)]
    },
    [CommandHandler('finance', start_interface)]
)
