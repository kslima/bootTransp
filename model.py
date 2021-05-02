class Remessa:

    def __init__(self, numero_ordem, quantidade, produto):
        self.numero_ordem = numero_ordem
        self.quantidade = quantidade
        self.produto = produto


class Produto:

    def __init__(self):
        self.codigo = None
        self.nome = None
        self.deposito = None
        self.lote = None
        self.inspecao_veiculo = None
        self.inspecao_produto = None
        self.remover_a = None

    def __str__(self):
        return "Código: {}   Lote: {}   Deposito: {}".format(self.codigo, self.lote, self.deposito)


class Motorista:

    def __init__(self):
        self.nome = None
        self.cpf = None
        self.cnh = None
        self.rg = None


class Veiculo:

    def __init__(self):
        self.tipo_veiculo = None
        self.tolerancia_balanca = None
        self.quantidade_lacres = None
        self.placa_1 = None
        self.placa_2 = None
        self.placa_3 = None
        self.placa_4 = None
        self.codigo_municipio_placa_1 = None
        self.codigo_municipio_placa_2 = None
        self.codigo_municipio_placa_3 = None
        self.codigo_municipio_placa_4 = None

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