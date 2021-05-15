from collections import defaultdict


class Kleuder:

    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        self._nome = valor

    def __eq__(self, other):
        if isinstance(other, Kleuder):
            return self.nome == other.nome and self.idade == other.idade
        return False

    def __str__(self):
        return "Nome: {} Idade: {}".format(self.nome, self.idade)


kl = []
k1 = Kleuder("Kleuder", 30)
k2 = Kleuder("Kleuder", 31)
k3 = Kleuder("Kleuder Lima", 31)
k4 = Kleuder("Kleuder Lima", 31)
k5 = Kleuder("Kleuder Souza", 31)
k6 = Kleuder("Kleuder Souza", 31)
k7 = Kleuder("Thomas", 31)
k8 = Kleuder("Thomas", 31)

kl.append(k1)
kl.append(k2)
kl.append(k3)
kl.append(k4)
kl.append(k5)
kl.append(k6)
kl.append(k7)
kl.append(k8)

dic = {}

for k in kl:
    dic[k.nome] = []

for k in kl:
    dic[k.nome].append(k)

for key in dic:
    for kleuder in dic[key]:
        print(kleuder)