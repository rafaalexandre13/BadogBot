import pytesseract as ocr
import cv2
import numpy as np


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
    crop = image[100:270, 0:400]
    provides = 300.0 / crop.shape[1]
    resize = (300, int(crop.shape[0] * provides))
    final_image = cv2.resize(crop, resize, interpolation=cv2.INTER_AREA)

    """ VIZUALIZAR A IMAGEM GRAFICA """
    # cv2.imshow("teste", final_image)
    # cv2.waitKey(0)

    # OCR
    ocr_image = ocr.image_to_string(final_image, lang='por')
    captured_info = ocr_image.splitlines()

    # CAPTURANDO INFORMACOES
    for item in captured_info:
        """ Remover espacos inuteis para melhor leitura da lista """
        if item == '':
            captured_info.remove(item)

    pagamento = float(captured_info[0].replace('R$', '').replace(',', '.'))
    data_pagamento = captured_info[2].split()[2].replace('.', '')
    codigo_boleto = captured_info[4].replace('.', '').replace(
        ' ', '') + captured_info[5].replace('.', '').replace(' ', '')

    return pagamento, data_pagamento, codigo_boleto


def ocr_bbrasil(img_dir):
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
    crop = image[220:330, 0:400]
    provides = 1500.0 / crop.shape[1]
    resize = (1200, int(crop.shape[0] * provides))
    final_image = cv2.resize(crop, resize, interpolation=cv2.INTER_AREA)

    """ Processo de binerizacao da imagem """
    npimagem = np.asarray(final_image).astype(np.uint8)
    npimagem[:, :, 0] = 0
    npimagem[:, :, 0] = 0

    img = cv2.cvtColor(npimagem, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (3, 7), 2)
    ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY +
                                cv2.THRESH_OTSU)

    """ VIZUALIZAR A IMAGEM GRAFICA """
    # cv2.imshow("teste", erosion)
    # cv2.waitKey(0)

    # OCR
    ocr_image = ocr.image_to_string(thresh, lang='por')
    captured_info = ocr_image.splitlines()

    # CAPTURANDO INFORMACOES
    for item in captured_info:
        if item == '':
            captured_info.remove(item)

    pagamento = float(captured_info[4].split()[2].replace(',', '.') +
                      captured_info[4].split()[3])
    codigo_boleto = captured_info[0].replace(' ', '')
    data_pagamento = captured_info[2].split()[3]

    return pagamento, data_pagamento, codigo_boleto
