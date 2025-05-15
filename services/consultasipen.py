import datetime
from time import sleep

import holidays
import xlwings as xw
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException, NoSuchFrameException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.webdriver import *
import models.SeletoresRelatorios as s
import models.links as l


class ConsultaSipen:
    driver = None
    matricula = None
    senha = None
    def __init__(self, login, senha, arquivo):
        self.matricula = login
        self.senha = senha
        self.arquivo = arquivo
        self.janela_atual = None
    def chama_driver(self):
        # Profile
        profile = os.path.join(r'C:\Users\c084029\PycharmProjects\WhatsappAuto', "profile", "sipen")
        # options = webdriver.Firefox()
        # options.add_argument(
        #     r"user-data-dir={}".format(profile))
        # options.add_argument("disable-infobars")
        # options.add_argument("start-maximized")
        self.driver = webdriver.Firefox(service=Service(
            executable_path=r"C:\Users\c084029\.wdm\drivers\chromedriver\win64\129.0.6668.71\chromedriver-win32\geckodriver.exe",
            port=443))

        self.driver.maximize_window()

    def acessar_relatorio(self, link, seletor):
        if self.login():
            self.driver.get(l.sipen + link)
            try:
                self.pesquisa_seletor(seletor, 60)
                return True
            except:
                return False
        # else:
        #     self.acessar_relatorio(link, seletor)
    def set_janela(self):
        self.janela_atual = self.driver.current_window_handle

    def get_janela(self):
        self.driver.switch_to.window(self.janela_atual)
    def start(self):
        self.chama_driver()
        self.acessar_relatorio_menu(s.menu_novos)

    def acessar_relatorio_menu(self, seletor):
        if self.login():
            menu = self.pesquisa_seletor(s.menu, 10)
            menu.click()
            sleep(.5)
            menu_rel = self.pesquisa_seletor(s.menu_relatorios, 10)
            menu_rel.click()
            sleep(.5)
            relatorio = self.pesquisa_seletor(seletor, 10)
            relatorio.click()
            try:
                sleep(.5)
                self.driver.switch_to.frame("iframe01")
                self.pesquisa_seletor(s.data_ref, 60)
                self.set_janela()
                return True
            except:
                return False
        else:
            self.acessar_relatorio_menu(seletor)

    def mudar_frame(self):
        try:
            self.driver.switch_to.frame("iframe01")
        except NoSuchFrameException:
            try:
                self.driver.switch_to.default_content()
                self.driver.switch_to.frame("principal")
                self.driver.switch_to.frame("iframe01")
            except NoSuchFrameException:
                try:
                    self.voltar()
                    self.driver.switch_to.default_content()
                    self.driver.switch_to.frame("principal")
                except: pass
    def consulta_data(self, data_inicial, data_final, tabelas):
        if type(data_inicial) == str:
            data_inicial = datetime.datetime.strptime(data_inicial, "%d/%m/%Y")
        if type(data_final) == str:
            data_final = datetime.datetime.strptime(data_final, "%d/%m/%Y")
        if data_inicial > data_final:
            return
        elif self.driver == None:
            self.start()
            # window = self.driver.current_window_handle

        while data_inicial <= data_final:
            if self.dia_semana(data_inicial):
                print(f"Iniciando pesquisa para data {data_inicial.strftime('%d/%m/%Y')}")
                self.mudar_frame()
                try:
                    data_ref = self.pesquisa_seletor(s.data_ref, 2)
                except:
                    try:
                        self.voltar()
                        data_ref = self.pesquisa_seletor(s.data_ref, 2)
                    except:
                        self.mudar_frame()
                        data_ref = self.pesquisa_seletor(s.data_ref, 2)


                data_ref.clear()
                data_ref.send_keys(data_inicial.strftime("%d/%m/%Y"))
                data_ref.send_keys(Keys.RETURN)
                try:
                    sleep(0.5)
                    if self.driver.switch_to.alert.text == "DATA INFORMADA NÃO É UM DIA ÚTIL":
                        self.driver.switch_to.alert.accept()
                        sleep(.2)
                        self.get_janela()
                    else:
                        self.driver.switch_to.alert.accept()
                        sleep(.2)
                        # self.voltar()
                        self.get_janela()
                except:
                    self.procura_tabela(tabelas=tabelas, arquivo=self.arquivo)
                data_inicial = self.proximo_dia_util(data_inicial)
            else:
                data_inicial = self.proximo_dia_util(data_inicial)
        self.driver.close()
    def window(self):
        if (len(self.driver.window_handles)) == 2:
            self.driver.switch_to.window(self.driver.window_handles[0])

    def voltar(self):
        try:
            self.window()
            self.driver.switch_to.default_content()
            WebDriverWait(self.driver, 2).until(ec.presence_of_element_located((By.ID, "principal")))
            self.driver.switch_to.frame("principal")
            self.driver.find_element(By.CSS_SELECTOR, s.voltar_novos).click()
        except:
            try:
                self.window()
                self.driver.find_element(By.CSS_SELECTOR,
                                     s.voltar_novos).click()
            except:
                pass
    def procura_tabela(self, tabelas: list, arquivo: str):
        try:
            self.driver.switch_to.window(self.driver.window_handles[0])
            self.driver.switch_to.frame("principal")
            items = self.pesquisa_seletor("body > form > div.pagination", 2).text.split("\n")
            paginas = len(items) - 4

            pagina = 3
            if len(items) == 15:
                breakpoint()


            for _ in range(0, paginas):
                for i in tabelas:
                    try:
                        relatorio = self.driver.find_element(By.CSS_SELECTOR, f"body > form > table:nth-child({i})").text
                        self.tratamento_relatorio(relatorio, arquivo)
                    except NoSuchElementException:
                        print(f"Tabela {i} não existe")
                pagina += 1

                self.driver.find_element(By.CSS_SELECTOR,
                                         f"body > form > div.pagination > ul > li:nth-child({pagina}) > a").click()
            self.voltar()
        except TimeoutException:
            for i in tabelas:
                try:
                    relatorio = self.driver.find_element(By.CSS_SELECTOR, f"body > form > table:nth-child({i})").text
                    self.tratamento_relatorio(relatorio, arquivo)

                except NoSuchElementException as e:
                    self.voltar()
                    return

    def tratamento_relatorio(self, relatorio: str, path):
        texto_divido = relatorio.split("\n")
        contador = 0
        texto = ""
        for i in texto_divido:
            if "1631.213" in i:
                contador = 0
                texto = i + " "
                contador += 1
                continue
            if "Prazo" in i:
                contador += 1
                continue
            if contador == 2:
                texto = texto + i
                contador = 0
                if texto != "":
                    self.gravacao_txt(texto, path)

    def ultima_data(self):
        try:
            arquivo = open(self.arquivo,
                           "r")
        except:
            return "06/11/2011"

        linhas = arquivo.readlines()
        # Campos6,7
        ultima_linha = linhas[-1]
        ultima_linha = ultima_linha.split(";")
        prazo = ultima_linha[5]
        vencimento = ultima_linha[6]

        data = datetime.datetime.strptime(vencimento, "%d/%m/%Y")
        data = data + datetime.timedelta(days=-(int(prazo))+1)
        return data.strftime("%d/%m/%Y")

    def proximo_dia_util(self, data):
        if data.weekday() == 5:
            data += datetime.timedelta(days=2)
        else:
            data += datetime.timedelta(days=1)
        if data in holidays.country_holidays(country='Brazil', years=data.year).keys():
            data += datetime.timedelta(days=1)
            if data.weekday() == 5:
                data = data + datetime.timedelta(days=2)
        return data
    @staticmethod
    def ultimo_dia_util():
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
            return data.strftime('%d/%m/%Y')
        else:
            return data.strftime('%d/%m/%Y')

    def gravacao_txt(self, texto, path):

        try:
            arquivo = open(path,
                           "a")
        except:
            arquivo = open(path,
                           "w")

        nome = ""
        depois_cpf = False
        for i in texto.split(" "):
            if not depois_cpf:
                if "1631.213." in i:
                    arquivo.write(i)
                    arquivo.write(";")
                    continue
                if "1631.20" in i:
                    arquivo.write(i)
                    arquivo.write(";")
                    continue
                if not (len(i) == 14 and "." in i and "-" in i):
                    nome = nome + i + " "
                elif len(i) == 14 and "." in i and "-" in i:
                    arquivo.write(nome)
                    arquivo.write(";")
                    arquivo.write(i)
                    arquivo.write(";")
                    depois_cpf = True
            else:
                arquivo.write(i)
                arquivo.write(";")
        arquivo.write("\n")
        arquivo.close()

    def pesquisa_seletor(self, selector: str, tempo: int):
        return WebDriverWait(self.driver, tempo).until(ec.presence_of_element_located((By.CSS_SELECTOR, selector)))

    def ler_arquivo(self):
        try:
            book = xw.Book(r"C:\Bezel 0.5.7956.34384\Reports\renovacao.xlsx")
            book.sheets[0]['U1'].value = 'Valor Renovação'
            cpf = book.sheets[0]['B2'].value
            lista_celulas = book.sheets[0]['A2'].expand('vertical')
        except:
            raise Exception

        return book, lista_celulas, cpf

    def atualiza_pagina(self):
        self.driver.get("http://sipen.caixa/")
        WebDriverWait(self.driver, 120).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, s.usuario)))

    def login(self) -> bool:
        if self.matricula is not None and self.senha is not None:
            self.driver.get("http://sipen.caixa/")
            try:
                if self.frame('frame'):
                    WebDriverWait(self.driver, 120).until(ec.visibility_of_element_located((By.CSS_SELECTOR, s.usuario)))
                    _usuario = self.pesquisa_seletor(s.usuario, 30).send_keys(self.matricula)
                    _senha = self.pesquisa_seletor(s.senha, 10).send_keys(self.senha)

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

    def consulta_campo(self, campo: str, coluna: str, corte: int, cel: object, book: object):
        try:
            WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR, campo)))
            consultado = self.driver.find_element(By.CSS_SELECTOR, campo).text
            print(consultado)
            cortado = self.driver.find_element(By.CSS_SELECTOR, campo).text[corte::]
            if len(cel.address) < 8:
                book.sheets[0][f'{coluna}{cel.address[3 - len(cel.address)::]}'].value = cortado
            elif len(cel.address) > 8:
                book.sheets[0][f'{coluna}{cel.address[9 - len(cel.address)::]}'].value = cortado
        except Exception as e:
            print(e)

    @staticmethod
    def dia_semana(data: datetime):
        if type(data) == str:
            pass
        elif type(data) == datetime.datetime:
            if data.weekday() == 5 or data.weekday == 6:
                return False
            return True

    @staticmethod
    def ontem_feriado(self) -> datetime:
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
