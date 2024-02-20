import asyncio
import os
from time import sleep
import pathlib
from selenium import webdriver
# from selenium.common import TimeoutException
# from selenium.common import TimeoutException, NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd

from models.utils import *
import holidays
from selenium.webdriver.chrome.webdriver import *
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
# import undetected_chromedriver as uc

from models.Seletores import data_inventario, usuario, contratos_ativos, confirma_inventario, menu, cpf_selector, \
    situacao, modalidade


class Sipen:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Sipen, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        super().__init__()
        self.erro = []
        self.driver = None
        self.user = None
        self.password = None
        self.sipen = "http://sipen.caixa/sipen"
        self.pesquisa_cliente = "/CarregarManterPesquisaCliente.do?"
        self.consulta_contrato = "https://sipen.caixa/sipen/ListarInformacaoContrato.do?method=carregar&numeroContrato="

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
        if head == True:
            options = webdriver.ChromeOptions()
            options.add_argument("-headless")
        # self.driver = uc.Chrome(driver_executable_path=r"C:\Users\c084029\Downloads\chromedriver_win32\chromedriver.exe", options=options)
        self.driver = webdriver.Chrome(service=Service(
            executable_path=r"C:\Users\c084029\.wdm\drivers\chromedriver\win32\107.0.5304.62\chromedriver.exe", port
            =443), options=options)
        # self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(driver_version="107.0.5304.62").install()), options=options)

        self.driver.maximize_window()

    def load_sipen(self):
        self.driver.get("http://sipen.caixa/sipen/Login.do?method=carregar")
        WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.CSS_SELECTOR, menu)))

    def fecha_driver(self):
        try:
            self.driver.quit()
        except:
            pass

    def set_user(self, user):
        user = self.user

    def set_password(self, password):
        password = self.password

    def pesquisa_seletor(self, selector: str, tempo: int):
        return WebDriverWait(self.driver, tempo).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))

    def atualiza_pagina(self):
        self.driver.get("http://sipen.caixa/sipen/Login.do?method=carregar")
        WebDriverWait(self.driver, 120).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, usuario)))

    async def inventario(self) -> None:
        while self.driver is None:
            sleep(1)
        self.load_sipen()
        data = ontem_feriado()
        data = data.strftime("%d/%m/%Y")
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
        sleep(5)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        for j in self.driver.window_handles:
            if j != window:
                self.driver.switch_to.window(j)
                self.driver.close()
                self.driver.switch_to.window(window)
                break

    def abre_inventario(self):
        try:
            inventario = pathlib.Path(r"C:\Users\c084029\Downloads\RelatorioInventarioGeralContrato.xls")
            data = datetime.datetime.fromtimestamp(inventario.stat().st_atime)
            data = datetime.date(year=data.year, month=data.month, day=data.day)
            hoje = datetime.datetime.today()
            hoje = datetime.date(year=hoje.year, month=hoje.month, day=hoje.day)
            if data == hoje:
                return True
            else:
                return False
        except FileNotFoundError as e:
            return False

    async def atualizar(self):
        while self.driver is None:
            sleep(1)
        try:
            self.pesquisa_seletor(menu, 3)
        except:
            self.load_sipen()
        inventario = pathlib.Path(r"C:\Users\c084029\Downloads\RelatorioInventarioGeralContrato.xls")
        inventarioDF = pd.read_excel(inventario, header=3)

        for idx, i in inventarioDF.iterrows():
            print(f"Iniciando pesquisa para Contrato {i['Nr. Contrato']}")
            i['Nr. Contrato'] = i['Nr. Contrato'].replace(".", "").replace("-", "")
            # WebDriverWait(driver, 10).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, usuario)))
            try:
                await self.situacao(numero=i['Nr. Contrato'], vencimento=i['Vencimento'],
                                    valor_avaliacao=i['Avaliação'],
                                    valor_emprestimo=i['Empréstimo'],
                                    emissao=i['Emissão'], prazo=i['Prz.'])
            except Exception as e:
                self.load_sipen()
                try:
                    await self.situacao(numero=i['Nr. Contrato'], vencimento=i['Vencimento'],
                                        valor_avaliacao=i['Avaliação'],
                                        valor_emprestimo=i['Empréstimo'],
                                        emissao=i['Emissão'], prazo=i['Prz.'])
                except Exception as e:
                    print(e)
                    self.erro.append(i['Nr. Contrato'])
        self.fecha_driver()

    async def situacao(self, numero, vencimento, valor_emprestimo, valor_avaliacao, emissao, prazo):
        while self.driver is None:
            sleep(1)
        # self.load_sipen()
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

    # def main(self):
    #     try:
    #         sipen = Sipen()
    #         if sipen.abre_inventario():
    #             sipen.chama_driver()
    #             # sipen.load_sipen()
    #             asyncio.run(sipen.atualizar())
    #             # sipen.fecha_driver()
    #         else:
    #             sipen.deleta_arquivo()
    #             sipen.chama_driver()
    #             # sipen.load_sipen()
    #             sipen.inventario()
    #             asyncio.run(sipen.atualizar())
    #             # sipen.fecha_driver()
    #         sleep(1)
    #         limpa_contratos()
    #         sipen.deleta_arquivo()
    #
    #     except NoSuchWindowException:
    #         pass
    #     except FileNotFoundError as e:
    #         sipen = Sipen()
    #         sipen.chama_driver()
    #         sipen.load_sipen()
    #         sipen.atualizar()
    #         sipen.fecha_driver()


# Função para verificar se ontem foi feriado
def ontem_feriado():
    hoje = datetime.datetime.now()
    if hoje.weekday() == 0:
        data = hoje + datetime.timedelta(days=-3)
    else:
        data = hoje + datetime.timedelta(days=-1)
    data = datetime.date(year=data.year, month=data.month, day=data.day)

    if data in holidays.country_holidays(country='Brazil', years=2023).keys():
        if hoje.weekday() == 0:
            data = hoje + datetime.timedelta(days=-3)
        else:
            data = hoje + datetime.timedelta(days=-1)
        return data
    else:
        return data
