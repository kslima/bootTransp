import tkinter
from tkinter import StringVar, Label, Entry, Button, W, messagebox, DISABLED, scrolledtext, END, INSERT
from service import PacoteLacreService
from model import PacoteLacre
from datetime import datetime, date


class CadastroLacres:

    def __init__(self, master):
        self.app_main = tkinter.Toplevel(master)
        self.app_main.title("Cadastro de Lacres")
        self.app_main.geometry('220x400')
        self.centralizar_tela()

        self.atualizando_cadastro = False
        self.nome = StringVar()
        self.lacre_1 = StringVar()
        self.lacre_2 = StringVar()
        self.lacre_3 = StringVar()
        self.lacre_4 = StringVar()
        self.lacre_5 = StringVar()
        self.lacre_6 = StringVar()
        self.lacre_7 = StringVar()
        self.lacre_8 = StringVar()
        self.lacre_9 = StringVar()
        self.lacre_10 = StringVar()
        self.lacre_11 = StringVar()
        self.lacre_12 = StringVar()
        self.lacre_13 = StringVar()
        self.lacre_14 = StringVar()
        self.pacote_lacre_atual = None

        Label(self.app_main, text="Lacres: ", font=(None, 8, 'bold')).grid(sticky=W, column=0, row=0, padx=10)

        Label(self.app_main, text="Lacre 01: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=1, padx=10)
        entry_lacre_1 = Entry(self.app_main, textvariable=self.lacre_1)
        entry_lacre_1.grid(sticky=W, column=1, row=1, padx=5, pady=2, columnspan=2)
        entry_lacre_1.bind('<KeyRelease>', lambda x: CadastroLacres.somente_numero_bind(self.lacre_1))

        Label(self.app_main, text="Lacre 02: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=2, padx=10)
        entry_lacre_2 = Entry(self.app_main, textvariable=self.lacre_2)
        entry_lacre_2.grid(sticky=W, column=1, row=2, padx=5, pady=2, columnspan=2)
        entry_lacre_2.bind('<KeyRelease>', lambda x: CadastroLacres.somente_numero_bind(self.lacre_2))

        Label(self.app_main, text="Lacre 03: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=3, padx=10)
        entry_lacre_3 = Entry(self.app_main, textvariable=self.lacre_3)
        entry_lacre_3.grid(sticky=W, column=1, row=3, padx=5, pady=2, columnspan=2)
        entry_lacre_3.bind('<KeyRelease>', lambda x: CadastroLacres.somente_numero_bind(self.lacre_3))

        Label(self.app_main, text="Lacre 04: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=4, padx=10)
        entry_lacre_4 = Entry(self.app_main, textvariable=self.lacre_4)
        entry_lacre_4.grid(sticky=W, column=1, row=4, padx=5, pady=2, columnspan=2)
        entry_lacre_4.bind('<KeyRelease>', lambda x: CadastroLacres.somente_numero_bind(self.lacre_4))

        Label(self.app_main, text="Lacre 05: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=5, padx=10)
        entry_lacre_5 = Entry(self.app_main, textvariable=self.lacre_5)
        entry_lacre_5.grid(sticky=W, column=1, row=5, padx=5, pady=2, columnspan=2)
        entry_lacre_5.bind('<KeyRelease>', lambda x: CadastroLacres.somente_numero_bind(self.lacre_5))

        Label(self.app_main, text="Lacre 06: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=6, padx=10)
        entry_lacre_6 = Entry(self.app_main, textvariable=self.lacre_6)
        entry_lacre_6.grid(sticky=W, column=1, row=6, padx=5, pady=2, columnspan=2)
        entry_lacre_6.bind('<KeyRelease>', lambda x: CadastroLacres.somente_numero_bind(self.lacre_6))

        Label(self.app_main, text="Lacre 07: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=7, padx=10)
        entry_lacre_7 = Entry(self.app_main, textvariable=self.lacre_7)
        entry_lacre_7.grid(sticky=W, column=1, row=7, padx=5, pady=2, columnspan=2)
        entry_lacre_7.bind('<KeyRelease>', lambda x: CadastroLacres.somente_numero_bind(self.lacre_7))

        Label(self.app_main, text="Lacre 08: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=8, padx=10)
        entry_lacre_8 = Entry(self.app_main, textvariable=self.lacre_8)
        entry_lacre_8.grid(sticky=W, column=1, row=8, padx=5, pady=2, columnspan=2)
        entry_lacre_8.bind('<KeyRelease>', lambda x: CadastroLacres.somente_numero_bind(self.lacre_8))

        Label(self.app_main, text="Lacre 09: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=9, padx=10)
        entry_lacre_9 = Entry(self.app_main, textvariable=self.lacre_9)
        entry_lacre_9.grid(sticky=W, column=1, row=9, padx=5, pady=2, columnspan=2)
        entry_lacre_9.bind('<KeyRelease>', lambda x: CadastroLacres.somente_numero_bind(self.lacre_9))

        Label(self.app_main, text="Lacre 10: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=10, padx=10)
        entry_lacre_10 = Entry(self.app_main, textvariable=self.lacre_10)
        entry_lacre_10.grid(sticky=W, column=1, row=10, padx=5, pady=2, columnspan=2)
        entry_lacre_10.bind('<KeyRelease>', lambda x: CadastroLacres.somente_numero_bind(self.lacre_10))

        Label(self.app_main, text="Lacre 11: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=11, padx=10)
        entry_lacre_11 = Entry(self.app_main, textvariable=self.lacre_11)
        entry_lacre_11.grid(sticky=W, column=1, row=11, padx=5, pady=2, columnspan=2)
        entry_lacre_11.bind('<KeyRelease>', lambda x: CadastroLacres.somente_numero_bind(self.lacre_11))

        Label(self.app_main, text="Lacre 12: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=12, padx=10)
        entry_lacre_12 = Entry(self.app_main, textvariable=self.lacre_12)
        entry_lacre_12.grid(sticky=W, column=1, row=12, padx=5, pady=2, columnspan=2)
        entry_lacre_12.bind('<KeyRelease>', lambda x: CadastroLacres.somente_numero_bind(self.lacre_12))

        Label(self.app_main, text="Lacre 13: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=13, padx=10)
        entry_lacre_13 = Entry(self.app_main, textvariable=self.lacre_13)
        entry_lacre_13.grid(sticky=W, column=1, row=13, padx=5, pady=2, columnspan=2)
        entry_lacre_13.bind('<KeyRelease>', lambda x: CadastroLacres.somente_numero_bind(self.lacre_13))

        Label(self.app_main, text="Lacre 14: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=14, padx=10)
        entry_lacre_14 = Entry(self.app_main, textvariable=self.lacre_14)
        entry_lacre_14.grid(sticky=W, column=1, row=14, padx=5, pady=2, columnspan=2)
        entry_lacre_14.bind('<KeyRelease>', lambda x: CadastroLacres.somente_numero_bind(self.lacre_14))

        Button(self.app_main, text='Salvar', command=self.salvar_ou_atualizar).grid(sticky='we', column=1, row=15,
                                                                                    padx=10, pady=10)
        self.botao_deletar = Button(self.app_main, text='Excluir', command=self.deletar, state=DISABLED)
        self.botao_deletar.grid(sticky='we', column=2, row=15, padx=10, pady=10)

    @staticmethod
    def somente_numero_bind(var):
        if not var.get().isdigit():
            var.set(''.join(x for x in var.get() if x.isdigit()))
        if len(var.get()) > 7:
            var.set(var.get()[0:7])

    def centralizar_tela(self):
        # Gets the requested values of the height and widht.
        window_width = self.app_main.winfo_reqwidth()
        window_height = self.app_main.winfo_reqheight()
        print("Width", window_width, "Height", window_height)

        # Gets both half the screen width/height and window width/height
        position_right = int(self.app_main.winfo_screenwidth() / 2.3 - window_width / 2)
        position_down = int(self.app_main.winfo_screenheight() / 3 - window_height / 2)

        # Positions the window in the center of the page.
        self.app_main.geometry("+{}+{}".format(position_right, position_down))

    def nome_maiusculo(self, event):
        self.nome.set(self.nome.get().upper())

    def verificar_campos_obrigatorios(self):
        if not self.lacre_1.get() \
                and not self.lacre_2.get() \
                and not self.lacre_3.get() \
                and not self.lacre_4.get() \
                and not self.lacre_5.get() \
                and not self.lacre_6.get() \
                and not self.lacre_7.get() \
                and not self.lacre_8.get() \
                and not self.lacre_9.get() \
                and not self.lacre_10.get() \
                and not self.lacre_11.get() \
                and not self.lacre_12.get() \
                and not self.lacre_13.get() \
                and not self.lacre_14.get():
            messagebox.showerror("Campo obrigatório", "É necessário informar ao menos 1 lacre!")
            return False
        return True

    def salvar_ou_atualizar(self):
        if self.verificar_campos_obrigatorios():
            if self.pacote_lacre_atual is None or self.pacote_lacre_atual.id_pacote_lacre is None:
                self.salvar()
            else:
                self.atualizar()

    def salvar(self):
        codigo = CadastroLacres.gerar_codigo()
        self.pacote_lacre_atual = PacoteLacre(codigo=codigo,
                                              lacre_1=self.lacre_1.get(),
                                              lacre_2=self.lacre_2.get(),
                                              lacre_3=self.lacre_3.get(),
                                              lacre_4=self.lacre_4.get(),
                                              lacre_5=self.lacre_5.get(),
                                              lacre_6=self.lacre_6.get(),
                                              lacre_7=self.lacre_7.get(),
                                              lacre_8=self.lacre_8.get(),
                                              lacre_9=self.lacre_9.get(),
                                              lacre_10=self.lacre_10.get(),
                                              lacre_11=self.lacre_11.get(),
                                              lacre_12=self.lacre_12.get(),
                                              lacre_13=self.lacre_13.get(),
                                              lacre_14=self.lacre_14.get())

        pacote_lacre_inserido = PacoteLacreService.inserir_pacote_lacre(self.pacote_lacre_atual)
        if pacote_lacre_inserido[0]:
            messagebox.showinfo("Sucesso", pacote_lacre_inserido[1])
            self.app_main.destroy()
        else:
            messagebox.showerror("Erro", pacote_lacre_inserido[1])

    @staticmethod
    def gerar_codigo():
        data_atual = date.today().strftime("%d%m%y")
        hora_atual = datetime.now().strftime("%H%M%S")
        return '{}{}'.format(data_atual, hora_atual)

    def atualizar(self):
        self.pacote_lacre_atual.lacre_1 = self.lacre_1.get()
        self.pacote_lacre_atual.lacre_2 = self.lacre_1.get()
        self.pacote_lacre_atual.lacre_3 = self.lacre_1.get()
        self.pacote_lacre_atual.lacre_4 = self.lacre_1.get()
        self.pacote_lacre_atual.lacre_5 = self.lacre_1.get()
        self.pacote_lacre_atual.lacre_6 = self.lacre_1.get()
        self.pacote_lacre_atual.lacre_7 = self.lacre_1.get()
        self.pacote_lacre_atual.lacre_8 = self.lacre_1.get()
        self.pacote_lacre_atual.lacre_9 = self.lacre_1.get()
        self.pacote_lacre_atual.lacre_10 = self.lacre_1.get()
        self.pacote_lacre_atual.lacre_11 = self.lacre_1.get()
        self.pacote_lacre_atual.lacre_12 = self.lacre_1.get()
        self.pacote_lacre_atual.lacre_13 = self.lacre_1.get()
        self.pacote_lacre_atual.lacre_14 = self.lacre_1.get()

        pacote_lacre_atualizado = PacoteLacreService.atualizar_pacote_lacres(self.pacote_lacre_atual)
        if pacote_lacre_atualizado[0]:
            messagebox.showinfo("Sucesso", pacote_lacre_atualizado[1])
            self.app_main.destroy()
        else:
            messagebox.showerror("Erro", pacote_lacre_atualizado[1])

    def deletar(self):
        deletar = messagebox.askokcancel("Confirmar", "Excluir registro pernamentemente ?")
        if deletar:
            pacote_lacre_deletado = PacoteLacreService.deletar_pacote_lacres(self.pacote_lacre_atual.id_pacote_lacre)
            if pacote_lacre_deletado[0]:
                messagebox.showinfo("Sucesso", pacote_lacre_deletado[1])
                self.app_main.destroy()
            else:
                messagebox.showerror("Erro", pacote_lacre_deletado[1])

    def setar_campos_para_edicao(self, pacote_lacre):
        self.botao_deletar['state'] = 'normal'
        self.pacote_lacre_atual = pacote_lacre
        self.lacre_1.set(self.pacote_lacre_atual.lacre_1)
        self.lacre_2.set(self.pacote_lacre_atual.lacre_1)
        self.lacre_3.set(self.pacote_lacre_atual.lacre_1)
        self.lacre_4.set(self.pacote_lacre_atual.lacre_1)
        self.lacre_5.set(self.pacote_lacre_atual.lacre_1)
        self.lacre_6.set(self.pacote_lacre_atual.lacre_1)
        self.lacre_7.set(self.pacote_lacre_atual.lacre_1)
        self.lacre_8.set(self.pacote_lacre_atual.lacre_1)
        self.lacre_9.set(self.pacote_lacre_atual.lacre_1)
        self.lacre_10.set(self.pacote_lacre_atual.lacre_1)
        self.lacre_11.set(self.pacote_lacre_atual.lacre_1)
        self.lacre_12.set(self.pacote_lacre_atual.lacre_1)
        self.lacre_13.set(self.pacote_lacre_atual.lacre_1)
        self.lacre_14.set(self.pacote_lacre_atual.lacre_1)


if __name__ == '__main__':
    app_main = tkinter.Tk()
    CadastroLacres(app_main)
    app_main.mainloop()