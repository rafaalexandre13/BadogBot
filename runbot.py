from my_finances.chatbot.chatbot import *


def main():
    """ Inicialização da aplicação """

    updater.dispatcher.add_handler(manage_finances)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
