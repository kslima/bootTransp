import tkinter
from tkinter import StringVar, Label, Entry, Button, W, Checkbutton, messagebox
from tkinter.ttk import Combobox

import service
from model import Produto


class CadastroVeiculo:

    def __init__(self):
        # self.app_main = tkinter.Toplevel(master)
        self.app_main = tkinter.Tk()
        self.app_main.title("Cadastro de Veículo")

        self.atualizando_cadastro = False

        self.codigo = StringVar()
        self.nome = StringVar()
        self.deposito = StringVar()
        self.lote = StringVar()
        self.inspecao_produto = StringVar()
        self.inspecao_veiculo = StringVar()
        self.remover_a = StringVar()

        Label(self.app_main, text="Tipo Veículo: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=0, padx=5)
        self.txt_codigo = Combobox(self.app_main, textvariable=self.codigo, width=10)
        self.txt_codigo.grid(sticky=W, column=0, row=1, padx=5)
        self.txt_codigo.bind("<KeyRelease>", self.codigo_somento_numero)

        Label(self.app_main, text="Peso Balança: ", font=(None, 8, 'normal')).grid(sticky=W, column=1, row=0, padx=5)
        self.txt_nome = Combobox(self.app_main, textvariable=self.nome, width=10)
        self.txt_nome.grid(sticky="we", column=1, row=1, padx=5)
        self.txt_nome.bind("<KeyRelease>", self.converter_nome_maiusculo)

        Label(self.app_main, text="Placa 1: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=3, padx=5)
        self.txt_lote = Entry(self.app_main, textvariable=self.lote, width=13)
        self.txt_lote.grid(sticky=W, column=0, row=4, padx=5)
        self.txt_lote.bind("<KeyRelease>", self.converter_lote_maiusculo)

        Label(self.app_main, text="Município Placa 1: ", font=(None, 8, 'normal')).grid(sticky=W, column=1, row=3,
                                                                                        padx=5)
        self.txt_lote = Entry(self.app_main, textvariable=self.lote, width=20)
        self.txt_lote.grid(sticky=W, column=1, row=4, padx=(5, 10))
        self.txt_lote.bind("<KeyRelease>", self.converter_lote_maiusculo)

        Label(self.app_main, text="Placa 2: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=5, padx=5)
        self.txt_lote = Entry(self.app_main, textvariable=self.lote, width=13)
        self.txt_lote.grid(sticky=W, column=0, row=6, padx=5)
        self.txt_lote.bind("<KeyRelease>", self.converter_lote_maiusculo)

        Label(self.app_main, text="Município Placa 2: ", font=(None, 8, 'normal')).grid(sticky=W, column=1,
                                                                                        row=5, padx=5)
        self.txt_lote = Entry(self.app_main, textvariable=self.lote, width=20)
        self.txt_lote.grid(sticky=W, column=1, row=6, padx=(5, 10))
        self.txt_lote.bind("<KeyRelease>", self.converter_lote_maiusculo)

        Label(self.app_main, text="Placa 3: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=7, padx=5)
        self.txt_lote = Entry(self.app_main, textvariable=self.lote, width=13)
        self.txt_lote.grid(sticky=W, column=0, row=8, padx=5)
        self.txt_lote.bind("<KeyRelease>", self.converter_lote_maiusculo)

        Label(self.app_main, text="Município Placa 3: ", font=(None, 8, 'normal')).grid(sticky=W, column=1,
                                                                                        row=7, padx=5)
        self.txt_lote = Entry(self.app_main, textvariable=self.lote, width=20)
        self.txt_lote.grid(sticky=W, column=1, row=8, padx=(5, 10))
        self.txt_lote.bind("<KeyRelease>", self.converter_lote_maiusculo)

        Label(self.app_main, text="Placa 4: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=9, padx=5)
        self.txt_lote = Entry(self.app_main, textvariable=self.lote, width=13)
        self.txt_lote.grid(sticky=W, column=0, row=10, padx=5)
        self.txt_lote.bind("<KeyRelease>", self.converter_lote_maiusculo)

        Label(self.app_main, text="Município Placa 4: ", font=(None, 8, 'normal')).grid(sticky=W, column=1,
                                                                                        row=9, padx=5)
        self.txt_lote = Entry(self.app_main, textvariable=self.lote, width=20)
        self.txt_lote.grid(sticky=W, column=1, row=10, padx=(5, 10))
        self.txt_lote.bind("<KeyRelease>", self.converter_lote_maiusculo)

        Label(self.app_main, text="Qtd. Lacres:", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=11,
                                                                                 padx=5)
        self.txt_deposito = tkinter.Spinbox(self.app_main, textvariable=self.deposito, width=10)
        self.txt_deposito.grid(sticky="we", column=0, row=12, padx=5)
        self.txt_deposito.bind("<KeyRelease>", self.converter_deposito_maiusculo)

        Button(self.app_main, text='Salvar', command=self.salvar_produto).grid(sticky='we', column=0, row=13, padx=5,
                                                                               pady=10)

        tkinter.mainloop()

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


cadastro = CadastroVeiculo()
