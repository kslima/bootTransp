from tkinter import StringVar, Label, Toplevel, Entry, Tk, W, Button


class DialogoEntrada:

    def __init__(self, master):
        self.top = Toplevel(master)
        self.centralizar_tela()
        self.entrada = StringVar()

        Label(self.top, text="Entrada: ", font=(None, 8, 'normal')).grid(sticky=W, column=0, row=0, padx=10)
        self.entry_entrada = Entry(self.top, textvariable=self.entrada, width=50)
        self.entry_entrada.grid(sticky="we", column=0, row=1, padx=10, pady=2, columnspan=2)
        self.entry_entrada.bind('<Return>', lambda event: self.fechar_event(event))

        botao_inserir = Button(self.top, text='Inserir', command=self.fechar)
        botao_inserir.grid(sticky='we', column=0, row=2, padx=10, pady=10)

        Button(self.top, text='Cancelar', command=self.fechar).grid(sticky='we', column=1,
                                                                                           row=2, padx=10, pady=10)
        self.entry_entrada.focus()

    def centralizar_tela(self):
        # Gets the requested values of the height and widht.
        window_width = self.top.winfo_reqwidth()
        window_height = self.top.winfo_reqheight()
        print("Width", window_width, "Height", window_height)

        # Gets both half the screen width/height and window width/height
        position_right = int(self.top.winfo_screenwidth() / 2.3 - window_width / 2)
        position_down = int(self.top.winfo_screenheight() / 3 - window_height / 2)

        # Positions the window in the center of the page.
        self.top.geometry("+{}+{}".format(position_right, position_down))

    def fechar(self):
        self.top.destroy()

    def fechar_event(self, event):
        self.top.destroy()

    def inserir_texto(self, texto):
        self.entrada.set(texto)
        self.entry_entrada.icursor(0)
        self.entry_entrada.icursor(len(self.entrada.get()))


if __name__ == '__main__':
    app_main = Tk()
    DialogoEntrada(app_main)
    app_main.mainloop()
