from model import Produto, Remessa, ItemRemessa
from sapgui import SAPGuiApplication
from service import ProdutoService
from transaction import SAPTransaction
from sapguielements import SAPGuiElements, SAVE_BUTTON, MESSAGE_ELEMENT

import re

SPLIT_STR = "/ssubSUBSCREEN_BODY"

SHIPPING_PLACE_VALUE = "1014"

SHIPPING_PLACE_FIELD = "wnd[0]/usr/ctxtLIKP-VSTEL"
SHIPPING_ORDER_FIELD = "wnd[0]/usr/ctxtLV50C-VBELN"

ELEMENTO_NUMERO_ITEM = "wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\02/ssubSUBSCREEN_BODY:SAPMV50A:1104/" \
                       "tblSAPMV50ATC_LIPS_PICK/txtLIPS-POSNR[0,{}]"


ELEMENTO_CODIGO_PRODUTO = "wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\02/ssubSUBSCREEN_BODY:SAPMV50A:1104/" \
                          "tblSAPMV50ATC_LIPS_PICK/ctxtLIPS-MATNR[1,0]"

ELEMENTO_CODIGOS_PRODUTO = "wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\02/ssubSUBSCREEN_BODY:SAPMV50A:1104/" \
                          "tblSAPMV50ATC_LIPS_PICK/ctxtLIPS-MATNR[1,{}]"

ELEMENTO_DEPOSITO = "wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\02/ssubSUBSCREEN_BODY:SAPMV50A:1104" \
                         "/tblSAPMV50ATC_LIPS_PICK/ctxtLIPS-LGORT[3,0]"

ELEMENTO_DEPOSITOS = "wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\02/ssubSUBSCREEN_BODY:SAPMV50A:1104" \
                         "/tblSAPMV50ATC_LIPS_PICK/ctxtLIPS-LGORT[3,{}]"


ELEMENTO_QUANTIDADE = "wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\02/ssubSUBSCREEN_BODY:SAPMV50A:1104" \
                        "/tblSAPMV50ATC_LIPS_PICK/txtLIPSD-G_LFIMG[4,0]"

ELEMENTO_QUANTIDADES = "wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\02/ssubSUBSCREEN_BODY:SAPMV50A:1104" \
                        "/tblSAPMV50ATC_LIPS_PICK/txtLIPSD-G_LFIMG[4,{}]"

ELEMENTO_PICKING = "wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\02/ssubSUBSCREEN_BODY:SAPMV50A:1104" \
                         "/tblSAPMV50ATC_LIPS_PICK/txtLIPSD-PIKMG[6,0]"

ELEMENTO_LOTE = "wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\02/ssubSUBSCREEN_BODY:SAPMV50A:1104" \
                       "/tblSAPMV50ATC_LIPS_PICK/ctxtLIPS-CHARG[8,0]"

ELEMENTO_LOTES = "wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\02/ssubSUBSCREEN_BODY:SAPMV50A:1104" \
                       "/tblSAPMV50ATC_LIPS_PICK/ctxtLIPS-CHARG[8,{}]"

ELEMENTO_BOTAO_FLUXO_DOCUMENTO = "wnd[0]/tbar[1]/btn[7]"

PARTIAL_SHIPPINGS_MESSAGE = "wnd[1]/tbar[0]/btn[0]"

ELEMENTO_CAMPO_REMESSA = "wnd[0]/usr/ctxtLIKP-VBELN"


class VL01:

    @staticmethod
    def create(sap_session, remessa):

        SAPTransaction.call(sap_session, 'vl01n')
        SAPGuiElements.set_text(sap_session, SHIPPING_PLACE_FIELD, SHIPPING_PLACE_VALUE)
        SAPGuiElements.set_text(sap_session, SHIPPING_ORDER_FIELD, remessa.numero_ordem)
        SAPGuiElements.press_keyboard_keys(sap_session, "Enter")

        tipo_mensagem = str(sap_session.FindById("wnd[0]/sbar/").MessageType)

        if tipo_mensagem and tipo_mensagem != 'S':
            # erro ao tentar entrar na ordem
            error_message = VL01.get_message(sap_session, MESSAGE_ELEMENT)
            raise RuntimeError(VL01.get_formated_error_message(error_message, remessa))

        # caso nao mostre nenhuma mensagem de erro, continua a execucao
        else:
            if remessa.produto.deposito:
                SAPGuiElements.select_element(sap_session, ELEMENTO_DEPOSITO.split(SPLIT_STR)[0])
                SAPGuiElements.set_text(sap_session, ELEMENTO_DEPOSITO, remessa.produto.deposito)

            SAPGuiElements.select_element(sap_session, ELEMENTO_QUANTIDADE.split(SPLIT_STR)[0])
            SAPGuiElements.set_text(sap_session, ELEMENTO_QUANTIDADE, remessa.quantidade)

            SAPGuiElements.select_element(sap_session, ELEMENTO_PICKING.split(SPLIT_STR)[0])
            SAPGuiElements.set_text(sap_session, ELEMENTO_PICKING, remessa.quantidade)

            if remessa.produto.lote:
                SAPGuiElements.select_element(sap_session, ELEMENTO_LOTE.split(SPLIT_STR)[0])
                SAPGuiElements.set_text(sap_session, ELEMENTO_LOTE, remessa.produto.lote)

            SAPGuiElements.press_button(sap_session, SAVE_BUTTON)
            try:
                # ignorando mensagem de remessas parciais
                SAPGuiElements.press_button(sap_session, PARTIAL_SHIPPINGS_MESSAGE)
            finally:
                tipo_mensagem = str(sap_session.FindById("wnd[0]/sbar/").MessageType)
                message = SAPGuiElements.get_text(sap_session, MESSAGE_ELEMENT)
                if tipo_mensagem == 'S':
                    # remessa criada com sucesso
                    return VL01.get_shipping_number(message)

                else:
                    raise RuntimeError(VL01.get_formated_error_message(message, remessa))

    @staticmethod
    def get_message(sap_session, element):
        message = ""
        try:
            message = SAPGuiElements.get_text(sap_session, element)
        finally:
            return message

    @staticmethod
    def get_formated_error_message(mensagem_erro, remessa):
        return "Falha ao criar uma remessa na ordem {}.\nErro SAP: '{}'".format(remessa.numero_ordem, mensagem_erro)

    @staticmethod
    def get_shipping_number(mensagem_sucesso):
        return "".join(re.findall("\\d+", mensagem_sucesso))


class VL03:
    # método que retorna um produto através de uma remessa já pronta
    @staticmethod
    def gerar_produto_remessa_pronta(sap_session, numero_remessa):
        try:
            SAPTransaction.call(sap_session, 'vl03n')
            SAPGuiElements.set_text(sap_session, ELEMENTO_CAMPO_REMESSA, numero_remessa)
            SAPGuiElements.press_keyboard_keys(sap_session, "Enter")
            SAPGuiElements.verificar_mensagem_barra_inferior(sap_session)

            remessa = Remessa(None, None)
            proximo_item = True
            c = 0
            while proximo_item:
                numero_item = SAPGuiElements.get_text(sap_session, ELEMENTO_NUMERO_ITEM.format(str(c)))
                proximo_item = str(numero_item).isdigit()
                if proximo_item:
                    codigo_produto = SAPGuiElements.get_text(sap_session, ELEMENTO_CODIGOS_PRODUTO.format(str(c)))
                    deposito = SAPGuiElements.get_text(sap_session, ELEMENTO_DEPOSITOS.format(str(c)))
                    quantidade = SAPGuiElements.get_text(sap_session, ELEMENTO_QUANTIDADES.format(str(c)))
                    lote = SAPGuiElements.get_text(sap_session, ELEMENTO_LOTES.format(str(c)))

                    produto = ProdutoService.pesquisar_produto_pelo_codigo(codigo_produto)

                    '''
                    # TODO informar ao usuario se ele deseja continuar caso lote ou deposito esteja diferente
                    if produto.lote != lote:
                        raise RuntimeError('Lote da remessa diferente do lote cadastrado para o produto {}!'
                                           .format(produto.nome))

                    if produto.deposito != deposito:
                        raise RuntimeError('Deposito da remessa diferente do deposito cadastrado para o produto {}!'
                                           .format(produto.nome))
                    '''
                    item = ItemRemessa(quantidade=quantidade,
                                       produto=produto,
                                       numero_item=numero_item,
                                       deposito=deposito,
                                       lote=lote)
                    remessa.itens.append(item)
                c += 1
            return remessa
        except Exception as e:
            print(e)


if __name__ == '__main__':
    session = SAPGuiApplication.connect()
    VL03.gerar_produto_remessa_pronta(session, "80684179")
