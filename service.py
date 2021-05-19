import xml.etree.ElementTree as Et
from model import Motorista, Veiculo, Municipio, Produto, Lacre, TipoCarregamento
import sqlite3
connection = sqlite3.connect("C:\\Users\\kslima\\Desktop\\sqlite\\banco.db")

# connection = sqlite3.connect("C:\\Users\\kleud\\Desktop\\sqlite\\banco.db")

FILE_PATH = "properties.xml"


def load_xml_file():
    source = open(FILE_PATH)
    tree = Et.parse(source)
    root = tree.getroot()
    return source, tree, root


def listar_produtos():
    xml = load_xml_file()
    root = xml[2]
    produtos = []
    for tag_produto in root.findall("produto"):
        for item in tag_produto.findall("item"):
            produto = Produto()
            produto.codigo = item.get("codigo")
            produto.nome = item.get("nome")
            produto.deposito = item.get("deposito")
            produto.lote = item.get("lote")
            produto.inspecao_veiculo = item.get("inspecao_veiculo")
            produto.inspecao_produto = item.get("inspecao_produto")
            produto.remover_a = item.get("remover_a")
            produtos.append(produto)
    xml[0].close()
    return produtos


# pesquisa um produto pela descricao
def procurar_produto_pelo_nome(nome_produto):
    produtos = listar_produtos()
    for p in produtos:
        if p.nome == nome_produto:
            return p


# pesquisa um produto pela descricao
def procurar_produto_pelo_codigo(codigo_produto):
    produtos = listar_produtos()
    for p in produtos:
        if p.codigo == codigo_produto:
            return p


def cadastrar_produto_se_nao_exister(novo_produto):
    xml = load_xml_file()
    root = xml[2]
    produto_procurado = procurar_produto_pelo_codigo(novo_produto.codigo)
    if produto_procurado is None:
        try:
            atributos_novo_produto = {"codigo": novo_produto.codigo,
                                      "nome": novo_produto.nome,
                                      "deposito": novo_produto.deposito,
                                      "lote": novo_produto.lote,
                                      "inspecao_veiculo": novo_produto.inspecao_veiculo,
                                      "inspecao_produto": novo_produto.inspecao_produto,
                                      "remover_a": novo_produto.remover_a}

            produto_tag = root.find('produto')
            item = Et.SubElement(produto_tag, 'item', atributos_novo_produto)
            item.attrib = atributos_novo_produto
            xml[1].write(FILE_PATH)
            return 1, "Produto cadastrado com sucesso!"
        except Exception as e:
            print(e)
            return 0, "Erro ao cadastrar novo produto!\n{}".format(str(e))
        finally:
            xml[0].close()
    else:
        return -1, "Já existe um produto cadastrado com esses dados!"


def atualizar_produto(produto_para_atualizar):
    xml = load_xml_file()
    try:
        root = xml[2]
        for produto_tag in root.findall("produto"):
            for item in produto_tag.findall("item"):
                if item.get("codigo") == produto_para_atualizar.codigo:
                    item.attrib['nome'] = produto_para_atualizar.nome
                    item.attrib['deposito'] = produto_para_atualizar.deposito
                    item.attrib['lote'] = produto_para_atualizar.lote
                    item.attrib['inspecao_veiculo'] = produto_para_atualizar.inspecao_veiculo
                    item.attrib['inspecao_produto'] = produto_para_atualizar.inspecao_produto
                    item.attrib['remover_a'] = produto_para_atualizar.remover_a
        xml[1].write(FILE_PATH)
        return True, "Produto '{}' atualizado com sucesso!".format(produto_para_atualizar.codigo)
    except Exception as e:
        return False, "Erro ao atualizar novo produto!\n{}".format(str(e))
    finally:
        xml[0].close()


# lista todos os motoristas
def listar_motoristas():
    xml = load_xml_file()
    root = xml[2]
    motoristas = []
    for tag_motorista in root.findall("motorista"):
        for item in tag_motorista.findall("item"):
            motorista = Motorista(nome=item.get("nome"),
                                  cpf=item.get("cpf"),
                                  cnh=item.get("cnh"),
                                  rg=item.get("rg"))
            motoristas.append(motorista)
    xml[0].close()

    for motorista in motoristas:
        MotoristaService.inserir_motoristas(motorista)
    return motoristas


# pesquisa um motorista pelo cpf, cnh ou rg
def procurar_motorista_por_documento(*args):
    motoristas = listar_motoristas()
    _motorista = None
    for motorista in motoristas:
        for documento in args:
            if __comparar_ignorando_vazio(motorista.cpf, documento) or \
                    __comparar_ignorando_vazio(motorista.cnh, documento) or \
                    __comparar_ignorando_vazio(motorista.rg, documento):
                _motorista = motorista

    # caso nao encontre, ele verifica se contem
    if _motorista is None:
        for motorista in motoristas:
            for documento in args:
                if __verificar_se_contem_ignorando_vazio(documento, motorista.cpf) or \
                        __verificar_se_contem_ignorando_vazio(documento, motorista.cnh) or \
                        __verificar_se_contem_ignorando_vazio(documento, motorista.rg):
                    _motorista = motorista
    return _motorista


# cria um novo motorista
def cadastrar_motorista_se_nao_existir(novo_motorista):
    xml = load_xml_file()
    root = xml[2]
    motorista_procurado = procurar_motorista_por_documento(novo_motorista.cpf, novo_motorista.cnh, novo_motorista.rg)
    if motorista_procurado is None:
        try:
            atributos_motorista = {"nome": novo_motorista.nome,
                                   "cpf": novo_motorista.cpf,
                                   "cnh": novo_motorista.cnh,
                                   "rg": novo_motorista.rg}

            motorista_tag = root.find('motorista')
            item = Et.SubElement(motorista_tag, 'item', atributos_motorista)
            item.attrib = atributos_motorista
            xml[1].write(FILE_PATH)
            return 1, "Motorista cadastrado com sucesso!"
        except Exception as e:
            print(e)
            return 0, "Erro ao cadastrar novo motorista!\n{}".format(str(e))
        finally:
            xml[0].close()
    else:
        return -1, "já existe um motorista cadastrado com esses dados!"


def atualizar_motorista(motorista_para_atualizar):
    xml = load_xml_file()
    try:
        root = xml[2]
        for tag_motorista in root.findall("motorista"):
            for item in tag_motorista.findall("item"):
                if item.get("cpf") == motorista_para_atualizar.cpf or item.get("cnh") == motorista_para_atualizar.cnh \
                        or item.get("rg") == motorista_para_atualizar.rg:
                    item.attrib['nome'] = motorista_para_atualizar.nome
                    item.attrib['cpf'] = motorista_para_atualizar.cpf
                    item.attrib['cnh'] = motorista_para_atualizar.cnh
                    item.attrib['rg'] = motorista_para_atualizar.rg

        xml[1].write(FILE_PATH)
        return True, "Motorista '{}' atualizado com sucesso!".format(motorista_para_atualizar.nome)
    except Exception as e:
        return False, "Erro ao atualizar motorista {}!\n{}".format(motorista_para_atualizar.nome, str(e))
    finally:
        xml[0].close()


def listar_veiculos():
    xml = load_xml_file()
    root = xml[2]
    veiculos = []
    for tag_veiculo in root.findall("veiculo"):
        for item in tag_veiculo.findall("item"):
            veiculo = Veiculo(tipo_veiculo=item.get("tipo_veiculo"),
                              tolerancia_balanca=item.get("tolerancia_balanca"),
                              quantidade_lacres=item.get("quantidade_lacres"),
                              placa_1=item.get("placa_1"),
                              placa_2=item.get("placa_2"),
                              placa_3=item.get("placa_3"),
                              placa_4=item.get("placa_4"),
                              codigo_municipio_placa_1=item.get("codigo_municipio_placa_1"),
                              codigo_municipio_placa_2=item.get("codigo_municipio_placa_2"),
                              codigo_municipio_placa_3=item.get("codigo_municipio_placa_3"),
                              codigo_municipio_placa_4=item.get("codigo_municipio_placa_4"))
            veiculos.append(veiculo)
    xml[0].close()

    for veiculo in veiculos:
        VeiculoService.inserir_veiculo(veiculo)
    return veiculos


def procurar_veiculos(placa):
    lista_veiculos = listar_veiculos()
    veiculos_encontrados = []
    for veiculo in lista_veiculos:
        if veiculo.placa_1 == placa:
            veiculos_encontrados.append(veiculo)
    return veiculos_encontrados


def cadastrar_veiculo_se_nao_exister(novo_veiculo):
    xml = load_xml_file()
    root = xml[2]
    veiculo_procurado = procurar_veiculos(novo_veiculo.placa_1)
    if len(veiculo_procurado) == 0:
        try:
            atributos_novo_produto = {"tipo_veiculo": novo_veiculo.tipo_veiculo.strip(),
                                      "tolerancia_balanca": novo_veiculo.tolerancia_balanca.strip(),
                                      "quantidade_lacres": novo_veiculo.quantidade_lacres.strip(),
                                      "placa_1": novo_veiculo.placa_1.strip(),
                                      "placa_2": novo_veiculo.placa_2.strip(),
                                      "placa_3": novo_veiculo.placa_3.strip(),
                                      "placa_4": novo_veiculo.placa_4.strip(),
                                      "codigo_municipio_placa_1": novo_veiculo.codigo_municipio_placa_1.strip(),
                                      "codigo_municipio_placa_2": novo_veiculo.codigo_municipio_placa_2.strip(),
                                      "codigo_municipio_placa_3": novo_veiculo.codigo_municipio_placa_3.strip(),
                                      "codigo_municipio_placa_4": novo_veiculo.codigo_municipio_placa_4.strip()}

            tag_veiculo = root.find('veiculo')
            item = Et.SubElement(tag_veiculo, 'item', atributos_novo_produto)
            item.attrib = atributos_novo_produto
            xml[1].write(FILE_PATH)
            return 1, "Veículo cadastrado com sucesso!"
        except Exception as e:
            print(e)
            return 0, "Erro ao cadastrar novo Veículo!\n{}".format(str(e))
        finally:
            xml[0].close()
    else:
        return -1, "Já existe um veículo cadastrado com esses dados!"


def atualizar_veiculo(veiculo_para_atualizar):
    xml = load_xml_file()
    try:
        root = xml[2]
        for tag_veiculo in root.findall("veiculo"):
            for item in tag_veiculo.findall("item"):
                if item.get("placa_1") == veiculo_para_atualizar.placa_1:
                    item.attrib['tipo_veiculo'] = veiculo_para_atualizar.tipo_veiculo
                    item.attrib['tolerancia_balanca'] = veiculo_para_atualizar.tolerancia_balanca
                    item.attrib['quantidade_lacres'] = veiculo_para_atualizar.quantidade_lacres
                    item.attrib['placa_1'] = veiculo_para_atualizar.placa_1
                    item.attrib['placa_2'] = veiculo_para_atualizar.placa_2
                    item.attrib['placa_3'] = veiculo_para_atualizar.placa_3
                    item.attrib['placa_4'] = veiculo_para_atualizar.placa_4
                    item.attrib['codigo_municipio_placa_1'] = veiculo_para_atualizar.codigo_municipio_placa_1
                    item.attrib['codigo_municipio_placa_2'] = veiculo_para_atualizar.codigo_municipio_placa_2
                    item.attrib['codigo_municipio_placa_3'] = veiculo_para_atualizar.codigo_municipio_placa_3
                    item.attrib['codigo_municipio_placa_4'] = veiculo_para_atualizar.codigo_municipio_placa_4

        xml[1].write(FILE_PATH)
        return True, "Veículo '{}' atualizado com sucesso!".format(veiculo_para_atualizar.placa_1)
    except Exception as e:
        return False, "Erro ao atualizar veículo {}!\n{}".format(veiculo_para_atualizar.placa_1, str(e))
    finally:
        xml[0].close()


def __comparar_ignorando_vazio(v1, v2):
    if v1 == "" or v2 == "":
        return False
    return v1 == v2


def __verificar_se_contem_ignorando_vazio(v1, v2):
    if v1 == "" or v2 == "":
        return False
    return v1 in v2


class MunicipioService:
    @staticmethod
    def listar_municipios_brasileiros():
        municipios = []
        with connection as conn:
            cursor = conn.cursor()
            rows = cursor.execute("SELECT rowid, nome, codigo_municipio, uf FROM municipio").fetchall()
            for row in rows:
                municipios.append(Municipio(id_municipio=row[0],
                                            nome_municipio=row[1],
                                            codigo_municipio=row[2],
                                            uf=row[3]))
        return municipios


class ProdutoService:
    @staticmethod
    def listar_produtos():
        produtos = []
        with connection as conn:
            cursor = conn.cursor()
            rows = cursor.execute("SELECT rowid,"
                                  " codigo, nome,"
                                  " deposito, lote,"
                                  " inspecao_veiculo,"
                                  " inspecao_produto,"
                                  " remover_a "
                                  "FROM produto").fetchall()
            for row in rows:
                produtos.append(Produto(id_produto=row[0],
                                        codigo=row[1],
                                        nome=row[2],
                                        deposito=row[3],
                                        lote=row[4],
                                        inspecao_veiculo=row[5],
                                        inspecao_produto=row[6],
                                        remover_a=row[7]))
        return produtos

    @staticmethod
    def inserir_produto(produto):
        sql = "INSERT INTO produto VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(produto.codigo,
                                                                                             produto.nome,
                                                                                             produto.deposito,
                                                                                             produto.lote,
                                                                                             produto.inspecao_veiculo,
                                                                                             produto.inspecao_produto,
                                                                                             produto.remover_a)
        with connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql)
                connection.commit()
            except sqlite3.Error:
                conn.rollback()
                return "Erro ao inserir novo produto!"

    @staticmethod
    def deletar_produto(produto_id):
        sql = "DELETE FROM produto WHERE rowid = ?"
        with connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql, str(produto_id))
                connection.commit()
            except sqlite3.Error:
                conn.rollback()
                return "Erro ao deletar produto!"

    @staticmethod
    def atualizar_produto(produto):
        sql = "UPDATE produto SET" \
              " codigo = ?," \
              " nome = ?," \
              " deposito = ?," \
              " lote = ?," \
              " inspecao_veiculo = ?," \
              " inspecao_produto = ?," \
              " remover_a = ?" \
              " WHERE rowid = ?"
        with connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql, (produto.codigo,
                                     produto.nome,
                                     produto.deposito,
                                     produto.lote,
                                     produto.inspecao_veiculo,
                                     produto.inspecao_produto,
                                     produto.remover_a,
                                     produto.id_produto))
                connection.commit()
            except sqlite3.Error:
                conn.rollback()
                return "Erro ao atualizar produto!"

    @staticmethod
    def pesquisar_produto_pelo_codigo(codigo_produto):
        sql = "SELECT rowid," \
              " codigo, nome," \
              " deposito, lote," \
              " inspecao_veiculo," \
              " inspecao_produto," \
              " remover_a " \
              "FROM produto WHERE codigo = {}".format(codigo_produto)
        with connection as conn:
            cursor = conn.cursor()
            row = cursor.execute(sql).fetchone()
            produto = Produto(id_produto=row[0],
                              codigo=row[1],
                              nome=row[2],
                              deposito=row[3],
                              lote=row[4],
                              inspecao_veiculo=row[5],
                              inspecao_produto=row[6],
                              remover_a=row[7])
        return produto


class MotoristaService:
    @staticmethod
    def listar_motoristas():
        motoristas = []
        with connection as conn:
            cursor = conn.cursor()
            rows = cursor.execute("SELECT rowid,"
                                  " nome,"
                                  " cpf,"
                                  " cnh,"
                                  " rg"
                                  " FROM motorista").fetchall()
            for row in rows:
                motoristas.append(Motorista(id_motorista=row[0],
                                            nome=row[1],
                                            cpf=row[2],
                                            cnh=row[3],
                                            rg=row[4]))
        return motoristas

    @staticmethod
    def inserir_motoristas(motorista):
        motoristas = MotoristaService.listar_motoristas()
        for mot in motoristas:
            if motorista.id_motorista != str(mot.id_motorista) and (motorista.cpf == mot.cpf
                                                                    or motorista.cnh == mot.cpf
                                                                    or motorista.rg == mot.rg):
                return False, "Já existe um motorista cadastrado com esses dados!"

        with connection as conn:
            cursor = conn.cursor()
            sql = "INSERT INTO motorista VALUES (?, ?, ?, ?)"
            try:
                cursor.execute(sql, (motorista.nome,
                                     motorista.cpf if motorista.cpf else None,
                                     motorista.cnh if motorista.cnh else None,
                                     motorista.rg if motorista.rg else None))
                connection.commit()
                return True, "Motorista salvo com sucesso!"

            except sqlite3.Error as e:
                conn.rollback()
                return False, "Erro ao inserir novo motorista!\n{}".format(e)

    @staticmethod
    def atualizar_motorista(motorista):
        motoristas = MotoristaService.listar_motoristas()
        for mot in motoristas:
            if motorista.id_motorista != str(mot.id_motorista) and (motorista.cpf == mot.cpf
                                                                    or motorista.cnh == mot.cpf
                                                                    or motorista.rg == mot.rg):
                return False, "Já existe um motorista cadastrado com esses dados!"

        with connection as conn:
            cursor = conn.cursor()
            sql = "UPDATE motorista SET" \
                  " nome = ?," \
                  " cpf = ?," \
                  " cnh = ?," \
                  " rg = ? " \
                  " WHERE rowid = ?"

            try:
                cursor.execute(sql, (motorista.nome,
                                     motorista.cpf,
                                     motorista.cnh,
                                     motorista.rg,
                                     motorista.id_motorista))
                connection.commit()
                return True, "Motorista atualizado com sucesso!"

            except sqlite3.Error as e:
                conn.rollback()
                return False, "Erro ao atualizar motorista!\n{}".format(e)

    @staticmethod
    def deletar_motoristas(id_motorista):
        with connection as conn:
            cursor = conn.cursor()
            sql = "DELETE FROM motorista WHERE rowid = ?"

            try:
                cursor.execute(sql, (id_motorista,))
                connection.commit()
                return True, "Motorista deletado com sucesso"
            except sqlite3.Error as e:
                conn.rollback()
                print(e)
                return False, "Erro ao deletar novo motorista!"

    @staticmethod
    def pesquisar_motorista(criterio):
        motoristas = []
        with connection as conn:
            cursor = conn.cursor()
            sql = "SELECT rowid," \
                  " nome," \
                  " cpf," \
                  " cnh," \
                  " rg" \
                  " FROM motorista WHERE nome like ? or cpf like ? or cnh like ? or rg like ?"
            rows = cursor.execute(sql,
                                  ('%{}%'.format(criterio),
                                   '%{}%'.format(criterio),
                                   '%{}%'.format(criterio),
                                   '%{}%'.format(criterio))
                                  ).fetchall()
            for row in rows:
                motoristas.append(Motorista(id_motorista=row[0],
                                            nome=row[1],
                                            cpf=row[2],
                                            cnh=row[3],
                                            rg=row[4]))
        return motoristas


class VeiculoService:
    @staticmethod
    def listar_veiculos():
        veiculos = []
        with connection as conn:
            cursor = conn.cursor()
            rows = cursor.execute("SELECT rowid,"
                                  " tipo_veiculo,"
                                  " tolerancia_balanca,"
                                  " quantidade_lacres,"
                                  " placa_1,"
                                  " placa_2,"
                                  " placa_3,"
                                  " placa_4,"
                                  " codigo_municipio_placa_1,"
                                  " codigo_municipio_placa_2,"
                                  " codigo_municipio_placa_3,"
                                  " codigo_municipio_placa_4"
                                  " FROM veiculo").fetchall()
            for row in rows:
                veiculos.append(Veiculo(id_veiculo=row[0],
                                        tipo_veiculo=row[1],
                                        tolerancia_balanca=row[2],
                                        quantidade_lacres=row[3],
                                        placa_1=row[4],
                                        placa_2=row[5],
                                        placa_3=row[6],
                                        placa_4=row[7],
                                        codigo_municipio_placa_1=row[8],
                                        codigo_municipio_placa_2=row[9],
                                        codigo_municipio_placa_3=row[10],
                                        codigo_municipio_placa_4=row[11]))
        return veiculos

    @staticmethod
    def inserir_veiculo(veiculo):
        with connection as conn:
            cursor = conn.cursor()
            sql = "INSERT INTO veiculo VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            try:
                cursor.execute(sql, (veiculo.tipo_veiculo,
                                     veiculo.tolerancia_balanca,
                                     veiculo.quantidade_lacres if veiculo.quantidade_lacres else None,
                                     veiculo.placa_1,
                                     veiculo.placa_2 if veiculo.placa_2 else None,
                                     veiculo.placa_3 if veiculo.placa_1 else None,
                                     veiculo.placa_4 if veiculo.placa_1 else None,
                                     veiculo.codigo_municipio_placa_1,
                                     veiculo.codigo_municipio_placa_2 if veiculo.codigo_municipio_placa_2 else None,
                                     veiculo.codigo_municipio_placa_3 if veiculo.codigo_municipio_placa_3 else None,
                                     veiculo.codigo_municipio_placa_4 if veiculo.codigo_municipio_placa_4 else None))
                connection.commit()
                return True, "Veículo salvo com sucesso!"
            except sqlite3.IntegrityError as e:
                conn.rollback()
                return False, "Erro!\nVeículo já cadastrado!"

            except sqlite3.Error as e:
                conn.rollback()
                return False, "Erro ao inserir veículo!\n{}".format(e)

    @staticmethod
    def atualizar_veiculo(veiculo):
        with connection as conn:
            cursor = conn.cursor()
            sql = "UPDATE veiculo SET" \
                  " tipo_veiculo = ?," \
                  " tolerancia_balanca = ?," \
                  " quantidade_lacres = ?," \
                  " placa_1 = ?, " \
                  " placa_2 = ?, " \
                  " placa_3 = ?, " \
                  " placa_4 = ?, " \
                  " codigo_municipio_placa_1 = ?, " \
                  " codigo_municipio_placa_2 = ?, " \
                  " codigo_municipio_placa_3 = ?, " \
                  " codigo_municipio_placa_4 = ? " \
                  " WHERE rowid = ?"

            try:
                cursor.execute(sql, (veiculo.tipo_veiculo,
                                     veiculo.tolerancia_balanca,
                                     veiculo.quantidade_lacres if veiculo.quantidade_lacres else None,
                                     veiculo.placa_1,
                                     veiculo.placa_2 if veiculo.placa_2 else None,
                                     veiculo.placa_3 if veiculo.placa_1 else None,
                                     veiculo.placa_4 if veiculo.placa_1 else None,
                                     veiculo.codigo_municipio_placa_1,
                                     veiculo.codigo_municipio_placa_2 if veiculo.codigo_municipio_placa_2 else None,
                                     veiculo.codigo_municipio_placa_3 if veiculo.codigo_municipio_placa_3 else None,
                                     veiculo.codigo_municipio_placa_4 if veiculo.codigo_municipio_placa_4 else None,
                                     veiculo.id_veiculo))
                connection.commit()
                return True, "Veículo atualizado com sucesso!"
            except sqlite3.Error as e:
                conn.rollback()
                return False, "Erro ao atualizar veículo!\n{}".format(e)

    @staticmethod
    def deletar_veiculo(id_veiculo):
        with connection as conn:
            cursor = conn.cursor()
            sql = "DELETE FROM veiculo WHERE rowid = ?"

            try:
                cursor.execute(sql, str(id_veiculo))
                connection.commit()
                return True, "Veículo deletado com sucesso"
            except sqlite3.Error:
                conn.rollback()
                return False, "Erro ao deletar veículo!"

    @staticmethod
    def pesquisar_veiculo(criterio):
        veiculos = []
        with connection as conn:
            cursor = conn.cursor()
            sql = "SELECT rowid," \
                  " tipo_veiculo," \
                  " tolerancia_balanca," \
                  " quantidade_lacres," \
                  " placa_1," \
                  " placa_2," \
                  " placa_3," \
                  " placa_4," \
                  " codigo_municipio_placa_1," \
                  " codigo_municipio_placa_2," \
                  " codigo_municipio_placa_3," \
                  " codigo_municipio_placa_4" \
                  " FROM veiculo where placa_1 like ? or placa_2 like ? or placa_3 like ? or placa_4 like ?"
            rows = cursor.execute(sql,
                                  ('%{}%'.format(criterio),
                                   '%{}%'.format(criterio),
                                   '%{}%'.format(criterio),
                                   '%{}%'.format(criterio))
                                  ).fetchall()
            for row in rows:
                veiculos.append(Veiculo(id_veiculo=row[0],
                                        tipo_veiculo=row[1],
                                        tolerancia_balanca=row[2],
                                        quantidade_lacres=row[3],
                                        placa_1=row[4],
                                        placa_2=row[5],
                                        placa_3=row[6],
                                        placa_4=row[7],
                                        codigo_municipio_placa_1=row[8],
                                        codigo_municipio_placa_2=row[9],
                                        codigo_municipio_placa_3=row[10],
                                        codigo_municipio_placa_4=row[11]))
        return veiculos

    @staticmethod
    def pesquisar_veiculo_pelo_id(id_veiculo):
        with connection as conn:
            cursor = conn.cursor()
            sql = "SELECT rowid," \
                  " tipo_veiculo," \
                  " tolerancia_balanca," \
                  " quantidade_lacres," \
                  " placa_1," \
                  " placa_2," \
                  " placa_3," \
                  " placa_4," \
                  " codigo_municipio_placa_1," \
                  " codigo_municipio_placa_2," \
                  " codigo_municipio_placa_3," \
                  " codigo_municipio_placa_4" \
                  " FROM veiculo where rowid = ?"
            row = cursor.execute(sql, (id_veiculo,)).fetchone()
            return Veiculo(id_veiculo=row[0],
                           tipo_veiculo=row[1],
                           tolerancia_balanca=row[2],
                           quantidade_lacres=row[3],
                           placa_1=row[4],
                           placa_2=row[5],
                           placa_3=row[6],
                           placa_4=row[7],
                           codigo_municipio_placa_1=row[8],
                           codigo_municipio_placa_2=row[9],
                           codigo_municipio_placa_3=row[10],
                           codigo_municipio_placa_4=row[11])

    @staticmethod
    def listar_tolerancias_balanca():
        return ["Z2 - Vei. 2 eix(16.000)",
                "Z3 - Vei. 3 eix(23.000)",
                "Z4 - Vei. 4 eix < 16m(31500)",
                "Z5 - Vei. 5 eix < 16m(41500)",
                "Z6 - Vei. 5 eix < 16m distan(45000)",
                "Z7 - Vei. 5 eix >= 16m(41500)",
                "Z8 - Vei. 6 eix < 16m(45000)",
                "Z9 - Vei. 6 eix >= 16m tandem(48500)",
                "ZA - Vei. 6 eix >= 16m tandem + Isol(50.000)",
                "ZB - Vei. 6 eix >= 16m distan(53.000)",
                "ZC - Vei. 7 eix(57.000)",
                "ZD - Vei. 9 eix(74.000)",
                "ZE - Vei. 7 eix Tq c/ Lic(59.850)",
                "ZF - Vei. 9 eix Tq c/ Lic(77.700)",
                "ZG - Vei. 5 eix > 16m distan(46.000)",
                "ZH - Vei. 6 eix >= 16m distan c/ Lic(55.650)",
                "ZI - Vei. 5 eix > 16m C/ Licença(43.580)",
                "ZJ - Vei. 3 eix Cav.Mec + SemiReboq.(26.000)",
                "ZK - Vei. 5 eix Cav.Mec + SemiReboq.(40.000)",
                "ZL - Vei. 3 eix Cav.Mec+Semi c/lic.(27.300)"]

    @staticmethod
    def listar_tipos_veiculos():
        return ["01 - Outros",
                "02 - Postal",
                "03 - Ferroviário",
                "04 - Marítimo",
                "05 - Graneleiro",
                "06 - Caçamba",
                "07 - Tanque",
                "08 - Coleta",
                "09 - Bi Caçamba",
                "10 - Bi Graneleiro",
                "11 - Hopper",
                "12 - Bi Tanque",
                "13 - RodoTrem",
                "14 - Vanderleia",
                "15 - PICK-UP",
                "16 - VEICULO 3/4",
                "17 - TRUCK",
                "18 - CARRETA",
                "19 - Bi-Trem"]


class LacreService:
    @staticmethod
    def listar_lacres():
        lacres = []
        with connection as conn:
            cursor = conn.cursor()
            rows = cursor.execute("SELECT rowid,"
                                  " codigo,"
                                  " numero"
                                  " FROM lacre").fetchall()
            for row in rows:
                lacres.append(Lacre(id_lacre=row[0],
                                    codigo=row[1],
                                    numero=row[2]))
        return lacres

    @staticmethod
    def inserir_pacotes_lacres(lacres):
        with connection as conn:
            cursor = conn.cursor()
            sql = "INSERT INTO lacre VALUES (?, ?)"
            numero_lacre_atual = ''
            try:
                for lacre in lacres:
                    numero_lacre_atual = lacre.numero
                    cursor.execute(sql, (lacre.codigo, lacre.numero))
                connection.commit()
                return True, "Lacres salvos com sucesso!" \
                             "\nCódigo: {}".format(lacres[0].codigo)
            except sqlite3.IntegrityError as e:
                conn.rollback()
                print(e)
                return False, "Erro!\nLacre(s) já cadastrado(s)\nLacre duplicado: {}".format(numero_lacre_atual)

            except sqlite3.Error as e:
                conn.rollback()
                return False, "Erro ao inserir lacres!\n{}".format(e)

    @staticmethod
    def atualizar_pacote_lacres(lacres):
        with connection as conn:
            cursor = conn.cursor()
            sql = "UPDATE lacre SET" \
                  " numero = ?" \
                  " WHERE rowid = ?"
        numero_lacre_atual = ''
        try:
            for lacre in lacres:
                numero_lacre_atual = lacre.numero
                cursor.execute(sql, (lacre.numero,
                                     lacre.id_lacre))
            connection.commit()
            return True, "Lacres atualizados com sucesso!"
        except sqlite3.IntegrityError as e:
            conn.rollback()
            print(e)
            return False, "Erro!\nLacre(s) já cadastrado(s)\nLacre duplicado: {}".format(numero_lacre_atual)
        except sqlite3.Error as e:
            conn.rollback()
            return False, "Erro ao atualizar lacre{}!".format(numero_lacre_atual)

    @staticmethod
    def deletar_pacote_lacres(lacres):
        with connection as conn:
            cursor = conn.cursor()
            sql = "DELETE FROM lacre WHERE rowid = ?"

            try:
                for lacre in lacres:
                    cursor.execute(sql, (lacre.id_lacre,))
                connection.commit()
                return True, "Lacres deletado com sucesso"

            except sqlite3.Error as re:
                conn.rollback()
                print(re)
                return False, "Erro ao deletar pacote de lacres!"

    @staticmethod
    def pesquisar_pacote_lacres_pelo_codigo(codigo):
        lacres = []
        with connection as conn:
            cursor = conn.cursor()
            sql = "SELECT rowid," \
                  " codigo," \
                  " numero" \
                  " FROM lacre WHERE codigo = ?"
        rows = cursor.execute(sql, (codigo,)).fetchall()
        for row in rows:
            lacres.append(Lacre(id_lacre=row[0],
                                codigo=row[1],
                                numero=row[2]))
        return lacres


class TipoCarregamentoService:
    @staticmethod
    def listar_tipos_carregamento():
        tipos_carregamento = []
        with connection as conn:
            cursor = conn.cursor()
            rows = cursor.execute("SELECT rowid,"
                                  " nome,"
                                  " numero_ordem,"
                                  " numero_pedido_frete,"
                                  " inspecao_veiculo,"
                                  " inspecao_produto,"
                                  " remover_a,"
                                  " tipo_frete,"
                                  " destino_frete,"
                                  " codigo_transportador,"
                                  " tipo_lacre,"
                                  " doc_diversos,"
                                  " itens_str"
                                  " FROM tipo_carregamento").fetchall()
            for row in rows:
                tc = TipoCarregamento()
                tc.id_tipo_carregamento = row[0]
                tc.nome = row[1]
                tc.numero_ordem = row[2]
                tc.numero_pedido_frete = row[3]
                tc.inspecao_veiculo = row[4]
                tc.inspecao_produto = row[5]
                tc.remover_a = row[6]
                tc.tipo_frete = row[7]
                tc.destino_frete = row[8]
                tc.codigo_transportador = row[9]
                tc.tipo_lacre = row[10]
                tc.doc_diversos = row[11]
                tc.itens_str = row[12]

                tipos_carregamento.append(tc)
        return tipos_carregamento

    @staticmethod
    def inserir_tipo_carregamento(tipo_carreagmento):
        sql = "INSERT INTO tipo_carregamento (" \
              " nome," \
              " numero_ordem," \
              " numero_pedido_frete," \
              " inspecao_veiculo," \
              " inspecao_produto, " \
              " remover_a," \
              " tipo_frete," \
              " destino_frete," \
              " codigo_transportador," \
              " tipo_lacre," \
              " doc_diversos," \
              " itens_str)" \
              " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        with connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql, (tipo_carreagmento.nome,
                                     tipo_carreagmento.numero_ordem,
                                     tipo_carreagmento.numero_pedido_frete,
                                     tipo_carreagmento.inspecao_veiculo,
                                     tipo_carreagmento.inspecao_produto,
                                     tipo_carreagmento.remover_a,
                                     tipo_carreagmento.tipo_frete,
                                     tipo_carreagmento.destino_frete,
                                     tipo_carreagmento.codigo_transportador,
                                     tipo_carreagmento.tipo_lacre,
                                     tipo_carreagmento.doc_diversos,
                                     tipo_carreagmento.itens_str))
                connection.commit()
            except sqlite3.Error:
                conn.rollback()
                return "Erro ao inserir novo tipo de carregamento!"

    @staticmethod
    def deletar_tipo_carregamento(id_tipo_carregamento):
        sql = "DELETE FROM tipo_carregamento WHERE rowid = ?"
        with connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql, str(id_tipo_carregamento, ))
                connection.commit()
            except sqlite3.Error:
                conn.rollback()
                return "Erro ao deletar tipo de carregamento!"

    @staticmethod
    def atualizar_tipo_carregamento(tipo_carreagmento):

        sql = "UPDATE tipo_carregamento SET" \
              " nome = ?," \
              " numero_ordem = ?," \
              " numero_pedido_frete = ?," \
              " inspecao_veiculo = ?," \
              " inspecao_produto = ?, " \
              " remover_a = ?," \
              " tipo_frete = ?," \
              " destino_frete = ?," \
              " codigo_transportador = ?," \
              " tipo_lacre = ?," \
              " doc_diversos = ?," \
              " itens_str = ?)" \
              " WHERE rowid = ?"

        with connection as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(sql, (tipo_carreagmento.nome,
                                     tipo_carreagmento.numero_ordem,
                                     tipo_carreagmento.numero_pedido_frete,
                                     tipo_carreagmento.inspecao_veiculo,
                                     tipo_carreagmento.inspecao_produto,
                                     tipo_carreagmento.remover_a,
                                     tipo_carreagmento.tipo_frete,
                                     tipo_carreagmento.destino_frete,
                                     tipo_carreagmento.codigo_transportador,
                                     tipo_carreagmento.tipo_lacre,
                                     tipo_carreagmento.doc_diversos,
                                     tipo_carreagmento.itens_str,
                                     tipo_carreagmento.id_tipo_carregamento))
                connection.commit()
            except sqlite3.Error:
                conn.rollback()
                return "Erro ao atualizar tipo de carregamento!"

    @staticmethod
    def pesquisar_tipo_carregamento(id_tipo_carregamento):
        sql = " SELECT rowid," \
              " nome," \
              " numero_ordem," \
              " numero_pedido_frete," \
              " inspecao_veiculo," \
              " inspecao_produto," \
              " remover_a," \
              " tipo_frete," \
              " destino_frete," \
              " codigo_transportador," \
              " tipo_lacre," \
              " doc_diversos," \
              " itens_str" \
              " FROM tipo_carregamento WHERE rowid == ?"
        with connection as conn:
            cursor = conn.cursor()
            row = cursor.execute(sql, (id_tipo_carregamento,)).fetchone()
            tc = TipoCarregamento()
            tc.id_tipo_carregamento = row[0]
            tc.nome = row[1]
            tc.numero_ordem = row[2]
            tc.numero_pedido_frete = row[3]
            tc.inspecao_veiculo = row[4]
            tc.inspecao_produto = row[5]
            tc.remover_a = row[6]
            tc.tipo_frete = row[7]
            tc.destino_frete = row[8]
            tc.codigo_transportador = row[9]
            tc.tipo_lacre = row[10]
            tc.doc_diversos = row[11]
            tc.itens_str = row[12]

            return tc


if __name__ == '__main__':
    # listar_veiculos()
    pass
