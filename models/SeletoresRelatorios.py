# Seletores
cliente = "body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(1) > td > form > table:nth-child(62) > tbody > tr:nth-child(3) > td:nth-child(2)"
data_vencimento = "body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(1) > td > form > table:nth-child(62) > tbody > tr:nth-child(11) > td:nth-child(2)"
availiacao = "body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(1) > td > form > table:nth-child(62) > tbody > tr:nth-child(8) > td:nth-child(2)"
emprestimo = "body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(1) > td > form > table:nth-child(62) > tbody > tr:nth-child(9) > td:nth-child(2)"
avaliador = "body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(1) > td > form > table:nth-child(62) > tbody > tr:nth-child(22) > td:nth-child(2)"
situacao = "body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(1) > td > form > table:nth-child(62) > tbody > tr:nth-child(5) > td:nth-child(2)"
usuario = "#Layer1 > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > input:nth-child(1)"
#Renovação
cpf_renovacao = "#numeroCPFCNPJ"
botao_pesquisar = "body > form > table:nth-child(5) > tbody > tr > td > input"
todos = "#tipoPesquisa > option:nth-child(1)"
vencidos = "#tipoPesquisa > option:nth-child(2)"
licitacao = "#tipoPesquisa > option:nth-child(3)"
contrato = "body > form > table:nth-child(43) > tbody > tr:nth-child(2) > td > div > table:nth-child(2) > tbody > tr:nth-child(1) > td:nth-child(2)"
renovacao_contrato ="https://sipen.caixa/sipen/CarregarPenhorContrato.do?method=carregar&validaSeguranca=VALIDA&numeroContrato="
# Renovação em Lote
botao_pesquisar_situacao = "body > form:nth-child(6) > table:nth-child(32) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(3) > input:nth-child(1)"
botao_calcular = "#btnCalcular"
numero_contrato = "table.TabelaPadrao:nth-child(35) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2)"
valor_renovacao = "#spnValorLiquidoRenovacao-"
# Relatorio emprestimo
data_ref = "#dataReferencia" ##dataReferencia
tabela = "body > form > table:nth-child(12)"
tabela_micro = "body > form > table:nth-child(13)"
#sipen
senha = "#Layer1 > table > tbody > tr:nth-child(4) > td > table > tbody > tr > td:nth-child(1) > input[type=password]:nth-child(1)"
login = "#Layer1 > table > tbody > tr:nth-child(2) > td > input[type=text]"
botao = "#Layer1 > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(4) > td:nth-child(1) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > a:nth-child(1)"
menu = "body > table > tbody > tr:nth-child(1) > td > table > tbody > tr > td:nth-child(1) > button"
botao_login = "#Layer1 > table > tbody > tr:nth-child(4) > td > table > tbody > tr > td:nth-child(2) > a"
#liquidados
tabela_liquidado = "body > form > table:nth-child(16)"
numero_paginas = "#totalPaginas"
pagina = "body > form > div.pagination > ul > li:nth-child(4) > a"
paginacao = "body > form > div.pagination" #self.driver.find_element(By.CLASS_NAME, "pagination")
#document.querySelector("body > form > div.pagination > ul > li:nth-child(5) > a")
proxima = "body > form > div.pagination > ul > li:nth-child(5) > a"

# menu = "body > table > tbody > tr:nth-child(1) > td > table > tbody > tr > td:nth-child(1) > button"
manutencao_penhor = "#NavegacaoPrincipal > div:nth-child(4) > div.panel-heading > h4"
menu_relatorios = "#NavegacaoPrincipal > div:nth-child(7) > div.panel-heading > h4"
menu_renovados = "#menu7 > div > ul > li:nth-child(3) > ul > li:nth-child(3) > a"
menu_novos = "#menu7 > div > ul > li:nth-child(3) > ul > li:nth-child(1) > a"
menu_liquidados = "#menu7 > div > ul > li:nth-child(3) > ul > li:nth-child(2) > a"
menu_licitacao = "#NavegacaoPrincipal > div:nth-child(9) > div.panel-heading"
menu_apuracao = "#menu9 > div > ul > li:nth-child(4) > ul > li:nth-child(1) > a"

#Renovados
tabela_novos = "body > form > table:nth-child(10)"
voltar = "body > form > table:nth-child(8) > tbody > tr:nth-child(1) > td:nth-child(2) > a"
voltar_novos = "body > form > table:nth-child(5) > tbody > tr:nth-child(1) > td:nth-child(2) > a"
# body > form > table:nth-child(13) body > form > table:nth-child(12)
tabela_renovado = "body > form > table:nth-child(11)"
voltar_liquidados = "#botaoVoltar > table > tbody > tr:nth-child(1) > td:nth-child(2) > a"

tabela_outras_agencias = "body > form > div:nth-child(12) > table:nth-child(3)" #body > form > div:nth-child(12) > table:nth-child(3) / body > form > div:nth-child(12) > div > table:nth-child(3) / body > form > div:nth-child(12) > table:nth-child(3)
tabela_renovacao = "body > form > table:nth-child(11)" #body > form > table:nth-child(11) # body > form > table:nth-child(11)

#body > form > div:nth-child(12) > div > table:nth-child(3)
#body > form > div:nth-child(12) > table:nth-child(3)
#body > form > div:nth-child(12) > div > div > table:nth-child(3)
#body > form > div:nth-child(12) > div > div > div > table:nth-child(3)


# Seletores
quantidade_renovacoes = "body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(1) > td > form > table:nth-child(62) > tbody > tr:nth-child(7) > td:nth-child(4)"
data_atualizacao = "body > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(1) > td > form > table:nth-child(62) > tbody > tr:nth-child(2) > td:nth-child(2)"
data_licitacao = "body > table > tbody > tr:nth-child(2) > td > form > table:nth-child(4) > tbody > tr > td > table > tbody > tr.FonteSubTituloTabela > td:nth-child(1) > input[type=text]"
centralizadora = "#numeroAgencia-comboeditavel-input"
por_lote = "#opcaoPor" #Value 2
confirmar = "#botaoConfirmarLink"

#Guarda Penhor
confirmar_envio = "#botaoImprimir > table > tbody > tr > td:nth-child(1) > a > img"
imprimir_envio = "#botaoImprimir > table > tbody > tr > td > img"
javascript_envio = "menuIrPara('/CarregarMovimentacaoPVRETPV.do?method=carregar')"
javascript ="menuIrPara('/CarregarConfirmaEntregaGarantiasPVRETPV.do?method=carregar')"
confirmar_recebimento = "https://sipen.caixa/sipen/jsp/Comuns/Principal.jsp?destino=//sipen/CarregarMovimentacaoPVRETPV.do?method=carregar&validaSeguranca=VALIDA#"
enviar_garantias = "https://sipen.caixa/sipen/jsp/Comuns/Principal.jsp?destino=//sipen/CarregarMovimentacaoPVRETPV.do?method=carregar&validaSeguranca=VALIDA"
