import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from models.utils import *
import holidays
from selenium.webdriver.chrome.webdriver import *
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

from enviar import EnviaMensagem
from models.Seletores import data_inventario, usuario, contratos_ativos, confirma_inventario, menu

class Sipen(EnviaMensagem):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.user = None
        self.password = None

    def chama_driver(self, head: bool = False) -> None:
        profile = os.path.join(r'C:\Users\c084029\PycharmProjects\WhatsappAuto', "profile", "sipen")
        options = webdriver.ChromeOptions()
        options.add_argument(
            r"user-data-dir={}".format(profile))
        if head == True:
            options = Options()
            options.add_argument("-headless")
            self.driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager(driver_version="107.0.5304.62").install()), options=options)
        else:
            self.driver = webdriver.Chrome(
                service=ChromeService(ChromeDriverManager(driver_version="107.0.5304.62").install()), options=options)
        self.driver.get("http://sipen.caixa/sipen/Login.do?method=carregar")
        WebDriverWait(self.driver, 120).until(EC.presence_of_element_located((By.CSS_SELECTOR, menu)))

    def set_user(self, user):
        user = self.user

    def set_password(self, password):
        password = self.password

    def atualiza_pagina(self):
        self.driver.get("http://sipen.caixa/sipen/Login.do?method=carregar")
        WebDriverWait(self.driver, 120).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, usuario)))

    def inventario(self):
        data = ontem_feriado()
        data = data.strftime("%d/%m/%Y")
        self.driver.get("https://sipen.caixa/sipen/jsp/Comuns/Principal.jsp?destino=/CarregarRelInventarioGeralContratos.do")
        frame = self.driver.find_element(By.CSS_SELECTOR, "#iframe01")
        self.driver.switch_to.frame(frame)
        self.pesquisa_seletor(data_inventario, 30).send_keys(data)
        self.driver.find_element(By.CSS_SELECTOR, data_inventario).send_keys(data)
        self.pesquisa_seletor(contratos_ativos, 5).click()
        self.driver.find_element(By.CSS_SELECTOR, confirma_inventario).click()
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.find_element(By.CSS_SELECTOR, "#btnExportar").click()


# Função para verificar se ontem foi feriado
def ontem_feriado():
    hoje = datetime.datetime.now()
    if hoje.weekday() == 0:
        data = hoje + datetime.timedelta(days=-3)
    else:
        data = hoje + datetime.timedelta(days=-1)
    data = datetime.date(year=data.year, month=data.month, day=data.day)

    if data in holidays.country_holidays(country='Brazil', years=2023).keys():
        data -= datetime.timedelta(days=1)
        return data
    else:
        return data


sipen = Sipen()
sipen.chama_driver()
sipen.inventario()