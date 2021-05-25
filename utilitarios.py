class StringUtils:

    @staticmethod
    def is_empty(string):
        if string is None:
            return True
        return len(string.strip()) == 0

    @staticmethod
    def is_equal(str1, str2):
        if not str1 or not str2:
            return False
        return str1.strip() == str2.strip()

    @staticmethod
    def to_upper_case(event, var):
        var.set(var.get().upper())

    @staticmethod
    def converter_texto_para_lista_itens_remessa(texto):
        pass

    @staticmethod
    def converter_lista_itens_remessa_para_texto(lista_itens):
        pass


class NumberUtils:

    @staticmethod
    def formatar_numero(numero):
        return "{:.3f}".format(numero).replace(".", ",")

    @staticmethod
    def str_para_float(string, formatar=False):
        numero = float(string.replace(",", "."))
        if formatar:
            return NumberUtils.formatar_numero(numero)
        return numero

    @staticmethod
    def eh_decimal(texto):
        if not texto.strip():
            return True
        else:
            try:
                float(texto.replace(",", "."))
                return True
            except ValueError:
                return False

    @staticmethod
    def eh_inteiro(texto):
        if not texto.strip():
            return True
        else:
            try:
                int(texto)
                return True
            except ValueError:
                return False

    @staticmethod
    def eh_lacre(texto):
        if texto == " ":
            return False
        if NumberUtils.eh_inteiro(texto):
            return len(texto) <= 7
        return False
