import logging
from time import sleep

from services.consultasipen import ConsultaSipen


class GuardaPenhor(ConsultaSipen):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ConsultaSipen, cls).__new__(cls)
        return cls.instance

    def __init__(self, login, senha, arquivo):
        super().__init__(login, senha, arquivo)
        self.driver = None
        self.matricula = login
        self.senha = senha

    def confirma(self):
        try:
            if self.driver is None:
                self.chama_driver()
            self.login()
            self.driver.execute_script("""
                function
            menuIrPara(url)
            {
                var
            iframe;
            if (url.indexOf("Login.do") != -1) {
            iframe = window.parent.parent.frames["principal"];
            } else {
            iframe = window.frames["iframe01"];
            }
            iframe.location.href = CONTEXT + url;
            }
            menuIrPara('/CarregarConfirmaEntregaGarantiasPVRETPV.do?method=carregar')
            """
                                       )
            sleep(2)
            self.mudar_frame()
            # self.pesquisa_seletor(
            #     "body > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > form > table > tbody > tr:nth-child(1) > td:nth-child(2) > input.ObjForm",
            #     5).send_keys("1631")
            self.driver.execute_script("""function s_Pesquisar(){
                                            document.forms[0].numeroUnidade.value = "1631"
    
                                            document.forms[0].numeroUnidadeOrigem.value = "";
                                            document.forms[0].numeroUnidadeDestino.value = "";
                                            document.forms[0].funcionalidade.value="C";// da funcionalidade Confirma��o de envio de garantias.
                                            document.forms[0].action = CONTEXT+"GarantiasConfirmadaPVRETPV.do?method=carregar&validaSeguranca=VALIDA";
                                            desabilita();
                                            document.forms[0].submit();
                                                }
                                                s_Pesquisar()
            """)
            sleep(1)
            self.driver.execute_script("""function s_Emitir_Relatorio(){
                                                if( document.forms[0].numeroUnidadeOrigem.value == "" ){
                                                    alert("SELECIONE UM ITEM DA LISTA.");
                                                    document.forms[0].numeroUnidadeOrigem.focus();
                                                    return;
                                                }
                                                if( document.forms[0].numeroUnidadeDestino.value == "" ){
                                                    alert("SELECIONE UM ITEM DA LISTA.");
                                                    document.forms[0].numeroUnidadeDestino.focus();
                                                    return;
                                                }
                                            
                                                document.forms[0].nomeUnidadeOrigem.value=getSelectedText(document.forms[0].numeroUnidadeOrigem);
                                                document.forms[0].nomeUnidadeDestino.value=getSelectedText(document.forms[0].numeroUnidadeDestino);
                                                desabilita();
                                                document.forms[0].funcionalidade.value="R";// da funcionalidade Confirma��o de envio de garantias.
                                                document.forms[0].tipoConsulta.value="A";
                                                document.forms[0].action = CONTEXT+"ConfirmarEntregaGarantias.do?method=carregar&validaSeguranca=VALIDA";
                                                document.forms[0].target = "principal";
                                                document.forms[0].submit();
                                            }
                                            s_Emitir_Relatorio()
                                            """)
            try:
                sleep(5)
                self.driver.switch_to.alert.accept()
                self.driver.close()
                return True
            except Exception:
                self.driver.switch_to.default_content()
                self.driver.switch_to.frame("principal")
                self.pesquisa_seletor("#btnConfirmar", 5).click()
                sleep(1)
                alerta = self.driver.switch_to.alert.text
                self.driver.switch_to.alert.accept()
                if "sucesso" in alerta:
                    self.pesquisa_seletor("#botaoImprimir > table > tbody > tr > td > input", 5).click()
                    sleep(2)
                    return True
        except Exception:
            logging.basicConfig(filename='erro.log', level=logging.ERROR)

            return False

    def envia(self):
        try:
            if self.driver is None:
                self.chama_driver()
            self.login()
            self.driver.execute_script("""
                function
            menuIrPara(url)
            {
                var
            iframe;
            if (url.indexOf("Login.do") != -1) {
            iframe = window.parent.parent.frames["principal"];
            } else {
            iframe = window.frames["iframe01"];
            }
            iframe.location.href = CONTEXT + url;
            }
            menuIrPara('/CarregarMovimentacaoPVRETPV.do?method=carregar')
            """
                                       )
            try:
                sleep(3)
                self.driver.switch_to.alert.accept()
                return True
            except:
                self.driver.switch_to.default_content()
                self.mudar_frame()
                self.driver.execute_script("""function s_Confirmar(){
                                                updateString();
                                            
                                                if (document.forms[0].stringContratos.value.length >0) {
                                                    var acao = "EfetuarFechamento.do?validaSeguranca=VALIDA&method=carregar";	
                                                    updateString();
                                                    document.forms[0].action = acao;
                                                    document.forms[0].target = "principal";
                                                    document.forms[0].submit();
                                                } else {
                                                    alert("1rio enviar pelo menos um item.");
                                                }
                                            }
                                            s_Confirmar()
                                            """)
                sleep(3)
                alerta = self.driver.switch_to.alert.text
                self.driver.switch_to.alert.accept()
                if "SUCESSO" in alerta:
                    self.mudar_frame()
                    self.pesquisa_seletor("#botaoImprimir > table > tbody > tr > td > img", 10).click()
                    sleep(5)
                    return True

        except Exception as e:
            print(e)
            return False
            # self.driver.close()
