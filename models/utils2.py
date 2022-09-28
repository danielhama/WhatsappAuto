import datetime
import logging
from models.utils import listar_clientes_telefone, pesquisa_id, inserir_id_envio, deletar_lista
logging.basicConfig(filename='app.log', level=logging.INFO)


def filtra_vencimento():
    deletar_lista()
    clientes1 = []
    clientes = listar_clientes_telefone()
    hoje = datetime.datetime.today()
    hj = datetime.datetime.weekday(hoje)
    hoje = hoje.strftime('%Y-%m-%d')
    if hj == 0:
        hoje = datetime.datetime.today()
        ontem = hoje - datetime.timedelta(days=1)
        anteontem = hoje - datetime.timedelta(days=2)
        hoje = hoje.strftime('%Y-%m-%d')
        ontem = ontem.strftime('%Y-%m-%d')
        anteontem = anteontem.strftime('%Y-%m-%d')
        for cliente in clientes:
            vencimento = cliente['Vencimento'].split(" ")[0]
            if vencimento == hoje or vencimento == ontem or vencimento == anteontem:
                id = pesquisa_id(cliente["CPF"])
                inserir_id_envio(id)
                clientes1.append(cliente)
        return clientes1
    else:
        for cliente in clientes:
            if cliente['Vencimento'].split(' ')[0] == hoje:
                id = pesquisa_id(cliente["CPF"])
                clientes1.append(cliente)
                inserir_id_envio(id)
        return clientes1


def filtra_data(pesquisa):
    deletar_lista()
    clientes = listar_clientes_telefone()
    try:
        if '/' in pesquisa:
            data = datetime.datetime.strptime(pesquisa, '%d/%m/%Y')
            try:
                clientes1 = []
                for cliente in clientes:
                    if cliente['Vencimento'] == str(data):
                        inserir_id_envio(pesquisa_id(cliente['CPF']))
                        clientes1.append(cliente)
                return clientes1
            except Exception as e:
                logging.exception(str(e))
                clientes1 = []
                for cliente in clientes:
                    if cliente['Vencimento'] == data:

                        clientes1.append(cliente)
                return clientes1
        else:
            try:
                pesquisa = pesquisa.upper()
                clientes1 = []
                for cliente in clientes:
                    if pesquisa in cliente['Nome']:
                        inserir_id_envio(pesquisa_id(cliente['CPF']))
                        clientes1.append(cliente)
                return clientes1
            except:
                clientes1 = []
                for cliente in clientes:
                    if pesquisa in cliente[0]:
                        inserir_id_envio(pesquisa_id(cliente['CPF']))
                        clientes1.append(cliente)
                return clientes1
    except:
        pass


def filtra_nome(pesquisa):
    clientes = listar_clientes_telefone()
    try:
        clientes1 = []
        for cliente in clientes:
            telefones = []
            if pesquisa in cliente[0]:
                for i in cliente[2].split("'"):
                    if len(i) > 10:
                        telefones.append(i)
                clientes1.append({'Nome': cliente[0], 'CPF': cliente[1], 'Telefones': telefones, 'Vencimento': cliente[3]})
        return clientes
    except:
        clientes1 = []
        for cliente in clientes:
            telefones = []
            if pesquisa in cliente[0]:
                for i in cliente[2].split("'"):
                    if len(i) > 10:
                        telefones.append(i)
                clientes1.append({'Nome': cliente[0], 'CPF': cliente[1], 'Telefones': telefones, 'Vencimento': cliente[3]})
        return clientes

# def filtra_margem():
#     clientes = listar_clientes_telefone()
#     hoje = datetime.datetime.today()
#     clientes1 = []
#     for cliente in clientes:
#         if type(cliente['Vencimento']) == str:
#             data = datetime.datetime.strptime(cliente['Vencimento'], '%d/%m/%Y')
#             if data < hoje:
#                 clientes1.append(cliente)
#     return clientes1



def tempo_execucao(inicio, fim):
    tempo_exec = fim - inicio
    horas = int(tempo_exec // 3600)
    horas_resto = tempo_exec % 3600
    minutos = int(horas_resto // 60)
    segundos = int(horas_resto % 60)

    return horas, minutos, segundos

def salva_texto(texto, file):
    with open(file, 'w') as arquivo:
        for linha in texto:
            arquivo.write(linha)
            arquivo.write('\n')

def leia_texto(file):
    with open(file, 'r') as arquivo:
        texto = arquivo.readlines()
        juncao = ''
        for msg in texto:
            juncao = juncao + msg
        return juncao

##



