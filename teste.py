import re

SUCCSESS_MESSAGE = "Lote de controle 1014 890000150159 foi criado"
s = "".join(re.findall("\\d{12}", SUCCSESS_MESSAGE)).strip()

print(s)
