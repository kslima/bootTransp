import time

from sapgui import SAPGuiApplication
from sapguielements import SAPGuiElements, SAVE_BUTTON, MESSAGE_ELEMENT
from transaction import SAPTransaction

ELEMENTO_LOTE_CONTROLE = "wnd[0]/usr/ctxtQALS-PRUEFLOS"
ELEMENTO_OPERACAO = "wnd[0]/usr/ctxtQAQEE-VORNR"
ELEMENTO_CENTRO = "wnd[0]/usr/ctxtQAQEE-PRPLATZWRK"
ELEMENTO_COLUNA_S = "wnd[0]/usr/tabsEE_DATEN/tabpSISP/ssubSUB_EE_DATEN:SAPLQEEM:0202/tblSAPLQEEMSUMPLUS/ctxtQAQEE" \
                    "-SUMPLUS[8,{}]"
ELEMENTO_BOTAO_SELECIONAR_TODOS = "wnd[0]/usr/tabsEE_DATEN/tabpSISP/ssubSUB_EE_DATEN:SAPLQEEM:0202/subSUB_" \
                                  "EE_FCODE:SAPLQEEM:5300/btnSELECT_ALL"

ELEMENTO_BOTAO_AVALIAR = "wnd[0]/usr/tabsEE_DATEN/tabpSISP/ssubSUB_EE_DATEN:SAPLQEEM:0202/subSUB_EE_FCODE:" \
                         "SAPLQEEM:5300/btnCLOSING"

ELEMENTO_BOTAO_PROXIMA_OPERACAO = "wnd[0]/usr/ssubPIC_GRO_EE:SAPLQEEM:5000/btnNAECHSTER_VORGANG"
ELEMENTO_BOTAO_GRAVAR_PRIMEIRO = "wnd[1]/usr/btnSPOP-OPTION1"
ELEMENTO_FILTRO_CARACTERISTICAS = "wnd[0]/usr/cmbQAQEE-MODUS"
ELEMENTO_TABELA_RESULTADOS = "wnd[0]/usr/tabsEE_DATEN/tabpSISP/ssubSUB_EE_DATEN:SAPLQEEM:0202/tblSAPLQEEMSUMPLUS"


class QE01:

    @staticmethod
    def criar(sap_session, numero_inspecao_veicular):
        return QE01.__abrir_transacao(sap_session, numero_inspecao_veicular)

    @staticmethod
    def __abrir_transacao(sap_session, numero_inspecao_veicular):
        SAPTransaction.call(sap_session, 'qe01')
        SAPGuiElements.set_text(sap_session, ELEMENTO_LOTE_CONTROLE, numero_inspecao_veicular)
        SAPGuiElements.set_text(sap_session, ELEMENTO_OPERACAO, "0010")
        SAPGuiElements.set_text(sap_session, ELEMENTO_CENTRO, "1014")
        sap_session.findById(ELEMENTO_FILTRO_CARACTERISTICAS).key = 1
        SAPGuiElements.press_keyboard_keys(sap_session, "Enter")

        existe_proxima_operacao = True
        while existe_proxima_operacao:
            '''
            row = 0
            while row < sap_session.findById(ELEMENTO_TABELA_RESULTADOS).RowCount:
                # print(row)
                # print(SAPGuiElements.get_text(sap_session, ELEMENTO_COLUNA_S.format(row)))
                # session.findById(ELEMENTO_TABELA_RESULTADOS).selectedRows = row
                row += 1
            '''
            QE01.__inserir_s(sap_session)
            SAPGuiElements.press_button(sap_session, ELEMENTO_BOTAO_SELECIONAR_TODOS)
            SAPGuiElements.press_button(sap_session, ELEMENTO_BOTAO_AVALIAR)
            # TODO verificar essa l??gica
            SAPGuiElements.press_button(sap_session, ELEMENTO_BOTAO_PROXIMA_OPERACAO)
            existe_proxima_operacao = SAPGuiElements.is_enable(sap_session, ELEMENTO_BOTAO_PROXIMA_OPERACAO)

            try:
                SAPGuiElements.press_button(sap_session, ELEMENTO_BOTAO_GRAVAR_PRIMEIRO)
            except AttributeError:
                pass
        SAPGuiElements.press_button(sap_session, SAVE_BUTTON)
        tipo_mensagem = SAPGuiElements.get_sbar_message_type(sap_session)
        message = SAPGuiElements.get_text(sap_session, MESSAGE_ELEMENT)
        if tipo_mensagem and tipo_mensagem == 'S':
            return True, message
        else:
            return False, message

    @staticmethod
    def __inserir_s(sap_session):
        continuar = True
        contador = 0
        while continuar:
            try:
                SAPGuiElements.set_text(sap_session, ELEMENTO_COLUNA_S.format(contador), "S")
                contador = contador + 1

            except AttributeError:
                return


if __name__ == '__main__':
    session = SAPGuiApplication.connect()
    QE01.criar(session, '070000301267')
