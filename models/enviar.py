import os
import random
import socket
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from models.utils import *
from models.ferramentas import threaded
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import models.Seletores as sel
from selenium.webdriver.chrome.webdriver import *
import undetected_chromedriver as uc



class EnviaMensagem:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(EnviaMensagem, cls).__new__(cls)
        return cls.instance


    def __init__(self):
        super().__init__()
        self.driver = None
        self.lista_sem_whats = lista_Telefones(0)
        self.excluidos = 0
        self.sem_whats = []


    @threaded
    def chama_driver(self, head: bool = True) -> None:

        profile = os.path.join(r'C:\Users\c084029\PycharmProjects\WhatsappAuto', "profile", "wpp")
        options = uc.ChromeOptions()
        options.user_data_dir = profile
        options.headless = False

        options.browser_version = "107"
        if head == True:
            options = Options()
            options.add_argument("-headless")
            self.driver = uc.Chrome(driver_executable_path=r"C:\Users\c084029\Downloads\chromedriver_win32\chromedriver.exe", options=options)

                # service=ChromeService(ChromeDriverManager().install()), options=options)
        else:
            self.driver = uc.Chrome(driver_executable_path=r"C:\Users\c084029\Downloads\chromedriver_win32\chromedriver.exe", options=options)
            # self.driver = webdriver.Chrome(executable_path=r"C:\Users\c084029\Downloads\chromedriver_win32\chromedriver.exe", options=options)

                # service=ChromeService(ChromeDriverManager(driver_version="107.0.5304.62").install()), options=options)
        self.driver.execute_script("document.body.style.zoom='90 %'")
        self.driver.maximize_window()
        self.driver.get("https://web.whatsapp.com")


    def fecha_driver(self):
        try:
            self.driver.quit()
        except:
            pass
    def verifica_login(self) -> bool:
        try:
            WebDriverWait(self.driver, 3).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, sel.desconectar)))
            return True
        except:
            try:
                WebDriverWait(self.driver, 2).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "._2UwZ_ > canvas:nth-child(3)")))
                return False
            except Exception as e:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel.nova_conversa)))
                return True

    def pesquisa_seletor(self, selector: str, tempo: int):
        return WebDriverWait(self.driver, tempo).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))

    def clica_campo(self, selector: str):
        try:
            self.driver.find_element(By.CSS_SELECTOR, selector).click()
        except:
            pass

    async def send_whatsapp_msg(self, numero, texto, nome: str, cpf, header: bool = True) -> bool:  # Faz a chamada de contato pelo número de telefone.
        # if self.verifica_login():
        try:
            try:
                self.pesquisa_box = self.pesquisa_seletor(sel.campo_pesquisa, 20)
            except:
                print("Seletor de campo de pesquisa não encontrado")
            self.clica_campo(sel.apagar_pesquisa)
            self.pesquisa_box.send_keys(str(numero)[-8::])
            sleep(random.random()*3 + 1)

            try:
                self.nome_pesquisado = self.pesquisa_seletor(sel.nome_CSS, 5)
            except:
                print("não encontrado")
                self.sem_whats.append(numero)
                id = pesquisa_id(cpf)
                inserir_sem_whats(numero[2::])
                deletar_enviado(id)
                return False

            sleep(random.random()*3+1)

            if nome in self.nome_pesquisado.text.split(',')[0]:
                self.nome_pesquisado.click()
                print('achei')
            else:
                print(f"Nome pesquisado {self.nome_pesquisado.text.split(',')[0]}")
                self.nome_pesquisado = None
                print("Nome divergente do cadastro")
                print(f"Nome de Envio {nome}")
                # deletar_enviado(numero)
                return False

        except Exception as e:
            print(e)
        try:
            bloqueado = self.pesquisa_seletor(sel.bloqueado, 2)
            if "bloqueado" in bloqueado.text:
                print(bloqueado.text)
                inserir_sem_whats(numero[2::])
                return False
        except:
            pass

        selecionado = self.driver.find_element(By.CSS_SELECTOR, sel.barra_superior).text.split(',')[0]
        if selecionado == nome:
            nome = nome.split()
            nome = nome[0].capitalize()
            self.txt_box = self.pesquisa_seletor(sel.campo_msg, 5)
            if header == True:
                self.txt_box.send_keys(f'Prezado(a) {nome}')
                ActionChains(self.driver).key_down(Keys.SHIFT).send_keys(Keys.RETURN).key_up(Keys.SHIFT).perform()
            for msg in texto:
                self.txt_box.send_keys(msg)
                ActionChains(self.driver).key_down(Keys.SHIFT).send_keys(Keys.RETURN).key_up(Keys.SHIFT).perform()
            sleep(random.random()*3 + .5)
            self.txt_box.send_keys(Keys.RETURN)
            id = pesquisa_id(cpf)
            deletar_enviado(id)
            return True
        else:
            return False

        # except Exception as e:
        #     return False
    # else:
    #     return False

    def send_whatsapp_msg_valor(self, numero, texto) -> None:  # Faz a chamada de contato pelo número de telefone.
        try:
            numero = str(numero)
            if len(numero) == 13:
                self.driver.get(f"https://web.whatsapp.com/send?phone={numero[0:4]+numero[5:13]}&source=&data=#")
            else:
                self.driver.get(f"https://web.whatsapp.com/send?phone={numero}&source=&data=#")
        except:
            return
        try:
            sleep(3)
            self.driver.switch_to.alert().accept()
        except Exception as e:
            pass
        # Testa se existe o campo de mensagem na página e envia as mensagens
        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel.campo_msg)))
            txt_box = self.driver.find_element(By.CSS_SELECTOR, sel.campo_msg)
            ActionChains(self.driver).key_down(Keys.SHIFT).send_keys(Keys.RETURN).key_up(Keys.SHIFT).perform()
            for msg in texto:
                txt_box.send_keys(msg)
                ActionChains(self.driver).key_down(Keys.SHIFT).send_keys(Keys.RETURN).key_up(Keys.SHIFT).perform()
            sleep(.5)
            sleep(random.random())
            # txt_box.send_keys(Keys.RETURN)
            sleep(1)
            sleep(random.random())
            sleep(random.random())
            sleep(random.random())
            self.pesquisa_box.clear()
            return


        except Exception as e:
            pass

    def element_presence(self, by, xpath, time):  # Define espera para a presença de determinado elemento
        element_present = EC.presence_of_element_located((by, xpath))
        WebDriverWait(self.driver, time).until(element_present)

    def element_not_presence(self, by, id, time):  # Defina espera para a não presença de determinado elemento
        element_not_present = EC.invisibility_of_element_located((by, id))
        WebDriverWait(self.driver, time).until(element_not_present)

    def is_connected(self):  # Testa se existe conexão

        try:
            socket.create_connection(("www.google.com", 80))
            return True
        except:
            self.is_connected()

    async def testa(self, numero) -> bool:
        try:
            if len(numero['Telefones']) == 11:
                self.driver.get(f"https://web.whatsapp.com/send?phone={'55' + numero['Telefones'][0:2] + numero['Telefones'][3::]}&source=&data=#")
            else:
                self.driver.get(f"https://web.whatsapp.com/send?phone={'55' + numero['Telefones']}&source=&data=#")
        except:
            return False
        try:
            sleep(4)
            # WebDriverWait(self.driver, 10).until(
            #     EC.visibility_of_element_located((By.CSS_SELECTOR, sel.ok)))
            self.pesquisa_seletor(sel.ok, 10).click()
            sleep(.1)
            inserir_sem_whats(numero['Telefones'][2::])
            return True
        except Exception as e:
            try:
                self.element_presence(By.CSS_SELECTOR, sel.campo_msg, 10)
                deletar_sem_whats(numero['Telefones'][2::])
                self.excluidos += 1
                return False
            except:
                return self.testa(numero)

    async def teste(self, numero, cpf):

        numero = str(numero)
        if len(numero) == 13:
            self.driver.get(f"https://web.whatsapp.com/send?phone={numero[0:4] + numero[5:13]}&source=&data=#")
        else:
            self.driver.get(f"https://web.whatsapp.com/send?phone={numero}&source=&data=#")
        try:
            self.element_presence(By.CSS_SELECTOR, sel.campo_msg, 10)
            return True

        except Exception as e:
            try:
                self.element_presence(By.CSS_SELECTOR, sel.ok, 5)
                inserir_sem_whats(numero)
                self.sem_whats.append(numero)
                return False
            except Exception as e:
                print(e)
                return self.teste(numero, cpf)

    # def code(self):
    #     """ Cria um qrcode a partir dos dados obtidos do campo 'data=ref' """
    #     try:
    #         self.element_presence(By.XPATH, '//*[@id="app"]', 5)
    #         data = self.driver.find_element(By.CSS_SELECTOR, "div[data-ref]").get_attribute("data-ref")
    #         self.img = make(data)
    #         self.img.show()
    #         self.img.save(stream='qrcode.jpg')
    #         igual = True
    #         while igual:
    #             data1 = self.driver.find_element(By.CSS_SELECTOR, "div[data-ref]").get_attribute("data-ref")
    #             if data == data1:
    #                 sleep(2)
    #             else:
    #                 igual = False

        #
        #     for proc in psutil.process_iter():
        #         if proc.name() == "display":
        #             proc.kill()
        #     return self.code()
        # except:
        #
        #     for proc in psutil.process_iter():
        #         if proc.name() == "display":
        #             proc.kill()


    def checar_msg(self):
        self.driver.find_element(By.XPATH,"/html//body/div/div[1]/div[1]/div[4]/div[1]/div[3]/div/div/div[2]/div[5]/div/div/div/div[2]/div/span").click()


    def read_last_in_message(self):
        """
        Reading the last message that you got in from the chatter
        """
        message = ""
        emojis = []
        for messages in self.driver.find_elements_by_xpath(
                "//div[contains(@class,'message-in')]"):
            try:

                message_container = messages.find_element_by_xpath(
                    ".//div[@class='copyable-text']")

                message = message_container.find_element_by_xpath(
                    ".//span[contains(@class,'copyable-text')]"
                ).text

                for emoji in message_container.find_elements_by_xpath(
                        ".//img[contains(@class,'copyable-text')]"
                ):
                    emojis.append(emoji.get_attribute("data-plain-text"))

            except Exception as e:  # In case there are only emojis in the message
                try:
                    message = ""
                    emojis = []
                    message_container = messages.find_element_by_xpath(
                        ".//div[contains(@class,'copyable-text')]")

                    for emoji in message_container.find_elements_by_xpath(
                            ".//img[contains(@class,'copyable-text')]"
                    ):
                        emojis.append(emoji.get_attribute("data-plain-text"))
                except Exception:
                    pass

        return message, emojis

