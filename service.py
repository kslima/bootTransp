import xml.etree.ElementTree as Et
import peewee
from peewee import JOIN

import model
import model2
from model2 import Municipio, Veiculo, Motorista, PesoBalanca, TipoVeiculo, SetorAtividade, CanalDistribuicao, \
    TipoInspecaoVeiculo, Produto, Transportador
from model import Lacre, TipoCarregamento
import sqlite3

connection = sqlite3.connect("C:\\Users\\kslima\\Desktop\\sqlite\\banco.db")

# connection = sqlite3.connect("C:\\Users\\kleud\\Desktop\\sqlite\\banco.db")
# connection = None

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
        try:
            return Municipio.select().where(Municipio.codigo == codigo)
        except peewee.DoesNotExist:
            return None


class ProdutoService:
    @staticmethod
    def listar_produtos():
        return Produto.select()

    @staticmethod
    def salvar_ou_atualizar(produto):
        try:
            produto.save()
        except Exception as e:
            raise e

    @staticmethod
    def deletar_produto(produto):
        try:
            produto.delete_instance()
        except peewee.DoesNotExist:
            raise RuntimeError('Produto não existe na base de dados')
        except Exception as e:
            raise e

    @staticmethod
    def pesquisar_produto_pelo_codigo(codigo_produto):
        try:
            return Produto.select().where(Produto.codigo_sap == codigo_produto).get()
        except peewee.DoesNotExist:
            return None


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
        try:
            return Motorista.select().where(Motorista.nome.contains(criterio)
                                            or Motorista.cpf.contains(criterio)
                                            or Motorista.cnh.contains(criterio)
                                            or Motorista.rg.contains(criterio))
        except peewee.DoesNotExist:
            return None

    @staticmethod
    def pesquisar_motorista_pelo_id(id_motorista):
        return Motorista.get_by_id(id_motorista)


class PesoBalancaService:
    @staticmethod
    def listar_pesos_balanca():
        return PesoBalanca.select()

    @staticmethod
    def pesquisar_pesos_balanca_pela_descricao(descricao):
        try:
            return PesoBalanca.select().where(PesoBalanca.descricao == descricao)
        except peewee.DoesNotExist:
            return None


class SetorAtividadeService:
    @staticmethod
    def listar_setores_atividade():
        return SetorAtividade.select()

    @staticmethod
    def pesquisar_setor_atividade_pela_descricao(descricao):
        try:
            return SetorAtividade.select().where(SetorAtividade.descricao == descricao)
        except peewee.DoesNotExist:
            return None

    @staticmethod
    def pesquisar_setor_atividade_pelo_codigo(codigo):
        try:
            return SetorAtividade.select().where(SetorAtividade.codigo == codigo)
        except peewee.DoesNotExist:
            return None


class CanalDistribuicaoService:
    @staticmethod
    def listar_canais_distribuicao():
        return CanalDistribuicao.select()

    @staticmethod
    def pesquisar_canail_distribuicao_pela_descricao(descricao):
        try:
            return CanalDistribuicao.get(CanalDistribuicao.descricao == descricao)
        except peewee.DoesNotExist:
            return None

    @staticmethod
    def pesquisar_canail_distribuicao_pelo_codigo(codigo):
        try:
            return CanalDistribuicao.get(CanalDistribuicao.codigo == codigo)
        except peewee.DoesNotExist:
            return None


class TipoInspecaoVeiculoService:
    @staticmethod
    def listar_tipos_inspecao_veiculo():
        return TipoInspecaoVeiculo.select()

    @staticmethod
    def pesquisar_tipo_inspecao_veiculo_pela_descricao(descricao):
        try:
            return TipoInspecaoVeiculo.get(TipoInspecaoVeiculo.descricao == descricao)
        except peewee.DoesNotExist:
            return None

    @staticmethod
    def pesquisar_tipo_inspecao_veiculo_pelo_codigo(codigo):
        try:
            return TipoInspecaoVeiculo.get(TipoInspecaoVeiculo.codigo == codigo)
        except peewee.DoesNotExist:
            return None


class TipoVeiculoService:
    @staticmethod
    def listar_tipos_veiculos():
        return TipoVeiculo.select()

    @staticmethod
    def pesquisar_tipo_veiculo_pela_descricao(descricao):
        try:
            return TipoVeiculo.select().where(TipoVeiculo.descricao == descricao)
        except peewee.DoesNotExist:
            return None


class VeiculoService:
    @staticmethod
    def listar_veiculos():
        return Veiculo.select()

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
        try:
            return Veiculo.select().where(Veiculo.placa1.contains(criterio)
                                          or Veiculo.placa2.contains(criterio)
                                          or Veiculo.placa3.contains(criterio)
                                          or Veiculo.placa4.contains(criterio))
        except peewee.DoesNotExist:
            return None

    @staticmethod
    def pesquisar_veiculo_pelo_id(id_veiculo):
        return Veiculo.get_by_id(id_veiculo)


class TransportadorService:
    @staticmethod
    def listar_transportadores():
        return Transportador.select()

    @staticmethod
    def salvar_ou_atualizar(transportador):
        try:
            transportador.save()
        except Exception as e:
            raise e

    @staticmethod
    def deletar_veiculo(transportador):
        try:
            transportador.delete_instance()
        except peewee.DoesNotExist:
            raise RuntimeError('Transportador não existe na base de dados')
        except Exception as e:
            raise e

    @staticmethod
    def pesquisar_transportador(criterio):
        try:
            return Transportador.select().where(
                (Transportador.codigo_sap == criterio) |
                (Transportador.cnpj_cpf == criterio)).get()
        except peewee.DoesNotExist:
            return None

    @staticmethod
    def pesquisar_transportador_pelo_id(id_transportador):
        return Transportador.get_by_id(id_transportador)


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


if __name__ == '__main__':
    '''
    municipios = []
    with connection as conn:
        cursor = conn.cursor()
        rows = cursor.execute("SELECT rowid, nome, codigo_municipio, uf FROM municipio").fetchall()
        for row in rows:
            municipios.append(model.Municipio(id_municipio=row[0],
                                              nome_municipio=row[1],
                                              codigo_municipio=row[2],
                                              uf=row[3]))

    for m in municipios:
        m2 = model2.Municipio()
        m2.codigo = m.codigo_municipio
        m2.nome = m.nome_municipio
        m2.uf = m.uf
        m2.save()
        '''
