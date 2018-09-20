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
from .bot_menssages import *

TOKEN = config('TOKEN')
bot = Bot(TOKEN)
updater = Updater(TOKEN)
dispatcher = updater.dispatcher

database = Database()
db_directory = "my_finances/FinancesDB.db"
voucher_directory = "my_finances/bank_voucher/ocr_me.jpg"


# Variaveis para retorno de função
START, MAIN, DEPOSIT, CONFIRM, EXTRACT = range(5)


def start_interface(bot, update):
    """ START

    Primeira interface a ser chamado pela aplicação
    Bot envia botões (Depositar, Extrato, Sair)
    """
    update.message.reply_text(
        "O que deseja?",
        reply_markup=ButtonsInterface.main_buttons()
    )
    return MAIN


def main_interface(bot, update):
    """ MAIN

    Condições sobre a decisão dos botões da interface START
    """
    if update.callback_query.data == "/deposit":
        """ Se o botão escolhido for (Depositar)
        
        Interface para escolha do Banco
        Bot envia botões (Banco do Brasil, Itaú, Voltar, Sair)
        """
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Escolha o Banco em que foi gerado o comprovante",
            reply_markup=ButtonsInterface.deposit_buttons()
        )
        return DEPOSIT

    elif update.callback_query.data == "/extract":
        """ Se o botão escolhido for (Extrato)
        
        Interface para escolha de tipo do Extrato
        Bot envia botões (Valor total, Ultimas transações, Voltar, Sair)
        """
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Extratos:",
            reply_markup=ButtonsInterface.extract_buttons()
        )
        return EXTRACT

    elif update.callback_query.data == "/exit":
        """ Se o botão escolhido for (Sair)
        
        Encerrar a aplicação
        """
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Até logo..."
        )


def deposit(bot, update):
    """ DEPOSIT

    Condições sobre a decisão dos botões da interface MAIN
    """
    if update.callback_query.data == '/bbrasil':
        """ Se o botão escolhido for (Banco do Brasil)
            
        Usuário deve enviar o comprovante da transação Emitido pelo
        Banco do Brasil
        """
        def bbrasil(bot, update):
            """ Confirmação Banco do Brasil

            Bot envia informações com os dados coletados do comprovante e
            botões (Continuar, Voltar, Cancelar)
            """

            # Coletando username do telegram
            username = update.message.chat.username

            # Capturando o comprovante enviado pelo usuário
            image = bot.getFile(update.message.photo[-1].file_id)
            image.download(voucher_directory)

            # OCR do comprovante do Banco do Brasil
            voucher = ocr.ocr_bbrasil(voucher_directory)

            bot.send_message(
                chat_id=update.message.chat_id,
                text=confirmation_message.format(
                    voucher[0], voucher[1], voucher[2]),
                parse_mode=ParseMode.MARKDOWN
            )

            update.message.reply_text(
                "Confirme as informações",
                reply_markup=ButtonsInterface.confirm_deposit_buttons(
                    username, voucher[0], voucher[1], voucher[2]
                ))

            dispatcher.remove_handler(voucher_handler)

        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Envie o comprovante emitido pelo Banco do Brasil"
        )

        voucher_handler = MessageHandler(Filters.photo, bbrasil)
        dispatcher.add_handler(voucher_handler)

    elif update.callback_query.data == "/itau":
        """ Se o botão escolhido for (Itaú)
            
        Usuário deve enviar o comprovante da transação Emitido pelo
        Itau 
        """
        def itau(bot, update):
            """ Confirmação Itau

            Bot envia informações com os dados coletados do comprovante e
            botões (Continuar, Voltar, Cancelar)
            """

            # Coletando username do telegram
            username = update.message.chat.username

            # Capturando o comprovante enviado pelo usuário
            image = bot.getFile(update.message.photo[-1].file_id)
            image.download(voucher_directory)

            # OCR do comprovante do Banco Itau
            voucher = ocr.ocr_itau(voucher_directory)

            bot.send_message(
                chat_id=update.message.chat_id,
                text=confirmation_message.format(
                    voucher[0], voucher[1], voucher[2]),
                parse_mode=ParseMode.MARKDOWN
            )

            update.message.reply_text(
                "Confirme as informações",
                reply_markup=ButtonsInterface.confirm_deposit_buttons(
                    username, voucher[0], voucher[1], voucher[2]
                ))

            dispatcher.remove_handler(voucher_handler)

        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Envie o comprovante emitido pelo Itau"
        )

        voucher_handler = MessageHandler(Filters.photo, itau)
        dispatcher.add_handler(voucher_handler)

    elif update.callback_query.data == "/back":
        """ Se o botão escolhido for (Voltar)
        
        Volta para a interface START
        Bot envia botões (Depositar, Extrato, Sair)
        """
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="O que deseja?",
            reply_markup=ButtonsInterface.main_buttons()
        )
        return MAIN

    elif update.callback_query.data == "/exit":
        """Se o botão escolhido for (Sair)
        
        Encerrar a aplicação
        """
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Até logo..."
        )
        return

    return CONFIRM


def confirm_information(bot, update):
    """ CONFIRM

    Condições sobre a decisão dos botões da interface DEPOSIT
    """
    if update.callback_query.data == "success":
        """Se o botão escolhido for (Continuar) e o database retornar (success) 
        os dados do comprovante serão salvos
        
        Bot envia mensagem de status da operação
        """
        # TODO Fazer voltar ao menu princial
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Dados salvos com sucesso.",
        )

    elif update.callback_query.data == "failed":
        """ Se o botão escolhido for (Continuar) e o database retornar (failed) 
        os dados do comprovante não serão salvos por já existir algum 
        comprovante com o mesmo código de barras
        
        Bot envia mensagem de status da operação
        """
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Já existe um comprovante com esse código de barras.",
            reply_markup=ButtonsInterface.deposit_buttons()
        )
        return DEPOSIT

    elif update.callback_query.data == "/back":
        """ Se o botão escolhido for (Voltar)
        
        Volta para a interface DEPOSIT
        Bot envia botões (Banco do Brasil, Itaú, Voltar, Sair)
        """
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Escolha o Banco em que foi gerado o comprovante",
            reply_markup=ButtonsInterface.deposit_buttons()
        )
        return DEPOSIT

    elif update.callback_query.data == "/cancel":
        """ Se o botão escolhido for (Sair)
        
        Encerrar a aplicação
        """
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Até logo..."
        )


def extract(bot, update):
    """ EXTRACT

    Condições sobre a decisão dos botões da interface MAIN
    """
    if update.callback_query.data == "/total_value":
        """ Se o botão escolhido for (Valor total)
        
        Bot envia o valor total e os botões 
        (Valor total, Ultimas transações, Voltar, Sair)
        """
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Valor total: R${:.2f}\n".format(
                    database.total_value(db_directory)),
            reply_markup=ButtonsInterface.extract_buttons()
        )
        return EXTRACT

    elif update.callback_query.data == "/last_transactions":
        """Se o botão escolhido for (Ultimas transações)
        
        Bot envia as ultimas transações e os botões
        (Valor total, Ultimas transações, Voltar, Sair)
        """
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text=message_last_transactions(
                database.latest_transactions(db_directory)),
            reply_markup=ButtonsInterface.extract_buttons()
        )
        return EXTRACT

    elif update.callback_query.data == "/back":
        """ Se o botão escolhido for (Voltar)
        
        Volta para a interface MAIN
        Bot envia botões (Depositar, Extrato, Sair)
        """
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="O que deseja?",
            reply_markup=ButtonsInterface.main_buttons()
        )
        return MAIN

    elif update.callback_query.data == "/exit":
        """Se o botão escolhido for (Sair)
        
        Encerrar a aplicação
        """
        bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            text="Até logo..."
        )


# Variavel a ser chamada para inicialização da aplicação my_finance
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
