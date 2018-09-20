# Formatação das mensagens enviadas pelo bot


def message_last_transactions(transactions_list):
    """
    Mensagem das Ultimas transações realizadas
    """
    context = []
    for transaction in transactions_list:
        context.append("@{}\nValor R$ {}\nData {}".format(
            transaction[0], transaction[1], transaction[2]))

    return ' \n\n'.join(context)


# Mensagem de Confirmação de dados realizado pelo OCR
confirmation_message = "Valor depositado: R$ `{}`\n" \
                       "Data: `{}`\n" \
                       "Código de barras:\n`{}`"
