

from peewee import SqliteDatabase, Model, TextField, ForeignKeyField, BooleanField, IntegerField, DecimalField

db = SqliteDatabase('C:\\Users\\kslima\\Desktop\\sqlite\\database.db')


class BaseModel(Model):
    class Meta:
        database = db


class Municipio(BaseModel):
    codigo = TextField()
    nome = TextField()
    uf = TextField()

    def __str__(self):
        return "{} {}".format(self.uf, self.nome)


class Transportador(BaseModel):
    nome = TextField(null=False)
    codigo_sap = TextField(null=False)
    municipio = ForeignKeyField(Municipio, backref='municipio')
    cnpj_cpf = TextField(unique=True, null=False)

    def __str__(self):
        return "{} - {} ({})".format(self.codigo_sap, self.nome,
                                     '{} - {}'.format(self.municipio.uf, self.municipio.nome))


class TipoInspecaoVeiculo(BaseModel):
    descricao = TextField(null=False)


class CanalDistribuicao(BaseModel):
    codigo = IntegerField(unique=True)
    descricao = TextField()

    def __str__(self):
        return "{} - {}".format(self.codigo, self.descricao)


class SetorAtividade(BaseModel):
    descricao = TextField()
    codigo = IntegerField()

    def __str__(self):
        return "{} - {}".format(self.codigo, self.descricao)


class Produto(BaseModel):
    codigo_sap = TextField()
    nome = TextField()
    deposito = TextField()
    lote = TextField()
    canal_distribuicao = ForeignKeyField(CanalDistribuicao, backref='canal_distribuicao', null=True)
    setor_atividade = ForeignKeyField(SetorAtividade, backref='setor_atividade', null=True)
    cfop = TextField()
    df_icms = TextField()
    df_ipi = TextField()
    df_pis = TextField()
    df_cofins = TextField()
    codigo_imposto = TextField()
    inspecao_veiculo = BooleanField(default=0)
    tipo_inspecao_veiculo = ForeignKeyField(TipoInspecaoVeiculo, backref='tipo_inspecao_veiculo', null=True,
                                            default=None)
    inspecao_produto = BooleanField(default=0)
    remover_a = BooleanField(default=0)
    tipo_lacres = IntegerField(default=0)  # 0 - Nehum / 1 - lacres normal / 2 - lacres lona
    numero_ordem = TextField()
    pedido_frete = TextField()
    icoterms1 = TextField()
    icoterms2 = TextField()
    transportador = ForeignKeyField(Transportador, backref='transportador', null=True, default=None)
    documentos_diversos = TextField()

    def __str__(self):
        return "{} - {}".format(self.codigo_sap, self.nome)


class Motorista(BaseModel):
    nome = TextField(null=False)
    cpf = TextField(null=True)
    cnh = TextField(null=True)
    rg = TextField(null=True)


class TipoVeiculo(BaseModel):
    codigo = TextField()
    descricao = TextField()

    def __str__(self):
        return '{} - {}'.format(self.codigo, self.descricao)


class PesoBalanca(BaseModel):
    codigo = TextField()
    descricao = TextField()
    peso_maximo = DecimalField()

    def __str__(self):
        return '{} - {}'.format(self.codigo, self.descricao)


class Veiculo(BaseModel):
    tipo_veiculo = ForeignKeyField(TipoVeiculo, backref='tipo_veiculo')
    peso_balanca = ForeignKeyField(PesoBalanca, backref='peso_balanca')
    quantidade_lacres = IntegerField()
    placa1 = TextField()
    placa2 = TextField()
    placa3 = TextField()
    placa4 = TextField()
    municipio_placa1 = ForeignKeyField(Municipio, backref='municipio1')
    municipio_placa2 = ForeignKeyField(Municipio, backref='municipio2', null=True)
    municipio_placa3 = ForeignKeyField(Municipio, backref='municipio3', null=True)
    municipio_placa4 = ForeignKeyField(Municipio, backref='municipio4', null=True)


class Lacre(BaseModel):
    codigo = TextField()
    numero = TextField()

    def __str__(self):
        return "{}".format(self.numero)


class Remessa:

    def __init__(self, numero_remessa=None, itens=None):
        if itens is None:
            itens = []
        self.numero_remessa = numero_remessa
        self.itens = itens


class ItemRemessa:
    def __init__(self):
        self.numero_ordem = None
        self.quantidade = None
        self.produto = None

    def __str__(self):
        return "Ordem: {} Quantidade: {} Produto: {}" \
            .format(self.numero_ordem, self.quantidade, self.produto)

    def __eq__(self, other):
        if isinstance(other, ItemRemessa):
            return self.numero_ordem == other.numero_ordem
        return False


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


class Carregamento:

    def __init__(self):
        self.etapas = {}
        self.remessas = None
        self.lotes_qualidade = None
        self.transportador = None
        self.lote_veiculo = None
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


class Ordem:
    def __init__(self):
        self.data = None
        self.numero = None
        self.material = None
        self.codigo_material = None
        self.cliente = None
        self.cidade = None
        self.uf = None
        self.qtd = None
        self.qtd_saida = None
        self.qtd_disponivel = None
        self.pedido = None
        self.tipo = None
        self.status = None
        self.cnpj = None


Motorista.create_table()
# db.create_tables([Municipio, Transportador, TipoInspecaoVeiculo, CanalDistribuicao, SetorAtividade, Produto,
# Motorista, TipoVeiculo, PesoBalanca, Veiculo])
'''

for i in ['INSPVEICACUCAR', 'INSPVEICALCOOL']:
    t = TipoInspecaoVeiculo(descricao=i)
    t.save()
    
lista = ['10 - Mercado Interno', '20 - Mercado Externo', '30 - E-commerce']
for v in lista:
    codigo = v[:2]
    descricao = v[5:]
    c = CanalDistribuicao(codigo=codigo, descricao=descricao)
    c.save()
    
lista = ['10 - Açúcar', '20 - Álcool', '30 - Energia', '40 - SubProduto', '50 - Cana de Açúcar', '60 - Outros']
for v in lista:
    codigo = v[:2]
    descricao = v[5:]
    c = SetorAtividade(codigo=codigo, descricao=descricao)
    c.save()
    
    
lista = ['01 - Outros ',
         '02 - Postal ',
         '03 - Ferroviário ',
         '04 - Marítimo   ',
         '05 - Graneleiro    ',
         '06 - Caçamba     ',
         '07 - Tanque      ',
         '08 - Coleta ',
         '09 - Bi Caçamba   ',
         '10 - Bi Graneleiro',
         '11 - Hopper   ',
         '12 - Bi Tanque ',
         '13 - RodoTrem    ',
         '14 - Vanderleia  ',
         '15 - PICK-UP    ',
         '16 - VEICULO 3/4 ',
         '17 - TRUCK  ',
         '18 - CARRETA ',
         '19 - Bi-Trem ']

for name in lista:
    tv = TipoVeiculo()
    tv.codigo = name.split("-")[0].strip()
    tv.descricao = name.split("- ")[1].strip()
    tv.save()    
    
    

lista = [
    'Z2 - Vei. 2 eix (16.000)',
    'Z3 - Vei. 3 eix (23.000)   ',
    'Z4 - Vei. 4 eix < 16m (31.500)',
    'Z5 - Vei. 5 eix < 16m (41.500)  ',
    'Z6 - Vei. 5 eix < 16m distan (45.000) ',
    'Z7 - Vei. 5 eix >= 16m (41.500)',
    'Z8 - Vei. 6 eix < 16m (45.000)  ',
    'Z9 - Vei. 6 eix >= 16m tandem (48.500) ',
    'ZA - Vei. 6 eix >= 16m tandem + Isol (50.000)',
    'ZB - Vei. 6 eix >= 16m distan (53.000) ',
    'ZC - Vei. 7 eix (57.000) ',
    'ZD - Vei. 9 eix (74.000)  ',
    'ZE - Vei. 7 eix Tq c/ Lic (59.850)   ',
    'ZF - Vei. 9 eix Tq c/ Lic (77.700) ',
    'ZG - Vei. 5 eix > 16m distan (46.000)',
    'ZH - Vei. 6 eix >= 16m distan c/ Lic (55.650)',
    'ZI - Vei. 5 eix > 16m C/ Licença (43.580)',
    'ZJ - Vei. 3 eix Cav.Mec + SemiReboq. (26.000)',
    'ZK - Vei. 5 eix Cav.Mec + SemiReboq. (40.000)',
    'ZL - Vei. 3 eix Cav.Mec+Semi c/lic. (27.300) ',
    'ZM - Vei. 4 eix Cav.Mec + SemiReboq. (54.500)',
    'ZN - Vei. 4 eix Cav.Mec + SemiReboq. (36.000)',
    'ZO - Vei. 8 eix (65.500)',
    'ZP - Vei. 9 eix Cav.Mec + 3 SemiReb. (74.000)',
    'ZQ - Vei. 5 eix >= 16m tandem + Isol (43.000)',
    'ZR - Vei. 6 eix >= 16m tand+Isol(52.500)c/lic',
    'ZS - Vei. 4 eix < 16m (29.000)  ',
    'ZT - Vei. 5 eix >= 16m td+Isol c/lic.(45.150)',
    'ZU - Vei. 8 eix Cav.Mec(2 eix Direc)(63.000) ',
    'ZV - Veic. 7 eix Tandem+Eix Susp Cav (56.000)',
    'ZX - Vei. 4 eix Cv.Mc (2ei)+Semi(2ei)(33.000)',
    'ZY - Veic. 7 eixos+tandem Isol. >16m (58.500)']

for name in lista:
    pb = PesoBalanca()
    pb.codigo = name.split("-")[0].strip()
    pb.descricao = name.split("- ")[1].strip()
    pb.peso_maximo = float(re.findall('\d{2}\.?\d{3}', name)[0])
    pb.save()    
'''
