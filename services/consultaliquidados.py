import datetime
from time import sleep

import xlwings as xw
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

import models.SeletoresRelatorios as s
from services.consultasipen import ConsultaSipen

class SipenLiquidados(ConsultaSipen):
    pass

    def tratamento_relatorio(self, relatorio: str, path):
        texto_divido = relatorio.split("\n")
        contador = 0
        posicao = [1, 3, 6]
        texto = ""
        tamanho_relatorio = len(texto_divido) - 1
        quantidade_contratos = tamanho_relatorio / 6
        for i in range(0, int(quantidade_contratos)):
            if "Modalidade" in texto_divido[posicao[0]]:
                posicao = [pos + 1 for pos in posicao]
            if "1631.213" in texto_divido[posicao[0]]:
                texto = texto_divido[posicao[0]] + " "
                texto = texto + texto_divido[posicao[1]] + " "
                texto = texto + texto_divido[posicao[2]]
                self.gravacao_txt(texto, path)
            posicao = [pos + 6 for pos in posicao]

    def start(self):
        self.chama_driver()
        self.acessar_relatorio_menu(s.menu_liquidados)
    def gravacao_txt(self, texto, path):

        try:
            arquivo = open(path,
                           "a")
        except Exception as e:
            arquivo = open(path,
                           "w")
        posicoes = [1, 5, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26]
        texto_divido = texto.split(" ")
        if "1631." in texto_divido[1]:
            if len(texto_divido) == 28:
                for i in posicoes:
                    arquivo.write(texto_divido[i])
                    arquivo.write(";")

                arquivo.write("\n")
        arquivo.close()

    def ultima_data(self):
        try:
            arquivo = open(r"C:\Users\c084029\OneDrive - Caixa Economica Federal\Documentos\Análise Penhor\liquidado.txt",
                           "r")
        except Exception as e:
            return "06/11/2011"

        linhas = arquivo.readlines()
        # Campos6,7
        ultima_linha = linhas[-1]
        ultima_linha = ultima_linha.split(";")
        guia = ultima_linha[1].split(".")
        data_guia_str = guia[1]
        data = datetime.date(int(data_guia_str[0:4]), int(data_guia_str[4:6]), int(data_guia_str[6:]))
        data = data + datetime.timedelta(days=1)
        return data.strftime("%d/%m/%Y")

    def voltar(self):
        try:
            self.window()
            self.driver.switch_to.default_content()
            WebDriverWait(self.driver, 2).until(ec.presence_of_element_located((By.ID, "principal")))
            self.driver.switch_to.frame("principal")
            self.driver.find_element(By.CSS_SELECTOR, s.voltar_liquidados).click()
        except:
            try:
                self.window()
                self.driver.find_element(By.CSS_SELECTOR,
                                     s.voltar_liquidados).click()
            except:
               pass

    def consulta_data_faltantes(self, tabelas, arquivo):
        book = xw.Book(r"C:\Users\c084029\OneDrive - Caixa Economica Federal\Documentos\Análise Penhor\datasliquidados.xlsx")
        lista = book.sheets[0]['A2'].expand('vertical')
        for data in lista:
            self.mudar_frame()
            try:
                data_ref = self.pesquisa_seletor(s.data_ref, 60)
            except:
                self.voltar()
                data_ref = self.pesquisa_seletor(s.data_ref, 60)

            data_ref.clear()
            data_ref.send_keys(data.formula)
            data_ref.send_keys(Keys.RETURN)
            try:
                sleep(0.5)
                if self.driver.switch_to.alert.text == "DATA INFORMADA NÃO É UM DIA ÚTIL":
                    self.driver.switch_to.alert.accept()
                    sleep(.2)
                else:
                    self.driver.switch_to.alert.accept()
                    sleep(.2)
                    self.voltar()
            except:
                self.procura_tabela(tabelas=tabelas, arquivo=arquivo)

