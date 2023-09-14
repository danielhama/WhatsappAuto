import sqlite3
import datetime
import pandas as pd
from models.calculo import calcular_margem
from models.ferramentas import *
import logging


logging.basicConfig(filename='app.log', level=logging.INFO)


def conectar():
    """
    Função para conectar ao servidor
    """
    conn = sqlite3.connect(r"C:\Bezel\DataFile\BezelDataBase.db", detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.
                           PARSE_COLNAMES)

    conn.execute("""CREATE TABLE IF NOT EXISTS "Clientes" (
    "Id" INTEGER NOT NULL CONSTRAINT "PK_Clientes" PRIMARY KEY AUTOINCREMENT,
    "IsDeleted" INTEGER NOT NULL DEFAULT 0,
    "CPF" TEXT NULL,
    "Nome" TEXT NULL,
    "DataNascimento" TEXT NOT NULL,
    "Limite" INTEGER NOT NULL,
    "DataAtualizacao" TEXT NOT NULL
);""")

    conn.execute("""CREATE TABLE IF NOT EXISTS "Contratos" (
    "Id" INTEGER NOT NULL CONSTRAINT "PK_Contratos" PRIMARY KEY AUTOINCREMENT,
    "IsDeleted" INTEGER NOT NULL DEFAULT 0,
    "Numero" TEXT NOT NULL,
    "Emissao" TEXT NOT NULL,
    "Vencimento" TEXT NOT NULL,
    "Prazo" INTEGER NOT NULL,
    "ValorAvaliacao" TEXT NOT NULL,
    "ValorEmprestimo" TEXT NOT NULL,
    "DataInclusao" TEXT NULL,
    "Situacao" TEXT NULL,
    "CPF" TEXT NULL,
    "Modalidade" INTEGER NOT NULL,
    "QtdeRenovacoes" INTEGER NOT NULL,
    "Peso" TEXT NOT NULL,
    "QtdeParcelas" INTEGER NOT NULL,
    "DataAtualizacao" TEXT NOT NULL,
    "Ativo" INTEGER NOT NULL
);""")

    conn.execute("""CREATE TABLE IF NOT EXISTS "Telefones" (
    "Id" INTEGER NOT NULL CONSTRAINT "PK_Telefones" PRIMARY KEY AUTOINCREMENT,
    "ClienteID" INTEGER NOT NULL,
    "Numero" TEXT NULL,
    "whatsapp" INTEGER NOT NULL DEFAULT 1,
    "DDD" TEXT NULL,
    CONSTRAINT "FK_Telefones_Clientes_ClienteID" FOREIGN KEY ("ClienteID") REFERENCES "Clientes" ("Id") ON DELETE CASCADE);""")

    conn.execute("""CREATE TABLE IF NOT EXISTS "envio" (
            "id"	INTEGER NOT NULL,
            "id_cliente"	TEXT NOT NULL UNIQUE,
            PRIMARY KEY("id" AUTOINCREMENT),
            FOREIGN KEY("id_cliente") REFERENCES "Clientes"("Id"));"""
                 )

    return conn


def desconectar(conn):
    """
    FunÃ§Ã£o para desconectar do servidor.
    """
    conn.close()

# Lista Envio


def inserir_id_envio(id) -> bool:
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO envio (id_cliente) VALUES ('{id}')")
        conn.commit()
        desconectar(conn)
        return True

    except sqlite3.IntegrityError as e:
        desconectar(conn)
        return False

def criar_lista_envio():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT Clientes.id FROM Clientes")
    ids = cursor.fetchall()
    for id in ids:
        try:
            inserir_id_envio(id[0])
        except sqlite3.IntegrityError as e:
            print(e)
    desconectar(conn)

def deletar_enviado(id):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM envio WHERE id_cliente = {id}")
        conn.commit()
    except:
        pass
    conn.close()


def deletar_lista():
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM envio")
        conn.commit()
    except:
        pass
    conn.close()


# INSERIR

def inserir_cliente(nome, cpf, limite):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO Clientes (Nome, CPF, Limite) VALUES ('{nome}', '{cpf}', {limite})")
        conn.commit()
    except:
        pass
    conn.close()

def inserir_telefone(DDD, telefone, id):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO Telefones (numero, whatsapp, ClienteID, DDD) VALUES ('{telefone}', 1, {id}, {DDD})")
        conn.commit()
    except:
        pass
    desconectar(conn)

def inserir_sem_whats(telefone):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(f"UPDATE Telefones SET whatsapp=0 WHERE numero={telefone}")
        conn.commit()
    except Exception as e:
        pass
    desconectar(conn)


def inserir_contrato(numero, emissao, vencimento, valor_emprestimo, valor_avaliacao, situacao, prazo, cpf, data, modalidade):
    conn = conectar()
    cursor = conn.cursor()
    hoje = datetime.datetime.today()
    # data = datetime.datetime.strptime(data.split(' ')[0], '%d/%m/%Y')
    valor_avaliacao = convert_to_float(valor_avaliacao)
    valor_emprestimo = convert_to_float(valor_emprestimo)
    try:
        cursor.execute(f"INSERT INTO Contratos (numero, Emissao, Vencimento, ValorEmprestimo, ValorAvaliacao, situacao, prazo, cpf, DataAtualizacao, Modalidade, QtdeRenovacoes, QtdeRenovacoes, Ativo, Peso, QtdeParcelas, DataInclusao) VALUES ('{numero}', '{emissao}', '{vencimento}', {valor_emprestimo}, {valor_avaliacao}, '{situacao}', {prazo}, '{cpf}', '{data}', {modalidade}, 0, 0, 1, '0.0', 0, '{hoje}')")
        conn.commit()
        if cursor.rowcount == 1:
            print("Contrato incluído com sucesso")
    except Exception as e:
        print(e)
        atualizado = datetime.datetime.strptime(pesquisa_data_atualizacao(numero).split(" ")[0], '%Y-%m-%d')
        if atualizado < data:

            cursor.execute(f"UPDATE Contratos SET vencimento='{vencimento}', ValorEmprestimo={valor_emprestimo}, ValorAvaliacao={valor_avaliacao}, DataAtualizacao='{data}', situacao='{situacao}' WHERE numero='{numero}'")
            conn.commit()
            if cursor.rowcount == 1:
                print('Contrato Atualizado com Sucesso!')
            else:
                print('Erro na atualização')
        else:
            print('Data do relatório mais antiga que a base de dados')
    conn.close()


# LISTAR

def listar_Clientes_telefone_envio():
    """
    Função para listar os Telefones
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT cli.nome, cli.cpf, Telefones.DDD || Telefones.numero, envio.id_cliente, Contratos.vencimento FROM "
                   "Telefones, Clientes as cli, envio, Contratos WHERE envio.id_cliente = cli.id AND "
                   "Telefones.ClienteId = cli.id and Telefones.whatsapp = 1 AND Contratos.Situacao != 'LIQUIDADO' GROUP BY Telefones.DDD || Telefones.numero")
    Clientes = cursor.fetchall()
    lista_Clientes = []
    if len(Clientes) > 0:
        for cliente in Clientes:
            cliente = {'Nome': cliente[0], 'CPF': cliente[1], 'Telefones': cliente[2], 'Vencimento':cliente[4]}
            lista_Clientes.append(cliente)
    else:
        print('Não existem Clientes cadastrados.')
    desconectar(conn)
    return lista_Clientes


def listar():
    """
    Função para listar os Clientes
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT cli.Nome, cli.CPF FROM Clientes as cli')
    Clientes = cursor.fetchall()
    lista_Clientes = []
    if len(Clientes) > 0:
        for cliente in Clientes:
            cliente = {'Nome': cliente[0], 'CPF': cliente[1]}
            lista_Clientes.append(cliente)
    else:
        print('Não existem Clientes cadastrados.')
    desconectar(conn)
    return lista_Clientes


def listar_Clientes_telefone():
    """
    Função para listar os Telefones
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT cli.nome, cli.cpf, Telefones.DDD || Telefones.numero, Contratos.CPF, Contratos.vencimento FROM Telefones, Clientes as cli, Contratos WHERE cli.CPF = Contratos.CPF and Telefones.ClienteID = cli.Id and Telefones.whatsapp = 1 GROUP BY Telefones.Numero')  # GROUP BY Telefones.numero')
    Clientes = cursor.fetchall()
    lista_Clientes = []
    if len(Clientes) > 0:
        for cliente in Clientes:
            cliente = {'Nome': cliente[0], 'CPF': cliente[1], 'Telefones':cliente[2], 'Vencimento':cliente[4]}
            lista_Clientes.append(cliente)
    else:
        print('Não existem Clientes cadastrados.')
    desconectar(conn)
    return lista_Clientes



def listar_Telefones_por_cpf(cpf):
    """
        Função para listar os Telefones
        """
    conn = conectar()
    cursor = conn.cursor()
    id = pesquisa_id(cpf)
    cursor.execute(
        f'SELECT Telefones.DDD || Telefones.numero FROM Telefones WHERE Telefones.ClienteID = {id}')
    Telefones = cursor.fetchall()
    lista_Telefones = []
    if len(Telefones) > 0:
        for telefone in Telefones:
            lista_Telefones.append(telefone[0])
    else:
        print('Não existem Clientes cadastrados.')
    desconectar(conn)
    return lista_Telefones

def listar_nome(cpf):
    """
        Função para listar os nomes
        """
    conn = conectar()
    cursor = conn.cursor()
    id = pesquisa_id(cpf)
    cursor.execute(
        f'SELECT Clientes.nome FROM Clientes WHERE Clientes.id = {id}')
    nomes = cursor.fetchall()
    lista_nomes = []
    if len(nomes) > 0:
        for nome in nomes:
            lista_nomes.append(nome[0])
    else:
        print('Não existem Clientes cadastrados.')
    desconectar(conn)
    return lista_nomes

def listar_Contratos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Contratos')
    Contratos = cursor.fetchall()
    lista_Contratos = []
    for contrato in Contratos:
        lista_Contratos.append(contrato[1])
    desconectar(conn)
    return lista_Contratos

def listar_Contratos_vencidos():
    """
    Função para listar os Contratos vencidos
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT cli.Nome,  Contratos.Vencimento, cli.id FROM Clientes as cli, Contratos WHERE Contratos.CPF = cli.CPF AND Contratos.Vencimento < date('now','-2 day') AND Contratos.Situacao NOT LIKE '%LIQUIDADO%'  GROUP BY cli.Id")
    Clientes = cursor.fetchall()
    lista_Clientes = []
    if len(Clientes) > 0:
        for cliente in Clientes:
            # cliente = {'Nome': cliente[0], 'CPF': cliente[1], 'Telefones': cliente[2], 'Vencimento': cliente[4]}
            # lista_Clientes.append(cliente)
            inserir_id_envio(cliente[2])
    else:
        print('Não existem Clientes cadastrados.')
    desconectar(conn)
    # return lista_Clientes

#
def listar_Contratos_licitacao():
    """
    Função para listar os Contratos vencidos
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT cli.nome, cli.cpf, Telefones.DDD || Telefones.numero,  Contratos.vencimento FROM Telefones, Clientes as cli, Contratos WHERE Contratos.situacao LIKE '%LICI%' AND Telefones.whatsapp == 1 AND Telefones.ClienteID = cli.id AND Contratos.CPF = cli.CPF GROUP BY Telefones.Numero")
    Clientes = cursor.fetchall()
    lista_Clientes = []
    if len(Clientes) > 0:
        for cliente in Clientes:
            inserir_id_envio(str(cliente[3]))
            cliente = {'Nome': cliente[0], 'CPF': cliente[1], 'Telefones': cliente[2], 'Vencimento': cliente[3]}
            lista_Clientes.append(cliente)
    else:
        print('Não existem Clientes cadastrados.')
    desconectar(conn)
    return lista_Clientes


def lista_Telefones(whatsapp):
    """
    Função para listar os Telefones
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM 'Telefones' WHERE Telefones.whatsapp = {whatsapp} ORDER BY ID DESC")
    Telefones = cursor.fetchall()
    lista_Telefones = []
    if len(Telefones) > 0:
        for telefone in Telefones:
            lista_Telefones.append(telefone[3]+telefone[2])
    else:
        print('Não existem números cadastrados.')
    desconectar(conn)
    return lista_Telefones

def filtra_calculo_margem():
    """
            Função para listar Clientes com margem acima de R$ 500,00
            """
    # data30, data60, data90, data120 = calcular_data()

    try:
        conn = conectar()
        cursor = conn.cursor()
        Clientes1 = []
        cursor.execute(
            f'SELECT Clientes.id, Clientes.cpf, Clientes.nome, Clientes.limite FROM Clientes')
        Clientes = cursor.fetchall()

        for cliente in Clientes:
            id = cliente[0]
            d30 = 0
            d60 = 0
            d90 = 0
            d120 = 0
            total_emprestimo = 0
            cursor.execute(
                f"select SUM(Contratos.ValorAvaliacao) as total, Clientes.limite from Contratos, Clientes where Contratos.CPF = Clientes.CPF AND Clientes.id = {id} AND Contratos.situacao NOT LIKE  '%LIQUIDADO%'")
            cliente_limite = cursor.fetchall()
            total = cliente_limite[0][0]
            limite = cliente_limite[0][1]
            cursor.execute(
                f"select Contratos.numero, Contratos.vencimento, Contratos.ValorAvaliacao, Contratos.ValorEmprestimo, Contratos.prazo, Contratos.CPF, Clientes.CPF, Clientes.Id from Contratos, Clientes where Contratos.CPF = Clientes.CPF AND Clientes.Id = {id} AND Contratos.situacao NOT LIKE  '%LIQUIDADO%'")
            Contratos = cursor.fetchall()
            if len(Contratos) > 0:
                for contrato in Contratos:
                    vencimento = datetime.datetime.strptime(contrato[1].split(' ')[0], '%Y-%m-%d')
                    prazo = contrato[4]
                    avaliacao = float(contrato[2])
                    emprestimo = float(contrato[3])
                    # limite = contrato[5]
                    if limite == 100:
                        total_emprestimo += avaliacao
                    else:
                        total_emprestimo += avaliacao * .85
                    if total_emprestimo > emprestimo:
                        d30_t, d60_t, d90_t, d120_t = calcular_margem(avaliacao, emprestimo,
                                                                      vencimento, prazo, limite, total)
                        d30 += d30_t
                        d60 += d60_t
                        d90 += d90_t
                        d120 += d120_t
                if d30 < -500:
                    inserir_id_envio(id)
                    Telefones = listar_Telefones_por_cpf(cliente[1])
                    # sem_whats = lista_Telefones("0")
                    if len(Telefones) >= 1:
                        for telefone in Telefones:
                            telefone = telefone[0:4]+telefone[5:13]
                            cliente_1 = {'Nome': cliente[2], 'CPF': cliente[1], 'Telefones': telefone,
                                       'Vencimento': vencimento, 'Margem': d30}
                            Clientes1.append(cliente_1)
                        # telefone = telefone[0:4]+telefone[5:13]
                        # cliente_1 = {'Nome': cliente[2], 'CPF': cliente[1], 'Telefones': telefone,
                        #            'Vencimento': vencimento, 'Margem': d30}
                        # Clientes1.append(cliente_1)

        desconectar(conn)
        Clientes = pd.DataFrame(Clientes1)
        Clientes.drop_duplicates(subset='Telefones', inplace=True)
        Clientes1 = Clientes.to_dict('records')

        return Clientes1

    except Exception as e:
        print(e)
        pass

def consulta_prazo(contrato):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT prazo FROM Contratos WHERE Contratos.numero = '{contrato}'")
        prazo = cursor.fetchall()
        desconectar(conn)
        return prazo[0][0]
    except:
        desconectar(conn)


# DELETAR
def deletar_contrato(numero):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM 'Contratos' WHERE numero='{numero}'")
        conn.commit()
    except:
        pass
    conn.close()

def deletar_contrato_desatualizado(data):
    conn = conectar()
    cursor = conn.cursor()
    try:
        data = datetime.datetime.strftime(datetime.datetime.strptime(data.split()[0], '%d/%m/%Y'), '%Y-%m-%d %H:%M:%S')
        cursor.execute(f"DELETE FROM 'Contratos' WHERE Contratos.DataAtualizacao!='{data}'")
        conn.commit()
        print("Excluindo Contratos liquidados")
    except:
        pass
    conn.close()
def deletar_telefone(telefone):
    conn = conectar()
    cursor = conn.cursor()
    if len(str(telefone)) > 9:
        telefone = str(telefone)[2::]
    try:
        cursor.execute(f"DELETE FROM 'Telefones' WHERE numero={telefone}")
        conn.commit()
    except:
        pass
    conn.close()

def deletar_cliente(cpf):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM 'Clientes' WHERE cpf='{cpf}'")
        conn.commit()
    except:
        pass
    conn.close()

def deletar_sem_whats(telefone):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(f"UPDATE Telefones set whatsapp={1} WHERE numero={telefone}")
        conn.commit()
    except:
        pass
    conn.close()


# ATUALIZAR
def atualizar_contrato(numero, vencimento, valor_avaliacao, valor_emprestimo, prazo, data):
    conn = conectar()
    cursor = conn.cursor()
    data = datetime.datetime.strptime(data, '%d/%m/%Y')
    # hoje = datetime.datetime.today()
    # hoje = hoje.strftime('%d/%m/%Y')
    valor_avaliacao = convert_to_float(valor_avaliacao)
    valor_emprestimo = convert_to_float(valor_emprestimo)
    atualizado = pesquisa_data_atualizacao(numero)
    if atualizado != None:
        atualizado = datetime.datetime.strptime(atualizado.split(' ')[0], '%Y-%m-%d')
    else:
        print("Novo contrato faça a inclusão pelo relatório da bezel")
        return
    if atualizado <= data:
        cursor.execute(
                f"UPDATE Contratos SET vencimento='{vencimento}', ValorEmprestimo={valor_emprestimo}, ValorAvaliacao={valor_avaliacao}, DataAtualizacao='{data}', prazo={prazo} WHERE numero='{numero}'")
        conn.commit()
    if cursor.rowcount == 1:
        print('Contrato atualizado com sucesso.')
    else:
        print('Erro ao atualizar contrato.')


# PESQUISA ID

def pesquisa_id(cpf):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(f"SELECT id FROM Clientes WHERE cpf='{cpf}'")
    id = cursor.fetchone()

    return id[0]

def pesquisa_id_por_telefone(numero):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(f"SELECT t.DDD || t.numero as telefone, t.ClienteID, c.id, c.cpf FROM Telefones as t, Clientes as c where c.id = t.ClienteID and telefone = {numero}")
    id = cursor.fetchone()
    if id[0] is not None:
        return id[0]

def pesquisa_data_atualizacao(numero_contrato):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"SELECT c.DataAtualizacao FROM Contratos as c WHERE c.numero='{numero_contrato}'")
    data = cursor.fetchone()
    conn.close()
    if data == None:
        print(f'Contrato novo {numero_contrato} efetuar a inclusão pelo relatório da bezel')
        return None
    return data[0]



# OUTROS


def limpa_contratos():
    conn = conectar()
    cursor = conn.cursor()
    date = datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
    cursor.execute(f"DELETE FROM Contratos WHERE DataAtualizacao < '{date}'")
    conn.commit()
    conn.close()



