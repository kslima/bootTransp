import tkinter
from tkinter.ttk import *
from tkinter import scrolledtext, END, Listbox, W, DISABLED, INSERT, messagebox, E, CENTER, SW, simpledialog, NO, YES
import re
from win32api import MessageBox
from cadastro_motorista import CadastroMotorista
from cadastro_veiculo import CadastroVeiculo
from model import Produto, Motorista, Remessa, Veiculo, Transporte, Carregamento, LoteInspecao
from service import MotoristaService, VeiculoService, ProdutoService
import service
from utilitarios import StringUtils, NumberUtils
from cadastro_produto import CadastroProduto
from cadastro_lacres import CadastroLacres
from qa01 import QA01
from vt02 import VT02
from qe01 import QE01
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
        self.app_main.geometry('750x700')
        self.centralizar_tela()

        menubar = tkinter.Menu(self.app_main)

        filemenu = tkinter.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Abrir planilha de configuração")
        filemenu.add_command(label="Sair", command=self.app_main.quit)

        menubar.add_cascade(label="Arquivo", menu=filemenu)

        self.app_main.config(menu=menubar)

        self.TEXTO_DADOS_MOTORISTA = "** NENHUM MOTORISTA SELECIONADO **"
        self.TEXTO_DADOS_VEICULO = "** NENHUM VEÍCULO SELECIONADO **"

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
        self.tabControl.place(x=10, y=10)

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

        '''
        self.dados_produto.set("*")
        label_dados_remessa = Label(self.tab_remessa, textvariable=self.dados_produto, font=(None, 9, 'bold'))
        label_dados_remessa.configure(foreground="green")
        label_dados_remessa.grid(sticky=W, column=0, row=3, padx=2, columnspan=4)
        
        Label(self.tab_remessa, text="Ordem/Quantidade ", font=(None, 9, 'normal')) \
            .grid(sticky=W, column=0, row=4, padx=2, ipady=2, columnspan=4)

        self.scroll_ordem_quantidade = scrolledtext.ScrolledText(self.tab_remessa, undo=True, height=4, width=25,
                                                                 state="disable")
        self.scroll_ordem_quantidade.grid(sticky=W, column=0, row=5, padx=5, rowspan=6, columnspan=2)
        self.scroll_ordem_quantidade.bind('<KeyRelease>', self.mostrar_total_remessas)

        self.label_total_remessas.set("Total: {}".format("0,000"))
        label_quantidade = Label(self.tab_remessa, textvariable=self.label_total_remessas, font=(None, 8, 'bold'))
        label_quantidade.grid(sticky=SW, column=2, row=5, padx=2, columnspan=4)
        label_quantidade.configure(foreground="blue")

        self.total_itens_remessas.set("Remessas: {}".format("0"))
        label_numero_remessas = Label(self.tab_remessa, textvariable=self.total_itens_remessas,
                                      font=(None, 8, 'bold'))
        label_numero_remessas.grid(sticky=SW, column=2, row=6, padx=2, columnspan=4)
        label_numero_remessas.configure(foreground="blue")

        self.total_acumulado_remessas.set("Acumulado: {}".format("0,000"))
        label_acumulado = Label(self.tab_remessa, textvariable=self.total_acumulado_remessas,
                                font=(None, 8, 'bold'))
        label_acumulado.grid(sticky=SW, column=2, row=7, padx=2, columnspan=4)
        label_acumulado.configure(foreground="blue")

        self.total_pendente_remessas.set("Pendente: {}".format("0,000"))
        self.label_quantidade_pendente = Label(self.tab_remessa, textvariable=self.total_pendente_remessas,
                                               font=(None, 8, 'bold'))
        self.label_quantidade_pendente.grid(sticky=SW, column=2, row=8, padx=2, columnspan=4)
        self.label_quantidade_pendente.configure(foreground="blue")
        '''

    def criar_frame_motorista(self):

        Label(self.tab_motorista, text="Pesquisar motorista").grid(sticky=W, column=0, row=0, padx=2)
        self.txt_pesquisa_motorista = Entry(self.tab_motorista, textvariable=self.pesquisa_motorista, width=62)
        self.txt_pesquisa_motorista.grid(sticky="we", column=0, row=1, padx=5, ipady=1, pady=(0, 5), columnspan=2)
        # self.txt_pesquisa_motorista.bind('<Return>', self.pesquisar_motorista)
        self.txt_pesquisa_motorista.bind("<KeyRelease>", self.pesquisar_motorista)

        Button(self.tab_motorista, text='Novo', command=self.cadastrar_novo_motorista) \
            .grid(sticky=W, column=2, row=1, padx=2, pady=(0, 5))

        Button(self.tab_motorista, text='Editar', command=self.editar_motorista) \
            .grid(sticky=W, column=3, row=1, padx=2, pady=(0, 5))

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
        self.campo_pesquisa_veiculo = Entry(self.tab_motorista, textvariable=self.texto_pesquisa_transportador,
                                            width=50)
        self.campo_pesquisa_veiculo.bind('<Return>', self.pesquisar_transportador)
        self.campo_pesquisa_veiculo.grid(sticky="we", column=0, row=5, padx=2, ipady=1, pady=(0, 5), columnspan=3)

        Button(self.tab_motorista, text='Pesquisar', command=lambda: self.pesquisar_transportador('')) \
            .grid(sticky=W, column=3, row=5, padx=2, pady=(0, 5))

        Label(self.tab_motorista, text="Pedido").grid(sticky=W, column=0, row=6, padx=2)
        Entry(self.tab_motorista, textvariable=self.numero_pedido).grid(sticky=W, column=0, row=7, padx=5,
                                                                        ipady=1, pady=(0, 5))

        self.dados_transportador_selecionado.set("** NENHUM TRANSPORTADOR SELECIONADO **")
        label_dados_transportadora = Label(self.tab_motorista, wraplength=540, font=(None, 8, 'bold'),
                                           textvariable=self.dados_transportador_selecionado)
        label_dados_transportadora.grid(sticky="we", column=0, row=8, padx=2, columnspan=4)
        label_dados_transportadora.configure(foreground="red")

    def criar_frame_veiculo(self):
        Label(self.tab_veiculo, text="Pesquisar (Placa Cavalo)").grid(sticky=W, column=0, row=3, padx=2)
        self.campo_pesquisa_veiculo = Entry(self.tab_veiculo, textvariable=self.pesquisa_veiculo, width=62)
        self.campo_pesquisa_veiculo.bind('<Return>', self.pesquisar_veiculo)
        self.campo_pesquisa_veiculo.bind("<KeyRelease>", self.pesquisar_veiculo)
        self.campo_pesquisa_veiculo.grid(sticky="we", column=0, row=4, padx=5, ipady=1, pady=(0, 5), columnspan=4)

        Button(self.tab_veiculo, text='Novo', command=self.cadastrar_novo_veiculo) \
            .grid(sticky=W, column=4, row=4, padx=2, pady=(0, 5))

        Button(self.tab_veiculo, text='Editar', command=self.editar_veiculo) \
            .grid(sticky=W, column=5, row=4, padx=2, pady=(0, 5))

        self.treeview_veiculo = Treeview(self.tab_veiculo, selectmode="browse", height=4,
                                         column=("c0", "c1", "c2", "c3", "c4"), show="headings")
        self.treeview_veiculo.heading("#1", text="ID")
        self.treeview_veiculo.heading("#2", text="Cavalo")
        self.treeview_veiculo.heading("#3", text="Carreta 1")
        self.treeview_veiculo.heading("#4", text="Carreta 2")
        self.treeview_veiculo.heading("#5", text="Carreta 3")

        self.treeview_veiculo.column("c0", width=60, stretch=NO, anchor=CENTER)
        self.treeview_veiculo.column("c1", width=120, stretch=NO, anchor=CENTER)
        self.treeview_veiculo.column("c2", width=120, stretch=NO, anchor=CENTER)
        self.treeview_veiculo.column("c3", width=120, stretch=NO, anchor=CENTER)
        self.treeview_veiculo.column("c4", width=120, stretch=NO, anchor=CENTER)

        self.treeview_veiculo.grid(sticky=W, column=0, row=5, padx=5, columnspan=6)
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
        self.frame_saida.place(x=10, y=330, width=555)

        Label(self.frame_saida, text="Remessa(s)").grid(sticky="we", column=0, row=0, padx=2)
        Entry(self.frame_saida, textvariable=self.saida_remessas, width=42, state=DISABLED) \
            .grid(sticky="we", column=0, row=1, padx=2, ipady=1)
        Button(self.frame_saida, text='Inserir',
               command=lambda: self.saida_remessas.set(self.entrar_dados_manualmente("Remessa(s)"))) \
            .grid(sticky="we", column=1, row=1, padx=2)

        Label(self.frame_saida, text="Lote Inspecao Produto(89)").grid(sticky="we", column=0, row=2, padx=2)
        Entry(self.frame_saida, textvariable=self.saida_inpecao_produto, width=20, state=DISABLED) \
            .grid(sticky="we", column=0, row=3, padx=2)

        Label(self.frame_saida, text="Transporte").grid(sticky="we", column=0, row=4, padx=2)
        Entry(self.frame_saida, textvariable=self.saida_transporte, width=20, state=DISABLED) \
            .grid(sticky="we", column=0, row=5, padx=2)

        Label(self.frame_saida, text="Lote Inspecao Veicular(07)").grid(sticky="we", column=0, row=6, padx=2)
        Entry(self.frame_saida, textvariable=self.saida_inspecao_veiculo, width=20, state=DISABLED) \
            .grid(sticky="we", column=0, row=7, padx=2)
        # rodapé
        botao_criar = Button(self.frame_saida, text='Criar', command=self.criar)
        botao_criar.grid(sticky="we", column=0, row=9, padx=2, pady=(15, 0))

    def entrar_dados_manualmente(self, texto):
        entrada = simpledialog.askstring(title="", prompt=texto)
        return entrada

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

    def atualizar_lista_produtos(self):
        p = service.ProdutoService.listar_produtos()
        self.cbo_produtos['values'] = tuple("{} - {}".format(prod.codigo, prod.nome) for prod in p)

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
        self.label_dados_nome_motorista.configure(foreground="blue")
        self.dados_motorista_selecionado.set("** {} - {} **".format(id_motorista, nome).upper())

    def limpar_treeview_motoristas(self):
        for item in self.treeview_motorista.get_children():
            self.treeview_motorista.delete(item)
        self.dados_motorista_selecionado.set(self.TEXTO_DADOS_MOTORISTA)
        self.label_dados_nome_motorista.configure(foreground="red")
        self.motorista_selecionado = None

    def pesquisar_transportador(self, event):
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

            else:
                self.dados_transportador_selecionado.set("")
                MessageBox(None, "Transportador não encontrado!")
        else:
            MessageBox(None, "Informe um cpf ou cnpj válido!")

    def pesquisar_veiculo(self, event):
        criterio = self.pesquisa_veiculo.get().strip()
        if criterio:
            self.limpar_treeview_veiculos()
            for veiculo in VeiculoService.pesquisar_veiculo(criterio):
                self.treeview_veiculo.insert("", "end", values=(veiculo.id_veiculo,
                                                                veiculo.placa_1,
                                                                veiculo.placa_2 if veiculo.placa_2 else "",
                                                                veiculo.placa_3 if veiculo.placa_3 else "",
                                                                veiculo.placa_3 if veiculo.placa_3 else ""))
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
        self.label_dados_veiculo_selecionado.configure(foreground="blue")
        self.dados_veiculo_selecionado.set("** {} - {} {} {} {} **".format(id_veiculo, self.veiculo_selecionado.placa_1,
                                                                           self.veiculo_selecionado.placa_2,
                                                                           self.veiculo_selecionado.placa_3,
                                                                           self.veiculo_selecionado.placa_4))

    def cadastrar_novo_veiculo(self):
        CadastroVeiculo(self.app_main)

    def editar_veiculo(self):
        if self.veiculo_selecionado is None:
            messagebox.showerror("Erro", "Selecione um veículo!")
            return
        cadastro = CadastroVeiculo(self.app_main)
        cadastro.setar_campos_para_edicao(self.veiculo_selecionado)
        cadastro.atualizando_cadastro = True

    def cadastrar_lacres(self):
        CadastroLacres(self.app_main)

    def editar_lacres(self):
        cadastro_lacres = CadastroLacres(self.app_main)
        cadastro_lacres.setar_campos_para_edicao(self.lacres_selecionados)
        cadastro_lacres.atualizando_cadastro = True

    def contar_lacres(self):
        lacres = self.lacres.get().strip()
        if lacres != "":
            lacres = lacres.split("/")
        self.label_quantidade_lacres.set("Lacres: ({})".format(str(len(lacres))))

    def buscar_lacres(self, event):
        self.lacres_selecionados = service.LacreService.pesquisar_pacote_lacres_pelo_codigo(self.codigo_lacres.get())
        if len(self.lacres_selecionados) == 0:
            messagebox.showerror("Sem resultados", "Nenhum registro encontrado!")
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
        self.contar_lacres()

    def criar_remessas(self, session):
        numero_remessas = []
        for remessa in self.remessas:
            result = VL01.create(session, remessa)
            if result[0]:
                numero_remessas.append(result[1])
            else:
                # caso erro, retorna a mensagem de erro.
                return result
        # caso sucesso, retorna uma lista com os numeros das remessas criadas
        print(numero_remessas)
        return True, numero_remessas

    def lote_qualidade(self, produto, numero_remessa):
        lote = LoteInspecao()
        lote.material = produto.codigo
        lote.origem = "89"
        lote.lote = produto.lote
        lote.deposito = produto.deposito
        lote.texto_breve = numero_remessa
        return lote

    # criando lotes de controle de qualidade
    def criar_lotes_qualidade(self, session, remessas):
        lotes = []
        messagem_progresso = "Lote {} criado na remessa {}..."
        for remessa in remessas:
            lote = self.lote_qualidade(self.produto_selecionado, remessa)
            result = QA01.create(session, lote)
            self.inserir_saida(messagem_progresso.format(result[1], remessa))
            # se cair nesse laço, significa que o lote foi criado com sucesso
            if result[0]:
                lotes.append(result[1])

            else:
                # caso erro, retorna a mensagem de erro.
                return result

        # lote de controle com a primeira remessa. Será usado no transporte.
        if len(remessas) > 1:
            lote = self.lote_qualidade(self.produto_selecionado, remessas[0])
            ultimo_lote = QA01.create(session, lote)
            self.inserir_saida(messagem_progresso.format(ultimo_lote[1], remessas[0]))
            lotes.append(ultimo_lote[1])
            print(lotes)
        return True, lotes

    def criar_transporte(self, session, carregamento):
        resultado = VT01.create(session, carregamento)
        if resultado[0]:
            self.inserir_saida("Transporte {} criado...".format(resultado[1]))
        return resultado

    def inserir_saida(self, info):
        pass

    def criar(self):
        resultado_remessas = None
        resultado_lotes_qualidade = None
        resultado_transporte = None
        resultado_inspecao_veicular = None
        resultado_lancar_s_inspecao_veicular = None

        session = SAPGuiApplication.connect()
        if self.assert_shipping():
            resultado_remessas = self.criar_remessas(session)

            # se houver erro, uma mensagem será exibida com o erro.
            if not resultado_remessas[0]:
                messagebox.showerror("Erro", resultado_remessas[1])
                return

        # mostrando remssas criadas
        self.saida_remessas.set(resultado_remessas[1])
        self.app_main.update_idletasks()

        if self.produto_selecionado.inspecao_produto == "s":
            resultado_lotes_qualidade = self.criar_lotes_qualidade(session, resultado_remessas[1])

            if not resultado_lotes_qualidade[0]:
                messagebox.showerror("Erro", resultado_lotes_qualidade[1])
                return

            # mostrando saídas lote de inspecao do produto
            self.saida_inpecao_produto.set(resultado_lotes_qualidade[1])
            self.app_main.update_idletasks()

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

        # mostrando saida transporte
        self.saida_transporte.set(resultado_transporte[1])
        self.app_main.update_idletasks()

        if carregamento.produto.inspecao_veiculo.lower() == "s":
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


main = AppView()
