import os
import sys
import tkinter
from tkinter.ttk import *
from tkinter import scrolledtext, END, Listbox, W, DISABLED, INSERT, messagebox, E, CENTER, SW
import re
from win32api import MessageBox

from cadastro_motorista import CadastroMotorista
from model import Produto, Motorista, Remessa, Veiculo, Transporte, Carregamento, LoteInspecao
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
        self.app_main.geometry('515x800')

        menubar = tkinter.Menu(self.app_main)

        filemenu = tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Abrir planilha de configuração")
        filemenu.add_command(label="Sair", command=self.app_main.quit)

        menubar.add_cascade(label="Arquivo", menu=filemenu)

        self.app_main.config(menu=menubar)

        self.produto_selecionado = None
        self.remessas = []
        self.dados_produto = tkinter.StringVar()
        self.nome_produto = tkinter.StringVar()
        self.amount = tkinter.StringVar()

        self.ov = tkinter.StringVar()
        self.total_itens_remessas = tkinter.StringVar()
        self.total_acumulado_remessas = tkinter.StringVar()
        self.total_pendente_remessas = tkinter.StringVar()
        self.label_total_remessas = tkinter.StringVar()
        self.msg = tkinter.StringVar()

        self.driver_name = tkinter.StringVar()
        self.cpf = tkinter.StringVar()
        self.cnh = tkinter.StringVar()
        self.rg = tkinter.StringVar()
        self.txt_pesquisa_motorista = tkinter.StringVar()
        self.motorista_selecionado = None

        self.lacres = tkinter.StringVar()
        self.pesquisa_veiculo = tkinter.StringVar()
        self.lista_veiculos = []
        self.veiculo_selecionado = None

        # dados de remssa
        self.frame_remessa = None
        self.scroll_ordem_quantidade = None
        self.cbo_produtos = None
        self.label_quantidade_pendente = None
        self.criar_frame_remessas()

        # dados motorista
        self.frame_motorista = None
        self.txt_pesquisa_motorista = None
        self.criar_frame_motorista()

        # dados da trnsportadora
        self.texto_pesquisa_transportador = tkinter.StringVar()
        self.dados_transportador_selecionado = tkinter.StringVar()
        self.codigo_transportador_selecionado = tkinter.StringVar()
        self.numero_pedido = tkinter.StringVar()
        self.frame_transportador = None
        self.campo_pesquisa_transportador = None
        self.criar_frame_transportador()

        # dados do veiculo
        self.frame_veiculo = None
        self.campo_pesquisa_veiculo = None
        self.lista_veiculos_encontrados = None
        self.label_dados_conjunto = None
        self.label_quantidade_lacres = tkinter.StringVar()
        self.dados_conjunto = tkinter.StringVar()
        self.criar_frame_veiculo()

        # dados saída
        self.frame_saida = None
        self.campo_saida = None
        self.criar_frame_saida()

        tkinter.mainloop()

    def criar_frame_remessas(self):
        self.frame_remessa = LabelFrame(self.app_main, text="Remessa")
        self.frame_remessa.place(x=10, y=10, height=190, width=490)

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
        label_quantidade = Label(self.frame_remessa, textvariable=self.label_total_remessas, font=(None, 8, 'bold'))
        label_quantidade.grid(sticky=SW, column=1, row=5, padx=2, columnspan=4)
        label_quantidade.configure(foreground="blue")

        self.total_itens_remessas.set("Remessas: {}".format("0"))
        label_numero_remessas = Label(self.frame_remessa, textvariable=self.total_itens_remessas,
                                      font=(None, 8, 'bold'))
        label_numero_remessas.grid(sticky=SW, column=1, row=6, padx=2, columnspan=4)
        label_numero_remessas.configure(foreground="blue")

        self.total_acumulado_remessas.set("Acumulado: {}".format("0,000"))
        label_acumulado = Label(self.frame_remessa, textvariable=self.total_acumulado_remessas,
                                font=(None, 8, 'bold'))
        label_acumulado.grid(sticky=SW, column=1, row=7, padx=2, columnspan=4)
        label_acumulado.configure(foreground="blue")

        self.total_pendente_remessas.set("Pendente: {}".format("0,000"))
        self.label_quantidade_pendente = Label(self.frame_remessa, textvariable=self.total_pendente_remessas,
                                               font=(None, 8, 'bold'))
        self.label_quantidade_pendente.grid(sticky=SW, column=1, row=8, padx=2, columnspan=4)
        self.label_quantidade_pendente.configure(foreground="blue")

    def criar_frame_motorista(self):
        self.frame_motorista = LabelFrame(self.app_main, text="Motorista")
        self.frame_motorista.place(x=10, y=210, width=490, height=110)

        Label(self.frame_motorista, text="Pesquisar").grid(sticky=W, column=0, row=0, padx=2)
        self.txt_pesquisa_motorista = Entry(self.frame_motorista, textvariable=self.txt_pesquisa_motorista, width=39)
        self.txt_pesquisa_motorista.grid(sticky="we", column=0, row=1, padx=2, ipady=1, pady=(0, 5), columnspan=2)
        self.txt_pesquisa_motorista.bind('<Return>', self.pesquisar_motorista)

        Button(self.frame_motorista, text='Pesquisar', command=lambda: self.pesquisar_motorista('')) \
            .grid(sticky="we", column=2, row=1, padx=2, pady=(0, 5))

        Button(self.frame_motorista, text='Novo', command=self.cadastrar_novo_motorista) \
            .grid(sticky="we", column=3, row=1, padx=2, pady=(0, 5))

        Button(self.frame_motorista, text='Editar', command=self.editar_motorista) \
            .grid(sticky="we", column=4, row=1, padx=2, pady=(0, 5))

        self.driver_name.set("*")
        label_nome_motorista = Label(self.frame_motorista, textvariable=self.driver_name, font=(None, 8, 'bold'),
                                     wraplength=450)
        label_nome_motorista.grid(sticky=W, column=0, row=2, padx=5, columnspan=5)
        label_nome_motorista.configure(foreground="green")

    def criar_frame_transportador(self):
        self.frame_transportador = LabelFrame(self.app_main, text="Transportador")
        self.frame_transportador.place(x=10, y=330, width=490, height=110)
        self.frame_transportador.grid_columnconfigure(1, weight=1)

        Label(self.frame_transportador, text="Pesquisar", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=0,
                                                                                         padx=2)
        self.campo_pesquisa_veiculo = Entry(self.frame_transportador, textvariable=self.texto_pesquisa_transportador,
                                            width=45)
        self.campo_pesquisa_veiculo.bind('<Return>', self.pesquisar_transportador)
        self.campo_pesquisa_veiculo.grid(sticky="we", column=0, row=1, padx=2, ipady=1, pady=(0, 5))

        Button(self.frame_transportador, text='Pesquisar', command=lambda: self.pesquisar_transportador('')) \
            .grid(sticky=W, column=1, row=1, padx=2, pady=(0, 5))

        Label(self.frame_transportador, text="Pedido", font=(None, 8, 'normal')).grid(sticky=W, column=2, row=0,
                                                                                      padx=2)
        Entry(self.frame_transportador, textvariable=self.numero_pedido).grid(sticky=W, column=2, row=1, padx=5,
                                                                              ipady=1, pady=(0, 5))

        self.dados_transportador_selecionado.set("*")
        label_dados_transportadora = Label(self.frame_transportador, font=(None, 8, 'bold'), wraplength=450,
                                           textvariable=self.dados_transportador_selecionado)
        label_dados_transportadora.grid(sticky="we", column=0, row=2, padx=2, columnspan=4)
        label_dados_transportadora.configure(foreground="green")

    def criar_frame_veiculo(self):
        self.frame_veiculo = LabelFrame(self.app_main, text="Veículo")
        self.frame_veiculo.place(x=10, y=450, width=490, height=200)

        Label(self.frame_veiculo, text="Pesquisar", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=0, padx=2)
        self.campo_pesquisa_veiculo = Entry(self.frame_veiculo, textvariable=self.pesquisa_veiculo, width=52)
        self.campo_pesquisa_veiculo.bind('<Return>', self.pesquisar_veiculo)
        self.campo_pesquisa_veiculo.grid(sticky="we", column=0, row=1, padx=2, ipady=1, pady=(0, 5), columnspan=2)

        Button(self.frame_veiculo, text='Pesquisar', command=lambda: self.pesquisar_veiculo('')) \
            .grid(sticky=W, column=2, row=1, padx=2, pady=(0, 5))

        Button(self.frame_veiculo, text='Novo', command=self.cadastrar_novo_produto) \
            .grid(sticky=W, column=3, row=1, padx=2, pady=(0, 5))

        Label(self.frame_veiculo, text="Conjuntos encontrados: ", font=(None, 8, 'normal')).grid(sticky="we", column=0,
                                                                                                 row=2,
                                                                                                 padx=2)
        self.lista_veiculos_encontrados = Listbox(self.frame_veiculo, font=('Consolas', 8), height=3)
        self.lista_veiculos_encontrados.bind('<Double-Button>', self.selecionar_veiculo)
        self.lista_veiculos_encontrados.grid(sticky="we", column=0, row=3, columnspan=4, padx=2)

        self.label_dados_conjunto = Label(self.frame_veiculo, text="*", font=(None, 8, 'bold'),
                                          textvariable=self.dados_conjunto)
        self.label_dados_conjunto.configure(foreground="green")
        self.label_dados_conjunto.grid(sticky="we", column=0, row=4, padx=2)

        self.label_quantidade_lacres.set("Lacres: (0)")
        Label(self.frame_veiculo, font=(None, 8, 'normal'), textvariable=self.label_quantidade_lacres) \
            .grid(sticky="we", column=0, row=5, padx=2)

        entrada_lacres = Entry(self.frame_veiculo, textvariable=self.lacres)
        entrada_lacres.grid(sticky="we", column=0, row=6, padx=5, columnspan=4)
        entrada_lacres.bind("<KeyRelease>", self.separar_lacres)

    def criar_frame_saida(self):
        self.frame_saida = LabelFrame(self.app_main, text="Saída")
        self.frame_saida.place(x=10, y=660, width=490, height=120)
        self.frame_saida.grid_rowconfigure(1, weight=1)

        self.campo_saida = scrolledtext.ScrolledText(self.frame_saida, height=4, width=57)
        self.campo_saida.config(state=DISABLED)
        self.campo_saida.grid(sticky="we", column=0, row=0, padx=2)

        # rodapé
        Button(self.frame_saida, text='Criar', command=self.criar).grid(sticky=W, column=0, row=1, padx=2)

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
        self.separar_remessas(text)

        acumulados = self.somar_total_remessas()
        itens = acumulados[0]
        acumulado = acumulados[1]
        self.total_itens_remessas.set("Remessas: {}".format(itens))
        self.total_acumulado_remessas.set("Acumulado: {}".format(acumulado).replace(".", ","))

        total = self.verificar_info_total(text)
        if total:
            total = float(total)
            acumulado = float(acumulado)
            pendente = total - acumulado
            self.label_total_remessas.set('Total: {:,.3f}'.format(total).replace(".", ","))
            self.total_pendente_remessas.set('Pendente: {:,.3f}'.format(pendente).replace(".", ","))
            if pendente == 0:
                self.label_quantidade_pendente.configure(foreground="blue")
            else:
                self.label_quantidade_pendente.configure(foreground="red")

    def verificar_info_total(self, text):
        if not text.strip():
            return "0.000"

        remessas_digitadas = text.splitlines()
        for remessa in remessas_digitadas:
            remessa = remessa.strip()
            if re.findall("^(\\([0-9]*[,]*[0-9]+\\))$", remessa):
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
            if re.findall("^(\\d*)=([0-9]*[,]*[0-9]+)$", remessa):
                numero_ordem = split_shipping(remessa, 0)
                quantidade = split_shipping(remessa, 1)
                self.remessas.append(Remessa(numero_ordem, quantidade, self.produto_selecionado))
        print(self.remessas)

    def somar_total_remessas(self):
        tot = 0.0
        contador_itens = 0
        for remessa in self.remessas:
            vl = float(remessa.quantidade.replace(",", "."))
            tot += vl
            contador_itens = contador_itens + 1
        acumulado = '{:,.3f}'.format(tot)

        return contador_itens, acumulado
        # self.label_total_remessas.set(self.FORMATO_LABEL_TOTAL.format(contador_itens, total_str))

    def assert_shipping(self):
        print('tamanho da lista ' + str(len(self.remessas)))
        if self.produto_selecionado is None:
            messagebox.showerror("Campo obrigatório", "Selecione um produto!")
            return False

        if len(self.remessas) == 0:
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
                self.motorista_selecionado = None
                self.setar_dados_motorista_selecionado()
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
                self.codigo_transportador_selecionado.set(codigo)
                self.dados_transportador_selecionado.set("({}) - {}".format(codigo, endereco))

            else:
                self.dados_transportador_selecionado.set("")
                MessageBox(None, "Transportador não encontrado!")
        else:
            MessageBox(None, "Informe um cpf ou cnpj válido!")

    def setar_dados_motorista_selecionado(self):
        if self.motorista_selecionado is None:
            self.driver_name.set("")
        else:
            self.driver_name.set(self.motorista_selecionado)

    def pesquisar_veiculo(self, event):
        placa = self.pesquisa_veiculo.get()
        if placa == "":
            MessageBox(None, "Informe uma placa para pesquisa!")

        elif not re.findall("^[a-zA-Z]{3}[0-9][A-Za-z0-9][0-9]{2}$", placa):
            MessageBox(None, "A placa formato incorreto!")

        else:
            # self.clear_truck()
            veiculos_encontrados = service.find_trucks(placa)
            if len(veiculos_encontrados) > 0:
                # self.truck_list.clear()

                for veiculo in veiculos_encontrados:
                    self.lista_veiculos.append(veiculo)
                    self.lista_veiculos_encontrados.insert(END, veiculo)

            else:
                self.veiculo_selecionado = Veiculo
                MessageBox(None, "Nenhum conjunto com essa placa foi encontrado. Informe manualmente!")

    def selecionar_veiculo(self, event):
        index = self.lista_veiculos_encontrados.curselection()[0]
        self.veiculo_selecionado = self.lista_veiculos[index]
        self.dados_conjunto.set(self.veiculo_selecionado)

    def cadastrar_novo_veiculo(self):
        pass

    def separar_lacres(self, event):
        lacres = self.lacres.get().strip()
        if lacres != "":
            lacres = lacres.split(" ")
        self.label_quantidade_lacres.set("Lacres: ({})".format(str(len(lacres))))

    def criar_remessas(self, session):
        numero_remessas = []
        for remessa in self.remessas:
            result = VL01.create(session, remessa)
            if result[0]:
                numero_remessas.append(result[1])
                self.inserir_saida("Remessa {} criada na ordem {}...".format(result[1], remessa.numero_ordem))
            else:
                # caso erro, retorna a mensagem de erro.
                return result
        # caso sucesso, retorna uma lista com os numeros das remessas criadas
        print(numero_remessas)
        return True, numero_remessas

    # criando lotes de controle de qualidade
    def criar_lotes_qualidade(self, session, remessas):
        lotes = []
        oritem_lote = "89"
        messagem_progresso = "Lote {} criado na remessa {}..."
        for remessa in remessas:
            result = QA01.create(session, self.produto_selecionado, remessa, oritem_lote)
            self.inserir_saida(messagem_progresso.format(result[1], remessa))
            # se cair nesse laço, significa que o lote foi criado com sucesso
            if result[0]:
                lotes.append(result[1])

            else:
                # caso erro, retorna a mensagem de erro.
                return result

        # lote de controle com a primeira remessa. Será usado no transporte.
        if len(remessas) > 1:
            last_batch = QA01.create(session, self.produto_selecionado, remessas[0], oritem_lote)
            self.inserir_saida(messagem_progresso.format(last_batch[1], remessas[0]))
            lotes.append(last_batch[1])
            print(lotes)
        return True, lotes

    def criar_transporte(self, session, carregamento):
        resultado = VT01.create(session, carregamento)
        if resultado[0]:
            self.inserir_saida("Transporte {} criado...".format(resultado[0]))
        return resultado

    def inserir_saida(self, info):
        self.campo_saida.config(state="normal")
        self.campo_saida.insert(INSERT, "{}\n".format(info))
        self.campo_saida.config(state="disable")
        self.app_main.update_idletasks()

    def criar(self):
        resultado_remessas = None
        resultado_lotes_qualidade = None
        resultado_transporte = None
        session = SAPGuiApplication.connect()
        if self.assert_shipping():
            resultado_remessas = self.criar_remessas(session)

            # se houver erro, uma mensagem será exibida com o erro.
            if not resultado_remessas[0]:
                messagebox.showerror("Erro", resultado_remessas[1])
                return

        if self.produto_selecionado.inspecao_produto == "s":
            resultado_lotes_qualidade = self.criar_lotes_qualidade(session, resultado_remessas[1])

            if not resultado_lotes_qualidade[0]:
                messagebox.showerror("Erro", resultado_lotes_qualidade[1])
                return

        carregamento = Carregamento()
        carregamento.remessas = resultado_remessas[1]

        if resultado_lotes_qualidade is not None:
            carregamento.lotes_qualidade = resultado_lotes_qualidade[1]

        carregamento.codigo_transportador = self.codigo_transportador_selecionado.get()
        carregamento.produto = self.produto_selecionado
        carregamento.veiculo = self.veiculo_selecionado
        carregamento.motorista = self.motorista_selecionado
        carregamento.lacres = self.lacres.get()
        carregamento.numero_pedido = self.numero_pedido.get()

        resultado_transporte = self.criar_transporte(session, carregamento)
        if not resultado_transporte[0]:
            messagebox.showerror("Erro", resultado_transporte[1])
            return

        if carregamento.lote_veiculo.lower() == "s":
            inspecao_veicular = main.criar_lote_inspecao_veiculo(session,
                                                                 carregamento.produto.codigo,
                                                                 carregamento.veiculo.placa_1,
                                                                 resultado_transporte[1])
        '''
                    if self.current_driver is None:
                # criando novo motorista
                if self.create_new_driver():
                    pass
                    
                        elif self.current_truck is None:
            MessageBox(None, "Informe um veículo!")
            return False
            '''

    @staticmethod
    def criar_lote_inspecao_veiculo(sap_session, codigo_produto, lote, texto_breve):
        inspecao_veiculo = LoteInspecao()
        if codigo_produto[0] == "1":
            inspecao_veiculo.material = "INSPVEICALCOOL"
        elif codigo_produto[0] == "3":
            inspecao_veiculo.material.codigo = "INSPVEICACUCAR"

        inspecao_veiculo.centro = "1014"
        inspecao_veiculo.origem = "07"
        inspecao_veiculo.lote = lote
        inspecao_veiculo.texto_breve = texto_breve
        return inspecao_veiculo


main = AppView()
