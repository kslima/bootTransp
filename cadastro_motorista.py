import tkinter
from tkinter import StringVar, Label, Entry, Button, W, messagebox, DISABLED

import peewee

from service import MotoristaService
from model import Motorista
from utilitarios import NumberUtils
import sys
import traceback


class CadastroMotorista:

    def __init__(self, master):
        self.app_main = tkinter.Toplevel(master)
        self.app_main.title("Cadastro de Motorista")
        self.app_main.resizable(False, False)
        self.centralizar_tela()

        self.atualizando_cadastro = False
        self.nome = StringVar()
        self.cpf = StringVar()
        self.cnh = StringVar()
        self.rg = StringVar()
        self.search = StringVar()
        self.motorista_atual = None

        Label(self.app_main, text="Nome: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=0, padx=10)
        self.txt_name = Entry(self.app_main, textvariable=self.nome)
        self.txt_name.grid(sticky='we', column=0, row=1, padx=10, columnspan=3)
        self.txt_name.bind("<KeyRelease>", self.nome_maiusculo)

        Label(self.app_main, text="CPF: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=2, padx=10)
        self.txt_cpf = Entry(self.app_main, textvariable=self.cpf)
        self.txt_cpf.grid(sticky='we', column=0, row=3, padx=10)
        self.txt_cpf.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_inteiro), '%P'))

        Label(self.app_main, text="CNH: ", font=(None, 8, 'normal')).grid(sticky=W, column=1, row=2, padx=10)
        self.txt_cnh = Entry(self.app_main, textvariable=self.cnh)
        self.txt_cnh.grid(sticky='we', column=1, row=3, padx=10)
        self.txt_cnh.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_inteiro), '%P'))

        Label(self.app_main, text="RG: ", font=(None, 8, 'normal')).grid(sticky=W, column=2, row=2, padx=10)
        self.txt_rg = Entry(self.app_main, textvariable=self.rg)
        self.txt_rg.grid(sticky='we', column=2, row=3, padx=10)
        self.txt_rg.bind("<KeyRelease>", self.rg_maiusculo)

        Button(self.app_main, text='Salvar', command=self.salvar_ou_atualizar).grid(sticky='we', column=0, row=4,
                                                                                    padx=10, pady=10)

        self.botao_deletar = Button(self.app_main, text='Excluir', command=self.deletar, state=DISABLED)
        self.botao_deletar.grid(sticky='we', column=1, row=4, padx=10, pady=10)

    def centralizar_tela(self):
        window_width = self.app_main.winfo_reqwidth()
        window_height = self.app_main.winfo_reqheight()

        position_right = int(self.app_main.winfo_screenwidth() / 2.3 - window_width / 2)
        position_down = int(self.app_main.winfo_screenheight() / 3 - window_height / 2)

        # Positions the window in the center of the page.
        self.app_main.geometry("+{}+{}".format(position_right, position_down))

    def nome_maiusculo(self, event):
        self.nome.set(self.nome.get().upper())

    def rg_maiusculo(self, event):
        self.rg.set(self.rg.get().upper())

    def verificar_campos_obrigatorios(self):
        if not self.nome.get():
            self.app_main.lift()
            messagebox.showerror("Campo obrigatório", "O campo 'nome' é obrigatório!")
            return False
        if not self.cpf.get() and not self.cnh.get() and not self.rg.get():
            self.app_main.lift()
            messagebox.showerror("Campo obrigatório", "Ao menos um documento deve ser informado!")
            return False
        return True

    def salvar_ou_atualizar(self):
        if self.verificar_campos_obrigatorios():
            if self.motorista_atual is None or self.motorista_atual.id is None:
                self.salvar()
            else:
                self.atualizar()

    def salvar(self):
        try:
            self.motorista_atual = Motorista()
            self.atualizar_dados_motorista()
            MotoristaService.salvar_ou_atualizar(self.motorista_atual)
            messagebox.showinfo("Sucesso", "Motorista salvo com sucesso!")
            self.app_main.destroy()
        except peewee.IntegrityError:
            traceback.print_exc(file=sys.stdout)
            messagebox.showerror("Cadastro duplicado!", "Já existe um motorista cadastrado com esses dados!")

        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            messagebox.showerror("Erro", e)

    def atualizar(self):
        try:
            self.atualizar_dados_motorista()
            MotoristaService.salvar_ou_atualizar(self.motorista_atual)
            messagebox.showinfo("Sucesso", "Motorista atualizado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", e)
        self.app_main.destroy()

    def deletar(self):
        deletar = messagebox.askokcancel("Confirmar", "Excluir registro pernamentemente ?")
        if deletar:
            try:
                MotoristaService.deletar_motoristas(self.motorista_atual)
                messagebox.showinfo("Sucesso", "Motorista deletado com sucesso!")

            except Exception as e:
                messagebox.showerror("Erro", "Erro deletar motorista!\n{}".format(e))

    def atualizar_dados_motorista(self):
        nome = self.nome.get().strip().strip()
        cpf = self.cpf.get().strip().strip()
        cnh = self.cnh.get().strip().strip()
        rg = self.rg.get().strip().strip()
        self.motorista_atual.nome = nome
        self.motorista_atual.cpf = cpf
        self.motorista_atual.cnh = cnh
        self.motorista_atual.rg = rg

    def setar_campos_para_edicao(self, motorista):
        self.botao_deletar['state'] = 'normal'
        self.motorista_atual = motorista
        self.nome.set(self.motorista_atual.nome)
        self.cpf.set(self.motorista_atual.cpf)
        self.cnh.set(self.motorista_atual.cnh)
        self.rg.set(self.motorista_atual.rg)


if __name__ == '__main__':
    app_main = tkinter.Tk()
    CadastroMotorista(app_main)
    app_main.mainloop()
