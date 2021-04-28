import tkinter
from tkinter.ttk import *
from tkinter import filedialog, scrolledtext, END, OUTSIDE, Listbox, W, E
import re
import win32com.client
from win32api import MessageBox
import model
import constants as ct
import service

# lista com todos os produtos salvos no arquivo 'properties.xml'
from qa01 import QA01
from sapgui import SAPGuiApplication
from vl_01 import VL01

products = service.list_products()


def get_tag_value(item, tag):
    return item.findall(tag)[0].text


def split_shipping(shipping, index):
    return shipping.split('=')[index]


class AppView:

    def __init__(self):

        self.app_main = tkinter.Tk()
        self.app_main.title("Utilitário de Faturamento")
        self.app_main.geometry('600x700')

        self.remessas = []
        self.product_name = tkinter.StringVar()
        self.batch = tkinter.StringVar()
        self.amount = tkinter.StringVar()
        self.storage = tkinter.StringVar()
        self.ov = tkinter.StringVar()
        self.total_txt = tkinter.StringVar()
        self.msg = tkinter.StringVar()
        self.product = None

        self.driver_name = tkinter.StringVar()
        self.cpf = tkinter.StringVar()
        self.cnh = tkinter.StringVar()
        self.rg = tkinter.StringVar()
        self.search = tkinter.StringVar()
        self.current_driver = None

        self.lacres = []
        self.truck_search = tkinter.StringVar()
        self.truck_type = tkinter.StringVar()
        self.truck_number_seals = tkinter.StringVar()
        self.truck_axle = tkinter.StringVar()
        self.truck_board_1 = tkinter.StringVar()
        self.truck_board_2 = tkinter.StringVar()
        self.truck_board_3 = tkinter.StringVar()
        self.truck_board_4 = tkinter.StringVar()
        self.truck_cod_board_1 = tkinter.StringVar()
        self.truck_cod_board_2 = tkinter.StringVar()
        self.truck_cod_board_3 = tkinter.StringVar()
        self.truck_cod_board_4 = tkinter.StringVar()
        self.truck_list = []
        self.current_truck = None

        menubar = tkinter.Menu(self.app_main)

        filemenu = tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Abrir planilha de configuração")
        filemenu.add_command(label="Sair", command=self.app_main.quit)

        menubar.add_cascade(label="Arquivo", menu=filemenu)

        self.app_main.config(menu=menubar)

        # dados de remssa
        self.shipping_frame = LabelFrame(self.app_main, text="Remessa")
        self.shipping_frame.grid(column=0, row=0)

        self.frame_motorista = None
        self.criar_frame_motorista()

        self.truck_frame = LabelFrame(self.app_main, text="Veículo")
        self.truck_frame.grid(column=0, row=2)

        # self.shipping_frame.place(bordermode=OUTSIDE, x=10, y=10, height=170, width=430)

        self.scr = scrolledtext.ScrolledText(self.shipping_frame, undo=True, height=2, width=15)
        self.cbo_product = Combobox(self.shipping_frame, textvariable=self.product_name, state="readonly")
        self.position_shipping_fields()

        self.txt_search = None
        self.txt_name = Entry(self.frame_motorista, textvariable=self.driver_name)
        self.txt_rg = Entry(self.frame_motorista, textvariable=self.rg)
        self.txt_cnh = Entry(self.frame_motorista, textvariable=self.cnh)
        self.txt_cpf = Entry(self.frame_motorista, textvariable=self.cpf)
        self.position_driver_fields()

        # dados do motorista

        # self.truck_frame.place(bordermode=OUTSIDE, x=10, y=370, height=400, width=430)

        self.txt_truck_search = Entry(self.truck_frame, textvariable=self.truck_search)
        self.lb_trucks = Listbox(self.truck_frame, font=('Consolas', 8))
        self.scr_seals = scrolledtext.ScrolledText(self.truck_frame, undo=True, height=2, width=15)
        self.position_truck_fields()

        # rodapé
        Button(self.app_main, text='Criar', command=self.create).place(x=10, y=820)
        self.lbl_msg = Label(self.app_main, textvariable=self.msg, font=(None, 10, 'bold'))
        self.lbl_msg.place(x=10, y=850)

        # exibindo em looping
        tkinter.mainloop()

    def position_shipping_fields(self):
        # frame da remessa

        # produto
        Label(self.shipping_frame, text="Produto: ", font=(None, 8, 'normal')).place(x=10, y=5, width=150)
        self.cbo_product['values'] = tuple(prod.description for prod in products)
        self.cbo_product.bind('<<ComboboxSelected>>', self.product_change)
        self.cbo_product.place(x=10, y=25, width=150)

        # deposito
        Label(self.shipping_frame, text="Deposito: ", font=(None, 8, 'normal')).place(x=170, y=5, width=80)
        Entry(self.shipping_frame, textvariable=self.storage).place(x=170, y=25, width=80)
        # lote
        Label(self.shipping_frame, text="Lote: ", font=(None, 8, 'normal')).place(x=260, y=5, width=120)
        Entry(self.shipping_frame, textvariable=self.batch).place(x=260, y=25, width=120)

        Label(self.shipping_frame, text="Ordem/Quantidade: ", font=(None, 8, 'normal')).place(x=10, y=60, width=150)
        self.scr.bind('<KeyRelease>', self.print)
        self.scr.place(x=10, y=80, width=150)

        Label(self.shipping_frame, text="Total: ", font=(None, 12, 'bold')).place(x=170, y=110, width=50)
        Label(self.shipping_frame, textvariable=self.total_txt, font=(None, 12, 'bold')).place(x=230, y=110, width=80)
        self.total_txt.set("0,000")

    def criar_frame_motorista(self):
        self.frame_motorista = LabelFrame(self.app_main, text="Motorista")
        self.frame_motorista.grid(sticky=W, column=0, row=0, ipadx=2, padx=5)
        # self.frame_motorista.columnconfigure(1, weight=1)
        # dados de remssa
        Label(self.frame_motorista, text="Pesquisar").grid(sticky=W, column=0, row=0, padx=2)
        self.txt_search = Entry(self.frame_motorista, textvariable=self.search, width=40)
        self.txt_search.grid(sticky="we", column=0, row=1, padx=2, columnspan=4, ipady=1, pady=(0, 5))
        self.txt_search.bind('<Return>', self.find_driver)

        Button(self.frame_motorista, text='Pesquisar', command=lambda: self.find_driver('')) \
            .grid(sticky="we", column=0, row=2, padx=2)

        Button(self.frame_motorista, text='Editar', command=self.clear_driver) \
            .grid(sticky="we", column=1, row=2, padx=2)

        Label(self.frame_motorista, text="Nome: ", font=(None, 8, 'bold')).grid(sticky=W, column=0, row=3, padx=5)
        Label(self.frame_motorista, textvariable=self.driver_name, font=(None, 8, 'bold')).grid(sticky=W, column=1,
                                                                                                row=3, padx=5,
                                                                                                columnspan=3)
        Label(self.frame_motorista, text="CPF: ", font=(None, 8, 'bold')).grid(sticky=W, column=0, row=4, padx=5)
        Label(self.frame_motorista, textvariable=self.cpf, font=(None, 8, 'bold')).grid(sticky=W, column=1,
                                                                                        row=4, padx=5,
                                                                                        columnspan=3)
        Label(self.frame_motorista, text="CNH: ", font=(None, 8, 'bold')).grid(sticky=W, column=0, row=5, padx=5)
        Label(self.frame_motorista, textvariable=self.cnh, font=(None, 8, 'bold')).grid(sticky=W, column=1,
                                                                                        row=5, padx=5,
                                                                                        columnspan=3)
        Label(self.frame_motorista, text="RG: ", font=(None, 8, 'bold')).grid(sticky=W, column=0, row=6, padx=5)
        Label(self.frame_motorista, textvariable=self.rg, font=(None, 8, 'bold')).grid(sticky=W, column=1,
                                                                                       row=6, padx=5,
                                                                                       columnspan=3)

    # posiciona os campos do motorista na tela
    def position_driver_fields(self):
        pass
        # Motorista
        # Campo de pesquisa
        # Label(self.frame_motorista, text="Pesquisar(CPF, CNH ou RG)", font=(None, 8, 'normal')).place(x=10, y=5, width=160)
        # self.txt_search.place(x=10, y=25, width=250, height=23)
        # self.txt_search.bind('<Return>', self.find_driver)
        # Button(self.frame_motorista, text='Pesquisar', command=lambda: self.find_driver('')).place(x=270, y=24, width=70)
        # Button(self.frame_motorista, text='Limpar', command=self.clear_driver).place(x=350, y=24, width=70)

    def position_truck_fields(self):

        # Campo de pesquisa
        Label(self.truck_frame, text="Pesquisar", font=(None, 8, 'normal')).place(x=10, y=5, width=160)
        self.txt_truck_search.place(x=10, y=25, width=250, height=23)
        self.txt_truck_search.bind('<Return>', self.find_trucks)

        Button(self.truck_frame, text='Pesquisar', command=lambda: self.find_trucks('')).place(x=270, y=24, width=70)
        Button(self.truck_frame, text='Limpar', command=self.clear_truck_search).place(x=350, y=24, width=70)

        self.lb_trucks.place(bordermode=OUTSIDE, x=10, y=70, height=60, width=413)
        self.lb_trucks.bind('<Double-Button>', self.set_truck)

        # tipo
        Label(self.truck_frame, text="Tipo: ", font=(None, 8, 'normal')).place(x=10, y=115, width=60)
        Entry(self.truck_frame, textvariable=self.truck_type).place(x=10, y=135, width=60)

        # eixo
        Label(self.truck_frame, text="Eixo: ", font=(None, 8, 'normal')).place(x=80, y=115, width=60)
        Entry(self.truck_frame, textvariable=self.truck_axle).place(x=80, y=135, width=60)

        # numero de lacres
        Label(self.truck_frame, text="Qtd. Lacres:", font=(None, 8, 'normal')).place(x=150, y=115, width=90)
        Entry(self.truck_frame, textvariable=self.truck_number_seals).place(x=150, y=135, width=90)

        # placa cavalo
        Label(self.truck_frame, text="Cavalo", font=(None, 8, 'normal')).place(x=10, y=160, width=100)
        Entry(self.truck_frame, textvariable=self.truck_board_1).place(x=10, y=180, width=100)
        Label(self.truck_frame, text="Código Município", font=(None, 8, 'normal')).place(x=120, y=160, width=120)
        Entry(self.truck_frame, textvariable=self.truck_cod_board_1).place(x=120, y=180, width=120)

        # placa carreta 01
        Label(self.truck_frame, text="Carreta 01", font=(None, 8, 'normal')).place(x=10, y=205, width=100)
        Entry(self.truck_frame, textvariable=self.truck_board_2).place(x=10, y=225, width=100)
        Label(self.truck_frame, text="Código Município", font=(None, 8, 'normal')).place(x=120, y=205, width=120)
        Entry(self.truck_frame, textvariable=self.truck_cod_board_2).place(x=120, y=225, width=120)

        # placa carreta 02
        Label(self.truck_frame, text="Carreta 02", font=(None, 8, 'normal')).place(x=10, y=250, width=100)
        Entry(self.truck_frame, textvariable=self.truck_board_3).place(x=10, y=275, width=100)
        Label(self.truck_frame, text="Código Município", font=(None, 8, 'normal')).place(x=120, y=250, width=120)
        Entry(self.truck_frame, textvariable=self.truck_cod_board_3).place(x=120, y=275, width=120)

        # placa carreta 03
        Label(self.truck_frame, text="Carreta 03", font=(None, 8, 'normal')).place(x=10, y=300, width=100)
        Entry(self.truck_frame, textvariable=self.truck_board_4).place(x=10, y=325, width=100)
        Label(self.truck_frame, text="Código Município", font=(None, 8, 'normal')).place(x=120, y=300, width=120)
        Entry(self.truck_frame, textvariable=self.truck_cod_board_4).place(x=120, y=325, width=120)

        Label(self.truck_frame, text="Lacres: ", font=(None, 8, 'normal')).place(x=260, y=115, width=120)
        self.scr_seals.bind('<KeyRelease>', self.append_seals_list)
        self.scr_seals.place(x=260, y=135, width=150, height=210)

    # método que captura o produto selecionado
    def product_change(self, event):
        self.product = service.find_product_by_description(self.product_name.get())
        self.storage.set(self.product.storage)
        self.batch.set(self.product.batch)

    # método que verifica se o texto digitado no campo ordem/quantidade está no formato correto
    def print(self, event):
        text = self.scr.get("1.0", END)

        self.create_shippings(text)

        self.show_total()

    # verifica se o texto digitado para remessa está correto e adiciona a lista de remessas
    def create_shippings(self, text):
        sp = text.splitlines()
        self.remessas.clear()
        for r in sp:
            if re.findall("^(\\d*)=([0-9]+[,]+[0-9]{3,})$", r.strip()):
                # ordem de venda
                ov = split_shipping(r, 0)
                # quantidade
                amt = split_shipping(r, 1)
                self.remessas.append(model.Shipping(ov, amt, self.product))

    # mostrar o valor somado de todas as remessas
    def show_total(self):
        tot = 0.0
        for ov in self.remessas:
            vl = float(ov.amount.replace(",", "."))
            tot += vl
        self.total_txt.set('{:,.3f}'.format(tot).replace('.', ','))

    def shipping(self):
        pass

    def check_product_update(self):
        update = False
        if self.product.storage != self.storage.get():
            self.product.storage = self.storage.get()
            update = True
        if self.product.batch != self.batch.get():
            self.product.batch = self.batch.get()
            update = True
        return update

    def assert_shipping(self):
        if self.product is None:
            MessageBox(None, "Selecione um produto!")
            return False

        elif self.storage.get() == "":
            MessageBox(None, "Informe um depósito!")
            return False

        elif self.batch.get() == "":
            MessageBox(None, "Informe um lote!")
            return False

        elif len(self.remessas) == 0:
            MessageBox(None, "Informe ao menos uma remessa!")
            return False

        return True

    def find_driver(self, event):
        value = ""
        self.current_driver = None
        if self.search.get() != "":
            value = self.search.get()

        if value == "":
            self.clear_driver()
            MessageBox(None, "Ao menos um valor para CPF, CNH ou RG deve ser informado!")
        else:
            self.current_driver = service.find_driver(value)
            if self.current_driver is not None:
                self.set_driver(self.current_driver)
            else:
                self.clear_driver()
                MessageBox(None, "Nenhum motorista encontrado. Insira manualmente!")

    def set_driver(self, driver):
        self.cpf.set(driver.cpf)
        self.cnh.set(driver.cnh)
        self.rg.set(driver.rg)
        self.driver_name.set(driver.name)

    def clear_driver(self):
        self.search.set('')
        self.cpf.set('')
        self.cnh.set('')
        self.rg.set('')
        self.driver_name.set('')

    def save_or_update_driver(self):
        # verificando se o motorista ainda nao foi cadastrado
        new_driver = False
        if self.current_driver is None:
            self.current_driver = model.Driver()
            new_driver = True

        # atualizando os dados
        self.current_driver.name = self.driver_name.get()
        self.current_driver.cpf = self.cpf.get()
        self.current_driver.cnh = self.cnh.get()
        self.current_driver.rg = self.rg.get()

        if new_driver:
            service.create_driver(self.current_driver)
        else:
            service.update_driver(self.current_driver)

        # redefinindo o motorista para None
        self.current_driver = None
        self.clear_driver()

    def create_new_driver(self):
        if (re.findall("^\\d{11}$", self.cpf.get()) or re.findall("^\\d{9}$", self.cnh.get()) or self.rg.get() != "") \
                and self.driver_name.get() != "":
            self.current_driver = model.Driver
            self.current_driver.name = self.driver_name.get()
            self.current_driver.cpf = self.cpf.get()
            self.current_driver.cnh = self.cnh.get()
            self.current_driver.rg = self.rg.get()
            service.create_driver(self.current_driver)
            return True
        MessageBox(None, "Pelo menos um número de documento e o nome do motorista devem ser informados!")
        return False

    def find_trucks(self, event):
        board = self.truck_search.get()
        if board == "":
            MessageBox(None, "Informe uma placa para pesquisa!")

        elif not re.findall("^[a-zA-Z]{3}[0-9][A-Za-z0-9][0-9]{2}$", board):
            MessageBox(None, "A placa formato incorreto!")

        else:
            self.clear_truck()
            trucks = service.find_trucks(board)
            if len(trucks) > 0:
                self.truck_list.clear()

                for truck in trucks:
                    self.truck_list.append(truck)
                    self.lb_trucks.insert(END, truck)

            else:
                self.current_truck = model.Truck()
                MessageBox(None, "Nenhum conjunto com essa placa foi encontrado. Informe manualmente!")

    def set_truck(self, event):
        index = self.lb_trucks.curselection()[0]
        self.current_truck = self.truck_list[index]

        self.truck_type.set(self.current_truck.type)
        self.truck_axle.set(self.current_truck.axle)
        self.truck_number_seals.set(self.current_truck.number_seals)
        self.truck_board_1.set(self.current_truck.board_1)
        self.truck_board_2.set(self.current_truck.board_2)
        self.truck_board_3.set(self.current_truck.board_3)
        self.truck_board_4.set(self.current_truck.board_4)
        self.truck_cod_board_1.set(self.current_truck.board_code_1)
        self.truck_cod_board_2.set(self.current_truck.board_code_2)
        self.truck_cod_board_3.set(self.current_truck.board_code_3)
        self.truck_cod_board_4.set(self.current_truck.board_code_4)

    def clear_truck_search(self):
        self.truck_search.set('')
        self.clear_truck()

    def clear_truck(self):
        self.current_truck = None
        self.lb_trucks.delete(0, END)
        self.truck_type.set('')
        self.truck_axle.set('')
        self.truck_number_seals.set('')
        self.truck_board_1.set('')
        self.truck_board_2.set('')
        self.truck_board_3.set('')
        self.truck_board_4.set('')
        self.truck_cod_board_1.set('')
        self.truck_cod_board_2.set('')
        self.truck_cod_board_3.set('')
        self.truck_cod_board_4.set('')
        self.scr_seals.delete('1.0', END)

    # preenche a lista de lacres
    def append_seals_list(self, event):
        text = self.scr_seals.get("1.0", END)
        sp = text.splitlines()
        self.lacres.clear()
        for seal in sp:
            if re.findall("^\\d{7}$", seal.strip()):
                self.lacres.append(seal)

        print(self.lacres)

    def execute_vl01(self, session):
        shippings_number = []
        for shipping in self.remessas:
            result = VL01.create(session, shipping)
            if result[0]:
                shippings_number.append(result[1])
            else:
                # caso erro, retorna a mensagem de erro.
                return result
        # caso sucesso, retorna uma lista com os numeros das remessas criadas
        print(shippings_number)
        return True, shippings_number

    # criando lotes de controle de qualidade
    def criar_lotes_qualidade(self, session, shippings_number):
        batchs = []
        if len(batchs) == 1:
            return QA01.create(session, self.product, shippings_number[0])
        else:
            for shipping in shippings_number:
                result = QA01.create(session, self.product, shipping)
                # se cair nesse laço, significa que o lote foi criado com sucesso
                if result[0]:
                    batchs.append(result[1])

                else:
                    # caso erro, retorna a mensagem de erro.
                    return result

            # lote de controle com a primeira remessa. Será usado no transporte.
            last_batch = QA01.create(session, self.product, shippings_number[0])
            batchs.append(last_batch[1])
            print(batchs)
            return True, batchs

    def create(self):
        session = SAPGuiApplication.connect()
        if self.assert_shipping():
            result = self.execute_vl01(session)
            # se houver erro, uma mensagem será exibida com o erro.
            if not result[0]:
                MessageBox(None, result[1])

            # se nao houver erro, continua a execucao
            else:
                lotes_qualidade = self.criar_lotes_qualidade(session, result[1])

                if lotes_qualidade[0]:
                    transporte = model.Transporte()
                    transporte.documento = ""
                    transporte.motorista = self.current_driver
                    transporte.conjunto = self.current_truck
                    transporte.lacres = self.lacres
                    transporte.remessas = self.remessas
                    pass
        '''
                    if self.current_driver is None:
                # criando novo motorista
                if self.create_new_driver():
                    pass
                    
                        elif self.current_truck is None:
            MessageBox(None, "Informe um veículo!")
            return False
            '''


main = AppView()
