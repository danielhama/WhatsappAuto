import os
import tempfile
import pathlib
from time import sleep
import pyautogui as pa
import holidays
from selenium import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.firefox.webdriver import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

import models.SeletoresRelatorios as s
from models.Seletores import data_inventario, usuario, contratos_ativos, confirma_inventario, cpf_selector, \
    situacao, modalidade, vencimento_seletor, vencimento_seletor2
from models.utils import *
import datetime



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
        self._logger_configure()


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

    def _logger_configure(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

        LOG_DIR = os.path.join(BASE_DIR, "logs")

        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)

        log_filename = os.path.join(
            LOG_DIR,
            datetime.datetime.now().strftime("%Y-%m-%d.log")
        )

        self.logger = logging.getLogger("chamafila")
        self.logger.setLevel(logging.INFO)

        # evita duplicação de handlers
        if not self.logger.handlers:
            formatter = logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s"
            )

            # arquivo
            file_handler = logging.FileHandler(
                log_filename, encoding="utf-8"
            )
            file_handler.setFormatter(formatter)

            # terminal
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

        self.logger.info("=" * 60)
        self.logger.info("Iniciando Sipen")
        self.logger.info("=" * 60)

    # @threaded
    def chama_driver(self, head: bool = True) -> None:
        options = webdriver.FirefoxOptions()
        profile_dir = r"C:\Users\c084029\PycharmProjects\WhatsappAuto\profile\firefox"
        MIME_TYPES = ",".join([
            "application/vnd.ms-excel",
            "application/msexcel",
            "application/x-msexcel",
            "application/x-ms-excel",
            "application/x-excel",
            "application/x-dos_ms_excel",
            "application/xls",
            "application/x-xls",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ])

        prefs = {
            "browser.download.folderList": 2,
            "browser.download.dir": "downloaddir",
            "browser.download.useDownloadDir": True,
            "browser.download.viewableInternally.enabledTypes": "",
            "browser.download.manager.useWindow": False,
            "browser.download.manager.showWhenStarting": False,
            "browser.download.manager.closeWhenDone": True,
            "browser.download.panel.shown": False,
            "browser.helperApps.alwaysAsk.force": False,
            "browser.helperApps.neverAsk.openFile": MIME_TYPES,
            "browser.helperApps.neverAsk.saveToDisk": MIME_TYPES,
        }

        # Grava user.js manualmente no disco
        user_js_path = os.path.join(profile_dir, "user.js")
        with open(user_js_path, "w") as f:
            for key, value in prefs.items():
                if isinstance(value, bool):
                    f.write(f'user_pref("{key}", {"true" if value else "false"});\n')
                elif isinstance(value, int):
                    f.write(f'user_pref("{key}", {value});\n')
                else:
                    f.write(f'user_pref("{key}", "{value}");\n')

        options.add_argument("-profile")
        options.add_argument(profile_dir)

        if not head:
            options.add_argument("-headless")

        self.driver = webdriver.Firefox(
            service=Service(
            executable_path=r"C:\Users\c084029\.wdm\drivers\chromedriver\win64\129.0.6668.71\chromedriver-win32\geckodriver.exe",
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
            sleep(.5)
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
        sleep(0.5)
        # self.driver.find_element(By.CSS_SELECTOR, "#btnExportar").click()
        # sleep(3)
        # pa.press('enter')
        # sleep(1)
        # 1. Intercepta a URL que o botão geraria
        url_download = self.driver.execute_script("""
            // Sobrescreve o window.open temporariamente para capturar a URL
            var captured_url = null;
            var original_open = window.open;
            window.open = function(url) { captured_url = url; };

            // Dispara o clique normalmente
            document.querySelector('#btnExportar').click();

            // Restaura o window.open original
            window.open = original_open;

            return captured_url;
        """)

        sleep(1)
        url_base = "https://sipen.caixa"
        url_download = url_base + url_download


        # 2. Navega direto na URL — sem nova janela, sem diálogo
        self.driver.get(url_download)
        timeout = 15
        start = datetime.time()
        while datetime.time() - start < timeout:
            # Tenta localizar o botão "Salvar arquivo" na tela
            btn = pa.locateOnScreen('salvar_btn.png', confidence=0.8)
            if btn:
                pa.click(btn)
                break
            sleep(0.5)
        else:
            # Fallback: só pressiona Enter (botão padrão já é Salvar)
            pa.press('enter')

        sleep(3)

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
        while dl_wait and seconds < 30:
            sleep(1)
            dl_wait = False
            for fname in os.listdir(r"C:\Users\c084029\Downloads"):
                if fname.endswith('.crdownload'):
                    dl_wait = True
                    sleep(1)
            seconds += 1
        return False

    def abre_inventario(self):
        try:
            self.inventario_path = pathlib.Path(r"C:\Users\c084029\Downloads\RelatorioInventarioGeralContrato.xls")
            data = datetime.datetime.fromtimestamp(self.inventario_path.stat().st_atime)
            data = datetime.date(year=data.year,
                                 month=data.month,
                                 day=data.day)
            hoje = datetime.datetime.today()
            hoje = datetime.date(year=hoje.year,
                                 month=hoje.month,
                                 day=hoje.day)
            if data == hoje:
                return True
            else:
                return False
        except FileNotFoundError:
            return False

    def atualizar(self, forcar=False):
        while self.driver is None:
            sleep(1)

        try:
            if self.driver.find_element(By.CSS_SELECTOR, s.menu) is not None: 
                self.login() 
        except:
            self.login()
        inventarioDF = pd.read_excel(self.inventario_path,
                                     header=3, engine='xlrd')
        hoje = datetime.datetime.today()
        hoje = datetime.datetime(year=hoje.year,
                                 month=hoje.month,
                                 day=hoje.day)
        for idx, i in inventarioDF.iterrows():
            print(f"Iniciando pesquisa para Contrato {i['Nr. Contrato']}")
            i['Nr. Contrato'] = i['Nr. Contrato'].replace(".", "").replace("-", "")
            data_anterior = pesquisa_data_atualizacao(i['Nr. Contrato'])
            if data_anterior is not None:
                data_anterior = datetime.datetime.strptime(data_anterior.split(" ")[0], "%Y-%m-%d")
                if not forcar:
                    if data_anterior == hoje:
                        continue
            # WebDriverWait(driver, 10).until(ec.invisibility_of_element_located((By.CSS_SELECTOR, usuario)))
            try:
                self.situacao(numero=i['Nr. Contrato'],
                              vencimento=i['Vencimento'],
                              valor_avaliacao=i['Avaliação'],
                              valor_emprestimo=i['Empréstimo'],
                              emissao=i['Emissão'],
                              prazo=i['Prz.'])
            except Exception as e:
                self.login()
                try:
                    self.situacao(numero=i['Nr. Contrato'],
                                  vencimento=i['Vencimento'],
                                  valor_avaliacao=i['Avaliação'],
                                  valor_emprestimo=i['Empréstimo'],
                                  emissao=i['Emissão'],
                                  prazo=i['Prz.'])
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
        vencimento = self.pesquisa_seletor(vencimento_seletor, 5).text
        # vencimento = datetime.datetime.strptime(vencimento, '%d/%m/%Y')
        if "R$" in vencimento:
            vencimento = self.pesquisa_seletor(
                selector=vencimento_seletor2,
                tempo=5
            ).text
        try:
            vencimento = datetime.datetime.strptime(vencimento, '%d/%m/%Y')
        except:
            vencimento = datetime.datetime.today()

        emissao = datetime.datetime.strptime(emissao, '%d/%m/%Y')
        try:
            inserir_contrato(numero=numero,
                             emissao=emissao,
                             vencimento=vencimento,
                             valor_emprestimo=valor_emprestimo,
                             valor_avaliacao=valor_avaliacao,
                             situacao=_situacao,
                             prazo=prazo,
                             cpf=cpf,
                             data=datetime.datetime.today(),
                             modalidade=_modalidade)
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
    data = datetime.date(year=data.year,
                         month=data.month,
                         day=data.day)

    if data in holidays.country_holidays(country='Brazil',
                                         years=hoje.year).keys():
        if hoje.weekday() == 0:
            data = hoje + datetime.timedelta(days=-3)
        else:
            data = hoje + datetime.timedelta(days=-1)
        return data
    else:
        return data
