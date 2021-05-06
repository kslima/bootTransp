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
        self.inspecao_veiculo = False
        self.inspecao_produto = False
        self.remover_a = False

    def __str__(self):
        return "Código: {}  Deposito: {} Lote: {}".format(self.codigo, self.deposito, self.lote)


class Motorista:

    def __init__(self):
        self.nome = None
        self.cpf = None
        self.cnh = None
        self.rg = None

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


class Municipio:

    def __init__(self, codigo_uf, municipio, codigo_municipio):
        self.estados = {"11": "RO",
                        "12": "AC",
                        "13": "AM",
                        "14": "RR",
                        "15": "PA",
                        "16": "AP",
                        "17": "TO",
                        "21": "MA",
                        "22": "PI",
                        "23": "CE",
                        "24": "RN",
                        "25": "PB",
                        "26": "PE",
                        "27": "AL",
                        "28": "SE",
                        "29": "BA",
                        "31": "MG",
                        "32": "ES",
                        "33": "RJ",
                        "35": "SP",
                        "41": "PR",
                        "42": "SC",
                        "43": "RS",
                        "50": "MS",
                        "51": "MT",
                        "52": "GO",
                        "53": "DF", }
        self.codigo_uf = codigo_uf
        self.uf = self.procurar_estado_por_codigo(codigo_uf)
        self.municipio = municipio
        self.codigo_municipio = codigo_municipio

    def procurar_estado_por_codigo(self, codigo_estado):
        return self.estados[codigo_estado]

    def __str__(self):
        return "{} {}".format(self.uf.upper(), self.municipio)
