import tkinter
from datetime import date, timedelta
from tkinter import StringVar, Label, Entry, Button, W, Checkbutton, messagebox, DISABLED, IntVar, Text, NO, CENTER, \
    END, INSERT, E, ttk
from tkinter.ttk import Notebook, Frame, Radiobutton, Combobox, Treeview

from dateutil.relativedelta import relativedelta
from sapgui import SAPGuiApplication
from service import TipoCarregamentoService
from model import Produto, TipoCarregamento, ItemRemessa, Ordem
from utilitarios import NumberUtils, StringUtils
from zsd020 import ZSD020


class ConsultaSaldo:

    def __init__(self, master, main=None):
        self.app_main = tkinter.Toplevel(master)
        self.app_main.title("Cadastro de Tipo de Carregamento")
        self.app_main.configure(bg='#dfebf5')
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

        self.entry_cnpj = None

        self.entry_data_inicial = None
        self.entry_data_final = None
        self.dif_icms = StringVar()
        self.cnpj = StringVar()
        self.data_inicial = StringVar()
        self.data_final = StringVar()
        self.treeview_itens = None

        self.atualizando_cadastro = False
        self.produto_atual = None

        options = {'font': (None, 9), 'bg': '#dfebf5'}
        Label(self.app_main, text="CNPJ", **options).grid(sticky=W, column=0, row=0, padx=10)
        self.entry_cnpj = Entry(self.app_main, textvariable=self.cnpj)
        self.entry_cnpj.grid(sticky="we", column=0, row=1, padx=10, ipady=2, columnspan=2)
        self.entry_cnpj.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_inteiro), '%P'))

        Label(self.app_main, text="Data Inicial", **options).grid(sticky=W, column=2, row=0, padx=10)
        self.entry_cnpj = Entry(self.app_main, textvariable=self.data_inicial)
        self.entry_cnpj.grid(sticky="we", column=2, row=1, padx=10, ipady=2)

        Label(self.app_main, text="Data Final", **options).grid(sticky=W, column=3, row=0, padx=10)
        self.entry_cnpj = Entry(self.app_main, textvariable=self.data_final)
        self.entry_cnpj.grid(sticky="we", column=3, row=1, padx=10, ipady=2)

        Button(self.app_main, text='Pesquisar', command=self.consultar_saldo) \
            .grid(sticky="we", column=4, row=1)

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

        self.treeview_itens.grid(sticky="we", row=7, padx=10, pady=5, columnspan=10)

        Label(self.app_main, text="Quantidade: ", **options).grid(sticky=W, row=8, padx=10)
        self.entry_data_inicial = Entry(self.app_main, textvariable=self.quantidade_item_remessa)
        self.entry_data_inicial.grid(sticky="we", row=9, column=0, padx=10, ipady=2, pady=(0, 15))
        self.entry_data_inicial.config(validate="key",
                                       validatecommand=(self.app_main.register(NumberUtils.eh_decimal), '%P'))

        Button(self.app_main, text='Inserir', command=self.inserir_main) \
            .grid(sticky="we", column=1, row=9, pady=(0, 15))

        self.setar_datas()

    def centralizar_tela(self):
        # Gets the requested values of the height and widht.
        window_width = self.app_main.winfo_reqwidth()
        window_height = self.app_main.winfo_reqheight()

        # Gets both half the screen width/height and window width/height
        position_right = int(self.app_main.winfo_screenwidth() / 2.3 - window_width / 2)
        position_down = int(self.app_main.winfo_screenheight() / 3 - window_height / 2)

        # Positions the window in the center of the page.
        self.app_main.geometry("+{}+{}".format(position_right, position_down))

    def setar_datas(self):
        hoje = date.today()
        hoje_formatado = hoje.strftime("%d.%m.%Y")
        data_inicial = hoje - relativedelta(years=1)
        data_inicial_formatada = data_inicial.strftime("%d.%m.%Y")
        self.data_inicial.set(data_inicial_formatada)
        self.data_final.set(hoje_formatado)

    def consultar_saldo(self):
        session = SAPGuiApplication.connect()
        ordens = ZSD020.consultar_saldo_cliente(session, self.cnpj.get(),
                                                self.data_inicial.get(),
                                                self.data_final.get())
        self.inserir_item_remessa(ordens)

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
        self.main.inserir_item_remessa(None)

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

    def verificar_campos_obrigatorios(self):
        return True

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
