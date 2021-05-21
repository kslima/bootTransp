import time

from model import Produto, Remessa, ItemRemessa
from sapgui import SAPGuiApplication
from service import ProdutoService
from transaction import SAPTransaction
from sapguielements import SAPGuiElements, SAVE_BUTTON, MESSAGE_ELEMENT

import re

from utilitarios import StringUtils

SPLIT_STR = "/ssubSUBSCREEN_BODY"
SHIPPING_PLACE_VALUE = "1014"
SHIPPING_PLACE_FIELD = "wnd[0]/usr/ctxtLIKP-VSTEL"
SHIPPING_ORDER_FIELD = "wnd[0]/usr/ctxtLV50C-VBELN"
ELEMENTO_ABA_PICKING = "wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\02"
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
ELEMENTO_PICKINGS = "wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\02/ssubSUBSCREEN_BODY:SAPMV50A:1104" \
                    "/tblSAPMV50ATC_LIPS_PICK/txtLIPSD-PIKMG[6,{}]"
ELEMENTO_LOTE = "wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\02/ssubSUBSCREEN_BODY:SAPMV50A:1104" \
                "/tblSAPMV50ATC_LIPS_PICK/ctxtLIPS-CHARG[8,0]"
ELEMENTO_LOTES = "wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\02/ssubSUBSCREEN_BODY:SAPMV50A:1104" \
                 "/tblSAPMV50ATC_LIPS_PICK/ctxtLIPS-CHARG[8,{}]"
ELEMENTO_CFOP = "wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\\07/ssubSUBSCREEN_BODY:SAPMV50A:3110/ctxtLIPS-J_1BCFOP"
ELEMENTO_CODIGO_IMPOSTO = "wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\\07/ssubSUBSCREEN_BODY:SAPMV50A:3110/" \
                          "ctxtLIPS-J_1BTXSDC"
ELEMENTO_ICMS = "wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\\07/ssubSUBSCREEN_BODY:SAPMV50A:3110/ctxtLIPS-J_1BTAXLW1"
ELEMENTO_IPI = "wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\\07/ssubSUBSCREEN_BODY:SAPMV50A:3110/ctxtLIPS-J_1BTAXLW2"
ELEMENTO_PIS = "wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\\07/ssubSUBSCREEN_BODY:SAPMV50A:3110/ctxtLIPS-J_1BTAXLW5"
ELEMENTO_COFINS = "wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\\07/ssubSUBSCREEN_BODY:SAPMV50A:3110/ctxtLIPS-J_1BTAXLW4"
ELEMENTO_LINHA = "wnd[0]/usr/tabsTAXI_TABSTRIP_OVERVIEW/tabpT\\02/ssubSUBSCREEN_BODY:SAPMV50A:1104" \
                 "/tblSAPMV50ATC_LIPS_PICK"
ELEMENTO_BOTAO_FLUXO_DOCUMENTO = "wnd[0]/tbar[1]/btn[7]"
ELEMENTO_BOTAO_DETALHE_CABECALHJO = "wnd[0]/tbar[1]/btn[8]"
ELEMENTO_ABA_TRANSPORTE = "wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\\04"
ELEMENTO_ICOTERMS_1 = "wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\\04/ssubSUBSCREEN_BODY:SAPMV50A:2108/ctxtLIKP-INCO1"
ELEMENTO_ICOTERMS_2 = "wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\\04/ssubSUBSCREEN_BODY:SAPMV50A:2108/txtLIKP-INCO2"
ELEMENTO_TIPO_VEICULO = "wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\\04/ssubSUBSCREEN_BODY:SAPMV50A:2108/ctxtLIKP-TRATY"
ELEMENTO_PLACA = "wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\\04/ssubSUBSCREEN_BODY:SAPMV50A:2108/txtLIKP-TRAID"
ELEMENTO_ABA_PARCEIROS = "wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\\08"
ELEMENTO_COLUNA_TIPO_PARCEIRO = "wnd[0]/usr/tabsTAXI_TABSTRIP_HEAD/tabpT\\08/ssubSUBSCREEN_BODY:SAPMV50A:2114/" \
                                "subSUBSCREEN_PARTNER_OVERVIEW:SAPLV09C:1000/tblSAPLV09CGV_TC_PARTNER_OVERVIEW/cmbGVS" \
                                "_TC_DATA-REC-PARVW[0,{}]"
ELEMENTO_ABA_PROCESSAMENTO_FINANCEIRO = "wnd[0]/usr/tabsTAXI_TABSTRIP_ITEM/tabpT\\07"
PARTIAL_SHIPPINGS_MESSAGE = "wnd[1]/tbar[0]/btn[0]"
ELEMENTO_CAMPO_REMESSA = "wnd[0]/usr/ctxtLIKP-VBELN"


class VL01:

    @staticmethod
    def criar_remessa(sap_session, remessa):
        try:
            ordem = remessa.itens[0].numero_ordem
            SAPTransaction.call(sap_session, 'vl01n')
            SAPGuiElements.set_text(sap_session, SHIPPING_PLACE_FIELD, SHIPPING_PLACE_VALUE)
            SAPGuiElements.set_text(sap_session, SHIPPING_ORDER_FIELD, ordem)
            SAPGuiElements.press_keyboard_keys(sap_session, "Enter")

            # verificando se houve alguma mensagem de erro.
            # Uma exceçao será lançada no caso de erro.
            SAPGuiElements.verificar_mensagem_barra_inferior(sap_session)
            SAPGuiElements.select_element(sap_session, ELEMENTO_ABA_PICKING)

            linha = 0
            for item in remessa.itens:
                linha_str = str(linha)
                cod_prod_sap = SAPGuiElements.get_text(sap_session, ELEMENTO_CODIGOS_PRODUTO.format(str(linha_str)))
                num_item_sap = SAPGuiElements.get_text(sap_session, ELEMENTO_NUMERO_ITEM.format(str(linha_str)))

                if not StringUtils.is_equal(cod_prod_sap, item.produto.codigo):
                    raise RuntimeError('Divergência de produtos no item: {}'
                                       '\nProduto selecionado: {}'
                                       '\nProduto encontrado : {}'
                                       .format(num_item_sap, item.produto.codigo, cod_prod_sap))

                VL01.__inserir_deposito(sap_session, item.produto.deposito, linha_str)
                VL01.__inserir_lote(sap_session, item.produto.lote, linha_str)
                VL01.__inserir_quantidade(sap_session, item.quantidade, linha_str)
                VL01.__inserir_picking(sap_session, item.quantidade, linha_str)

                VL01.__alterar_direitos_fiscais_se_necessario(sap_session, item.produto, linha)
                linha += 1
            VL01.__inserir_dados_cabecalho(sap_session, remessa.itens[0].produto)

            SAPGuiElements.salvar(sap_session)

            # ignorando alerta de remessas parciais
            SAPGuiElements.ignorar_alerta(sap_session)

            # verificando se houve alguma mensagem de erro.
            mensagem = SAPGuiElements.verificar_mensagem_barra_inferior(sap_session)

            # retornando o número da remessa
            return VL01.extrair_numero_remessa(mensagem)

        except Exception as e:
            raise e

    @staticmethod
    def __alterar_direitos_fiscais_se_necessario(sap_session, produto,  linha):
        try:
            if produto.cfop or \
                    produto.codigo_imposto or \
                    produto.df_icms or \
                    produto.df_ipi or \
                    produto.df_pis or \
                    produto.df_cofins:
                VL01.__abrir_item_para_edicao(sap_session, linha)
                VL01.__inserir_direitos_fiscais(sap_session, produto)

        except Exception as e:
            raise e

    @staticmethod
    def __inserir_dados_cabecalho(sap_session, produto):
        if produto.tipo_frete:
            VL01.__abrir_detalhes_cabecalho(sap_session)
            VL01.__inserir_dados_aba_transporte(sap_session, produto)
            # VL01.__inserir_dados_aba_parceiros(sap_session)

    @staticmethod
    def __inserir_deposito(sap_session, deposito, linha_item):

        if deposito:
            try:
                SAPGuiElements.select_element(sap_session, ELEMENTO_DEPOSITOS.split(SPLIT_STR)[0])
                SAPGuiElements.set_text(sap_session, ELEMENTO_DEPOSITOS.format(linha_item), deposito)

            except Exception:
                if SAPGuiElements.verificar_mensagem_barra_inferior(sap_session):
                    SAPGuiElements.enter(sap_session)
                raise RuntimeError('Erro ao inserir o depósito!')

    @staticmethod
    def __inserir_lote(sap_session, lote, linha_item):

        if lote:
            try:
                SAPGuiElements.select_element(sap_session, ELEMENTO_LOTES.split(SPLIT_STR)[0])
                SAPGuiElements.set_text(sap_session, ELEMENTO_LOTES.format(linha_item), lote)
            except Exception:
                if SAPGuiElements.verificar_mensagem_barra_inferior(sap_session):
                    SAPGuiElements.enter(sap_session)
                raise RuntimeError('Erro ao inserir o lote!')

    @staticmethod
    def __inserir_quantidade(sap_session, quantidade, linha_item):

        if quantidade:
            try:
                SAPGuiElements.select_element(sap_session, ELEMENTO_QUANTIDADES.split(SPLIT_STR)[0])
                SAPGuiElements.set_text(sap_session, ELEMENTO_QUANTIDADES.format(linha_item), quantidade)
            except Exception:
                if SAPGuiElements.verificar_mensagem_barra_inferior(sap_session):
                    SAPGuiElements.enter(sap_session)
                raise RuntimeError('Erro ao inserir a quantidade!')

    @staticmethod
    def __inserir_picking(sap_session, picking, linha_item):

        if picking:
            try:
                SAPGuiElements.select_element(sap_session, ELEMENTO_PICKINGS.split(SPLIT_STR)[0])
                SAPGuiElements.set_text(sap_session, ELEMENTO_PICKINGS.format(linha_item), picking)
            except Exception:
                if SAPGuiElements.verificar_mensagem_barra_inferior(sap_session):
                    SAPGuiElements.enter(sap_session)
                raise RuntimeError('Erro ao inserir o picking!')

    @staticmethod
    def __abrir_item_para_edicao(sap_session, linha):

        try:
            SAPGuiElements.selecionar_linha(sap_session, ELEMENTO_LINHA, linha)
            sap_session.findById("wnd[0]").sendVKey(2)
            SAPGuiElements.ignorar_alerta(sap_session)
            if SAPGuiElements.verificar_mensagem_barra_inferior(sap_session):
                SAPGuiElements.enter(sap_session)
        except Exception:
            raise RuntimeError('Erro ao inserir direitos fiscais!')

    @staticmethod
    def __abrir_detalhes_cabecalho(sap_session):
        SAPGuiElements.press_button(sap_session, ELEMENTO_BOTAO_DETALHE_CABECALHJO)
        SAPGuiElements.ignorar_alerta(sap_session)

    @staticmethod
    def __inserir_dados_aba_transporte(sap_session, produto):
        SAPGuiElements.select_element(sap_session, ELEMENTO_ABA_TRANSPORTE)
        SAPGuiElements.set_text(sap_session, ELEMENTO_ICOTERMS_1, produto.tipo_frete)
        SAPGuiElements.set_text(sap_session, ELEMENTO_ICOTERMS_2, produto.complemento_tipo_frete)
        SAPGuiElements.set_text(sap_session, ELEMENTO_TIPO_VEICULO, '1000')
        # SAPGuiElements.set_text(sap_session, ELEMENTO_PLACA, 'MG QUN3792')

    @staticmethod
    def __inserir_dados_aba_parceiros(sap_session):

        SAPGuiElements.select_element(sap_session, ELEMENTO_ABA_PARCEIROS)
        indisponivel = True
        linha = 0
        # sap_session.findById(ELEMENTO_COLUNA_TIPO_PARCEIRO.format(str(8))).key = 'SP'
        # TODO continuar aqui.... achar o retorno corereto
        while indisponivel:
            texto = sap_session.findById(ELEMENTO_COLUNA_TIPO_PARCEIRO.format(str(linha))).key
            print(texto)
            if texto is None:
                print('texto é none')
                indisponivel = False
                sap_session.findById(ELEMENTO_COLUNA_TIPO_PARCEIRO.format(str(linha))).key = 'SP'
            linha += 1

    @staticmethod
    def __inserir_direitos_fiscais(sap_session, produto):
        SAPGuiElements.select_element(sap_session, ELEMENTO_ABA_PROCESSAMENTO_FINANCEIRO)
        SAPGuiElements.set_text(sap_session, ELEMENTO_CFOP, produto.cfop)
        SAPGuiElements.set_text(sap_session, ELEMENTO_CODIGO_IMPOSTO, produto.codigo_imposto)
        SAPGuiElements.set_text(sap_session, ELEMENTO_ICMS, produto.df_icms)
        SAPGuiElements.set_text(sap_session, ELEMENTO_IPI, produto.df_ipi)
        SAPGuiElements.set_text(sap_session, ELEMENTO_PIS, produto.df_pis)
        SAPGuiElements.set_text(sap_session, ELEMENTO_COFINS, produto.df_cofins)

    @staticmethod
    def extrair_numero_remessa(mensagem):
        return "".join(re.findall("\\d+", mensagem))


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
                                       numero_item=numero_item)
                    remessa.itens.append(item)
                c += 1
            return remessa
        except Exception as e:
            print(e)


if __name__ == '__main__':
    session = SAPGuiApplication.connect()
    VL03.gerar_produto_remessa_pronta(session, "80684179")
