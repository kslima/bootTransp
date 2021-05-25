import xml.etree.ElementTree as Et
import peewee
from model import Municipio, Veiculo, Motorista, PesoBalanca, TipoVeiculo, SetorAtividade, CanalDistribuicao, \
    TipoInspecaoVeiculo, Produto, Transportador, Lacre, TipoCarregamento
import sqlite3

from utilitarios import StringUtils

#connection = sqlite3.connect("C:\\Users\\kslima\\Desktop\\sqlite\\banco.db")

connection = sqlite3.connect("F:\\Campo Florido\\Compartilhados\\Faturamento\\B - DOCUMENTOS DO FATURAMENTO\\db-utilitario-faturmento-nao-apagar\\banco.db")
# connection = None

FILE_PATH = "properties.xml"


def load_xml_file():
    source = open(FILE_PATH)
    tree = Et.parse(source)
    root = tree.getroot()
    return source, tree, root


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

    @staticmethod
    def pesquisar_produto_pelo_id(id_produto):
        return Produto.get_by_id(id_produto)


class MotoristaService:
    @staticmethod
    def listar_motoristas():
        return Motorista.select()

    @staticmethod
    def salvar_ou_atualizar(motorista):
        motoristas = MotoristaService.listar_motoristas()
        for mot in motoristas:
            if(StringUtils.is_equal(mot.cnh, motorista.cnh) or
               StringUtils.is_equal(mot.cpf, motorista.cpf) or
               StringUtils.is_equal(mot.rg, motorista.rg)) and mot.id != motorista.id:
                raise RuntimeError("Motorista já cadastrado!")

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
            return Motorista.select().where(
                (Motorista.nome.contains(criterio)) |
                (Motorista.cpf.contains(criterio)) |
                (Motorista.cnh.contains(criterio)) |
                (Motorista.rg.contains(criterio)))
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
            return PesoBalanca.get(PesoBalanca.descricao == descricao)
        except peewee.DoesNotExist:
            return None

    @staticmethod
    def pesquisar_pesos_balanca_pelo_codigo(codigo):
        try:
            return PesoBalanca.get(PesoBalanca.codigo == codigo)
        except peewee.DoesNotExist:
            return None


class SetorAtividadeService:
    @staticmethod
    def listar_setores_atividade():
        return SetorAtividade.select()

    @staticmethod
    def pesquisar_setor_atividade_pela_descricao(descricao):
        try:
            return SetorAtividade.get(SetorAtividade.descricao == descricao)
        except peewee.DoesNotExist:
            return None

    @staticmethod
    def pesquisar_setor_atividade_pelo_codigo(codigo):
        try:
            return SetorAtividade.get(SetorAtividade.codigo == codigo)
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
            return TipoVeiculo.get(TipoVeiculo.descricao == descricao)
        except peewee.DoesNotExist:
            return None

    @staticmethod
    def pesquisar_tipo_veiculo_pelo_codigo(codigo):
        try:
            return TipoVeiculo.get(TipoVeiculo.codigo == codigo)
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
        return Lacre.select()

    @staticmethod
    def salvar_ou_atualizar(lacres):
        try:
            for lacre in lacres:
                lacre.save()
        except Exception as e:
            raise e

    @staticmethod
    def deletar(lacres):
        try:
            for lacre in lacres:
                lacre.delete_instance()
        except peewee.DoesNotExist:
            raise RuntimeError('Lacres não existem na base de dados')
        except Exception as e:
            raise e

    @staticmethod
    def pesquisar_pacote_lacres_pelo_codigo(codigo):
        return Lacre.select().where(Lacre.codigo == codigo)

    @staticmethod
    def pesquisar_codigo_lacre(numero_lacre):
        return Lacre.get(Lacre.numero == numero_lacre)


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


def converter_para_inteiro(numero):
    try:
        return int(numero)
    except Exception:
        return 0


if __name__ == '__main__':


    '''
*********************************** - ******************
ADICIONAR MOTORISTAS   
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
            motorista = Motorista()
            motorista.nome = row[1]
            motorista.cpf = row[2]
            motorista.cnh = row[3]
            motorista.rg = row[4]
            motorista.save()
            
************************ - ****************************
        ADICIONAR VEICULOS
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
            cod_tipo_veiculo = row[1].strip()
            tipo_veiculo = TipoVeiculoService.pesquisar_tipo_veiculo_pelo_codigo(cod_tipo_veiculo)
            cod_peso_balanca = row[2]
            peso_balanca = PesoBalancaService.pesquisar_pesos_balanca_pelo_codigo(cod_peso_balanca)
            qtd_lacres = converter_para_inteiro(row[3])
            p1 = row[4]
            p2 = row[5]
            p3 = row[6]
            p4 = row[7]

            veiculo = Veiculo()
            veiculo.tipo_veiculo = tipo_veiculo
            veiculo.peso_balanca = peso_balanca
            veiculo.quantidade_lacres = qtd_lacres
            veiculo.placa1 = p1
            mp1 = MunicipioService.pesquisar_municipio_pelo_codigo(row[8].split(' ')[1].strip())
            veiculo.municipio_placa1 = mp1
            if p2:
                veiculo.placa2 = p2
                mp2 = MunicipioService.pesquisar_municipio_pelo_codigo(row[9].split(' ')[1].strip())
                print('p2: {}'.format(p2))
                veiculo.municipio_placa2 = mp2
            if p3:
                veiculo.placa3 = p3
                mp3 = MunicipioService.pesquisar_municipio_pelo_codigo(row[10].split(' ')[1].strip())
                print('p3: {}'.format(p3))
                veiculo.municipio_placa3 = mp3
            if p4:
                veiculo.placa4 = p4
                mp4 = MunicipioService.pesquisar_municipio_pelo_codigo(row[11].split(' ')[1].strip())
                print('p4: {}'.format(p4))
                veiculo.municipio_placa4 = mp4

            veiculo.save()
            
***************************************** --- **********************
LACRES
    with connection as conn:
        cursor = conn.cursor()
        rows = cursor.execute("SELECT rowid,"
                              " codigo,"
                              " numero"
                              " FROM lacre").fetchall()
        for row in rows:
            lacre = Lacre()
            lacre.codigo = row[1]
            lacre.numero = row[2]
            lacre.save()            
            
            '''


