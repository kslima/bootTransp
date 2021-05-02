import os
import sys
import tkinter
from tkinter.ttk import *
from tkinter import scrolledtext, END, Listbox, W, DISABLED, INSERT, messagebox, E, CENTER, SW
import re
from win32api import MessageBox

from cadastro_motorista import CadastroMotorista
from model import Produto, Motorista, Remessa, Veiculo, Transporte
import service

# lista com todos os produtos salvos no arquivo 'properties.xml'
from cadastro_produto import CadastroProduto
from qa01 import QA01
from sapgui import SAPGuiApplication
from vl01 import VL01
from vt01 import VT01


def get_tag_value(item, tag):
    return item.findall(tag)[0].text


def split_shipping(shipping, index):
    return shipping.split('=')[index]


class AppView:

    def __init__(self):

        self.FORMATO_LABEL_TOTAL = "Qtd itens: {}  / Total: {}"
        self.app_main = tkinter.Tk()
        self.app_main.title("Utilitário de Faturamento")
        self.app_main.geometry('675x620')

        self.produto_selecionado = None
        self.remessas = []
        self.dados_produto = tkinter.StringVar()
        self.nome_produto = tkinter.StringVar()
        self.amount = tkinter.StringVar()

        self.ov = tkinter.StringVar()
        self.label_total_itens_remessas = tkinter.StringVar()
        self.label_total_pendente_remessas = tkinter.StringVar()
        self.label_total_remessas = tkinter.StringVar()
        self.msg = tkinter.StringVar()

        self.driver_name = tkinter.StringVar()
        self.cpf = tkinter.StringVar()
        self.cnh = tkinter.StringVar()
        self.rg = tkinter.StringVar()
        self.txt_pesquisa_motorista = tkinter.StringVar()
        self.motorista_selecionado = None

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
        # ------------------self.criar_frame_motorista()

        # dados da trnsportadora
        self.texto_pesquisa_transportador = tkinter.StringVar()
        self.dados_transportador_selecionado = tkinter.StringVar()
        self.frame_transportador = None
        self.campo_pesquisa_transportador = None
        # ----------------------self.criar_frame_transportador()

        # dados do veiculo
        self.frame_veiculo = None
        self.campo_pesquisa_veiculo = None
        self.lista_veiculos_encontrados = None
        self.campo_lacres = None
        # ----------------self.criar_frame_veiculo()

        # dados saída
        self.frame_saida = None
        self.campo_saida = None
        # --------------------self.criar_frame_saida()

        # exibindo em looping
        tkinter.mainloop()

    def criar_frame_remessas(self):
        self.frame_remessa = LabelFrame(self.app_main, text="Remessa")
        self.frame_remessa.place(x=10, y=10, height=190)

        Label(self.frame_remessa, text="Produto: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=0, padx=2)
        self.cbo_produtos = Combobox(self.frame_remessa, textvariable=self.nome_produto, state="readonly",
                                     postcommand=self.atualizar_lista_produtos, width=50)
        self.cbo_produtos.bind('<<ComboboxSelected>>', self.mudar_produto)
        self.cbo_produtos.grid(sticky="we", column=0, row=1, padx=2, ipady=1, pady=(0, 5), columnspan=2)

        Button(self.frame_remessa, text='Novo', command=self.cadastrar_novo_produto) \
            .grid(sticky=W, column=2, row=1, padx=2, pady=(0, 5))

        Button(self.frame_remessa, text='Editar', command=self.editar_produto) \
            .grid(sticky=W, column=3, row=1, padx=2, pady=(0, 5))

        self.dados_produto.set("*")
        label_dados_remessa = Label(self.frame_remessa, textvariable=self.dados_produto, font=(None, 9, 'bold'))
        label_dados_remessa.configure(foreground="green")
        label_dados_remessa.grid(sticky=W, column=0, row=3, padx=2, columnspan=4)

        Label(self.frame_remessa, text="Ordem/Quantidade ", font=(None, 9, 'normal')) \
            .grid(sticky=W, column=0, row=4, padx=2, ipady=2, columnspan=4)

        self.scroll_ordem_quantidade = scrolledtext.ScrolledText(self.frame_remessa, undo=True, height=4, width=20,
                                                                 state="disable")
        self.scroll_ordem_quantidade.grid(sticky=W, column=0, row=5, padx=5, rowspan=6, columnspan=2)
        self.scroll_ordem_quantidade.bind('<KeyRelease>', self.mostrar_total_remessas)

        self.label_total_remessas.set("Total: {}".format("0,000"))
        label_quantidade = Label(self.frame_remessa, textvariable=self.label_total_remessas, font=(None, 10, 'bold'))
        label_quantidade.grid(sticky=SW, column=1, row=5, padx=2, columnspan=4)
        label_quantidade.configure(foreground="blue")

        self.label_total_itens_remessas.set("Total: {}".format("0,000"))
        label_quantidade = Label(self.frame_remessa, textvariable=self.label_total_itens_remessas, font=(None, 10, 'bold'))
        label_quantidade.grid(sticky=SW, column=1, row=7, padx=2, columnspan=4)
        label_quantidade.configure(foreground="blue")

        self.label_total_pendente_remessas.set("Total pendente: {}".format("0,000"))
        label_quantidade = Label(self.frame_remessa, textvariable=self.label_total_pendente_remessas, font=(None, 10, 'bold'))
        label_quantidade.grid(sticky=SW, column=1, row=9, padx=2, columnspan=4)
        label_quantidade.configure(foreground="red")

    '''
    def criar_frame_motorista(self):
        self.frame_motorista = LabelFrame(self.app_main, text="Motorista")
        self.frame_motorista.place(x=340, y=10, width=320, height=190)

        Label(self.frame_motorista, text="Pesquisar").grid(sticky=W, column=0, row=0, padx=2)
        self.txt_pesquisa_motorista = Entry(self.frame_motorista, textvariable=self.txt_pesquisa_motorista)
        self.txt_pesquisa_motorista.grid(sticky="we", column=0, row=1, padx=2, ipady=1, pady=(0, 5), columnspan="2")
        self.txt_pesquisa_motorista.bind('<Return>', self.pesquisar_motorista)

        Button(self.frame_motorista, text='Pesquisar', command=lambda: self.pesquisar_motorista('')) \
            .grid(sticky="we", column=2, row=1, padx=2, pady=(0, 5))

        Button(self.frame_motorista, text='Novo', command=self.cadastrar_novo_motorista) \
            .grid(sticky="we", column=0, row=2, padx=2, pady=(0, 5))

        Button(self.frame_motorista, text='Editar', command=self.editar_motorista) \
            .grid(sticky="we", column=1, row=2, padx=2, pady=(0, 5))

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
                                                                                       row=6, padx=5, columnspan=3)

    def criar_frame_transportador(self):
        self.frame_transportador = LabelFrame(self.app_main, text="Transportador")
        self.frame_transportador.place(x=10, y=200, width=650, height=90)
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
    '''

    def mudar_produto(self, event):
        self.produto_selecionado = service.procurar_produto_pelo_nome(self.nome_produto.get())
        self.dados_produto.set(self.produto_selecionado)
        if self.produto_selecionado is not None:
            self.scroll_ordem_quantidade.configure(state="normal")
        else:
            self.scroll_ordem_quantidade.configure(state="disable")

    def cadastrar_novo_produto(self):
        CadastroProduto(self.app_main)

    def editar_produto(self):
        if self.produto_selecionado is None:
            messagebox.showerror("Erro", "Selecione um produto!")
        else:
            novo_produto = CadastroProduto(self.app_main)
            novo_produto.setar_campos_para_edicao(self.produto_selecionado)
            novo_produto.atualizando_cadastro = True

    def atualizar_lista_produtos(self):
        p = service.listar_produtos()
        self.cbo_produtos['values'] = tuple(prod.nome for prod in p)

    def mostrar_total_remessas(self, event):
        text = self.scroll_ordem_quantidade.get("1.0", END)
        total = self.verificar_info_total(text)
        if total:
            total = float(total)
            self.label_total_remessas.set('Total: {:,.3f}'.format(total).replace(".", ","))

        self.separar_remessas(text)

        acumulados = self.somar_total_remessas()
        self.label_total_itens_remessas.set("Total ítens: {}".format(acumulados[0]))

    def verificar_info_total(self, text):
        remessas_digitadas = text.splitlines()
        self.remessas.clear()
        for remessa in remessas_digitadas:
            remessa = remessa.strip()
            if re.findall("^\\((\\d*\\.?\\d+|\\d+(,\\d+)*(\\.\\d+)?)\\)$", remessa):
                total = remessa.replace(",", ".")
                total = total.replace("(", "")
                total = total.replace(")", "")
                return total
        return ""

    def separar_remessas(self, text):
        remessas_digitadas = text.splitlines()
        self.remessas.clear()
        for remessa in remessas_digitadas:
            remessa = remessa.strip()
            if re.findall("^(\\d*)=([0-9]+[,]+[0-9]{3,})$", remessa):
                numero_ordem = split_shipping(remessa, 0)
                quantidade = split_shipping(remessa, 1)
                self.remessas.append(Remessa(numero_ordem, quantidade, self.produto_selecionado))

    def somar_total_remessas(self):
        tot = 0.0
        contador_itens = 0
        for remessa in self.remessas:
            vl = float(remessa.quantidade.replace(",", "."))
            tot += vl
            contador_itens = contador_itens + 1
        acumulado = '{:,.3f}'.format(tot).replace(".", ",")

        return contador_itens, acumulado
        # self.label_total_remessas.set(self.FORMATO_LABEL_TOTAL.format(contador_itens, total_str))

    def assert_shipping(self):
        if self.produto_selecionado is None:
            messagebox.showerror("Campo obrigatório", "Selecione um produto!")
            return False

        elif self.deposito.get() == "":
            messagebox.showerror("Campo obrigatório", "Informe um depósito!")
            return False

        elif self.lote.get() == "":
            messagebox.showerror("Campo obrigatório", "Informe um lote!")
            return False

        elif len(self.remessas) == 0:
            messagebox.showerror("Campo obrigatório", "Informe ao menos uma remessa!")
            return False

        return True

    def cadastrar_novo_motorista(self):
        CadastroMotorista(self.app_main)

    def editar_motorista(self):
        if self.motorista_selecionado is None:
            messagebox.showerror("Erro", "Selecione um motorista!")
        else:
            novo_motorista = CadastroMotorista(self.app_main)
            novo_motorista.setar_campos_para_edicao(self.motorista_selecionado)
            novo_motorista.atualizando_cadastro = True

    def pesquisar_motorista(self, event):
        if self.txt_pesquisa_motorista.get() != "":
            self.motorista_selecionado = service.procurar_motorista_por_documento(self.txt_pesquisa_motorista.get())

            if self.motorista_selecionado is not None:
                self.setar_dados_motorista_selecionado()
            else:
                messagebox.showerror("Erro", "Nenhum motorista encontrado!")
        else:
            messagebox.showerror("Erro", "Ao menos um valor para CPF, CNH ou RG deve ser informado!")

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

    def setar_dados_motorista_selecionado(self):
        self.driver_name.set(self.motorista_selecionado.nome)
        self.cpf.set(self.motorista_selecionado.cpf)
        self.cnh.set(self.motorista_selecionado.cnh)
        self.rg.set(self.motorista_selecionado.rg)

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
                self.current_truck = Veiculo
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
                    transporte = Transporte()
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
