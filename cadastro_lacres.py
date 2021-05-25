import subprocess
import tempfile
import tkinter
from datetime import datetime, date
from tkinter import StringVar, Label, Entry, Button, W, messagebox, DISABLED
from reportlab.graphics.barcode import code39
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from model import Lacre
from service import LacreService
from utilitarios import NumberUtils


class CadastroLacres:

    def __init__(self, master):
        self.app_main = tkinter.Toplevel(master)
        self.app_main.title("Cadastro de Lacres")
        self.app_main.resizable(False, False)
        # self.app_main.geometry('220x400')
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
        self.lacres_atual = None

        Label(self.app_main, text="Lacres: ", font=(None, 8, 'bold')).grid(sticky=W, column=0, row=0, padx=10)

        Label(self.app_main, text="Lacre 01: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=1, padx=10)
        self.entry_lacre_1 = Entry(self.app_main, textvariable=self.lacre_1)
        self.entry_lacre_1.grid(sticky="we", column=1, row=1, padx=(0, 10), pady=2, columnspan=2)
        self.entry_lacre_1.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_lacre), '%P'))
        self.entry_lacre_1.bind('<Return>', CadastroLacres.focar_proximo_elemento)
        self.entry_lacre_1.bind("<FocusOut>", lambda event: self.preencher_com_zeros(event, self.lacre_1))

        Label(self.app_main, text="Lacre 02: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=2, padx=10)
        self.entry_lacre_2 = Entry(self.app_main, textvariable=self.lacre_2)
        self.entry_lacre_2.grid(sticky="we", column=1, row=2, padx=(0, 10), pady=2, columnspan=2)
        self.entry_lacre_2.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_lacre), '%P'))
        self.entry_lacre_2.bind('<Return>', CadastroLacres.focar_proximo_elemento)
        self.entry_lacre_2.bind("<FocusOut>", lambda event: self.preencher_com_zeros(event, self.lacre_2))

        Label(self.app_main, text="Lacre 03: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=3, padx=10)
        self.entry_lacre_3 = Entry(self.app_main, textvariable=self.lacre_3)
        self.entry_lacre_3.grid(sticky="we", column=1, row=3, padx=(0, 10), pady=2, columnspan=2)
        self.entry_lacre_3.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_lacre), '%P'))
        self.entry_lacre_3.bind('<Return>', CadastroLacres.focar_proximo_elemento)
        self.entry_lacre_3.bind("<FocusOut>", lambda event: self.preencher_com_zeros(event, self.lacre_3))

        Label(self.app_main, text="Lacre 04: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=4, padx=10)
        self.entry_lacre_4 = Entry(self.app_main, textvariable=self.lacre_4)
        self.entry_lacre_4.grid(sticky="we", column=1, row=4, padx=(0, 10), pady=2, columnspan=2)
        self.entry_lacre_4.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_lacre), '%P'))
        self.entry_lacre_4.bind('<Return>', CadastroLacres.focar_proximo_elemento)
        self.entry_lacre_4.bind("<FocusOut>", lambda event: self.preencher_com_zeros(event, self.lacre_4))

        Label(self.app_main, text="Lacre 05: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=5, padx=10)
        self.entry_lacre_5 = Entry(self.app_main, textvariable=self.lacre_5)
        self.entry_lacre_5.grid(sticky="we", column=1, row=5, padx=(0, 10), pady=2, columnspan=2)
        self.entry_lacre_5.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_lacre), '%P'))
        self.entry_lacre_5.bind('<Return>', CadastroLacres.focar_proximo_elemento)
        self.entry_lacre_5.bind("<FocusOut>", lambda event: self.preencher_com_zeros(event, self.lacre_5))

        Label(self.app_main, text="Lacre 06: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=6, padx=10)
        self.entry_lacre_6 = Entry(self.app_main, textvariable=self.lacre_6)
        self.entry_lacre_6.grid(sticky="we", column=1, row=6, padx=(0, 10), pady=2, columnspan=2)
        self.entry_lacre_6.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_lacre), '%P'))
        self.entry_lacre_6.bind('<Return>', CadastroLacres.focar_proximo_elemento)
        self.entry_lacre_6.bind("<FocusOut>", lambda event: self.preencher_com_zeros(event, self.lacre_6))

        Label(self.app_main, text="Lacre 07: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=7, padx=10)
        self.entry_lacre_7 = Entry(self.app_main, textvariable=self.lacre_7)
        self.entry_lacre_7.grid(sticky="we", column=1, row=7, padx=(0, 10), pady=2, columnspan=2)
        self.entry_lacre_7.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_lacre), '%P'))
        self.entry_lacre_7.bind('<Return>', CadastroLacres.focar_proximo_elemento)
        self.entry_lacre_7.bind("<FocusOut>", lambda event: self.preencher_com_zeros(event, self.lacre_7))

        Label(self.app_main, text="Lacre 08: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=8, padx=10)
        self.entry_lacre_8 = Entry(self.app_main, textvariable=self.lacre_8)
        self.entry_lacre_8.grid(sticky="we", column=1, row=8, padx=(0, 10), pady=2, columnspan=2)
        self.entry_lacre_8.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_lacre), '%P'))
        self.entry_lacre_8.bind('<Return>', CadastroLacres.focar_proximo_elemento)
        self.entry_lacre_8.bind("<FocusOut>", lambda event: self.preencher_com_zeros(event, self.lacre_8))

        Label(self.app_main, text="Lacre 09: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=9, padx=10)
        self.entry_lacre_9 = Entry(self.app_main, textvariable=self.lacre_9)
        self.entry_lacre_9.grid(sticky="we", column=1, row=9, padx=(0, 10), pady=2, columnspan=2)
        self.entry_lacre_9.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_lacre), '%P'))
        self.entry_lacre_9.bind('<Return>', CadastroLacres.focar_proximo_elemento)
        self.entry_lacre_9.bind("<FocusOut>", lambda event: self.preencher_com_zeros(event, self.lacre_9))

        Label(self.app_main, text="Lacre 10: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=10, padx=10)
        self.entry_lacre_10 = Entry(self.app_main, textvariable=self.lacre_10)
        self.entry_lacre_10.grid(sticky="we", column=1, row=10, padx=(0, 10), pady=2, columnspan=2)
        self.entry_lacre_10.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_lacre), '%P'))
        self.entry_lacre_10.bind('<Return>', CadastroLacres.focar_proximo_elemento)
        self.entry_lacre_10.bind("<FocusOut>", lambda event: self.preencher_com_zeros(event, self.lacre_10))

        Label(self.app_main, text="Lacre 11: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=11, padx=10)
        self.entry_lacre_11 = Entry(self.app_main, textvariable=self.lacre_11)
        self.entry_lacre_11.grid(sticky="we", column=1, row=11, padx=(0, 10), pady=2, columnspan=2)
        self.entry_lacre_11.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_lacre), '%P'))
        self.entry_lacre_11.bind('<Return>', CadastroLacres.focar_proximo_elemento)
        self.entry_lacre_11.bind("<FocusOut>", lambda event: self.preencher_com_zeros(event, self.lacre_11))

        Label(self.app_main, text="Lacre 12: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=12, padx=10)
        self.entry_lacre_12 = Entry(self.app_main, textvariable=self.lacre_12)
        self.entry_lacre_12.grid(sticky="we", column=1, row=12, padx=(0, 10), pady=2, columnspan=2)
        self.entry_lacre_12.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_lacre), '%P'))
        self.entry_lacre_12.bind('<Return>', CadastroLacres.focar_proximo_elemento)
        self.entry_lacre_12.bind("<FocusOut>", lambda event: self.preencher_com_zeros(event, self.lacre_12))

        Label(self.app_main, text="Lacre 13: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=13, padx=10)
        self.entry_lacre_13 = Entry(self.app_main, textvariable=self.lacre_13)
        self.entry_lacre_13.grid(sticky="we", column=1, row=13, padx=(0, 10), pady=2, columnspan=2)
        self.entry_lacre_13.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_lacre), '%P'))
        self.entry_lacre_13.bind('<Return>', CadastroLacres.focar_proximo_elemento)
        self.entry_lacre_13.bind("<FocusOut>", lambda event: self.preencher_com_zeros(event, self.lacre_13))

        Label(self.app_main, text="Lacre 14: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=14, padx=10)
        self.entry_lacre_14 = Entry(self.app_main, textvariable=self.lacre_14)
        self.entry_lacre_14.grid(sticky="we", column=1, row=14, padx=(0, 10), pady=2, columnspan=2)
        self.entry_lacre_14.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_lacre), '%P'))
        self.entry_lacre_14.bind("<FocusOut>", lambda event: self.preencher_com_zeros(event, self.lacre_14))

        self.botao_salvar = Button(self.app_main, text='Salvar', command=self.salvar_ou_atualizar)
        self.botao_salvar.grid(sticky='we', column=0, row=15, padx=10, pady=10)

        self.botao_deletar = Button(self.app_main, text='Excluir', command=self.deletar, state=DISABLED)
        self.botao_deletar.grid(sticky='we', column=1, row=15, padx=10, pady=10)

        self.botao_gerar_envelope = Button(self.app_main, text='Gerar Envelope', state=DISABLED,
                                           command=self.gerar_envelope)
        self.botao_gerar_envelope.grid(sticky='we', column=2, row=15, padx=10, pady=10)

    @staticmethod
    def focar_proximo_elemento(event):
        event.widget.tk_focusNext().focus()

    @staticmethod
    def preencher_com_zeros(event, entry):
        texto = entry.get().strip()
        if 7 > len(texto) > 0:
            entry.set(texto.zfill(7))

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

    def salvar_ou_atualizar(self):
        try:
            self.lacres_atual = self.preencher_lista_lacres()
            self.verificar_campos_obrigatorios()
            if self.lacres_atual is None or self.lacres_atual[0].id is None:
                self.salvar()
            else:
                self.atualizar()

        except Exception as e:
            messagebox.showerror("Erro", e)
        finally:
            self.app_main.lift()

    def verificar_campos_obrigatorios(self):
        if len(self.lacres_atual) < 4:
            raise RuntimeError("Informar pelo menos 4 lacres!")

    def preencher_lista_lacres(self):
        lacres = []
        self.preencher_com_zeros(None, self.lacre_1)
        self.preencher_com_zeros(None, self.lacre_2)
        self.preencher_com_zeros(None, self.lacre_3)
        self.preencher_com_zeros(None, self.lacre_4)
        self.preencher_com_zeros(None, self.lacre_5)
        self.preencher_com_zeros(None, self.lacre_6)
        self.preencher_com_zeros(None, self.lacre_7)
        self.preencher_com_zeros(None, self.lacre_8)
        self.preencher_com_zeros(None, self.lacre_9)
        self.preencher_com_zeros(None, self.lacre_10)
        self.preencher_com_zeros(None, self.lacre_11)
        self.preencher_com_zeros(None, self.lacre_12)
        self.preencher_com_zeros(None, self.lacre_13)
        self.preencher_com_zeros(None, self.lacre_14)

        codigo = CadastroLacres.gerar_codigo()
        self.lacres_atual = []
        if self.lacre_1.get():
            lacre = Lacre()
            lacre.codigo = codigo
            lacre.numero = self.lacre_1.get().strip()
            lacres.append(lacre)
        if self.lacre_2.get():
            lacre = Lacre()
            lacre.codigo = codigo
            lacre.numero = self.lacre_2.get().strip()
            lacres.append(lacre)
        if self.lacre_3.get():
            lacre = Lacre()
            lacre.codigo = codigo
            lacre.numero = self.lacre_3.get().strip()
            lacres.append(lacre)
        if self.lacre_4.get():
            lacre = Lacre()
            lacre.codigo = codigo
            lacre.numero = self.lacre_4.get().strip()
            lacres.append(lacre)
        if self.lacre_5.get():
            lacre = Lacre()
            lacre.codigo = codigo
            lacre.numero = self.lacre_5.get().strip()
            lacres.append(lacre)
        if self.lacre_6.get():
            lacre = Lacre()
            lacre.codigo = codigo
            lacre.numero = self.lacre_6.get().strip()
            lacres.append(lacre)
        if self.lacre_7.get():
            lacre = Lacre()
            lacre.codigo = codigo
            lacre.numero = self.lacre_7.get().strip()
            lacres.append(lacre)
        if self.lacre_8.get():
            lacre = Lacre()
            lacre.codigo = codigo
            lacre.numero = self.lacre_8.get().strip()
            lacres.append(lacre)
        if self.lacre_9.get():
            lacre = Lacre()
            lacre.codigo = codigo
            lacre.numero = self.lacre_9.get().strip()
            lacres.append(lacre)
        if self.lacre_10.get():
            lacre = Lacre()
            lacre.codigo = codigo
            lacre.numero = self.lacre_10.get().strip()
            lacres.append(lacre)
        if self.lacre_11.get():
            lacre = Lacre()
            lacre.codigo = codigo
            lacre.numero = self.lacre_11.get().strip()
            lacres.append(lacre)
        if self.lacre_12.get():
            lacre = Lacre()
            lacre.codigo = codigo
            lacre.numero = self.lacre_12.get().strip()
            lacres.append(lacre)
        if self.lacre_13.get():
            lacre = Lacre()
            lacre.codigo = codigo
            lacre.numero = self.lacre_13.get().strip()
            lacres.append(lacre)
        if self.lacre_14.get():
            lacre = Lacre()
            lacre.codigo = codigo
            lacre.numero = self.lacre_14.get().strip()
            lacres.append(lacre)
        return lacres

    def salvar(self):
        try:
            LacreService.salvar_ou_atualizar(self.lacres_atual)
            messagebox.showinfo("Sucesso", 'Lacres salvos com sucesso!')
            self.gerar_envelope()
            self.novo_cadastro()
        except Exception as e:
            raise e

    @staticmethod
    def gerar_codigo():
        data_atual = date.today().strftime("%d%m%y")
        hora_atual = datetime.now().strftime("%H%M%S")
        return '{}{}'.format(data_atual, hora_atual)

    def atualizar(self):
        try:
            if len(self.lacres_atual) > 0:
                self.lacres_atual[0].numero = self.lacre_1.get()
            if len(self.lacres_atual) > 1:
                self.lacres_atual[1].numero = self.lacre_2.get()
            if len(self.lacres_atual) > 2:
                self.lacres_atual[2].numero = self.lacre_3.get()
            if len(self.lacres_atual) > 3:
                self.lacres_atual[3].numero = self.lacre_4.get()
            if len(self.lacres_atual) > 4:
                self.lacres_atual[4].numero = self.lacre_5.get()
            if len(self.lacres_atual) > 5:
                self.lacres_atual[5].numero = self.lacre_6.get()
            if len(self.lacres_atual) > 6:
                self.lacres_atual[6].numero = self.lacre_7.get()
            if len(self.lacres_atual) > 7:
                self.lacres_atual[7].numero = self.lacre_8.get()
            if len(self.lacres_atual) > 8:
                self.lacres_atual[8].numero = self.lacre_9.get()
            if len(self.lacres_atual) > 9:
                self.lacres_atual[9].numero = self.lacre_10.get()
            if len(self.lacres_atual) > 10:
                self.lacres_atual[10].numero = self.lacre_11.get()
            if len(self.lacres_atual) > 11:
                self.lacres_atual[11].numero = self.lacre_12.get()
            if len(self.lacres_atual) > 12:
                self.lacres_atual[12].numero = self.lacre_13.get()
            if len(self.lacres_atual) > 13:
                self.lacres_atual[13].numero = self.lacre_14.get()

            # desabilitar campos vazios
            if len(self.lacres_atual) < 2:
                self.entry_lacre_2['state'] = 'disabled'

            if len(self.lacres_atual) < 3:
                self.entry_lacre_3['state'] = 'disabled'

            if len(self.lacres_atual) < 4:
                self.entry_lacre_4['state'] = 'disabled'

            if len(self.lacres_atual) < 5:
                self.entry_lacre_5['state'] = 'disabled'

            if len(self.lacres_atual) < 6:
                self.entry_lacre_6['state'] = 'disabled'

            if len(self.lacres_atual) < 7:
                self.entry_lacre_7['state'] = 'disabled'

            if len(self.lacres_atual) < 8:
                self.entry_lacre_8['state'] = 'disabled'

            if len(self.lacres_atual) < 9:
                self.entry_lacre_9['state'] = 'disabled'

            if len(self.lacres_atual) < 10:
                self.entry_lacre_10['state'] = 'disabled'

            if len(self.lacres_atual) < 11:
                self.entry_lacre_11['state'] = 'disabled'

            if len(self.lacres_atual) < 12:
                self.entry_lacre_12['state'] = 'disabled'

            if len(self.lacres_atual) < 13:
                self.entry_lacre_13['state'] = 'disabled'

            if len(self.lacres_atual) < 14:
                self.entry_lacre_14['state'] = 'disabled'

            LacreService.salvar_ou_atualizar(self.lacres_atual)
            messagebox.showinfo("Sucesso", "Lacres atualizados com sucesso!")
            self.app_main.destroy()

        except Exception as e:
            raise e

    def deletar(self):
        deletar = messagebox.askokcancel("Confirmar", "Excluir registro pernamentemente ?")
        if deletar:
            try:
                LacreService.deletar(self.lacres_atual)
                messagebox.showinfo("Sucesso", "Lacres deletados com sucesso!")
                self.app_main.destroy()
            except Exception as e:
                raise e

    def setar_campos_para_edicao(self, lacres):

        self.botao_salvar['state'] = 'disable'
        self.botao_deletar['state'] = 'normal'
        self.botao_gerar_envelope['state'] = 'normal'
        self.lacres_atual = lacres

        # setando o 4 primeiros lacres (pelo menos 4 sao obrigatorios)
        self.lacre_1.set(self.lacres_atual[0].numero)
        self.lacre_2.set(self.lacres_atual[1].numero)
        self.lacre_3.set(self.lacres_atual[2].numero)
        self.lacre_4.set(self.lacres_atual[3].numero)

        # setando os outros lacres (não obrigatorios)
        if len(self.lacres_atual) > 4:
            self.lacre_5.set(self.lacres_atual[4].numero)
        if len(self.lacres_atual) > 5:
            self.lacre_6.set(self.lacres_atual[5].numero)
        if len(self.lacres_atual) > 6:
            self.lacre_7.set(self.lacres_atual[6].numero)
        if len(self.lacres_atual) > 7:
            self.lacre_8.set(self.lacres_atual[7].numero)
        if len(self.lacres_atual) > 8:
            self.lacre_9.set(self.lacres_atual[8].numero)
        if len(self.lacres_atual) > 9:
            self.lacre_10.set(self.lacres_atual[9].numero)
        if len(self.lacres_atual) > 10:
            self.lacre_11.set(self.lacres_atual[10].numero)
        if len(self.lacres_atual) > 11:
            self.lacre_12.set(self.lacres_atual[11].numero)
        if len(self.lacres_atual) > 12:
            self.lacre_13.set(self.lacres_atual[12].numero)
        if len(self.lacres_atual) > 13:
            self.lacre_14.set(self.lacres_atual[13].numero)

        self.entry_lacre_14['state'] = 'disable'
        self.entry_lacre_13['state'] = 'disable'
        self.entry_lacre_12['state'] = 'disable'
        self.entry_lacre_11['state'] = 'disable'
        self.entry_lacre_10['state'] = 'disable'
        self.entry_lacre_9['state'] = 'disable'
        self.entry_lacre_8['state'] = 'disable'
        self.entry_lacre_7['state'] = 'disable'
        self.entry_lacre_6['state'] = 'disable'
        self.entry_lacre_5['state'] = 'disable'
        self.entry_lacre_4['state'] = 'disable'
        self.entry_lacre_3['state'] = 'disable'
        self.entry_lacre_2['state'] = 'disable'
        self.entry_lacre_1['state'] = 'disable'

        # desabilitando os campos que nao contem lacres não é possível adicionar lacres na edicao, apenas editar os
        # que ja estao lançados. o motivo de nao poder adicionar lacre é que adicionar seria um novo inserte no
        # banco, e como o código é um campo unique, isso geraria um comflito no banco de dados.
        '''
                if len(self.lacres_atual) < 14:
            self.entry_lacre_14['state'] = 'disable'
        if len(self.lacres_atual) < 13:
            self.entry_lacre_13['state'] = 'disable'
        if len(self.lacres_atual) < 12:
            self.entry_lacre_12['state'] = 'disable'
        if len(self.lacres_atual) < 11:
            self.entry_lacre_11['state'] = 'disable'
        if len(self.lacres_atual) < 10:
            self.entry_lacre_10['state'] = 'disable'
        if len(self.lacres_atual) < 9:
            self.entry_lacre_9['state'] = 'disable'
        if len(self.lacres_atual) < 8:
            self.entry_lacre_8['state'] = 'disable'
        if len(self.lacres_atual) < 7:
            self.entry_lacre_7['state'] = 'disable'
        if len(self.lacres_atual) < 6:
            self.entry_lacre_6['state'] = 'disable'
        if len(self.lacres_atual) < 5:
            self.entry_lacre_5['state'] = 'disable'
        '''

    @staticmethod
    def criar_string_lacres(lista_lacres):
        cont = 0
        string = ""
        for lacre in lista_lacres:
            string += lacre
            if cont < len(lista_lacres) - 1:
                string += '/'
            cont += 1
        return string

    def gerar_envelope(self):
        try:
            tamanho_lista = len(self.lacres_atual)
            f = tempfile.NamedTemporaryFile()
            nome_pdf = f.name + '.pdf'
            pdf = canvas.Canvas(nome_pdf, pagesize=A4)
            y = 700
            x_inicial = 40 * mm

            pdf.setTitle(nome_pdf)

            pdf.setFont("Helvetica-Bold", 22)
            pdf.drawString(x_inicial, y, 'Lacres')

            y = y - 25
            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawString(x_inicial, y, "Quantidade: {}".format(tamanho_lista))

            y = y - 25
            codigo = self.lacres_atual[0].codigo
            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawString(x_inicial, y, 'Código: {}'.format(codigo))

            pdf.setFont("Helvetica", 12)
            i = 0
            f = 4
            continuar = True

            lista_lacres = []
            for lacre in self.lacres_atual:
                lista_lacres.append(lacre.numero)

            while continuar:
                y -= 25
                s = ' / '.join(lista_lacres[i:f])
                pdf.drawString(x_inicial, y, s)
                i += 4
                f += 4
                if i > tamanho_lista:
                    continuar = False

            bc = code39.Extended39(codigo, barWidth=0.5 * mm, barHeight=20 * mm)
            y = y - 70
            bc.drawOn(pdf, x_inicial - 20, y)

            pdf.setFont("Helvetica-Bold", 14)
            linha = '--------------------------------------------------------------------------------------------------'
            pdf.drawString(x_inicial - 50, 380, linha)

            # now create the actual PDF
            pdf.showPage()

            pdf.save()

            subprocess.Popen([nome_pdf], shell=True)

        except Exception as e:
            print('erro' + str(e))

    def novo_cadastro(self):
        self.entry_lacre_1.focus()
        self.lacre_1.set('')
        self.lacre_2.set('')
        self.lacre_3.set('')
        self.lacre_4.set('')
        self.lacre_5.set('')
        self.lacre_6.set('')
        self.lacre_7.set('')
        self.lacre_8.set('')
        self.lacre_9.set('')
        self.lacre_10.set('')
        self.lacre_11.set('')
        self.lacre_12.set('')
        self.lacre_13.set('')
        self.lacre_14.set('')
        self.lacres_atual = None


if __name__ == '__main__':
    '''
    lacres = ["1234567", "1234567", "1234567", "1234567", "1234567", "1234567", "1234567", "1234567", "1234567",
                 "1234567", "1234567", "1234567", "1234567", "1234567"]
       CadastroLacres.gerar_pdf(lacres)
    '''
    app_main = tkinter.Tk()
    CadastroLacres(app_main)
    app_main.mainloop()
