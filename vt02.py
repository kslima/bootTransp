from sapgui import SAPGuiApplication
from sapguielements import SAPGuiElements, SAVE_BUTTON
from transaction import SAPTransaction

ELEMENTO_NUMERO_TRANSPORTE = "wnd[0]/usr/ctxtVTTK-TKNUM"
ELEMENTO_NUMERO_INSPECAO_VEICULAR = "wnd[0]/usr/tabsHEADER_TABSTRIP1/tabpTABS_OV_ID/ssubG_HEADER_SUBSCREEN1" \
                                    ":SAPMV56A:1022/txtVTTK-EXTI2"
ELEMENTO_ABA_IDENTIFICACAO = "wnd[0]/usr/tabsHEADER_TABSTRIP1/tabpTABS_OV_ID"


class VT02:

    @staticmethod
    def inserir_inspecao_veicular(sap_session, numero_transporte, numero_inspecao_veicular):
        SAPTransaction.call(sap_session, 'vt02n')
        SAPGuiElements.set_text(sap_session, ELEMENTO_NUMERO_TRANSPORTE, numero_transporte)
        SAPGuiElements.press_keyboard_keys(sap_session, "Enter")

        SAPGuiElements.select_element(sap_session, ELEMENTO_ABA_IDENTIFICACAO)
        SAPGuiElements.set_text(sap_session, ELEMENTO_NUMERO_INSPECAO_VEICULAR, numero_inspecao_veicular)
        SAPGuiElements.press_button(sap_session, SAVE_BUTTON)

        tipo_mensagem = SAPGuiElements.get_sbar_message_type(sap_session)
        if tipo_mensagem and tipo_mensagem == 'S':
            return True, ""
        return False, "Erro ao inserir inspecao {} no transporte {}".format(numero_inspecao_veicular, numero_transporte)
