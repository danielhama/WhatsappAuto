from models.utils import listar, listar_telefones_por_cpf
from csv import writer
from random import choice
from os import path


def alea():
    tipo = ['WORK', 'HOME', 'WORK2', 'HOME2']
    return choice(tipo)


def csv_para_vcf():
    with open(path.join(path.expanduser('~'), 'whatsrelatorios/contatos.vcf'), 'w') as file:
        escritor = writer(file, delimiter='|')
        clientes = listar()
        for cliente in clientes:
            telefones = listar_telefones_por_cpf(cliente['CPF'])
            escritor.writerow({'BEGIN:VCARD'})
            escritor.writerow({'VERSION:2.1'})
            escritor.writerow({f"N:;{cliente['Nome']};;;{cliente['CPF']}"})
            escritor.writerow({f"FN:{cliente['Nome']}"+","+f"{cliente['CPF']}"})
            for numero in telefones:
                numero = str(numero)
                i = numero[0:13]
                tipo = alea()
                escritor.writerow({f"TEL;{tipo};;CELL:+{i}"})
            escritor.writerow({'END:VCARD'})


# def clientes_vcard():
#     try:
#         csv_para_vcf('whatsrelatorios/Clientes.csv')
#     except:
#         pass
# def clientes_com_whats_vcard():
#     csv_para_vcf('whatsrelatorios/Clientes_com_whats.csv')
#
#

