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
        PRIMARY KEY("id" AUTOINCREMENT));""")

    conn.execute("""CREATE TABLE IF NOT EXISTS  "contratos" (
        "id"	INTEGER NOT NULL,
        "numero"	TEXT NOT NULL UNIQUE,
        "vencimento"	TEXT NOT NULL,
        "valor_emprestimo"	REAL NOT NULL,
        "valor_avaliacao"	REAL NOT NULL,
        "data_atualizacao"	TEXT NOT NULL,
        "limite"	INTEGER NOT NULL,
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



    return conn


def desconectar(conn):
    """
    FunÃ§Ã£o para desconectar do servidor.
    """
    conn.close()

# INSERIR

def inserir_cliente(nome, cpf):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO clientes (nome, cpf) VALUES ('{nome}', '{cpf}')")
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


def inserir_contrato(numero, vencimento, valor_emprestimo, valor_avaliacao, limite, prazo, id_cliente, data):
    conn = conectar()
    cursor = conn.cursor()
    hoje = datetime.datetime.today()
    data = datetime.datetime.strptime(data.split(' ')[0], '%d/%m/%Y')
    valor_avaliacao = convert_to_float(valor_avaliacao)
    valor_emprestimo = convert_to_float(valor_emprestimo)
    try:
        cursor.execute(f"INSERT INTO contratos (numero, vencimento, valor_emprestimo, valor_avaliacao, limite, prazo, id_cliente, data_atualizacao) VALUES ('{numero}', '{vencimento}', '{valor_emprestimo}', '{valor_avaliacao}', {limite}, {prazo}, {id_cliente}, '{data}')")
        conn.commit()
        if cursor.rowcount == 1:
            print("Contrato incluído com sucesso")
    except Exception as e:
        atualizado = datetime.datetime.strptime(pesquisa_data_atualizacao(numero).split(" ")[0], '%Y-%m-%d')
        if atualizado < data:

            cursor.execute(f"UPDATE contratos SET vencimento='{vencimento}', valor_emprestimo={valor_emprestimo}, valor_avaliacao={valor_avaliacao}, data_atualizacao='{data}' WHERE numero='{numero}'")
            conn.commit()
            if cursor.rowcount == 1:
                print('Contrato Atualizado com Sucesso!')
            else:
                print('Erro na atualização')
        else:
            print('Data do relatório mais antiga que a base de dados')
    conn.close()


# LISTAR

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
        "SELECT cli.nome, cli.cpf, telefones.numero, contratos.id_cliente, contratos.vencimento FROM telefones, clientes as cli, contratos WHERE telefones.whatsapp == 1 AND cli.id = contratos.id_cliente and telefones.id_cliente = cli.id AND contratos.vencimento < date('now','-2 day') GROUP BY telefones.numero")
    clientes = cursor.fetchall()
    lista_clientes = []
    if len(clientes) > 0:
        for cliente in clientes:
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
            Função para listar os contratos do cliente
            """
    # data30, data60, data90, data120 = calcular_data()

    try:
        conn = conectar()
        cursor = conn.cursor()
        calculos = []
        clientes1 = []
        # hoje = datetime.datetime.today()
        d30 = 0

        cursor.execute(
            f'select contratos.numero, contratos.vencimento, contratos.valor_avaliacao, contratos.valor_emprestimo, contratos.prazo, contratos.limite, clientes.nome, clientes.cpf from contratos, clientes where contratos.id_cliente = clientes.id')
        clientes = cursor.fetchall()
        if len(clientes) > 0:
            for cliente in clientes:
                vencimento = cliente[1].split(' ')
                vencimento = datetime.datetime.strptime(vencimento[0], '%Y-%m-%d')
                prazo = cliente[4]
                total_avaliacao = cliente[2]
                total_emprestimo = cliente[3]
                limite = cliente[5]
                d30_t, d60_t, d90_t, d120_t = calcular_margem(total_avaliacao, total_emprestimo,
                                                              vencimento, prazo, limite, 0)
                if d30_t < 0 and d30_t < -500:
                    telefones = listar_telefones_por_cpf(cliente[7])
                    sem_whats = lista_telefones("0")
                    if len(telefones) >= 1:
                        for telefone in telefones:
                            if telefone not in sem_whats:
                                cliente_1 = {'Nome': cliente[6], 'CPF': cliente[7], 'Telefones': telefone,
                                           'Vencimento': vencimento, 'Margem': d30_t}
                                clientes1.append(cliente_1)



        else:
            print('Cliente sem margem')
        desconectar(conn)
        clientes = pd.DataFrame(clientes1)
        clientes.drop_duplicates(subset='Telefones', inplace=True)
        clientes1 = clientes.to_dict('records')
        return clientes1

    except Exception as e:
        print(e)
        pass


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
    atualizado = datetime.datetime.strptime(atualizado.split(' ')[0], '%Y-%m-%d')
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
        breakpoint()
    return data[0]

# OUTROS




