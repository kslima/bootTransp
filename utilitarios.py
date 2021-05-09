class StringUtils:

    @staticmethod
    def is_empty(string):
        if string is None:
            return True
        return len(string.strip()) == 0


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
        if NumberUtils.eh_inteiro(texto):
            return len(texto) <= 7
        return False
