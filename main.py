import sys
import tkinter
import traceback
from tkinter import W, DISABLED, messagebox, CENTER, NO, ttk
from tkinter.ttk import *

import peewee
from ttkbootstrap import Style
from win32api import MessageBox

import service
from cadastro_lacres import CadastroLacres
from cadastro_motorista import CadastroMotorista
from cadastro_produto import CadastroProduto
from cadastro_veiculo import CadastroVeiculo
from consulta_saldo import ConsultaSaldo
from dialogo_entrada import DialogoEntrada
from model import Remessa, Carregamento, LoteInspecao, ItemRemessa
from qa import QA01
from qe import QE01
from sapgui import SAPGuiApplication
from sapguielements import SAPGuiElements
from service import MotoristaService, VeiculoService, ProdutoService, TransportadorService
from utilitarios import StringUtils, NumberUtils
from vl import VL01
from vt import VT01, VT02
import sys
import traceback

from xk03 import XK03


class Main:

    def __init__(self):
        self.style = Style()
        self.app_main = self.style.master
        self.style.theme_use("flatly")
        self.app_main.title("Utilitário de Faturamento")
        # self.app_main.geometry('600x680')
        self.centralizar_tela()

        # self.app_main.configure(bg='#eaf1f6')

        self.janela_cadastro_lacres = None
        self.carregamento_atual = None

        # Main.criar_estilo()

        menubar = tkinter.Menu(self.app_main)

        filemenu = tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Abrir planilha de configuração")
        filemenu.add_command(label="Sair", command=self.app_main.quit)

        menubar.add_cascade(label="Arquivo", menu=filemenu)

        self.app_main.config(menu=menubar)

        self.TEXTO_DADOS_MOTORISTA = "** NENHUM MOTORISTA SELECIONADO **"
        self.TEXTO_DADOS_VEICULO = "** NENHUM VEÍCULO SELECIONADO **"
        self.TEXTO_DADOS_TRANPORTADOR = "** NENHUM TRANSPORTADOR SELECIONADO **"

        self.produto_selecionado = None
        self.lacres_selecionados = None
        self.transportador_selecionado = None
        self.remessas = []
        self.dados_produto = tkinter.StringVar()
        self.nome_produto = tkinter.StringVar()
        self.amount = tkinter.StringVar()

        self.ov = tkinter.StringVar()
        self.total_itens_remessas = tkinter.StringVar()
        self.total_acumulado_itens_remessas = tkinter.StringVar()
        self.total_pendente_itens_remessas = tkinter.StringVar()
        self.total_acumulado_remessas = tkinter.StringVar()
        self.total_pendente_remessas = tkinter.StringVar()
        self.label_total_remessas = tkinter.StringVar()
        self.msg = tkinter.StringVar()

        self.saida_remessas = tkinter.StringVar()
        self.saida_inpecao_produto = tkinter.StringVar()
        self.saida_transporte = tkinter.StringVar()
        self.saida_inspecao_veiculo = tkinter.StringVar()

        self.dados_motorista_selecionado = tkinter.StringVar()
        self.cpf = tkinter.StringVar()
        self.cnh = tkinter.StringVar()
        self.rg = tkinter.StringVar()
        self.txt_pesquisa_motorista = tkinter.StringVar()
        self.motorista_selecionado = None

        self.codigo_lacres = tkinter.StringVar()
        self.lacres = tkinter.StringVar()
        self.pesquisa_veiculo = tkinter.StringVar()
        self.lista_veiculos = []
        self.veiculo_selecionado = None

        self.label_quantidade_lacres = tkinter.StringVar()
        self.dados_veiculo_selecionado = tkinter.StringVar()
        self.pesquisa_motorista = tkinter.StringVar()

        # tabs
        self.tabControl = Notebook(self.app_main)
        self.tab_remessa = None
        self.tab_motorista = None
        self.tab_veiculo = None
        self.tab_transporte = None
        self.criar_abas()

        # dados de remssa
        self.frame_remessa = None
        self.cbo_produtos = None
        self.label_quantidade_pendente = None

        # dados motorista
        self.frame_motorista = None
        self.txt_pesquisa_motorista = None
        self.treeview_motorista = None
        self.label_dados_nome_motorista = None
        self.label_dados_transportadora = None

        # dados da trnsportadora
        self.texto_pesquisa_transportador = tkinter.StringVar()
        self.dados_transportador_selecionado = tkinter.StringVar()
        self.codigo_transportador_selecionado = tkinter.StringVar()
        self.numero_pedido = tkinter.StringVar()
        self.ordem_item_remessa = tkinter.StringVar()
        self.quantidade_item_remessa = tkinter.StringVar()
        self.frame_transportador = None
        self.campo_pesquisa_transportador = None

        # dados do veiculo
        self.frame_veiculo = None
        self.campo_pesquisa_veiculo = None
        self.lista_veiculos_encontrados = None
        self.label_dados_veiculo_selecionado = None
        self.treeview_veiculo = None
        self.treeview_remessas = None
        self.entry_ordem_remessa = None
        self.entry_quantidade_remessa = None
        self.entry_quantidade_total_remessas = None
        self.entry_quantidade_acumulada_remessas = None
        self.entry_quantidade_pendente_remessas = None
        self.label_total_itens_remessas = None

        # dados saída
        self.frame_saida = None
        self.criar_frame_remessas()
        self.criar_frame_motorista()
        self.criar_frame_veiculo()
        # self.criar_frame_transportador()
        self.criar_frame_saida()

        tkinter.mainloop()

    def criar_estilo(self):

        style = ttk.Style()
        style.theme_create('Cloud', settings={
            ".": {
                "configure": {
                    "background": '#dfebf5',  # All colors except for active tab-button
                    "font": 'red',
                    "font-size": '8'
                }
            },
            "TNotebook": {
                "configure": {
                    "background": '#eaf1f6',  # color behind the notebook
                    "tabmargins": [5, 5, 0, 0],
                    # [left margin, upper margin, right margin, margin beetwen tab and frames]
                }
            },
            "TNotebook.Tab": {
                "configure": {
                    "background": '#cbdbea',  # Color of non selected tab-button
                    "padding": [5, 2],
                    "font": "white"
                },
                "map": {
                    "background": [("selected", '#8db2da')],  # Color of active tab
                    "expand": [("selected", [1, 1, 1, 0])]  # [expanse of text]
                }
            }
        })

    def centralizar_tela(self):
        # Gets the requested values of the height and widht.
        window_width = self.app_main.winfo_reqwidth()
        window_height = self.app_main.winfo_reqheight()

        # Gets both half the screen width/height and window width/height
        position_right = int(self.app_main.winfo_screenwidth() / 2.5 - window_width / 2)
        position_down = int(self.app_main.winfo_screenheight() / 5 - window_height / 2)

        # Positions the window in the center of the page.
        self.app_main.geometry("+{}+{}".format(position_right, position_down))

    def criar_abas(self):
        self.tab_remessa = Frame(self.tabControl)
        self.tab_motorista = Frame(self.tabControl)
        self.tab_veiculo = Frame(self.tabControl)

        self.tabControl.add(self.tab_remessa, text="Remessas")
        self.tabControl.add(self.tab_motorista, text="Motorista")
        self.tabControl.add(self.tab_veiculo, text="Veículo")
        self.tabControl.grid(sticky=W, column=0, row=0, padx=10, pady=10)

    def criar_frame_remessas(self):
        Label(self.tab_remessa, text="Produto: ").grid(sticky=W, column=0, row=0, padx=5)
        self.cbo_produtos = Combobox(self.tab_remessa, textvariable=self.nome_produto, state="readonly",
                                     postcommand=self.atualizar_lista_produtos)
        self.cbo_produtos.bind('<<ComboboxSelected>>', self.mudar_produto)
        self.cbo_produtos.grid(sticky="we", column=0, row=1, padx=5, ipady=1, pady=(0, 5), columnspan=2)

        Button(self.tab_remessa, text='Novo', command=self.cadastrar_novo_produto) \
            .grid(sticky="we", column=2, row=1, padx=5, pady=(0, 5))

        Button(self.tab_remessa, text='Editar', command=self.editar_produto) \
            .grid(sticky="we", column=3, row=1, padx=5, pady=(0, 5))

        Label(self.tab_remessa, text="Ordem: ").grid(sticky=W, row=2, padx=5)
        frame_ordem = Frame(self.tab_remessa)
        frame_ordem.grid(sticky="we", row=3, padx=5, ipady=1)
        self.entry_ordem_remessa = Entry(frame_ordem, textvariable=self.ordem_item_remessa)
        self.entry_ordem_remessa.grid(sticky="we", row=3, ipady=1)
        self.entry_ordem_remessa.config(validate="key",
                                        validatecommand=(self.app_main.register(NumberUtils.eh_inteiro), '%P'))

        Button(frame_ordem, text='...', command=self.pesquisar_ordens) \
            .grid(sticky="we", column=1, row=3, padx=(5, 0))

        Label(self.tab_remessa, text="Quantidade: ").grid(sticky=W, column=1, row=2, padx=5)
        self.entry_quantidade_remessa = Entry(self.tab_remessa, textvariable=self.quantidade_item_remessa)
        self.entry_quantidade_remessa.grid(sticky="we", column=1, row=3, padx=(0, 5), ipady=1)
        self.entry_quantidade_remessa.config(validate="key",
                                             validatecommand=(self.app_main.register(NumberUtils.eh_decimal), '%P'))
        self.entry_quantidade_remessa.bind('<Return>', self.inserir_item_remessa)
        # self.entry_quantidade_remessa.bind('<KeyRelease>', self.mostrar_total_remessas)

        Button(self.tab_remessa, text='Adicionar', command=lambda: self.inserir_item_remessa(None)) \
            .grid(sticky="we", column=2, row=3, padx=5)

        Button(self.tab_remessa, text='Remover', command=self.eliminar_item_remessas) \
            .grid(sticky="we", column=3, row=3, padx=5)

        self.treeview_remessas = Treeview(self.tab_remessa, height=4,
                                          column=("c0", "c1", "c2", "c3", "c4"), show="headings")
        self.treeview_remessas.heading("#1", text="Ordem")
        self.treeview_remessas.heading("#2", text="Produto")
        self.treeview_remessas.heading("#3", text="Quantidade")
        self.treeview_remessas.heading("#4", text="Deposito")
        self.treeview_remessas.heading("#5", text="Lote")

        self.treeview_remessas.column("c0", width=80, stretch=NO, anchor=CENTER)
        self.treeview_remessas.column("c1", stretch=NO, anchor=CENTER)
        self.treeview_remessas.column("c2", width=100, stretch=NO, anchor=CENTER)
        self.treeview_remessas.column("c3", width=100, stretch=NO, anchor=CENTER)
        self.treeview_remessas.column("c4", stretch=NO, anchor=CENTER)

        self.treeview_remessas.grid(sticky="we", column=0, row=4, padx=5, columnspan=4, pady=(5, 0))
        # self.treeview_remessas.tag_configure('bg', background='yellow')

        frame_totais = Frame(self.tab_remessa)
        frame_totais.grid(sticky=W, row=5, padx=5, columnspan=3, pady=(10, 0))

        Label(frame_totais, text="Total: ").grid(sticky=W, padx=5)
        self.entry_quantidade_total_remessas = Entry(frame_totais, textvariable=self.total_itens_remessas)
        self.entry_quantidade_total_remessas.grid(sticky="we", row=1, ipady=1, pady=(0, 5), padx=(0, 5))
        self.entry_quantidade_total_remessas.config(validate="key",
                                                    validatecommand=(self.app_main.register(NumberUtils.eh_decimal),
                                                                     '%P'))
        self.entry_quantidade_total_remessas.bind("<KeyRelease>", self.calcular_total_itens_remessa)

        self.total_acumulado_itens_remessas.set("0,000")
        Label(frame_totais, text="Acumulado: ").grid(sticky=W, column=1, row=0, padx=5)
        self.entry_quantidade_acumulada_remessas = Entry(frame_totais, state="readonly",
                                                         textvariable=self.total_acumulado_itens_remessas)
        self.entry_quantidade_acumulada_remessas \
            .grid(sticky="we", column=1, row=1, padx=5, ipady=1, pady=(0, 5))
        self.entry_quantidade_acumulada_remessas.config(validate="key", validatecommand=(
            self.app_main.register(NumberUtils.eh_decimal), '%P'))

        self.total_pendente_itens_remessas.set("0,000")
        Label(frame_totais, text="Pendente: ").grid(sticky=W, column=2, row=0, padx=5)
        self.entry_quantidade_pendente_remessas = Entry(frame_totais, state="readonly",
                                                        textvariable=self.total_pendente_itens_remessas)
        self.entry_quantidade_pendente_remessas \
            .grid(sticky="we", column=2, row=1, padx=5, ipady=1, pady=(0, 5))
        self.entry_quantidade_pendente_remessas.config(validate="key",
                                                       validatecommand=(
                                                           self.app_main.register(NumberUtils.eh_decimal), '%P'))

    def criar_frame_motorista(self):

        Label(self.tab_motorista, text="Pesquisar motorista").grid(sticky=W, column=0, row=0, padx=5)
        self.txt_pesquisa_motorista = Entry(self.tab_motorista, textvariable=self.pesquisa_motorista)
        self.txt_pesquisa_motorista.grid(sticky="we", column=0, row=1, padx=5, ipady=1, pady=(0, 5), columnspan=3)
        # self.txt_pesquisa_motorista.bind('<Return>', self.pesquisar_motorista)
        self.txt_pesquisa_motorista.bind("<KeyRelease>", self.pesquisar_motorista)

        Button(self.tab_motorista, text='Novo', command=self.cadastrar_novo_motorista) \
            .grid(sticky="we", column=3, row=1, padx=5, pady=(0, 5))

        Button(self.tab_motorista, text='Editar', command=self.editar_motorista) \
            .grid(sticky="we", column=4, row=1, padx=5, pady=(0, 5))

        self.treeview_motorista = Treeview(self.tab_motorista, selectmode="browse", height=4,
                                           column=("c0", "c1", "c2", "c3", "c4"), show="headings")
        self.treeview_motorista.heading("#1", text="ID")
        self.treeview_motorista.heading("#2", text="Nome")
        self.treeview_motorista.heading("#3", text="CPF")
        self.treeview_motorista.heading("#4", text="CNH")
        self.treeview_motorista.heading("#5", text="RG")

        self.treeview_motorista.column("c0", width=40, stretch=NO, anchor=CENTER)
        self.treeview_motorista.column("c1", stretch=NO, anchor=CENTER)
        self.treeview_motorista.column("c2", stretch=NO, anchor=CENTER)
        self.treeview_motorista.column("c3", width=120, stretch=NO, anchor=CENTER)
        self.treeview_motorista.column("c4", width=120, stretch=NO, anchor=CENTER)

        self.treeview_motorista.grid(sticky=W, column=0, row=2, padx=5, columnspan=5)
        self.treeview_motorista.bind("<Double-1>", self.setar_motorista_selecionado)

        self.dados_motorista_selecionado.set(self.TEXTO_DADOS_MOTORISTA)
        self.label_dados_nome_motorista = Label(self.tab_motorista, textvariable=self.dados_motorista_selecionado,
                                                font=(None, 8, 'bold'), wraplength=450)
        self.label_dados_nome_motorista.grid(sticky=W, column=0, row=3, padx=5, columnspan=5)
        self.label_dados_nome_motorista.configure(foreground="red")

        # ---------------------

        Label(self.tab_motorista, text="Transportador").grid(sticky=W, row=4, padx=2)
        self.campo_pesquisa_transportador = Entry(self.tab_motorista, textvariable=self.texto_pesquisa_transportador)
        self.campo_pesquisa_transportador.bind('<Return>', self.pesquisar_transportador)
        self.campo_pesquisa_transportador.config(validate="key",
                                                 validatecommand=(self.app_main.register(NumberUtils.eh_inteiro), '%P'))
        self.campo_pesquisa_transportador.grid(sticky="we", row=5, padx=2, ipady=1, pady=(0, 5), columnspan=4)

        Button(self.tab_motorista, text='Pesquisar', command=lambda: self.pesquisar_transportador('')) \
            .grid(sticky="we", column=4, row=5, padx=5, pady=(0, 5))

        Label(self.tab_motorista, text="Pedido de frete").grid(sticky=W, column=0, row=6, padx=5)
        Entry(self.tab_motorista, textvariable=self.numero_pedido).grid(sticky="we", column=0, row=7, padx=5,
                                                                        ipady=1, pady=(0, 5), columnspan=5)

        self.dados_transportador_selecionado.set(self.TEXTO_DADOS_TRANPORTADOR)
        self.label_dados_transportadora = Label(self.tab_motorista, wraplength=540, font=(None, 8, 'bold'),
                                                textvariable=self.dados_transportador_selecionado)
        self.label_dados_transportadora.grid(sticky="we", column=0, row=8, padx=2, columnspan=5)
        self.label_dados_transportadora.configure(foreground="red")

    def criar_frame_veiculo(self):
        Label(self.tab_veiculo, text="Pesquisar").grid(sticky=W, column=0, row=3, padx=2)
        self.campo_pesquisa_veiculo = Entry(self.tab_veiculo, textvariable=self.pesquisa_veiculo)
        self.campo_pesquisa_veiculo.bind('<Return>', self.pesquisar_veiculo)
        self.campo_pesquisa_veiculo.bind("<KeyRelease>", self.pesquisar_veiculo)
        self.campo_pesquisa_veiculo.grid(sticky="we", column=0, row=4, padx=5, ipady=1, pady=(0, 5), columnspan=3)

        Button(self.tab_veiculo, text='Novo', command=self.cadastrar_novo_veiculo) \
            .grid(sticky="we", column=3, row=4, padx=5, pady=(0, 5))

        Button(self.tab_veiculo, text='Editar', command=self.editar_veiculo) \
            .grid(sticky="we", column=4, row=4, padx=5, pady=(0, 5))

        self.treeview_veiculo = Treeview(self.tab_veiculo, selectmode="browse", height=4,
                                         column=("c0", "c1", "c2", "c3", "c4", "c5", "c6", "c7"), show="headings")
        self.treeview_veiculo.heading("#1", text="ID")
        self.treeview_veiculo.heading("#2", text="Cavalo")
        self.treeview_veiculo.heading("#3", text="Carreta 1")
        self.treeview_veiculo.heading("#4", text="Carreta 2")
        self.treeview_veiculo.heading("#5", text="Carreta 3")
        self.treeview_veiculo.heading("#6", text="Tipo")
        self.treeview_veiculo.heading("#7", text="P. Bal")
        self.treeview_veiculo.heading("#8", text="Lacres")

        self.treeview_veiculo.column("c0", width=40, stretch=NO, anchor=CENTER)
        self.treeview_veiculo.column("c1", width=100, stretch=NO, anchor=CENTER)
        self.treeview_veiculo.column("c2", width=100, stretch=NO, anchor=CENTER)
        self.treeview_veiculo.column("c3", width=100, stretch=NO, anchor=CENTER)
        self.treeview_veiculo.column("c4", width=100, stretch=NO, anchor=CENTER)
        self.treeview_veiculo.column("c5", width=80, stretch=NO, anchor=CENTER)
        self.treeview_veiculo.column("c6", width=80, stretch=NO, anchor=CENTER)
        self.treeview_veiculo.column("c7", width=80, stretch=NO, anchor=CENTER)

        self.treeview_veiculo.grid(sticky=W, column=0, row=5, padx=5, columnspan=5)
        self.treeview_veiculo.bind("<Double-1>", self.setar_veiculo_selecionado)

        self.dados_veiculo_selecionado.set(self.TEXTO_DADOS_VEICULO)
        self.label_dados_veiculo_selecionado = Label(self.tab_veiculo, font=(None, 8, 'bold'),
                                                     textvariable=self.dados_veiculo_selecionado,
                                                     wraplength=450)
        self.label_dados_veiculo_selecionado.configure(foreground="red")
        self.label_dados_veiculo_selecionado.grid(sticky=W, column=0, row=7, padx=5, columnspan=5)

        Label(self.tab_veiculo, text='Código lacre').grid(sticky=W, row=8, padx=2)
        entry_codigo_lacres = Entry(self.tab_veiculo, textvariable=self.codigo_lacres)
        entry_codigo_lacres.grid(sticky="we", row=9, padx=5, ipady=1, pady=(0, 5), columnspan=3)
        entry_codigo_lacres.bind('<Return>', self.buscar_lacres)

        Button(self.tab_veiculo, text='Novo', command=self.cadastrar_lacres) \
            .grid(sticky="we", column=3, row=9, padx=5, pady=(0, 5))

        Button(self.tab_veiculo, text='Editar', command=self.editar_lacres) \
            .grid(sticky="we", column=4, row=9, padx=5, pady=(0, 5))

        self.label_quantidade_lacres.set("Lacres: (0)")
        Label(self.tab_veiculo, textvariable=self.label_quantidade_lacres).grid(sticky="we", column=0, row=10, padx=2)

        entrada_lacres = Entry(self.tab_veiculo, textvariable=self.lacres)
        entrada_lacres.grid(sticky="we", column=0, row=11, padx=2, columnspan=4, pady=(0, 5), ipady=1)
        entrada_lacres.bind("<KeyRelease>", self.contar_lacres)

        Button(self.tab_veiculo, text='Pesquisar', command=self.pesquisar_codigo_lacre) \
            .grid(sticky="we", column=4, row=11, padx=5, pady=(0, 5))

    def criar_frame_saida(self):

        self.frame_saida = LabelFrame(self.app_main, text="Saídas")
        self.frame_saida.grid(sticky="we", column=0, row=1, padx=10, pady=10)
        self.frame_saida.grid_columnconfigure(0, weight=1)

        Label(self.frame_saida, text="Remessa(s)").grid(sticky="we", column=0, row=0, padx=5)
        entry_remessas = Entry(self.frame_saida, textvariable=self.saida_remessas, state=DISABLED)
        entry_remessas.grid(sticky="we", row=1, padx=5)
        entry_remessas.bind("<Double-Button-1>", self.entrar_numero_remessa_manualmente)

        Label(self.frame_saida, text="Lote Inspecao Produto(89)").grid(sticky="we", column=0, row=2, padx=5)
        entry_numero_inspecao_produto = Entry(self.frame_saida, textvariable=self.saida_inpecao_produto, state=DISABLED)
        entry_numero_inspecao_produto.grid(sticky="we", row=3, padx=5)
        entry_numero_inspecao_produto.bind("<Double-Button-1>", self.entrar_numero_inspecao_produto_manualmente)

        Label(self.frame_saida, text="Transporte").grid(sticky="we", column=0, row=4, padx=5)
        entry_numero__transporte = Entry(self.frame_saida, textvariable=self.saida_transporte, state=DISABLED)
        entry_numero__transporte.grid(sticky="we", column=0, row=5, padx=5)
        entry_numero__transporte.bind("<Double-Button-1>", self.entrar_numero_transporte_manualmente)

        Label(self.frame_saida, text="Lote Inspecao Veicular(07)").grid(sticky="we", column=0, row=6, padx=5)
        entry_numero_inspecao_veiculo = Entry(self.frame_saida, textvariable=self.saida_inspecao_veiculo,
                                              state=DISABLED)
        entry_numero_inspecao_veiculo.grid(sticky="we", row=7, padx=5)
        entry_numero_inspecao_veiculo.bind("<Double-Button-1>", self.entrar_numero_inspecao_veiculo_manualmente)

        # rodapé
        botao_criar = Button(self.frame_saida, text='Criar', command=self.criar)
        botao_criar.grid(sticky="we", column=0, row=8, padx=5, pady=5)

    def atualizar_lista_produtos(self):
        p = ProdutoService.listar_produtos()
        self.cbo_produtos['values'] = tuple("{} - {}".format(prod.codigo_sap, prod.nome) for prod in p)

    def entrar_numero_remessa_manualmente(self, event):
        dialog = DialogoEntrada(self.app_main)
        dialog.inserir_texto(self.saida_remessas.get())
        self.app_main.wait_window(dialog.top)
        self.saida_remessas.set(dialog.entrada.get())

    def entrar_numero_inspecao_produto_manualmente(self, event):
        dialog = DialogoEntrada(self.app_main)
        dialog.inserir_texto(self.saida_inpecao_produto.get())
        self.app_main.wait_window(dialog.top)
        self.saida_inpecao_produto.set(dialog.entrada.get())

    def entrar_numero_transporte_manualmente(self, event):
        dialog = DialogoEntrada(self.app_main)
        dialog.inserir_texto(self.saida_transporte.get())
        self.app_main.wait_window(dialog.top)
        self.saida_transporte.set(dialog.entrada.get())

    def entrar_numero_inspecao_veiculo_manualmente(self, event):
        dialog = DialogoEntrada(self.app_main)
        dialog.inserir_texto(self.saida_inspecao_veiculo.get())
        self.app_main.wait_window(dialog.top)
        self.saida_inspecao_veiculo.set(dialog.entrada.get())

    def converter_pesquisa_placa_maiusculo(self, event):
        self.pesquisa_veiculo.set(self.pesquisa_veiculo.get().upper())

    def mudar_produto(self, event):
        codigo_produto = self.nome_produto.get().split("-")[0].strip()
        self.produto_selecionado = ProdutoService.pesquisar_produto_pelo_codigo(codigo_produto)
        if self.produto_selecionado is not None:
            ordem = self.produto_selecionado.numero_ordem
            pedido = self.produto_selecionado.pedido_frete

            self.ordem_item_remessa.set(ordem)
            self.numero_pedido.set(pedido)
            self.entry_quantidade_remessa.focus()

            try:
                self.transportador_selecionado = self.produto_selecionado.transportador
                self.setar_dados_transportador()
            except peewee.DoesNotExist:
                pass

    def cadastrar_novo_produto(self):
        cadastro = CadastroProduto(self.app_main)
        cadastro.app_main.transient(self.app_main)
        cadastro.app_main.focus_force()
        cadastro.app_main.grab_set()

    def pesquisar_ordens(self):
        pesquisa = ConsultaSaldo(self.app_main, self)
        pesquisa.app_main.transient(self.app_main)
        pesquisa.app_main.focus_force()
        pesquisa.app_main.grab_set()

    def editar_produto(self):
        if self.produto_selecionado is None:
            messagebox.showerror("Erro", "Selecione um produto!")
        else:
            cadastro = CadastroProduto(self.app_main)
            cadastro.app_main.transient(self.app_main)
            cadastro.app_main.focus_force()
            cadastro.app_main.grab_set()
            cadastro.setar_campos_para_edicao(self.produto_selecionado)
            cadastro.atualizando_cadastro = True

    def inserir_item_remessa(self, event):
        try:
            self.validar_novo_item_remesa()
            self.treeview_remessas.insert("", "end", values=(self.ordem_item_remessa.get().strip(),
                                                             self.produto_selecionado.codigo_sap.strip(),
                                                             self.quantidade_item_remessa.get().strip(),
                                                             self.produto_selecionado.deposito.strip(),
                                                             self.produto_selecionado.lote.strip()))
            self.calcular_total_itens_remessa(None)
            self.ordem_item_remessa.set('')
            self.quantidade_item_remessa.set('')

        except Exception as e:
            messagebox.showerror("Erro", e)

    def validar_novo_item_remesa(self):
        if self.produto_selecionado is None:
            self.cbo_produtos.focus()
            raise RuntimeError("selecione um produto!")

        if StringUtils.is_empty(self.ordem_item_remessa.get()):
            self.entry_ordem_remessa.focus()
            raise RuntimeError("Informe uma ordem ou pedido!")

        if StringUtils.is_empty(self.quantidade_item_remessa.get()):
            self.entry_quantidade_remessa.focus()
            raise RuntimeError("Informe a quantidade!")

        itens = self.treeview_remessas.get_children()
        for item in itens:
            cod_produto_item = self.treeview_remessas.item(item, "values")[1]
            ordem_item = self.treeview_remessas.item(item, "values")[0]
            num_ordem = self.ordem_item_remessa.get()

            if StringUtils.is_equal(cod_produto_item, self.produto_selecionado.codigo_sap) and \
                    StringUtils.is_equal(ordem_item, num_ordem):
                raise RuntimeError("Já existem um item inserido na ordem {} com o produto {}!"
                                   .format(num_ordem, cod_produto_item))

    def calcular_total_itens_remessa(self, event):
        print(self.total_itens_remessas.get())
        acum = 0
        itens = self.treeview_remessas.get_children()
        for item in itens:
            qtd = NumberUtils.str_para_float(self.treeview_remessas.item(item, "values")[2])
            acum += qtd
        self.total_acumulado_itens_remessas.set('{}'.format(NumberUtils.formatar_numero(acum)))

        texto_total = self.total_itens_remessas.get()
        total = NumberUtils.str_para_float(texto_total) if not StringUtils.is_empty(texto_total) else 0
        pend = total - acum

        if StringUtils.is_empty(texto_total):
            self.total_pendente_itens_remessas.set('0,000')

        elif len(itens) != 0:
            self.total_pendente_itens_remessas.set(NumberUtils.formatar_numero(pend))

        if pend > 0:
            self.entry_quantidade_pendente_remessas.configure(foreground="red")
        else:
            self.entry_quantidade_pendente_remessas.configure(foreground="black")

    def eliminar_item_remessas(self):
        selected_items = self.treeview_remessas.selection()
        if len(selected_items) == 0:
            messagebox.showerror("Erro", "Sem ítens para eliminar!")
            return
        for item in selected_items:
            self.treeview_remessas.delete(item)
        self.calcular_total_itens_remessa(None)

    def limpar_treeview_remessas(self):
        for item in self.treeview_remessas.get_children():
            self.treeview_remessas.delete(item)

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
        cadastro = CadastroMotorista(self.app_main)
        cadastro.app_main.transient(self.app_main)
        cadastro.app_main.focus_force()
        cadastro.app_main.grab_set()

    def editar_motorista(self):
        if self.motorista_selecionado is None:
            messagebox.showerror("Erro", "Selecione um motorista!")
        else:
            cadastro = CadastroMotorista(self.app_main)
            cadastro.app_main.transient(self.app_main)
            cadastro.app_main.focus_force()
            cadastro.app_main.grab_set()
            cadastro.setar_campos_para_edicao(self.motorista_selecionado)
            cadastro.atualizando_cadastro = True

    def pesquisar_motorista(self, event):
        criterio = self.pesquisa_motorista.get().strip()
        if criterio:
            self.limpar_treeview_motoristas()
            for motorista in MotoristaService.pesquisar_motorista(criterio):
                self.treeview_motorista.insert("", "end", values=(motorista.id,
                                                                  motorista.nome,
                                                                  motorista.cpf if motorista.cpf else "",
                                                                  motorista.cnh if motorista.cnh else "",
                                                                  motorista.rg if motorista.rg else ""))
        else:
            self.limpar_treeview_motoristas()

    def setar_motorista_selecionado(self, event):
        selection = self.treeview_motorista.selection()
        id_motorista = self.treeview_motorista.item(selection, "values")[0]
        self.motorista_selecionado = MotoristaService.pesquisar_motorista_pelo_id(int(id_motorista))
        self.label_dados_nome_motorista.configure(foreground="green")
        self.dados_motorista_selecionado.set("** {} - {} **"
                                             .format(id_motorista, self.motorista_selecionado.nome).upper())

    def limpar_treeview_motoristas(self):
        for item in self.treeview_motorista.get_children():
            self.treeview_motorista.delete(item)
        self.dados_motorista_selecionado.set(self.TEXTO_DADOS_MOTORISTA)
        self.label_dados_nome_motorista.configure(foreground="red")
        self.motorista_selecionado = None

    def pesquisar_transportador(self, event=None):
        try:
            criterio = self.texto_pesquisa_transportador.get().strip()
            tamanho_valido = len(criterio) == 14 or len(criterio) == 11 or len(criterio) == 7
            if not criterio and not tamanho_valido:
                messagebox.showerror("Erro", "Informe código válido! (CPF, CNPJ ou Código Trasnportador)")
                return

            self.transportador_selecionado = Main.pesquisar_transportador_no_banco(criterio)
            # se nao achar o transportador no banco de dados, ele busca diretamente no SAP.
            if self.transportador_selecionado is None:
                self.transportador_selecionado = Main.pesquisar_transportador_no_sap(criterio)
            self.setar_dados_transportador()

        except Exception as error:
            traceback.print_exc(file=sys.stdout)
            messagebox.showerror("Erro", error)

    def setar_dados_transportador(self):
        self.texto_pesquisa_transportador.set(self.transportador_selecionado.codigo_sap)
        self.dados_transportador_selecionado.set(str(self.transportador_selecionado).upper())
        self.label_dados_transportadora.configure(foreground="green")

    @staticmethod
    def pesquisar_transportador_no_banco(criterio):
        return TransportadorService.pesquisar_transportador(criterio)

    @staticmethod
    def pesquisar_transportador_no_sap(criterio):
        # session = SAPGuiApplication.connect()
        return XK03.pesquisar_transportador(None, criterio)

    def pesquisar_veiculo(self, event):
        criterio = self.pesquisa_veiculo.get().strip()
        if criterio:
            self.limpar_treeview_veiculos()
            for veiculo in VeiculoService.pesquisar_veiculo(criterio):
                self.treeview_veiculo.insert("", "end", values=(veiculo.id,
                                                                veiculo.placa1,
                                                                veiculo.placa2 if veiculo.placa2 else "",
                                                                veiculo.placa3 if veiculo.placa3 else "",
                                                                veiculo.placa4 if veiculo.placa4 else "",
                                                                veiculo.tipo_veiculo.descricao
                                                                if veiculo.tipo_veiculo else "",
                                                                veiculo.peso_balanca.descricao if
                                                                veiculo.peso_balanca else "",
                                                                veiculo.quantidade_lacres))
        else:
            self.limpar_treeview_veiculos()

    def limpar_treeview_veiculos(self):
        for item in self.treeview_veiculo.get_children():
            self.treeview_veiculo.delete(item)
        self.dados_veiculo_selecionado.set(self.TEXTO_DADOS_VEICULO)
        self.label_dados_veiculo_selecionado.configure(foreground="red")
        self.veiculo_selecionado = None

    def setar_veiculo_selecionado(self, event):
        selection = self.treeview_veiculo.selection()
        id_veiculo = self.treeview_veiculo.item(selection, "values")[0]
        self.veiculo_selecionado = VeiculoService.pesquisar_veiculo_pelo_id(int(id_veiculo))
        if self.veiculo_selecionado is not None:
            self.label_dados_veiculo_selecionado.configure(foreground="green")
            placa1 = self.veiculo_selecionado.placa1
            placa2 = self.veiculo_selecionado.placa2
            placa3 = self.veiculo_selecionado.placa3
            placa4 = self.veiculo_selecionado.placa4
            self.dados_veiculo_selecionado.set("** {} - {} {} {} {} **".format(id_veiculo,
                                                                               placa1 if placa1 is not None else '',
                                                                               placa2 if placa2 is not None else '',
                                                                               placa3 if placa3 is not None else '',
                                                                               placa4 if placa4 is not None else ''))

    def cadastrar_novo_veiculo(self):
        cadastro = CadastroVeiculo(self.app_main)
        cadastro.app_main.transient(self.app_main)
        cadastro.app_main.focus_force()
        cadastro.app_main.grab_set()

    def editar_veiculo(self):
        if self.veiculo_selecionado is None:
            messagebox.showerror("Erro", "Selecione um veículo!")
            return
        cadastro = CadastroVeiculo(self.app_main)
        cadastro.app_main.transient(self.app_main)
        cadastro.app_main.focus_force()
        cadastro.app_main.grab_set()
        cadastro.setar_campos_para_edicao(self.veiculo_selecionado)
        cadastro.atualizando_cadastro = True

    def cadastrar_lacres(self):
        cadastro = CadastroLacres(self.app_main)
        cadastro.app_main.transient(self.app_main)
        cadastro.app_main.focus_force()
        cadastro.app_main.grab_set()

    def editar_lacres(self):
        lacres = service.LacreService.pesquisar_pacote_lacres_pelo_codigo(self.codigo_lacres.get())
        if len(lacres) == 0:
            messagebox.showerror("Sem resultados", "Nenhum lacre encontrado para o código informado!")
            return

        cadastro = CadastroLacres(self.app_main)
        cadastro.app_main.transient(self.app_main)
        cadastro.app_main.focus_force()
        cadastro.app_main.grab_set()
        cadastro.setar_campos_para_edicao(lacres)
        cadastro.atualizando_cadastro = True

    def contar_lacres(self, event):
        lacres = self.lacres.get().strip()
        if lacres != "":
            lacres = lacres.split("/")
        self.label_quantidade_lacres.set("Lacres: ({})".format(str(len(lacres))))

    def buscar_lacres(self, event):
        self.lacres_selecionados = service.LacreService.pesquisar_pacote_lacres_pelo_codigo(self.codigo_lacres.get())
        if len(self.lacres_selecionados) == 0:
            messagebox.showerror("Sem resultados", "Nenhum lacre encontrado para o código informado!")
            self.lacres.set('')
            return
        cont = 0
        lacres = ""
        for lacre in self.lacres_selecionados:
            lacres += lacre.numero
            if cont < len(self.lacres_selecionados) - 1:
                lacres += '/'
            cont += 1
        self.lacres.set(lacres)
        self.contar_lacres(None)

    def pesquisar_codigo_lacre(self):
        numero_lacre = self.lacres.get().strip()
        if not numero_lacre:
            messagebox.showerror("Erro", "Informe um lacre!".format(numero_lacre))
            return
        lacre = service.LacreService.pesquisar_codigo_lacre(numero_lacre)
        if not lacre:
            messagebox.showerror("Sem resultados", "O lacre '{}' nao está cadastrado!".format(numero_lacre))
            return
        messagebox.showinfo("Código Lacre", "O lacre informado pertence ao pacote de número {}.".format(lacre.codigo))

    @staticmethod
    def trazer_janela_para_frente(janela):
        janela.attributes('-topmost', 1)
        janela.attributes('-topmost', 0)

    def criar(self):
        try:
            # self.validar_carregamento()

            # conectando ao SAP
            session = SAPGuiApplication.connect()
            SAPGuiElements.maximizar_janela(session)
            Main.trazer_janela_para_frente(self.app_main)

            # iniciando um novo carregamento
            self.carregamento_atual = Carregamento()

            # criando remessas
            self.carregamento_atual.remessas = self.criar_remessas(session)

            # criando lotes de controle do produto caso necessário
            inspecionar_produto = self.carregamento_atual.remessas[0].itens[0].produto.inspecao_produto == 1
            if inspecionar_produto:
                self.carregamento_atual.lotes_qualidade = \
                    self.criar_lotes_qualidade(session, self.carregamento_atual.remessas)

            self.carregamento_atual.codigo_transportador = self.codigo_transportador_selecionado.get()
            self.carregamento_atual.veiculo = self.veiculo_selecionado
            self.carregamento_atual.motorista = self.motorista_selecionado
            self.carregamento_atual.lacres = self.lacres.get()
            self.carregamento_atual.numero_pedido = self.numero_pedido.get()

            numero_transporte = Main.criar_transporte(session, self.carregamento_atual)
            # mostrando saida transporte
            self.saida_transporte.set(numero_transporte)
            self.app_main.update_idletasks()

            inspecionar_veiculo = self.carregamento_atual.remessas[0].itens[0].produto.inspecao_veiculo == 1
            if inspecionar_veiculo:
                resultado_inspecao_veicular = \
                    self.criar_lote_inspecao_veiculo(session,
                                                     numero_transporte,
                                                     self.carregamento_atual.veiculo.placa_1)

                # inserindo o lote de inspecao no transporte
                Main.inserir_lote_inspecao_transporte(session, numero_transporte, resultado_inspecao_veicular)

            messagebox.showinfo("Sucesso", "Carregamento criado com sucesso!")
            self.novo_carregamento()

        except Exception as error:
            traceback.print_exc(file=sys.stdout)
            messagebox.showerror("Erro", error)

    def validar_carregamento(self):
        if len(self.treeview_remessas.get_children()) == 0:
            raise RuntimeError("Insira ao menos um ítem para continuar!")

        if self.motorista_selecionado is None:
            raise RuntimeError("Selecione um motorista!")

        if not self.codigo_transportador_selecionado.get():
            raise RuntimeError("Selecione um transportador!")

        if self.veiculo_selecionado is None:
            raise RuntimeError("Selecione um veículo!")

    def criar_remessas(self, session):
        remessas = self.extrair_remessas()
        for remessa in remessas:
            try:
                numero_remessa = VL01.criar_remessa(session, remessa)
                remessa.numero_remessa = numero_remessa
                self.atualizar_saida_remessas(remessa.numero_remessa)
            except Exception as e:
                raise e

        return remessas

    def extrair_remessas(self):
        remessas = []
        dic_itens = {}
        childrens = self.treeview_remessas.get_children()

        for item in childrens:
            numero_ordem = self.treeview_remessas.item(item, "values")[0].strip()
            codigo_produto = self.treeview_remessas.item(item, "values")[1].strip()
            produto = ProdutoService.pesquisar_produto_pelo_codigo(codigo_produto)
            quantidade = self.treeview_remessas.item(item, "values")[2].strip()

            item_remessa = ItemRemessa()
            item_remessa.numero_ordem = numero_ordem
            item_remessa.quantidade = quantidade
            item_remessa.produto = produto

            # adicionando o item ao dicionário...
            dic_itens.setdefault(item_remessa.numero_ordem, []).append(item_remessa)

        for chave in dic_itens:
            remessas.append(Remessa(itens=dic_itens[chave]))

        return remessas

    def atualizar_saida_remessas(self, remessa):
        # atualizando a saída de remessas
        saida_remessa = self.saida_remessas.get().strip()
        self.saida_remessas.set('{}{}{}'.format(saida_remessa, '/' if saida_remessa else '', remessa))
        self.app_main.update_idletasks()

    def atualizar_saida_inspecao_produto(self, lote):
        # atualizando a saída de remessas
        saida_lote = self.saida_inpecao_produto.get().strip()
        self.saida_inpecao_produto.set('{} {} {}'.format(saida_lote, '/' if saida_lote else '', lote))
        self.app_main.update_idletasks()

    def criar_lotes_qualidade(self, session, remessas):
        lotes = []

        # verificando se o usuário inseriu os lotes manualmente
        if self.saida_inpecao_produto.get():
            # TODO criar um código para ir qa03, pegar o numero da remessa(texto breve), verificar a qual remessa
            # TODO pertence e continuar a execucao.
            pass

        for remessa in remessas:
            try:
                lote = Main.__gerar_lote_qualidade(remessa)
                numero_lote_criado = QA01.create(session, lote)
                lote.numero_lote = numero_lote_criado
                lotes.append(lote)

                # atualizando a saída de remessas
                self.atualizar_saida_inspecao_produto(numero_lote_criado)
            except Exception as e:
                raise e

        # se houver mais de uma remessa, será criado mais um lote usando a primeira remessa. Será usado no transporte.
        if len(remessas) > 1:
            try:
                lote = Main.__gerar_lote_qualidade(remessas[0])
                numero_ultimo_lote = QA01.create(session, lote)
                lote.numero_lote = numero_ultimo_lote
                lotes.append(lote)

                # atualizando a saída de remessas
                self.atualizar_saida_inspecao_produto(numero_ultimo_lote)
            except Exception as e:
                raise e

        return lotes

    @staticmethod
    def __gerar_lote_qualidade(remessa):
        lote = LoteInspecao()
        lote.material = remessa.itens[0].produto.codigo
        lote.origem = "89"
        lote.lote = remessa.itens[0].produto.lote
        lote.deposito = remessa.itens[0].produto.deposito
        lote.texto_breve = remessa.numero_remessa
        return lote

    @staticmethod
    def criar_transporte(session, carregamento):
        return VT01.create(session, carregamento)

    def criar_lote_inspecao_veiculo(self, sap_session, numero_transporte, placa_cavalo):
        produto = self.carregamento_atual.remessas[0].itens[0].produto
        lancar_s = False
        inspecao_veiculo = LoteInspecao()
        inspecao_veiculo.material = produto.tipo_inspecao_veiculo
        if inspecao_veiculo.material == 'INSPVEICALCOOL':
            lancar_s = True

        inspecao_veiculo.centro = "1014"
        inspecao_veiculo.origem = "07"
        inspecao_veiculo.lote = placa_cavalo
        inspecao_veiculo.texto_breve = numero_transporte
        numero_lote_insp_veiculo = QA01.create(sap_session, inspecao_veiculo)
        # mostrando saida lote de inspecao veiculo
        self.saida_inspecao_veiculo.set(numero_lote_insp_veiculo)
        self.app_main.update_idletasks()
        if lancar_s:
            QE01.criar(sap_session, numero_lote_insp_veiculo[1])
        return numero_lote_insp_veiculo

    @staticmethod
    def inserir_lote_inspecao_transporte(session, numero_transporte, numero_inspecao_veicular):
        return VT02.inserir_inspecao_veicular(session, numero_transporte, numero_inspecao_veicular)

    def novo_carregamento(self):
        self.carregamento_atual = None
        self.nome_produto.set('')
        self.produto_selecionado = None
        self.remessas = []
        self.limpar_treeview_remessas()

        self.motorista_selecionado = None
        self.limpar_treeview_motoristas()

        self.texto_pesquisa_transportador.set('')
        self.dados_transportador_selecionado.set('')

        self.numero_pedido.set('')

        self.pesquisa_veiculo.set('')
        self.veiculo_selecionado = None
        self.limpar_treeview_veiculos()

        self.codigo_lacres.set('')
        self.lacres.set('')
        self.dados_transportador_selecionado.set(self.TEXTO_DADOS_TRANPORTADOR)
        self.label_dados_transportadora.configure(foreground="red")
        self.label_quantidade_lacres.set("Lacres: (0)")

        self.saida_remessas.set('')
        self.saida_inpecao_produto.set('')
        self.saida_transporte.set('')
        self.saida_inspecao_veiculo.set('')


main = Main()
