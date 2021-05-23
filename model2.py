import enum

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


class TipoInspecaoVeiculo(BaseModel):
    descricao = TextField(null=False)


class CanalDistribuicao(BaseModel):
    codigo = IntegerField(unique=True)
    descricao = TextField()


class SetorAtividade(BaseModel):
    descricao = TextField()
    codigo = IntegerField()


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
    tipo_inspecao_veiculo = ForeignKeyField(TipoInspecaoVeiculo, backref='tipo_inspecao_veiculo', null=True)
    inspecao_produto = BooleanField(default=0)
    remover_a = BooleanField(default=0)
    tipo_lacres = IntegerField(default=0)  # 0 - Nehum / 1 - lacres normal / 2 - lacres lona
    numero_ordem = TextField()
    pedido_frete = TextField()
    icoterms1 = TextField()
    icoterms2 = TextField()
    transportador = ForeignKeyField(Transportador, backref='transportador', null=True)
    documentos_diversos = TextField()

    def __str__(self):
        return "{} - {}".format(self.codigo_sap, self.nome)


class Motorista(BaseModel):
    nome = TextField(null=False)
    cpf = TextField(null=True, unique=True)
    cnh = TextField(null=True, unique=True)
    rg = TextField(null=True, unique=True)


class TipoVeiculo(BaseModel):
    descricao = TextField()


class PesoBalanca(BaseModel):
    descricao = TextField()
    peso_maximo = DecimalField()


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


# db.create_tables([Municipio, Transportador, TipoInspecaoVeiculo, CanalDistribuicao, SetorAtividade, Produto, Motorista, TipoVeiculo, PesoBalanca, Veiculo])
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
'''