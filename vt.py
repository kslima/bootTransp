import re

from sapgui import SAPGuiApplication
from sapguielements import SAPGuiElements, SAVE_BUTTON, MESSAGE_ELEMENT
from transaction import SAPTransaction
import sys
import traceback

ELEMENTO_CODIGO_TRANSPORTADOR = "wnd[0]/usr/tabsHEADER_TABSTRIP1/tabpTABS_OV_PR/ssubG_HEADER_SUBSCREEN1:SAPMV56A:1021" \
                                "/ctxtVTTK-TDLNR"
ELEMENTO_ORGANIZACAO = "wnd[0]/usr/ctxtVTTK-TPLST"
ELEMENTO_TIPO_TRANSPORTE = "wnd[0]/usr/cmbVTTK-SHTYP"
ELEMENTO_CNPJ = "wnd[1]/usr/tabsG_SELONETABSTRIP/tabpTAB007/ssubSUBSCR_PRESEL:SAPLSDH4:0220/sub:SAPLSDH4:0220/txtG" \
                "_SELFLD_TAB-LOW[0,24]"
ELEMENTO_CPF = "wnd[1]/usr/tabsG_SELONETABSTRIP/tabpTAB007/ssubSUBSCR_PRESEL:SAPLSDH4:0220/sub:SAPLSDH4:0220/" \
               "txtG_SELFLD_TAB-LOW[1,24]"
FILTER_BUTTOn_ELEMENT = "wnd[1]/tbar[0]/btn[17]"
CAR_TYPE_ELEMENT = "wnd[0]/usr/tabsHEADER_TABSTRIP1/tabpTABS_OV_PR/ssubG_HEADER_SUBSCREEN1:SAPMV56A:1021/ctxtVTTK-VSART"
ELEMENTO_PLACA_CAVALO = "wnd[0]/usr/tabsHEADER_TABSTRIP1/tabpTABS_OV_PR/ssubG_HEADER_SUBSCREEN1:SAPMV56A:1021/txtVTTK" \
                        "-SIGNI"
ELEMENTO_LACRES = "wnd[0]/usr/tabsHEADER_TABSTRIP1/tabpTABS_OV_PR/ssubG_HEADER_SUBSCREEN1:SAPMV56A:1021/ctxtVTTK-SDABW"
ELEMENTO_NUMERO_PEDIDO = "wnd[0]/usr/tabsHEADER_TABSTRIP1/tabpTABS_OV_PR/ssubG_HEADER_SUBSCREEN1:SAPMV56A:1021" \
                         "/ctxtVTTK-EXTI1"
ELEMENT_ABA_TXTS = "wnd[0]/usr/tabsHEADER_TABSTRIP2/tabpTABS_OV_TX"
ELEMENT_TXT_FIELDS = "wnd[0]/usr/tabsHEADER_TABSTRIP2/tabpTABS_OV_TX/ssubG_HEADER_SUBSCREEN2:SAPMV56A:1034/" \
                     "subTEXTEDIT:SAPLV70T:2101/cntlSPLITTER_CONTAINER/shellcont/shellcont/shell/shellcont[0]/shell"
ELEMENT_TXT_SELECTED_FIELD = "wnd[0]/usr/tabsHEADER_TABSTRIP2/tabpTABS_OV_TX/ssubG_HEADER_SUBSCREEN2:SAPMV56A:1034/" \
                             "subTEXTEDIT:SAPLV70T:2101/cntlSPLITTER_CONTAINER/shellcont/shellcont/shell/shellcont[1]" \
                             "/shell"
ELEMENT_ADC_DATAS = "wnd[0]/usr/tabsHEADER_TABSTRIP2/tabpTABS_OV_AI"
ELEMENTO_MUNICIPIO_PLACA_01 = "wnd[0]/usr/tabsHEADER_TABSTRIP2/tabpTABS_OV_AI/ssubG_HEADER_SUBSCREEN2:SAPMV56A" \
                              ":1030/ctxtVTTK-ADD01"
ELEMENTO_MUNICIPIO_PLACA_02 = "wnd[0]/usr/tabsHEADER_TABSTRIP2/tabpTABS_OV_AI/ssubG_HEADER_SUBSCREEN2:SAPMV56A" \
                              ":1030/ctxtVTTK-ADD02"
ELEMENTO_MUNICIPIO_PLACA_03 = "wnd[0]/usr/tabsHEADER_TABSTRIP2/tabpTABS_OV_AI/ssubG_HEADER_SUBSCREEN2:SAPMV56A" \
                              ":1030/ctxtVTTK-ADD03"
ELEMENTO_MUNICIPIO_PLACA_04 = "wnd[0]/usr/tabsHEADER_TABSTRIP2/tabpTABS_OV_AI/ssubG_HEADER_SUBSCREEN2:SAPMV56A" \
                              ":1030/ctxtVTTK-ADD04"
ELEMENTO_PLACA_02 = "wnd[0]/usr/tabsHEADER_TABSTRIP2/tabpTABS_OV_AI/ssubG_HEADER_SUBSCREEN2:SAPMV56A:1030/txtVTTK-TEXT1"
ELEMENTO_PLACA_03 = "wnd[0]/usr/tabsHEADER_TABSTRIP2/tabpTABS_OV_AI/ssubG_HEADER_SUBSCREEN2:SAPMV56A:1030/txtVTTK-TEXT2"
ELEMENTO_PLACA_04 = "wnd[0]/usr/tabsHEADER_TABSTRIP2/tabpTABS_OV_AI/ssubG_HEADER_SUBSCREEN2:SAPMV56A:1030/txtVTTK-TEXT3"
ELEMENTO_LOTE_PRODUTO = "wnd[0]/usr/tabsHEADER_TABSTRIP2/tabpTABS_OV_AI/ssubG_HEADER_SUBSCREEN2:SAPMV56A:1030" \
                        "/txtVTTK-TEXT4"

ELEMENTO_BOTAO_ADICIONAR_REMESSAS = "wnd[0]/tbar[1]/btn[6]"
ELEMENTO_BOTAO_ADICIONAR_MAIS_REMESSAS = "wnd[1]/usr/btn%_S_VBELN_%_APP_%-VALU_PUSH"
ELEMENT_SHIPPING_FIELDS = "wnd[2]/usr/tabsTAB_STRIP/tabpSIVA/ssubSCREEN_HEADER:SAPLALDB:3010/tblSAPLALDBSINGLE/" \
                          "ctxtRSCSEL_255-SLOW_I[1,{}]"

ELEMENT_EXECUTE_BUTTON_1 = "wnd[2]/tbar[0]/btn[8]"
ELEMENT_EXECUTE_BUTTON_2 = "wnd[1]/tbar[0]/btn[8]"
ELEMENTO_SINTESE = "wnd[0]/tbar[1]/btn[16]"

ELEMENTO_ORGANIZAR_TRANSPORTE = "wnd[0]/usr/tabsHEADER_TABSTRIP2/tabpTABS_OV_DE/ssubG_HEADER_SUBSCREEN2:SAPMV56A" \
                                ":1025/btn*RV56A-ICON_STDIS"
ELEMENTO_ABA_DADOS = "wnd[0]/usr/tabsHEADER_TABSTRIP2/tabpTABS_OV_DE"

# ELEMENTOS VT02
ELEMENTO_NUMERO_TRANSPORTE = "wnd[0]/usr/ctxtVTTK-TKNUM"
ELEMENTO_NUMERO_INSPECAO_VEICULAR = "wnd[0]/usr/tabsHEADER_TABSTRIP1/tabpTABS_OV_ID/ssubG_HEADER_SUBSCREEN1" \
                                    ":SAPMV56A:1022/txtVTTK-EXTI2"
ELEMENTO_ABA_IDENTIFICACAO = "wnd[0]/usr/tabsHEADER_TABSTRIP1/tabpTABS_OV_ID"


class VT01:
    @staticmethod
    def create(sap_session, carregamento):
        try:

            VT01.__abrir_transacao(sap_session)
            VT01.__inserir_codigo_transportador(sap_session, carregamento.transportador.codigo_sap)
            VT01.__inserir_dados_veiculo(sap_session, carregamento.veiculo)

            if carregamento.remessas[0].itens[0].produto.inspecao_produto == 1:
                VT01.__inserir_lote_controle_produto(sap_session, carregamento.lotes_qualidade[-1])
            SAPGuiElements.enter(sap_session)

            SAPGuiElements.verificar_mensagem_barra_inferior(sap_session)

            VT01.__inserir_dados_motorista(sap_session, carregamento.motorista)

            # verificando se é necessário lacres para esse produto
            tipo_lacres = carregamento.remessas[0].itens[0].produto.tipo_lacres
            if tipo_lacres != 0:
                VT01.__inserir_lacres(sap_session, tipo_lacres, carregamento.lacres)

            # verificando se há número de pedido
            if carregamento.numero_pedido:
                VT01.__inserir_pedido(sap_session, carregamento.numero_pedido)

            SAPGuiElements.enter(sap_session)

            VT01.__inserir_remessas(sap_session, carregamento.remessas)
            SAPGuiElements.press_button(sap_session, ELEMENTO_SINTESE)
            sap_session.findById(ELEMENTO_ABA_DADOS).select()
            SAPGuiElements.press_button(sap_session, ELEMENTO_ORGANIZAR_TRANSPORTE)

            SAPGuiElements.salvar(sap_session)

            message = SAPGuiElements.verificar_mensagem_barra_inferior(sap_session)
            transport_number = VT01.extrair_numero_transport(message)
            return transport_number

        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            raise e

    @staticmethod
    def __abrir_transacao(sap_session):
        SAPTransaction.call(sap_session, 'vt01n')
        SAPGuiElements.set_text(sap_session, ELEMENTO_ORGANIZACAO, "1000")
        sap_session.findById(ELEMENTO_TIPO_TRANSPORTE).key = "ZDIR"
        SAPGuiElements.press_keyboard_keys(sap_session, "Enter")

    @staticmethod
    def __inserir_codigo_transportador(sap_session, codigo_transportador):
        SAPGuiElements.set_text(sap_session, ELEMENTO_CODIGO_TRANSPORTADOR, codigo_transportador)
        SAPGuiElements.enter(sap_session)
        SAPGuiElements.verificar_mensagem_barra_inferior(sap_session)

    @staticmethod
    def __inserir_dados_veiculo(sap_session, veiculo):
        tipo_veiculo = veiculo.tipo_veiculo.codigo
        peso_balanca = veiculo.peso_balanca.codigo
        SAPGuiElements.set_text(sap_session, CAR_TYPE_ELEMENT, tipo_veiculo)
        SAPGuiElements.set_text(sap_session, ELEMENTO_PLACA_CAVALO, veiculo.placa1)
        SAPGuiElements.set_text(sap_session, ELEMENTO_LACRES, peso_balanca)

        SAPGuiElements.select_element(sap_session, ELEMENT_ADC_DATAS)

        print(str(veiculo.municipio_placa1))
        SAPGuiElements.set_text(sap_session, ELEMENTO_MUNICIPIO_PLACA_01,
                                '{} {}'.format(veiculo.municipio_placa1.uf,
                                               veiculo.municipio_placa1
                                               .codigo))

        if veiculo.placa2:
            SAPGuiElements.set_text(sap_session, ELEMENTO_MUNICIPIO_PLACA_02,
                                    '{} {}'.format(veiculo.municipio_placa2.uf,
                                                   veiculo.municipio_placa2
                                                   .codigo))
            SAPGuiElements.set_text(sap_session, ELEMENTO_PLACA_02, veiculo.placa2)
        if veiculo.placa3:
            SAPGuiElements.set_text(sap_session, ELEMENTO_MUNICIPIO_PLACA_03,
                                    '{} {}'.format(veiculo.municipio_placa3.uf,
                                                   veiculo.municipio_placa3
                                                   .codigo))
            SAPGuiElements.set_text(sap_session, ELEMENTO_PLACA_03, veiculo.placa3)
        if veiculo.placa4:
            SAPGuiElements.set_text(sap_session, ELEMENTO_MUNICIPIO_PLACA_04,
                                    '{} {}'.format(veiculo.municipio_placa4.uf,
                                                   veiculo.municipio_placa4
                                                   .codigo))
            SAPGuiElements.set_text(sap_session, ELEMENTO_PLACA_04, veiculo.placa4)

    @staticmethod
    def __inserir_dados_motorista(sap_session, motorista):
        sap_session.findById(ELEMENT_ABA_TXTS).select()
        VT01.insert_item_text(sap_session, "ZMOT", motorista.nome)
        VT01.insert_item_text(sap_session, "ZCPF", motorista.cpf)
        VT01.insert_item_text(sap_session, "ZCNH", motorista.cnh)
        VT01.insert_item_text(sap_session, "ZNRG", motorista.rg)

    @staticmethod
    def __inserir_lacres(sap_session, tipo_lacres, lacres):
        lacres = lacres.replace("/", "/\n")
        sap_session.findById(ELEMENT_ABA_TXTS).select()
        # lacres normais
        if tipo_lacres == 1:
            VT01.insert_item_text(sap_session, "ZLAC", lacres)

        # lacres lona
        elif tipo_lacres == 2:
            VT01.insert_item_text(sap_session, "ZLON", lacres)

    @staticmethod
    def __inserir_pedido(sap_session, pedido):
        SAPGuiElements.set_text(sap_session, ELEMENTO_NUMERO_PEDIDO, pedido)

    @staticmethod
    def __inserir_remessas(sap_session, remessas):
        try:
            SAPGuiElements.press_button(sap_session, ELEMENTO_BOTAO_ADICIONAR_REMESSAS)

            remover_a = remessas[0].itens[0].produto.remover_a == 1
            if remover_a:
                VT01.__remover_a(sap_session)

            SAPGuiElements.press_button(sap_session, ELEMENTO_BOTAO_ADICIONAR_MAIS_REMESSAS)
            cont = 0
            for remessa in remessas:
                field = ELEMENT_SHIPPING_FIELDS.format(cont)
                sap_session.findById(field).text = remessa.numero_remessa
                cont = cont + 1

            SAPGuiElements.press_button(sap_session, ELEMENT_EXECUTE_BUTTON_1)
            SAPGuiElements.press_button(sap_session, ELEMENT_EXECUTE_BUTTON_2)

            mensagem = SAPGuiElements.verificar_mensagem_barra_inferior(sap_session)
            total_remessas_adicionadas = "".join(re.findall("\\d*", mensagem))
            total_remessas_adicionadas = int(total_remessas_adicionadas)
            total_remessas = len(remessas)

            if total_remessas_adicionadas != total_remessas:
                raise RuntimeError('Erro ao adicionar remessas!')

        except Exception as e:
            raise e

    @staticmethod
    def __remover_a(sap_session):
        SAPGuiElements.set_text(sap_session, "wnd[1]/usr/ctxtS_WBSTK-LOW", "")
        SAPGuiElements.set_text(sap_session, "wnd[1]/usr/ctxtS_TRSTA-LOW", "")
        SAPGuiElements.set_text(sap_session, "wnd[1]/usr/ctxtS_TRSTA-HIGH", "")

    @staticmethod
    def __inserir_lote_controle_produto(sap_session, lote_qualidade_produto):
        SAPGuiElements.set_text(sap_session, ELEMENTO_LOTE_PRODUTO, lote_qualidade_produto.numero_lote)

    @staticmethod
    def insert_item_text(sap_session, field, valor):
        SAPGuiElements.select_item(sap_session, ELEMENT_TXT_FIELDS, field, "column1")
        SAPGuiElements.ensure_visible_horizontal_item(sap_session, ELEMENT_TXT_FIELDS, field, "column1")
        SAPGuiElements.double_click_element(sap_session, ELEMENT_TXT_FIELDS, field, "column1")
        SAPGuiElements.set_item_text(sap_session, ELEMENT_TXT_SELECTED_FIELD, valor)

    @staticmethod
    def extrair_numero_transport(sucsses_message):
        return "".join(re.findall("\\d*", sucsses_message))

    @staticmethod
    def pesquisar_transportador(sap_session, numero_documento):

        VT01.__abrir_transacao(sap_session)

        if re.findall("^\\d{7}$", numero_documento):
            return VT01.pesquisar_transportador_por_codigo(sap_session, numero_documento)

        sap_session.findById("wnd[0]").sendVKey(4)
        SAPGuiElements.press_button(sap_session, FILTER_BUTTOn_ELEMENT)

        # campo para o selecionar o primeiro elemento da tabela caso encontre um transportador
        primeiro_elemento = "wnd[1]/usr/lbl[1,5]"
        # verificando se é um cnpj
        if re.findall("^\\d{14}$", numero_documento):
            SAPGuiElements.set_text(sap_session, ELEMENTO_CNPJ, numero_documento)

        elif re.findall("^\\d{11}$", numero_documento):
            SAPGuiElements.set_text(sap_session, ELEMENTO_CPF, numero_documento)
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

    @staticmethod
    def pesquisar_transportador_por_codigo(sap_session, codigo_transportador):
        SAPGuiElements.set_text(sap_session, "wnd[0]/usr/tabsHEADER_TABSTRIP1/tabpTABS_OV_PR/ssubG_HEADER_SUBSCREEN1:"
                                             "SAPMV56A:1021/ctxtVTTK-TDLNR", codigo_transportador)
        SAPGuiElements.enter(sap_session)
        SAPGuiElements.verificar_mensagem_barra_inferior(sap_session)
        endereco_transportador = SAPGuiElements.get_text(sap_session, "wnd[0]/usr/tabsHEADER_TABSTRIP1/tabpTABS_OV"
                                                                      "_PR/ssubG_HEADER_SUBSCREEN1:SAPMV56A:1021/"
                                                                      "txtVTTKD-TXTSP")
        SAPTransaction.exit_transaction(sap_session)
        return True, codigo_transportador, endereco_transportador


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
