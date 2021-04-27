import re

from sapguielements import SAPGuiElements, SAVE_BUTTON, MESSAGE_ELEMENT
from transaction import SAPTransaction

PRODUCT_COD_ELEMENT = "wnd[0]/usr/ctxtQALS-MATNR"
CENTER_ELEMENT = "wnd[0]/usr/ctxtQALS-WERK"
CENTER_VALUE = "1014"
ORIGIN_BATCH_ELEMENT = "wnd[0]/usr/ctxtQALS-HERKUNFT"
ORIGIN_BATCH = "89"

BATCH_ELEMENT = "wnd[0]/usr/subLOT_HEADER:SAPLQPL1:1102/ctxtQALS-CHARG"
DEPOSIT_ELEMENT = "wnd[0]/usr/subLOT_HEADER:SAPLQPL1:1102/ctxtQALS-LAGORTCHRG"
QTD_BATCH_ELEMENT = "wnd[0]/usr/tabsTABSTRIP/tabpHERK/ssubSUBSCR_TABSTRIP:SAPLQPL1:0212/txtQALS-LOSMENGE"
QTD_BATCH_VALUE = "1"
TEXT_ELEMENT = "wnd[0]/usr/tabsTABSTRIP/tabpHERK/ssubSUBSCR_TABSTRIP:SAPLQPL1:0212/txtQALS-KTEXTLOS"
OPTIONAL_CREATE = "wnd[1]/usr/btnSPOP-OPTION1"
ERROR_MESSAGE_ELEMENT = "wnd[1]/usr/txtMESSTXT1"


class QA01:
    @staticmethod
    def create(sap_session, product_model, shipping):
        SAPTransaction.call(sap_session, 'qa01')
        SAPGuiElements.set_text(sap_session, PRODUCT_COD_ELEMENT, product_model.cod)
        SAPGuiElements.set_text(sap_session, CENTER_ELEMENT, CENTER_VALUE)
        SAPGuiElements.set_text(sap_session, ORIGIN_BATCH_ELEMENT, ORIGIN_BATCH)
        SAPGuiElements.press_keyboard_keys(sap_session, "Enter")

        sap_session.findById("wnd[1]/usr/lbl[1,3]").setFocus()
        SAPGuiElements.press_keyboard_keys(sap_session, "Enter")

        SAPGuiElements.set_text(sap_session, BATCH_ELEMENT, product_model.batch)
        SAPGuiElements.set_text(sap_session, DEPOSIT_ELEMENT, product_model.storage)
        SAPGuiElements.set_text(sap_session, QTD_BATCH_ELEMENT, QTD_BATCH_VALUE)
        SAPGuiElements.set_text(sap_session, TEXT_ELEMENT, shipping)

        SAPGuiElements.press_button(sap_session, SAVE_BUTTON)
        try:
            # ignorando mensagem de remessas parciais
            SAPGuiElements.press_button(sap_session, OPTIONAL_CREATE)
            error_message = SAPGuiElements.get_text(sap_session, ERROR_MESSAGE_ELEMENT)
            if error_message:
                return False, QA01.get_formated_error_message(error_message, shipping)

        finally:
            message = SAPGuiElements.get_text(sap_session, MESSAGE_ELEMENT)
            if QA01.assert_sucsses_message(message):

                # remessa criada com sucesso
                return True, QA01.get_batch_controller_number(message)

            else:
                # erro ao criar lote
                message = SAPGuiElements.get_text(sap_session, ERROR_MESSAGE_ELEMENT)
                return False, QA01.get_formated_error_message(message, shipping)

    @staticmethod
    def get_message(sap_session, element):
        message = ""
        try:
            message = SAPGuiElements.get_text(sap_session, element)
            print(message)
        finally:
            return message

    @staticmethod
    def get_formated_error_message(error_message, shipping):
        return "Falha ao criar lote de controle para remessa {}.\nErro SAP: '{}'".format(shipping, error_message)

    @staticmethod
    def assert_sucsses_message(message):
        if re.findall("^(Lote de controle 1014 \\d{12} foi criado)$", message.strip()):
            return True
        return False

    @staticmethod
    def get_batch_controller_number(sucsses_message):
        return "".join(re.findall("\\d{12}", sucsses_message))


'''
session = SAPGuiApplication.connect()
product = service.find_product_by_description("Alcool Anidro")
print(QA01.create(session, product, "80602726"))
'''