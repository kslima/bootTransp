import tkinter
from tkinter import StringVar, Label, Entry, Button, W, Checkbutton, messagebox
from tkinter.ttk import Combobox

import service
from model import Produto, Veiculo


class CadastroVeiculo:

    def __init__(self):
        # self.app_main = tkinter.Toplevel(master)
        self.app_main = tkinter.Tk()
        self.app_main.title("Cadastro de Veículo")

        self.atualizando_cadastro = False

        self.tipo_veiculo = StringVar()
        self.tolerancia_balanca = StringVar()
        self.quantidade_lacres = StringVar()
        self.lote = StringVar()
        self.placa_1 = StringVar()
        self.placa_2 = StringVar()
        self.placa_3 = StringVar()
        self.placa_4 = StringVar()
        self.municipio_placa_1 = StringVar()
        self.municipio_placa_2 = StringVar()
        self.municipio_placa_3 = StringVar()
        self.municipio_placa_4 = StringVar()

        Label(self.app_main, text="Tipo Veículo: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=0, padx=5)
        self.txt_codigo = Combobox(self.app_main, textvariable=self.tipo_veiculo, width=10)
        self.txt_codigo.grid(sticky=W, column=0, row=1, padx=5)
        self.txt_codigo.bind("<KeyRelease>", self.tipo_veiculo_somento_numero)

        Label(self.app_main, text="Peso Balança: ", font=(None, 8, 'normal')).grid(sticky=W, column=1, row=0, padx=5)
        self.txt_nome = Combobox(self.app_main, textvariable=self.tolerancia_balanca, width=5)
        self.txt_nome.grid(sticky="we", column=1, row=1, padx=5)
        self.txt_nome.bind("<KeyRelease>", self.converter_peso_balanca_maiusculo)

        Label(self.app_main, text="Qtd. Lacres:", font=(None, 8, 'normal')).grid(sticky=W, column=2, row=0,
                                                                                 padx=5)
        self.txt_deposito = tkinter.Entry(self.app_main, textvariable=self.quantidade_lacres, width=5)
        self.txt_deposito.grid(sticky="we", column=2, row=1, padx=5)
        self.txt_deposito.bind("<KeyRelease>", self.quantidade_lacre_somento_numero)

        Label(self.app_main, text="Placa 1: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=3, padx=5)
        self.txt_lote = Entry(self.app_main, textvariable=self.placa_1, width=13)
        self.txt_lote.grid(sticky=W, column=0, row=4, padx=5)
        self.txt_lote.bind("<KeyRelease>", self.converter_placa_1_maiusculo)

        Label(self.app_main, text="Município Placa 1: ", font=(None, 8, 'normal')).grid(sticky=W, column=1, row=3,
                                                                                        padx=5)
        self.txt_lote = Entry(self.app_main, textvariable=self.municipio_placa_1, width=20)
        self.txt_lote.grid(sticky="we", column=1, row=4, padx=(5, 10), columnspan=2)
        self.txt_lote.bind("<KeyRelease>", self.converter_municipio_placa_1_maiusculo)

        Label(self.app_main, text="Placa 2: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=5, padx=5)
        self.txt_lote = Entry(self.app_main, textvariable=self.placa_2, width=13)
        self.txt_lote.grid(sticky=W, column=0, row=6, padx=5)
        self.txt_lote.bind("<KeyRelease>", self.converter_placa_2_maiusculo)

        Label(self.app_main, text="Município Placa 2: ", font=(None, 8, 'normal')).grid(sticky=W, column=1,
                                                                                        row=5, padx=5)
        self.txt_lote = Entry(self.app_main, textvariable=self.municipio_placa_2, width=20)
        self.txt_lote.grid(sticky="we", column=1, row=6, padx=(5, 10), columnspan=2)
        self.txt_lote.bind("<KeyRelease>", self.converter_municipio_placa_2_maiusculo)

        Label(self.app_main, text="Placa 3: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=7, padx=5)
        self.txt_lote = Entry(self.app_main, textvariable=self.placa_3, width=13)
        self.txt_lote.grid(sticky=W, column=0, row=8, padx=5)
        self.txt_lote.bind("<KeyRelease>", self.converter_placa_3_maiusculo)

        Label(self.app_main, text="Município Placa 3: ", font=(None, 8, 'normal')).grid(sticky=W, column=1,
                                                                                        row=7, padx=5)
        self.txt_lote = Entry(self.app_main, textvariable=self.municipio_placa_3, width=20)
        self.txt_lote.grid(sticky="we", column=1, row=8, padx=(5, 10), columnspan=2)
        self.txt_lote.bind("<KeyRelease>", self.converter_municipio_placa_3_maiusculo)

        Label(self.app_main, text="Placa 4: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=9, padx=5)
        self.txt_lote = Entry(self.app_main, textvariable=self.placa_4, width=13)
        self.txt_lote.grid(sticky=W, column=0, row=10, padx=5)
        self.txt_lote.bind("<KeyRelease>", self.converter_placa_4_maiusculo)

        Label(self.app_main, text="Município Placa 4: ", font=(None, 8, 'normal')).grid(sticky=W, column=1,
                                                                                        row=9, padx=5)
        self.txt_lote = Entry(self.app_main, textvariable=self.municipio_placa_4, width=20)
        self.txt_lote.grid(sticky="we", column=1, row=10, padx=(5, 10), columnspan=2)
        self.txt_lote.bind("<KeyRelease>", self.converter_municipio_placa_4_maiusculo)

        Button(self.app_main, text='Pesquisar Município', command=self.pesquisar_municipios) \
            .grid(sticky='we', column=0, row=13, padx=5, pady=5, columnspan=2)
        Button(self.app_main, text='Salvar', command=self.salvar_veiculo()) \
            .grid(sticky='we', column=0, row=14, padx=5, pady=5, columnspan=2)

        tkinter.mainloop()

    def quantidade_lacre_somento_numero(self, *args):
        if not self.quantidade_lacres.get().isdigit():
            self.quantidade_lacres.set(''.join(x for x in self.quantidade_lacres.get() if x.isdigit()))

    def tipo_veiculo_somento_numero(self, *args):
        if not self.quantidade_lacres.get().isdigit():
            self.quantidade_lacres.set(''.join(x for x in self.quantidade_lacres.get() if x.isdigit()))

    def converter_peso_balanca_maiusculo(self, event):
        self.tolerancia_balanca.set(self.tolerancia_balanca.get().upper())

    def converter_placa_1_maiusculo(self, event):
        self.placa_1.set(self.placa_1.get().upper())

    def converter_placa_2_maiusculo(self, event):
        self.placa_2.set(self.placa_2.get().upper())

    def converter_placa_3_maiusculo(self, event):
        self.placa_3.set(self.placa_3.get().upper())

    def converter_placa_4_maiusculo(self, event):
        self.placa_4.set(self.placa_4.get().upper())

    def converter_municipio_placa_1_maiusculo(self, event):
        self.municipio_placa_1.set(self.municipio_placa_1.get().upper())

    def converter_municipio_placa_2_maiusculo(self, event):
        self.municipio_placa_2.set(self.municipio_placa_2.get().upper())

    def converter_municipio_placa_3_maiusculo(self, event):
        self.municipio_placa_3.set(self.municipio_placa_3.get().upper())

    def converter_municipio_placa_4_maiusculo(self, event):
        self.municipio_placa_4.set(self.municipio_placa_4.get().upper())

    def pesquisar_municipios(self):
        pass

    def salvar_veiculo(self):
        if self.verificar_campos_obrigatorios():
            novo_veiculo = Veiculo()
            novo_veiculo.tipo_veiculo = self.tipo_veiculo.get()
            novo_veiculo.tolerancia_balanca = self.tolerancia_balanca.get()
            novo_veiculo.quantidade_lacres = self.quantidade_lacres.get()
            novo_veiculo.placa_1 = self.placa_1.get()
            novo_veiculo.placa_2 = self.placa_2.get()
            novo_veiculo.placa_3 = self.placa_3.get()
            novo_veiculo.placa_4 = self.placa_4.get()
            novo_veiculo.codigo_municipio_placa_1 = self.municipio_placa_1.get()
            novo_veiculo.codigo_municipio_placa_2 = self.municipio_placa_2.get()
            novo_veiculo.codigo_municipio_placa_3 = self.municipio_placa_3.get()
            novo_veiculo.codigo_municipio_placa_4 = self.municipio_placa_4.get()

            if self.atualizando_cadastro:
                self.atualizar_veiculo(novo_veiculo)

            else:
                cadastrado = service.cadastrar_veiculo_se_nao_exister(novo_veiculo)
                if cadastrado[0] == 1:
                    messagebox.showinfo("Sucesso", cadastrado[1])
                    self.app_main.destroy()
                else:
                    messagebox.showerror("Erro", cadastrado[1])

    def atualizar_veiculo(self, veiculo_para_atualizar):
        veiculo_atualizado = service.atualizar_veiculo(veiculo_para_atualizar)
        if veiculo_atualizado:
            messagebox.showinfo("Sucesso", veiculo_atualizado[1])
            self.app_main.destroy()

        else:
            messagebox.showerror("Erro", veiculo_atualizado[1])

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
