import os
from pathlib import Path
import subprocess
import sys

caminhoUser = Path.home()
pastaPIP = "PIP"
nomeArquivo = "pip.ini"
caminhoPasta = caminhoUser / pastaPIP
caminhoArquivo = caminhoPasta / nomeArquivo

conteudoPipIni = """[global]
index=http://binario.caixa:8081/repository/pypi-repo/pypi
index-url=http://binario.caixa:8081/repository/pypi-repo/simple
trusted-host=binario.caixa
"""

# Criação do diretório e arquivo pip.ini, se necessário
if not caminhoPasta.exists():
    os.makedirs(caminhoPasta)
    print(f"Criada {caminhoPasta}")
else:
    print(f"{caminhoPasta} já existente")

if not caminhoArquivo.exists():
    with open(caminhoArquivo, 'w') as file:
        file.write(conteudoPipIni)
    print(f"Criado {caminhoArquivo}")

# Função para instalar pacotes
def install(required_packages):
    for package in required_packages:
        try:
            __import__(package)
            print(f"{package} já instalado")
        except ImportError:
            print(f"Instalando {package}.")
            try:
                # Primeiro tenta instalar do repositório privado
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"{package} instalado")
            except subprocess.CalledProcessError:
                print(f"Falha ao instalar {package} do repositório privado. Tentando instalar do PyPI oficial.")
                try:
                    # Tenta instalar do PyPI oficial se o repositório privado falhar
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--index-url=https://pypi.org/simple", "--trusted-host=pypi.org"])
                    print(f"{package} instalado com sucesso do PyPI oficial.")
                except subprocess.CalledProcessError as e:
                    print(f"Erro ao instalar {package}: {e}")

# Lista de pacotes a serem instalados
required_packages = ["io", "tkinter", "zipfile", "pandas", "fnmatch", "array", "lxml", "datetime", "numpy", "openpyxl", "termcolor"]
install(required_packages)
