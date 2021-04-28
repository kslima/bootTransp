import tkinter
from tkinter import Tk, StringVar, Menu, Label, LabelFrame, Entry, Listbox, scrolledtext, Button, OUTSIDE, W
from win32api import MessageBox

import service
from model import Driver


class CadastroMotorista:

    def __init__(self):
        self.app_main = Tk()
        self.app_main.title("Cadastro de Motorista")

        self.driver_name = StringVar()
        self.cpf = StringVar()
        self.cnh = StringVar()
        self.rg = StringVar()
        self.search = StringVar()
        self.current_driver = None

        Label(self.app_main, text="Nome: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=0, padx=10)
        self.txt_name = Entry(self.app_main, textvariable=self.driver_name)
        self.txt_name.grid(sticky='we', column=0, row=1, padx=10, columnspan=3)
        self.txt_name.bind("<KeyRelease>", self.caps_name)

        Label(self.app_main, text="CPF: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=2, padx=10)
        self.txt_cpf = Entry(self.app_main, textvariable=self.cpf)
        self.txt_cpf.grid(sticky='we', column=0, row=3, padx=10)
        self.txt_cpf.bind("<KeyRelease>", self.cpf_number)

        Label(self.app_main, text="CNH: ", font=(None, 8, 'normal')).grid(sticky=W, column=1, row=2, padx=10)
        self.txt_cnh = Entry(self.app_main, textvariable=self.cnh)
        self.txt_cnh.grid(sticky='we', column=1, row=3, padx=10)
        self.txt_cnh.bind("<KeyRelease>", self.cnh_number)

        Label(self.app_main, text="RG: ", font=(None, 8, 'normal')).grid(sticky=W, column=2, row=2, padx=10)
        self.txt_rg = Entry(self.app_main, textvariable=self.rg)
        self.txt_rg.grid(sticky='we', column=2, row=3, padx=10)
        self.txt_rg.bind("<KeyRelease>", self.caps_rg)

        Button(self.app_main, text='Salvar', command=self.salvar).grid(sticky='we', column=0, row=4, padx=10, pady=10)

        # exibindo em looping
        tkinter.mainloop()

    def caps_name(self, event):
        self.driver_name.set(self.driver_name.get().upper())

    def caps_rg(self, event):
        self.rg.set(self.rg.get().upper())

    def cpf_number(self, *args):
        if not self.cpf.get().isdigit():
            self.cpf.set(''.join(x for x in self.cpf.get() if x.isdigit()))

    def cnh_number(self, *args):
        if not self.cnh.get().isdigit():
            self.cnh.set(''.join(x for x in self.cnh.get() if x.isdigit()))

    def verificar_motorista_valido(self):
        if not self.driver_name.get():
            MessageBox(None, "Informe o nome do motorista")
            return False
        if not self.cpf.get() and not self.cnh.get() and not self.rg.get():
            MessageBox(None, "Ao menos um documento deve ser informado!")
            return False
        return True

    def salvar(self):
        if self.verificar_motorista_valido():
            driver = Driver()
            driver.name = self.driver_name.get()
            driver.cpf = self.cpf.get()
            driver.cnh = self.cnh.get()
            driver.rg = self.rg.get()
            try:
                service.create_driver(driver)
                MessageBox(None, "Motorista salvo com sucesso!")
                self.app_main.destroy()

            except Exception as e:
                MessageBox(None, "Erro ao salvar motorista!\n" + str(e))

    def atualizar(self):
        pass


cadastro_motorista = CadastroMotorista()
