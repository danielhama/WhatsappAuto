from models.utils import *
logging.basicConfig(filename='app.log', level=logging.INFO)


def leia_arquivo(arquivo):
    """ Função importa o relatório csv usando o pandas, separa os telefones em colunas e
    define como uma lista
"""
    relatorio = arquivo

    try:
        relatorio = arquivo
        clientes = importacao(relatorio)
        clientes = formata_telefone(clientes)

        return clientes
    except:
        print("Erro na importação")

def importacao(relatorio):
    try:
        try:
            dados = pd.read_csv(relatorio, sep=';', header=0)
        except KeyError as e:
            dados = pd.read_csv(relatorio, sep=',', header=0)
        dados.drop_duplicates(subset='CPF', inplace=True)
        clientes = []
        for idx, linha in dados.iterrows():
            inserir_cliente(linha['Nome'], linha['CPF'])
        for idx, linha in dados.iterrows():
            cliente = {'Nome': linha['Nome'], 'CPF': linha['CPF'], 'Telefones': linha['Telefones']}
            clientes.append(cliente)
        return clientes
    except KeyError as e:
        try:
            dados = pd.read_csv(relatorio, sep=';', header=0)
        except KeyError as e:

            dados = pd.read_csv(relatorio, sep=',', header=0)
        if dados['Vencimento'] is not None:
            dados.dropna(inplace=True)
            clientes = []
            for idx, linha in dados.iterrows():
                inserir_cliente(linha['Nome'], linha['CPF'])
            dados.drop_duplicates(subset='CPF', inplace=True)
            for idx, linha in dados.iterrows():
                cliente = {'Nome': linha['Nome'], 'CPF': linha['CPF'], 'Telefones': linha['Telefones']}
                clientes.append(cliente)
            return clientes

def formata_telefone(clientes):
    try:
        for idx1, cliente in enumerate(clientes):
            if type(cliente['Telefones'])  == str:
                lista = cliente['Telefones'].split(',')
                lista_telefones = []
                for i in lista:
                    if type(i) == float:
                        lista.remove(i)
                    else:
                        try:
                            i = i.strip()
                            if i[2] == i[2] == '9' or i[2] == '8':
                                lista_telefones.append("55" + i)
                        except Exception as e:
                            pass


                for idx, i in enumerate(lista_telefones):
                    j = i
                    if len(str(i)) == 12:
                        i = str(i)
                        x = i[0:4]
                        i = x + '9' + i[4:12]
                        lista_telefones.remove(j)
                        lista_telefones.insert(idx, i)

                    lista_telefones = set(lista_telefones)
                    lista_telefones = list(lista_telefones)

                    try:
                        id_cliente = pesquisa_id(clientes[idx1]['CPF'])
                        if len(lista_telefones) > 0:
                            for telefone in lista_telefones:
                                inserir_telefone(telefone, id_cliente)
                    except:
                        pass
                clientes[idx1]['Telefones'] = lista_telefones
            elif type(cliente['Telefones']) == int:
                telefone = str(cliente['Telefones'])
                if len(telefone) == 12:
                    ddd = telefone[0:2]
                    i = ddd + '9' + telefone[-8::]
                    telefone = i
                telefone = "55"+telefone
                id_cliente = pesquisa_id(cliente['CPF'])
                inserir_telefone(telefone, id_cliente)

        clientes = exclui_sem_whats(clientes)
        return clientes
    except Exception as e:
        print(e)

def ler_inventario(arquivo):
    try:
        with open(arquivo, 'r') as file:
            reader = file.readlines()
            lista_contratos = []
            for line in reader:
                if '.213.' in line:
                    numero = line[2:21].strip()
                    lista_contratos.append(numero)
            lista_contratos_antiga = listar_contratos()
            for contrato in lista_contratos_antiga:
                if contrato not in lista_contratos:
                    deletar_contrato(contrato)
            for line in reader:
                if 'REF.:' in line:
                    data = line[123:133]
                if '.213.' in line:
                    numero = line[2:21].strip()
                    vencimento = line[73:83].strip()
                    prazo = line[85:88].strip()
                    avaliacao = line[90:99].strip().replace('.', '')
                    emprestimo = line[108:117].strip().replace('.', '')
                    vencimento = datetime.datetime.strptime(vencimento, '%d/%m/%Y')
                    atualizar_contrato(numero, vencimento, avaliacao, emprestimo, prazo, data)


    except Exception as e:
        logging.exception(str(e))


def exclui_sem_whats(clientes):
    try:
        lista_sem_whats = lista_telefones(0)
        for idx, cliente in enumerate(clientes):
            for idx2, numero in enumerate(cliente['Telefones']):
                if int(numero) in lista_sem_whats:
                    clientes[idx]['Telefones'].remove(numero)
        #             clientes_sem_whats = list(filter(lambda cliente: not cliente['Telefones'], clientes))
        # clientes = list(filter(lambda cliente: cliente['Telefones'], clientes))
        # clientes_sem_whats_df = pd.DataFrame(clientes_sem_whats)
        # clientes_sem_whats_df.to_csv(path.join(path.expanduser('~'), 'whatsrelatorios/Clientes_sem_Whats.csv'), index=False)
        return clientes
    except Exception as e:
        logging.exception(str(e))
        return clientes

# def leia_inventario(arquivo):
#     """ Função importa o relatório csv usando o pandas, separa os telefones em colunas e
#     define como uma lista
# """
#
#     relatorio = arquivo
#     try:
#         lista_contratos =listar_contratos()
#     except Exception as e:
#         logging.exception(str(e))
#     try:
#         try:
#             dados = pd.read_csv(relatorio, sep=';', header=0)
#         except KeyError as e:
#             logging.exception(str(e))
#             dados = pd.read_csv(relatorio, sep=',', header=0)
#         dados.dropna(inplace=True)
#         # labels = list(filter(lambda label: label not in ['Nome', 'Telefones', 'CPF', 'Vencimento'], dados))
#         # dados.drop(columns=labels, inplace=True)
#         lista_contratos_novo = []
#         for idx, linha in dados.iterrows():
#             vencimento = linha['Vencimento'].split(' ')
#             id_cliente = pesquisa_id(linha['CPF'])
#             inserir_contrato(linha['Número'], vencimento[0], linha['Empréstimo'], linha['Avaliação'], id_cliente)
#             lista_contratos_novo.append(linha['Número'])
#         for contrato in lista_contratos:
#             if contrato not in lista_contratos_novo:
#                 deletar_contrato(contrato)
#     except KeyError as e:
#         logging.exception(str(e))
#         try:
#             dados = pd.read_csv(relatorio, sep=';', header=0)
#             # dados.drop_duplicates(subset='CPF', inplace=True)
#         except KeyError as e:
#             logging.exception(str(e))
#             dados = pd.read_csv(relatorio, sep=',', header=0)
#             # dados.drop_duplicates(subset='CPF', inplace=True)
#         if dados['Vencimento'] is not None:
#             dados.dropna(inplace=True)
#         lista_contratos_novo = []
#         for idx, linha in dados.iterrows():
#             vencimento = linha['Vencimento'].split(' ')
#             id_cliente = pesquisa_id(linha['CPF'])
#             inserir_contrato(linha['Número'], vencimento[0], linha['Empréstimo'], linha['Avaliação'], id_cliente)
#             lista_contratos_novo.append(linha['Número'])
#         for contrato in lista_contratos:
#             if contrato not in lista_contratos_novo:
#                 deletar_contrato(contrato)

