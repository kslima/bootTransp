import tkinter
from tkinter import StringVar, Label, Entry, Button, W, messagebox, DISABLED
from service import MotoristaService
from model import Motorista


class CadastroMotorista:

    def __init__(self, master):
        self.app_main = tkinter.Toplevel(master)
        self.app_main.title("Cadastro de Motorista")
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
        self.txt_cpf.bind("<KeyRelease>", self.cpf_somente_numero)

        Label(self.app_main, text="CNH: ", font=(None, 8, 'normal')).grid(sticky=W, column=1, row=2, padx=10)
        self.txt_cnh = Entry(self.app_main, textvariable=self.cnh)
        self.txt_cnh.grid(sticky='we', column=1, row=3, padx=10)
        self.txt_cnh.bind("<KeyRelease>", self.cnh_somente_numero)

        Label(self.app_main, text="RG: ", font=(None, 8, 'normal')).grid(sticky=W, column=2, row=2, padx=10)
        self.txt_rg = Entry(self.app_main, textvariable=self.rg)
        self.txt_rg.grid(sticky='we', column=2, row=3, padx=10)
        self.txt_rg.bind("<KeyRelease>", self.rg_maiusculo)

        Button(self.app_main, text='Salvar', command=self.salvar_ou_atualizar).grid(sticky='we', column=0, row=4,
                                                                                    padx=10, pady=10)

        self.botao_deletar = Button(self.app_main, text='Excluir', command=self.deletar, state=DISABLED)
        self.botao_deletar.grid(sticky='we', column=1, row=4, padx=10, pady=10)

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
            if self.motorista_atual is None or self.motorista_atual.id_motorista is None:
                self.salvar()
            else:
                self.atualizar()

    def salvar(self):
        self.motorista_atual = Motorista(nome=self.nome.get().strip(),
                                         cpf=self.cpf.get().strip(),
                                         cnh=self.cnh.get().strip(),
                                         rg=self.rg.get().strip())
        motorista_inserido = MotoristaService.inserir_motoristas(self.motorista_atual)
        if motorista_inserido[0]:
            messagebox.showinfo("Sucesso", motorista_inserido[1])
            self.app_main.destroy()
        else:
            messagebox.showerror("Erro", motorista_inserido[1])

    def atualizar(self):
        self.motorista_atual.nome = self.nome.get().strip()
        self.motorista_atual.cpf = self.cpf.get().strip()
        self.motorista_atual.cnh = self.cnh.get().strip()
        self.motorista_atual.rg = self.rg.get().strip()

        motorista_atualizado = MotoristaService.atualizar_motorista(self.motorista_atual)
        if motorista_atualizado[0]:
            messagebox.showinfo("Sucesso", motorista_atualizado[1])
            self.app_main.destroy()
        else:
            messagebox.showerror("Erro", motorista_atualizado[1])

    def deletar(self):
        deletar = messagebox.askokcancel("Confirmar", "Excluir registro pernamentemente ?")
        if deletar:
            motorista_deletado = MotoristaService.deletar_motoristas(self.motorista_atual.id_motorista)
            if motorista_deletado[0]:
                messagebox.showinfo("Sucesso", motorista_deletado[1])
                self.app_main.destroy()
            else:
                messagebox.showerror("Erro", motorista_deletado[1])

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
