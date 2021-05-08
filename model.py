class Remessa:

    def __init__(self, numero_ordem, quantidade, produto):
        self.numero_ordem = numero_ordem
        self.quantidade = quantidade
        self.produto = produto


class Produto:

    def __init__(self, codigo, nome, deposito, lote, inspecao_veiculo, inspecao_produto, remover_a, id_produto=None):
        self.id_produto = id_produto
        self.codigo = codigo
        self.nome = nome
        self.deposito = deposito
        self.lote = lote
        self.inspecao_veiculo = inspecao_veiculo
        self.inspecao_produto = inspecao_produto
        self.remover_a = remover_a

    def __str__(self):
        return "Deposito: {} Lote: {}".format(self.deposito, self.lote)


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
        self.material = ""
        self.centro = "1014"
        self.origem = ""
        self.lote = ""
        self.deposito = ""
        self.texto_breve = ""


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


class Municipio:

    def __init__(self, id_municipio, nome_municipio, codigo_municipio, uf):
        self.id_municipio = id_municipio
        self.nome_municipio = nome_municipio
        self.codigo_municipio = codigo_municipio
        self.uf = uf

    def __str__(self):
        return "{} {}".format(self.uf.upper(), self.nome_municipio)
