import re

from sapgui import SAPGuiApplication
from sapguielements import SAPGuiElements, SAVE_BUTTON, MESSAGE_ELEMENT
from transaction import SAPTransaction

ORGANIZATION_ELEMENT = "wnd[0]/usr/ctxtVTTK-TPLST"
TRANSPORT_TYPE_ELEMENT = "wnd[0]/usr/cmbVTTK-SHTYP"
CNPJ_ELEMENT = "wnd[1]/usr/tabsG_SELONETABSTRIP/tabpTAB007/ssubSUBSCR_PRESEL:SAPLSDH4:0220/sub:SAPLSDH4:0220/txtG" \
               "_SELFLD_TAB-LOW[0,24]"
CPF_ELEMENT = "wnd[1]/usr/tabsG_SELONETABSTRIP/tabpTAB007/ssubSUBSCR_PRESEL:SAPLSDH4:0220/sub:SAPLSDH4:0220/txtG_SELFLD" \
              "_TAB-LOW[1,24]"
FILTER_BUTTOn_ELEMENT = "wnd[1]/tbar[0]/btn[17]"
CAR_TYPE_ELEMENT = "wnd[0]/usr/tabsHEADER_TABSTRIP1/tabpTABS_OV_PR/ssubG_HEADER_SUBSCREEN1:SAPMV56A:1021/ctxtVTTK-VSART"
BOARD_01_ELEMENT = "wnd[0]/usr/tabsHEADER_TABSTRIP1/tabpTABS_OV_PR/ssubG_HEADER_SUBSCREEN1:SAPMV56A:1021/txtVTTK-SIGNI"
SEALS_ELEMENT = "wnd[0]/usr/tabsHEADER_TABSTRIP1/tabpTABS_OV_PR/ssubG_HEADER_SUBSCREEN1:SAPMV56A:1021/ctxtVTTK-SDABW"
ORDER_NUMBER_ELEMENT = "wnd[0]/usr/tabsHEADER_TABSTRIP1/tabpTABS_OV_PR/ssubG_HEADER_SUBSCREEN1:SAPMV56A:1021/ctxtVTTK" \
                       "-EXTI1"


class VT01:
    @staticmethod
    def create(sap_session, document):
        SAPTransaction.call(sap_session, 'vt01n')
        SAPGuiElements.set_text(sap_session, ORGANIZATION_ELEMENT, "1000")
        sap_session.findById(TRANSPORT_TYPE_ELEMENT).key = "ZDIR"
        SAPGuiElements.press_keyboard_keys(sap_session, "Enter")
        sap_session.findById("wnd[0]").sendVKey(4)
        SAPGuiElements.press_button(sap_session, FILTER_BUTTOn_ELEMENT)

        # campo para o selecionar o primeiro elemento da tabela caso encontre um transportador
        element_one = "wnd[1]/usr/lbl[1,5]"
        # verificando se é um cnpj
        if re.findall("^\\d{14}$", document):
            SAPGuiElements.set_text(sap_session, CNPJ_ELEMENT, document)

        elif re.findall("^\\d{11}$", document):
            SAPGuiElements.set_text(sap_session, CPF_ELEMENT, document)
            element_one = "wnd[1]/usr/lbl[1,3]"
        else:
            return "CNPJ ou CPF Inválido!"

        SAPGuiElements.press_keyboard_keys(sap_session, "Enter")

        error_message = SAPGuiElements.get_text(sap_session, "wnd[0]/sbar")
        if error_message:
            return error_message

        else:
            # selecionando o primeiro elemento da tabela
            sap_session.findById(element_one).setFocus()
            SAPGuiElements.press_keyboard_keys(sap_session, "Enter")

            SAPGuiElements.set_text(sap_session, CAR_TYPE_ELEMENT, "06")
            SAPGuiElements.set_text(sap_session, BOARD_01_ELEMENT, "KSL1089")
            SAPGuiElements.set_text(sap_session, SEALS_ELEMENT, "ZC")
            SAPGuiElements.set_text(sap_session, ORDER_NUMBER_ELEMENT, "45004584578")
            SAPGuiElements.press_keyboard_keys(sap_session, "Enter")


session = SAPGuiApplication.connect()
print(VT01.create(session, "12229415001435"))
