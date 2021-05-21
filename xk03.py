from sapguielements import SAPGuiElements
from transaction import SAPTransaction

class XK03:

    @staticmethod
    def __abrir_transacao(sap_session):
        SAPTransaction.call(sap_session, 'vt01n')
        SAPGuiElements.set_text(sap_session, ELEMENTO_ORGANIZACAO, "1000")
        sap_session.findById(ELEMENTO_TIPO_TRANSPORTE).key = "ZDIR"
        SAPGuiElements.press_keyboard_keys(sap_session, "Enter")