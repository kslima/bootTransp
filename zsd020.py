from sapgui import SAPGuiApplication
from sapguielements import SAPGuiElements
from transaction import SAPTransaction

ELEMENTO_LOCAL_NEGOCIOS = "wnd[0]/usr/ctxtP_WERKS-LOW"
ELEMENTO_ORGANIZACAO_VENDAS = "wnd[0]/usr/ctxtP_VKORG"
ELEMENTO_CANAL_DISTRIBUICAO = "wnd[0]/usr/ctxtP_VTWEG"
ELEMENTO_SETOR_VENDAS = "wnd[0]/usr/ctxtP_SPART"

ELEMENTO_EMISSOR_ORDEM = "wnd[0]/usr/ctxtR_KUNNR-LOW"
ELEMENTO_DATA_INICIAL = "wnd[0]/usr/ctxtS_AUDAT-LOW"
ELEMENTO_DATA_FINAL = "wnd[0]/usr/ctxtS_AUDAT-HIGH"

ELEMENTO_APENAS_ORDENS_VENDA = "wnd[0]/usr/radP_VAPEND"  # (selected)
ELEMENTO_INCLUIR_BLOQUEADAS = "wnd[0]/usr/chkP_BLOCK"  # (.selected = True)

ELEMENTO_CAMPO_CNPJ = "wnd[1]/usr/tabsG_SELONETABSTRIP/tabpTAB006/ssubSUBSCR_PRESEL:SAPLSDH4:0220/sub:SAPLSDH4:0220/" \
                      "txtG_SELFLD_TAB-LOW[0,24]"

ELEMENTO_BOTAO_SELECIONAR_LAYOUT = "wnd[0]/tbar[1]/btn[33]"

ELEMENTO_TABELA_LAYOUTS = "wnd[1]/usr/ssubD0500_SUBSCREEN:SAPLSLVC_DIALOG:0501/cntlG51_CONTAINER/shellcont/shell"

ELEMENTO_TABELA_ORDENS = "wnd[0]/usr/cntlGRID1/shellcont/shell"
ELEMENTO_COLUNA_DATA = "AUDAT"
ELEMENTO_COLUNA_ORDEM = "VBELN"
ELEMENTO_COLUNA_CLIENTE = "NAME"
ELEMENTO_COLUNA_CIDADE = "MCOD3"
ELEMENTO_COLUNA_UF = "REGIO"
ELEMENTO_COLUNA_QTD_ORDEM = "KWMENG"
ELEMENTO_COLUNA_QTD_SAIDA = "MENGE"
ELEMENTO_COLUNA_QTD_DISPONIVEL = "KBMENG"
ELEMENTO_COLUNA_MATERIAL = "MAKTX"
ELEMENTO_COLUNA_COD_MATERIAL = "MATNR"
ELEMENTO_COLUNA_PEDIDO = "BSTNK"
ELEMENTO_COLUNA_TIPO_ORDEM = "AUART"
ELEMENTO_COLUNA_NF_REFERENCIA = "XBLNR"
ELEMENTO_COLUNA_STATUS = "SPSTG"
ELEMENTO_COLUNA_CNPJ = "CPF_CNPJ"


class ZSD020:

    @staticmethod
    def consultar_saldo_cliente(sap_session):
        SAPTransaction.call(sap_session, 'zsd020')
        SAPGuiElements.set_text(sap_session, ELEMENTO_LOCAL_NEGOCIOS, '1014')
        SAPGuiElements.set_text(sap_session, ELEMENTO_ORGANIZACAO_VENDAS, '1000')
        SAPGuiElements.set_text(sap_session, ELEMENTO_CANAL_DISTRIBUICAO, '10')
        SAPGuiElements.set_text(sap_session, ELEMENTO_SETOR_VENDAS, '20')
        SAPGuiElements.select_element(sap_session, ELEMENTO_APENAS_ORDENS_VENDA)
        SAPGuiElements.set_checkbox(sap_session, ELEMENTO_INCLUIR_BLOQUEADAS)
        SAPGuiElements.set_focus(sap_session, ELEMENTO_EMISSOR_ORDEM)
        SAPGuiElements.send_key(sap_session, 4)

        SAPGuiElements.set_text(sap_session, ELEMENTO_CAMPO_CNPJ, '33453598010862')
        SAPGuiElements.enter(sap_session)
        SAPGuiElements.enter(sap_session)
        SAPGuiElements.send_key(sap_session, 8)
        SAPGuiElements.press_button(sap_session, ELEMENTO_BOTAO_SELECIONAR_LAYOUT)

        row = 0
        while row < sap_session.findById(ELEMENTO_TABELA_LAYOUTS).RowCount:
            nome_layout = session.findById(ELEMENTO_TABELA_LAYOUTS).GetCellValue(row, "TEXT")

            if nome_layout == 'KSLIMA':
                session.findById(ELEMENTO_TABELA_LAYOUTS).selectedRows = row
                session.findById(ELEMENTO_TABELA_LAYOUTS).setCurrentCell(row, "TEXT")
                session.findById(ELEMENTO_TABELA_LAYOUTS).firstVisibleRow = row
                session.findById(ELEMENTO_TABELA_LAYOUTS).clickCurrentCell()
                break
            row += 1

        row = 0
        while row < sap_session.findById(ELEMENTO_TABELA_ORDENS).RowCount:
            ordem = session.findById(ELEMENTO_TABELA_ORDENS).GetCellValue(row, ELEMENTO_COLUNA_ORDEM)
            ordem = str(int(ordem))
            data = session.findById(ELEMENTO_TABELA_ORDENS).GetCellValue(row, ELEMENTO_COLUNA_DATA)
            cidade = session.findById(ELEMENTO_TABELA_ORDENS).GetCellValue(row, ELEMENTO_COLUNA_CIDADE)
            uf = session.findById(ELEMENTO_TABELA_ORDENS).GetCellValue(row, ELEMENTO_COLUNA_UF)
            cliente = session.findById(ELEMENTO_TABELA_ORDENS).GetCellValue(row, ELEMENTO_COLUNA_CLIENTE)
            qtd = session.findById(ELEMENTO_TABELA_ORDENS).GetCellValue(row, ELEMENTO_COLUNA_QTD_ORDEM)
            qtd_saida = session.findById(ELEMENTO_TABELA_ORDENS).GetCellValue(row, ELEMENTO_COLUNA_QTD_SAIDA)
            qtd_disponivel = session.findById(ELEMENTO_TABELA_ORDENS).GetCellValue(row, ELEMENTO_COLUNA_QTD_DISPONIVEL)
            material = session.findById(ELEMENTO_TABELA_ORDENS).GetCellValue(row, ELEMENTO_COLUNA_MATERIAL)
            codigo_material = session.findById(ELEMENTO_TABELA_ORDENS).GetCellValue(row, ELEMENTO_COLUNA_COD_MATERIAL)
            pedido = session.findById(ELEMENTO_TABELA_ORDENS).GetCellValue(row, ELEMENTO_COLUNA_PEDIDO)
            tipo_ordem = session.findById(ELEMENTO_TABELA_ORDENS).GetCellValue(row, ELEMENTO_COLUNA_TIPO_ORDEM)
            status = session.findById(ELEMENTO_TABELA_ORDENS).GetCellValue(row, ELEMENTO_COLUNA_STATUS)
            cnpj = session.findById(ELEMENTO_TABELA_ORDENS).GetCellValue(row, ELEMENTO_COLUNA_CNPJ)
            print('produto: {} quantidade disponivel : {} ordem: {}'.format(material, qtd_disponivel, ordem))
            row += 1


if __name__ == '__main__':
    session = SAPGuiApplication.connect()
    ZSD020.consultar_saldo_cliente(session)
