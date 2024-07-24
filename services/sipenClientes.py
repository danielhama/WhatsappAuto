from models.sipen import Sipen


class SipenClientes(Sipen):

    def __init__(self, login, senha):
        super().__init__(login, senha)
        self.cadastro = '/CarregarManterPesquisaCliente.do?method=carregar&menuOrigem=incluirAvaliacaoBens'
    def acessar_cliente(self):
        self.chama_driver()
        self.login()
        self.driver.get(self.sipen + self.cadastro)
        self.driver.find_element(By.CSS_SELECTOR, "#idNumeroContratoCPF").send_keys("85717312920")


inst = SipenClientes('c084029', 'Iris1346')
inst.acessar_cliente()