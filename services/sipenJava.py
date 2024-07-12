def menuIrpara(driver, url):
    driver.execute_script("""function menuIrPara(url)
                    {var iframe;
                    if (url.indexOf("Login.do") != -1) {
                    iframe = window.parent.parent.frames["principal"];
                    } else {
                    iframe = window.frames["iframe01"];
                    }
                    iframe.location.href = CONTEXT + url;
                    }""" +  f"menuIrPara({url})")


def irParaRenovacao(driver):
    driver.execute_script("""function menuIrPara(url)
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
                menuIrPara('/RenovarContratoLote.do?method=carregar')
                """
                          )


def renovacao(driver, cpf):
    driver.execute_script(f"""
                document.forms.renovarContratoLoteForm.numeroCPFCNPJ.value = {cpf}
                document.forms[0].target = 'principal';
                document.forms[0].action = CONTEXT + 'RenovarContratoLote.do?method=validar';
                document.forms[0].submit();

    """)

# Guarda Penhor
def confirmarEnvio(driver):
    """
    function s_Confirmar(){
	updateString();

	if (document.forms[0].stringContratos.value.length >0) {
		var acao = "EfetuarFechamento.do?validaSeguranca=VALIDA&method=carregar";
		updateString();
		document.forms[0].action = acao;
		document.forms[0].target = "principal";
		document.forms[0].submit();
	} else {
		alert("É necessário enviar pelo menos um item.");
	}
}
s_Confirmar()
    """