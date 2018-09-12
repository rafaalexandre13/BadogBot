import pytesseract as ocr
import cv2


def ocr_itau(img_dir):
    """
    OPTMIZACAO DA IMAGEM
    Realiza o corte na imagem onde as informacoes necessarias se encontram,
    redimenciona a imagem para melhor leitura do OCR

    OCR
    Realiza o OCR da imagem

    :param img_dir: Diretorio da imagem
    :return: Tupla com as informacoes de pagamento, codigo de barras e data
    do pagamento realizado
    """

    # OPTMIZACAO DA IMAGEM
    image = cv2.imread(img_dir)
    crop = image[330:1000, 0:1000]
    provides = 300.0 / crop.shape[1]
    resize = (300, int(crop.shape[0] * provides))
    final_image = cv2.resize(crop, resize, interpolation=cv2.INTER_AREA)

    """ VIZUALIZAR A IMAGEM GRAFICA """
    # cv2.imshow("teste", final_image)
    # cv2.waitKey(0)

    # OCR
    ocr_image = ocr.image_to_string(final_image, lang='por')
    captured_info = ocr_image.splitlines()

    for item in captured_info:
        """ Remover espacos inuteis para melhor leitura da lista """
        if item == '':
            captured_info.remove(item)

    pagamento = float(captured_info[0].replace('R$', '').replace(',', '.'))
    data_pagamento = captured_info[2].split()[2].replace('.', '')
    codigo_boleto = captured_info[4].replace('.', '').replace(
        ' ', '') + captured_info[5].replace('.', '').replace(' ', '')

    return pagamento, codigo_boleto, data_pagamento
