import tkinter
from tkinter import Tk, StringVar, Menu, Label, LabelFrame, Entry, Listbox, scrolledtext, Button, OUTSIDE, W, messagebox
from win32api import MessageBox

import service
from model import Motorista


class CadastroMotorista:

    def __init__(self, master):
        self.app_main = tkinter.Toplevel(master)
        self.app_main.title("Cadastro de Motorista")

        self.atualizando_cadastro = False
        self.nome = StringVar()
        self.cpf = StringVar()
        self.cnh = StringVar()
        self.rg = StringVar()
        self.search = StringVar()
        self.current_driver = None

        Label(self.app_main, text="Nome: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=0, padx=10)
        self.txt_name = Entry(self.app_main, textvariable=self.nome)
        self.txt_name.grid(sticky='we', column=0, row=1, padx=10, columnspan=3)
        self.txt_name.bind("<KeyRelease>", self.nome_maiusculo)

        Label(self.app_main, text="CPF: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=2, padx=10)
        self.txt_cpf = Entry(self.app_main, textvariable=self.cpf)
        self.txt_cpf.grid(sticky='we', column=0, row=3, padx=10)
        self.txt_cpf.bind("<KeyRelease>", self.cpf_somente_numero)

        Label(self.app_main, text="CNH: ", font=(None, 8, 'normal')).grid(sticky=W, column=1, row=2, padx=10)
        self.txt_cnh = Entry(self.app_main, textvariable=self.cnh)
        self.txt_cnh.grid(sticky='we', column=1, row=3, padx=10)
        self.txt_cnh.bind("<KeyRelease>", self.cnh_somente_numero)

        Label(self.app_main, text="RG: ", font=(None, 8, 'normal')).grid(sticky=W, column=2, row=2, padx=10)
        self.txt_rg = Entry(self.app_main, textvariable=self.rg)
        self.txt_rg.grid(sticky='we', column=2, row=3, padx=10)
        self.txt_rg.bind("<KeyRelease>", self.rg_maiusculo)

        Button(self.app_main, text='Salvar', command=self.salvar_ou_atualizar).grid(sticky='we', column=0, row=4, padx=10, pady=10)

    def nome_maiusculo(self, event):
        self.nome.set(self.nome.get().upper())

    def rg_maiusculo(self, event):
        self.rg.set(self.rg.get().upper())

    def cpf_somente_numero(self, *args):
        if not self.cpf.get().isdigit():
            self.cpf.set(''.join(x for x in self.cpf.get() if x.isdigit()))

    def cnh_somente_numero(self, *args):
        if not self.cnh.get().isdigit():
            self.cnh.set(''.join(x for x in self.cnh.get() if x.isdigit()))

    def verificar_campos_obrigatorios(self):
        if not self.nome.get():
            messagebox.showerror("Campo obrigatório", "O campo 'nome' é obrigatório!")
            return False
        if not self.cpf.get() and not self.cnh.get() and not self.rg.get():
            messagebox.showerror("Campo obrigatório", "Ao menos um documento deve ser informado!")
            return False
        return True

    def salvar_ou_atualizar(self):
        if self.verificar_campos_obrigatorios():
            novo_motorista = Motorista()
            novo_motorista.nome = self.nome.get()
            novo_motorista.cpf = self.cpf.get()
            novo_motorista.cnh = self.cnh.get()
            novo_motorista.rg = self.rg.get()

            if self.atualizando_cadastro:
                self.atualizar(novo_motorista)

            else:
                cadastrado = service.cadastrar_motorista_se_nao_existir(novo_motorista)
                if cadastrado[0] == 1:
                    messagebox.showinfo("Sucesso", cadastrado[1])
                    self.app_main.destroy()
                else:
                    messagebox.showerror("Erro", cadastrado[1])

    def atualizar(self, motorista_para_atualizar):
        motorista_atualizado = service.atualizar_motorista(motorista_para_atualizar)
        if motorista_atualizado:
            messagebox.showinfo("Sucesso", motorista_atualizado[1])
            self.app_main.destroy()

        else:
            messagebox.showerror("Erro", motorista_atualizado[1])

    def setar_campos_para_edicao(self, motorista_para_editar):
        self.nome.set(motorista_para_editar.nome)
        self.cpf.set(motorista_para_editar.cpf)
        self.cnh.set(motorista_para_editar.cnh)
        self.rg.set(motorista_para_editar.rg)