import tkinter
from tkinter import StringVar, Label, Entry, Button, W, Checkbutton, messagebox, DISABLED
from tkinter.ttk import Notebook, Frame, Radiobutton

from service import ProdutoService
from model import Produto
from utilitarios import NumberUtils, StringUtils


class CadastroProduto:

    def __init__(self, master):
        self.app_main = tkinter.Toplevel(master)
        self.app_main.title("Cadastro de Produto")
        self.centralizar_tela()

        self.atualizando_cadastro = False
        self.produto_atual = None
        # tabs
        self.tabControl = Notebook(self.app_main, width=430)
        self.tabControl.grid(sticky="we", row=0, padx=10, pady=10, columnspan=4)
        self.tab_produto = None
        self.tab_transporte = None
        self.txt_codigo = None
        self.txt_nome = None
        self.txt_deposito = None
        self.txt_lote = None
        self.cb_inspecao_veiculo = None
        self.cb_inspecao_produto = None
        self.cb_remover_a = None
        self.entry_ordem = None
        self.entry_pedido = None
        self.entry_tipo_frete = None
        self.entry_destino_frete = None
        self.entry_codigo_transportador = None
        self.entry_docs_diversos = None
        self.rb_nao_informar_lacres = None
        self.rb_informar_lacres_lona = None
        self.rb_informar_lacres = None

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

        self.codigo = StringVar()
        self.nome = StringVar()
        self.deposito = StringVar()
        self.lote = StringVar()
        self.inspecao_produto = StringVar()
        self.inspecao_veiculo = StringVar()
        self.tipo_lacre = tkinter.IntVar()
        self.remover_a = StringVar()
        self.ordem = StringVar()
        self.pedido = StringVar()
        self.tipo_frete = StringVar()
        self.destino_frete = StringVar()
        self.codigo_transportador = StringVar()

        Button(self.app_main, text='Salvar', command=self.salvar_produto).grid(sticky='we', row=1, padx=(10, 5),
                                                                               pady=10)
        self.botao_deletar = Button(self.app_main, text='Excluir', command=self.deletar, state=DISABLED)
        self.botao_deletar.grid(sticky='we', column=1, row=1, padx=(5, 10), pady=10)

        self.criar_aba_geral()
        self.criar_aba_transporte()

    def criar_aba_geral(self):
        self.tab_produto = Frame(self.tabControl)
        self.tabControl.add(self.tab_produto, text="Principal")

        container_produto = tkinter.LabelFrame(self.tab_produto, text='Produto')
        container_produto.grid(sticky='we', padx=10, columnspan=3, ipady=5, pady=5)

        Label(container_produto, text="Código").grid(sticky=W, row=0, padx=10)
        self.txt_codigo = Entry(container_produto, textvariable=self.codigo)
        self.txt_codigo.grid(sticky='we', row=1, padx=10)
        self.txt_codigo.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_inteiro), '%P'))

        Label(container_produto, text="Nome").grid(sticky=W, row=2, padx=10)
        self.txt_nome = Entry(container_produto, textvariable=self.nome)
        self.txt_nome.grid(sticky='we', row=3, padx=10, columnspan=4)
        self.txt_nome.bind("<KeyRelease>", self.converter_nome_maiusculo)

        Label(container_produto, text="Deposito").grid(sticky=W, row=4, padx=10)
        self.txt_deposito = Entry(container_produto, textvariable=self.deposito)
        self.txt_deposito.grid(sticky='we', row=5, padx=10, pady=(0, 10), columnspan=2)
        self.txt_deposito.bind("<KeyRelease>", self.converter_deposito_maiusculo)

        Label(container_produto, text="Lote").grid(sticky=W, column=2, row=4, padx=10)
        self.txt_lote = Entry(container_produto, textvariable=self.lote)
        self.txt_lote.grid(sticky='we', column=2, row=5, padx=10, pady=(0, 10), columnspan=2)
        self.txt_lote.bind("<KeyRelease>", self.converter_lote_maiusculo)

        container_dir_fiscais = tkinter.LabelFrame(self.tab_produto, text='Direitos Fiscais')
        container_dir_fiscais.grid(sticky='we', padx=10, ipady=5, pady=5)

        Label(container_dir_fiscais, text="DIF. ICMS").grid(sticky=W, row=6, padx=10)
        self.entry_df_icms = Entry(container_dir_fiscais, textvariable=self.dif_icms)
        self.entry_df_icms.bind('<KeyRelease>', lambda ev: StringUtils.to_upper_case(ev, self.dif_icms))
        self.entry_df_icms.grid(sticky="we", row=7, padx=10)

        Label(container_dir_fiscais, text="DIF. IPI").grid(sticky=W, column=1, row=6, padx=10)
        self.entry_df_ipi = Entry(container_dir_fiscais, textvariable=self.dif_ipi)
        self.entry_df_ipi.bind('<KeyRelease>', lambda ev: StringUtils.to_upper_case(ev, self.dif_ipi))
        self.entry_df_ipi.grid(sticky="we", column=1, row=7, padx=10)

        Label(container_dir_fiscais, text="DIF. PIS").grid(sticky=W, column=0, row=8, padx=10)
        self.entry_df_pis = Entry(container_dir_fiscais, textvariable=self.dif_pis)
        self.entry_df_pis.bind('<KeyRelease>', lambda ev: StringUtils.to_upper_case(ev, self.dif_pis))
        self.entry_df_pis.grid(sticky="we", column=0, row=9, padx=10)

        Label(container_dir_fiscais, text="DIF. COFINS").grid(sticky=W, column=1, row=8, padx=10)
        self.entry_df_cofins = Entry(container_dir_fiscais, textvariable=self.dif_cofins)
        self.entry_df_cofins.bind('<KeyRelease>', lambda ev: StringUtils.to_upper_case(ev, self.dif_cofins))
        self.entry_df_cofins.grid(sticky="we", column=1, row=9, padx=10)

        Label(container_dir_fiscais, text="CFOP").grid(sticky=W, column=0, row=10, padx=10)
        self.entry_cfop = Entry(container_dir_fiscais, textvariable=self.cfop)
        self.entry_cfop.bind('<KeyRelease>', lambda ev: StringUtils.to_upper_case(ev, self.cfop))
        self.entry_cfop.grid(sticky="we", column=0, row=11, padx=10)

        Label(container_dir_fiscais, text="COD. IMPOSTO").grid(sticky=W, column=1, row=10, padx=10)
        self.entry_df_cofins = Entry(container_dir_fiscais, textvariable=self.codigo_imposto)
        self.entry_df_cofins.bind('<KeyRelease>', lambda ev: StringUtils.to_upper_case(ev, self.codigo_imposto))
        self.entry_df_cofins.grid(sticky="we", column=1, row=11, padx=10)

    def criar_aba_transporte(self):
        self.tab_transporte = Frame(self.tabControl)
        self.tabControl.add(self.tab_transporte, text="Transporte")

        self.inspecao_veiculo.set(1)
        self.cb_inspecao_veiculo = Checkbutton(self.tab_transporte, text="Inspeção veículo (07)", onvalue=1, offvalue=0,
                                               variable=self.inspecao_veiculo)
        self.cb_inspecao_veiculo.grid(sticky=W, row=2, padx=5, columnspan=2)

        self.inspecao_produto.set(0)
        self.cb_inspecao_produto = Checkbutton(self.tab_transporte, text="Inspeção produto (89)", onvalue=1, offvalue=0,
                                               variable=self.inspecao_produto)
        self.cb_inspecao_produto.grid(sticky=W, row=3, padx=5, columnspan=2)

        self.remover_a.set(0)
        self.cb_remover_a = Checkbutton(self.tab_transporte, text="Remover 'A'", onvalue=1, offvalue=0,
                                        variable=self.remover_a)
        self.cb_remover_a.grid(sticky=W, row=4, padx=5, columnspan=2)

        container_lacres = tkinter.LabelFrame(self.tab_transporte, text='Lacres')
        container_lacres.grid(sticky='we', column=0, row=5, padx=10, columnspan=3, ipady=5, pady=5)

        self.tipo_lacre.set(0)
        self.rb_nao_informar_lacres = Radiobutton(container_lacres, text="Nenhum", value=0,
                                                  variable=self.tipo_lacre)
        self.rb_nao_informar_lacres.grid(sticky="we", padx=5)

        self.rb_informar_lacres = Radiobutton(container_lacres, text="Lacres", value=1,
                                              variable=self.tipo_lacre)
        self.rb_informar_lacres.grid(sticky="we", row=0, column=1, padx=5)

        self.rb_informar_lacres_lona = Radiobutton(container_lacres, text="Lona", value=2,
                                                   variable=self.tipo_lacre)
        self.rb_informar_lacres_lona.grid(sticky="we", row=0, column=2, padx=5)

        Label(self.tab_transporte, text="Ordem").grid(sticky=W, row=6, padx=10)
        self.entry_ordem = Entry(self.tab_transporte, textvariable=self.ordem)
        self.entry_ordem.grid(sticky='we', row=7, padx=10, pady=(0, 10))
        self.entry_ordem.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_inteiro), '%P'))

        Label(self.tab_transporte, text="Pedido de frete").grid(sticky=W, column=1, row=6, padx=10)
        self.entry_pedido = Entry(self.tab_transporte, textvariable=self.pedido)
        self.entry_pedido.grid(sticky='we', column=1, row=7, pady=(0, 10), padx=10, columnspan=2)
        self.entry_pedido.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_inteiro), '%P'))

        Label(self.tab_transporte, text="Tipo frete").grid(sticky=W, row=8, padx=10)
        self.entry_tipo_frete = Entry(self.tab_transporte, textvariable=self.tipo_frete, width=20)
        self.entry_tipo_frete.grid(sticky=W, row=9, padx=10, ipady=1)
        self.entry_tipo_frete.bind('<KeyRelease>', lambda ev: StringUtils.to_upper_case(ev, self.tipo_frete))

        Label(self.tab_transporte, text="Compl. frete").grid(sticky=W, column=1, row=8, padx=10)
        self.entry_destino_frete = Entry(self.tab_transporte, textvariable=self.destino_frete, width=20)
        self.entry_destino_frete.grid(sticky=W, column=1, row=9, padx=10, ipady=1)
        self.entry_destino_frete.bind('<KeyRelease>', lambda ev: StringUtils.to_upper_case(ev, self.destino_frete))

        Label(self.tab_transporte, text="Código transportador").grid(sticky=W, column=2, row=8, padx=10)
        self.entry_codigo_transportador = Entry(self.tab_transporte, textvariable=self.codigo_transportador, width=20)
        self.entry_codigo_transportador.grid(sticky=W, column=2, row=9, padx=10, ipady=1)
        self.entry_codigo_transportador.config(validate="key", validatecommand=(self.app_main
                                                                                .register(NumberUtils.eh_inteiro),
                                                                                '%P'))

        Label(self.tab_transporte, text="Docs. Diversos: ").grid(sticky=W, row=10, padx=10, pady=(5, 0))

        self.entry_docs_diversos = tkinter.Text(self.tab_transporte, height=3, width=51)
        self.entry_docs_diversos.grid(sticky=W, row=11, padx=10, pady=(0, 15), columnspan=3)

    def centralizar_tela(self):
        # Gets the requested values of the height and widht.
        window_width = self.app_main.winfo_reqwidth()
        window_height = self.app_main.winfo_reqheight()

        # Gets both half the screen width/height and window width/height
        position_right = int(self.app_main.winfo_screenwidth() / 2.3 - window_width / 2)
        position_down = int(self.app_main.winfo_screenheight() / 3 - window_height / 2)

        # Positions the window in the center of the page.
        self.app_main.geometry("+{}+{}".format(position_right, position_down))

    def converter_nome_maiusculo(self, event):
        self.nome.set(self.nome.get().upper())

    def converter_lote_maiusculo(self, event):
        self.lote.set(self.lote.get().upper())

    def converter_deposito_maiusculo(self, event):
        self.deposito.set(self.deposito.get().upper())

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
    CadastroProduto(app_main)
    app_main.mainloop()
