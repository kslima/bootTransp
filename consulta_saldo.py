import tkinter
from tkinter import StringVar, Label, Entry, Button, W, Checkbutton, messagebox, DISABLED, IntVar, Text, NO, CENTER, \
    END, INSERT, E, ttk
from tkinter.ttk import Notebook, Frame, Radiobutton, Combobox, Treeview
from cadastro_produto import CadastroProduto
from dialogo_entrada import DialogoEntrada
from service import ProdutoService, TipoCarregamentoService
from model import Produto, TipoCarregamento, ItemRemessa, Ordem
from utilitarios import NumberUtils, StringUtils


class ConsultaSaldo:

    def __init__(self, master, main=None):
        self.app_main = tkinter.Toplevel(master)
        self.app_main.title("Cadastro de Tipo de Carregamento")
        self.centralizar_tela()
        self.main = main

        self.tipo_carregamento_atual = None

        self.entry_nome = None
        self.cb_inspecao_veiculo = None
        self.cb_inspecao_produto = None
        self.cb_remover_a = None
        self.rb_nao_informar_lacres = None
        self.rb_informar_lacres_lona = None
        self.rb_informar_lacres = None
        self.rb_informar_lacres_lona = None
        self.entry_codigo_transportador = None
        self.entry_tipo_frete = None
        self.entry_destino_frete = None
        self.entry_docs_diversos = None
        self.entry_numero_ordem = None
        self.entry_numero_pedido_frete = None
        self.nome = StringVar()
        self.inspecao_produto = IntVar()
        self.inspecao_veiculo = IntVar()
        self.remover_a = IntVar()
        self.tipo_lacre = IntVar()
        self.codigo_transportador = StringVar()
        self.tipo_frete = StringVar()
        self.destino_frete = StringVar()
        self.numero_ordem = StringVar()
        self.numero_pedido_frete = StringVar()
        self.quantidade_item_remessa = StringVar()

        self.produto_selecionado = None
        self.cbo_produtos = None
        self.nome_produto_selecionado = StringVar()
        self.entry_df_icms = None
        self.entry_df_ipi = None
        self.entry_df_pis = None
        self.entry_df_cofins = None
        self.entry_cfop = None
        self.entry_codigo_imposto = None
        self.entry_quantidade_remessa = None
        self.dif_icms = StringVar()
        self.dif_ipi = StringVar()
        self.dif_pis = StringVar()
        self.dif_cofins = StringVar()
        self.cfop = StringVar()
        self.codigo_imposto = StringVar()
        self.treeview_itens = None

        self.atualizando_cadastro = False
        self.produto_atual = None

        Label(self.app_main, text="CNPJ").grid(sticky=W, column=0, row=0, padx=10)
        self.entry_df_cofins = Entry(self.app_main, textvariable=self.codigo_imposto)
        self.entry_df_cofins.grid(sticky="we", column=0, row=1, padx=10, ipady=2, columnspan=2)

        Button(self.app_main, text='Pesquisar', command=self.consultar_saldo) \
            .grid(sticky="we", column=2, row=1, padx=10)

        self.treeview_itens = Treeview(self.app_main, height=10,
                                       column=("c0", "c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8")
                                       , show="headings")
        self.treeview_itens.bind("<Double-1>", self.inserir_quantidade_item)

        self.treeview_itens.heading("#1", text="Data")
        self.treeview_itens.heading("#2", text="Ordem")
        self.treeview_itens.heading("#3", text="Material")
        self.treeview_itens.heading("#4", text="Cliente")
        self.treeview_itens.heading("#5", text="Cidade")
        self.treeview_itens.heading("#6", text="Qtd")
        self.treeview_itens.heading("#7", text="Qtd. Disp.")
        self.treeview_itens.heading("#8", text="Pedido")
        self.treeview_itens.heading("#9", text="Tipo")

        self.treeview_itens.column("c0", width=70, stretch=NO, anchor=CENTER)
        self.treeview_itens.column("c1", width=60, stretch=NO, anchor=CENTER)
        self.treeview_itens.column("c2", width=120, stretch=NO, anchor=CENTER)
        self.treeview_itens.column("c3", width=150, stretch=NO, anchor=CENTER)
        self.treeview_itens.column("c4", width=100, stretch=NO, anchor=CENTER)
        self.treeview_itens.column("c5", width=70, stretch=NO, anchor=CENTER)
        self.treeview_itens.column("c6", width=70, stretch=NO, anchor=CENTER)
        self.treeview_itens.column("c7", width=70, stretch=NO, anchor=CENTER)
        self.treeview_itens.column("c8", width=50, stretch=NO, anchor=CENTER)

        self.treeview_itens.tag_configure('bg', background='yellow')
        self.treeview_itens.tag_configure('fg', foreground='red')

        self.treeview_itens.grid(sticky="we", row=7, padx=10, pady=5, columnspan=6)

        Label(self.app_main, text="Quantidade: ").grid(sticky=W, row=8, padx=10)
        self.entry_quantidade_remessa = Entry(self.app_main, textvariable=self.quantidade_item_remessa)
        self.entry_quantidade_remessa.grid(sticky="we", row=9, column=0, padx=10, ipady=2, pady=(0, 15))
        self.entry_quantidade_remessa.config(validate="key",
                                             validatecommand=(self.app_main.register(NumberUtils.eh_decimal), '%P'))

        Button(self.app_main, text='Inserir', command=self.inserir_main) \
            .grid(sticky="we", column=1, row=9, padx=10, pady=(0, 15))

    def centralizar_tela(self):
        # Gets the requested values of the height and widht.
        window_width = self.app_main.winfo_reqwidth()
        window_height = self.app_main.winfo_reqheight()

        # Gets both half the screen width/height and window width/height
        position_right = int(self.app_main.winfo_screenwidth() / 2.3 - window_width / 2)
        position_down = int(self.app_main.winfo_screenheight() / 3 - window_height / 2)

        # Positions the window in the center of the page.
        self.app_main.geometry("+{}+{}".format(position_right, position_down))

    def criar_botao_salvar_excluir(self):

        frame = Frame(self.app_main)
        frame.grid(sticky=W, column=0, row=1, padx=10, pady=10)

        Button(frame, text='Salvar', command=self.salvar_tipo_transporte, width=20) \
            .grid(sticky="we", column=0, row=1, padx=(0, 10))

        Button(frame, text='Excluir', command=self.extrair_itens, width=20) \
            .grid(sticky="we", column=1, row=1)

    def consultar_saldo(self):
        ordem = Ordem()
        ordem.data = '18/05/2021'
        ordem.numero = '10895'
        ordem.material = 'ETANOL ANIDRO'
        ordem.cliente = 'PETROBRAS'
        ordem.cidade = 'PAULINIA - SP'
        ordem.qtd = '1000,00'
        ordem.qtd_saida = '235,450'
        ordem.qtd_disponivel = '764,55'
        ordem.pedido = '450045232'
        ordem.tipo = 'ZORB'
        ordem.cnpj = '12229415001435'
        ordem.status = ''

        ordem1 = Ordem()
        ordem1.data = '18/05/2021'
        ordem1.numero = '10895'
        ordem1.material = 'ETANOL ANIDRO'
        ordem1.cliente = 'PETROBRAS'
        ordem1.cidade = 'PAULINIA - SP'
        ordem1.qtd = '1000,00'
        ordem1.qtd_saida = '235,450'
        ordem1.qtd_disponivel = '764,55'
        ordem1.pedido = '450045232'
        ordem1.tipo = 'ZORB'
        ordem1.cnpj = '12229415001435'
        ordem1.status = ''

        ordens = [ordem, ordem1]
        self.inserir_item_remessa(ordens)

    def atualizar_lista_produtos(self):
        p = ProdutoService.listar_produtos()
        self.cbo_produtos['values'] = tuple("{} - {}".format(prod.codigo, prod.nome) for prod in p)

    def inserir_item_remessa(self, ordens):
        try:
            self.validar_novo_item()
        except RuntimeError as e:
            messagebox.showerror("Erro", str(e))
            return

        self.limpar_treeview()
        for ordem in ordens:
            self.treeview_itens.insert("", "end", values=(ordem.data,
                                                          ordem.numero,
                                                          ordem.material,
                                                          ordem.cliente,
                                                          ordem.cidade,
                                                          ordem.qtd,
                                                          ordem.qtd_disponivel,
                                                          ordem.pedido,
                                                          ordem.tipo))

    def inserir_quantidade_item(self, event):
        selection = self.treeview_itens.selection()
        saldo = self.treeview_itens.item(selection, "values")[6]
        self.quantidade_item_remessa.set(saldo)

    def inserir_main(self):
        selection = self.treeview_itens.selection()
        ordem = self.treeview_itens.item(selection, "values")[1]
        self.main.ordem_item_remessa.set(ordem)
        self.main.quantidade_item_remessa.set(self.quantidade_item_remessa.get())
        self.main.inserir_item_remessa()

    def limpar_treeview(self):
        for item in self.treeview_itens.get_children():
            self.treeview_itens.delete(item)

    def validar_novo_item(self):
        return True

    def eliminar_item_remessas(self):
        selected_items = self.treeview_itens.selection()
        if len(selected_items) == 0:
            messagebox.showerror("Erro", "Sem ítens para eliminar!")
            return
        for item in selected_items:
            self.treeview_itens.delete(item)

    def mudar_produto(self, event):
        codigo_produto = self.nome_produto_selecionado.get().split("-")[0].strip()
        self.produto_selecionado = ProdutoService.pesquisar_produto_pelo_codigo(codigo_produto)

    def cadastrar_novo_produto(self):
        CadastroProduto(self.app_main)

    def editar_produto(self):
        if self.produto_selecionado is None:
            messagebox.showerror("Erro", "Selecione um produto!")
        else:
            novo_produto = CadastroProduto(self.app_main)
            novo_produto.setar_campos_para_edicao(self.produto_selecionado)
            novo_produto.atualizando_cadastro = True

    def salvar_tipo_transporte(self):
        try:
            self.verificar_campos_obrigatorios()
            # verifando se o produto possui id
            if self.produto_atual is None or self.produto_atual.id_produto is None:
                self.salvar()
            else:
                self.atualizar()

        except RuntimeError as e:
            messagebox.showerror("Erro", str(e))

    def salvar(self):
        self.tipo_carregamento_atual = TipoCarregamento()
        self.tipo_carregamento_atual.nome = self.nome.get().strip()
        self.tipo_carregamento_atual.inspecao_veiculo = self.inspecao_veiculo.get()
        self.tipo_carregamento_atual.inspecao_produto = self.inspecao_produto.get()
        self.tipo_carregamento_atual.remover_a = self.remover_a.get()
        self.tipo_carregamento_atual.tipo_lacre = self.tipo_lacre.get()
        self.tipo_carregamento_atual.numero_ordem = self.numero_ordem.get().strip()
        self.tipo_carregamento_atual.numero_pedido_frete = self.numero_pedido_frete.get().strip()
        self.tipo_carregamento_atual.tipo_frete = self.tipo_frete.get().strip()
        self.tipo_carregamento_atual.destino_frete = self.destino_frete.get().strip()
        self.tipo_carregamento_atual.doc_diversos = self.entry_docs_diversos.get("1.0", END)
        self.tipo_carregamento_atual.codigo_transportador = self.codigo_transportador.get()
        self.tipo_carregamento_atual.itens_str = self.extrair_itens()

        try:
            TipoCarregamentoService.inserir_tipo_carregamento(self.tipo_carregamento_atual)
            messagebox.showinfo("Sucesso", "Tipo de carregamento salvo com sucesso!")
            self.app_main.destroy()
        except Exception as e:
            messagebox.showerror("Erro", "Erro ao salvar tipo de carregamento\n{}".format(e))

    def atualizar(self):
        self.produto_atual.codigo = self.codigo.get()
        self.produto_atual.nome = self.nome.get()
        self.produto_atual.deposito = self.deposito.get()
        self.produto_atual.lote = self.lote.get()
        self.produto_atual.inspecao_veiculo = self.inspecao_veiculo.get()
        self.produto_atual.inspecao_produto = self.inspecao_produto.get()
        self.produto_atual.remover_a = self.remover_a.get()
        try:
            ProdutoService.atualizar_produto(self.produto_atual)
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
            self.app_main.destroy()
        except Exception as e:
            print(e)
            messagebox.showerror("Erro", "Erro ao atualizar produto\n{}".format(e))

    def deletar(self):
        deletar = messagebox.askokcancel("Confirmar", "Excluir registro pernamentemente ?")
        if deletar:
            try:
                ProdutoService.deletar_produto(self.produto_atual.id_produto)
                messagebox.showinfo("Sucesso", "Produto deletado com sucesso!")
                self.app_main.destroy()
            except Exception as e:
                print(e)
                messagebox.showerror("Erro", "Erro ao deletar produto\n{}".format(e))

    def verificar_campos_obrigatorios(self):
        return True

    def setar_campos_para_edicao(self, produto):
        self.botao_deletar['state'] = 'normal'
        self.produto_atual = produto
        self.codigo.set(self.produto_atual.codigo)
        self.nome.set(self.produto_atual.nome)
        self.deposito.set(self.produto_atual.deposito)
        self.lote.set(self.produto_atual.lote)
        self.inspecao_veiculo.set(self.produto_atual.inspecao_veiculo)
        self.inspecao_produto.set(self.produto_atual.inspecao_produto)
        self.remover_a.set(self.produto_atual.remover_a)

    def extrair_itens(self):
        lista = []
        itens = self.treeview_itens.get_children()
        for item in itens:
            i = ';'.join(self.treeview_itens.item(item, "values"))
            lista.append('[{}]'.format(i))
        return ''.join(lista)


if __name__ == '__main__':
    app_main = tkinter.Tk()
    ConsultaSaldo(app_main)
    app_main.mainloop()
