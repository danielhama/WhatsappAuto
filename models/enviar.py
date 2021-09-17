import socket
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import invisibility_of_element_located
from qrcode import make
import psutil
from models.utils import *
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import models.Seletores as sel
from selenium.webdriver.firefox.webdriver import FirefoxProfile


class EnviaMensagem:
    def __init__(self):
        super().__init__()
        self.driver = None
        self.lista_sem_whats = lista_telefones(0)
        self.excluidos = 0
        self.sem_whats = []



    def chama_driver(self, head: bool = True) -> None:
        self.profile = FirefoxProfile("/home/daniel/.mozilla/firefox/l4nddl6a.Whatsapp")
        if head == True:
            options = Options()
            options.add_argument("-headless")
            self.driver = webdriver.Firefox(executable_path="geckodriver", options=options, firefox_profile=self.profile)
        else:
            self.driver = webdriver.Firefox(executable_path="geckodriver", firefox_profile=self.profile)
        self.driver.get("https://web.whatsapp.com")

    def fecha_driver(self):
        self.driver.quit()

    def verifica_login(self) -> bool:
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "._2UwZ_ > canvas:nth-child(3)")))
            return False
        except Exception as e:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel.nova_conversa)))
            return True

    def send_whatsapp_msg(self, numero, texto, nome: str, cpf, header: bool = True) -> None:  # Faz a chamada de contato pelo número de telefone.
        try:
            numero = str(numero)
            if len(numero) == 13:
                self.driver.get(f"https://web.whatsapp.com/send?phone={numero[0:4]+numero[5:13]}&source=&data=#")
                # sleep(5)
            else:
                self.driver.get(f"https://web.whatsapp.com/send?phone={numero}&source=&data=#")
                # sleep(5)

        except:
            return
        try:
            sleep(0.5)
            self.driver.switch_to.alert().accept()
        except Exception as e:
            pass
        # Testa se existe o campo de mensagem na página e envia as mensagens
        try:

            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel.campo_msg)))
            txt_box = self.driver.find_element(By.CSS_SELECTOR, sel.campo_msg)
            nome = nome.capitalize()
            if header == True:
                txt_box.send_keys(f'Prezado(a) {nome}')
                ActionChains(self.driver).key_down(Keys.SHIFT).send_keys(Keys.RETURN).key_up(Keys.SHIFT).perform()
            for msg in texto:
                txt_box.send_keys(msg)
                ActionChains(self.driver).key_down(Keys.SHIFT).send_keys(Keys.RETURN).key_up(Keys.SHIFT).perform()
            sleep(.5)
            txt_box.send_keys(Keys.RETURN)
            sleep(.5)

        except Exception as e:
            try:
                self.element_presence(By.XPATH, '//*[@id="app"]/div[1]/span[2]/div[1]/span[1]/div[1]/div[1]', 5)
                print("Número de telefone não tem zap:" + str(numero))
                self.sem_whats.append(numero)
                inserir_sem_whats(numero)
            except:
                return self.send_whatsapp_msg(numero, texto, nome, cpf)

    def element_presence(self, by, xpath, time):  # Define espera para a presença de determinado elemento
        element_present = EC.presence_of_element_located((by, xpath))
        WebDriverWait(self.driver, time).until(element_present)

    def element_not_presence(self, by, id, time):  # Defina espera para a não presença de determinado elemento
        element_not_present = invisibility_of_element_located((by, id))
        WebDriverWait(self.driver, time).until(element_not_present)

    def is_connected(self):  # Testa se existe conexão

        try:
            socket.create_connection(("www.google.com", 80))
            return True
        except:
            self.is_connected()

    def testa(self, numero_celular, id_sem):
        try:
            self.driver.get(f"https://web.whatsapp.com/send?phone={numero_celular}&source=&data=#")
        except:
            return
        try:
            self.element_presence(By.CSS_SELECTOR, sel.ok, 15)

        except Exception as e:
            try:
                self.element_presence(By.CSS_SELECTOR, sel.campo_msg, 10)
                deletar_sem_whats(numero_celular)
                self.excluidos += 1
            except:
                return self.testa(numero_celular=numero_celular, id_sem=0)

    def teste(self, numero_celular, cpf):

        self.driver.get(f"https://web.whatsapp.com/send?phone={numero_celular}&source=&data=#")
        try:
            self.element_presence(By.CSS_SELECTOR, sel.campo_msg, 10)

        except Exception as e:
            try:
                self.element_presence(By.CSS_SELECTOR, sel.ok, 5)
                inserir_sem_whats(numero_celular)
                self.sem_whats.append(numero_celular)
            except:
                return self.teste(numero_celular, cpf)

    def code(self):
        """ Cria um qrcode a partir dos dados obtidos do campo 'data=ref' """
        try:
            self.element_presence(By.XPATH, '//*[@id="app"]', 5)
            data = self.driver.find_element(By.CSS_SELECTOR, "div[data-ref]").get_attribute("data-ref")
            # self.tmp = tempfile.NamedTemporaryFile(delete=True)
            self.img = make(data)
            self.img.show()
            self.img.save(stream='qrcode.jpg')
            igual = True
            while igual:
                data1 = self.driver.find_element(By.CSS_SELECTOR, "div[data-ref]").get_attribute("data-ref")
                if data == data1:
                    sleep(2)
                else:
                    igual = False


            for proc in psutil.process_iter():
                if proc.name() == "display":
                    proc.kill()
            return self.code()
        except:

            for proc in psutil.process_iter():
                if proc.name() == "display":
                    proc.kill()


    def checar_msg(self):
        self.driver.find_element(By.XPATH,"/html//body/div/div[1]/div[1]/div[4]/div[1]/div[3]/div/div/div[2]/div[5]/div/div/div/div[2]/div/span").click()



