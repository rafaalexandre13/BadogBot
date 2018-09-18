import pytesseract as ocr
import numpy as np
import cv2


def ocr_itau(voucher_directory):
    """
    OPTMIZACAO DA IMAGEM
    Realiza o corte na imagem onde as informacoes necessarias se encontram,
    redimenciona a imagem para melhor leitura do OCR

    OCR
    Realiza o OCR da imagem

    :param voucher_directory: Diretorio da imagem
    :return: Tupla com as informacoes de transaction_value, codigo de barras e data
    do transaction_value realizado
    """

    # OPTMIZACAO DA IMAGEM
    image = cv2.imread(voucher_directory)
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

    # CAPTURANDO E LIMPANDO AS INFORMACOES
    for item in captured_info:
        if item == '':
            captured_info.remove(item)

    transaction_value = float(
        captured_info[0].replace('R$', '').replace(',', '.'))

    transaction_date = captured_info[2].split()[2].replace('.', '')

    barcode = captured_info[4].replace('.', '').replace(
        ' ', '') + captured_info[5].replace('.', '').replace(' ', '')

    return transaction_value, transaction_date, barcode


def ocr_bbrasil(voucher_directory):
    """
    OPTMIZACAO DA IMAGEM
    Realiza o corte na imagem onde as informacoes necessarias se encontram,
    redimenciona a imagem para melhor leitura do OCR

    OCR
    Realiza o OCR da imagem

    :param voucher_directory: Diretorio da imagem
    :return: Tupla com as informacoes de transaction_value, codigo de barras e data
    do transaction_value realizado
    """

    # OPTMIZACAO DA IMAGEM
    image = cv2.imread(voucher_directory)
    crop = image[220:330, 0:400]
    provides = 1500.0 / crop.shape[1]
    resize = (1200, int(crop.shape[0] * provides))
    final_image = cv2.resize(crop, resize, interpolation=cv2.INTER_AREA)

    # PROCESSO DE BINERIZACAO DA IMAGEM
    npimagem = np.asarray(final_image).astype(np.uint8)
    npimagem[:, :, 0] = 0
    npimagem[:, :, 0] = 0

    img = cv2.cvtColor(npimagem, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (3, 7), 2)

    ret, thresh = cv2.threshold(
        img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    """ VIZUALIZAR A IMAGEM GRAFICA """
    # cv2.imshow("teste", erosion)
    # cv2.waitKey(0)

    # OCR
    ocr_image = ocr.image_to_string(thresh, lang='por')
    captured_info = ocr_image.splitlines()

    # CAPTURANDO E LIMPANDO AS INFORMACOES
    for item in captured_info:
        if item == '':
            captured_info.remove(item)

    transaction_value = float(
        captured_info[4].split()[2].replace(',', '.') +
        captured_info[4].split()[3]
    )

    barcode = captured_info[0].replace(' ', '')

    transaction_date = captured_info[2].split()[3]

    return transaction_value, transaction_date, barcode
