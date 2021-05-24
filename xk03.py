import re

from model2 import Transportador
from sapgui import SAPGuiApplication
from sapguielements import SAPGuiElements
from service import MunicipioService
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
ELEMENTO_CPF = "wnd[0]/usr/txtLFA1-STCD2"
ELEMENTO_CODIGO_MUNICIPIO = "wnd[0]/usr/ctxtLFA1-TXJCD"
ELEMENTO_ABA_INFORMACOES_FISCAIS = "wnd[1]/usr/tabsG_SELONETABSTRIP/tabpTAB006"
ELEMENTO_PESQUISA_CNPJ = "wnd[1]/usr/tabsG_SELONETABSTRIP/tabpTAB006/ssubSUBSCR_PRESEL:SAPLSDH4:0220/sub:" \
                         "SAPLSDH4:0220/txtG_SELFLD_TAB-LOW[0,24]"
ELEMENTO_PESQUISA_CPF = "wnd[1]/usr/tabsG_SELONETABSTRIP/tabpTAB006/ssubSUBSCR_PRESEL:SAPLSDH4:0220/sub:SAPLSDH4:" \
                        "0220/txtG_SELFLD_TAB-LOW[1,24]"


class XK03:

    @staticmethod
    def pesquisar_transportador(sap_session, criterio):
        try:
            if len(criterio) != 7:
                criterio = XK03.__pesquisar_codigo_transportador_por_cnpj_ou_cpf(sap_session, criterio)
            XK03.__abrir_transacao(sap_session, criterio)
            nome = SAPGuiElements.get_text(sap_session, ELEMENTO_NOME)

            SAPGuiElements.press_button(sap_session, ELEMENTO_PROXIMA_PAGINA)
            identificador = SAPGuiElements.get_text(sap_session, ELEMENTO_CNPJ)
            if not identificador:
                identificador = SAPGuiElements.get_text(sap_session, ELEMENTO_CPF)

            codigo_municipio = SAPGuiElements.get_text(sap_session, ELEMENTO_CODIGO_MUNICIPIO)
            codigo_municipio = "".join(re.findall("\\d*", codigo_municipio))
            municipio = MunicipioService.pesquisar_municipio_pelo_codigo(codigo_municipio)
            if municipio is None:
                raise RuntimeError('Não possivel definir o municipio do transportador!')

            transportador = Transportador()
            transportador.nome = nome
            transportador.codigo_sap = criterio
            transportador.cnpj_cpf = identificador
            transportador.municipio = municipio
            transportador.save()
            return transportador
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            raise e

    @staticmethod
    def __abrir_campo_pesquisa_por_cnpj_cpf(sap_session):
        SAPGuiElements.send_key(sap_session, 4)
        SAPGuiElements.select_element(sap_session, ELEMENTO_ABA_INFORMACOES_FISCAIS)

    @staticmethod
    def __pesquisar_codigo_transportador_por_cnpj_ou_cpf(sap_session, criterio):
        try:
            XK03.__abrir_campo_pesquisa_por_cnpj_cpf(sap_session)
            cnpj = len(criterio) == 14
            SAPGuiElements.set_text(sap_session, ELEMENTO_PESQUISA_CNPJ if cnpj else ELEMENTO_PESQUISA_CPF,
                                    criterio)
            SAPGuiElements.enter(sap_session)
            msg_nenhum_resultado = SAPGuiElements.verificar_mensagem_barra_inferior(sap_session)
            if msg_nenhum_resultado:
                raise RuntimeError(msg_nenhum_resultado)

            SAPGuiElements.enter(sap_session)
            return SAPGuiElements.get_text(sap_session, ELEMENTO_CODIGO_FORNECEDOR)

        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            raise e

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
    XK03.pesquisar_transportador(session, '')
