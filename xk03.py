from sapgui import SAPGuiApplication
from sapguielements import SAPGuiElements
from transaction import SAPTransaction
import sys
import traceback

ELEMENTO_CODIGO_FORNECEDOR = "wnd[0]/usr/ctxtRF02K-LIFNR"
ELEMENTO_ENDERECO = "wnd[0]/usr/chkRF02K-D0110"
ELEMENTO_CONTROLE = "wnd[0]/usr/chkRF02K-D0120"
ELEMENTO_UF = "wnd[0]/usr/subADDRESS:SAPLSZA1:0300/subCOUNTRY_SCREEN:SAPLSZA1:0301/ctxtADDR1_DATA-REGION"
ELEMENTO_NOME = "wnd[0]/usr/subADDRESS:SAPLSZA1:0300/subCOUNTRY_SCREEN:SAPLSZA1:0301/txtADDR1_DATA-NAME1"
ELEMENTO_CIDADE = "wnd[0]/usr/subADDRESS:SAPLSZA1:0300/subCOUNTRY_SCREEN:SAPLSZA1:0301/txtADDR1_DATA-CITY1"
ELEMENTO_PROXIMA_PAGINA = "wnd[0]/tbar[1]/btn[8]"
ELEMENTO_CNPJ = "wnd[0]/usr/txtLFA1-STCD1"


class XK03:

    @staticmethod
    def pesquisar_transportador(sap_session, codigo_fornecedor):
        try:
            XK03.__abrir_transacao(sap_session, codigo_fornecedor)
            print(SAPGuiElements.get_text(sap_session, ELEMENTO_NOME))
            print(SAPGuiElements.get_text(sap_session, ELEMENTO_CIDADE))
            print(SAPGuiElements.get_text(sap_session, ELEMENTO_UF))

            SAPGuiElements.press_button(sap_session, ELEMENTO_PROXIMA_PAGINA)
            print(SAPGuiElements.get_text(sap_session, ELEMENTO_CNPJ))

        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            raise e

    @staticmethod
    def pesquisar_transportador_por_cnpj():
        pass

    @staticmethod
    def pesquisar_transportador_por_cpf():
        pass

    @staticmethod
    def __abrir_transacao(sap_session, codigo_fornecedor):
        try:
            SAPTransaction.call(sap_session, 'xk03')
            SAPGuiElements.set_text(sap_session, ELEMENTO_CODIGO_FORNECEDOR, codigo_fornecedor)
            SAPGuiElements.marcar_elemento(sap_session, ELEMENTO_ENDERECO)
            SAPGuiElements.marcar_elemento(sap_session, ELEMENTO_CONTROLE)
            SAPGuiElements.enter(sap_session)
            SAPGuiElements.verificar_mensagem_barra_inferior(sap_session)
        except Exception as e:
            raise e

    @staticmethod
    def __extrair_dados():
        pass


if __name__ == '__main__':
    session = SAPGuiApplication.connect()
    XK03.pesquisar_transportador(session)