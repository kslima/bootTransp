from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext


class AutorizacaoSharePoint:
    def __init__(self):
        self.id_autorizacao = None
        self.fornecedor = None
        self.numero_ordem = None
        self.transportador = None
        self.nome_motorista = None
        self.cpf = None
        self.rg = None
        self.cnh = None
        self.cavalo = None
        self.minicipio_cavalo = None
        self.carreta_1 = None
        self.municipio_carreta_1 = None
        self.carreta_2 = None
        self.municipio_carreta_2 = None
        self.tipo_veiculo = None
        self.procedimento_especial = None
        self.numero_eixos = None
        self.quantidade_ordens = None
        self.geradas = None
        self.data_inicio = None
        self.data_final = None
        self.data_execucao = None
        self.ativo = None
        self._id = None


def conn(numero_autorizacao):
    # Definindo parametros de conexão
    # ID e Senha criados pelo portal do sharepoint
    app_settings = {
        'url': 'https://usinacoruripe.sharepoint.com/sites/FaturamentoTorta',
        'client_id': 'c74022f1-d1b5-47e3-913f-84d7a98cf032',
        'client_secret': 'qfHtOWl6YieOhGAAavzuzUDvuf9pl2ZvD/0JSqvZhsQ='
    }

    # Chamando conexão com API Rest
    context_auth = AuthenticationContext(url=app_settings['url'])
    context_auth.acquire_token_for_app(client_id=app_settings['client_id'],
                                       client_secret=app_settings['client_secret'])
    ctx = ClientContext(app_settings['url'], context_auth)

    # Puxando valores da lista
    lista_share = ctx.web.lists.get_by_title("Autorizações")
    items = lista_share.get_items()
    ctx.load(items)
    ctx.execute_query()
    for item in items:
        _id = '{0}'.format(item.properties["ID"])
        id_autorizacao = '{0}'.format(item.properties["NumAutoriza_x00e7__x00e3_o"])
        if id_autorizacao == numero_autorizacao:
            id_autorizacao = '{0}'.format(item.properties["NumAutoriza_x00e7__x00e3_o"])
            fornecedor = '{0}'.format(item.properties["Fornecedor"]).strip()
            numero_ordem = '{0}'.format(item.properties["uwih"]).strip()
            transportador = '{0}'.format(item.properties["r9n0"]).strip()
            nome_motorista = '{0}'.format(item.properties["yecy"]).strip()
            cpf = '{0}'.format(item.properties["jcvj"]).strip()
            rg = '{0}'.format(item.properties["OData__x006d_vk6"]).strip()
            cnh = '{0}'.format(item.properties["wwof"]).strip()
            cavalo = '{0}'.format(item.properties["qbkd"]).strip()
            cavalo = cavalo.replace('-', '')
            minicipio_cavalo = '{0}'.format(item.properties["hr0e"]).strip()
            carreta_1 = '{0}'.format(item.properties["OData__x006d_cb0"]).strip()
            carreta_1 = carreta_1.replace('-', '')
            if carreta_1.upper() == 'NONE':
                carreta_1 = ''

            municipio_carreta_1 = '{0}'.format(item.properties["a8fj"]).strip()
            if municipio_carreta_1.upper() == 'NONE':
                municipio_carreta_1 = ''

            carreta_2 = '{0}'.format(item.properties["qdqz"]).strip()
            carreta_2 = carreta_2.replace('-', '')
            if carreta_2.upper() == 'NONE':
                carreta_2 = ''

            municipio_carreta_2 = '{0}'.format(item.properties["OData__x0071_aw9"]).strip()
            if municipio_carreta_2.upper() == 'NONE':
                municipio_carreta_2 = ''

            tipo_veiculo = '{0}'.format(item.properties["OData__x0065_op5"])
            procedimento_especial = '{0}'.format(item.properties["i0dv"])
            numero_eixos = '{0}'.format(item.properties["ahpu"])
            quantidade_ordens = '{0}'.format(item.properties["hpzf"])
            geradas = '{0}'.format(item.properties["OData__x006d_kv6"])
            data_inicio = '{0}'.format(item.properties["OData__x0068_qp8"])
            data_final = '{0}'.format(item.properties["OData__x0078_od1"])
            data_execucao = '{0}'.format(item.properties["ejtw"])
            ativo = '{0}'.format(item.properties["ATIVA"])

            autoriazacao = AutorizacaoSharePoint()
            autoriazacao.id_autorizacao = id_autorizacao
            autoriazacao.fornecedor = fornecedor
            autoriazacao.numero_ordem = numero_ordem
            autoriazacao.transportador = transportador
            autoriazacao.nome_motorista = nome_motorista
            autoriazacao.cpf = cpf
            autoriazacao.rg = rg
            autoriazacao.cnh = cnh
            autoriazacao.cavalo = cavalo
            autoriazacao.minicipio_cavalo = minicipio_cavalo
            autoriazacao.carreta_1 = carreta_1
            autoriazacao.municipio_carreta_1 = municipio_carreta_1
            autoriazacao.carreta_2 = carreta_2
            autoriazacao.municipio_carreta_2 = municipio_carreta_2
            autoriazacao.tipo_veiculo = tipo_veiculo
            autoriazacao.procedimento_especial = procedimento_especial
            autoriazacao.numero_eixos = numero_eixos
            autoriazacao.quantidade_ordens = quantidade_ordens
            autoriazacao.geradas = geradas
            autoriazacao.data_inicio = data_inicio
            autoriazacao.data_final = data_final
            autoriazacao.data_execucao = data_execucao
            autoriazacao.ativo = ativo
            autoriazacao._id = _id
            return autoriazacao
    return None


def alterarDataExec(ID, DataExec):
    # Definindo parametros de conexão
    # ID e Senha criados pelo portal do sharepoint
    app_settings = {
        'url': 'https://usinacoruripe.sharepoint.com/sites/FaturamentoTorta',
        'client_id': 'c74022f1-d1b5-47e3-913f-84d7a98cf032',
        'client_secret': 'qfHtOWl6YieOhGAAavzuzUDvuf9pl2ZvD/0JSqvZhsQ='
    }

    # Chamando conexão com API Rest
    context_auth = AuthenticationContext(url=app_settings['url'])
    context_auth.acquire_token_for_app(client_id=app_settings['client_id'],
                                       client_secret=app_settings['client_secret'])
    ctx = ClientContext(app_settings['url'], context_auth)

    # Puxando valores da lista
    listaShare = ctx.web.lists.get_by_title("Autorizações")
    items = listaShare.get_items()
    ctx.load(items)
    ctx.execute_query()

    item = listaShare.get_item_by_id(ID)
    item.set_property('ejtw', DataExec)
    item.set_property('OData__x006d_kv6', '0')
    item.update()
    ctx.execute_query()


def alterarGeradas(ID, sumGeradas):
    # Definindo parametros de conexão
    # ID e Senha criados pelo portal do sharepoint
    app_settings = {
        'url': 'https://usinacoruripe.sharepoint.com/sites/FaturamentoTorta',
        'client_id': 'c74022f1-d1b5-47e3-913f-84d7a98cf032',
        'client_secret': 'qfHtOWl6YieOhGAAavzuzUDvuf9pl2ZvD/0JSqvZhsQ='
    }

    # Chamando conexão com API Rest
    context_auth = AuthenticationContext(url=app_settings['url'])
    context_auth.acquire_token_for_app(client_id=app_settings['client_id'],
                                       client_secret=app_settings['client_secret'])
    ctx = ClientContext(app_settings['url'], context_auth)

    # Puxando valores da lista
    listaShare = ctx.web.lists.get_by_title("Autorizações")
    items = listaShare.get_items()
    ctx.load(items)
    ctx.execute_query()

    item = listaShare.get_item_by_id(ID)
    item.set_property('OData__x006d_kv6', sumGeradas)
    item.update()
    ctx.execute_query()
