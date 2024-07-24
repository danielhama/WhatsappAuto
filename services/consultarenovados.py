import datetime
from time import sleep

import pandas as pd
import xlwings as xw
from selenium.common.exceptions import NoSuchFrameException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

import models.SeletoresRelatorios as s
from services.consultasipen import ConsultaSipen


class Renovados(ConsultaSipen):
    dataframe = None
    path = None

    def __init__(self, path, login, senha):
        super().__init__(login, senha)
        self.path = path

    def start(self):
        self.chama_driver()
        self.acessar_relatorio_menu(s.menu_renovados)
    def data_referencia(self) -> object:
        try:
            self.driver.switch_to.frame("iframe01")
        except NoSuchFrameException:
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame("principal")
            self.driver.switch_to.frame("iframe01")

        return self.pesquisa_seletor(s.data_ref, 60)

    def abrir_arquivo(self):
        self.dataframe = pd.read_csv(self.path, delimiter=';')

    def consulta_data(self, data_inicial, data_final, tabelas, arquivo):
        if type(data_inicial) == str:
            data_inicial = datetime.datetime.strptime(data_inicial, "%d/%m/%Y")
        if type(data_final) == str:
            data_final = datetime.datetime.strptime(data_final, "%d/%m/%Y")
        if data_inicial > data_final:
            return
        elif self.driver == None:
            self.start()
        while data_inicial <= data_final:
            if self.dia_semana(data_inicial):
                data_ref = self.data_referencia()
                data_ref.clear()
                data_ref.send_keys(data_inicial.strftime("%d/%m/%Y"))
                data_ref.send_keys(Keys.RETURN)
                try:
                    sleep(0.5)
                    if self.driver.switch_to.alert.text == "DATA INFORMADA NÃO É UM DIA ÚTIL":
                        self.driver.switch_to.alert.accept()
                        sleep(.2)
                        try:
                            self.data_referencia()
                        except:
                            self.voltar()
                    else:
                        self.driver.switch_to.alert.accept()
                        sleep(.2)
                        self.voltar()
                except:
                    self.procura_relatorio()
                data_inicial = data_inicial + datetime.timedelta(days=+1)
            else:
                data_inicial = data_inicial + datetime.timedelta(days=+1)

    def dataframe_to_csv(self):
        self.dataframe.to_csv(
            r"C:\Users\c084029\OneDrive - Caixa Economica Federal\Documentos\Análise Penhor\renovacoes1.csv", sep=";",
            index=False)

    def procura_relatorio(self):
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame("principal")
        sleep(.5)
        relatorio = self.driver.find_element(By.CSS_SELECTOR, 'body').text
        self.tratamento_relatorio_renovacao(relatorio)
        self.dataframe_to_csv()
        self.voltar()

    def tratamento_relatorio_renovacao(self, relatorio: str):
        linha = []
        posicoes = [3, 5, 7]
        contador = 0
        data = relatorio.split("\n")[2].split(" ")[7]
        relatorio = relatorio.split("\n")
        tamanho = len(relatorio)
        if tamanho > 0:
            while posicoes[2] < tamanho:
                if relatorio[posicoes[0]] == "":
                    posicoes = [pos + 4 for pos in posicoes]
                if "TOTALIZADORES" in relatorio[posicoes[0]] or "OUTRAS AGÊNCIAS" in relatorio[posicoes[0]]:
                    break
                primeira_linha = relatorio[posicoes[0]].split(" ")
                if len(primeira_linha) == 1:
                    break
                linha.append(primeira_linha[1])
                linha.append(primeira_linha[4])
                linha.append(primeira_linha[8])
                linha.append(primeira_linha[16])
                linha.append(primeira_linha[12])
                for i in relatorio[posicoes[1]].split(" "):
                    linha.append(i)
                for i in relatorio[posicoes[2]].split(" "):
                    linha.append(i)

                if len(linha) == 32:
                    linha.pop(11)
                    linha.pop(24)
                linha.append(data)
                if self.dataframe is None:
                    self.dataframe = pd.DataFrame(data=[linha],
                                                  columns=["CONTRATO", "UNIDADE AUTENT.", "NUMERO DA GUIA",
                                                           "VLR LIQUIDO",
                                                           "(P/R)", "SIT ANT", "PRAZO ANT", "MOD ANT", "VENCIMENTO ANT",
                                                           "AVALIACAO ANT", "EMPRESTIMO ANT", "APROP JUROS",
                                                           "JUROS P/C.A",
                                                           "DEDUCAO", "DEDUCAO AFSTO", "ACERTO", "TAXA LICITACAO",
                                                           "DEBITO ANTERIOR", "SITUACAO", "PRAZO", "MOD", "VENCIMENTO",
                                                           "AVALIACAO", "EMPRESTIMO", "JUROS", "SEGURO", "IOF", "TAC",
                                                           "CUSTODIA", "LIQUIDO", "DATA REFERENCIA"]
                                                  )
                    linha = []
                else:
                    self.dataframe.loc[len(self.dataframe)] = linha
                    linha = []

                posicoes = [pos + 5 for pos in posicoes]

    def voltar(self):
        try:
            self.window()
            self.driver.switch_to.default_content()
            WebDriverWait(self.driver, 2).until(ec.presence_of_element_located((By.ID, "principal")))
            self.driver.switch_to.frame("principal")
            self.driver.find_element(By.CSS_SELECTOR, s.voltar).click()
        except:
            try:
                self.window()
                self.driver.find_element(By.CSS_SELECTOR,
                                         s.voltar).click()
            except:
                pass

    def ultima_data(self):
        if self.dataframe is not None:
            ultima_linha = self.dataframe.loc[len(self.dataframe) - 1]
            data = datetime.datetime.strptime(ultima_linha["DATA REFERENCIA"], "%d/%m/%Y")
            data = data + datetime.timedelta(days=1)
            return data.strftime("%d/%m/%Y")


        else:
            return "06/11/2011"


    def consulta_data_faltantes(self, tabelas, arquivo):
        book = xw.Book(
            r"C:\Users\c084029\OneDrive - Caixa Economica Federal\Documentos\Análise Penhor\datasliquidados.xlsx")
        lista = book.sheets[0]['A2'].expand('vertical')
        book.close()
        for data in lista:
            if self.dia_semana(data.formula):
                data_ref = self.data_referencia()
                data_ref.clear()
                data_ref.send_keys(data.formula)
                data_ref.send_keys(Keys.RETURN)
                try:
                    sleep(0.5)
                    if self.driver.switch_to.alert.text == "DATA INFORMADA NÃO É UM DIA ÚTIL":
                        self.driver.switch_to.alert.accept()
                        sleep(.2)
                        try:
                            self.data_referencia()
                        except:
                            self.voltar()
                    else:
                        self.driver.switch_to.alert.accept()
                        sleep(.2)
                        self.voltar()
                except:
                    self.procura_relatorio()
