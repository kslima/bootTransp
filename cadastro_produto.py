import tkinter
from tkinter import StringVar, Label, Entry, Button, W, Checkbutton, messagebox
import service
from model import Produto


class CadastroProduto:

    def __init__(self, master):
        self.app_main = tkinter.Toplevel(master)
        self.app_main.title("Cadastro de Produto")

        self.atualizando_cadastro = False

        self.codigo = StringVar()
        self.nome = StringVar()
        self.deposito = StringVar()
        self.lote = StringVar()
        self.inspecao_produto = StringVar()
        self.inspecao_veiculo = StringVar()
        self.remover_a = StringVar()

        Label(self.app_main, text="Código: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=0, padx=10)
        self.txt_codigo = Entry(self.app_main, textvariable=self.codigo)
        self.txt_codigo.grid(sticky='we', column=0, row=1, padx=10, columnspan=2)
        self.txt_codigo.bind("<KeyRelease>", self.codigo_somento_numero)

        Label(self.app_main, text="Nome: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=2, padx=10)
        self.txt_nome = Entry(self.app_main, textvariable=self.nome)
        self.txt_nome.grid(sticky='we', column=0, row=3, padx=10, columnspan=2)
        self.txt_nome.bind("<KeyRelease>", self.converter_nome_maiusculo)

        Label(self.app_main, text="Deposito: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=4, padx=10)
        self.txt_deposito = Entry(self.app_main, textvariable=self.deposito)
        self.txt_deposito.grid(sticky='we', column=0, row=5, padx=10)
        self.txt_deposito.bind("<KeyRelease>", self.converter_deposito_maiusculo)

        Label(self.app_main, text="Lote: ", font=(None, 8, 'normal')).grid(sticky=W, column=1, row=4, padx=10)
        self.txt_lote = Entry(self.app_main, textvariable=self.lote)
        self.txt_lote.grid(sticky='we', column=1, row=5, padx=10)
        self.txt_lote.bind("<KeyRelease>", self.converter_lote_maiusculo)

        self.inspecao_veiculo.set("s")
        self.cb_inspecao_veiculo = Checkbutton(self.app_main, text="Inspeção veículo (07)", onvalue="s", offvalue="n",
                                               variable=self.inspecao_veiculo)
        self.cb_inspecao_veiculo.grid(sticky=W, column=0, row=6, padx=5)

        self.inspecao_produto.set("n")
        self.cb_inspecao_produto = Checkbutton(self.app_main, text="Inspeção produto (89)", onvalue="s", offvalue="n",
                                               variable=self.inspecao_produto)
        self.cb_inspecao_produto.grid(sticky=W, column=0, row=7, padx=5)

        self.remover_a.set("n")
        self.cb_remover_a = Checkbutton(self.app_main, text="Remover 'A'", onvalue="s", offvalue="n",
                                        variable=self.remover_a)
        self.cb_remover_a.grid(sticky=W, column=0, row=8, padx=5)

        Button(self.app_main, text='Salvar', command=self.salvar_produto).grid(sticky='we', column=0, row=9, padx=10, pady=10)

    def codigo_somento_numero(self, *args):
        if not self.codigo.get().isdigit():
            self.codigo.set(''.join(x for x in self.codigo.get() if x.isdigit()))

    def converter_nome_maiusculo(self, event):
        self.nome.set(self.nome.get().upper())

    def converter_lote_maiusculo(self, event):
        self.lote.set(self.lote.get().upper())

    def converter_deposito_maiusculo(self, event):
        self.deposito.set(self.deposito.get().upper())

    def salvar_produto(self):
        if self.verificar_campos_obrigatorios():
            novo_produto = Produto()
            novo_produto.codigo = self.codigo.get()
            novo_produto.nome = self.nome.get()
            novo_produto.deposito = self.deposito.get()
            novo_produto.lote = self.lote.get()
            novo_produto.inspecao_veiculo = self.inspecao_veiculo.get()
            novo_produto.inspecao_produto = self.inspecao_produto.get()
            novo_produto.remover_a = self.remover_a.get()

            if self.atualizando_cadastro:
                self.atualizar_produto(novo_produto)

            else:
                cadastrado = service.cadastrar_produto_se_nao_exister(novo_produto)
                if cadastrado[0] == 1:
                    messagebox.showinfo("Sucesso", cadastrado[1])
                    self.app_main.destroy()
                else:
                    messagebox.showerror("Erro", cadastrado[1])

    def atualizar_produto(self, produto_para_atualizar):
        produto_atualizado = service.atualizar_produto(produto_para_atualizar)
        if produto_atualizado:
            messagebox.showinfo("Sucesso", produto_atualizado[1])
            self.app_main.destroy()

        else:
            messagebox.showerror("Erro", produto_atualizado[1])

    def verificar_campos_obrigatorios(self):
        if self.codigo.get() == "":
            messagebox.showerror("Campo obrigatório", "O campo 'código' é obrigatório!")
            return False
        if self.nome.get() == "":
            messagebox.showerror("Campo obrigatório", "O campo 'nome' é obrigatório!")
            return False
        return True

    def setar_campos_para_edicao(self, produto_para_editar):
        self.codigo.set(produto_para_editar.codigo)
        self.nome.set(produto_para_editar.nome)
        self.deposito.set(produto_para_editar.deposito)
        self.lote.set(produto_para_editar.lote)
        self.inspecao_veiculo.set(produto_para_editar.inspecao_veiculo)
        self.inspecao_produto.set(produto_para_editar.inspecao_produto)
        self.remover_a.set(produto_para_editar.remover_a)
