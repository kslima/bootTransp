import sqlite3

connection = sqlite3.connect("C:\\Users\\kslima\\Desktop\\sqlite\\banco.db")
cursor = connection.cursor()

# cursor.execute("INSERT INTO motorista VALUES ('Kleuder Lima', '07712410461', '035451245', 'MG18475387')")
# rows = cursor.execute("SELECT rowid, nome, cpf, cnh, rg FROM motorista").fetchall()
# connection.commit()
'''
   connection = sqlite3.connect("C:\\Users\\kslima\\Desktop\\sqlite\\banco.db")
   cursor = connection.cursor()
   for m in municipios:
       m.municipio = unidecode(m.municipio).replace("'", " ")
       cursor.execute("INSERT INTO municipio VALUES ('{}', '{}', '{}')".format(m.municipio,
                                                                               m.codigo_municipio,
                                                                               m.uf))
   connection.commit()
   '''


def criar_tabela_municipio():
    cursor.execute("CREATE TABLE municipio (nome TEXT, codigo_municipio TEXT, uf TEXT)")


def criar_tabela_motorista():
    cursor.execute("CREATE TABLE motorista (nome TEXT, cpf TEXT, cnh TEXT, rg TEXT)")


def criar_tabela_produto():
    cursor.execute("CREATE TABLE produto (codigo TEXT, nome TEXT, deposito TEXT, lote TEXT,"
                   " inspecao_veiculo INT, inspecao_produto INT, remover_a INT)")


criar_tabela_produto()