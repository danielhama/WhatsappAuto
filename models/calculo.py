import datetime
import logging
logging.basicConfig(filename='app.log', level=logging.INFO)


def calcular_juros(valor_avaliacao, valor_emprestimo, vencimento, prazo):
    hoje = datetime.datetime.today()
    atraso = (hoje - vencimento).days
    if hoje.weekday() == 0 and atraso <=2 and atraso > 0:
        atraso = 0
    ultima_renovacao = vencimento - datetime.timedelta(prazo)
    alteracao_taxa = datetime.datetime.strptime('20/03/2020', '%d/%m/%Y')
    dias = (30, 60, 90, 120)
    IOF_30 = 0.0037241537315997
    IOF_60 = 0.0036488274565912
    IOF_90 = 0.0035730309514621
    IOF_120 = 0.0034980290099124
    taxa = 0.0199
    mora = 1/100
    taxa_diaria = taxa / 30
    tarifa = round((valor_avaliacao * 0.9/100),2)
    # iof = valor_emprestimo * IOF
    juros = []
    if ultima_renovacao < alteracao_taxa:
        taxa_remuneratoria = 0.021
    else:
        taxa_remuneratoria = 0.0199
    for dia in dias:
        if dia == 30:
            iof = round((IOF_30 * valor_emprestimo), 2)
        elif dia == 60:
            iof = round((IOF_60 * valor_emprestimo), 2)
        elif dia == 90:
            iof = round((IOF_90 * valor_emprestimo), 2)
        else:
            iof = round((IOF_120 * valor_emprestimo), 2)
        juro = round(((valor_emprestimo * taxa_diaria * dia) + tarifa + iof), 2)
        juros.append(juro)
    if atraso > 0:
        encargos_atraso = round(((valor_emprestimo * (taxa_remuneratoria/30) * atraso) + (valor_emprestimo * 0.0075) + (
                valor_emprestimo * mora * atraso / 30)),2 )
        for idx, juro in enumerate(juros):
            juro = juros[idx] + encargos_atraso
            juros.pop(idx)
            juros.insert(idx, juro)
        return juros

    elif atraso < 0:
        desconto = atraso * valor_emprestimo * taxa_diaria
        for idx, juro in enumerate(juros):
            juro = juro + desconto
            juros.pop(idx)
            juros.insert(idx, juro)
        return juros
    else:
        return juros

def calcular_data():
    hoje = datetime.datetime.today()
    dias = (30, 60, 90, 120)
    datas = []
    for dia in dias:
        data = hoje + datetime.timedelta(dia)
        data = datetime.datetime.strftime(data, '%d/%m/%Y')
        datas.append(data)
    return datas

def calcular_data_futura(data_futura):
    data_futura = datetime.datetime.strptime(data_futura, '%d/%m/%Y')
    dias = (30, 60, 90, 120)
    datas = []
    for dia in dias:
        data = data_futura + datetime.timedelta(dia)
        data = datetime.datetime.strftime(data, '%d/%m/%Y')
        datas.append(data)
    return datas

def calcular_juros_futuros(valor_avaliacao, valor_emprestimo, vencimento, prazo, data):
    # data = datetime.datetime.strptime(data, '%d/%m/%Y')
    # vencimento = datetime.datetime.strptime(vencimento, '%d/%m/%Y')
    atraso = (data - vencimento).days
    if data.weekday() == 0 and atraso <=2 and atraso > 0:
        atraso = 0
    ultima_renovacao = vencimento - datetime.timedelta(prazo)
    alteracao_taxa = datetime.datetime.strptime('20/03/2020', '%d/%m/%Y')
    dias = (30, 60, 90, 120)
    IOF_30 = 0.0037241537315997
    IOF_60 = 0.0036488274565912
    IOF_90 = 0.0035730309514621
    IOF_120 = 0.0034980290099124
    taxa = 0.0199
    mora = 1/100
    taxa_diaria = taxa / 30
    tarifa = round(valor_avaliacao * 0.9/100, 2)
    juros = []
    if ultima_renovacao < alteracao_taxa:
        taxa_remuneratoria = 0.021
    else:
        taxa_remuneratoria = 0.0199
    for dia in dias:
        if dia == 30:
            iof = IOF_30 * valor_emprestimo
        elif dia == 60:
            iof = IOF_60 * valor_emprestimo
        elif dia == 90:
            iof = IOF_90 * valor_emprestimo
        else:
            iof = IOF_120 * valor_emprestimo
        juro = round(((valor_emprestimo * taxa_diaria * dia) + tarifa + iof), 2)
        juros.append(juro)
    if atraso > 0:
        encargos_atraso = round((valor_emprestimo * (taxa_remuneratoria/30) * atraso) + (valor_emprestimo * 0.0075) + (
                valor_emprestimo * mora * atraso / 30),2)
        for idx, juro in enumerate(juros):
            juro = juros[idx] + encargos_atraso
            juros.pop(idx)
            juros.insert(idx, juro)
        return juros

    elif atraso < 0:
        desconto = atraso * valor_emprestimo * taxa_diaria
        for idx, juro in enumerate(juros):
            juro = juro + desconto
            juros.pop(idx)
            juros.insert(idx, juro)
        return juros
    else:
        return juros

def calcular_margem(valor_avaliacao, valor_emprestimo, vencimento, prazo, limite, total):
    hoje = datetime.datetime.today()
    if limite == 100 and total < 400000:
        margem = valor_avaliacao - valor_emprestimo
        valor_emprestimo1 = valor_avaliacao
    else:
        margem = (valor_avaliacao*.85) - valor_emprestimo
        valor_emprestimo1 = valor_avaliacao * 0.85
    atraso = (hoje - vencimento).days
    ultima_renovacao = vencimento - datetime.timedelta(prazo)
    alteracao_taxa = datetime.datetime.strptime('23/03/2020', '%d/%m/%Y')
    dias = (30, 60, 90, 120)
    IOF_30 = 0.0037241537315997
    IOF_60 = 0.0036488274565912
    IOF_90 = 0.0035730309514621
    IOF_120 = 0.0034980290099124
    taxa = 0.0199
    mora = 1 / 100
    taxa_diaria = taxa / 30
    tarifa = round((valor_avaliacao * 0.9 / 100), 2)
    juros = []
    if ultima_renovacao < alteracao_taxa:
        taxa_remuneratoria = 0.021
    else:
        taxa_remuneratoria = 0.0199
    for dia in dias:
        if dia == 30:
            iof = IOF_30 * valor_emprestimo1
        elif dia == 60:
            iof = IOF_60 * valor_emprestimo1
        elif dia == 90:
            iof = IOF_90 * valor_emprestimo1
        else:
            iof = IOF_120 * valor_emprestimo1
        juro = (valor_emprestimo1 * taxa_diaria * dia) + tarifa + iof - margem
        juros.append(juro)
    if atraso > 0:
        encargos_atraso = (valor_emprestimo * (taxa_remuneratoria / 30) * atraso) + (valor_emprestimo * 0.0075) + (
            valor_emprestimo * mora * atraso / 30)
        for idx, juro in enumerate(juros):
            juro = juros[idx] + encargos_atraso
            juros.pop(idx)
            juros.insert(idx, juro)
        return juros

    elif atraso < 0:
        desconto = atraso * valor_emprestimo * taxa_diaria
        for idx, juro in enumerate(juros):
            juro = juro + desconto
            juros.pop(idx)
            juros.insert(idx, juro)
        return juros
    else:
        return juros

def calcular_liquidacao(valor_emprestimo, vencimento, prazo):
    hoje = datetime.datetime.today()
    atraso = (hoje - vencimento).days
    if hoje.weekday() == 0 and atraso <=2 and atraso > 0:
        atraso = 0
    ultima_renovacao = vencimento - datetime.timedelta(prazo)
    alteracao_taxa = datetime.datetime.strptime('23/03/2020', '%d/%m/%Y')
    taxa = 0.0199
    mora = 1 / 100
    taxa_diaria = taxa / 30

    if ultima_renovacao < alteracao_taxa:
        taxa_remuneratoria = 0.021
    else:
        taxa_remuneratoria = 0.0199

    if atraso > 0:
        encargos_atraso = (valor_emprestimo * (taxa_remuneratoria / 30) * atraso) + (valor_emprestimo * 0.0075) + (
            valor_emprestimo * mora * atraso / 30)
        valor_liquidacao = valor_emprestimo + encargos_atraso
        return valor_liquidacao, encargos_atraso

    elif atraso < 0:
        desconto = atraso * valor_emprestimo * taxa_diaria
        valor_liquidacao = valor_emprestimo + desconto
        return valor_liquidacao, desconto
    else:
        return valor_emprestimo, 0

# print(calcular_juros(3074, 1600, '26/02/2021', 30))