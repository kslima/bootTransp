class Shipping:

    def __init__(self, order_number, amount, product):
        self.order = order_number
        self.product = product
        self.amount = amount


class Product:

    def __init__(self):
        self.cod = None
        self.description = None
        self.storage = None
        self.batch = None


class Driver:

    def __init__(self):
        self.name = None
        self.cpf = None
        self.cnh = None
        self.rg = None


class Truck:

    def __init__(self):
        self.type = None
        self.axle = None
        self.number_seals = None
        self.board_1 = None
        self.board_2 = None
        self.board_3 = None
        self.board_4 = None
        self.board_code_1 = None
        self.board_code_2 = None
        self.board_code_3 = None
        self.board_code_4 = None

    def __str__(self):
        return "Placas: {}/{}/{}/{} Tipo:{} Eixos:{} Lacres:{}".format(self.board_1, self.board_2, self.board_3,
                                                                       self.board_4, self.type, self.axle,
                                                                       self.number_seals)


class Transporte:

    def __init__(self):
        self.documento = None
        self.motorista = None
        self.conjunto = None
        self.lacres = []
        self.remessas = []
