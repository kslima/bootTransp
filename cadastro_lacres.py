import tkinter
from tkinter import StringVar, Label, Entry, Button, W, messagebox, DISABLED
from service import LacreService
from model import Lacre
from datetime import datetime, date
from utilitarios import NumberUtils, StringUtils
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4



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
        self.lacres_atual = None

        Label(self.app_main, text="Lacres: ", font=(None, 8, 'bold')).grid(sticky=W, column=0, row=0, padx=10)

        Label(self.app_main, text="Lacre 01: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=1, padx=10)
        self.entry_lacre_1 = Entry(self.app_main, textvariable=self.lacre_1)
        self.entry_lacre_1.grid(sticky=W, column=1, row=1, padx=5, pady=2, columnspan=2)
        self.entry_lacre_1.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_lacre), '%P'))

        Label(self.app_main, text="Lacre 02: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=2, padx=10)
        self.entry_lacre_2 = Entry(self.app_main, textvariable=self.lacre_2)
        self.entry_lacre_2.grid(sticky=W, column=1, row=2, padx=5, pady=2, columnspan=2)
        self.entry_lacre_2.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_lacre), '%P'))

        Label(self.app_main, text="Lacre 03: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=3, padx=10)
        self.entry_lacre_3 = Entry(self.app_main, textvariable=self.lacre_3)
        self.entry_lacre_3.grid(sticky=W, column=1, row=3, padx=5, pady=2, columnspan=2)
        self.entry_lacre_3.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_lacre), '%P'))

        Label(self.app_main, text="Lacre 04: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=4, padx=10)
        self.entry_lacre_4 = Entry(self.app_main, textvariable=self.lacre_4)
        self.entry_lacre_4.grid(sticky=W, column=1, row=4, padx=5, pady=2, columnspan=2)
        self.entry_lacre_4.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_lacre), '%P'))

        Label(self.app_main, text="Lacre 05: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=5, padx=10)
        self.entry_lacre_5 = Entry(self.app_main, textvariable=self.lacre_5)
        self.entry_lacre_5.grid(sticky=W, column=1, row=5, padx=5, pady=2, columnspan=2)
        self.entry_lacre_5.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_lacre), '%P'))

        Label(self.app_main, text="Lacre 06: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=6, padx=10)
        self.entry_lacre_6 = Entry(self.app_main, textvariable=self.lacre_6)
        self.entry_lacre_6.grid(sticky=W, column=1, row=6, padx=5, pady=2, columnspan=2)
        self.entry_lacre_6.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_lacre), '%P'))

        Label(self.app_main, text="Lacre 07: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=7, padx=10)
        self.entry_lacre_7 = Entry(self.app_main, textvariable=self.lacre_7)
        self.entry_lacre_7.grid(sticky=W, column=1, row=7, padx=5, pady=2, columnspan=2)
        self.entry_lacre_7.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_lacre), '%P'))

        Label(self.app_main, text="Lacre 08: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=8, padx=10)
        self.entry_lacre_8 = Entry(self.app_main, textvariable=self.lacre_8)
        self.entry_lacre_8.grid(sticky=W, column=1, row=8, padx=5, pady=2, columnspan=2)
        self.entry_lacre_8.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_lacre), '%P'))

        Label(self.app_main, text="Lacre 09: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=9, padx=10)
        self.entry_lacre_9 = Entry(self.app_main, textvariable=self.lacre_9)
        self.entry_lacre_9.grid(sticky=W, column=1, row=9, padx=5, pady=2, columnspan=2)
        self.entry_lacre_9.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_lacre), '%P'))

        Label(self.app_main, text="Lacre 10: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=10, padx=10)
        self.entry_lacre_10 = Entry(self.app_main, textvariable=self.lacre_10)
        self.entry_lacre_10.grid(sticky=W, column=1, row=10, padx=5, pady=2, columnspan=2)
        self.entry_lacre_10.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_lacre), '%P'))

        Label(self.app_main, text="Lacre 11: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=11, padx=10)
        self.entry_lacre_11 = Entry(self.app_main, textvariable=self.lacre_11)
        self.entry_lacre_11.grid(sticky=W, column=1, row=11, padx=5, pady=2, columnspan=2)
        self.entry_lacre_11.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_lacre), '%P'))

        Label(self.app_main, text="Lacre 12: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=12, padx=10)
        self.entry_lacre_12 = Entry(self.app_main, textvariable=self.lacre_12)
        self.entry_lacre_12.grid(sticky=W, column=1, row=12, padx=5, pady=2, columnspan=2)
        self.entry_lacre_12.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_lacre), '%P'))

        Label(self.app_main, text="Lacre 13: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=13, padx=10)
        self.entry_lacre_13 = Entry(self.app_main, textvariable=self.lacre_13)
        self.entry_lacre_13.grid(sticky=W, column=1, row=13, padx=5, pady=2, columnspan=2)
        self.entry_lacre_13.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_lacre), '%P'))

        Label(self.app_main, text="Lacre 14: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=14, padx=10)
        self.entry_lacre_14 = Entry(self.app_main, textvariable=self.lacre_14)
        self.entry_lacre_14.grid(sticky=W, column=1, row=14, padx=5, pady=2, columnspan=2)
        self.entry_lacre_14.config(validate="key", validatecommand=(self.app_main.register(NumberUtils.eh_lacre), '%P'))

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
            if self.lacres_atual is None or self.lacres_atual[0].id_lacre is None:
                self.salvar()
            else:
                self.atualizar()

    def salvar(self):
        codigo = CadastroLacres.gerar_codigo()
        self.lacres_atual = []
        if self.lacre_1.get():
            self.lacres_atual.append(Lacre(codigo=codigo, numero=self.lacre_1.get()))
        if self.lacre_2.get():
            self.lacres_atual.append(Lacre(codigo=codigo, numero=self.lacre_2.get()))
        if self.lacre_3.get():
            self.lacres_atual.append(Lacre(codigo=codigo, numero=self.lacre_3.get()))
        if self.lacre_4.get():
            self.lacres_atual.append(Lacre(codigo=codigo, numero=self.lacre_4.get()))
        if self.lacre_5.get():
            self.lacres_atual.append(Lacre(codigo=codigo, numero=self.lacre_5.get()))
        if self.lacre_6.get():
            self.lacres_atual.append(Lacre(codigo=codigo, numero=self.lacre_6.get()))
        if self.lacre_7.get():
            self.lacres_atual.append(Lacre(codigo=codigo, numero=self.lacre_7.get()))
        if self.lacre_8.get():
            self.lacres_atual.append(Lacre(codigo=codigo, numero=self.lacre_8.get()))
        if self.lacre_9.get():
            self.lacres_atual.append(Lacre(codigo=codigo, numero=self.lacre_9.get()))
        if self.lacre_10.get():
            self.lacres_atual.append(Lacre(codigo=codigo, numero=self.lacre_10.get()))
        if self.lacre_11.get():
            self.lacres_atual.append(Lacre(codigo=codigo, numero=self.lacre_11.get()))
        if self.lacre_12.get():
            self.lacres_atual.append(Lacre(codigo=codigo, numero=self.lacre_12.get()))
        if self.lacre_13.get():
            self.lacres_atual.append(Lacre(codigo=codigo, numero=self.lacre_13.get()))
        if self.lacre_14.get():
            self.lacres_atual.append(Lacre(codigo=codigo, numero=self.lacre_14.get()))

        pacote_lacre_inserido = LacreService.inserir_pacotes_lacres(self.lacres_atual)
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

        pacote_lacre_atualizado = LacreService.atualizar_pacote_lacres(self.lacres_atual)
        if pacote_lacre_atualizado[0]:
            messagebox.showinfo("Sucesso", pacote_lacre_atualizado[1])
            self.app_main.destroy()
        else:
            messagebox.showerror("Erro", pacote_lacre_atualizado[1])

    def deletar(self):
        deletar = messagebox.askokcancel("Confirmar", "Excluir registro pernamentemente ?")
        if deletar:
            pacote_lacre_deletado = LacreService.deletar_pacote_lacres(self.lacres_atual)
            if pacote_lacre_deletado[0]:
                messagebox.showinfo("Sucesso", pacote_lacre_deletado[1])
                self.app_main.destroy()
            else:
                messagebox.showerror("Erro", pacote_lacre_deletado[1])

    def setar_campos_para_edicao(self, lacres):
        self.botao_deletar['state'] = 'normal'
        self.lacres_atual = lacres
        if len(self.lacres_atual) > 0:
            self.lacre_1.set(self.lacres_atual[0].numero)
        if len(self.lacres_atual) > 1:
            self.lacre_2.set(self.lacres_atual[1].numero)
        if len(self.lacres_atual) > 2:
            self.lacre_3.set(self.lacres_atual[2].numero)
        if len(self.lacres_atual) > 3:
            self.lacre_4.set(self.lacres_atual[3].numero)
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

    @staticmethod
    def criar_string_lacres(lista_lacres):
        cont = 0
        string = ""
        for lacre in lista_lacres:
            string += lacre
            if cont < len(lacres) - 1:
                string += '/'
            cont += 1
        return string

    @staticmethod
    def gerar_pdf(lista_lacres):
        try:
            nome_pdf = 'C:\\Users\\kleud\\Desktop\\sqlite\\lacres'
            pdf = canvas.Canvas('{}.pdf'.format(nome_pdf), pagesize=A4)
            x = 720

            # pdf.drawString(50, x, '{}'.format(_lacres))
            pdf.setTitle(nome_pdf)

            pdf.setFont("Helvetica-Bold", 22)
            pdf.drawString(50, 750, 'Lacres')

            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawString(50, 720, 'Quantidade: 8')

            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawString(50, 695, 'Código: 090521090218')

            pdf.setFont("Helvetica", 12)
            lacres_4 = ''
            cont = 0
            y = 670
            for lacre in lacres:
                lacres_4 += lacre + '/'
                if cont == 3:
                    pdf.drawString(50, y, lacres_4[:-1])
                    y = y - 20
                    cont = 0
                    lacres_4 = ''
                    continue
                cont += 1

            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(245, 600, 'Nome e idade')
            pdf.save()
            print('{}.pdf criado com sucesso!'.format(nome_pdf))

        except Exception as e:
            print('erro' + str(e))


if __name__ == '__main__':
    lacres = ["1234567", "1234567", "1234567", "1234567", "1234567", "1234567", "1234567", "1234567", "1234567", "1234567", "1234567", "1234567", "1234567", "1234567"]
    CadastroLacres.gerar_pdf(lacres)
