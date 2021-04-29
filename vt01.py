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
ELEMENT_ABA_TXTS = "wnd[0]/usr/tabsHEADER_TABSTRIP2/tabpTABS_OV_TX"
ELEMENT_TXT_FIELDS = "wnd[0]/usr/tabsHEADER_TABSTRIP2/tabpTABS_OV_TX/ssubG_HEADER_SUBSCREEN2:SAPMV56A:1034/" \
                     "subTEXTEDIT:SAPLV70T:2101/cntlSPLITTER_CONTAINER/shellcont/shellcont/shell/shellcont[0]/shell"
ELEMENT_TXT_SELECTED_FIELD = "wnd[0]/usr/tabsHEADER_TABSTRIP2/tabpTABS_OV_TX/ssubG_HEADER_SUBSCREEN2:SAPMV56A:1034/" \
                             "subTEXTEDIT:SAPLV70T:2101/cntlSPLITTER_CONTAINER/shellcont/shellcont/shell/shellcont[1]" \
                             "/shell"
ELEMENT_ADC_DATAS = "wnd[0]/usr/tabsHEADER_TABSTRIP2/tabpTABS_OV_AI"
ELEMENT_MUN_BOARD_1 = "wnd[0]/usr/tabsHEADER_TABSTRIP2/tabpTABS_OV_AI/ssubG_HEADER_SUBSCREEN2:SAPMV56A" \
                      ":1030/ctxtVTTK-ADD01"
ELEMENT_MUN_BOARD_2 = "wnd[0]/usr/tabsHEADER_TABSTRIP2/tabpTABS_OV_AI/ssubG_HEADER_SUBSCREEN2:SAPMV56A" \
                      ":1030/ctxtVTTK-ADD02"
ELEMENT_MUN_BOARD_3 = "wnd[0]/usr/tabsHEADER_TABSTRIP2/tabpTABS_OV_AI/ssubG_HEADER_SUBSCREEN2:SAPMV56A" \
                      ":1030/ctxtVTTK-ADD03"
ELEMENT_MUN_BOARD_4 = "wnd[0]/usr/tabsHEADER_TABSTRIP2/tabpTABS_OV_AI/ssubG_HEADER_SUBSCREEN2:SAPMV56A" \
                      ":1030/ctxtVTTK-ADD04"
ELEMENT_BOARD_1 = "wnd[0]/usr/tabsHEADER_TABSTRIP2/tabpTABS_OV_AI/ssubG_HEADER_SUBSCREEN2:SAPMV56A:1030/txtVTTK-TEXT1"
ELEMENT_BOARD_2 = "wnd[0]/usr/tabsHEADER_TABSTRIP2/tabpTABS_OV_AI/ssubG_HEADER_SUBSCREEN2:SAPMV56A:1030/txtVTTK-TEXT2"
ELEMENT_BOARD_3 = "wnd[0]/usr/tabsHEADER_TABSTRIP2/tabpTABS_OV_AI/ssubG_HEADER_SUBSCREEN2:SAPMV56A:1030/txtVTTK-TEXT3"
ELEMENT_BOARD_4 = "wnd[0]/usr/tabsHEADER_TABSTRIP2/tabpTABS_OV_AI/ssubG_HEADER_SUBSCREEN2:SAPMV56A:1030/txtVTTK-TEXT4"

ELEMENT_ADD_SHIPPING_BUTTON = "wnd[0]/tbar[1]/btn[6]"
ELEMENT_ADD_SHIPPING_MORE_BUTTON = "wnd[1]/usr/btn%_S_VBELN_%_APP_%-VALU_PUSH"
ELEMENT_SHIPPING_FIELDS = "wnd[2]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/" \
                          "ctxtRSCSEL_255-SLOW_I[1,{}]"

ELEMENT_EXECUTE_BUTTON_1 = "wnd[2]/tbar[0]/btn[8]"
ELEMENT_EXECUTE_BUTTON_2 = "wnd[1]/tbar[0]/btn[8]"
ELEMENT_SINT_BUTTON = "wnd[0]/tbar[1]/btn[16]"

ELEMENT_ORG_BUTTON = "wnd[0]/usr/tabsHEADER_TABSTRIP2/tabpTABS_OV_DE/ssubG_HEADER_SUBSCREEN2:SAPMV56A" \
                     ":1025/btn*RV56A-ICON_STDIS"
ELEMENT_ABA_DATES = "wnd[0]/usr/tabsHEADER_TABSTRIP2/tabpTABS_OV_DE"


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

            sap_session.findById(ELEMENT_ABA_TXTS).select()

            # lacres
            VT01.insert_item_text(sap_session, "ZLAC", "0075281\n0075282\n0075283\n0075283\n0075283\n0075283\n0075283"
                                                       "\n0075283\n0075283\n0075283\n0075283\n0075283")
            # motorista
            VT01.insert_item_text(sap_session, "ZMOT", "KLEUDER LIMA")
            # cpf
            VT01.insert_item_text(sap_session, "ZCPF", "077.124.104-61")
            # cnh
            VT01.insert_item_text(sap_session, "ZCNH", "004578127")
            # rg
            VT01.insert_item_text(sap_session, "ZNRG", "MG-18475387 SSP/MG")

            sap_session.findById(ELEMENT_ADC_DATAS).select()
            SAPGuiElements.set_text(sap_session, ELEMENT_MUN_BOARD_1, "MG 3143302")
            SAPGuiElements.set_text(sap_session, ELEMENT_MUN_BOARD_2, "MG 3143302")
            SAPGuiElements.set_text(sap_session, ELEMENT_MUN_BOARD_3, "MG 3143302")
            SAPGuiElements.set_text(sap_session, ELEMENT_MUN_BOARD_4, "MG 3143302")

            SAPGuiElements.set_text(sap_session, ELEMENT_BOARD_1, "KSL1189")
            SAPGuiElements.set_text(sap_session, ELEMENT_BOARD_2, "KSL1289")
            SAPGuiElements.set_text(sap_session, ELEMENT_BOARD_3, "KSL1389")
            # SAPGuiElements.set_text(sap_session, ELEMENT_BOARD_4, "KSL1389")

            SAPGuiElements.press_keyboard_keys(sap_session, "Enter")

            error_message = SAPGuiElements.get_text(sap_session, "wnd[0]/sbar")
            if not error_message:
                SAPGuiElements.press_button(sap_session, ELEMENT_ADD_SHIPPING_BUTTON)
                SAPGuiElements.press_button(sap_session, ELEMENT_ADD_SHIPPING_MORE_BUTTON)
                shippings = ["80680693"]
                VT01.add_shippings(sap_session, shippings)

                SAPGuiElements.press_button(sap_session, ELEMENT_EXECUTE_BUTTON_1)
                SAPGuiElements.press_button(sap_session, ELEMENT_EXECUTE_BUTTON_2)
                message = SAPGuiElements.get_text(sap_session, "wnd[0]/sbar")
                total_add_shipping = "".join(re.findall("\\d*", message))
                total_add_shipping = int(total_add_shipping)
                total_shipping = len(shippings)

                if total_add_shipping == total_shipping:
                    SAPGuiElements.press_button(sap_session, ELEMENT_SINT_BUTTON)
                    sap_session.findById(ELEMENT_ABA_DATES).select()
                    SAPGuiElements.press_button(sap_session, ELEMENT_ORG_BUTTON)
                    SAPGuiElements.press_button(sap_session, SAVE_BUTTON)

                    message = SAPGuiElements.get_text(sap_session, MESSAGE_ELEMENT)
                    if VT01.assert_sucsses_message(message):
                        transport_number = VT01.get_transport_number(message)
                        return True, "Transporte {} criado com sucesso!".format(transport_number)

                else:
                    return False, "Erro ao adicionar remessas!\n{} de {} remessas foram adicionadas!" \
                        .format(total_add_shipping, total_shipping)

    @staticmethod
    def insert_item_text(sap_session, field, value):
        SAPGuiElements.select_item(sap_session, ELEMENT_TXT_FIELDS, field, "column1")
        SAPGuiElements.ensure_visible_horizontal_item(sap_session, ELEMENT_TXT_FIELDS, field, "column1")
        SAPGuiElements.double_click_element(sap_session, ELEMENT_TXT_FIELDS, field, "column1")
        SAPGuiElements.set_item_text(sap_session, ELEMENT_TXT_SELECTED_FIELD, value)

    @staticmethod
    def add_shippings(sap_session, shippings):
        cont = 0
        for shipping in shippings:
            field = ELEMENT_SHIPPING_FIELDS.format(cont)
            sap_session.findById(field).text = shipping
            cont = cont + 1

    @staticmethod
    def assert_sucsses_message(message):
        # .MessageType usar esse metodo para verifiar o tipo de mensagem
        if re.findall("^(O transporte \\d* foi gravado)$", message.strip()):
            return True
        return False

    @staticmethod
    def get_transport_number(sucsses_message):
        return "".join(re.findall("\\d*", sucsses_message))

    @staticmethod
    def pesquisar_transportador(sap_session, numero_documento):

        SAPTransaction.call(sap_session, 'vt01n')
        SAPGuiElements.set_text(sap_session, ORGANIZATION_ELEMENT, "1000")
        sap_session.findById(TRANSPORT_TYPE_ELEMENT).key = "ZDIR"
        SAPGuiElements.press_keyboard_keys(sap_session, "Enter")
        sap_session.findById("wnd[0]").sendVKey(4)
        SAPGuiElements.press_button(sap_session, FILTER_BUTTOn_ELEMENT)

        # campo para o selecionar o primeiro elemento da tabela caso encontre um transportador
        primeiro_elemento = "wnd[1]/usr/lbl[1,5]"
        # verificando se é um cnpj
        if re.findall("^\\d{14}$", numero_documento):
            SAPGuiElements.set_text(sap_session, CNPJ_ELEMENT, numero_documento)

        elif re.findall("^\\d{11}$", numero_documento):
            SAPGuiElements.set_text(sap_session, CPF_ELEMENT, numero_documento)
            primeiro_elemento = "wnd[1]/usr/lbl[1,3]"

        else:
            return "CNPJ ou CPF Inválido!"

        SAPGuiElements.press_keyboard_keys(sap_session, "Enter")

        error_message = SAPGuiElements.get_text(sap_session, "wnd[0]/sbar")

        if error_message:
            SAPTransaction.exit_transaction(sap_session)
            return False, error_message

        else:
            # selecionando o primeiro elemento da tabela
            SAPGuiElements.press_keyboard_keys(sap_session, "Enter")
            SAPGuiElements.press_keyboard_keys(sap_session, "Enter")
            codigo_transportador = SAPGuiElements.get_text(sap_session, "wnd[0]/usr/tabsHEADER_TABSTRIP1/tabpTABS_OV_"
                                                                        "PR/ssubG_HEADER_SUBSCREEN1:SAPMV56A:1021"
                                                                        "/ctxtVTTK-TDLNR")

            endereco_transportador = SAPGuiElements.get_text(sap_session, "wnd[0]/usr/tabsHEADER_TABSTRIP1/tabpTABS_OV"
                                                                          "_PR/ssubG_HEADER_SUBSCREEN1:SAPMV56A:1021/"
                                                                          "txtVTTKD-TXTSP")

            print('codigo :' + codigo_transportador)
            SAPTransaction.exit_transaction(sap_session)
            return True, codigo_transportador, endereco_transportador

# session = SAPGuiApplication.connect()
# print(VT01.create(session, "12229415001435"))
