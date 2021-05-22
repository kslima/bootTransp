import tkinter
from tkinter import StringVar, Label, Entry, Button, W, Checkbutton, messagebox, DISABLED, END, INSERT
from tkinter.ttk import Notebook, Frame, Radiobutton, Combobox

from service import ProdutoService
from model2 import Produto
from utilitarios import NumberUtils, StringUtils


class CadastroProduto:

    def __init__(self, master):
        self.app_main = tkinter.Toplevel(master)
        self.app_main.title("Cadastro de Produto")
        self.centralizar_tela()

        self.atualizando_cadastro = False
        self.produto_atual = None
        # tabs
        self.tabControl = Notebook(self.app_main)
        self.tabControl.grid(sticky="we", row=1, padx=10, pady=10, columnspan=4)
        self.tab_produto = None
        self.tab_transporte = None
        self.txt_codigo = None
        self.txt_nome = None
        self.txt_deposito = None
        self.txt_lote = None
        self.cb_inspecao_veiculo = None
        self.cbo_tipo_inspecao_veiculo = None
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
        self.canal_distribuicao = StringVar()
        self.setor_atividade = StringVar()

        self.codigo = StringVar()
        self.nome = StringVar()
        self.deposito = StringVar()
        self.lote = StringVar()
        self.inspecao_produto = tkinter.IntVar()
        self.tipo_inspecao_veiculo = StringVar()
        self.inspecao_veiculo = tkinter.IntVar()
        self.tipo_lacre = tkinter.IntVar()
        self.remover_a = tkinter.IntVar()
        self.ordem = StringVar()
        self.pedido = StringVar()
        self.tipo_frete = StringVar()
        self.complemento_tipo_frete = StringVar()
        self.codigo_transportador = StringVar()

        Button(self.app_main, text='Salvar', command=self.salvar_produto).grid(sticky='we', row=2, padx=(10, 5),
                                                                               pady=10)
        self.botao_deletar = Button(self.app_main, text='Excluir', command=self.deletar, state=DISABLED)
        self.botao_deletar.grid(sticky='we', column=1, row=2, padx=(5, 10), pady=10)

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

        Label(container_produto, text="Nome").grid(sticky=W, column=1, row=0, padx=10)
        self.txt_nome = Entry(container_produto, textvariable=self.nome)
        self.txt_nome.grid(sticky='we', column=1, row=1, padx=10, columnspan=3)
        self.txt_nome.bind("<KeyRelease>", self.converter_nome_maiusculo)

        Label(container_produto, text="Deposito").grid(sticky=W, column=0, row=2, padx=10)
        self.txt_deposito = Entry(container_produto, textvariable=self.deposito)
        self.txt_deposito.grid(sticky='we', column=0, row=3, padx=10)
        self.txt_deposito.bind("<KeyRelease>", self.converter_deposito_maiusculo)

        Label(container_produto, text="Lote").grid(sticky=W, column=1, row=2, padx=10)
        self.txt_lote = Entry(container_produto, textvariable=self.lote)
        self.txt_lote.grid(sticky='we', column=1, row=3, padx=10)
        self.txt_lote.bind("<KeyRelease>", self.converter_lote_maiusculo)

        Label(container_produto, text="CFOP").grid(sticky=W, column=2, row=2, padx=10)
        self.entry_cfop = Entry(container_produto, textvariable=self.cfop)
        self.entry_cfop.bind('<KeyRelease>', lambda ev: StringUtils.to_upper_case(ev, self.cfop))
        self.entry_cfop.grid(sticky="we", column=2, row=3, padx=10)

        Label(container_produto, text="COD. IMPOSTO").grid(sticky=W, column=3, row=2, padx=10)
        self.entry_df_cofins = Entry(container_produto, textvariable=self.codigo_imposto)
        self.entry_df_cofins.bind('<KeyRelease>', lambda ev: StringUtils.to_upper_case(ev, self.codigo_imposto))
        self.entry_df_cofins.grid(sticky="we", column=3, row=3, padx=10)

        Label(container_produto, text="DIF. ICMS").grid(sticky=W, row=4, padx=10)
        self.entry_df_icms = Entry(container_produto, textvariable=self.dif_icms)
        self.entry_df_icms.bind('<KeyRelease>', lambda ev: StringUtils.to_upper_case(ev, self.dif_icms))
        self.entry_df_icms.grid(sticky="we", row=5, padx=10)

        Label(container_produto, text="DIF. IPI").grid(sticky=W, column=1, row=4, padx=10)
        self.entry_df_ipi = Entry(container_produto, textvariable=self.dif_ipi)
        self.entry_df_ipi.bind('<KeyRelease>', lambda ev: StringUtils.to_upper_case(ev, self.dif_ipi))
        self.entry_df_ipi.grid(sticky="we", column=1, row=5, padx=10)

        Label(container_produto, text="DIF. PIS").grid(sticky=W, column=2, row=4, padx=10)
        self.entry_df_pis = Entry(container_produto, textvariable=self.dif_pis)
        self.entry_df_pis.bind('<KeyRelease>', lambda ev: StringUtils.to_upper_case(ev, self.dif_pis))
        self.entry_df_pis.grid(sticky="we", column=2, row=5, padx=10)

        Label(container_produto, text="DIF. COFINS").grid(sticky=W, column=3, row=4, padx=10)
        self.entry_df_cofins = Entry(container_produto, textvariable=self.dif_cofins)
        self.entry_df_cofins.bind('<KeyRelease>', lambda ev: StringUtils.to_upper_case(ev, self.dif_cofins))
        self.entry_df_cofins.grid(sticky="we", column=3, row=5, padx=10)

        Label(container_produto, text="Canal distribuição: ").grid(sticky=W, column=0, row=6, padx=5)
        Combobox(container_produto, textvariable=self.canal_distribuicao, state="readonly") \
            .grid(sticky="we", column=0, row=7, padx=5, columnspan=2)

        Label(container_produto, text="Setor de atividade: ").grid(sticky=W, column=2, row=6, padx=5)
        Combobox(container_produto, textvariable=self.setor_atividade, state="readonly") \
            .grid(sticky="we", column=2, row=7, padx=5, columnspan=2)

    def criar_aba_transporte(self):
        self.tab_transporte = Frame(self.tabControl)
        self.tabControl.add(self.tab_transporte, text="Transporte")

        self.inspecao_veiculo.set(0)
        self.cb_inspecao_veiculo = Checkbutton(self.tab_transporte, text="Inspeção veículo (07)", onvalue=1, offvalue=0,
                                               variable=self.inspecao_veiculo)
        self.cb_inspecao_veiculo.grid(sticky=W, row=2, padx=5, columnspan=2)

        frame = Frame(self.tab_transporte)
        frame.grid(sticky=W, column=1, row=2, pady=(5, 0), padx=5, columnspan=2)
        Label(frame, text="Tipo : ").grid(sticky=W)
        self.cbo_tipo_inspecao_veiculo = Combobox(frame, textvariable=self.tipo_inspecao_veiculo,
                                                  state="readonly")
        self.cbo_tipo_inspecao_veiculo['values'] = ['INSPVEICACUCAR', 'INSPVEICALCOOL']
        self.cbo_tipo_inspecao_veiculo.grid(sticky=W, column=1, row=0)

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
        self.entry_pedido.grid(sticky='we', column=1, row=7, pady=(0, 10), padx=10)
        self.entry_pedido.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_inteiro), '%P'))

        Label(self.tab_transporte, text="Icoterms").grid(sticky=W, column=0, row=8, padx=10)
        self.entry_tipo_frete = Entry(self.tab_transporte, textvariable=self.tipo_frete)
        self.entry_tipo_frete.grid(sticky="we", column=0, row=9, padx=10, ipady=1)
        self.entry_tipo_frete.bind('<KeyRelease>', lambda ev: StringUtils.to_upper_case(ev, self.tipo_frete))

        Label(self.tab_transporte, text="Icoterms2").grid(sticky=W, column=1, row=8, padx=10)
        self.entry_destino_frete = Entry(self.tab_transporte, textvariable=self.complemento_tipo_frete, width=20)
        self.entry_destino_frete.grid(sticky="we", column=1, row=9, padx=10, ipady=1)
        self.entry_destino_frete.bind('<KeyRelease>', lambda ev: StringUtils.to_upper_case(ev,
                                                                                           self.complemento_tipo_frete))

        Label(self.tab_transporte, text="Código transportador").grid(sticky="we", column=2, row=8, padx=10)
        self.entry_codigo_transportador = Entry(self.tab_transporte, textvariable=self.codigo_transportador, width=20)
        self.entry_codigo_transportador.grid(sticky="we", column=2, row=9, padx=10, ipady=1)
        self.entry_codigo_transportador.config(validate="key", validatecommand=(self.app_main
                                                                                .register(NumberUtils.eh_inteiro),
                                                                                '%P'))

        Label(self.tab_transporte, text="Docs. Diversos: ").grid(sticky=W, row=10, padx=10, pady=(5, 0))

        self.entry_docs_diversos = tkinter.Text(self.tab_transporte, height=3)
        self.entry_docs_diversos.grid(sticky="we", row=11, padx=10, pady=(0, 15), columnspan=3)

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

    def selecionar_produto_pai(self):
        valor = self.salvar_como_sub_item.get()
        if valor == 0:
            self.cb_salvar_como_sub_item['state'] = 'disabled'
        else:
            self.cb_salvar_como_sub_item['state'] = 'normal'

    def salvar_produto(self):
        try:
            self.verificar_campos_obrigatorios()
            if self.produto_atual is None or self.produto_atual.id_produto is None:
                self.salvar()
            else:
                self.atualizar()
        except Exception as e:
            messagebox.showerror('Erro', e)

    def salvar(self):
        self.produto_atual = Produto()
        self.atualizar_dados_produto_atual()
        try:
            ProdutoService.inserir_produto(self.produto_atual)
            messagebox.showinfo("Sucesso", "Produto salvo com sucesso!")
            self.app_main.destroy()
        except Exception as e:
            messagebox.showerror("Erro", "Erro ao salvar produto\n{}".format(e))

    def atualizar(self):
        self.atualizar_dados_produto_atual()
        try:
            ProdutoService.atualizar_produto(self.produto_atual)
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
            self.app_main.destroy()
        except Exception as e:
            messagebox.showerror("Erro", e)

    def atualizar_dados_produto_atual(self):
        self.produto_atual.codigo_sap = self.codigo.get().strip()
        self.produto_atual.nome = self.nome.get().strip()
        self.produto_atual.deposito = self.deposito.get().strip()
        self.produto_atual.lote = self.lote.get().strip()

        self.produto_atual.cfop = self.cfop.get().strip()
        self.produto_atual.df_icms = self.dif_icms.get().strip()
        self.produto_atual.df_ipi = self.dif_ipi.get().strip()
        self.produto_atual.df_pis = self.dif_pis.get().strip()
        self.produto_atual.df_cofins = self.dif_cofins.get().strip()
        self.produto_atual.codigo_imposto = self.codigo_imposto.get().strip()

        self.produto_atual.inspecao_veiculo = self.inspecao_veiculo.get()

        # ----
        self.produto_atual.tipo_inspecao_veiculo = self.tipo_inspecao_veiculo.get()

        self.produto_atual.inspecao_produto = self.inspecao_produto.get()
        self.produto_atual.remover_a = self.remover_a.get()

        self.produto_atual.tipo_lacres = self.tipo_lacre.get()
        self.produto_atual.numero_ordem = self.ordem.get().strip()
        self.produto_atual.pedido_frete = self.pedido.get().strip()
        self.produto_atual.icoterms1 = self.tipo_frete.get().strip()
        self.produto_atual.icoterms2 = self.complemento_tipo_frete.get().strip()
        self.produto_atual.complemento_tipo_frete = self.complemento_tipo_frete.get().strip()

        # -----
        self.produto_atual.transportador = self.codigo_transportador.get().strip()

        self.produto_atual.documentos_diversos = self.entry_docs_diversos.get("1.0", END).strip()

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
        if not self.codigo.get().strip():
            raise RuntimeError("Informe um código para o produto!")

        if not self.nome.get().strip():
            raise RuntimeError("Informe um nome para o produto!")

        if self.inspecao_veiculo.get() == 1 and self.tipo_inspecao_veiculo.get().strip() == '':
            raise RuntimeError("Informe o tipo de inspeção do veículo")

    def setar_campos_para_edicao(self, produto):
        self.botao_deletar['state'] = 'normal'
        self.produto_atual = produto
        self.codigo.set(produto.codigo_sap)
        self.nome.set(produto.nome)
        self.deposito.set(produto.deposito if produto.deposito is not None else '')
        self.lote.set(produto.lote if produto.lote is not None else '')
        self.tipo_inspecao_veiculo.set(produto.tipo_inspecao_veiculo
                                       if produto.tipo_inspecao_veiculo is not None else '')
        self.inspecao_veiculo.set(produto.inspecao_veiculo)
        self.inspecao_produto.set(produto.inspecao_produto)
        self.remover_a.set(produto.remover_a)
        self.cfop.set(produto.cfop if produto.cfop is not None else '')
        self.dif_icms.set(produto.df_icms if produto.df_icms is not None else '')
        self.dif_ipi.set(produto.df_ipi if produto.df_ipi is not None else '')
        self.dif_pis.set(produto.df_pis if produto.df_pis is not None else '')
        self.dif_cofins.set(produto.df_cofins if produto.df_cofins is not None else '')
        self.codigo_imposto.set(produto.codigo_imposto if produto.codigo_imposto is not None else '')
        self.tipo_lacre.set(produto.tipo_lacres)
        self.ordem.set(produto.numero_ordem if produto.numero_ordem is not None else '')
        self.pedido.set(produto.pedido_frete if produto.pedido_frete is not None else '')
        self.tipo_frete.set(produto.tipo_frete if produto.tipo_frete is not None else '')
        self.complemento_tipo_frete.set(produto.complemento_tipo_frete
                                        if produto.complemento_tipo_frete is not None else '')
        self.codigo_transportador.set(produto.codigo_transportador
                                      if produto.codigo_transportador is not None else '')

        self.entry_docs_diversos.delete('1.0', END)
        txt = produto.documentos_diversos
        self.entry_docs_diversos.insert(INSERT, txt if txt is not None else '')


if __name__ == '__main__':
    app_main = tkinter.Tk()
    CadastroProduto(app_main)
    app_main.mainloop()
