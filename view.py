import tkinter
from tkinter.ttk import *
import model


class ShippingView(Frame):

    def __init__(self):
        super().__init__()

        self.batch = tkinter.StringVar()
        self.amount = tkinter.StringVar()
        self.shipping = model.Shipping()
        self.storage_area = tkinter.StringVar()

        # exibindo em looping
        self.init_ui()

    def init_ui(self):
        self.master.title("Criar Remessa")
        self.master.geometry('400x130')

        f = Frame(self)
        f.pack()

        Button(f, text="Inserir", command=self.set_shipping).place(x=5, y=50)

        # deposito
        Label(f, text="Deposito: ", font=(None, 8, 'normal')).place(x=5, y=5)

        Combobox(f, textvariable=self.storage_area).place(x=5, y=25, width=80)

        # quantidade
        Label(f, text="Quantidade: ", font=(None, 8, 'normal')).place(x=90, y=5)

        Entry(f, textvariable=self.amount).place(x=90, y=25, width=100)

        # lote
        Label(f, text="Lote: ", font=(None, 8, 'normal')).place(x=195, y=5)

        Combobox(f, textvariable=self.batch).place(x=195, y=25, width=160)

    def set_shipping(self):
        self.shipping.batch = self.batch.get()
        self.shipping.storage_area = self.storage_area.get()
        self.shipping.amount = self.amount.get()
        print(f"Deposito: {self.shipping.batch} Lote: {self.shipping.storage_area} Quantidade: {self.shipping.amount}")
        self.quit()

        """
                # ordem
               Label(self.shipping_frame, text="Ordem: ", font=(None, 8, 'normal')).grid(column=2, row=0, sticky=tkinter.W)
               Entry(self.shipping_frame, textvariable=self.ov, width=40).grid(column=2, row=1, sticky=tkinter.W, padx=2,
                                                                               pady=2, columnspan=3)

               # quantidade
               Label(self.shipping_frame, text="Quantidade: ", font=(None, 8, 'normal')).grid(column=2, row=2,
                                                                                              sticky=tkinter.W)
               Entry(self.shipping_frame, textvariable=self.amount, width=40).grid(column=2, row=3, sticky=tkinter.W, padx=2,
                                                                                   pady=2, columnspan=3)

               self.tranport_cod = tkinter.StringVar()
               self.transport_cnpj = tkinter.StringVar()
               self.type = tkinter.StringVar()
               self.proc = tkinter.StringVar()
               self.order = tkinter.StringVar()
               self.horse = tkinter.StringVar()
               self.cart_1 = tkinter.StringVar()
               self.cart_2 = tkinter.StringVar()
               self.cart_3 = tkinter.StringVar()
               # frame transporte
               self.transport_frame = LabelFrame(app_main, text="Transporte")
               self.transport_frame.grid(column=0, row=4, padx=2, pady=10)

               # transportadora codigo
               Label(self.transport_frame, text="Código", font=(None, 8, 'normal')).grid(column=0, row=0, sticky=tkinter.W)
               Entry(self.transport_frame, textvariable=self.tranport_cod, width=30).grid(column=0, row=1, sticky=tkinter.W, padx=2,
                                                                                pady=2, columnspan=2)
               # transportadora cnpj
               Label(self.transport_frame, text="CNPJ", font=(None, 8, 'normal')).grid(column=2, row=0, sticky=tkinter.W)
               Entry(self.transport_frame, textvariable=self.transport_cnpj, width=30).grid(column=2, row=1, sticky=tkinter.W, padx=2,
                                                                                  pady=2, columnspan=2)
               # tipo veiculo
               Label(self.transport_frame, text="Tipo", font=(None, 8, 'normal')).grid(column=0, row=2, sticky=tkinter.W)
               Entry(self.transport_frame, textvariable=self.type, width=13).grid(column=0, row=3, sticky=tkinter.W, padx=1,
                                                                                  pady=2)
               # proced especial
               Label(self.transport_frame, text="Proc.", font=(None, 8, 'normal')).grid(column=1, row=2, sticky=tkinter.W)
               Entry(self.transport_frame, textvariable=self.type, width=13).grid(column=1, row=3, sticky=tkinter.W, padx=1,
                                                                                  pady=2)
               # proced especial
               Label(self.transport_frame, text="Pedido", font=(None, 8, 'normal')).grid(column=2, row=2, sticky=tkinter.W)
               Entry(self.transport_frame, textvariable=self.order, width=30).grid(column=2, row=3, sticky=tkinter.W, padx=2,
                                                                                   pady=2, columnspan=2)
               # placa cavalo
               Label(self.transport_frame, text="Cavalo", font=(None, 8, 'normal')).grid(column=0, row=4, sticky=tkinter.W)
               Entry(self.transport_frame, textvariable=self.transport_cnpj, width=13).grid(column=0, row=5, sticky=tkinter.W, padx=2,
                                                                                  pady=2)
               # placa carreta 1
               Label(self.transport_frame, text="Carreta 1", font=(None, 8, 'normal')).grid(column=1, row=4, sticky=tkinter.W)
               Entry(self.transport_frame, textvariable=self.type, width=13).grid(column=1, row=5, sticky=tkinter.W, padx=2,
                                                                                  pady=2)
               # placa carreta 2
               Label(self.transport_frame, text="Carreta 2", font=(None, 8, 'normal')).grid(column=2, row=4, sticky=tkinter.W)
               Entry(self.transport_frame, textvariable=self.type, width=15).grid(column=2, row=5, sticky=tkinter.W, padx=2,
                                                                                  pady=2)
               # placa carreta 3
               Label(self.transport_frame, text="Carreta 3", font=(None, 8, 'normal')).grid(column=3, row=4, sticky=tkinter.W)
               Entry(self.transport_frame, textvariable=self.order, width=15).grid(column=3, row=5, sticky=tkinter.W, padx=2,
                                                                                   pady=2)
               """
