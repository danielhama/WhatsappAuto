from models.utils import listar_Contratos, listar_Telefones_por_cpf, listar_nome, listar_limite, listar, \
                            listar_total_av_emp_por_CPF
import pandas as pd
def gera_personalizado_contratos():
    lista_contratos = []
    contratos = listar_Contratos()
    for contrato in contratos:
        telefones = listar_Telefones_por_cpf(contrato[10])
        nome = listar_nome(contrato[10])[0]
        limite = listar_limite(contrato[10])[0]
        margem = calcula_margem(float(contrato[6]), float(contrato[7]), limite)
        contrato_temp = {'Número': mascara_contrato(contrato[2]),
                         'CPF': mascara_cpf(contrato[10]),
                         "Nome": nome,
                         'Data de Emissão': contrato[3],
                         'Vencimento': contrato[4],
                         "Prazo": contrato[5],
                         'Avaliação': contrato[6].replace(".", ","),
                         'Empréstimo': contrato[7].replace(".", ","),
                         "Atualizado em": contrato[8][:-16],
                         "Situação": contrato[9],
                         "Modalidade": contrato[11],
                         "Qtde Renovações": contrato[12],
                         "Qtde Parcelas":   contrato[14],
                         "Telefones": telefone_string(telefones),
                         "Margem": str(margem).replace(".", ","),
                         "Limite": limite

                         }
        lista_contratos.append(contrato_temp)
    df = pd.DataFrame(lista_contratos)
    df.to_csv(r"C:\Bezel\Reports\Personalizado_Contratos.csv", index=False, sep=";")
def telefone_string(lista):
    string = ''
    for i in lista:
        string = string + mascara_telefone(i)
    return string
def mascara_cpf(cpf):
    return cpf[:3] + '.' + cpf[3:6] + "." + cpf[6:9] + "-" + cpf[9:]

def mascara_contrato(contrato):
    return contrato[:4] + "." + contrato[4:7] + "." + contrato[7:-1] + "-" + contrato[-1]

def calcula_margem(avaliacao, emprestimo, limite):
    avaliacao = float(avaliacao)
    emprestimo = float(emprestimo)
    limite = float(limite)
    valor_max = avaliacao * limite / 100
    return valor_max - emprestimo
def mascara_telefone(telefone):
    return "(" + telefone[:2] + ") " + telefone[2:] + " -"


def gera_clientes():
    lista_clientes = []
    clientes = listar()
    for cliente in clientes:
        telefones = listar_Telefones_por_cpf(cliente['CPF'])
        avaliacao, emprestimo = listar_total_av_emp_por_CPF(cliente['CPF'])
        contrato_temp = {'CPF': mascara_cpf(cliente['CPF']),
                         "Nome": cliente["Nome"],
                         "Telefones": telefone_string(telefones),
                         "Limite": cliente["Limite"],
                         "ΣEmpréstimo": str(emprestimo).replace(".", ","),
                         "ΣAvaliações": str(avaliacao).replace(".", ","),
                         "Atualização": cliente['Atualizacao']
                         }
        lista_clientes.append(contrato_temp)
    df = pd.DataFrame(lista_clientes)
    df.to_csv(r"C:\Bezel\Reports\Personalizado_Clientes.csv", index=False, sep=";")
