import sqlite3
import datetime
from os import path
import pandas as pd
from models.calculo import calcular_juros, calcular_data, calcular_margem
from models.ferramentas import *
import logging
logging.basicConfig(filename='app.log', level=logging.INFO)

def conectar():
    """
    Função para conectar ao servidor
    """
    conn = sqlite3.connect(path.join(path.expanduser('~'), 'whatsrelatorios\\whats.db'), detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)


    conn.execute("""CREATE TABLE IF NOT EXISTS "clientes" (
        "id"	INTEGER NOT NULL,
        "nome"	TEXT NOT NULL,
        "cpf"	TEXT NOT NULL UNIQUE,
        "limite" INTEGER NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT));""")

    conn.execute("""CREATE TABLE IF NOT EXISTS  "contratos" (
        "id"	INTEGER NOT NULL,
        "numero"	TEXT NOT NULL UNIQUE,
        "vencimento"	TEXT NOT NULL,
        "valor_emprestimo"	REAL NOT NULL,
        "valor_avaliacao"	REAL NOT NULL,
        "data_atualizacao"	TEXT NOT NULL,
        "situacao" TEXT NOT NULL,
        "prazo"	INTEGER NOT NULL,    
        "id_cliente"	INTEGER NOT NULL,
        FOREIGN KEY("id_cliente") REFERENCES "clientes"("id"),
        PRIMARY KEY("id" AUTOINCREMENT));""")

    conn.execute("""
        CREATE TABLE IF NOT EXISTS "telefones" (
        "id"	INTEGER NOT NULL,
        "numero"	INTEGER NOT NULL UNIQUE,
        "whatsapp" INTEGER NOT NULL,
        "id_cliente"	TEXT NOT NULL,
        PRIMARY KEY("id" AUTOINCREMENT),
        FOREIGN KEY("id_cliente") REFERENCES "clientes"("id"));"""
                 )

    conn.execute("""CREATE TABLE IF NOT EXISTS "envio" (
            "id"	INTEGER NOT NULL,
            "id_cliente"	TEXT NOT NULL,
            PRIMARY KEY("id" AUTOINCREMENT),
            FOREIGN KEY("id_cliente") REFERENCES "clientes"("id"));"""
                 )

    return conn


def desconectar(conn):
    """
    FunÃ§Ã£o para desconectar do servidor.
    """
    conn.close()

# Lista Envio

def inserir_id_envio(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO envio (id_cliente) VALUES ('{id}')")
    conn.commit()

    desconectar(conn)
def criar_lista_envio():
    conn =conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT clientes.id FROM clientes")
    ids = cursor.fetchall()
    for id in ids:
        inserir_id_envio(id[0])
    desconectar(conn)

def deletar_enviado(id):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM 'envio' WHERE id_cliente = {id}")
        conn.commit()
    except:
        pass
    conn.close()


def deletar_lista():
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM 'envio'")
        conn.commit()
    except:
        pass
    conn.close()


# INSERIR

def inserir_cliente(nome, cpf, limite):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO clientes (nome, cpf, limite) VALUES ('{nome}', '{cpf}', {limite})")
        conn.commit()
    except:
        pass
    conn.close()

def inserir_telefone(telefone, id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(f"INSERT INTO telefones (numero, whatsapp, id_cliente) VALUES ('{telefone}', 1, {id})")
    conn.commit()

    desconectar(conn)

def inserir_sem_whats(telefone):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(f"UPDATE telefones SET whatsapp=0 WHERE numero={telefone}")
        conn.commit()
    except Exception as e:
        pass
    desconectar(conn)


def inserir_contrato(numero, vencimento, valor_emprestimo, valor_avaliacao, situacao, prazo, id_cliente, data):
    conn = conectar()
    cursor = conn.cursor()
    hoje = datetime.datetime.today()
    data = datetime.datetime.strptime(data.split(' ')[0], '%d/%m/%Y')
    valor_avaliacao = convert_to_float(valor_avaliacao)
    valor_emprestimo = convert_to_float(valor_emprestimo)
    try:
        cursor.execute(f"INSERT INTO contratos (numero, vencimento, valor_emprestimo, valor_avaliacao, situacao, prazo, id_cliente, data_atualizacao) VALUES ('{numero}', '{vencimento}', {valor_emprestimo}, {valor_avaliacao}, '{situacao}', {prazo}, {id_cliente}, '{data}')")
        conn.commit()
        if cursor.rowcount == 1:
            print("Contrato incluído com sucesso")
    except Exception as e:
        atualizado = datetime.datetime.strptime(pesquisa_data_atualizacao(numero).split(" ")[0], '%Y-%m-%d')
        if atualizado < data:

            cursor.execute(f"UPDATE contratos SET vencimento='{vencimento}', valor_emprestimo={valor_emprestimo}, valor_avaliacao={valor_avaliacao}, data_atualizacao='{data}', situacao='{situacao}' WHERE numero='{numero}'")
            conn.commit()
            if cursor.rowcount == 1:
                print('Contrato Atualizado com Sucesso!')
            else:
                print('Erro na atualização')
        else:
            print('Data do relatório mais antiga que a base de dados')
    conn.close()


# LISTAR

def listar_clientes_telefone_envio():
    """
    Função para listar os telefones
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT cli.nome, cli.cpf, telefones.numero, envio.id_cliente, contratos.vencimento FROM telefones, clientes as cli, envio, contratos WHERE envio.id_cliente = cli.id AND telefones.id_cliente = cli.id and telefones.whatsapp = 1 AND contratos.id_cliente =envio.id_cliente GROUP BY telefones.numero')
    clientes = cursor.fetchall()
    lista_clientes = []
    if len(clientes) > 0:
        for cliente in clientes:
            cliente = {'Nome': cliente[0], 'CPF': cliente[1], 'Telefones':cliente[2], 'Vencimento':cliente[4]}
            lista_clientes.append(cliente)
    else:
        print('Não existem clientes cadastrados.')
    desconectar(conn)
    return lista_clientes

def listar():
    """
    Função para listar os clientes
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT cli.nome, cli.cpf FROM clientes as cli')
    clientes = cursor.fetchall()
    lista_clientes = []
    if len(clientes) > 0:
        for cliente in clientes:
            cliente = {'Nome': cliente[0], 'CPF': cliente[1]}
            lista_clientes.append(cliente)
    else:
        print('Não existem clientes cadastrados.')
    desconectar(conn)
    return lista_clientes


def listar_clientes_telefone():
    """
    Função para listar os telefones
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT cli.nome, cli.cpf, telefones.numero, contratos.id_cliente, contratos.vencimento FROM telefones, clientes as cli, contratos WHERE cli.id = contratos.id_cliente and telefones.id_cliente = cli.id and telefones.whatsapp = 1 GROUP BY telefones.numero')
    clientes = cursor.fetchall()
    lista_clientes = []
    if len(clientes) > 0:
        for cliente in clientes:
            cliente = {'Nome': cliente[0], 'CPF': cliente[1], 'Telefones':cliente[2], 'Vencimento':cliente[4]}
            lista_clientes.append(cliente)
    else:
        print('Não existem clientes cadastrados.')
    desconectar(conn)
    return lista_clientes


def listar_telefones_por_cpf(cpf):
    """
        Função para listar os telefones
        """
    conn = conectar()
    cursor = conn.cursor()
    id = pesquisa_id(cpf)
    cursor.execute(
        f'SELECT telefones.numero, clientes.id FROM telefones, clientes WHERE telefones.id_cliente = clientes.id AND id_cliente = {id}')
    telefones = cursor.fetchall()
    lista_telefones = []
    if len(telefones) > 0:
        for telefone in telefones:
            lista_telefones.append(telefone[0])
    else:
        print('Não existem clientes cadastrados.')
    desconectar(conn)
    return lista_telefones

def listar_nome(cpf):
    """
        Função para listar os nomes
        """
    conn = conectar()
    cursor = conn.cursor()
    id = pesquisa_id(cpf)
    cursor.execute(
        f'SELECT clientes.nome FROM clientes WHERE clientes.id = {id}')
    nomes = cursor.fetchall()
    lista_nomes = []
    if len(nomes) > 0:
        for nome in nomes:
            lista_nomes.append(nome[0])
    else:
        print('Não existem clientes cadastrados.')
    desconectar(conn)
    return lista_nomes

def listar_contratos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contratos')
    contratos = cursor.fetchall()
    lista_contratos = []
    for contrato in contratos:
        lista_contratos.append(contrato[1])
    desconectar(conn)
    return lista_contratos

def listar_contratos_vencidos():
    """
    Função para listar os contratos vencidos
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT cli.nome,  contratos.vencimento, cli.id FROM clientes as cli, contratos WHERE contratos.id_cliente = cli.id AND contratos.vencimento < date('now','-2 day') GROUP BY cli.id")
    clientes = cursor.fetchall()
    lista_clientes = []
    if len(clientes) > 0:
        for cliente in clientes:
            # cliente = {'Nome': cliente[0], 'CPF': cliente[1], 'Telefones': cliente[2], 'Vencimento': cliente[4]}
            # lista_clientes.append(cliente)
            inserir_id_envio(cliente[2])
    else:
        print('Não existem clientes cadastrados.')
    desconectar(conn)
    # return lista_clientes

#

def listar_contratos_licitacao():
    """
    Função para listar os contratos vencidos
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT cli.nome, cli.cpf, telefones.numero, contratos.id_cliente, contratos.vencimento FROM telefones, clientes as cli, contratos WHERE telefones.whatsapp == 1 AND cli.id = contratos.id_cliente and telefones.id_cliente = cli.id AND contratos.situacao LIKE '%LICI%'  GROUP BY contratos.id_cliente")
    clientes = cursor.fetchall()
    lista_clientes = []
    if len(clientes) > 0:
        for cliente in clientes:
            inserir_id_envio(str(cliente[3]))
            cliente = {'Nome': cliente[0], 'CPF': cliente[1], 'Telefones': cliente[2], 'Vencimento': cliente[4]}
            lista_clientes.append(cliente)
    else:
        print('Não existem clientes cadastrados.')
    desconectar(conn)
    return lista_clientes

def lista_telefones(whatsapp):
    """
    Função para listar os telefones
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM 'telefones' WHERE telefones.whatsapp = {whatsapp}")
    telefones = cursor.fetchall()
    lista_telefones = []
    if len(telefones) > 0:
        for telefone in telefones:
            lista_telefones.append(telefone[1])
    else:
        print('Não existem números cadastrados.')
    desconectar(conn)
    return lista_telefones

def filtra_calculo_margem():
    """
            Função para listar clientes com margem acima de R$ 500,00
            """
    # data30, data60, data90, data120 = calcular_data()

    try:
        conn = conectar()
        cursor = conn.cursor()
        clientes1 = []
        cursor.execute(
            f'SELECT clientes.id, clientes.cpf, clientes.nome, clientes.limite FROM clientes')
        clientes = cursor.fetchall()

        for cliente in clientes:
            id = cliente[0]
            d30 = 0
            d60 = 0
            d90 = 0
            d120 = 0
            total_emprestimo = 0
            cursor.execute(
                f'select SUM(contratos.valor_avaliacao) as total, clientes.limite from contratos, clientes where contratos.id_cliente = clientes.id AND clientes.id = {id}')
            cliente_limite = cursor.fetchall()
            total = cliente_limite[0][0]
            limite = cliente_limite[0][1]
            cursor.execute(
                f'select contratos.numero, contratos.vencimento, contratos.valor_avaliacao, contratos.valor_emprestimo, contratos.prazo, contratos.id_cliente, clientes.id from contratos, clientes where contratos.id_cliente = clientes.id AND clientes.id = {id}')
            contratos = cursor.fetchall()
            if len(contratos) > 0:
                for contrato in contratos:
                    vencimento = datetime.datetime.strptime(contrato[1].split(' ')[0], '%Y-%m-%d')
                    prazo = contrato[4]
                    avaliacao = contrato[2]
                    emprestimo = contrato[3]
                    # limite = contrato[5]
                    if limite == 100:
                        total_emprestimo += avaliacao
                    else:
                        total_emprestimo += avaliacao * .85
                    d30_t, d60_t, d90_t, d120_t = calcular_margem(avaliacao, emprestimo,
                                                                  vencimento, prazo, limite, total)
                    d30 += d30_t
                    d60 += d60_t
                    d90 += d90_t
                    d120 += d120_t
                if d30 < -500:
                    inserir_id_envio(id)
                    telefones = listar_telefones_por_cpf(cliente[1])
                    sem_whats = lista_telefones("0")
                    if len(telefones) >= 1:
                        for telefone in telefones:
                            if telefone not in sem_whats:
                                telefone = str(telefone)

                                if len(telefone) == 13:
                                    telefone = telefone[0:4]+telefone[5:13]
                                    cliente_1 = {'Nome': cliente[2], 'CPF': cliente[1], 'Telefones': telefone,
                                               'Vencimento': vencimento, 'Margem': d30}
                                    clientes1.append(cliente_1)
        else:
            print('Cliente sem contratos ativos')
        desconectar(conn)
        clientes = pd.DataFrame(clientes1)
        clientes.drop_duplicates(subset='Telefones', inplace=True)
        clientes1 = clientes.to_dict('records')

        return clientes1

    except Exception as e:
        print(e)
        pass

def consulta_prazo(contrato):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT prazo FROM contratos WHERE contratos.numero = '{contrato}'")
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
        cursor.execute(f"DELETE FROM 'contratos' WHERE numero='{numero}'")
        conn.commit()
    except:
        pass
    conn.close()

def deletar_contrato_desatualizado(data):
    conn = conectar()
    cursor = conn.cursor()
    try:
        data = datetime.datetime.strftime(datetime.datetime.strptime(data.split()[0], '%d/%m/%Y'), '%Y-%m-%d %H:%M:%S')
        cursor.execute(f"DELETE FROM 'contratos' WHERE data_atualizacao!='{data}'")
        conn.commit()
    except:
        pass
    conn.close()
def deletar_telefone(telefone):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM 'telefones' WHERE numero={telefone}")
        conn.commit()
    except:
        pass
    conn.close()

def deletar_cliente(cpf):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM 'clientes' WHERE cpf='{cpf}'")
        conn.commit()
    except:
        pass
    conn.close()

def deletar_sem_whats(telefone):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(f"UPDATE telefones set whatsapp={1} WHERE numero={telefone}")
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
                f"UPDATE contratos SET vencimento='{vencimento}', valor_emprestimo={valor_emprestimo}, valor_avaliacao={valor_avaliacao}, data_atualizacao='{data}', prazo={prazo} WHERE numero='{numero}'")
        conn.commit()
    if cursor.rowcount == 1:
        print('Contrato atualizado com sucesso.')
    else:
        print('Erro ao atualizar contrato.')


# PESQUISA ID

def pesquisa_id(cpf):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(f"SELECT id FROM clientes WHERE cpf='{cpf}'")
    id = cursor.fetchone()

    return id[0]

def pesquisa_id_por_telefone(numero):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(f"SELECT t.numero, t.id_cliente, c.id, c.cpf FROM telefones as t, clientes as c where c.id = id_cliente and t.numero = {numero}")
    id = cursor.fetchone()
    if id[0] is not None:
        return id[0]

def pesquisa_data_atualizacao(numero_contrato):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute(f"SELECT c.data_atualizacao FROM contratos as c WHERE c.numero='{numero_contrato}'")
    data = cursor.fetchone()
    if data == None:
        print(f'Contrato novo {numero_contrato} efetuar a inclusão pelo relatório da bezel')
        return None
    return data[0]

# OUTROS




