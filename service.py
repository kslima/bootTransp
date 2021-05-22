import xml.etree.ElementTree as Et
import peewee
from model2 import Municipio, Veiculo, Motorista, PesoBalanca, TipoVeiculo
from model import Lacre, TipoCarregamento, Transportador
import sqlite3

# connection = sqlite3.connect("C:\\Users\\kslima\\Desktop\\sqlite\\banco.db")

connection = sqlite3.connect("C:\\Users\\kleud\\Desktop\\sqlite\\banco.db")

FILE_PATH = "properties.xml"


def load_xml_file():
    source = open(FILE_PATH)
    tree = Et.parse(source)
    root = tree.getroot()
    return source, tree, root


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
        return Municipio.select()

    @staticmethod
    def pesquisar_municipio_pelo_codigo(codigo):
        return Municipio.select().where(Municipio.codigo == codigo)


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
                                  " remover_a, "
                                  " cfop,"
                                  " df_icms,"
                                  " df_ipi,"
                                  " df_pis,"
                                  " df_cofins,"
                                  " codigo_imposto,"
                                  " tipo_lacres,"
                                  " numero_ordem,"
                                  " pedido_frete,"
                                  " tipo_frete,"
                                  " complemento_tipo_frete,"
                                  " codigo_transportador,"
                                  " documentos_diversos,"
                                  " tipo_inspecao_veiculo"
                                  " FROM produto").fetchall()
            for row in rows:
                prd = Produto()
                prd.id_produto = row[0]
                prd.codigo = row[1]
                prd.nome = row[2]
                prd.deposito = row[3]
                prd.lote = row[4]
                prd.inspecao_veiculo = row[5]
                prd.inspecao_produto = row[6]
                prd.remover_a = row[7]
                prd.cfop = row[8]
                prd.df_icms = row[9]
                prd.df_ipi = row[10]
                prd.df_pis = row[11]
                prd.df_cofins = row[12]
                prd.codigo_imposto = row[13]
                prd.tipo_lacres = row[14]
                prd.numero_ordem = row[15]
                prd.pedido_frete = row[16]
                prd.tipo_frete = row[17]
                prd.complemento_tipo_frete = row[18]
                prd.codigo_transportador = row[19]
                prd.documentos_diversos = row[20]
                prd.tipo_inspecao_veiculo = row[21]
                produtos.append(prd)
        return produtos

    @staticmethod
    def inserir_produto(produto):
        sql = "INSERT INTO produto (" \
              " codigo," \
              " nome," \
              " deposito, " \
              " lote," \
              " inspecao_veiculo," \
              " inspecao_produto," \
              " remover_a, " \
              " cfop," \
              " df_icms," \
              " df_ipi," \
              " df_pis," \
              " df_cofins," \
              " codigo_imposto," \
              " tipo_lacres," \
              " numero_ordem," \
              " pedido_frete," \
              " tipo_frete," \
              " complemento_tipo_frete," \
              " codigo_transportador," \
              " documentos_diversos, " \
              " tipo_inspecao_veiculo )" \
              " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
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
                                     produto.cfop,
                                     produto.df_icms,
                                     produto.df_ipi,
                                     produto.df_pis,
                                     produto.df_cofins,
                                     produto.codigo_imposto,
                                     produto.tipo_lacres,
                                     produto.numero_ordem,
                                     produto.pedido_frete,
                                     produto.tipo_frete,
                                     produto.complemento_tipo_frete,
                                     produto.codigo_transportador,
                                     produto.documentos_diversos,
                                     produto.tipo_inspecao_veiculo))
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
              " remover_a = ?, " \
              " cfop = ?," \
              " df_icms = ?," \
              " df_ipi = ?," \
              " df_pis = ?," \
              " df_cofins = ?," \
              " codigo_imposto = ?," \
              " tipo_lacres = ?," \
              " numero_ordem = ?," \
              " pedido_frete = ?," \
              " tipo_frete = ?," \
              " complemento_tipo_frete = ?," \
              " codigo_transportador = ?," \
              " documentos_diversos = ?," \
              " tipo_inspecao_veiculo = ?" \
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
                                     produto.cfop,
                                     produto.df_icms,
                                     produto.df_ipi,
                                     produto.df_pis,
                                     produto.df_cofins,
                                     produto.codigo_imposto,
                                     produto.tipo_lacres,
                                     produto.numero_ordem,
                                     produto.pedido_frete,
                                     produto.tipo_frete,
                                     produto.complemento_tipo_frete,
                                     produto.codigo_transportador,
                                     produto.documentos_diversos,
                                     produto.tipo_inspecao_veiculo,
                                     produto.id_produto))
                connection.commit()
            except sqlite3.Error as e:
                conn.rollback()
                print(e)
                raise RuntimeError("Erro ao atualizar produto!\n".format(e))

    @staticmethod
    def pesquisar_produto_pelo_codigo(codigo_produto):
        sql = "SELECT rowid," \
              " codigo, nome," \
              " deposito, lote," \
              " inspecao_veiculo," \
              " inspecao_produto," \
              " remover_a, " \
              " cfop," \
              " df_icms," \
              " df_ipi," \
              " df_pis," \
              " df_cofins," \
              " codigo_imposto," \
              " tipo_lacres," \
              " numero_ordem," \
              " pedido_frete," \
              " tipo_frete," \
              " complemento_tipo_frete," \
              " codigo_transportador," \
              " documentos_diversos," \
              " tipo_inspecao_veiculo" \
              " FROM produto WHERE codigo = ?"

        with connection as conn:
            cursor = conn.cursor()
            row = cursor.execute(sql, (codigo_produto,)).fetchone()
            prd = Produto()
            prd.id_produto = row[0]
            prd.codigo = row[1]
            prd.nome = row[2]
            prd.deposito = row[3]
            prd.lote = row[4]
            prd.inspecao_veiculo = row[5]
            prd.inspecao_produto = row[6]
            prd.remover_a = row[7]
            prd.cfop = row[8]
            prd.df_icms = row[9]
            prd.df_ipi = row[10]
            prd.df_pis = row[11]
            prd.df_cofins = row[12]
            prd.codigo_imposto = row[13]
            prd.tipo_lacres = row[14]
            prd.numero_ordem = row[15]
            prd.pedido_frete = row[16]
            prd.tipo_frete = row[17]
            prd.complemento_tipo_frete = row[18]
            prd.codigo_transportador = row[19]
            prd.documentos_diversos = row[20]
            prd.tipo_inspecao_veiculo = row[21]
            return prd


class MotoristaService:
    @staticmethod
    def listar_motoristas():
        return Motorista.select()

    @staticmethod
    def salvar_ou_atualizar(motorista):
        try:
            motorista.save()
        except Exception as e:
            raise e

    @staticmethod
    def deletar_motoristas(motorista):
        try:
            motorista.delete_instance()
        except peewee.DoesNotExist:
            raise RuntimeError('Motorista não existe na base de dados')
        except Exception as e:
            raise e

    @staticmethod
    def pesquisar_motorista(criterio):
        return Motorista.select().where(Motorista.nome.contains(criterio)
                                        or Motorista.cpf.contains(criterio)
                                        or Motorista.cnh.contains(criterio)
                                        or Motorista.rg.contains(criterio))

    @staticmethod
    def pesquisar_motorista_pelo_id(id_motorista):
        return Motorista.get_by_id(id_motorista)


class PesoBalancaService:
    @staticmethod
    def listar_pesos_balanca():
        return PesoBalanca.select()

    @staticmethod
    def pesquisar_pesos_balanca_pela_descricao(descricao):
        return PesoBalanca.select().where(PesoBalanca.descricao == descricao)


class TipoVeiculoService:
    @staticmethod
    def listar_tipos_veiculos():
        return TipoVeiculo.select()

    @staticmethod
    def pesquisar_tipo_veiculo_pela_descricao(descricao):
        return TipoVeiculo.select().where(TipoVeiculo.descricao == descricao)


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
    def salvar_ou_atualizar(veiculo):
        try:
            veiculo.save()
        except Exception as e:
            raise e

    @staticmethod
    def deletar_veiculo(veiculo):
        try:
            veiculo.delete_instance()
        except peewee.DoesNotExist:
            raise RuntimeError('Veículo não existe na base de dados')
        except Exception as e:
            raise e

    @staticmethod
    def pesquisar_veiculo(criterio):
        return Veiculo.select().where(Veiculo.placa1.contains(criterio)
                                      or Veiculo.placa2.contains(criterio)
                                      or Veiculo.placa3.contains(criterio)
                                      or Veiculo.placa4.contains(criterio))

    @staticmethod
    def pesquisar_veiculo_pelo_id(id_veiculo):
        return Veiculo.get_by_id(id_veiculo)


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

    @staticmethod
    def pesquisar_codigo_lacre(numero_lacre):
        with connection as conn:
            cursor = conn.cursor()
            sql = "SELECT rowid," \
                  " codigo," \
                  " numero" \
                  " FROM lacre WHERE numero = ?"
        row = cursor.execute(sql, (numero_lacre,)).fetchone()
        return Lacre(id_lacre=row[0],
                     codigo=row[1],
                     numero=row[2])


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
              " FROM tipo_carregamento WHERE rowid = ?"
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


class TransportadorService:
    @staticmethod
    def listar_transportadores():
        transportadores = []
        with connection as conn:
            cursor = conn.cursor()
            rows = cursor.execute("SELECT rowid,"
                                  " codigo_sap,"
                                  " nome,"
                                  " cidade,"
                                  " uf,"
                                  " cnpj"
                                  " FROM transportador").fetchall()
            for row in rows:
                transportador = Transportador()
                transportador.codigo_sap = row[1]
                transportador.nome = row[2]
                transportador.cidade = row[3]
                transportador.uf = row[4]
                transportador.cnpj_cpf = row[5]
                transportadores.append(transportador)

        return transportadores

    @staticmethod
    def inserir_transportador(veiculo):
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
    def atualizar_transportador(veiculo):
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
    def deletar_transportador(id_veiculo):
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
    def pesquisar_transportador(criterio):
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


if __name__ == '__main__':
    for v in TipoVeiculoService.listar_tipos_veiculos():
        print(v.id)
