import re

from model import LoteInspecao
from sapgui import SAPGuiApplication
from sapguielements import SAPGuiElements, SAVE_BUTTON, MESSAGE_ELEMENT
from transaction import SAPTransaction

PRODUCT_COD_ELEMENT = "wnd[0]/usr/ctxtQALS-MATNR"
ELEMENTO_CENTRO = "wnd[0]/usr/ctxtQALS-WERK"
CENTRO = "1014"
ELEMENTO_LOTE_ORIGEM = "wnd[0]/usr/ctxtQALS-HERKUNFT"
LOTE_ORIGEM = "89"
ELEMENTO_LOTE = "wnd[0]/usr/subLOT_HEADER:SAPLQPL1:1102/ctxtQALS-CHARG"
ELEMENTO_DEPOSITO = "wnd[0]/usr/subLOT_HEADER:SAPLQPL1:1102/ctxtQALS-LAGORTCHRG"
ELEMENTO_QUANTIDADE_LOTE = "wnd[0]/usr/tabsTABSTRIP/tabpHERK/ssubSUBSCR_TABSTRIP:SAPLQPL1:0212/txtQALS-LOSMENGE"
QUANTIDADE_LOTE = "1"
ELEMENTO_TEXTO_BREVE_07 = "wnd[0]/usr/tabsTABSTRIP/tabpHERK/ssubSUBSCR_TABSTRIP:SAPLQPL1:0201/txtQALS-KTEXTLOS"
ELEMENTO_TEXTO_BREVE_89 = "wnd[0]/usr/tabsTABSTRIP/tabpHERK/ssubSUBSCR_TABSTRIP:SAPLQPL1:0212/txtQALS-KTEXTLOS"
OPTIONAL_CREATE = "wnd[1]/usr/btnSPOP-OPTION1"
ERROR_MESSAGE_ELEMENT = "wnd[1]/usr/txtMESSTXT1"


class QA01:
    @staticmethod
    def create(sap_session, lote_inspecao):
        # verificando se o lote é de inspecao de produto(89) ou de veiculo(07)
        inspecionando_produto = lote_inspecao.origem == "89"

        SAPTransaction.call(sap_session, 'qa01')
        SAPGuiElements.set_text(sap_session, PRODUCT_COD_ELEMENT, lote_inspecao.material)
        SAPGuiElements.set_text(sap_session, ELEMENTO_CENTRO, CENTRO)
        SAPGuiElements.set_text(sap_session, ELEMENTO_LOTE_ORIGEM, lote_inspecao.origem)
        SAPGuiElements.press_keyboard_keys(sap_session, "Enter")

        if inspecionando_produto:
            sap_session.findById("wnd[1]/usr/lbl[1,3]").setFocus()
            SAPGuiElements.press_keyboard_keys(sap_session, "Enter")

        SAPGuiElements.set_text(sap_session, ELEMENTO_LOTE, lote_inspecao.lote)
        SAPGuiElements.set_text(sap_session, ELEMENTO_DEPOSITO, lote_inspecao.deposito)

        if inspecionando_produto:
            SAPGuiElements.set_text(sap_session, ELEMENTO_QUANTIDADE_LOTE, QUANTIDADE_LOTE)
            SAPGuiElements.set_text(sap_session, ELEMENTO_TEXTO_BREVE_89, lote_inspecao.texto_breve)
        else:
            SAPGuiElements.set_text(sap_session, ELEMENTO_TEXTO_BREVE_07, lote_inspecao.texto_breve)

        SAPGuiElements.press_button(sap_session, SAVE_BUTTON)
        try:
            # ignorando mensagem de remessas parciais
            SAPGuiElements.press_button(sap_session, OPTIONAL_CREATE)
            error_message = SAPGuiElements.get_text(sap_session, ERROR_MESSAGE_ELEMENT)
            if error_message:
                raise RuntimeError(QA01.get_formated_error_message(error_message, lote_inspecao.texto_breve))

        finally:
            tipo_mensagem = str(sap_session.FindById("wnd[0]/sbar/").MessageType)
            message = SAPGuiElements.get_text(sap_session, MESSAGE_ELEMENT)
            if tipo_mensagem and tipo_mensagem == 'S':
                # remessa criada com sucesso
                return QA01.get_batch_controller_number(message)

            else:
                # erro ao criar lote
                message = SAPGuiElements.get_text(sap_session, ERROR_MESSAGE_ELEMENT)
                raise RuntimeError(QA01.get_formated_error_message(message, lote_inspecao.texto_breve))

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
    def get_batch_controller_number(sucsses_message):
        return "".join(re.findall("\\d{12}", sucsses_message))


