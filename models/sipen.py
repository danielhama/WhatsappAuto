import os
import pathlib
from time import sleep

import holidays
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import *
# from selenium.common import TimeoutException
# from selenium.common import TimeoutException, NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

import models.SeletoresRelatorios as s
from models.Seletores import data_inventario, usuario, contratos_ativos, confirma_inventario, cpf_selector, \
    situacao, modalidade
from models.utils import *


# import undetected_chromedriver as uc


class Sipen:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Sipen, cls).__new__(cls)
        return cls.instance

    def __init__(self, login, senha):
        super().__init__()
        self.inventario_path = None
        self.erro = []
        self.driver = None
        self.matricula = login
        self.senha = senha
        self.sipen = "http://sipen.caixa/sipen"
        self.pesquisa_cliente = "/CarregarManterPesquisaCliente.do?"
        self.consulta_contrato = "https://sipen.caixa/sipen/ListarInformacaoContrato.do?method=carregar&numeroContrato="

    def login(self) -> bool:
        if self.matricula is not None and self.senha is not None:
            self.driver.get("http://sipen.caixa/")
            try:
                if self.frame('frame'):
                    WebDriverWait(self.driver, 120).until(
                        ec.visibility_of_element_located((By.CSS_SELECTOR, s.usuario)))
                    self.pesquisa_seletor(s.usuario, 30).send_keys(self.matricula)
                    self.pesquisa_seletor(s.senha, 10).send_keys(self.senha)

                    self.pesquisa_seletor(s.botao_login, 10).click()
                    return True
            except:
                return False

    def frame(self, frame_name):
        try:
            self.driver.switch_to.default_content()
            frame = WebDriverWait(self.driver, 5).until(ec.presence_of_element_located((By.ID, "principal")))
            if frame.tag_name == frame_name:
                self.driver.switch_to.frame(frame)
                return True
            else:
                return False
        except:
            return False

    # @threaded
    def chama_driver(self, head: bool = False) -> None:
        profile = os.path.join(r'C:\Users\c084029\PycharmProjects\WhatsappAuto', "profile", "sipen")
        options = webdriver.ChromeOptions()
        options.add_argument(
            r"user-data-dir={}".format(profile))
        # options.headless = False
        # options.browser_version = "107"
        options.add_argument("disable-infobars")
        options.add_argument("start-maximized")
        if head:
            options = webdriver.ChromeOptions()
            options.add_argument("-headless")
        # self.driver = uc.Chrome(driver_executable_path=r"C:\Users\c084029\Downloads\chromedriver_win32\chromedriver.exe", options=options)
        self.driver = webdriver.Chrome(
            service=Service(
            executable_path=r"C:\Users\c084029\.wdm\drivers\chromedriver\win32\107.0.5304.62\chromedriver.exe",
            port=443),
            options=options)

        self.driver.maximize_window()

    def fecha_driver(self):
        try:
            self.driver.quit()
        except:
            pass

    def pesquisa_seletor(self, selector: str, tempo: int):
        return WebDriverWait(self.driver, tempo).until(ec.presence_of_element_located((By.CSS_SELECTOR, selector)))

    def atualiza_pagina(self):
        self.driver.get("http://sipen.caixa/sipen/Login.do?method=carregar")
        WebDriverWait(self.driver, 120).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, usuario)))

    def inventario(self) -> None:
        while self.driver is None:
            sleep(1)
        self.login()
        data = ontem_feriado()
        data = data.strftime("%d/%m/%Y")
        # menuIrpara(self.driver, '/CarregarRelInventarioGeralContratos.do')
        self.driver.get(
            "https://sipen.caixa/sipen/jsp/Comuns/Principal.jsp?destino=/CarregarRelInventarioGeralContratos.do")
        window = self.driver.current_window_handle

        frame = self.driver.find_element(By.CSS_SELECTOR, "#iframe01")
        self.driver.switch_to.frame(frame)
        self.pesquisa_seletor(data_inventario, 30).send_keys(data)
        self.driver.find_element(By.CSS_SELECTOR, data_inventario).send_keys(data)
        self.pesquisa_seletor(contratos_ativos, 5).click()
        self.driver.find_element(By.CSS_SELECTOR, confirma_inventario).click()
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.find_element(By.CSS_SELECTOR, "#btnExportar").click()
        self.download_wait()
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        for j in self.driver.window_handles:
            if j != window:
                self.driver.switch_to.window(j)
                self.driver.close()
                self.driver.switch_to.window(window)
                return

    def download_wait(self):
        seconds = 0
        dl_wait = True
        while dl_wait and seconds < 20:
            sleep(1)
            dl_wait = False
            for fname in os.listdir(r"C:\Users\c084029\Downloads"):
                if fname.endswith('.crdownload'):
                    dl_wait = True
            seconds += 1
        return False

    def abre_inventario(self):
        try:
            self.inventario_path = pathlib.Path(r"C:\Users\c084029\Downloads\RelatorioInventarioGeralContrato.xls")
            data = datetime.datetime.fromtimestamp(self.inventario_path.stat().st_atime)
            data = datetime.date(year=data.year, month=data.month, day=data.day)
            hoje = datetime.datetime.today()
            hoje = datetime.date(year=hoje.year, month=hoje.month, day=hoje.day)
            if data == hoje:
                return True
            else:
                return False
        except FileNotFoundError:
            return False

    def atualizar(self):
        while self.driver is None:
            sleep(1)

        try:
            if self.driver.find_element(By.CSS_SELECTOR, s.menu) is not None:
                pass
            self.login()
        except:
            self.login()
        inventarioDF = pd.read_excel(self.inventario_path, header=3)
        hoje = datetime.datetime.today()
        hoje = datetime.datetime(year=hoje.year, month=hoje.month, day=hoje.day)
        for idx, i in inventarioDF.iterrows():
            print(f"Iniciando pesquisa para Contrato {i['Nr. Contrato']}")
            i['Nr. Contrato'] = i['Nr. Contrato'].replace(".", "").replace("-", "")
            data_anterior = pesquisa_data_atualizacao(i['Nr. Contrato'])
            if data_anterior is not None:
                data_anterior = datetime.datetime.strptime(data_anterior.split(" ")[0], "%Y-%m-%d")

                if data_anterior == hoje:
                    continue
            # WebDriverWait(driver, 10).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, usuario)))
            try:
                self.situacao(numero=i['Nr. Contrato'], vencimento=i['Vencimento'],
                              valor_avaliacao=i['Avaliação'],
                              valor_emprestimo=i['Empréstimo'],
                              emissao=i['Emissão'], prazo=i['Prz.'])
            except Exception as e:
                self.login()
                try:
                    self.situacao(numero=i['Nr. Contrato'], vencimento=i['Vencimento'],
                                  valor_avaliacao=i['Avaliação'],
                                  valor_emprestimo=i['Empréstimo'],
                                  emissao=i['Emissão'], prazo=i['Prz.'])
                except Exception as e:
                    print(e)
                    self.erro.append(i['Nr. Contrato'])
        self.fecha_driver()

    def situacao(self, numero, vencimento, valor_emprestimo, valor_avaliacao, emissao, prazo):
        while self.driver is None:
            sleep(1)
        self.driver.get(self.consulta_contrato + numero)
        cpf = self.pesquisa_seletor(cpf_selector, 10).text
        cpf = cpf.replace(".", "").replace("-", "")
        _situacao = self.pesquisa_seletor(situacao, 5).text
        _modalidade = int(self.pesquisa_seletor(modalidade, 5).text)
        vencimento = datetime.datetime.strptime(vencimento, '%d/%m/%Y')
        emissao = datetime.datetime.strptime(emissao, '%d/%m/%Y')
        try:
            inserir_contrato(numero=numero, emissao=emissao, vencimento=vencimento,
                             valor_emprestimo=valor_emprestimo, valor_avaliacao=valor_avaliacao,
                             situacao=_situacao,
                             prazo=prazo, cpf=cpf, data=datetime.datetime.today(), modalidade=_modalidade)
        except Exception as e:
            print(e)
            self.erro.append(numero)

    def deleta_arquivo(self):
        try:
            os.remove(pathlib.Path(r"C:\Users\c084029\Downloads\RelatorioInventarioGeralContrato.xls"))
        except FileNotFoundError as e:
            print('Arquivo não existe')

    def fecha(self):
        self.driver.close()


# Função para verificar se ontem foi feriado
def ontem_feriado():
    hoje = datetime.datetime.now()
    if hoje.weekday() == 0:
        data = hoje + datetime.timedelta(days=-3)
    else:
        data = hoje + datetime.timedelta(days=-1)
    data = datetime.date(year=data.year, month=data.month, day=data.day)

    if data in holidays.country_holidays(country='Brazil', years=hoje.year).keys():
        if hoje.weekday() == 0:
            data = hoje + datetime.timedelta(days=-3)
        else:
            data = hoje + datetime.timedelta(days=-1)
        return data
    else:
        return data
