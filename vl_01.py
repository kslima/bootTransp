from sapgui import SAPGuiApplication
from transaction import SAPTransaction
from sapguielements import SAPGuiElements, SAVE_BUTTON, MESSAGE_ELEMENT
import service
from model import Shipping
import re

SPLIT_STR = "/ssubSUBSCREEN_BODY"

SHIPPING_PLACE_VALUE = "1014"

SHIPPING_PLACE_FIELD = "wnd[0]/usr/ctxtLIKP-VSTEL"
SHIPPING_ORDER_FIELD = "wnd[0]/usr/ctxtLV50C-VBELN"

SHIPPING_DEPOSIT_FIELD = "wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\02/ssubSUBSCREEN_BODY:SAPMV50A:1104" \
                         "/tblSAPMV50ATC_LIPS_PICK/ctxtLIPS-LGORT[3,0]"
SHIPPING_AMOUNT_FIELD = "wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\02/ssubSUBSCREEN_BODY:SAPMV50A:1104" \
                        "/tblSAPMV50ATC_LIPS_PICK/txtLIPSD-G_LFIMG[4,0]"
SHIPPING_PICKING_FIELD = "wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\02/ssubSUBSCREEN_BODY:SAPMV50A:1104" \
                         "/tblSAPMV50ATC_LIPS_PICK/txtLIPSD-PIKMG[6,0]"
SHIPPING_BATCH_FIELD = "wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\02/ssubSUBSCREEN_BODY:SAPMV50A:1104" \
                       "/tblSAPMV50ATC_LIPS_PICK/ctxtLIPS-CHARG[8,0]"

PARTIAL_SHIPPINGS_MESSAGE = "wnd[1]/tbar[0]/btn[0]"


class VL01:

    @staticmethod
    def create(sap_session, shipping_model):

        SAPTransaction.call(sap_session, 'vl01n')
        SAPGuiElements.set_text(sap_session, SHIPPING_PLACE_FIELD, SHIPPING_PLACE_VALUE)
        SAPGuiElements.set_text(sap_session, SHIPPING_ORDER_FIELD, shipping_model.order)
        SAPGuiElements.press_keyboard_keys(sap_session, "Enter")

        # error_message = VL01.get_message(sap_session, MESSAGE_ELEMENT)
        error_message = ""

        # caso nao mostre nenhuma mensagem de erro, continua a execucao
        if not error_message:

            SAPGuiElements.select_element(sap_session, SHIPPING_DEPOSIT_FIELD.split(SPLIT_STR)[0])
            SAPGuiElements.set_text(sap_session, SHIPPING_DEPOSIT_FIELD, shipping_model.product.storage)

            SAPGuiElements.select_element(sap_session, SHIPPING_AMOUNT_FIELD.split(SPLIT_STR)[0])
            SAPGuiElements.set_text(sap_session, SHIPPING_AMOUNT_FIELD, shipping_model.amount)

            SAPGuiElements.select_element(sap_session, SHIPPING_PICKING_FIELD.split(SPLIT_STR)[0])
            SAPGuiElements.set_text(sap_session, SHIPPING_PICKING_FIELD, shipping_model.amount)

            SAPGuiElements.select_element(sap_session, SHIPPING_BATCH_FIELD.split(SPLIT_STR)[0])
            SAPGuiElements.set_text(sap_session, SHIPPING_BATCH_FIELD, shipping_model.product.batch)

            SAPGuiElements.press_button(sap_session, SAVE_BUTTON)
            try:
                # ignorando mensagem de remessas parciais
                SAPGuiElements.press_button(sap_session, PARTIAL_SHIPPINGS_MESSAGE)
            finally:
                message = SAPGuiElements.get_text(sap_session, MESSAGE_ELEMENT)
                if VL01.assert_sucsses_message(message):
                    # remessa criada com sucesso
                    return True, VL01.get_shipping_number(message)

                else:
                    # erro ao criar a remessa
                    return False, VL01.get_formated_error_message(message, shipping_model)
        else:
            # erro ao tentar entrar na ordem
            return False, VL01.get_formated_error_message(error_message, shipping_model)

    @staticmethod
    def get_message(sap_session, element):
        message = ""
        try:
            message = SAPGuiElements.get_text(sap_session, element)
        finally:
            return message

    @staticmethod
    def get_formated_error_message(error_message, shipping_model):
        return "Falha ao criar uma remessa na ordem {}.\nErro SAP: '{}'".format(shipping_model.order, error_message)

    @staticmethod
    def get_shipping_number(sucsses_message):
        return "".join(re.findall("\\d+", sucsses_message))

    @staticmethod
    def assert_sucsses_message(message):
        return True
        '''
        if re.findall("^(Entrega Normal \\d+ gravado\\(s\\))$", message.strip()):
            return True
        return False
        '''


'''
session = SAPGuiApplication.connect()
product = service.find_product_by_description("Alcool Anidro")
shipping = Shipping('43087', '8', product)
print(VL01.create(session, shipping))
'''
