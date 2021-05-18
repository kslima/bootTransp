import tkinter
from tkinter import StringVar, Label, Entry, Button, W, Checkbutton, messagebox, DISABLED
from tkinter.ttk import Notebook, Frame

from service import ProdutoService
from model import Produto
from utilitarios import NumberUtils


class CadastroProduto:

    def __init__(self, master):
        self.app_main = tkinter.Toplevel(master)
        self.app_main.title("Cadastro de Produto")
        self.centralizar_tela()

        self.atualizando_cadastro = False
        self.produto_atual = None
        # tabs
        self.tabControl = Notebook(self.app_main)
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

        self.codigo = StringVar()
        self.nome = StringVar()
        self.deposito = StringVar()
        self.lote = StringVar()
        self.inspecao_produto = StringVar()
        self.inspecao_veiculo = StringVar()
        self.remover_a = StringVar()

        Button(self.app_main, text='Salvar', command=self.salvar_produto).grid(sticky='we', row=1, padx=(10, 5),
                                                                               pady=10)
        self.botao_deletar = Button(self.app_main, text='Excluir', command=self.deletar, state=DISABLED)
        self.botao_deletar.grid(sticky='we', column=1, row=1, padx=(5, 10), pady=10)

        self.criar_aba_geral()
        self.criar_aba_transporte()

    def criar_aba_geral(self):
        self.tab_produto = Frame(self.tabControl)
        self.tabControl.add(self.tab_produto, text="Produto")

        Label(self.tab_produto, text="Código: ", font=(None, 8, 'normal')).grid(sticky=W, row=0, padx=10)
        self.txt_codigo = Entry(self.tab_produto, textvariable=self.codigo)
        self.txt_codigo.grid(sticky='we', row=1, padx=10, columnspan=2)
        self.txt_codigo.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_inteiro), '%P'))

        Label(self.tab_produto, text="Nome: ", font=(None, 8, 'normal')).grid(sticky=W, row=2, padx=10)
        self.txt_nome = Entry(self.tab_produto, textvariable=self.nome)
        self.txt_nome.grid(sticky='we', row=3, padx=10, columnspan=2)
        self.txt_nome.bind("<KeyRelease>", self.converter_nome_maiusculo)

        Label(self.tab_produto, text="Deposito: ", font=(None, 8, 'normal')).grid(sticky=W, row=4, padx=10)
        self.txt_deposito = Entry(self.tab_produto, textvariable=self.deposito)
        self.txt_deposito.grid(sticky='we', row=5, padx=10, pady=(0, 10))
        self.txt_deposito.bind("<KeyRelease>", self.converter_deposito_maiusculo)

        Label(self.tab_produto, text="Lote: ", font=(None, 8, 'normal')).grid(sticky=W, column=1, row=4, padx=10)
        self.txt_lote = Entry(self.tab_produto, textvariable=self.lote)
        self.txt_lote.grid(sticky='we', column=1, row=5, padx=10, pady=(0, 10))
        self.txt_lote.bind("<KeyRelease>", self.converter_lote_maiusculo)

    def criar_aba_transporte(self):
        self.tab_transporte = Frame(self.tabControl)
        self.tabControl.add(self.tab_transporte, text="Transporte")

        self.inspecao_veiculo.set(1)
        self.cb_inspecao_veiculo = Checkbutton(self.tab_transporte, text="Inspeção veículo (07)", onvalue=1, offvalue=0,
                                               variable=self.inspecao_veiculo)
        self.cb_inspecao_veiculo.grid(sticky=W, row=2, padx=5)

        self.inspecao_produto.set(0)
        self.cb_inspecao_produto = Checkbutton(self.tab_transporte, text="Inspeção produto (89)", onvalue=1, offvalue=0,
                                               variable=self.inspecao_produto)
        self.cb_inspecao_produto.grid(sticky=W, row=3, padx=5)

        self.remover_a.set(0)
        self.cb_remover_a = Checkbutton(self.tab_transporte, text="Remover 'A'", onvalue=1, offvalue=0,
                                        variable=self.remover_a)
        self.cb_remover_a.grid(sticky=W, row=4, padx=5)

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
