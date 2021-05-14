import re
import tkinter
from tkinter import StringVar, Label, Entry, Button, W, Checkbutton, messagebox, DISABLED
from tkinter.ttk import Combobox

from service import VeiculoService
from componentes import AutocompleteEntry
from model import Produto, Veiculo
from utilitarios import NumberUtils


class CadastroVeiculo:

    def __init__(self, master):
        self.app_main = tkinter.Toplevel(master)
        # self.app_main = tkinter.Tk()
        self.app_main.title("Cadastro de Veículo")
        self.centralizar_tela()
        self.atualizando_cadastro = False
        self.veiculo_atual = None

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
        combobox_tipo_veiculo = Combobox(self.app_main, textvariable=self.tipo_veiculo, width=40, state="readonly")
        combobox_tipo_veiculo.grid(sticky="we", column=0, row=1, padx=5, columnspan=2)
        combobox_tipo_veiculo['values'] = VeiculoService.listar_tipos_veiculos()

        Label(self.app_main, text="Peso Balança: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=2, padx=5)
        combobox_peso_balanca = Combobox(self.app_main, textvariable=self.tolerancia_balanca, width=40,
                                         state="readonly")
        combobox_peso_balanca.grid(sticky="we", column=0, row=3, padx=5, columnspan=2)
        combobox_peso_balanca['values'] = VeiculoService.listar_tolerancias_balanca()

        Label(self.app_main, text="Qtd. Lacres:", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=4,
                                                                                 padx=5)
        entry_numero_lacres = tkinter.Entry(self.app_main, textvariable=self.quantidade_lacres)
        entry_numero_lacres.grid(sticky="we", column=0, row=5, padx=(5, 10), columnspan=2)
        entry_numero_lacres.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_inteiro),
                                                                    '%P'))

        Label(self.app_main, text="Cavalo: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=6, padx=5)
        entry_placa_1 = Entry(self.app_main, textvariable=self.placa_1)
        entry_placa_1.grid(sticky="we", column=0, row=7, padx=5)
        entry_placa_1.bind("<KeyRelease>", lambda ev: CadastroVeiculo.converter_para_maiusculo(ev, self.placa_1))

        Label(self.app_main, text="Município Cavalo: ", font=(None, 8, 'normal')).grid(sticky=W, column=1, row=6,
                                                                                        padx=5)
        self.entry_municipio_placa_1 = AutocompleteEntry(self.app_main, width=20)
        self.entry_municipio_placa_1.grid(sticky="we", column=1, row=7, padx=(5, 10))
        self.entry_municipio_placa_1.bind("<KeyRelease>", lambda ev: CadastroVeiculo
                                          .converter_para_maiusculo(ev, self.entry_municipio_placa_1.var))

        Label(self.app_main, text="Placa 2: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=8, padx=5)
        entry_placa_2 = Entry(self.app_main, textvariable=self.placa_2)
        entry_placa_2.grid(sticky="we", column=0, row=9, padx=5)
        entry_placa_2.bind("<KeyRelease>", lambda ev: CadastroVeiculo.converter_para_maiusculo(ev, self.placa_2))

        Label(self.app_main, text="Município Placa 2: ", font=(None, 8, 'normal')).grid(sticky=W, column=1,
                                                                                        row=8, padx=5)
        self.entry_municipio_placa_2 = AutocompleteEntry(self.app_main, width=20)
        self.entry_municipio_placa_2.grid(sticky="we", column=1, row=9, padx=(5, 10))
        self.entry_municipio_placa_2.bind("<KeyRelease>", lambda ev: CadastroVeiculo
                                          .converter_para_maiusculo(ev, self.entry_municipio_placa_2.var))

        Label(self.app_main, text="Placa 3: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=10, padx=5)
        entry_placa_3 = Entry(self.app_main, textvariable=self.placa_3)
        entry_placa_3.grid(sticky="we", column=0, row=11, padx=5)
        entry_placa_3.bind("<KeyRelease>", lambda ev: CadastroVeiculo.converter_para_maiusculo(ev, self.placa_3))

        Label(self.app_main, text="Município Placa 3: ", font=(None, 8, 'normal')).grid(sticky=W, column=1,
                                                                                        row=10, padx=5)
        self.entry_municipio_placa_3 = AutocompleteEntry(self.app_main, width=20)
        self.entry_municipio_placa_3.grid(sticky="we", column=1, row=11, padx=(5, 10))
        self.entry_municipio_placa_3.bind("<KeyRelease>", lambda ev: CadastroVeiculo
                                          .converter_para_maiusculo(ev, self.entry_municipio_placa_3.var))

        Label(self.app_main, text="Placa 4: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=12, padx=5)
        entry_placa_4 = Entry(self.app_main, textvariable=self.placa_4)
        entry_placa_4.grid(sticky="we", column=0, row=13, padx=5)
        entry_placa_4.bind("<KeyRelease>", lambda ev: CadastroVeiculo.converter_para_maiusculo(ev, self.placa_4))

        Label(self.app_main, text="Município Placa 4: ", font=(None, 8, 'normal')).grid(sticky=W, column=1,
                                                                                        row=12, padx=5)
        self.entry_municipio_placa_4 = AutocompleteEntry(self.app_main, width=20)
        self.entry_municipio_placa_4.grid(sticky="we", column=1, row=13, padx=(5, 10))
        self.entry_municipio_placa_4.bind("<KeyRelease>", lambda ev: CadastroVeiculo
                                          .converter_para_maiusculo(ev, self.entry_municipio_placa_4.var))

        Button(self.app_main, text='Salvar', command=self.salvar_ou_atualizar) \
            .grid(sticky='we', column=0, row=14, padx=5, pady=5)

        self.botao_deletar = Button(self.app_main, text='Excluir', command=self.deletar, state=DISABLED)
        self.botao_deletar.grid(sticky='we', column=1, row=14, padx=10, pady=10)

    def centralizar_tela(self):
        window_width = self.app_main.winfo_reqwidth()
        window_height = self.app_main.winfo_reqheight()

        position_right = int(self.app_main.winfo_screenwidth() / 2.3 - window_width / 2)
        position_down = int(self.app_main.winfo_screenheight() / 3 - window_height / 2)

        self.app_main.geometry("+{}+{}".format(position_right, position_down))

    @staticmethod
    def converter_para_maiusculo(event, var):
        var.set(var.get().upper())

    def salvar_ou_atualizar(self):
        try:
            self.verificar_campos_obrigatorios()
            if self.veiculo_atual is None or self.veiculo_atual.id_veiculo is None:
                self.salvar()
            else:
                self.atualizar()

        except RuntimeError as e:
            messagebox.showerror("Erro", e)

    def salvar(self):
        self.veiculo_atual = Veiculo(tipo_veiculo=self.tipo_veiculo.get().strip().split("-")[0].strip(),
                                     tolerancia_balanca=self.tolerancia_balanca.get().split("-")[0].strip(),
                                     quantidade_lacres=self.quantidade_lacres.get(),
                                     placa_1=self.placa_1.get().strip(),
                                     placa_2=self.placa_2.get().strip(),
                                     placa_3=self.placa_3.get().strip(),
                                     placa_4=self.placa_4.get().strip(),
                                     codigo_municipio_placa_1=self.entry_municipio_placa_1.var.get().strip(),
                                     codigo_municipio_placa_2=self.entry_municipio_placa_2.var.get().strip(),
                                     codigo_municipio_placa_3=self.entry_municipio_placa_3.var.get().strip(),
                                     codigo_municipio_placa_4=self.entry_municipio_placa_4.var.get().strip())

        veiculo_inserido = VeiculoService.inserir_veiculo(self.veiculo_atual)
        if veiculo_inserido[0]:
            messagebox.showinfo("Sucesso", veiculo_inserido[1])
            self.app_main.destroy()
        else:
            messagebox.showerror("Erro", veiculo_inserido[1])

    def atualizar(self):
        self.veiculo_atual.tipo_veiculo = self.tipo_veiculo.get().split("-")[0].strip()
        self.veiculo_atual.tolerancia_balanca = self.tolerancia_balanca.get().split("-")[0].strip()
        self.veiculo_atual.quantidade_lacres = self.quantidade_lacres.get().strip()
        self.veiculo_atual.placa_1 = self.placa_1.get().strip()
        self.veiculo_atual.placa_2 = self.placa_2.get().strip()
        self.veiculo_atual.placa_3 = self.placa_3.get().strip()
        self.veiculo_atual.placa_4 = self.placa_4.get().strip()
        self.veiculo_atual.codigo_municipio_placa_1 = self.entry_municipio_placa_1.var.get().strip()
        self.veiculo_atual.codigo_municipio_placa_2 = self.entry_municipio_placa_2.var.get().strip()
        self.veiculo_atual.codigo_municipio_placa_3 = self.entry_municipio_placa_3.var.get().strip()
        self.veiculo_atual.codigo_municipio_placa_4 = self.entry_municipio_placa_4.var.get().strip()
        veiculo_atualizado = VeiculoService.atualizar_veiculo(self.veiculo_atual)
        if veiculo_atualizado[0]:
            messagebox.showinfo("Sucesso", veiculo_atualizado[1])
            self.app_main.destroy()
        else:
            messagebox.showerror("Erro", veiculo_atualizado[1])

    def deletar(self):
        deletar = messagebox.askokcancel("Confirmar", "Excluir registro pernamentemente ?")
        if deletar:
            veiculo_deletado = VeiculoService.deletar_veiculo(self.veiculo_atual.id_veiculo)
            if veiculo_deletado[0]:
                messagebox.showinfo("Sucesso", veiculo_deletado[1])
                self.app_main.destroy()
            else:
                messagebox.showerror("Erro", veiculo_deletado[1])

    def verificar_campos_obrigatorios(self):
        if self.tipo_veiculo.get() == "":
            raise RuntimeError("Campo obrigatório", "O campo 'Tipo Veículo' é obrigatório!")

        if self.tolerancia_balanca.get() == "":
            RuntimeError("Campo obrigatório", "O campo 'Tolerância Balança' é obrigatório!")

        if not self.placa_1.get():
            RuntimeError("Campo obrigatório", "A placa do cavalo é obrigatório!")

        if not CadastroVeiculo.verificar_formato_placa(self.placa_1.get()):
            print('lancando erro')
            RuntimeError("Erro", "A placa do cavalo não está no formato AAA1111 ou AAA1X11!")

    @staticmethod
    def verificar_formato_placa(placa):
        resp = bool(re.match("[A-Z]{3}[0-9][0-9A-Z][0-9]{2}", placa))
        print(resp)
        return resp

    def setar_campos_para_edicao(self, veiculo):
        self.botao_deletar['state'] = 'normal'
        self.veiculo_atual = veiculo
        self.tipo_veiculo.set(veiculo.tipo_veiculo)
        self.tolerancia_balanca.set(veiculo.tolerancia_balanca)
        self.quantidade_lacres.set(veiculo.quantidade_lacres)
        self.placa_1.set(veiculo.placa_1)
        self.placa_2.set(veiculo.placa_2 if veiculo.placa_2 else '')
        self.placa_3.set(veiculo.placa_3 if veiculo.placa_3 else '')
        self.placa_4.set(veiculo.placa_4 if veiculo.placa_4 else '')
        self.entry_municipio_placa_1.var.set(veiculo.codigo_municipio_placa_1)
        self.entry_municipio_placa_2.var.set(veiculo.codigo_municipio_placa_2 if veiculo.codigo_municipio_placa_2
                                             else '')
        self.entry_municipio_placa_3.var.set(veiculo.codigo_municipio_placa_3 if veiculo.codigo_municipio_placa_3
                                             else '')
        self.entry_municipio_placa_4.var.set(veiculo.codigo_municipio_placa_4 if veiculo.codigo_municipio_placa_4
                                             else '')


if __name__ == '__main__':
    app_main = tkinter.Tk()
    CadastroVeiculo(app_main)
    app_main.mainloop()
