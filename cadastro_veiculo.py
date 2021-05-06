import tkinter
from tkinter import StringVar, Label, Entry, Button, W, Checkbutton, messagebox
from tkinter.ttk import Combobox

import service
from componentes import AutocompleteEntry
from model import Produto, Veiculo


class CadastroVeiculo:

    def __init__(self, master):
        self.app_main = tkinter.Toplevel(master)
        # self.app_main = tkinter.Tk()
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
        combobox_tipo_veiculo = Combobox(self.app_main, textvariable=self.tipo_veiculo, width=40)
        combobox_tipo_veiculo.grid(sticky="we", column=0, row=1, padx=5, columnspan=2)
        combobox_tipo_veiculo.bind("<KeyRelease>", self.tipo_veiculo_somento_numero)
        combobox_tipo_veiculo['values'] = service.listar_tipos_veiculos()

        Label(self.app_main, text="Peso Balança: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=2, padx=5)
        combobox_peso_balanca = Combobox(self.app_main, textvariable=self.tolerancia_balanca, width=40)
        combobox_peso_balanca.grid(sticky="we", column=0, row=3, padx=5, columnspan=2)
        combobox_peso_balanca.bind("<KeyRelease>", self.converter_peso_balanca_maiusculo)
        combobox_peso_balanca['values'] = service.listar_tolerancias_balanca()

        Label(self.app_main, text="Qtd. Lacres:", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=4,
                                                                                 padx=5)
        entry_numero_lacres = tkinter.Entry(self.app_main, textvariable=self.quantidade_lacres)
        entry_numero_lacres.grid(sticky="we", column=0, row=5, padx=(5, 10), columnspan=2)
        entry_numero_lacres.bind("<KeyRelease>", self.quantidade_lacre_somento_numero)

        Label(self.app_main, text="Placa 1: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=6, padx=5)
        entry_placa_1 = Entry(self.app_main, textvariable=self.placa_1)
        entry_placa_1.grid(sticky="we", column=0, row=7, padx=5)
        entry_placa_1.bind("<KeyRelease>", self.converter_placa_1_maiusculo)

        Label(self.app_main, text="Município Placa 1: ", font=(None, 8, 'normal')).grid(sticky=W, column=1, row=6,
                                                                                        padx=5)
        self.entry_municipio_placa_1 = AutocompleteEntry(self.app_main, width=20)
        self.entry_municipio_placa_1.grid(sticky="we", column=1, row=7, padx=(5, 10))
        self.entry_municipio_placa_1.bind("<KeyRelease>", self.converter_municipio_placa_1_maiusculo)

        Label(self.app_main, text="Placa 2: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=8, padx=5)
        entry_placa_2 = Entry(self.app_main, textvariable=self.placa_2)
        entry_placa_2.grid(sticky="we", column=0, row=9, padx=5)
        entry_placa_2.bind("<KeyRelease>", self.converter_placa_2_maiusculo)

        Label(self.app_main, text="Município Placa 2: ", font=(None, 8, 'normal')).grid(sticky=W, column=1,
                                                                                        row=8, padx=5)
        self.entry_municipio_placa_2 = AutocompleteEntry(self.app_main, width=20)
        self.entry_municipio_placa_2.grid(sticky="we", column=1, row=9, padx=(5, 10))
        self.entry_municipio_placa_2.bind("<KeyRelease>", self.converter_municipio_placa_2_maiusculo)

        Label(self.app_main, text="Placa 3: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=10, padx=5)
        entry_placa_3 = Entry(self.app_main, textvariable=self.placa_3)
        entry_placa_3.grid(sticky="we", column=0, row=11, padx=5)
        entry_placa_3.bind("<KeyRelease>", self.converter_placa_3_maiusculo)

        Label(self.app_main, text="Município Placa 3: ", font=(None, 8, 'normal')).grid(sticky=W, column=1,
                                                                                        row=10, padx=5)
        self.entry_municipio_placa_3 = AutocompleteEntry(self.app_main, width=20)
        self.entry_municipio_placa_3.grid(sticky="we", column=1, row=11, padx=(5, 10))
        self.entry_municipio_placa_3.bind("<KeyRelease>", self.converter_municipio_placa_3_maiusculo)

        Label(self.app_main, text="Placa 4: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=12, padx=5)
        entry_placa_4 = Entry(self.app_main, textvariable=self.placa_4)
        entry_placa_4.grid(sticky="we", column=0, row=13, padx=5)
        entry_placa_4.bind("<KeyRelease>", self.converter_placa_4_maiusculo)

        Label(self.app_main, text="Município Placa 4: ", font=(None, 8, 'normal')).grid(sticky=W, column=1,
                                                                                        row=12, padx=5)
        self.entry_municipio_placa_4 = AutocompleteEntry(self.app_main, width=20)
        self.entry_municipio_placa_4.grid(sticky="we", column=1, row=13, padx=(5, 10))
        self.entry_municipio_placa_4.bind("<KeyRelease>", self.converter_municipio_placa_4_maiusculo)

        Button(self.app_main, text='Salvar', command=self.salvar_veiculo) \
            .grid(sticky='we', column=0, row=14, padx=5, pady=5)

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
            novo_veiculo.tipo_veiculo = self.tipo_veiculo.get().split("-")[0]
            novo_veiculo.tolerancia_balanca = self.tolerancia_balanca.get().split("-")[0]
            novo_veiculo.quantidade_lacres = self.quantidade_lacres.get()
            novo_veiculo.placa_1 = self.placa_1.get()
            novo_veiculo.placa_2 = self.placa_2.get()
            novo_veiculo.placa_3 = self.placa_3.get()
            novo_veiculo.placa_4 = self.placa_4.get()
            novo_veiculo.codigo_municipio_placa_1 = self.entry_municipio_placa_1.var.get()
            novo_veiculo.codigo_municipio_placa_2 = self.entry_municipio_placa_2.var.get()
            novo_veiculo.codigo_municipio_placa_3 = self.entry_municipio_placa_3.var.get()
            novo_veiculo.codigo_municipio_placa_4 = self.entry_municipio_placa_4.var.get()

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
        if self.tipo_veiculo.get() == "":
            messagebox.showerror("Campo obrigatório", "O campo 'Tipo Veículo' é obrigatório!")
            return False
        if self.tolerancia_balanca.get() == "":
            messagebox.showerror("Campo obrigatório", "O campo 'Tolerância Balança' é obrigatório!")
            return False
        return True

    def setar_campos_para_edicao(self, veiculo_para_editar):
        print('editando ' + str(veiculo_para_editar))
        self.tipo_veiculo.set(veiculo_para_editar.tipo_veiculo)
        self.tolerancia_balanca.set(veiculo_para_editar.tolerancia_balanca)
        self.quantidade_lacres.set(veiculo_para_editar.quantidade_lacres)
        self.placa_1.set(veiculo_para_editar.placa_1)
        self.placa_2.set(veiculo_para_editar.placa_2)
        self.placa_3.set(veiculo_para_editar.placa_3)
        self.placa_4.set(veiculo_para_editar.placa_4)
        self.entry_municipio_placa_1.var.set(veiculo_para_editar.codigo_municipio_placa_1)
        self.entry_municipio_placa_2.var.set(veiculo_para_editar.codigo_municipio_placa_2)
        self.entry_municipio_placa_3.var.set(veiculo_para_editar.codigo_municipio_placa_3)
        self.entry_municipio_placa_4.var.set(veiculo_para_editar.codigo_municipio_placa_4)

