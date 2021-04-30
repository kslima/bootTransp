import tkinter
from tkinter.ttk import *
from tkinter import filedialog, scrolledtext, END, OUTSIDE, Listbox, W, E, DISABLED, INSERT
import re
from win32api import MessageBox
import model
import service
import time

# lista com todos os produtos salvos no arquivo 'properties.xml'
from qa01 import QA01
from sapgui import SAPGuiApplication
from vl01 import VL01
from vt01 import VT01

products = service.list_products()


def get_tag_value(item, tag):
    return item.findall(tag)[0].text


def split_shipping(shipping, index):
    return shipping.split('=')[index]


class AppView:

    def __init__(self):

        self.app_main = tkinter.Tk()
        self.app_main.title("Utilitário de Faturamento")
        self.app_main.geometry('675x620')

        self.produto_selecionado = None
        self.remessas = []
        self.deposito = tkinter.StringVar()
        self.product_name = tkinter.StringVar()
        self.lote = tkinter.StringVar()
        self.amount = tkinter.StringVar()

        self.ov = tkinter.StringVar()
        self.label_total_remessas = tkinter.StringVar()
        self.msg = tkinter.StringVar()

        self.driver_name = tkinter.StringVar()
        self.cpf = tkinter.StringVar()
        self.cnh = tkinter.StringVar()
        self.rg = tkinter.StringVar()
        self.search = tkinter.StringVar()
        self.current_driver = None

        self.lacres = []
        self.pesquisa_veiculo = tkinter.StringVar()
        self.truck_list = []
        self.current_truck = None

        menubar = tkinter.Menu(self.app_main)

        filemenu = tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Abrir planilha de configuração")
        filemenu.add_command(label="Sair", command=self.app_main.quit)

        menubar.add_cascade(label="Arquivo", menu=filemenu)

        self.app_main.config(menu=menubar)

        # dados de remssa
        self.frame_remessa = None
        self.scroll_ordem_quantidade = None
        self.cbo_produtos = None
        self.criar_frame_remessas()

        # dados motorista
        self.frame_motorista = None
        self.txt_pesquisa_motorista = None
        self.criar_frame_motorista()

        # dados da trnsportadora
        self.texto_pesquisa_transportador = tkinter.StringVar()
        self.dados_transportador_selecionado = tkinter.StringVar()
        self.frame_transportador = None
        self.campo_pesquisa_transportador = None
        self.criar_frame_transportador()

        # dados do veiculo
        self.frame_veiculo = None
        self.campo_pesquisa_veiculo = None
        self.lista_veiculos_encontrados = None
        self.campo_lacres = None
        self.criar_frame_veiculo()

        # dados saída
        self.frame_saida = None
        self.campo_saida = None
        self.criar_frame_saida()

        # exibindo em looping
        tkinter.mainloop()

    def criar_frame_remessas(self):
        self.frame_remessa = LabelFrame(self.app_main, text="Remessa")
        self.frame_remessa.place(x=10, y=10, width=320, height=160)

        Label(self.frame_remessa, text="Produto: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=0, padx=2)
        self.cbo_produtos = Combobox(self.frame_remessa, textvariable=self.product_name, state="readonly")
        self.cbo_produtos['values'] = tuple(prod.description for prod in products)
        self.cbo_produtos.bind('<<ComboboxSelected>>', self.mudar_produto)
        self.cbo_produtos.grid(sticky="we", column=0, row=1, padx=2, ipady=1, pady=(0, 5), columnspan=2)

        Button(self.frame_remessa, text='Editar', command=self.clear_driver) \
            .grid(sticky=W, column=2, row=1, padx=2, pady=(0, 5))

        Label(self.frame_remessa, text="Ordem/Quantidade").grid(sticky=W, column=0, row=4, padx=2, ipady=2)
        self.scroll_ordem_quantidade = scrolledtext.ScrolledText(self.frame_remessa, undo=True, height=2, width=15)
        self.scroll_ordem_quantidade.grid(sticky=W, column=0, row=5, padx=5, rowspan=3)
        self.scroll_ordem_quantidade.bind('<KeyRelease>', self.mostrar_total_remessas)

        self.deposito.set("Deposito..: -")
        Label(self.frame_remessa, textvariable=self.deposito, font=(None, 9, 'bold'), width=20).grid(sticky=W, column=1,
                                                                                                     row=5, padx=5,
                                                                                                     columnspan=2)
        self.lote.set("Lote..........: -")
        Label(self.frame_remessa, textvariable=self.lote, font=(None, 9, 'bold')).grid(sticky=W, column=1,
                                                                                       row=6, padx=5, columnspan=2)

        Label(self.frame_remessa, textvariable=self.label_total_remessas, font=(None, 9, 'bold')).grid(sticky=W,
                                                                                                       column=1, row=7,
                                                                                                       padx=5,
                                                                                                       columnspan=2)
        self.label_total_remessas.set("Total.........: 0,000")

    def criar_frame_motorista(self):
        self.frame_motorista = LabelFrame(self.app_main, text="Motorista")
        self.frame_motorista.place(x=340, y=10, width=320, height=160)

        Label(self.frame_motorista, text="Pesquisar").grid(sticky=W, column=0, row=0, padx=2)
        self.txt_pesquisa_motorista = Entry(self.frame_motorista, textvariable=self.search)
        self.txt_pesquisa_motorista.grid(sticky="we", column=0, row=1, padx=2, ipady=1, pady=(0, 5))
        self.txt_pesquisa_motorista.bind('<Return>', self.pesquisar_motorista)

        Button(self.frame_motorista, text='Pesquisar', command=lambda: self.pesquisar_motorista('')) \
            .grid(sticky="we", column=1, row=1, padx=2, pady=(0, 5))

        Button(self.frame_motorista, text='Editar', command=self.clear_driver) \
            .grid(sticky="we", column=2, row=1, padx=2, pady=(0, 5))

        self.driver_name.set("Nome..: ")
        Label(self.frame_motorista, textvariable=self.driver_name, font=(None, 8, 'bold')).grid(sticky=W, column=0,
                                                                                                row=3, padx=5,
                                                                                                pady=(10, 0),
                                                                                                columnspan=3)
        self.cpf.set("CPF......: ")
        Label(self.frame_motorista, textvariable=self.cpf, font=(None, 8, 'bold')).grid(sticky=W, column=0,
                                                                                        row=4, padx=5,
                                                                                        columnspan=3)
        self.cnh.set("CNH......: ")
        Label(self.frame_motorista, textvariable=self.cnh, font=(None, 8, 'bold')).grid(sticky=W, column=0,
                                                                                        row=5, padx=5,
                                                                                        columnspan=3)
        self.rg.set("RG........: ")
        Label(self.frame_motorista, textvariable=self.rg, font=(None, 8, 'bold')).grid(sticky=W, column=0,
                                                                                       row=6, padx=5,
                                                                                       columnspan=3)

    def criar_frame_transportador(self):
        self.frame_transportador = LabelFrame(self.app_main, text="Transportador")
        self.frame_transportador.place(x=10, y=175, width=650, height=90)
        self.frame_transportador.grid_columnconfigure(1, weight=1)

        Label(self.frame_transportador, text="Pesquisar", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=0,
                                                                                         padx=2)
        self.campo_pesquisa_veiculo = Entry(self.frame_transportador, textvariable=self.texto_pesquisa_transportador,
                                            width=40)
        self.campo_pesquisa_veiculo.bind('<Return>', self.pesquisar_transportador)
        self.campo_pesquisa_veiculo.grid(sticky="we", column=0, row=1, padx=2, ipady=1, pady=(0, 5))

        Button(self.frame_transportador, text='Pesquisar', command=lambda: self.pesquisar_transportador('')) \
            .grid(sticky=W, column=1, row=1, padx=2, pady=(0, 5))

        Label(self.frame_transportador, font=(None, 8, 'bold'),
              textvariable=self.dados_transportador_selecionado).grid(sticky="we", column=0, row=2, padx=2,
                                                                      columnspan=4)

    def criar_frame_veiculo(self):
        self.frame_veiculo = LabelFrame(self.app_main, text="Veículo")
        self.frame_veiculo.place(x=10, y=280, width=650, height=160)

        Label(self.frame_veiculo, text="Pesquisar", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=0, padx=2)
        self.campo_pesquisa_veiculo = Entry(self.frame_veiculo, textvariable=self.pesquisa_veiculo, width=60)
        self.campo_pesquisa_veiculo.bind('<Return>', self.pesquisar_veiculo)
        self.campo_pesquisa_veiculo.grid(sticky="we", column=0, row=1, padx=2, ipady=1, pady=(0, 5), columnspan=2)

        Button(self.frame_veiculo, text='Pesquisar', command=lambda: self.pesquisar_veiculo('')) \
            .grid(sticky="we", column=2, row=1, padx=2, pady=(0, 5))

        Label(self.frame_veiculo, text="Conjunto: ", font=(None, 8, 'normal')).grid(sticky="we", column=0, row=2,
                                                                                    padx=2)
        self.lista_veiculos_encontrados = Listbox(self.frame_veiculo, font=('Consolas', 8))
        self.lista_veiculos_encontrados.grid(sticky="we", column=0, row=3, columnspan=3)

        Label(self.frame_veiculo, text="Lacres: ", font=(None, 8, 'normal')).grid(sticky="we", column=4, row=2, padx=10)
        self.campo_lacres = scrolledtext.ScrolledText(self.frame_veiculo, undo=True, height=8, width=20, pady=6)
        self.campo_lacres.bind('<KeyRelease>', self.append_seals_list)
        self.campo_lacres.grid(sticky=W, column=4, row=3, padx=10)

    def criar_frame_saida(self):
        self.frame_saida = LabelFrame(self.app_main, text="Saída")
        self.frame_saida.place(x=10, y=450, width=650, height=160)
        self.frame_saida.grid_rowconfigure(1, weight=1)

        self.campo_saida = scrolledtext.ScrolledText(self.frame_saida, height=8, width=55)
        self.campo_saida.config(state=DISABLED)
        self.campo_saida.grid(sticky="we", column=0, row=0, padx=2, rowspan=2)

        # rodapé
        Button(self.frame_saida, text='Criar', command=self.criar).grid(sticky=W, column=1, row=0, padx=2, ipadx=40,
                                                                        ipady=20)

    # método que captura o produto selecionado
    def mudar_produto(self, event):
        self.produto_selecionado = service.find_product_by_description(self.product_name.get())
        self.deposito.set("Deposito..: {}".format(self.produto_selecionado.storage))
        self.lote.set("Lote..........: {}".format(self.produto_selecionado.batch))

    # método que verifica se o texto digitado no campo ordem/quantidade está no formato correto
    def mostrar_total_remessas(self, event):
        text = self.scroll_ordem_quantidade.get("1.0", END)

        self.separar_remessas(text)

        self.somar_total_remessas()

    # verifica se o texto digitado para remessa está correto e adiciona a lista de remessas
    def separar_remessas(self, text):
        sp = text.splitlines()
        self.remessas.clear()
        for r in sp:
            if re.findall("^(\\d*)=([0-9]+[,]+[0-9]{3,})$", r.strip()):
                # ordem de venda
                ov = split_shipping(r, 0)
                # quantidade
                amt = split_shipping(r, 1)
                self.remessas.append(model.Shipping(ov, amt, self.produto_selecionado))

    # mostrar o valor somado de todas as remessas
    def somar_total_remessas(self):
        tot = 0.0
        for ov in self.remessas:
            vl = float(ov.amount.replace(",", "."))
            tot += vl
        total_str = '{:,.3f}'.format(tot).replace(".", ",")
        self.label_total_remessas.set("Total.........: {}".format(total_str))

    def shipping(self):
        pass

    def check_product_update(self):
        update = False
        if self.produto_selecionado.storage != self.deposito.get():
            self.produto_selecionado.storage = self.deposito.get()
            update = True
        if self.produto_selecionado.batch != self.lote.get():
            self.produto_selecionado.batch = self.produto_selecionado.get()
            update = True
        return update

    def assert_shipping(self):
        if self.produto_selecionado is None:
            MessageBox(None, "Selecione um produto!")
            return False

        elif self.deposito.get() == "":
            MessageBox(None, "Informe um depósito!")
            return False

        elif self.lote.get() == "":
            MessageBox(None, "Informe um lote!")
            return False

        elif len(self.remessas) == 0:
            MessageBox(None, "Informe ao menos uma remessa!")
            return False

        return True

    def pesquisar_motorista(self, event):
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

    def pesquisar_transportador(self, event):
        pesquisa = self.texto_pesquisa_transportador.get()
        tamanho_pesquisa = len(pesquisa)
        if pesquisa and (tamanho_pesquisa == 14 or tamanho_pesquisa == 11) and pesquisa.isdigit():
            session = SAPGuiApplication.connect()
            transportador = VT01.pesquisar_transportador(session, self.texto_pesquisa_transportador.get())
            if transportador[0]:
                codigo = transportador[1]
                endereco = transportador[2]
                self.dados_transportador_selecionado.set("({}) - {}".format(codigo, endereco))

            else:
                self.dados_transportador_selecionado.set("")
                MessageBox(None, "Transportador não encontrado!")
        else:
            MessageBox(None, "Informe um cpf ou cnpj válido!")

    def set_driver(self, driver):
        self.driver_name.set("Nome..: {}".format(driver.name))
        self.cpf.set("CPF......: {}".format(driver.cpf))
        self.cnh.set("CNH......: {}".format(driver.cnh))
        self.rg.set("RG........: {}".format(driver.rg))

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

    def pesquisar_veiculo(self, event):
        board = self.pesquisa_veiculo.get()
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
                    self.lista_veiculos_encontrados.insert(END, truck)

            else:
                self.current_truck = model.Truck()
                MessageBox(None, "Nenhum conjunto com essa placa foi encontrado. Informe manualmente!")

    def set_truck(self, event):
        index = self.lista_veiculos_encontrados.curselection()[0]
        self.current_truck = self.truck_list[index]

    def clear_truck_search(self):
        self.pesquisa_veiculo.set('')
        self.clear_truck()

    def clear_truck(self):
        self.current_truck = None
        self.lista_veiculos_encontrados.delete(0, END)
        self.campo_lacres.delete('1.0', END)

    # preenche a lista de lacres
    def append_seals_list(self, event):
        text = self.campo_lacres.get("1.0", END)
        sp = text.splitlines()
        self.lacres.clear()
        for seal in sp:
            if re.findall("^\\d{7}$", seal.strip()):
                self.lacres.append(seal)

        print(self.lacres)

    def executar_vl01(self, session):
        shippings_number = []
        for shipping in self.remessas:
            result = VL01.create(session, shipping)
            if result[0]:
                shippings_number.append(result[1])
                self.inserir_saida("Remessa {} criada para ordem {}...".format(result[1], shipping.order))
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
            return QA01.create(session, self.produto_selecionado, shippings_number[0])
        else:
            for shipping in shippings_number:
                result = QA01.create(session, self.produto_selecionado, shipping)
                self.inserir_saida("Lote {} p/ remessa {}...".format(result[1], shipping))
                # se cair nesse laço, significa que o lote foi criado com sucesso
                if result[0]:
                    batchs.append(result[1])

                else:
                    # caso erro, retorna a mensagem de erro.
                    return result

            # lote de controle com a primeira remessa. Será usado no transporte.
            last_batch = QA01.create(session, self.produto_selecionado, shippings_number[0])
            self.inserir_saida("Lote {} p/ remessa {}...".format(last_batch[1], shippings_number[0]))
            batchs.append(last_batch[1])
            print(batchs)
            return True, batchs

    def inserir_saida(self, info):
        self.campo_saida.config(state="normal")
        self.campo_saida.insert(INSERT, "{}\n".format(info))
        self.campo_saida.config(state="disable")

    def criar(self):
        session = SAPGuiApplication.connect()
        if self.assert_shipping():
            result = self.executar_vl01(session)
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
