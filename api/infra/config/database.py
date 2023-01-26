import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        global con
        con = mysql.connector.connect(host='localhost', database='projeto_email', user='root', password='')
        
    except Error as e:
        print("Erro de conexão")

def close():
    try:
        global con
        if con.is_connected():
            con.close()
            print("Conexão ao MySQL foi encerrada")
    except Error as e:
        print("Erro de conexão")

def buscar(chave, tabela, nomeColuna):
    try:
        conectar()
        buscar_sql = f'select * from {tabela} where {nomeColuna} = \'{chave}\'' #chave_toker #instituicao
        #print(buscar_sql)
        cursor = con.cursor()
        cursor.execute(buscar_sql)
        linhas = cursor.fetchall()

        for linha in linhas:
            #print("Seja bem-vindo: ", linha[0])
            return True
            break
        else:
            #print("Chave Inválida!")
            return False

        cursor.close()
    except Error as e:
        print("Erro ao acessar tabela MySQL: {}".format(e))
    finally:
        close()

def inserindoEmail(infEmail, tabela, infChave):
        try:
            conectar()
            inserir_email = f"""insert into {tabela} values
                                            ('{infEmail}', default, {infChave});
                                      """
            cursor = con.cursor()
            cursor.execute(inserir_email)
            con.commit()
            print(cursor.rowcount, "Registro inserido na tabela!")
            cursor.close()
        except Error as e:
            print("Erro ao inserir os dados na tabela MySQL: {}".format(e))
        finally:
            close()
            
#verificar esse codigo
def atualizaSitEmail(tabela ,situacao, email):
    try:
        conectar()
        altera_situacao = f"""update {tabela} set situacao = {situacao}  where email = '{email}';"""
        cursor = con.cursor()
        cursor.execute(altera_situacao)
        con.commit()
        print("situacao alterado com sucesso!")
        cursor.close()
    except Error as erro:
        print("Falha ao inserir dados no MySQL: {}".format(erro))
    finally:
        close()

def buscarsituacao(email, tabela, nomeColuna, situacao):
    try:
        conectar()
        buscar_sql = f'select * from {tabela} where {nomeColuna} = \'{email}\' and situacao = {situacao}' #chave_toker #instituicao
        #print(buscar_sql)
        cursor = con.cursor()
        cursor.execute(buscar_sql)
        linhas = cursor.fetchall()

        for linha in linhas:
            #print("Seja bem-vindo: ", linha[0])
            return True
            break
        else:
            #print("Chave Inválida!")
            return False

        cursor.close()
    except Error as e:
        print("Erro ao acessar tabela MySQL: {}".format(e))
    finally:
        close()
#print(buscar(789456123, "instituicao", "chave_toker"))
#inserindoEmail("joaocostacametá@gmail.com", 789456123)