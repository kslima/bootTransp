import enum

from peewee import SqliteDatabase, Model, TextField, ForeignKeyField, BooleanField, IntegerField, DecimalField

db = SqliteDatabase('C:\\Users\\kleud\\Desktop\\sqlite\\database.db')


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


class Produto(BaseModel):
    codigo_sap = TextField(null=False)
    nome = TextField(null=False)
    deposito = TextField(null=True)
    lote = TextField(null=True)
    cfop = TextField(null=True)
    df_icms = TextField(null=True)
    df_ipi = TextField(null=True)
    df_pis = TextField(null=True)
    df_cofins = TextField(null=True)
    codigo_imposto = TextField(null=True)
    inspecao_veiculo = BooleanField(null=False, default=0)
    tipo_inspecao_veiculo = ForeignKeyField(TipoInspecaoVeiculo, backref='tipo_inspecao_veiculo', null=True)
    inspecao_produto = BooleanField(null=False, default=0)
    remover_a = BooleanField(null=False, default=0)
    tipo_lacres = IntegerField(null=False, default=0)  # 0 - Nehum / 1 - lacres normal / 2 - lacres lona
    numero_ordem = TextField(null=True)
    pedido_frete = TextField(null=True)
    icoterms1 = TextField(null=True)
    icoterms2 = TextField(null=True)
    transportador = ForeignKeyField(Transportador, backref='transportador', null=True)
    documentos_diversos = TextField(null=True)

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
    placa2 = TextField(null=True)
    placa3 = TextField(null=True)
    placa4 = TextField(null=True)
    municipio_placa1 = ForeignKeyField(Municipio, backref='municipio1')
    municipio_placa2 = ForeignKeyField(Municipio, backref='municipio2', null=True)
    municipio_placa3 = ForeignKeyField(Municipio, backref='municipio3', null=True)
    municipio_placa4 = ForeignKeyField(Municipio, backref='municipio4', null=True)


db.create_tables([Motorista])

'''
Transportador.create_table()
transp = Transportador(nome='Galego Transportes',
                       codigo_sap='1805168',
                       cidade='Iturama',
                       uf='MG',
                       cnpj_cpf='12229415001435')
transp.save()
'''