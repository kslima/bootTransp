import re
import tkinter
from tkinter import IntVar, StringVar, Label, Entry, Button, W, Checkbutton, messagebox, DISABLED
from tkinter.ttk import Combobox

from service import VeiculoService, TipoVeiculoService, PesoBalancaService, MunicipioService
from componentes import AutocompleteEntry
from model2 import Veiculo
from utilitarios import NumberUtils


class CadastroVeiculo:

    def __init__(self, master):
        self.app_main = tkinter.Toplevel(master)
        # self.app_main = tkinter.Tk()
        self.app_main.title("Cadastro de Veículo")
        self.centralizar_tela()
        self.atualizando_cadastro = False
        self.veiculo_atual = None
        self.combobox_tipo_veiculo = None
        self.combobox_peso_balanca = None

        self.tipo_veiculo = StringVar()
        self.tolerancia_balanca = StringVar()
        self.quantidade_lacres = IntVar()
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
        self.combobox_tipo_veiculo = Combobox(self.app_main, textvariable=self.tipo_veiculo, width=40, state="readonly")
        self.combobox_tipo_veiculo.grid(sticky="we", column=0, row=1, padx=5, columnspan=2)
        self.combobox_tipo_veiculo['values'] = [t.descricao for t in TipoVeiculoService.listar_tipos_veiculos()]

        Label(self.app_main, text="Peso Balança: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=2, padx=5)
        self.combobox_peso_balanca = Combobox(self.app_main, textvariable=self.tolerancia_balanca, width=40,
                                         state="readonly")
        self.combobox_peso_balanca.grid(sticky="we", column=0, row=3, padx=5, columnspan=2)
        self.combobox_peso_balanca['values'] = [t.descricao for t in PesoBalancaService.listar_pesos_balanca()]

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
            if self.veiculo_atual is None or self.veiculo_atual.id is None:
                self.salvar()
            else:
                self.atualizar()

        except RuntimeError as e:
            messagebox.showerror("Erro", e)

    def salvar(self):
        try:
            self.veiculo_atual = Veiculo()
            self.atualizar_dados_veiculo(self.veiculo_atual)
            VeiculoService.salvar_ou_atualizar(self.veiculo_atual)
            messagebox.showinfo("Sucesso", "Veículo salvo com sucesso!")
            self.app_main.destroy()
        except Exception as e:
            messagebox.showerror("Erro", e)

    def atualizar(self):
        try:
            self.atualizar_dados_veiculo(self.veiculo_atual)
            VeiculoService.salvar_ou_atualizar(self.veiculo_atual)
            messagebox.showinfo("Sucesso", "Veículo atualizado com sucesso!")
            self.app_main.destroy()
        except Exception as e:
            messagebox.showerror("Erro", e)

    def deletar(self):
        deletar = messagebox.askokcancel("Confirmar", "Excluir registro pernamentemente ?")
        if deletar:
            try:
                VeiculoService.deletar_veiculo(self.veiculo_atual)
                messagebox.showinfo("Sucesso", "Veículo deletado com sucesso!")

            except Exception as e:
                messagebox.showerror("Erro", "Erro deletar veículo!\n{}".format(e))

    def atualizar_dados_veiculo(self, veiculo):
        self.botao_deletar['state'] = 'normal'
        tipo_veiculo = TipoVeiculoService.pesquisar_tipo_veiculo_pela_descricao(self.tipo_veiculo.get())
        peso_balanca = PesoBalancaService.pesquisar_pesos_balanca_pela_descricao(self.tolerancia_balanca.get())
        quantidade_lacres = self.quantidade_lacres.get()
        placa1 = self.placa_1.get().strip() if self.placa_1.get().strip() else None
        placa2 = self.placa_2.get().strip() if self.placa_2.get().strip() else None
        placa3 = self.placa_3.get().strip() if self.placa_3.get().strip() else None
        placa4 = self.placa_4.get().strip() if self.placa_4.get().strip() else None
        c1 = CadastroVeiculo.extrair_codigo_municipio(self.entry_municipio_placa_1.get())
        c2 = CadastroVeiculo.extrair_codigo_municipio(self.entry_municipio_placa_2.get())
        c3 = CadastroVeiculo.extrair_codigo_municipio(self.entry_municipio_placa_3.get())
        c4 = CadastroVeiculo.extrair_codigo_municipio(self.entry_municipio_placa_4.get())
        municipio_placa1 = MunicipioService.pesquisar_municipio_pelo_codigo(c1)
        municipio_placa2 = MunicipioService.pesquisar_municipio_pelo_codigo(c2)
        municipio_placa3 = MunicipioService.pesquisar_municipio_pelo_codigo(c3)
        municipio_placa4 = MunicipioService.pesquisar_municipio_pelo_codigo(c4)

        veiculo.tipo_veiculo = tipo_veiculo
        veiculo.peso_balanca = peso_balanca
        veiculo.quantidade_lacres = quantidade_lacres
        veiculo.placa1 = placa1
        veiculo.placa2 = placa2
        veiculo.placa3 = placa3
        veiculo.placa4 = placa4
        veiculo.municipio_placa1 = municipio_placa1
        veiculo.municipio_placa2 = municipio_placa2
        veiculo.municipio_placa3 = municipio_placa3
        veiculo.municipio_placa4 = municipio_placa4

    @staticmethod
    def extrair_codigo_municipio(municipio):
        return "".join(re.findall("\\d*", municipio))

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

        CadastroVeiculo.selecionar_item_combobox(self.combobox_tipo_veiculo, veiculo.tipo_veiculo.descricao)
        CadastroVeiculo.selecionar_item_combobox(self.combobox_peso_balanca, veiculo.peso_balanca.descricao)
        self.quantidade_lacres.set(veiculo.quantidade_lacres)
        self.placa_1.set(veiculo.placa1)
        self.placa_2.set(veiculo.placa2 if veiculo.placa2 else '')
        self.placa_3.set(veiculo.placa3 if veiculo.placa3 else '')
        self.placa_4.set(veiculo.placa4 if veiculo.placa4 else '')

        self.entry_municipio_placa_1.var.set('{} {}'.format(veiculo.municipio_placa1.uf, veiculo.municipio_placa1.codigo))

        if veiculo.placa2 is not None:
            self.entry_municipio_placa_2.var.set(
                '{} {}'.format(veiculo.municipio_placa2.uf, veiculo.municipio_placa2.codigo))

        if veiculo.placa3 is not None:
            self.entry_municipio_placa_3.var.set(
                '{} {}'.format(veiculo.municipio_placa3.uf, veiculo.municipio_placa3.codigo))

        if veiculo.placa4 is not None:
            self.entry_municipio_placa_4.var.set(
                '{} {}'.format(veiculo.municipio_placa4.uf, veiculo.municipio_placa4.codigo))

    @staticmethod
    def selecionar_item_combobox(combobox, selecao):
        cont = 0
        for v in combobox['values']:
            if v == selecao:
                combobox.current(cont)
            cont += 1


if __name__ == '__main__':
    app_main = tkinter.Tk()
    CadastroVeiculo(app_main)
    app_main.mainloop()
