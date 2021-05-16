class ItemRemessa:
    def __init__(self):
        self.numero_ordem = None
        self.quantidade = None
        self.produto = None
        self.numero_item = None
        self.cfop = None
        self.df_icms = None
        self.df_ipi = None
        self.df_pis = None
        self.df_cofins = None
        self.codigo_imposto = None

    def __str__(self):
        return "Ordem: {} Quantidade: {} Produto: {} item: {}"\
            .format(self.numero_ordem, self.quantidade, self.produto, self.numero_item)

    def __eq__(self, other):
        if isinstance(other, ItemRemessa):
            return self.numero_ordem == other.numero_ordem
        return False


class Remessa:

    def __init__(self, numero_remessa=None, itens=None):
        if itens is None:
            itens = []
        self.numero_remessa = numero_remessa
        self.itens = itens


class Produto:

    def __init__(self, codigo, deposito, lote, inspecao_veiculo=0, nome="", inspecao_produto=0, remover_a=0,
                 id_produto=None):
        self.id_produto = id_produto
        self.codigo = codigo
        self.nome = nome
        self.deposito = deposito
        self.lote = lote
        self.inspecao_veiculo = inspecao_veiculo
        self.inspecao_produto = inspecao_produto
        self.remover_a = remover_a

    def __str__(self):
        return "{} - {}".format(self.codigo, self.nome)


class TipoCarregamento:
    def __init__(self):
        self.id_tipo_carregamento = None
        self.nome = None
        self.numero_ordem = None
        self.numero_pedido_frete = None
        self.inspecao_veiculo = 1
        self.inspecao_produto = 0
        self.remover_a = 0
        self.tipo_frete = None
        self.destino_frete = None
        self.codigo_transportador = None
        self.tipo_lacre = 0  # 0 - Sem lacre / 1 - Lacre Normal / 2 - Lacre Lona
        self.doc_diversos = None
        self.itens_str = None

    def __str__(self):
        return "Nome: {} Itens: {}".format(self.nome, self.itens_str)

class Motorista:

    def __init__(self, nome, cpf, cnh, rg, id_motorista=None):
        self.id_motorista = id_motorista
        self.nome = nome
        self.cpf = cpf
        self.cnh = cnh
        self.rg = rg

    def __str__(self):
        descricao_motorista = self.nome
        if self.cpf:
            descricao_motorista = descricao_motorista + " CPF: {}".format(self.cpf)
        if self.cnh:
            descricao_motorista = descricao_motorista + " CNH: {}".format(self.cnh)
        if self.rg:
            descricao_motorista = descricao_motorista + " RG: {}".format(self.rg)
        return descricao_motorista


class Veiculo:

    def __init__(self, tipo_veiculo, tolerancia_balanca, placa_1, codigo_municipio_placa_1, placa_2=None, placa_3=None,
                 placa_4=None, codigo_municipio_placa_2=None, codigo_municipio_placa_3=None,
                 codigo_municipio_placa_4=None, quantidade_lacres=None, id_veiculo=None):
        self.id_veiculo = id_veiculo
        self.tipo_veiculo = tipo_veiculo
        self.tolerancia_balanca = tolerancia_balanca
        self.quantidade_lacres = quantidade_lacres
        self.placa_1 = placa_1
        self.placa_2 = placa_2
        self.placa_3 = placa_3
        self.placa_4 = placa_4
        self.codigo_municipio_placa_1 = codigo_municipio_placa_1
        self.codigo_municipio_placa_2 = codigo_municipio_placa_2
        self.codigo_municipio_placa_3 = codigo_municipio_placa_3
        self.codigo_municipio_placa_4 = codigo_municipio_placa_4

    def __str__(self):
        return "Placas: {}/{}/{}/{} Tipo:{} Eixos:{} Lacres:{}".format(self.placa_1, self.placa_2, self.placa_3,
                                                                       self.placa_4, self.tipo_veiculo,
                                                                       self.tolerancia_balanca, self.quantidade_lacres)


class Transporte:

    def __init__(self):
        self.documento = None
        self.motorista = None
        self.conjunto = None
        self.lacres = []
        self.remessas = []


class Tranportador:

    def __init__(self):
        self.nome = None
        self.codigo = None
        self.cidade = None
        self.uf = None


class Carregamento:

    def __init__(self):
        self.etapas = {}
        self.remessas = None
        self.lotes_qualidade = None
        self.codigo_transportador = None
        self.lote_veiculo = None
        self.produto = None
        self.veiculo = None
        self.motorista = None
        self.lacres = None
        self.numero_pedido = None


class LoteInspecao:

    def __init__(self):
        self.material = None
        self.centro = "1014"
        self.origem = None
        self.lote = None
        self.deposito = None
        self.texto_breve = None
        self.numero_lote = None


class Placa:
    def __init__(self):
        self.placa = None
        self.uf = None
        self.municipio = None
        self.codigo_municipio = None

    def __str__(self):
        return "{} {}".format(self.uf, self.municipio)


class Lacre:
    def __init__(self, codigo, numero, id_lacre=None):
        self.id_lacre = id_lacre
        self.codigo = codigo
        self.numero = numero

    def __str__(self):
        return "{}".format(self.numero)


class Municipio:

    def __init__(self, id_municipio, nome_municipio, codigo_municipio, uf):
        self.id_municipio = id_municipio
        self.nome_municipio = nome_municipio
        self.codigo_municipio = codigo_municipio
        self.uf = uf

    def __str__(self):
        return "{} {}".format(self.uf.upper(), self.nome_municipio)
