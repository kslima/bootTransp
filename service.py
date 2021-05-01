import xml.etree.ElementTree as et
import model

FILE_PATH = "properties.xml"


def load_xml_file():
    source = open(FILE_PATH)
    tree = et.parse(source)
    root = tree.getroot()
    return source, tree, root


def listar_produtos():
    xml = load_xml_file()
    root = xml[2]
    produtos = []
    for produto_tag in root.findall("produto"):
        for item in produto_tag.findall("item"):
            produto = model.Produto()
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
            item = et.SubElement(produto_tag, 'item', atributos_novo_produto)
            item.attrib = atributos_novo_produto
            xml[1].write(FILE_PATH)
            return 1, "Produto cadastrado com sucesso!"
        except Exception as e:
            print(e)
            return 0, "Erro ao cadastrar novo produto!\n{}".format(str(e))
        finally:
            xml[0].close()
    else:
        return -1, "Código já cadastrado! \n Atualizar cadastro ?"


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
def list_drivers():
    xml = load_xml_file()
    root = xml[2]
    drivers = []
    for xml_driver in root.findall("driver"):
        for item in xml_driver.findall("item"):
            driver = model.Driver()
            driver.name = item.get("name")
            driver.cpf = item.get("cpf")
            driver.cnh = item.get("cnh")
            driver.rg = item.get("rg")
            drivers.append(driver)
    xml[0].close()
    return drivers


# pesquisa um motorista pelo cpf, cnh ou rg
def find_driver(value):
    drivers = list_drivers()
    for d in drivers:
        if d.cpf == value or d.cnh == value or d.rg == value:
            return d


# cria um novo motorista
def create_driver(driver):
    xml = load_xml_file()
    root = xml[2]
    try:
        myattributes = {"name": driver.name, "cpf": driver.cpf, "cnh": driver.cnh, "rg": driver.rg}
        d = root.find('driver')
        item = et.SubElement(d, 'item', myattributes)
        item.attrib = myattributes
        xml[1].write(FILE_PATH)

    except Exception:
        raise
    finally:
        xml[0].close()


# atualiza um produto no arquivo 'properties.xml'
def update_driver(driver):
    xml = load_xml_file()
    root = xml[2]
    print('modificando motorista ' + driver.name)
    for xml_product in root.findall("driver"):
        for item in xml_product.findall("item"):
            if item.get("cpf") == driver.cpf or item.get("cnh") == driver.cnh or item.get("rg") == driver.rg:
                item.attrib['name'] = driver.name
                item.attrib['cpf'] = driver.cpf
                item.attrib['cnh'] = driver.cnh
                item.attrib['rg'] = driver.rg
                break
    xml[1].write(FILE_PATH)
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
