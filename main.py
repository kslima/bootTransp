import re
import tkinter
from tkinter.ttk import *
from tkinter import W, DISABLED, messagebox, CENTER, NO, ttk, StringVar
from win32api import MessageBox
from cadastro_motorista import CadastroMotorista
from cadastro_tipo_carregamento import CadastroTipoCarregamento
from cadastro_veiculo import CadastroVeiculo
from model import Motorista, Remessa, Carregamento, LoteInspecao, ItemRemessa
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
import sys, traceback


class Main:

    def __init__(self):

        self.FORMATO_LABEL_TOTAL = "Qtd itens: {}  / Total: {}"
        self.app_main = tkinter.Tk()
        self.app_main.title("Utilitário de Faturamento")
        self.app_main.geometry('600x680')
        self.centralizar_tela()
        # self.app_main.configure(bg='#eaf1f6')

        self.janela_cadastro_lacres = None
        self.carregamento_atual = None

        self.tipo_carregamento = StringVar()
        self.cbo_tipo_carregamento = None

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

        self.tipo_carregamento_selecionado = None
        self.produto_selecionado = None
        self.lacres_selecionados = None
        self.remessas = []
        self.dados_produto = StringVar()
        self.nome_produto = StringVar()
        self.amount = StringVar()

        self.ov = StringVar()
        self.total_itens_remessas = StringVar()
        self.msg = StringVar()

        self.saida_remessas = StringVar()
        self.saida_inpecao_produto = StringVar()
        self.saida_transporte = StringVar()
        self.saida_inspecao_veiculo = StringVar()

        self.dados_motorista_selecionado = StringVar()
        self.cpf = StringVar()
        self.cnh = StringVar()
        self.rg = StringVar()
        self.txt_pesquisa_motorista = StringVar()
        self.motorista_selecionado = None

        self.codigo_lacres = StringVar()
        self.lacres = StringVar()
        self.pesquisa_veiculo = StringVar()
        self.lista_veiculos = []
        self.veiculo_selecionado = None

        self.label_quantidade_lacres = StringVar()
        self.dados_veiculo_selecionado = StringVar()
        self.pesquisa_motorista = StringVar()

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
        self.texto_pesquisa_transportador = StringVar()
        self.dados_transportador_selecionado = StringVar()
        self.codigo_transportador_selecionado = StringVar()
        self.numero_pedido = StringVar()
        self.ordem_item_remessa = StringVar()
        self.quantidade_item_remessa = StringVar()
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

        # dados saída
        self.frame_saida = None
        self.popup = None
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

        Label(self.tab_remessa, text="Tipo Carregamento: ").grid(sticky=W, column=0, row=0, padx=2)
        self.cbo_tipo_carregamento = Combobox(self.tab_remessa, textvariable=self.tipo_carregamento, state="readonly",
                                              postcommand=self.atualizar_lista_tipos_carregamento)
        self.cbo_tipo_carregamento.bind('<<ComboboxSelected>>', self.mudar_tipo_carregamento)
        self.cbo_tipo_carregamento.grid(sticky="we", column=0, row=1, padx=5, ipady=1, pady=(0, 5), columnspan=4)

        Button(self.tab_remessa, text='Novo', command=self.cadastrar_novo_tipo_carregamento) \
            .grid(sticky="we", column=4, row=1, padx=5, pady=(0, 5))

        Button(self.tab_remessa, text='Editar', command=self.editar_tipo_carregamento) \
            .grid(sticky="we", column=5, row=1, padx=5, pady=(0, 5))

        self.treeview_remessas = Treeview(self.tab_remessa, height=4,
                                          column=("c0", "c1", "c2", "c3", "c4"), show="headings")
        self.treeview_remessas.bind("<<TreeviewSelect>>", self.editar_item_remessa)
        self.treeview_remessas.bind("<Button-3>", self.exibir_pop_up_remessas)
        self.treeview_remessas.heading("#1", text="Produto")
        self.treeview_remessas.heading("#2", text="Deposito")
        self.treeview_remessas.heading("#3", text="Lote")
        self.treeview_remessas.heading("#4", text="Ordem/Pedido")
        self.treeview_remessas.heading("#5", text="Quantidade")

        self.treeview_remessas.column("c0", width=200, stretch=NO, anchor=CENTER)
        self.treeview_remessas.column("c1", width=80, stretch=NO, anchor=CENTER)
        self.treeview_remessas.column("c2", width=80, stretch=NO, anchor=CENTER)
        self.treeview_remessas.column("c3", width=100, stretch=NO, anchor=CENTER)
        self.treeview_remessas.column("c4", width=80, stretch=NO, anchor=CENTER)

        self.treeview_remessas.grid(sticky="we", column=0, row=2, padx=5, columnspan=6)

        self.popup = tkinter.Menu(self.app_main, tearoff=0)
        self.popup.add_command(label="Somar ítens selecionados", command=self.somar_itens_remessa)
        self.popup.add_command(label="Calcular quantidade pendente", command=self.somar_itens_remessa)
        self.popup.add_separator()

        Button(self.tab_remessa, text='Adicionar ítem', command=self.inserir_item_remessa) \
            .grid(sticky="we", column=4, row=4, padx=5, pady=(0, 5))

        Button(self.tab_remessa, text='Remover ítem', command=self.eliminar_item_remessas) \
            .grid(sticky="we", column=5, row=4, padx=5, pady=(0, 5))

        Label(self.tab_remessa, text="Ordem/Pedido: ").grid(sticky=W, row=3, padx=2)
        self.entry_ordem_remessa = Entry(self.tab_remessa, textvariable=self.ordem_item_remessa)
        self.entry_ordem_remessa.grid(sticky="we", row=4, padx=(5, 2), ipady=1, pady=(0, 5))
        self.entry_ordem_remessa.config(validate="key",
                                        validatecommand=(self.app_main.register(NumberUtils.eh_inteiro), '%P'))
        self.entry_ordem_remessa.bind('<KeyRelease>', self.editar_numero_ordem_item_selecionado)

        Label(self.tab_remessa, text="Quantidade: ").grid(sticky=W, column=1, row=3, padx=2)
        self.entry_quantidade_remessa = Entry(self.tab_remessa, textvariable=self.quantidade_item_remessa)
        self.entry_quantidade_remessa.grid(sticky="we", column=1, row=4, padx=5, ipady=1, pady=(0, 5))
        self.entry_quantidade_remessa.config(validate="key",
                                             validatecommand=(self.app_main.register(NumberUtils.eh_decimal), '%P'))
        self.entry_quantidade_remessa.bind('<KeyRelease>', self.editar_quantidade_item_selecionado)

        Button(self.tab_remessa, text='Pesquisar ordem', command=self.inserir_item_remessa, state='disable') \
            .grid(sticky="we", column=2, row=4, padx=5, pady=(0, 5))

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

    def exibir_pop_up_remessas(self, event):
        selecionado = self.treeview_remessas.focus()
        if selecionado:
            try:
                self.popup.selection = self.treeview_remessas.set(self.treeview_remessas.identify_row(event.y))
                self.popup.post(event.x_root, event.y_root)
            finally:
                # make sure to release the grab (Tk 8.0a1 only)
                self.popup.grab_release()

    def somar_itens_remessa(self):
        childrens = self.treeview_remessas.get_children()
        soma = 0
        for item in childrens:
            quantidade = self.treeview_remessas.item(item, "values")[4].strip()
            soma += NumberUtils.str_para_float(quantidade)
        messagebox.showinfo("Resultado soma", "A soma dos ítens é {}".format(NumberUtils.formatar_numero(soma)))

    def atualizar_lista_tipos_carregamento(self):
        tc_lista = service.TipoCarregamentoService.listar_tipos_carregamento()
        self.cbo_tipo_carregamento['values'] = tuple("{} - {}".format(tc.id_tipo_carregamento,
                                                                      tc.nome) for tc in tc_lista)

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

    def mudar_tipo_carregamento(self, event):
        self.limpar_treeview_remessas()
        self.inserir_item_remessa()

    def extrair_produtos_por_tipo_carregamento(self):
        codigos_produtos = []
        r = re.compile(r'\[(.*?)]')
        for match in r.finditer(self.tipo_carregamento_selecionado.itens_str):
            codigos_produtos.append(match.group(1).split(";")[0])
        return codigos_produtos

    def mudar_produto(self, event):
        codigo_produto = self.nome_produto.get().split("-")[0].strip()
        self.produto_selecionado = ProdutoService.pesquisar_produto_pelo_codigo(codigo_produto)
        self.dados_produto.set(self.produto_selecionado)

    def cadastrar_novo_tipo_carregamento(self):
        cadastro = CadastroTipoCarregamento(self.app_main)
        cadastro.app_main.transient(self.app_main)
        cadastro.app_main.focus_force()
        cadastro.app_main.grab_set()

    def editar_tipo_carregamento(self):
        if self.produto_selecionado is None:
            messagebox.showerror("Erro", "Selecione um tipo de carregamento!")
        else:
            cadastro = CadastroTipoCarregamento(self.app_main)
            cadastro.app_main.transient(self.app_main)
            cadastro.app_main.focus_force()
            cadastro.app_main.grab_set()
            # cadastro.setar_campos_para_edicao(lacres)
            cadastro.atualizando_cadastro = True

    def inserir_item_remessa(self):
        _id = self.tipo_carregamento.get().split('-')[0]
        self.tipo_carregamento_selecionado = service.TipoCarregamentoService.pesquisar_tipo_carregamento(_id)
        produtos = []
        codigos_produtos = self.extrair_produtos_por_tipo_carregamento()
        for codigo in codigos_produtos:
            produtos.append(ProdutoService.pesquisar_produto_pelo_codigo(codigo))

        for produto in produtos:
            ordem = self.tipo_carregamento_selecionado.numero_ordem
            if self.validar_novo_item_remesa():
                self.treeview_remessas.insert("", "end", values=(produto.codigo.strip(),
                                                                 produto.deposito.strip() if produto.deposito.strip()
                                                                 else '-',
                                                                 produto.lote.strip() if produto.lote.strip() else '-',
                                                                 ordem if ordem else '-',
                                                                 '-'))

    def editar_item_remessa(self, event):
        selecionado = self.treeview_remessas.focus()
        if selecionado:
            ordem = self.treeview_remessas.item(selecionado, "values")[3].strip()
            quantidade = self.treeview_remessas.item(selecionado, "values")[4].strip()
            self.ordem_item_remessa.set(ordem if ordem != '-' else '')
            self.quantidade_item_remessa.set(quantidade if quantidade != '-' else '')
            self.entry_ordem_remessa.focus_set()

    def editar_numero_ordem_item_selecionado(self, event):
        selecionado = self.treeview_remessas.focus()
        if selecionado:
            produto = self.treeview_remessas.item(selecionado, "values")[0].strip()
            deposito = self.treeview_remessas.item(selecionado, "values")[1].strip()
            lote = self.treeview_remessas.item(selecionado, "values")[2].strip()
            quantidade = self.treeview_remessas.item(selecionado, "values")[4].strip()
            self.treeview_remessas.item(selecionado, values=(produto, deposito, lote, self.ordem_item_remessa.get(),
                                                             quantidade))

    def editar_quantidade_item_selecionado(self, event):
        selecionado = self.treeview_remessas.focus()
        if selecionado:
            produto = self.treeview_remessas.item(selecionado, "values")[0].strip()
            deposito = self.treeview_remessas.item(selecionado, "values")[1].strip()
            lote = self.treeview_remessas.item(selecionado, "values")[2].strip()
            ordem = self.treeview_remessas.item(selecionado, "values")[3].strip()
            self.treeview_remessas.item(selecionado, values=(produto, deposito, lote, ordem,
                                                             self.quantidade_item_remessa.get()))

    def validar_novo_item_remesa(self):
        '''
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
        '''
        return True

    def eliminar_item_remessas(self):
        selected_items = self.treeview_remessas.selection()
        if len(selected_items) == 0:
            messagebox.showerror("Erro", "Sem ítens para eliminar!")
            return
        for item in selected_items:
            self.treeview_remessas.delete(item)
        # self.calcular_total_itens_remessa(None)

    def limpar_treeview_remessas(self):
        for item in self.treeview_remessas.get_children():
            self.treeview_remessas.delete(item)

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
            # TODO colocar aqui a validacao

            # conectando ao SAP
            session = SAPGuiApplication.connect()
            SAPGuiElements.maximizar_janela(session)
            Main.trazer_janela_para_frente(self.app_main)

            # iniciando um novo carregamento
            self.carregamento_atual = Carregamento()

            # criando remessas
            self.carregamento_atual.remessas = self.criar_remessas(session)

            return
            # criando lotes de controle do produto caso necessário
            if self.carregamento_atual.remessas[0].produto.inspecao_produto == 1:
                self.carregamento_atual.lotes_qualidade = self.criar_lotes_qualidade(session,
                                                                                     self.carregamento_atual.remessas)

            self.carregamento_atual.codigo_transportador = self.codigo_transportador_selecionado.get()
            self.carregamento_atual.produto = self.produto_selecionado
            self.carregamento_atual.veiculo = self.veiculo_selecionado
            self.carregamento_atual.motorista = self.motorista_selecionado
            self.carregamento_atual.lacres = self.lacres.get()
            self.carregamento_atual.numero_pedido = self.numero_pedido.get()

            resultado_transporte = self.criar_transporte(session, self.carregamento_atual)
            if not resultado_transporte[0]:
                messagebox.showerror("Erro", resultado_transporte[1])
                return

            # mostrando saida transporte
            self.saida_transporte.set(resultado_transporte[1])
            self.app_main.update_idletasks()

            if self.carregamento_atual.produto.inspecao_veiculo == 1:
                resultado_inspecao_veicular = self.criar_lote_inspecao_veiculo(session,
                                                                               self.carregamento_atual.produto.codigo,
                                                                               self.carregamento_atual.veiculo.placa_1,
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
            print(error)
            traceback.print_exc(file=sys.stdout)
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

    def criar_remessas(self, session):
        remessas = self.extrair_remessas()
        for remessa in remessas:
            try:
                numero_remessa = VL01.criar_remessa(session, remessa)
                remessa.numero_remessa = numero_remessa
                self.atualizar_saida_remessas(remessa)
            except Exception as e:
                raise e

        return remessas

    def extrair_remessas(self):
        remessas = []
        dic_itens = {}
        childrens = self.treeview_remessas.get_children()

        for item in childrens:
            codigo_produto = self.treeview_remessas.item(item, "values")[0].strip()
            produto = ProdutoService.pesquisar_produto_pelo_codigo(codigo_produto)
            quantidade = self.treeview_remessas.item(item, "values")[4].strip()
            ordem = self.treeview_remessas.item(item, "values")[3].strip()

            item_remessa = ItemRemessa()
            item_remessa.numero_ordem = ordem
            item_remessa.quantidade = quantidade
            item_remessa.produto = produto
            '''
            self.numero_ordem = None
        self.quantidade = None
        self.produto = None
        self.numero_item = None
        self.cfop = None
        self.df_icms = None
        self.df_ipi = None
        self.df_pis = None
        self.df_cofins = None
        self.codigo_imposto = None
            '''

            # adicionando o item ao dicionário...
            dic_itens.setdefault(item_remessa.numero_ordem, []).append(item_remessa)

        for chave in dic_itens:
            remessas.append(Remessa(itens=dic_itens[chave]))

        return remessas

    def atualizar_saida_remessas(self, remessa):
        # atualizando a saída de remessas
        saida_remessa = self.saida_remessas.get()
        self.saida_remessas.set('{} / {}'.format(saida_remessa, remessa))
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
