from tkinter import *
import re

from unidecode import unidecode

import service
from model import Placa


class AutocompleteEntry(Entry):
    def __init__(self, *args, **kwargs):

        # Listbox length
        if 'listboxLength' in kwargs:
            self.listboxLength = kwargs['listboxLength']
            del kwargs['listboxLength']
        else:
            self.listboxLength = 8

        # Custom matches function
        if 'matchesFunction' in kwargs:
            self.matchesFunction = kwargs['matchesFunction']
            del kwargs['matchesFunction']
        else:
            def matches(pesquisa, item_lista_placas):
                pattern = re.compile('.*' + re.escape(AutocompleteEntry.remover_caracteres(pesquisa)) + '.*',
                                     re.IGNORECASE)
                return re.match(pattern, AutocompleteEntry.remover_caracteres(str(item_lista_placas)))

            self.matchesFunction = matches

        Entry.__init__(self, *args, **kwargs)
        self.focus()

        self.autocompleteList = service.listar_municipios_brasileiros()
        self.listbox = None

        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        # self.bind("<Right>", self.selection)
        self.bind("<Up>", self.move_up)
        self.bind("<Down>", self.move_down)

        self.listboxUp = False

    def changed(self, name, index, mode):
        if self.var.get() == '':
            if self.listboxUp:
                self.listbox.destroy()
                self.listboxUp = False
        else:
            words = self.comparison()
            if words:
                if not self.listboxUp:
                    self.listbox = Listbox(self.master, width=self["width"], height=self.listboxLength)
                    self.listbox.bind('<<ListboxSelect>>', self.on_selection)
                    self.listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                    self.listboxUp = True

                self.listbox.delete(0, END)
                for w in words:
                    self.listbox.insert(END, w)
            else:
                if self.listboxUp:
                    self.listbox.destroy()
                    self.listboxUp = False

    def on_selection(self, event):
        if self.listboxUp:
            texto_selecionado = self.listbox.get(self.listbox.curselection())
            for municipio in self.autocompleteList:
                if str(municipio) == texto_selecionado:
                    self.var.set("{} {}".format(municipio.uf.upper(), municipio.codigo_municipio))
            self.listbox.destroy()
            self.listboxUp = False
            self.icursor(END)

    def move_up(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]

            if index != '0':
                self.listbox.selection_clear(first=index)
                index = str(int(index) - 1)

                self.listbox.see(index)  # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

    def move_down(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]

            if index != END:
                self.listbox.selection_clear(first=index)
                index = str(int(index) + 1)

                self.listbox.see(index)  # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

    def comparison(self):
        return [w for w in self.autocompleteList if self.matchesFunction(self.var.get(), w)]

    @staticmethod
    def remover_caracteres(texto):
        novo_texto = ''.join(e for e in texto if e.isalnum()).lower()
        return unidecode(novo_texto)


if __name__ == '__main__':
    municipios = service.listar_municipios_brasileiros()

    root = Tk()
    entry = AutocompleteEntry(municipios, root, listboxLength=6, width=32)
    entry.grid(row=0, column=0)
    Button(text='Python').grid(column=0)
    Button(text='Tkinter').grid(column=0)
    Button(text='Regular Expressions').grid(column=0)
    Button(text='Fixed bugs').grid(column=0)
    Button(text='New features').grid(column=0)
    Button(text='Check code comments').grid(column=0)
    root.mainloop()
