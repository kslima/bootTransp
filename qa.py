import re

from sapguielements import SAPGuiElements, SAVE_BUTTON, MESSAGE_ELEMENT
from transaction import SAPTransaction
import sys, traceback

ELEMENTO_CODIGO_PRODUTO = "wnd[0]/usr/ctxtQALS-MATNR"
ELEMENTO_CENTRO = "wnd[0]/usr/ctxtQALS-WERK"
CENTRO = "1014"
ELEMENTO_LOTE_ORIGEM = "wnd[0]/usr/ctxtQALS-HERKUNFT"
LOTE_ORIGEM = "89"
ELEMENTO_LOTE = "wnd[0]/usr/subLOT_HEADER:SAPLQPL1:1102/ctxtQALS-CHARG"
ELEMENTO_DEPOSITO = "wnd[0]/usr/subLOT_HEADER:SAPLQPL1:1102/ctxtQALS-LAGORTCHRG"
ELEMENTO_QUANTIDADE_LOTE = "wnd[0]/usr/tabsTABSTRIP/tabpHERK/ssubSUBSCR_TABSTRIP:SAPLQPL1:0212/txtQALS-LOSMENGE"
QUANTIDADE_LOTES = "1"
ELEMENTO_TXT_BREVE_INSP_VEICULO = "wnd[0]/usr/tabsTABSTRIP/tabpHERK/ssubSUBSCR_TABSTRIP:SAPLQPL1:0201/txtQALS-KTEXTLOS"
ELEMENTO_TXT_BREVE_INSP_PRODUTO = "wnd[0]/usr/tabsTABSTRIP/tabpHERK/ssubSUBSCR_TABSTRIP:SAPLQPL1:0212/txtQALS-KTEXTLOS"
OPTIONAL_CREATE = "wnd[1]/usr/btnSPOP-OPTION1"
ERROR_MESSAGE_ELEMENT = "wnd[1]/usr/txtMESSTXT1"


class QA01:
    @staticmethod
    def create(sap_session, lote_inspecao):
        try:
            SAPTransaction.call(sap_session, 'qa01')
            SAPGuiElements.set_text(sap_session, ELEMENTO_CODIGO_PRODUTO, lote_inspecao.material)
            SAPGuiElements.set_text(sap_session, ELEMENTO_CENTRO, CENTRO)
            SAPGuiElements.set_text(sap_session, ELEMENTO_LOTE_ORIGEM, lote_inspecao.origem)
            SAPGuiElements.press_keyboard_keys(sap_session, "Enter")

            # verificando se o lote é de inspecao de produto(89) ou de veiculo(07)
            inspecionando_produto = lote_inspecao.origem == "89"
            if inspecionando_produto:
                sap_session.findById("wnd[1]/usr/lbl[1,3]").setFocus()
                SAPGuiElements.press_keyboard_keys(sap_session, "Enter")
                SAPGuiElements.set_text(sap_session, ELEMENTO_QUANTIDADE_LOTE, QUANTIDADE_LOTES)
                SAPGuiElements.set_text(sap_session, ELEMENTO_TXT_BREVE_INSP_PRODUTO, lote_inspecao.texto_breve)
            else:
                SAPGuiElements.set_text(sap_session, ELEMENTO_TXT_BREVE_INSP_VEICULO, lote_inspecao.texto_breve)

            # o lote e o deposito sao setados agora pq caso o lote seja de inspecao de produto, o sap mostra uma
            # mensagem antes de abrir a tela do lote
            SAPGuiElements.set_text(sap_session, ELEMENTO_LOTE, lote_inspecao.lote)
            SAPGuiElements.set_text(sap_session, ELEMENTO_DEPOSITO,
                                    lote_inspecao.deposito if lote_inspecao.deposito is not None else '')

            SAPGuiElements.salvar(sap_session)

            try:
                SAPGuiElements.press_button(sap_session, OPTIONAL_CREATE)
                error_message = SAPGuiElements.get_text(sap_session, ERROR_MESSAGE_ELEMENT)
                if error_message:
                    raise RuntimeError(QA01.get_formated_error_message(error_message, lote_inspecao.texto_breve))

            except AttributeError:
                pass

            mensagem = SAPGuiElements.verificar_mensagem_barra_inferior(sap_session)
            return QA01.get_batch_controller_number(mensagem)

        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            raise e

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
