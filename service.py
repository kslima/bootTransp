import xml.etree.ElementTree as Et
from model import Motorista, Produto

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
            motorista = Motorista()
            motorista.nome = item.get("nome")
            motorista.cpf = item.get("cpf")
            motorista.cnh = item.get("cnh")
            motorista.rg = item.get("rg")
            motoristas.append(motorista)
    xml[0].close()
    return motoristas


# pesquisa um motorista pelo cpf, cnh ou rg
def procurar_motorista_por_documento(*args):
    motoristas = listar_motoristas()
    for motorista in motoristas:
        for documento in args:
            if motorista.cpf == documento or motorista.cnh == documento or motorista.rg == documento:
                return motorista


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


def list_trucks():
    xml = load_xml_file()
    root = xml[2]
    trucks = []
    for xml_driver in root.findall("truck"):
        for item in xml_driver.findall("item"):
            truck = model.Truck()
            truck.type = item.get("type")
            truck.axle = item.get("axle")
            truck.number_seals = item.get("number_seals")
            truck.board_1 = item.get("board_1")
            truck.board_2 = item.get("board_2")
            truck.board_3 = item.get("board_3")
            truck.board_4 = item.get("board_4")
            truck.board_code_1 = item.get("board_code_1")
            truck.board_code_2 = item.get("board_code_2")
            truck.board_code_3 = item.get("board_code_3")
            truck.board_code_4 = item.get("board_code_4")
            trucks.append(truck)
    xml[0].close()
    return trucks


# pesquisa todos os conjuntos de carretas de contem uma determinada placa
def find_trucks(board):
    all_trucks = list_trucks()
    trucks = []
    for t in all_trucks:
        if t.board_1 == board or t.board_2 == board or t.board_3 == board or t.board_4 == board:
            trucks.append(t)
    return trucks
