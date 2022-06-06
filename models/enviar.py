import os
import random
import socket
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from qrcode import make
import psutil
from models.utils import *
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import models.Seletores as sel
from selenium.webdriver.chrome.webdriver import *
import pyautogui
import pyperclip

class EnviaMensagem:
    def __init__(self):
        super().__init__()
        self.driver = None
        self.lista_sem_whats = lista_telefones(0)
        self.excluidos = 0
        self.sem_whats = []



    def chama_driver(self, head: bool = True) -> None:
        dir_path = os.getcwd()
        profile = os.path.join(dir_path, "profile", "cobranca")
        options = webdriver.ChromeOptions()
        options.add_argument(
            r"user-data-dir={}".format(profile))
        if head == True:
            options = Options()
            options.add_argument("-headless")
            self.driver = webdriver.Chrome(executable_path="/home/daniel/Documentos/WhatsappAuto/models/chromedriver", options=options)
        else:
            self.driver = webdriver.Chrome(executable_path="/home/daniel/Documentos/WhatsappAuto/models/chromedriver", options=options)

        self.driver.get("https://web.whatsapp.com")

    def fecha_driver(self):
        self.driver.quit()

    def verifica_login(self) -> bool:
        try:
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, sel.desconectar)))
            return True
        except:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "._2UwZ_ > canvas:nth-child(3)")))
                return False
            except Exception as e:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel.nova_conversa)))
                return True

    # def send_whatsapp_msg(self, numero, texto, nome: str, cpf, header: bool = True) -> None:  # Faz a chamada de contato pelo número de telefone.
    #     try:
    #         numero = str(numero)
    #         if len(numero) == 13:
    #             self.driver.get(f"https://web.whatsapp.com/send?phone={numero[0:4]+numero[5:13]}&source=&data=#")
    #         else:
    #             self.driver.get(f"https://web.whatsapp.com/send?phone={numero}&source=&data=#")
    #     except:
    #         return
    #     try:
    #         sleep(0.5)
    #         self.driver.switch_to.alert().accept()
    #     except Exception as e:
    #         pass
    #     # Testa se existe o campo de mensagem na página e envia as mensagens
    #     try:
    #
    #         WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel.campo_msg)))
    #         txt_box = self.driver.find_element(By.CSS_SELECTOR, sel.campo_msg)
    #         nome = nome.capitalize()
    #         if header == True:
    #             txt_box.send_keys(f'Prezado(a) {nome}')
    #             ActionChains(self.driver).key_down(Keys.SHIFT).send_keys(Keys.RETURN).key_up(Keys.SHIFT).perform()
    #         for msg in texto:
    #             txt_box.send_keys(msg)
    #             ActionChains(self.driver).key_down(Keys.SHIFT).send_keys(Keys.RETURN).key_up(Keys.SHIFT).perform()
    #         sleep(.5)
    #         txt_box.send_keys(Keys.RETURN)
    #         sleep(.5)
    #
    #     except Exception as e:
    #         try:
    #             self.element_presence(By.XPATH, '//*[@id="app"]/div[1]/span[2]/div[1]/span[1]/div[1]/div[1]', 5)
    #             self.sem_whats.append(numero)
    #             inserir_sem_whats(numero)
    #         except:
    #             return self.send_whatsapp_msg(numero, texto, nome, cpf)

    # def send_whatsapp_msg(self, numero, texto, nome: str, cpf, header: bool = False) -> None:  # Faz a chamada de contato pelo número de telefone.
    #
    #     try:
    #         try:
    #             WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, sel.pesquisa_contato)))
    #             self.pesquisa_box = self.driver.find_element(By.XPATH, sel.pesquisa_contato)
    #         except:
    #             WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel.campo_pesquisa)))
    #             self.pesquisa_box = self.driver.find_element(By.CSS_SELECTOR, sel.campo_pesquisa)
    #         self.pesquisa_box.clear()
    #         numero = str(numero)
    #         self.pesquisa_box.send_keys(nome)
    #         sleep(random.random()*3 + 2)
    #         # sleep(2)
    #
    #         try:
    #             self.nome_pesquisado = self.driver.find_element(By.XPATH, sel.nome_xpath1)
    #         except:
    #             try:
    #                 self.nome_pesquisado = self.driver.find_element(By.XPATH, sel.nome_xpath)
    #             except:
    #                 try:
    #                     self.nome_pesquisado = self.driver.find_element(By.XPATH, sel.nome_xpath2)
    #                 except:
    #                     print("não encontrado")
    #                     self.sem_whats.append(numero)
    #                     inserir_sem_whats(int(numero))
    #                     return
    #
    #         # sleep(.5)
    #         sleep(random.random()*3+2)
    #
    #         if f'{nome}' in self.nome_pesquisado.text:
    #             self.nome_pesquisado.click()
    #             print('achei')
    #             sleep(.5)
    #         else:
    #             self.nome_pesquisado = None
    #
    #
    #     except Exception as e:
    #         print(e)
    #         return
    #     # Testa se existe o campo de mensagem na página e envia as mensagens
    #     try:
    #
    #         WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel.campo_msg)))
    #         txt_box = self.driver.find_element(By.CSS_SELECTOR, sel.campo_msg)
    #         nome = nome.split()
    #         # nome = nome[0].capitalize()
    #         if header == True:
    #             txt_box.send_keys(f'Prezado(a) Cliente')
    #             ActionChains(self.driver).key_down(Keys.SHIFT).send_keys(Keys.RETURN).key_up(Keys.SHIFT).perform()
    #         for msg in texto:
    #             txt_box.send_keys(msg)
    #             ActionChains(self.driver).key_down(Keys.SHIFT).send_keys(Keys.RETURN).key_up(Keys.SHIFT).perform()
    #         sleep(random.random()*3 + .5)
    #         txt_box.send_keys(Keys.RETURN)
    #         sleep(.5)
    #         deletar_telefone(numero)
    #         deletar_cliente(cpf)
    #         self.nome_pesquisado = None
    #         return
    #
    #     except Exception as e:
    #         print(e)
    #         return

    def send_whatsapp_msg(self, numero, texto, nome: str, cpf, header: bool = False) -> None:  # Faz a chamada de contato pelo número de telefone.
        # try:
        #     numero = str(numero)
        #     if len(numero) == 13:
        #         self.driver.get(f"https://web.whatsapp.com/send?phone={numero[0:4]+numero[5:13]}&source=&data=#")
        #     else:
        #         self.driver.get(f"https://web.whatsapp.com/send?phone={numero}&source=&data=#")
        # except:
        #     return
        # try:
        #     sleep(0.5)
        #     self.driver.switch_to.alert().accept()
        # except Exception as e:
        #     pass

        try:
            try:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, sel.pesquisa_contato)))
                self.pesquisa_box = self.driver.find_element(By.XPATH, sel.pesquisa_contato)
            except:
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel.campo_pesquisa)))
                self.pesquisa_box = self.driver.find_element(By.CSS_SELECTOR, sel.campo_pesquisa)
            self.pesquisa_box.clear()
            numero = str(numero)
            self.pesquisa_box.send_keys(nome)
            sleep(random.random()*3 + 2)
            # sleep(2)

            try:
                self.nome_pesquisado = self.driver.find_element(By.XPATH, sel.nome_xpath1)
            except:
                try:
                    self.nome_pesquisado = self.driver.find_element(By.XPATH, sel.nome_xpath)
                except:
                    try:
                        self.nome_pesquisado = self.driver.find_element(By.XPATH, sel.nome_xpath2)
                    except:
                        print("não encontrado")
                        self.sem_whats.append(numero)
                        inserir_sem_whats(int(numero))
                        return

            # sleep(.5)
            sleep(random.random()*3+2)

            if f'{nome}' in self.nome_pesquisado.text:
                self.nome_pesquisado.click()
                print('achei')
                sleep(.5)
            else:
                self.nome_pesquisado = None


        except Exception as e:
            print(e)
            return
        # Testa se existe o campo de mensagem na página e envia as mensagens
        try:

            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel.botao_clip)))
            botao = self.driver.find_element(By.CSS_SELECTOR, sel.botao_clip)
            botao.click()
            self.driver.find_element(By.CSS_SELECTOR, sel.botao_doc).click()
            sleep(.5)
            sleep(random.random() * 3 + .5)
            pyperclip.copy("/home/daniel/Transferências/Eletrobras/Material_Publicitario Eletrobrás_2.pdf")
            pyautogui.leftClick(x=189, y=593)
            pyautogui.hotkey('ctrl', 'v')
            sleep(random.random() * 3 + .5)
            sleep(1)
            pyautogui.press('enter')
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, sel.botao_enviar)))
            self.driver.find_element(By.CSS_SELECTOR, sel.botao_enviar).click()
            sleep(.5)
            sleep(random.random() * 3 + .5)
            deletar_telefone(numero)
            deletar_cliente(cpf)
            self.nome_pesquisado = None
            return

        except Exception as e:
            print(e)
            return


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
            sleep(0.5)
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

    def testa(self, numero) -> bool:
        try:
            numero = str(numero)
            if len(numero) == 13:
                self.driver.get(f"https://web.whatsapp.com/send?phone={numero[0:4] + numero[5:13]}&source=&data=#")
            else:
                self.driver.get(f"https://web.whatsapp.com/send?phone={numero}&source=&data=#")
        except:
            return
        try:
            sleep(4)
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, sel.ok)))
            sleep(.1)
            return True
        except Exception as e:
            try:
                self.element_presence(By.CSS_SELECTOR, sel.campo_msg, 10)
                deletar_sem_whats(numero)
                self.excluidos += 1
                return False
            except:
                return self.testa(numero=numero)

    def teste(self, numero, cpf):

        numero = str(numero)
        if len(numero) == 13:
            self.driver.get(f"https://web.whatsapp.com/send?phone={numero[0:4] + numero[5:13]}&source=&data=#")
        else:
            self.driver.get(f"https://web.whatsapp.com/send?phone={numero}&source=&data=#")
        try:
            self.element_presence(By.CSS_SELECTOR, sel.campo_msg, 10)

        except Exception as e:
            try:
                self.element_presence(By.CSS_SELECTOR, sel.ok, 5)
                inserir_sem_whats(numero)
                self.sem_whats.append(numero)
            except Exception as e:
                print(e)
                return self.teste(numero, cpf)

    def code(self):
        """ Cria um qrcode a partir dos dados obtidos do campo 'data=ref' """
        try:
            self.element_presence(By.XPATH, '//*[@id="app"]', 5)
            data = self.driver.find_element(By.CSS_SELECTOR, "div[data-ref]").get_attribute("data-ref")
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



