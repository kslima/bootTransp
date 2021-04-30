from sapgui import SAPGuiApplication
from sapguielements import SAPGuiElements
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


class QE01:

    @staticmethod
    def criar(sap_session):
        QE01.__abrir_transacao(sap_session)

    @staticmethod
    def __abrir_transacao(sap_session):
        SAPTransaction.call(sap_session, 'qe01')
        SAPGuiElements.set_text(sap_session, ELEMENTO_LOTE_CONTROLE, "070000299454")
        # SAPGuiElements.set_text(sap_session, ELEMENTO_OPERACAO, "0010")
        SAPGuiElements.set_text(sap_session, ELEMENTO_CENTRO, "1014")
        SAPGuiElements.press_keyboard_keys(sap_session, "Enter")

        existe_proxima_operacao = True
        while existe_proxima_operacao:
            QE01.__inserir_s(sap_session)
            SAPGuiElements.press_button(sap_session, ELEMENTO_BOTAO_SELECIONAR_TODOS)
            SAPGuiElements.press_button(sap_session, ELEMENTO_BOTAO_AVALIAR)
            try:
                SAPGuiElements.press_button(sap_session, ELEMENTO_BOTAO_PROXIMA_OPERACAO)
            except Exception as e:
                print(type(e))

            try:
                SAPGuiElements.press_button(sap_session, ELEMENTO_BOTAO_GRAVAR_PRIMEIRO)
            except Exception as e:
                print("")
            # SAPGuiElements.press_button(sap_session, ELEMENTO_BOTAO_GRAVAR_PRIMEIRO)
            # print(sap_session.FindById(ELEMENTO_BOTAO_PROXIMA_OPERACAO).select())

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


session = SAPGuiApplication.connect()
qe = QE01()
qe.criar(session)
