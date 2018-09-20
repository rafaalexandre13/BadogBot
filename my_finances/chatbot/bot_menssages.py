# TODO Documentar
def message_last_transactions(parm):
    context = []
    for i in parm:
        context.append("@{}\nValor R$ {}\nData {}".format(i[0], i[1], i[2]))

    return ' \n\n'.join(context)


confirmation_message = "Valor depositado: R$ `{}`\n" \
                       "Data: `{}`\n" \
                       "Código de barras:\n`{}`"
