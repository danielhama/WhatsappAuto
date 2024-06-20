function s_Confirmar(){
	updateString();

	if (document.forms[0].stringContratos.value.length >0) {
		var acao = "EfetuarFechamento.do?validaSeguranca=VALIDA&method=carregar";
		updateString();
		document.forms[0].action = acao;
		document.forms[0].target = "principal";
		document.forms[0].submit();
	} else {
		alert("\u00C9 necess\u00E1rio enviar pelo menos um item.");
	}
}

function login(){
    if(!verifica_branco(document.forms[0].usuario.value)){
        alert("CAMPO DE PREENCHIMENTO OBRIGAT\u00D3RIO.");
        document.forms[0].usuario.focus();
        return;
    }
    else if(!verifica_branco(document.forms[0].senha.value)){
        alert("CAMPO DE PREENCHIMENTO OBRIGAT\u00D3RIO.");
        document.forms[0].senha.focus();
        return;
    }else{
        document.forms[0].submit();
    }
}

function sVoltarMenuPrincipal()
{
    document.forms[0].target = "principal";
    document.forms[0].action =CONTEXT + "jsp/Comuns/Principal.jsp";
    document.forms[0].submit();
}
function f_bValidaContrato(sContrato) {
	if (sContrato == "")
		return true;
	sContrato = sContrato.replace(".", "");
	sContrato = sContrato.replace(".", "");
	sContrato = sContrato.replace("-", "");

	unid = sContrato.substring(0, 4);
	prod = sContrato.substring(4, 7);
	seq = sContrato.substring(7, 15);
	digito = sContrato.substring(15, sContrato.length);

	if (unid == "0000") {
		return false;
	}

	if (prod == "000") {
		return false;
	}

	d1 = 0;
	for (i = 0; i < 4; i++)
		d1 += parseInt(unid.charAt(i)) * (8 - i);

	d2 = 0;
	for (i = 0; i < 3; i++)
		d2 += parseInt(prod.charAt(i)) * (4 - i);

	d3 = 0;
	for (i = 0; i < 8; i++)
		d3 += parseInt(seq.charAt(i)) * (9 - i);

	resultado = ((parseInt(d1) + parseInt(d2) + parseInt(d3)) * 10) % 11;

	if (resultado == NaN) {
		return false;
	}
	/*
	 * 1.1. Caso o resto da divisï¿½o seja igual a 10 (dez) ou 0(zeros), o dï¿½gito
	 * verificador serï¿½ 0(zero); caso contrï¿½rio o resto serï¿½ o DV (Dï¿½gito
	 * Verificador):
	 */

	if (resultado == 10 || resultado == 0) {
		if (digito != 0) {
			return false;
		}
	} else {
		if (digito != resultado) {
			return false;
		}
	}

	return true;
}
function menuIrPara(url) {
    var iframe;
    if (url.indexOf("Login.do") != -1) {
        iframe = window.parent.parent.frames["principal"];
    } else {
        iframe = window.frames["iframe01"];
    }
    iframe.location.href = CONTEXT + url;
}

function windowLoad(numUnidOrigem){
	//if ("<%=enviarGarantiasSolicitadasForm.getNumeroUnidadeOrigem().trim()%>" != "") {
	if (numUnidOrigem != ""){
		document.forms[0].numeroUnidadeOrigem.value = numUnidOrigem;
	}
}
function s_Voltar(){
	document.forms[0].action =CONTEXT+"jsp/Comuns/Branco.jsp";
	document.forms[0].submit();
}

function s_Emitir_Relatorio(){
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

function s_Pesquisar(){

	if( document.forms[0].numeroUnidade.value == "" ){
		alert("CAMPO DE PREENCHIMENTO OBRIGAT\u00D3RIO.");
		document.forms[0].numeroUnidade.focus();
		return;
	}
	document.forms[0].numeroUnidadeOrigem.value = "";
	document.forms[0].numeroUnidadeDestino.value = "";
	document.forms[0].funcionalidade.value="C";// da funcionalidade Confirma��o de envio de garantias.
	document.forms[0].action = CONTEXT+"GarantiasConfirmadaPVRETPV.do?method=carregar&validaSeguranca=VALIDA";
	desabilita();
	document.forms[0].submit();

}

function s_PesquisaUnidadeDestino(){
	document.forms[0].action = CONTEXT+"CarregarEnviarGarantiasSolicitadas.do?method=carregar&validaSeguranca=VALIDA";
	desabilita();
	document.forms[0].submit();

}

function mudaImagem( obj ){
	obj.src = CONTEXT+"imagem/bt_relatorio_off.gif";
}

function voltaImagem( obj ){
	obj.src = CONTEXT+"imagem/bt_relatorio_on.gif";
}

function mudaImagemPesquisa( obj ){
	obj.src = CONTEXT+"imagem/btn_pesquisar_pressionado.gif";
}

function voltaImagemPesquisa( obj ){
	obj.src = CONTEXT+"imagem/btn_pesquisar_ativo.gif";
}

function habilita() {
	document.getElementById('botaoHabilitado').style.display = "";
	document.getElementById('botaoDesabilitado').style.display = "none";
}
function desabilita() {
	document.getElementById('botaoHabilitado').style.display = "none";
	document.getElementById('botaoDesabilitado').style.display = "";
}

function f_TeclaPesquisa(){
	if (f_GetLetra(fnEvent(),false) == 13){
		s_Pesquisar();
		return false;
	}
	return true;
}


		function atualizarValoresGarantia(valorAvaliacao, valorSeguro, checked) {
			var clazz = "calcularValorTotalConfirmaRecebimentoGarantiaAjaxImpl";

			var valor_total_avaliacao = document.getElementById('valor_total_avaliacao').innerHTML;
			var valor_total_seguro = document.getElementById('valor_total_seguro').innerHTML;
			var quantidade_total_garantias = document.getElementById('quantidade_total_garantias').innerHTML;

			var param = "&valorTotalAvaliacao=" + valor_total_avaliacao;
			param += "&valorTotalSeguro=" + valor_total_seguro;
			param += "&quantidadeTotalGarantias=" + quantidade_total_garantias;
			param += "&valorAvaliacao=" + valorAvaliacao;
			param += "&valorSeguro=" + valorSeguro;
			param += "&checked=" + checked;
			requestAjax(clazz, param);
		}

		function callback(response) {
			if (response != null) {
				var jsonObject = null;
				try {
					jsonObject = eval("(" + response + ")");
				} catch (e) {

				}

				var valorTotalAvaliacao = jsonObject['valorTotalAvaliacao'];
				var valorTotalSeguro = jsonObject['valorTotalSeguro'];
				var quantidadeTotalGarantias = jsonObject['quantidadeTotalGarantias'];

				document.getElementById('valor_total_avaliacao').innerHTML = valorTotalAvaliacao;
				document.getElementById('valor_total_seguro').innerHTML = valorTotalSeguro;
				document.getElementById('quantidade_total_garantias').innerHTML = quantidadeTotalGarantias;
			}
		}

		function s_Confirmar() {
			var id = "arrayContratosRetidos";
			var aoMenosUmContratoSelecionado = false;
			var field  = document.forms[0].elements[id];
			if (field.length != undefined) {
				for (var aux = 0; aux < field.length; aux++) {
					if (field[aux].checked) {
						aoMenosUmContratoSelecionado = true;
					}
				}
			} else {
				if (document.forms[0].elements[id].checked) {
					aoMenosUmContratoSelecionado = true;
			  	 }
			}
			if (aoMenosUmContratoSelecionado) {
				if (f_EhVazio( document.forms[0].justificativa.value)) {
					alert("MA00001 - Campo de preenchimento obrigat\u00F3rio");
					document.forms[0].justificativa.focus();
					return;
				}
			}

			var todosContratosSelecionados = false;
			var totalContratosSelecionados = 0;
			var field  = document.forms[0].elements[id];
			if (field.length != undefined) {
				for (var aux = 0; aux < field.length; aux++) {
					if (field[aux].checked) {
						totalContratosSelecionados++;
					}
				}
				if (totalContratosSelecionados == field.length) {
					todosContratosSelecionados = true;
				}
			} else {
				if (document.forms[0].elements[id].checked) {
					todosContratosSelecionados = true;
			  }
			}
			if (todosContratosSelecionados) {
				alert("MA00119 - \u00C9 necess\u00E1rio confirmar pelo menos um.");
				document.forms[0].justificativa.focus();
				return;
			}

			document.forms[0].funcionalidade.value="C";
			document.forms[0].action = CONTEXT+"ConfirmarEntregaGarantias.do?method=confirmar&validaSeguranca=VALIDA";
			document.forms[0].submit();
			//}
		}

// 		function s_Confirmar() {
// 			var id = "arrayContratosRetidos";
// 			var aoMenosUmContratoSelecionado = false;
// 			var field  = document.forms[0].elements[id];
// 			if (field.length != undefined) {
// 				for (var aux = 0; aux < field.length; aux++) {
// 					if (field[aux].checked) {
// 						aoMenosUmContratoSelecionado = true;
// 					}
// 				}
// 			} else {
// 				if (document.forms[0].elements[id].checked) {
// 					aoMenosUmContratoSelecionado = true;
// 			  	 }
// 			}
// 			if (aoMenosUmContratoSelecionado) {
// 				if (f_EhVazio( document.forms[0].justificativa.value)) {
// 					alert("MA00001 - Campo de preenchimento obrigat\u00F3rio");
// 					document.forms[0].justificativa.focus();
// 					return;
// 				}
// 			}

// 			var todosContratosSelecionados = false;
// 			var totalContratosSelecionados = 0;
// 			var field  = document.forms[0].elements[id];
// 			if (field.length != undefined) {
// 				for (var aux = 0; aux < field.length; aux++) {
// 					if (field[aux].checked) {
// 						totalContratosSelecionados++;
// 					}
// 				}
// 				if (totalContratosSelecionados == field.length) {
// 					todosContratosSelecionados = true;
// 				}
// 			} else {
// 				if (document.forms[0].elements[id].checked) {
// 					todosContratosSelecionados = true;
// 			  }
// 			}
// 			if (todosContratosSelecionados) {
// 				alert("MA00119 - \u00C9 necess\u00E1rio confirmar pelo menos um.");
// 				document.forms[0].justificativa.focus();
// 				return;
// 			}

// 			if (document.getElementById("icConferenciaVisual").value == "S") {
// 				var arrayContratosRetidos = document.getElementsByName("arrayContratosRetidos");
// 				if (arrayContratosRetidos.length != undefined) {
// 					for (var aux = 0; aux < arrayContratosRetidos.length; aux++) {
// 						if (arrayContratosRetidos[aux].checked == false) {
// 							var arrayContratosConfirmados = document.createElement("input");
// 							arrayContratosConfirmados.setAttribute('type',"hidden");
// 							arrayContratosConfirmados.setAttribute('name',"arrayContratosConfirmados");
// 							arrayContratosConfirmados.setAttribute('id',"arrayContratosConfirmados");
// 							arrayContratosConfirmados.setAttribute('value', arrayContratosRetidos[aux].value);
// 							document.forms[0].appendChild(arrayContratosConfirmados);
// 						}
// 					}
// 				}


// 			} else {
// 				document.forms[0].funcionalidade.value="C";
// 				document.forms[0].action = CONTEXT+"ConfirmarEntregaGarantias.do?method=confirmar";
// 				document.forms[0].submit();
// 			}
// 		}

		/*ajustes modal ini*/
		function s_ConfirmarModal(operacao){
			if(operacao == "sim"){
				closeModal();
				document.forms[0].funcionalidade.value="C";
				document.forms[0].action = CONTEXT+"ConfirmarEntregaGarantias.do?method=realizarConferencia";
				document.forms[0].submit();

			}else if(operacao == "nao"){
				document.forms[0].funcionalidade.value="C";
				document.forms[0].action = CONTEXT+"ConfirmarEntregaGarantias.do?method=justificarConferencia";
				document.forms[0].submit();
				closeModal();
			}else{
				closeModal();
			}
		}

		function closeModal() {
			var modal = document.getElementById("myModal");
			modal.style.display = "none";
		}

		function showModal(msg) {
			var modal  = document.getElementById("myModal");
			var msgDiv = document.getElementById("myModalMsg");
			msgDiv.innerHTML = msg;
			modal.style.display = "block";
		}
		/*ajustes modal fim*/

