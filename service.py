import xml.etree.ElementTree as et
import model

FILE = "properties.xml"


def load_xml_file():
    arquivo = FILE
    tree = et.parse(arquivo)
    root = tree.getroot()

    return tree, root


items = load_xml_file()
tree_items = items[0]
xml_root = items[1]


def list_products():
    products = []
    for xml_product in xml_root.findall("product"):
        for item in xml_product.findall("item"):
            product = model.Product()
            product.cod = item.get("cod")
            product.description = item.get("description")
            product.storage = item.get("storage")
            product.batch = item.get("batch")
            products.append(product)
    return products


# pesquisa um produto pela descricao
def find_product_by_description(description):
    products = list_products()
    for p in products:
        if p.description == description:
            return p


# atualiza um produto no arquivo 'properties.xml'
def update_product(product):
    for xml_product in xml_root.findall("product"):
        for item in xml_product.findall("item"):
            if item.get("cod") == product.cod:
                item.attrib['storage'] = product.storage
                item.attrib['batch'] = product.batch
    tree_items.write(FILE)


# lista todos os motoristas
def list_drivers():
    drivers = []
    for xml_driver in xml_root.findall("driver"):
        for item in xml_driver.findall("item"):
            driver = model.Driver()
            driver.name = item.get("name")
            driver.cpf = item.get("cpf")
            driver.cnh = item.get("cnh")
            driver.rg = item.get("rg")
            drivers.append(driver)
    return drivers


# pesquisa um motorista pelo cpf, cnh ou rg
def find_driver(value):
    drivers = list_drivers()
    for d in drivers:
        if d.cpf == value or d.cnh == value or d.rg == value:
            return d


# atualiza um produto no arquivo 'properties.xml'
def update_driver(driver):
    print('modificando motorista ' + driver.name)
    for xml_product in xml_root.findall("driver"):
        for item in xml_product.findall("item"):
            if item.get("cpf") == driver.cpf or item.get("cnh") == driver.cnh or item.get("rg") == driver.rg:
                item.attrib['name'] = driver.name
                item.attrib['cpf'] = driver.cpf
                item.attrib['cnh'] = driver.cnh
                item.attrib['rg'] = driver.rg
                break
    tree_items.write(FILE)


# atualiza um produto no arquivo 'properties.xml'
def create_driver(driver):
    myattributes = {"name": driver.name, "cpf": driver.cpf, "cnh": driver.cnh, "rg": driver.rg}
    d = xml_root.find('driver')
    item = et.SubElement(d, 'item', myattributes)
    item.attrib = myattributes
    tree_items.write(FILE)


# lista todos os motoristas
def list_trucks():
    trucks = []
    for xml_driver in xml_root.findall("truck"):
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
    return trucks


# pesquisa todos os conjuntos de carretas de contem uma determinada placa
def find_trucks(board):
    all_trucks = list_trucks()
    trucks = []
    for t in all_trucks:
        if t.board_1 == board or t.board_2 == board or t.board_3 == board or t.board_4 == board:
            trucks.append(t)
    return trucks
