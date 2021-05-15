import tkinter
from tkinter import StringVar, Label, Entry, Button, W, Checkbutton, messagebox, DISABLED, IntVar, Text, NO, CENTER, \
    END, INSERT
from tkinter.ttk import Notebook, Frame, Radiobutton, Combobox, Treeview

from service import ProdutoService
from model import Produto
from utilitarios import NumberUtils, StringUtils


class CadastroTipoCarregamento:

    def __init__(self, master):
        self.app_main = tkinter.Toplevel(master)
        self.app_main.title("Cadastro de Tipo de Carregamento")
        self.centralizar_tela()

        # tabs
        self.tabControl = Notebook(self.app_main)
        self.tab_transporte = None
        self.cb_inspecao_veiculo = None
        self.cb_inspecao_produto = None
        self.cb_remover_a = None
        self.rb_nao_informar_lacres = None
        self.rb_informar_lacres_lona = None
        self.rb_informar_lacres = None
        self.rb_informar_lacres_lona = None
        self.entry_docs_diversos = None
        self.entry_numero_ordem_padrao = None
        self.entry_numero_pedido_frete_padrao = None
        self.inspecao_produto = IntVar()
        self.inspecao_veiculo = IntVar()
        self.remover_a = IntVar()
        self.informar_lacres = StringVar()
        self.docs_diversos = StringVar()
        self.numero_ordem_padrao = StringVar()
        self.numero_pedido_frete_padrao = StringVar()

        self.tab_impostos = None
        self.cbo_produtos = None
        self.nome_produto_selecionado = StringVar()
        self.entry_df_icms = None
        self.entry_df_ipi = None
        self.entry_df_pis = None
        self.entry_df_cofins = None
        self.entry_cfop = None
        self.entry_codigo_imposto = None
        self.dif_icms = StringVar()
        self.dif_ipi = StringVar()
        self.dif_pis = StringVar()
        self.dif_cofins = StringVar()
        self.cfop = StringVar()
        self.codigo_imposto = StringVar()
        self.treeview_itens = None

        self.tabControl.grid(sticky=W, column=0, row=0, padx=10, pady=10)
        self.criar_aba_transporte()
        self.criar_aba_impostos()

        self.atualizando_cadastro = False
        self.produto_atual = None

    def centralizar_tela(self):
        # Gets the requested values of the height and widht.
        window_width = self.app_main.winfo_reqwidth()
        window_height = self.app_main.winfo_reqheight()

        # Gets both half the screen width/height and window width/height
        position_right = int(self.app_main.winfo_screenwidth() / 2.3 - window_width / 2)
        position_down = int(self.app_main.winfo_screenheight() / 3 - window_height / 2)

        # Positions the window in the center of the page.
        self.app_main.geometry("+{}+{}".format(position_right, position_down))

    def criar_aba_transporte(self):
        self.tab_transporte = Frame(self.tabControl)
        self.tabControl.add(self.tab_transporte, text="Transporte")

        self.inspecao_veiculo.set(1)
        self.cb_inspecao_veiculo = Checkbutton(self.tab_transporte, text="Inspeção veículo (07)", onvalue=1, offvalue=0,
                                               variable=self.inspecao_veiculo)
        self.cb_inspecao_veiculo.grid(sticky=W, column=0, row=0, padx=5)

        self.inspecao_produto.set(0)
        self.cb_inspecao_produto = Checkbutton(self.tab_transporte, text="Inspeção produto (89)", onvalue=1, offvalue=0,
                                               variable=self.inspecao_produto)
        self.cb_inspecao_produto.grid(sticky=W, column=0, row=1, padx=5)

        self.remover_a.set(0)
        self.cb_remover_a = Checkbutton(self.tab_transporte, text="Remover 'A'", onvalue=1, offvalue=0,
                                        variable=self.remover_a)
        self.cb_remover_a.grid(sticky=W, column=0, row=2, padx=5)

        self.informar_lacres.set(0)
        self.rb_nao_informar_lacres = Radiobutton(self.tab_transporte, text="Sem lacres", value=0,
                                                  variable=self.informar_lacres)
        self.rb_nao_informar_lacres.grid(sticky=W, column=0, row=3, padx=5)

        self.rb_informar_lacres = Radiobutton(self.tab_transporte, text="Lacres", value=1,
                                              variable=self.informar_lacres)
        self.rb_informar_lacres.grid(sticky=W, column=1, row=3, padx=5)

        self.rb_informar_lacres_lona = Radiobutton(self.tab_transporte, text="Lacres lona", value=2,
                                                   variable=self.informar_lacres)
        self.rb_informar_lacres_lona.grid(sticky=W, column=2, row=3, padx=5)

        Label(self.tab_transporte, text="Docs. Diversos: ").grid(sticky=W, row=4, padx=5, pady=(5, 0))

        self.entry_docs_diversos = Text(self.tab_transporte, height=6, width=67)
        self.entry_docs_diversos.grid(sticky=W, row=5, padx=5, columnspan=9)
        self.entry_docs_diversos.bind("<KeyRelease>", self.converter_para_maiusculo)

        Label(self.tab_transporte, text="Ordem/Pedido").grid(sticky=W, row=6, padx=5)
        self.entry_numero_ordem_padrao = Entry(self.tab_transporte, textvariable=self.numero_ordem_padrao)
        self.entry_numero_ordem_padrao.grid(sticky="we", column=0, row=7, padx=5, ipady=1)
        self.entry_numero_ordem_padrao.config(validate="key", validatecommand=(self.app_main
                                                                               .register(NumberUtils.eh_inteiro),
                                                                               '%P'))

        Label(self.tab_transporte, text="Pedido de frete").grid(sticky=W, column=1, row=6, padx=5)
        self.entry_numero_pedido_frete_padrao = Entry(self.tab_transporte, textvariable=self.numero_pedido_frete_padrao)
        self.entry_numero_pedido_frete_padrao.grid(sticky="we", column=1, row=7, padx=5, ipady=1, columnspan=8)
        self.entry_numero_pedido_frete_padrao.config(validate="key", validatecommand=(self.app_main
                                                                                      .register(NumberUtils.eh_inteiro),
                                                                                      '%P'))

    def criar_aba_impostos(self):
        self.tab_impostos = Frame(self.tabControl)
        self.tabControl.add(self.tab_impostos, text="Impostos")

        Label(self.tab_impostos, text="Produto: ").grid(sticky=W, row=0, padx=5)
        self.cbo_produtos = Combobox(self.tab_impostos, textvariable=self.nome_produto_selecionado, state="readonly")
        self.cbo_produtos['values'] = tuple("{} - {}".format(prod.codigo, prod.nome) for prod in
                                            ProdutoService.listar_produtos())
        # self.cbo_produtos.bind('<<ComboboxSelected>>', self.mudar_produto)
        self.cbo_produtos.grid(sticky="we", row=1, padx=5, ipady=1, pady=(0, 5), columnspan=4)

        Button(self.tab_impostos, text='Novo', command=self.cadastrar_novo_produto) \
            .grid(sticky="we", column=4, row=1, padx=5, pady=(0, 5), columnspan=2)

        Button(self.tab_impostos, text='Editar', command=self.editar_produto) \
            .grid(sticky="we", column=6, row=1, padx=5, pady=(0, 5), columnspan=2)

        Label(self.tab_impostos, text="DIF. ICMS").grid(sticky=W, row=2, padx=5)
        self.entry_df_icms = Entry(self.tab_impostos, textvariable=self.dif_icms)
        self.entry_df_icms.grid(sticky="we", row=3, padx=5, columnspan=2)

        Label(self.tab_impostos, text="DIF. IPI").grid(sticky=W, column=2, row=2, padx=5)
        self.entry_df_icms = Entry(self.tab_impostos, textvariable=self.dif_ipi)
        self.entry_df_icms.grid(sticky="we", column=2, row=3, padx=5, columnspan=2)

        Label(self.tab_impostos, text="DIF. PIS").grid(sticky=W, column=4, row=2, padx=5)
        self.entry_df_icms = Entry(self.tab_impostos, textvariable=self.dif_pis)
        self.entry_df_icms.grid(sticky="we", column=4, row=3, padx=5, columnspan=2)

        Label(self.tab_impostos, text="DIF. COFINS").grid(sticky=W, column=6, row=2, padx=5)
        self.entry_df_icms = Entry(self.tab_impostos, textvariable=self.dif_cofins)
        self.entry_df_icms.grid(sticky="we", column=6, row=3, padx=5, columnspan=2)

        Label(self.tab_impostos, text="CFOP").grid(sticky=W, row=4, padx=5)
        self.entry_df_icms = Entry(self.tab_impostos, textvariable=self.cfop, width=12)
        self.entry_df_icms.grid(sticky="we", row=5, padx=5, columnspan=2)

        Label(self.tab_impostos, text="COD. IMPOSTO").grid(sticky=W, column=2, row=4, padx=5)
        self.entry_df_icms = Entry(self.tab_impostos, textvariable=self.codigo_imposto)
        self.entry_df_icms.grid(sticky="we", column=2, row=5, padx=5, columnspan=2)

        Button(self.tab_impostos, text='Adicionar', command=self.inserir_item_remessa) \
            .grid(sticky="we", row=6, padx=5, pady=5, columnspan=2)

        Button(self.tab_impostos, text='Remover', command=self.eliminar_item_remessas) \
            .grid(sticky="we", column=2, row=6, padx=5, pady=5, columnspan=2)

        self.treeview_itens = Treeview(self.tab_impostos, height=4,
                                       column=("c0", "c1", "c2", "c3", "c4", "c5", "c6"), show="headings")
        self.treeview_itens.heading("#1", text="COD. PRODUTO")
        self.treeview_itens.heading("#2", text="ICMS")
        self.treeview_itens.heading("#3", text="IPI")
        self.treeview_itens.heading("#4", text="PIS")
        self.treeview_itens.heading("#5", text="COFINS")
        self.treeview_itens.heading("#6", text="CFOP")
        self.treeview_itens.heading("#7", text="IMPOSTO")

        self.treeview_itens.column("c0", width=120, stretch=NO, anchor=CENTER)
        self.treeview_itens.column("c1", width=70, stretch=NO, anchor=CENTER)
        self.treeview_itens.column("c2", width=70, stretch=NO, anchor=CENTER)
        self.treeview_itens.column("c3", width=70, stretch=NO, anchor=CENTER)
        self.treeview_itens.column("c4", width=70, stretch=NO, anchor=CENTER)
        self.treeview_itens.column("c5", width=70, stretch=NO, anchor=CENTER)
        self.treeview_itens.column("c6", width=70, stretch=NO, anchor=CENTER)

        self.treeview_itens.grid(sticky="we", row=7, padx=5, pady=(5, 0), columnspan=8)

    def inserir_item_remessa(self):
        pass

    def eliminar_item_remessas(self):
        pass

    def cadastrar_novo_produto(self):
        pass

    def editar_produto(self):
        pass

    def converter_para_maiusculo(self, event):
        pass

    def salvar_produto(self):
        if self.verificar_campos_obrigatorios():
            # verifando se o produto possui id
            if self.produto_atual is None or self.produto_atual.id_produto is None:
                self.salvar()
            else:
                self.atualizar()

    def salvar(self):
        self.produto_atual = Produto(codigo=self.codigo.get(),
                                     nome=self.nome.get(),
                                     deposito=self.deposito.get(),
                                     lote=self.lote.get(),
                                     inspecao_veiculo=self.inspecao_veiculo.get(),
                                     inspecao_produto=self.inspecao_produto.get(),
                                     remover_a=self.remover_a.get())
        try:
            ProdutoService.inserir_produto(self.produto_atual)
            messagebox.showinfo("Sucesso", "Produto salvo com sucesso!")
            self.app_main.destroy()
        except Exception as e:
            messagebox.showerror("Erro", "Erro ao salvar produto\n{}".format(e))

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
        if self.codigo.get() == "":
            messagebox.showerror("Campo obrigatório", "O campo 'código' é obrigatório!")
            return False
        if self.nome.get() == "":
            messagebox.showerror("Campo obrigatório", "O campo 'nome' é obrigatório!")
            return False
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


if __name__ == '__main__':
    app_main = tkinter.Tk()
    CadastroTipoCarregamento(app_main)
    app_main.mainloop()
