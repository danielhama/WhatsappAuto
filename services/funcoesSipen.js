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

function login(){
    if(!verifica_branco(document.forms[0].usuario.value)){
        alert("CAMPO DE PREENCHIMENTO OBRIGATÓRIO.");
        document.forms[0].usuario.focus();
        return;
    }
    else if(!verifica_branco(document.forms[0].senha.value)){
        alert("CAMPO DE PREENCHIMENTO OBRIGATÓRIO.");
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
		alert("CAMPO DE PREENCHIMENTO OBRIGATÓRIO.");
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
					alert("MA00001 - Campo de preenchimento obrigatório");
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
				alert("MA00119 - É necessário confirmar pelo menos um.");
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
// 					alert("MA00001 - Campo de preenchimento obrigatório");
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
// 				alert("MA00119 - É necessário confirmar pelo menos um.");
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

/Renovacao/

        //<![CDATA[
            function fMascararCpfCnpj(elem)
            {
                var ckbTipoPessoa = document.getElementsByName( 'tipoPessoa' );
                if( ckbTipoPessoa[ 1 ].checked ){
                    return mascara( elem, '99.999.999/9999-99' );
                }
                return mascara( elem, '999.999.999-99' );
            }

            function fAtualizarFiltro(limparCampos)
            {
                var numeroCPFCNPJ = document.getElementById( 'numeroCPFCNPJ' );
                if( limparCampos ){
                    numeroCPFCNPJ.value = '';
                }
                numeroCPFCNPJ.focus();
            }

            function sPesquisar()
            {
                var ckbTipoPessoa = document.getElementsByName( 'tipoPessoa' );
                if( !ckbTipoPessoa[ 0 ].checked && !ckbTipoPessoa[ 1 ].checked ){
                    popupMensagemAjax( 'MA00001' );
                    ckbTipoPessoa[ 0 ].focus();
                    return;
                }
                var numeroCPFCNPJ = document.getElementById( 'numeroCPFCNPJ' );
                if( f_bEhVazio( numeroCPFCNPJ.value ) ){
                    popupMensagemAjax( 'MA00001' );
                    numeroCPFCNPJ.focus();
                    return;
                }

                if( ckbTipoPessoa[ 0 ].checked && !f_bValidaCPF( numeroCPFCNPJ.value ) ){
                    popupMensagemAjax( 'MA00079' );
                    numeroCPFCNPJ.focus();
                    return;
                }
                if( ckbTipoPessoa[ 1 ].checked && !f_bValidaCNPJ( numeroCPFCNPJ.value ) ){
                    popupMensagemAjax( 'MA00084' );
                    numeroCPFCNPJ.focus();
                    return;
                }

                document.forms[0].target = 'principal';
                document.forms[0].action = CONTEXT + 'RenovarContratoLote.do?method=validar';
                document.forms[0].submit();
            }
        //]]>



        //<![CDATA[
        	function s_Pesquisar(acao, pagina){

        		var formulario = document.forms[0];
        		formulario.paginaCorrente.value = pagina;
        		formulario.acao.value = acao;
        		document.forms[0].action = CONTEXT + "RenovarContratoLote.do?method=carregarPaginado";
        		document.forms[0].submit();

            }

            function YNconfirm(txt)
            {
                return typeof (suporteVBscript) == "undefined" ? confirm(txt) : VBconfirm(txt) == 6;
            }

            var hashCode = '';

            function fGerarHash()
            {
                hash = '';

                tipoPrazo = document.getElementsByName( 'tipoPrazo' );
                hash += tipoPrazo[0].checked;
                hash += document.getElementById( 'prazoRenovacao' ).value;

                hash += tipoPrazo[1].checked;
                hash += document.getElementById( 'dataVencimentoAlternativo' ).value;

                hash += document.getElementById( 'selecionarTodosContratos' ).value;

                ckbContratoSelecionado = document.getElementsByName( 'ckbContratoSelecionado' );
                if( ckbContratoSelecionado != undefined && ckbContratoSelecionado.length > 0 ){
                    for( index = 0; index < ckbContratoSelecionado.length; index++ ){
                        hash += ckbContratoSelecionado[ index ].checked + ckbContratoSelecionado[ index ].value;
                    }
                }

                txtValorNovoRenovacao = document.getElementsByName( 'txtValorNovoRenovacao' );
                if( txtValorNovoRenovacao != undefined && txtValorNovoRenovacao.length > 0 ){
                    for( index = 0; index < txtValorNovoRenovacao.length; index++ ){
                        hash += txtValorNovoRenovacao[ index ].value;
                    }
                }

                ckbNovoVencimento = document.getElementsByName( 'ckbNovoVencimento' );
                if( ckbNovoVencimento != undefined && ckbNovoVencimento.length > 0 ){
                    for( index = 0; index < ckbNovoVencimento.length; index++ ){
                        hash += ckbNovoVencimento[ index ].checked + ckbNovoVencimento[ index ].value;
                    }
                }

                txtDataNovoVencimento = document.getElementsByName( 'txtDataNovoVencimento' );
                if( txtDataNovoVencimento != undefined && txtDataNovoVencimento.length > 0 ){
                    for( index = 0; index < txtDataNovoVencimento.length; index++ ){
                        hash += txtDataNovoVencimento[ index ].value;
                    }
                }

                return hash;
            }

            function sVoltarInicioUC()
            {
                document.forms[0].action = CONTEXT + "jsp/Comuns/Principal.jsp?destino=/RenovarContratoLote.do?method=carregar";
                document.forms[0].submit();
            }

            function fApresentarModalidades()
            {
                document.getElementById( 'divModalidades' ).style.display = 'block';
                document.getElementById( 'trDetalharModalidade' ).style.display = 'none';
            }

            function fApresentarBoleto()
            {
                document.getElementById( 'divBoletos' ).style.display = 'block';
                document.getElementById( 'lnkDetalharBoleto' ).style.display = 'none';
            }

            function fOcultarBoleto()
            {
                document.getElementById( 'divBoletos' ).style.display = 'none';
                document.getElementById( 'lnkDetalharBoleto' ).style.display = 'block';
            }


            function fOcultarModalidades()
            {
                document.getElementById( 'divModalidades' ).style.display = 'none';
                document.getElementById( 'trDetalharModalidade' ).style.display = 'table-row';
            }

            function fAjustarTipoPrazo()
            {
                tipoPrazo = document.getElementsByName( 'tipoPrazo' );
                prazoRenovacao = document.getElementById( 'prazoRenovacao' );
                dataVencimentoAlternativo = document.getElementById( 'dataVencimentoAlternativo' );
                prazoRenovacao.disabled = true;
                dataVencimentoAlternativo.disabled = true;
                if( tipoPrazo[ 0 ].checked ){
                    prazoRenovacao.disabled = false;
                    prazoRenovacao.focus();
                }else{
                    dataVencimentoAlternativo.disabled = false;
                    dataVencimentoAlternativo.focus();
                }
            }

            function fHabilitarCalculo( habilitar )
            {
            	icPausa = 'N';

            	if( !habilitar ){
                    if( document.getElementsByClassName( 'destaqueAzul' ) > 0 || document.getElementsByClassName( 'destaqueLaranja' ) > 0 ){
                        habilitar = true;
                    }
                }
                if(icPausa != "S"){
                	document.getElementById( 'btnCalcular' ).disabled = ( !habilitar && ( fContarContratosSelecionados() > 0 ) );
                }else{
                	ckbContratoSelecionado = document.getElementsByName( 'ckbContratoSelecionado' );
                	permitePausa = document.getElementsByName( 'permitePausa' );
                	contPermitePausa = 0;
                	for( index = 0; index < ckbContratoSelecionado.length; index++ ){
                		if( permitePausa[ index ].value == 'S' ){
                			contPermitePausa++;
                		}
                    }
                	if(contPermitePausa == 0){
                		habilitar = false;
                	}
                	document.getElementById( 'btnCalcular' ).disabled = ( !habilitar && ( fContarContratosSelecionados() >= 0 ) );
                }
                document.getElementById( 'btnDetalhar' ).disabled = ( habilitar || ( fContarContratosSelecionados() <= 0 ) );
                if( habilitar ){
                    document.getElementById( 'tdQuantidadeContratosRenovados' ).innerHTML = '&nbsp;&nbsp;';
                    document.getElementById( 'tdValorTotalEmprestimo' ).innerHTML = '&nbsp;';
                    document.getElementById( 'tdValorTotalRenovacao' ).innerHTML = '&nbsp;';
                    spnValorLiquidoRenovacao = document.getElementsByName( 'spnValorLiquidoRenovacao' );
                    if( spnValorLiquidoRenovacao != undefined && spnValorLiquidoRenovacao.length > 0 ){
                        for( index = 0; index < spnValorLiquidoRenovacao.length; index++ ){
                            spnValorLiquidoRenovacao[ index ].innerHTML = '&nbsp;';
                        }
                    }
                }else{
                    document.getElementById( 'tdQuantidadeContratosRenovados' ).innerHTML = '&nbsp;' + document
                        .getElementById( 'hdnQuantidadeContratosRenovados' ).value + '&nbsp;';
                    document.getElementById( 'tdValorTotalEmprestimo' ).innerHTML = document.getElementById( 'hdnValorTotalEmprestimo' )
                        .value;
                    document.getElementById( 'tdValorTotalRenovacao' ).innerHTML = document.getElementById( 'hdnValorTotalRenovacao' )
                        .value + '&nbsp;' + document.getElementById( 'hdnSinalValorTotalRenovacao' ).value;
                    spnValorLiquidoRenovacao = document.getElementsByName( 'spnValorLiquidoRenovacao' );
                    hdnValorLiquidoRenovacao = document.getElementsByName( 'hdnValorLiquidoRenovacao' );
                    hdnTipoSaldo = document.getElementsByName( 'hdnTipoSaldo' );
                    if( spnValorLiquidoRenovacao != undefined && spnValorLiquidoRenovacao.length > 0 ){
                        for( index = 0; index < spnValorLiquidoRenovacao.length; index++ ){
                            spnValorLiquidoRenovacao[ index ].innerHTML = hdnValorLiquidoRenovacao[ index ].value + '&nbsp;'
                                + hdnTipoSaldo[ index ].value;
                        }
                    }
                }
            }

            function fVerificarSelecaoTodosContratos(elem)
            {
                ckbContratoSelecionado = document.getElementsByName( 'ckbContratoSelecionado' );
                ckbNovoVencimento = document.getElementsByName( 'ckbNovoVencimento' );
                txtValorNovoRenovacao = document.getElementsByName( 'txtValorNovoRenovacao' );
                txtDataNovoVencimento = document.getElementsByName( 'txtDataNovoVencimento' );
                icPausa = 'N';
                icPausaContrato = document.getElementsByName( 'icPausaContrato' );
                permitePausa = document.getElementsByName( 'permitePausa' );
                codigoMensagemNaoPausa = document.getElementsByName( 'codigoMensagemNaoPausa' );
                icContratoPausado = document.getElementsByName( 'icContratoPausado' );
                ckbDespausar = document.getElementsByName( 'ckbDespausar' );
            	ckbAlterarPausa = document.getElementsByName( 'ckbAlterarPausa' );

            	if( ckbContratoSelecionado != undefined ){
                    if( elem != undefined && elem.id == 'selecionarTodosContratos' ){
                    	if(icPausa != 'S'){
	                        for( index = 0; index < ckbContratoSelecionado.length; index++ ){
	                            ckbContratoSelecionado[ index ].checked = elem.checked;
	                        }
                    	}else{
                    		for( index = 0; index < ckbContratoSelecionado.length; index++ ){
		                        if( permitePausa[ index ].value == 'S' ){
		                        	ckbContratoSelecionado[…