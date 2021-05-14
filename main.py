import tkinter
from tkinter.ttk import *
from tkinter import W, DISABLED, messagebox, CENTER, NO, ttk
from win32api import MessageBox
from cadastro_motorista import CadastroMotorista
from cadastro_veiculo import CadastroVeiculo
from model import Motorista, Remessa, Carregamento, LoteInspecao
from dialogo_entrada import DialogoEntrada
from sapguielements import SAPGuiElements
from service import MotoristaService, VeiculoService, ProdutoService
import service
from utilitarios import StringUtils, NumberUtils
from cadastro_produto import CadastroProduto
from cadastro_lacres import CadastroLacres
from qa import QA01
from qe import QE01
from sapgui import SAPGuiApplication
from vl import VL01, VL03
from vt import VT01, VT02


class Main:

    def __init__(self):

        self.FORMATO_LABEL_TOTAL = "Qtd itens: {}  / Total: {}"
        self.app_main = tkinter.Tk()
        self.app_main.title("Utilitário de Faturamento")
        self.app_main.geometry('600x680')
        self.centralizar_tela()
        # self.app_main.configure(bg='#eaf1f6')


        self.janela_cadastro_lacres = None

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

    @staticmethod
    def criar_estilo():
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
        style.theme_use('Cloud')
        style.configure('.', font=('Helvetica', 10))

    def centralizar_tela(self):
        # Gets the requested values of the height and widht.
        window_width = self.app_main.winfo_reqwidth()
        window_height = self.app_main.winfo_reqheight()
        print("Width", window_width, "Height", window_height)

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
        Label(self.tab_remessa, text="Produto: ").grid(sticky=W, column=0, row=0, padx=2)
        self.cbo_produtos = Combobox(self.tab_remessa, textvariable=self.nome_produto, state="readonly",
                                     postcommand=self.atualizar_lista_produtos)
        self.cbo_produtos.bind('<<ComboboxSelected>>', self.mudar_produto)
        self.cbo_produtos.grid(sticky="we", column=0, row=1, padx=5, ipady=1, pady=(0, 5), columnspan=4)

        Button(self.tab_remessa, text='Novo', command=self.cadastrar_novo_produto) \
            .grid(sticky="we", column=4, row=1, padx=5, pady=(0, 5))

        Button(self.tab_remessa, text='Editar', command=self.editar_produto) \
            .grid(sticky="we", column=5, row=1, padx=5, pady=(0, 5))

        Label(self.tab_remessa, text="Ordem: ").grid(sticky=W, row=2, padx=2)
        self.entry_ordem_remessa = Entry(self.tab_remessa, textvariable=self.ordem_item_remessa)
        self.entry_ordem_remessa.grid(sticky="we", row=3, padx=5, ipady=1, pady=(0, 5), columnspan=2)
        self.entry_ordem_remessa.config(validate="key",
                                        validatecommand=(self.app_main.register(NumberUtils.eh_inteiro), '%P'))

        Label(self.tab_remessa, text="Quantidade: ").grid(sticky=W, column=2, row=2, padx=2)
        self.entry_quantidade_remessa = Entry(self.tab_remessa, textvariable=self.quantidade_item_remessa)
        self.entry_quantidade_remessa.grid(sticky="we", column=2, row=3, padx=5, ipady=1, pady=(0, 5), columnspan=2)
        self.entry_quantidade_remessa.config(validate="key",
                                             validatecommand=(self.app_main.register(NumberUtils.eh_decimal), '%P'))
        # self.entry_quantidade_remessa.bind('<KeyRelease>', self.mostrar_total_remessas)

        Button(self.tab_remessa, text='Adicionar ítem', command=self.inserir_item_remessa) \
            .grid(sticky="we", column=4, row=3, padx=5, pady=(0, 5))

        Button(self.tab_remessa, text='Remover ítem', command=self.eliminar_item_remessas) \
            .grid(sticky="we", column=5, row=3, padx=5, pady=(0, 5))

        self.treeview_remessas = Treeview(self.tab_remessa, height=4,
                                          column=("c0", "c1", "c2", "c3", "c4"), show="headings")
        self.treeview_remessas.heading("#1", text="Ordem")
        self.treeview_remessas.heading("#2", text="Produto")
        self.treeview_remessas.heading("#3", text="Quantidade")
        self.treeview_remessas.heading("#4", text="Deposito")
        self.treeview_remessas.heading("#5", text="Lote")

        self.treeview_remessas.column("c0", width=100, stretch=NO, anchor=CENTER)
        self.treeview_remessas.column("c1", width=140, stretch=NO, anchor=CENTER)
        self.treeview_remessas.column("c2", width=100, stretch=NO, anchor=CENTER)
        self.treeview_remessas.column("c3", width=100, stretch=NO, anchor=CENTER)
        self.treeview_remessas.column("c4", width=100, stretch=NO, anchor=CENTER)

        self.treeview_remessas.grid(sticky="we", column=0, row=4, padx=5, columnspan=6)

        Label(self.tab_remessa, text="Total: ").grid(sticky=W, column=0, row=5, padx=2)
        self.entry_quantidade_total_remessas = Entry(self.tab_remessa, textvariable=self.total_itens_remessas)
        self.entry_quantidade_total_remessas.grid(sticky="we", row=6, padx=5, ipady=1, pady=(0, 5), columnspan=2)
        self.entry_quantidade_total_remessas.config(validate="key",
                                                    validatecommand=(self.app_main.register(NumberUtils.eh_decimal),
                                                                     '%P'))
        self.entry_quantidade_total_remessas.bind("<KeyRelease>", self.calcular_total_itens_remessa)

        self.total_acumulado_itens_remessas.set("0,000")
        Label(self.tab_remessa, text="Acumulado: ").grid(sticky=W, column=2, row=5, padx=2)
        self.entry_quantidade_acumulada_remessas = Entry(self.tab_remessa, state="readonly",
                                                         textvariable=self.total_acumulado_itens_remessas)
        self.entry_quantidade_acumulada_remessas \
            .grid(sticky="we", column=2, row=6, padx=5, ipady=1, pady=(0, 5), columnspan=2)
        self.entry_quantidade_acumulada_remessas.config(validate="key", validatecommand=(
            self.app_main.register(NumberUtils.eh_decimal), '%P'))

        self.total_pendente_itens_remessas.set("0,000")
        Label(self.tab_remessa, text="Pendente: ").grid(sticky=W, column=4, row=5, padx=2)
        self.entry_quantidade_pendente_remessas = Entry(self.tab_remessa, state="readonly",
                                                        textvariable=self.total_pendente_itens_remessas)
        self.entry_quantidade_pendente_remessas \
            .grid(sticky="we", column=4, row=6, padx=5, ipady=1, pady=(0, 5), columnspan=2)
        self.entry_quantidade_pendente_remessas.config(validate="key",
                                                       validatecommand=(
                                                           self.app_main.register(NumberUtils.eh_decimal), '%P'))

    def criar_frame_motorista(self):

        Label(self.tab_motorista, text="Pesquisar motorista").grid(sticky=W, column=0, row=0, padx=2)
        self.txt_pesquisa_motorista = Entry(self.tab_motorista, textvariable=self.pesquisa_motorista)
        self.txt_pesquisa_motorista.grid(sticky="we", column=0, row=1, padx=5, ipady=1, pady=(0, 5), columnspan=2)
        # self.txt_pesquisa_motorista.bind('<Return>', self.pesquisar_motorista)
        self.txt_pesquisa_motorista.bind("<KeyRelease>", self.pesquisar_motorista)

        Button(self.tab_motorista, text='Novo', command=self.cadastrar_novo_motorista) \
            .grid(sticky="we", column=2, row=1, padx=2, pady=(0, 5))

        Button(self.tab_motorista, text='Editar', command=self.editar_motorista) \
            .grid(sticky="we", column=3, row=1, padx=2, pady=(0, 5))

        self.treeview_motorista = Treeview(self.tab_motorista, selectmode="browse", height=4,
                                           column=("c0", "c1", "c2", "c3", "c4"), show="headings")
        self.treeview_motorista.heading("#1", text="ID")
        self.treeview_motorista.heading("#2", text="Nome")
        self.treeview_motorista.heading("#3", text="CPF")
        self.treeview_motorista.heading("#4", text="CNH")
        self.treeview_motorista.heading("#5", text="RG")

        self.treeview_motorista.column("c0", width=40, stretch=NO, anchor=CENTER)
        self.treeview_motorista.column("c1", width=200, stretch=NO, anchor=CENTER)
        self.treeview_motorista.column("c2", width=100, stretch=NO, anchor=CENTER)
        self.treeview_motorista.column("c3", width=100, stretch=NO, anchor=CENTER)
        self.treeview_motorista.column("c4", width=100, stretch=NO, anchor=CENTER)

        self.treeview_motorista.grid(sticky=W, column=0, row=2, padx=5, columnspan=4)
        self.treeview_motorista.bind("<Double-1>", self.setar_motorista_selecionado)

        self.dados_motorista_selecionado.set(self.TEXTO_DADOS_MOTORISTA)
        self.label_dados_nome_motorista = Label(self.tab_motorista, textvariable=self.dados_motorista_selecionado,
                                                font=(None, 8, 'bold'), wraplength=450)
        self.label_dados_nome_motorista.grid(sticky=W, column=0, row=3, padx=5, columnspan=5)
        self.label_dados_nome_motorista.configure(foreground="red")

        # ---------------------

        Label(self.tab_motorista, text="Transportador", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=4,
                                                                                       padx=2)
        self.campo_pesquisa_veiculo = Entry(self.tab_motorista, textvariable=self.texto_pesquisa_transportador)
        self.campo_pesquisa_veiculo.bind('<Return>', self.pesquisar_transportador)
        self.campo_pesquisa_veiculo.grid(sticky="we", column=0, row=5, padx=2, ipady=1, pady=(0, 5), columnspan=3)

        Button(self.tab_motorista, text='Pesquisar', command=lambda: self.pesquisar_transportador('')) \
            .grid(sticky="we", column=3, row=5, padx=2, pady=(0, 5))

        Label(self.tab_motorista, text="Pedido").grid(sticky=W, column=0, row=6, padx=2)
        Entry(self.tab_motorista, textvariable=self.numero_pedido).grid(sticky=W, column=0, row=7, padx=5,
                                                                        ipady=1, pady=(0, 5))

        self.dados_transportador_selecionado.set(self.TEXTO_DADOS_TRANPORTADOR)
        self.label_dados_transportadora = Label(self.tab_motorista, wraplength=540, font=(None, 8, 'bold'),
                                                textvariable=self.dados_transportador_selecionado)
        self.label_dados_transportadora.grid(sticky="we", column=0, row=8, padx=2, columnspan=4)
        self.label_dados_transportadora.configure(foreground="red")

    def criar_frame_veiculo(self):
        Label(self.tab_veiculo, text="Pesquisar (Placa Cavalo)").grid(sticky=W, column=0, row=3, padx=2)
        self.campo_pesquisa_veiculo = Entry(self.tab_veiculo, textvariable=self.pesquisa_veiculo)
        self.campo_pesquisa_veiculo.bind('<Return>', self.pesquisar_veiculo)
        self.campo_pesquisa_veiculo.bind("<KeyRelease>", self.pesquisar_veiculo)
        self.campo_pesquisa_veiculo.grid(sticky="we", column=0, row=4, padx=5, ipady=1, pady=(0, 5), columnspan=2)

        Button(self.tab_veiculo, text='Novo', command=self.cadastrar_novo_veiculo) \
            .grid(sticky="we", column=2, row=4, padx=2, pady=(0, 5))

        Button(self.tab_veiculo, text='Editar', command=self.editar_veiculo) \
            .grid(sticky="we", column=3, row=4, padx=2, pady=(0, 5))

        self.treeview_veiculo = Treeview(self.tab_veiculo, selectmode="browse", height=4,
                                         column=("c0", "c1", "c2", "c3", "c4", "c5", "c6", "c7"), show="headings")
        self.treeview_veiculo.heading("#1", text="ID")
        self.treeview_veiculo.heading("#2", text="Cavalo")
        self.treeview_veiculo.heading("#3", text="Carreta 1")
        self.treeview_veiculo.heading("#4", text="Carreta 2")
        self.treeview_veiculo.heading("#5", text="Carreta 3")
        self.treeview_veiculo.heading("#6", text="Tipo")
        self.treeview_veiculo.heading("#7", text="P. Bal")
        self.treeview_veiculo.heading("#8", text="N. Lacres")

        self.treeview_veiculo.column("c0", width=40, stretch=NO, anchor=CENTER)
        self.treeview_veiculo.column("c1", width=80, stretch=NO, anchor=CENTER)
        self.treeview_veiculo.column("c2", width=80, stretch=NO, anchor=CENTER)
        self.treeview_veiculo.column("c3", width=80, stretch=NO, anchor=CENTER)
        self.treeview_veiculo.column("c4", width=80, stretch=NO, anchor=CENTER)
        self.treeview_veiculo.column("c5", width=60, stretch=NO, anchor=CENTER)
        self.treeview_veiculo.column("c6", width=60, stretch=NO, anchor=CENTER)
        self.treeview_veiculo.column("c7", width=60, stretch=NO, anchor=CENTER)

        self.treeview_veiculo.grid(sticky=W, column=0, row=5, padx=5, columnspan=4)
        self.treeview_veiculo.bind("<Double-1>", self.setar_veiculo_selecionado)

        self.dados_veiculo_selecionado.set(self.TEXTO_DADOS_VEICULO)
        self.label_dados_veiculo_selecionado = Label(self.tab_veiculo, font=(None, 8, 'bold'),
                                                     textvariable=self.dados_veiculo_selecionado,
                                                     wraplength=450)
        self.label_dados_veiculo_selecionado.configure(foreground="red")
        self.label_dados_veiculo_selecionado.grid(sticky=W, column=0, row=7, padx=5, columnspan=4)

        Label(self.tab_veiculo, text='Código lacre').grid(sticky=W, row=8, padx=2)
        entry_codigo_lacres = Entry(self.tab_veiculo, textvariable=self.codigo_lacres)
        entry_codigo_lacres.grid(sticky="we", row=9, padx=5, ipady=1, pady=(0, 5), columnspan=2)
        entry_codigo_lacres.bind('<Return>', self.buscar_lacres)

        Button(self.tab_veiculo, text='Novo', command=self.cadastrar_lacres) \
            .grid(sticky="we", column=2, row=9, padx=2, pady=(0, 5))

        Button(self.tab_veiculo, text='Editar', command=self.editar_lacres) \
            .grid(sticky="we", column=3, row=9, padx=2, pady=(0, 5))

        self.label_quantidade_lacres.set("Lacres: (0)")
        Label(self.tab_veiculo, textvariable=self.label_quantidade_lacres).grid(sticky="we", column=0, row=10, padx=2)

        entrada_lacres = Entry(self.tab_veiculo, textvariable=self.lacres)
        entrada_lacres.grid(sticky="we", column=0, row=11, padx=5, columnspan=6, pady=(0, 5), ipady=1)
        entrada_lacres.bind("<KeyRelease>", self.contar_lacres)

    def criar_frame_saida(self):

        self.frame_saida = LabelFrame(self.app_main, text="Saídas")
        self.frame_saida.grid(sticky="we", column=0, row=1, padx=10, pady=10)
        self.frame_saida.grid_columnconfigure(0, weight=1)

        Label(self.frame_saida, text="Remessa(s)").grid(sticky="we", column=0, row=0, padx=2)
        entry_remessas = Entry(self.frame_saida, textvariable=self.saida_remessas, state=DISABLED)
        entry_remessas.grid(sticky="we", row=1, padx=5)
        entry_remessas.bind("<Double-Button-1>", self.entrar_numero_remessa_manualmente)

        Label(self.frame_saida, text="Lote Inspecao Produto(89)").grid(sticky="we", column=0, row=2, padx=2)
        entry_numero_inspecao_produto = Entry(self.frame_saida, textvariable=self.saida_inpecao_produto, state=DISABLED)
        entry_numero_inspecao_produto.grid(sticky="we", row=3, padx=5)
        entry_numero_inspecao_produto.bind("<Double-Button-1>", self.entrar_numero_inspecao_produto_manualmente)

        Label(self.frame_saida, text="Transporte").grid(sticky="we", column=0, row=4, padx=2)
        entry_numero__transporte = Entry(self.frame_saida, textvariable=self.saida_transporte, state=DISABLED)
        entry_numero__transporte.grid(sticky="we", column=0, row=5, padx=5)
        entry_numero__transporte.bind("<Double-Button-1>", self.entrar_numero_transporte_manualmente)

        Label(self.frame_saida, text="Lote Inspecao Veicular(07)").grid(sticky="we", column=0, row=6, padx=2)
        entry_numero_inspecao_veiculo = Entry(self.frame_saida, textvariable=self.saida_inspecao_veiculo,
                                              state=DISABLED)
        entry_numero_inspecao_veiculo.grid(sticky="we", row=7, padx=5)
        entry_numero_inspecao_veiculo.bind("<Double-Button-1>", self.entrar_numero_inspecao_veiculo_manualmente)

        # rodapé
        botao_criar = Button(self.frame_saida, text='Criar', command=self.criar)
        botao_criar.grid(sticky="we", column=0, row=8, padx=5, pady=5)

    def atualizar_lista_produtos(self):
        p = service.ProdutoService.listar_produtos()
        self.cbo_produtos['values'] = tuple("{} - {}".format(prod.codigo, prod.nome) for prod in p)

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
        self.dados_produto.set(self.produto_selecionado)

    def cadastrar_novo_produto(self):
        CadastroProduto(self.app_main)

    def editar_produto(self):
        if self.produto_selecionado is None:
            messagebox.showerror("Erro", "Selecione um produto!")
        else:
            novo_produto = CadastroProduto(self.app_main)
            novo_produto.setar_campos_para_edicao(self.produto_selecionado)
            novo_produto.atualizando_cadastro = True

    def inserir_item_remessa(self):
        if self.validar_novo_item_remesa():
            self.treeview_remessas.insert("", "end", values=(self.ordem_item_remessa.get().strip(),
                                                             self.produto_selecionado.codigo.strip(),
                                                             self.quantidade_item_remessa.get().strip(),
                                                             self.produto_selecionado.deposito.strip(),
                                                             self.produto_selecionado.lote.strip()))
            self.calcular_total_itens_remessa(None)
            self.ordem_item_remessa.set('')
            self.quantidade_item_remessa.set('')

    def validar_novo_item_remesa(self):
        if self.produto_selecionado is None:
            self.cbo_produtos.focus()
            messagebox.showerror("Erro", "selecione um produto!")
            return False
        if StringUtils.is_empty(self.ordem_item_remessa.get()):
            self.entry_ordem_remessa.focus()
            messagebox.showerror("Erro", "Informe uma ordem ou pedido!")
            return False
        if StringUtils.is_empty(self.quantidade_item_remessa.get()):
            self.entry_quantidade_remessa.focus()
            messagebox.showerror("Erro", "Informe a quantidade!")
            return False
        return True

    def calcular_total_itens_remessa(self, event):
        acum = 0
        itens = self.treeview_remessas.get_children()
        for item in itens:
            qtd = NumberUtils.str_para_float(self.treeview_remessas.item(item, "values")[2])
            acum += qtd
        self.total_acumulado_itens_remessas.set('{}'.format(NumberUtils.formatar_numero(acum)))

        texto_total = self.total_itens_remessas.get()
        total = NumberUtils.str_para_float(texto_total) if not StringUtils.is_empty(texto_total) else 0
        pend = total - acum
        if pend > 0:
            self.entry_quantidade_pendente_remessas.configure(foreground="red")
        else:
            self.entry_quantidade_pendente_remessas.configure(foreground="black")

        if not StringUtils.is_empty(texto_total) or len(itens) == 0:
            self.total_pendente_itens_remessas.set(NumberUtils.formatar_numero(pend))

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
                self.treeview_motorista.insert("", "end", values=(motorista.id_motorista,
                                                                  motorista.nome,
                                                                  motorista.cpf if motorista.cpf else "",
                                                                  motorista.cnh if motorista.cnh else "",
                                                                  motorista.rg if motorista.rg else ""))
        else:
            self.limpar_treeview_motoristas()

    def setar_motorista_selecionado(self, event):
        selection = self.treeview_motorista.selection()
        id_motorista = self.treeview_motorista.item(selection, "values")[0]
        nome = self.treeview_motorista.item(selection, "values")[1]
        cpf = self.treeview_motorista.item(selection, "values")[2]
        cnh = self.treeview_motorista.item(selection, "values")[3]
        rg = self.treeview_motorista.item(selection, "values")[4]
        self.motorista_selecionado = Motorista(id_motorista=id_motorista,
                                               nome=nome,
                                               cpf=cpf,
                                               cnh=cnh,
                                               rg=rg)
        self.label_dados_nome_motorista.configure(foreground="green")
        self.dados_motorista_selecionado.set("** {} - {} **".format(id_motorista, nome).upper())

    def limpar_treeview_motoristas(self):
        for item in self.treeview_motorista.get_children():
            self.treeview_motorista.delete(item)
        self.dados_motorista_selecionado.set(self.TEXTO_DADOS_MOTORISTA)
        self.label_dados_nome_motorista.configure(foreground="red")
        self.motorista_selecionado = None

    def pesquisar_transportador(self, event):
        try:
            pesquisa = self.texto_pesquisa_transportador.get().strip()
            tamanho_pesquisa = len(pesquisa)
            if pesquisa and (tamanho_pesquisa == 14 or tamanho_pesquisa == 11 or tamanho_pesquisa == 7) \
                    and pesquisa.isdigit():

                session = SAPGuiApplication.connect()

                transportador = VT01.pesquisar_transportador(session, self.texto_pesquisa_transportador.get())
                if transportador[0]:
                    codigo = transportador[1]
                    endereco = transportador[2]
                    self.codigo_transportador_selecionado.set(codigo)
                    self.dados_transportador_selecionado.set("({}) - {}".format(codigo, endereco))
                    self.label_dados_transportadora.configure(foreground="green")
                else:
                    self.dados_transportador_selecionado.set("")
                    MessageBox(None, "Transportador não encontrado!")
            else:
                MessageBox(None, "Informe código válido! (CPF, CNPJ ou Código Trasnportador)")

        except Exception as error:
            messagebox.showerror("Erro", error)

    def pesquisar_veiculo(self, event):
        criterio = self.pesquisa_veiculo.get().strip()
        if criterio:
            self.limpar_treeview_veiculos()
            for veiculo in VeiculoService.pesquisar_veiculo(criterio):
                self.treeview_veiculo.insert("", "end", values=(veiculo.id_veiculo,
                                                                veiculo.placa_1,
                                                                veiculo.placa_2 if veiculo.placa_2 else "",
                                                                veiculo.placa_3 if veiculo.placa_3 else "",
                                                                veiculo.placa_4 if veiculo.placa_4 else "",
                                                                veiculo.tipo_veiculo if veiculo.tipo_veiculo else "",
                                                                veiculo.tolerancia_balanca if
                                                                veiculo.tolerancia_balanca else "",
                                                                veiculo.quantidade_lacres if
                                                                veiculo.quantidade_lacres else ""))
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
        self.veiculo_selecionado = VeiculoService.pesquisar_veiculo_pelo_id(id_veiculo)
        self.label_dados_veiculo_selecionado.configure(foreground="green")
        self.dados_veiculo_selecionado.set("** {} - {} {} {} {} **".format(id_veiculo, self.veiculo_selecionado.placa_1,
                                                                           self.veiculo_selecionado.placa_2,
                                                                           self.veiculo_selecionado.placa_3,
                                                                           self.veiculo_selecionado.placa_4))

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

    @staticmethod
    def trazer_janela_para_frente(janela):
        janela.attributes('-topmost', 1)
        janela.attributes('-topmost', 0)

    def criar(self):
        try:

            # self.validar_carregamento()

            carregamento = Carregamento()
            remessas = None
            lotes_inspecao_produto = None
            resultado_transporte = None
            resultado_inspecao_veicular = None
            resultado_lancar_s_inspecao_veicular = None

            # conectando ao SAP
            session = SAPGuiApplication.connect()
            SAPGuiElements.maximizar_janela(session)
            Main.trazer_janela_para_frente(self.app_main)

            # criando remessas
            carregamento.remessas = self.criar_remessas(session)
            return

            # criando lotes de controle do produto caso necessário
            if carregamento.remessas[0].produto.inspecao_produto == 1:
                carregamento.lotes_qualidade = self.criar_lotes_qualidade(session, carregamento.remessas)

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

            # mostrando saida transporte
            self.saida_transporte.set(resultado_transporte[1])
            self.app_main.update_idletasks()

            if carregamento.produto.inspecao_veiculo == 1:
                resultado_inspecao_veicular = self.criar_lote_inspecao_veiculo(session,
                                                                               carregamento.produto.codigo,
                                                                               carregamento.veiculo.placa_1,
                                                                               resultado_transporte[1])
                if not resultado_inspecao_veicular[0]:
                    messagebox.showerror("Erro", resultado_inspecao_veicular[1])
                    return

                # inserindo o lote de inspecao no transporte
                self.inserir_lote_inspecao_transporte(session, resultado_transporte[1], resultado_inspecao_veicular[1])

                # mostrando saida lote de inspecao veiculo
                self.saida_inspecao_veiculo.set(resultado_inspecao_veicular[1])
                self.app_main.update_idletasks()

            messagebox.showinfo("Sucesso", "Carregamento criado com sucesso!")
            self.novo_carregamento()

        except Exception as error:
            messagebox.showerror("Erro", error)

        finally:
            self.remessas = []

    def validar_carregamento(self):
        if len(self.treeview_remessas.get_children()) == 0:
            raise RuntimeError("Informe uma remessa!")

        if self.motorista_selecionado is None:
            raise RuntimeError("Selecione um motorista!")

        if self.codigo_transportador_selecionado is None:
            raise RuntimeError("Selecione um transportador!")

        if self.veiculo_selecionado is None:
            raise RuntimeError("Selecione um veículo!")

    # TODO mudar aqui...mesmo que o usuário informe a remessa manualmente, o sistema precisa ir na VL03 e verificar o
    # TODO o produto
    def criar_remessas(self, session):
        remessas = []
        if self.saida_remessas.get():
            numero_remessas_informadas = self.saida_remessas.get().split("/")
            for numero_remessa in numero_remessas_informadas:
                # TODO mudar aqui para buscar as informacoes da remessa direto na vl03
                remessas.append(VL03.gerar_produto_remessa_pronta(session, numero_remessa))
                for item in remessas[0].itens:
                    print(item)

            return remessas

        remessas = self.extrair_remessas()
        for numero_remessa in remessas:
            try:
                numero_remessa = VL01.create(session, numero_remessa)
                numero_remessa.numero_remessa = numero_remessa

                # atualizando a saída de remessas
                saida_remessa = self.saida_remessas.get()
                self.saida_remessas.set('{} / {}'.format(saida_remessa, numero_remessa))
                self.app_main.update_idletasks()

            except Exception as e:
                raise e

        return remessas

    def extrair_remessas(self):
        remessas = []
        itens = self.treeview_remessas.get_children()
        for item in itens:
            numero_ordem = self.treeview_remessas.item(item, "values")[0].strip()
            codigo_produto = self.treeview_remessas.item(item, "values")[1].strip()
            produto = ProdutoService.pesquisar_produto_pelo_codigo(codigo_produto)
            quantidade = self.treeview_remessas.item(item, "values")[2].strip()
            remessas.append(Remessa(numero_ordem, quantidade, produto))
        return remessas

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
                saida_lote_produto = self.saida_inpecao_produto.get()
                self.saida_inpecao_produto.set('{} / {}'.format(saida_lote_produto, numero_lote_criado))
                self.app_main.update_idletasks()

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
                saida_lote_produto = self.saida_inpecao_produto.get()
                self.saida_inpecao_produto.set('{} / {}'.format(saida_lote_produto, numero_ultimo_lote))
                self.app_main.update_idletasks()
            except Exception as e:
                raise e

        return lotes

    @staticmethod
    def __gerar_lote_qualidade(remessa):
        lote = LoteInspecao()
        lote.material = remessa.produto.codigo
        lote.origem = "89"
        lote.lote = remessa.produto.lote
        lote.deposito = remessa.produto.deposito
        lote.texto_breve = remessa.numero_remessa
        return lote

    def criar_transporte(self, session, carregamento):
        resultado = VT01.create(session, carregamento)
        if resultado[0]:
            self.inserir_saida("Transporte {} criado...".format(resultado[1]))
        return resultado

    def inserir_saida(self, info):
        pass

    def criar_lote_inspecao_veiculo(self, sap_session, codigo_produto, lote, texto_breve):
        inspecao_veiculo = LoteInspecao()
        lancar_s = False
        if codigo_produto[0] == "1":
            inspecao_veiculo.material = "INSPVEICALCOOL"
            lancar_s = True
        elif codigo_produto[0] == "3":
            inspecao_veiculo.material = "INSPVEICACUCAR"

        inspecao_veiculo.centro = "1014"
        inspecao_veiculo.origem = "07"
        inspecao_veiculo.lote = lote
        inspecao_veiculo.texto_breve = texto_breve
        resultado = QA01.create(sap_session, inspecao_veiculo)
        if resultado[0]:
            self.inserir_saida("Lote {} criado...".format(resultado[1]))
            if lancar_s:
                resultado_lancar_s = QE01.criar(sap_session, resultado[1])
                if resultado_lancar_s[0]:
                    self.inserir_saida("Resultados lançados para lote {} ...".format(resultado[1]))
                else:
                    self.inserir_saida("Erro ao lançar resultados para lote {} ...".format(resultado[1]))
        return resultado

    def inserir_lote_inspecao_transporte(self, session, numero_transporte, numero_inspecao_veicular):
        return VT02.inserir_inspecao_veicular(session, numero_transporte, numero_inspecao_veicular)

    def novo_carregamento(self):
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
