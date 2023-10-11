import locale
import os
import time
from os import mkdir, remove
import threading
import asyncio
import multiprocessing

import kivy
from kivy.app import App
from kivy.clock import mainthread
from models.ferramentas import threaded
from kivy.event import EventDispatcher
from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.event import EventDispatcher
from kivy.lang import Builder
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior

from models.calculo import *
from models.enviar import *
from models.formata import *
from models.utils2 import tempo_execucao, leia_texto, salva_texto, filtra_vencimento, filtra_data
from models.vCARD import csv_para_vcf

locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')

logging.basicConfig(filename='app.log', level=logging.INFO)
_kv_code = """
#:import utils kivy.utils
BoxLayout:
    canvas:
        Color:
            rgba: .1, .1, .1, 1
            
        Rectangle:
            size: self.size
            pos: self.pos
    orientation: 'vertical'
    HeadingLabel:
        text: 'WhatsappAuto'

    StackLayout:
        # Button is a subclass of Label and can be sized
        # to text in the same way

        Button:
            text: 'Abrir arquivo'
            on_release: app.show_load()

        Button:
            text: 'Enviar'
            on_release: app.enviar()

        Button:
            text: 'Parar envio'
            on_release: app.parar()
            
        Button:
            text: 'Testa Telefones na Base de dados'
            on_release: app.cria_iter_importados()

        Button:
            text: 'Testa sem whats'
            on_release: app.cria_iter_sem()

        Button:
            text: 'Abre Web Whats'
            on_release: app.chama()

        Spinner:
            text: 'Headless'
            values: 'Ativar', 'Desativar'
            on_text: app.spinner_headless(self.text)

        Button:
            text: 'vCARD'
            on_release: app.clientes_com_whats_vcard()

        Button:
            text: 'Exibir Clientes'
            on_release: app.exibir()

    GridLayout:
        id: grid_layout
        cols: 2
        height: cm(7)
        width: cm(10)
        size_hint_y: None

        HeadingLabel:
            text: "Digite o texto a ser enviado"

        HeadingLabel:
            text: 'Execução'

        TextInput:
            id: left_content
            disabled_color: 0, 0, 0, 0
            on_text: app.set_atalho()
            focus: True

        ScrollView:
            do_scroll_x: False
            do_scroll_y: True

            Label1:
                id: right_content
                text_size: self.size
                padding: dp(6), dp(6)
                halign: 'center'
                valign: 'center'

    BoxLayout:
        canvas:
            Color:
                rgba: .1, .1, .1, 1
            
            Rectangle:
                size: self.size
                pos: self.pos
        orientation: 'horizontal'
        size_hint_y: .12
        Button:
            text: 'Salvar Mensagem'
            on_release: app.salva_mensagem()

        Spinner:
            text: 'Mensagem'
            values: 'Vencimento', 'Margem', 'Vencidos', 'Leilao', 'msg2'
            on_text: app.spinner_mensagem(self.text)

        Button:
            text: 'Limpar'
            on_release: app.limpar()

        Button:
            text: 'Selecionar Tudo'
            on_release: app.selecionar()
        Label:
        
        Button:
            text: 'Enviar Filtrados'
            on_release: app.enviar_vencimento()

        Button:
            text: 'Listar Clientes'
            on_release: app.filtra_hoje()

        Button:
            text: 'Criar Lista de Envio'
            on_release: app.criar_lista()
            
        Button:
            text: 'Apagar Lista'
            on_release: app.apagar_lista()
        Button:
            text: 'Filtrar Licitação'
            on_release: app.filtra_licitacao()
        TextInput:
            id: conteudo_licitacao
            disabled_color: 0, 0, 0, 0
            multiline: False
            on_text_validate: app.filtra_licitacao()
            on_focus: root.ids.right_content.text: 'Digite uma data para filtrar os contratos'
            input_type: 'datetime'
        Label:
            text: 'Pesquisar'
            
        TextInput:
            id: middle_content
            disabled_color: 0, 0, 0, 0
            multiline: False
            on_text_validate: app.filtra_data()
            on_focus: root.ids.right_content.text: 'Digite uma data para filtrar os contratos'
            input_type: 'datetime'


    # Need one Widget without size_hint_y: None, so that BoxLayout fills
    # available space.

    RVContratos1:
        # data: clientes_importados
  

    ProgBar:
        id: progbar
        pos_hint: {'x':.05} 
        size_hint_x: .8
        size_hint_y: .1

# The column heading labels have their width set by the parent,
# but determine their height from the text.
<HeadingLabel@Label>:
    bold: True
    padding: dp(10), dp(4)
    valign: 'bottom'
    height: self.texture_size[1]
    text_size: self.width, None
    size_hint_y: None

<ToggleButton,Button>:
    padding: dp(20), dp(8)
    size_hint: None, None
    size: self.texture_size

# This inherits Button and the modifications above, so reset size
<Spinner>:
    size: sp(100), self.texture_size[1]

<Label1@Label>:
    # halign: app.halign
    # valign: app.valign


    canvas:
        Color:
            rgb: 68/255.0, 164/255.0, 201/255.0
        Line:
            rectangle: self.x, self.y, self.width, self.height

<StackLayout>:
    size_hint_y: None
    spacing: dp(0)
    padding: dp(0), dp(4)
    height: self.minimum_height

<LoadDialog>:
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        FileChooserListView:
            id: filechooser

        BoxLayout:
            size_hint_y: None
            height: 30
            Button:
                text: "Cancel"
                on_release: root.cancel()

            Button:
                text: "Load"
                on_release: root.load(filechooser.path, filechooser.selection)
                
<Row>:
    canvas.before:
        Color:
            rgb: utils.get_color_from_hex('#0270af') if self.selected else (0.2, 0.2, 0.2, 1)
        Rectangle:
            size: self.size
            pos: self.pos
<Row1>:
    canvas.before:
        Color:
            rgb: utils.get_color_from_hex('#0270af') if self.selected else (0.2, 0.2, 0.2, 1)
        Rectangle:
            size: self.size
            pos: self.pos
<Row2>:
    canvas.before:
        Color:
            rgb: utils.get_color_from_hex('#0270af') if self.selected else (0.2, 0.2, 0.2, 1)
        Rectangle:
            size: self.size
            pos: self.pos
<RV>:
    canvas:
        Color:
            rgba: 0.1, 0.1, 0.1, 1
        Rectangle:
            size: self.size
            pos: self.pos
    rv: rv
    orientation: 'vertical'
    GridLayout:
        cols: 3
        rows: 2
        size_hint_y: None
        height: dp(108)
        padding: dp(8)
        spacing: dp(16)
        Button:
            text: 'Listar Clientes'
            on_press: root.populate()
        BoxLayout:
            Button:
                text: 'Listar Contratos'
                on_release: root.populate_contratos()
            Spinner:
                text: 'Ordenado por'
                values: 'Avaliação', 'Empréstimo', 'Contrato', 'Vencimento'
                on_text: root.spinner_ordenado(self.text)
            Spinner:
                text: '/\ \/'
                values: 'Ascendente', 'Descendente'
                on_text: root.spinner_asc_desc(self.text)
        BoxLayout:
            Button:
                text: 'Mostrar telefones'
                on_press: root.exibir()
            Button:
                text: 'Mostrar Contratos'
                on_press: root.exibir_contratos()
        Button:
            text: 'Ordenar por Nome'
            on_press: root.sort()
        BoxLayout:
            Button:
                text: 'Inserir Cliente'
                on_press: root.insert(new_item_input.text, new_item_input_2.text)
            BoxLayout:
                spacing: dp(8)
    
                TextInput:
                    id: new_item_input
                    size_hint_x: 0.6
                    hint_text: 'Nome'
                    padding: dp(10), dp(10), 0, 0
                    multiline: False
                TextInput:
                    id: new_item_input_2
                    size_hint_x: 0.6
                    hint_text: 'CPF'
                    padding: dp(10), dp(10), 0, 0
                    multiline: False
        BoxLayout:
            spacing: dp(10)
            Button:
                text: 'Pesquisa'
                on_press: root.search(update_item_input.text)
            TextInput:
                id: update_item_input
                size_hint_x: 0.6
                hint_text: 'Pesquisa'
                padding: dp(10), dp(10), 0, 0
                multiline: False
                on_text_validate: root.search(self.text)
            Button:
                text: 'Remove item'
                on_press: root.remove()

    RecycleView:
        id: rv
        scroll_type: ['content']
        scroll_wheel_distance: dp(114)
        # bar_width: dp(10)
        viewclass: 'Row'
        SelectableRecycleBoxLayout:
            default_size: None, dp(56)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
            halign: 'left'
            valign: 'left'
            # pos_hint: {'x': 0.0, 'y': 0.5}
            # multiselect: True
            # touch_multiselect: True
            
<RVIncluirContrato>:            
    canvas:
        Color:
            rgba: 0.3, 0.3, 0.3, 1
        Rectangle:
            size: self.size
            pos: self.pos
    # rv_incluir_contrato: rv_incluir_contrato
    orientation: 'vertical'

    BoxLayout:
        # cols: 1
        # rows: 4
        # size_hint_y: .8
        # height: dp(50)
        # padding: dp(8)
        # spacing: dp(16)
        orientation: 'vertical'

        BoxLayout:
            # padding: dp(15)
            size_hint_y: None
            height: dp(40)
            spacing: dp(8)
            Button:
                text: 'Listar Contratos'
                on_press: root.populate()
            Button:
                text: 'Inserir Contrato'
                on_release: root.insert(numero.text, avaliacao.text, emprestimo.text, vencimento.text, prazo.text, limite.text)
            Button:
                text: 'Remove Contrato'
                on_press: root.remove()
        BoxLayout:
            # padding: dp(15)
            size_hint_y: None
            height: dp(40)
            spacing: dp(8)

            TextInput:
                padding: dp(15)
                id: numero
                size_hint_x: .4
                hint_text: 'Número do Contrato'
                padding: dp(10), dp(10), 0, 0
                multiline: False
                # on_text_validate: root.insert(self.text)
            TextInput:
                padding: dp(15)
                id: valor_avaliacao
                size_hint_x: .3
                hint_text: 'Valor Avaliação'
                padding: dp(10), dp(10), 0, 0
                multiline: False
                # on_text_validate: root.insert(self.text)
            TextInput:
                id: valor_emprestimo
                size_hint_x: .3
                hint_text: 'Valor Empréstimo'
                padding: dp(10), dp(10), 0, 0
                multiline: False


        BoxLayout:
            # padding: dp(15)
            size_hint_y: None
            height: dp(40)
            spacing: dp(8)
            
            TextInput:
                id: vencimento
                size_hint_x: .4
                hint_text: 'Vencimento'
                padding: dp(10), dp(10), 0, 0
                multiline: False
            TextInput:
                id: prazo
                size_hint_x: .2
                hint_text: 'Prazo'
                padding: dp(10), dp(10), 0, 0
                multiline: False
            TextInput:
                id: limite
                size_hint_x: 0.2
                hint_text: 'Limite 100% ou 85%'
                padding: dp(10), dp(10), 0, 0
                multiline: False
            Label:
                size_hint_x:.4



    RecycleView:
        id: rv_incluir_contrato
        scroll_type: ['content']
        scroll_wheel_distance: dp(114)
        bar_width: dp(20)
        viewclass: 'Row1'
        SelectableRecycleBoxLayout:
            default_size: None, dp(56)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'


<RVTelefones>:
    canvas:
        Color:
            rgba: 0.3, 0.3, 0.3, 1
        Rectangle:
            size: self.size
            pos: self.pos
    rv_telefone: rv_telefone
    orientation: 'vertical'
    
    GridLayout:
        cols: 4
        rows: 1
        size_hint_y: None
        height: dp(50)
        padding: dp(8)
        spacing: dp(16)
        
        
        BoxLayout:
            spacing: dp(8)
            Button:
                text: 'Listar Telefones'
                on_press: root.populate()
            Button:
                text: 'Inserir Telefone'
                on_press: root.insert(novo_telefone.text)
            TextInput:
                id: novo_telefone
                size_hint_x: 0.6
                hint_text: 'telefone'
                padding: dp(10), dp(10), 0, 0
                multiline: False
                on_text_validate: root.insert(self.text)
           
        Button:
            text: 'Remove telefone'
            on_press: root.remove()
    
    RecycleView:
        id: rv_telefone
        scroll_type: ['content']
        scroll_wheel_distance: dp(114)
        # bar_width: dp(10)
        viewclass: 'Row1'
        SelectableRecycleBoxLayout:
            default_size: None, dp(56)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
            
<RVTelefonesEnviar>:
    canvas:
        Color:
            rgba: 0.3, 0.3, 0.3, 1
        Rectangle:
            size: self.size
            pos: self.pos
    rv_telefone: rv_telefone
    orientation: 'vertical'
    
    GridLayout:
        cols: 4
        rows: 1
        size_hint_y: None
        height: dp(50)
        padding: dp(8)
        spacing: dp(16)
        
        
        BoxLayout:
            spacing: dp(8)
            Button:
                text: 'Enviar'
                on_release: root.enviar_mensagem()
            
    
    RecycleView:
        id: rv_telefone
        scroll_type: ['content']
        scroll_wheel_distance: dp(114)
        # bar_width: dp(10)
        viewclass: 'Row1'
        SelectableRecycleBoxLayout:
            default_size: None, dp(56)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'

<RVContratos>:
    canvas:
        Color:
            rgba: 0.0, 0.0, 0.0, 0
        Rectangle:
            size: self.size
            pos: self.pos
    rv_contratos: rv_contratos
    orientation: 'vertical'
    
    GridLayout:
        cols: 5
        rows: 1
        size_hint_y: None
        height: dp(50)
        padding: dp(8)
        spacing: dp(16)
              
        BoxLayout:
            # orientation: 'horizontal'
            spacing: dp(8)
            Button:
                text: "Incluir"
                on_release: root.incluir_contrato()
            Label:
                text: "Número"
            Label:
                text: "Avaliação"
            Label:
                text: 'Empréstimo'
            Label:
                text: 'Vencimento' 


    RecycleView:
        id: rv_contratos
        scroll_type: ['content']
        scroll_wheel_distance: dp(114)
        # bar_width: dp(10)
        viewclass: 'Row2'
        SelectableRecycleBoxLayout:
            default_size: None, dp(56)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
            pos_hint: {'x': 0.0, 'y': 0.5}
            multiselect: True
            touch_multiselect: True                        
    GridLayout:
        cols:5
        rows:1
        size_hint_y: None
        height: dp(50)
        padding: dp(8)
        spacing: dp(16)
        Button:
            text: 'Calcular Juros Todos'
            on_press: root.calcular()
        Button:
            text: 'Calcular Selecionados'
            on_press: root.calcular1()
        Button:
            text: 'Calcular Margem'
            on_press: root.calcular_margem()
        TextInput:
            id: 'data_futura'
            hint_text: 'Data de pagamento'
            multiline: False
            size_hint_y: 0.2
            on_text_validate: root.calcular2(self.text)
        Button:
            text: 'Calcular Liquidação'
            on_press: root.calcular_liquidacao()
        Label:
        Label:
        
<RVContratos1>:
    canvas:
        Color:
            rgba: 0, 0, 0, 0
        Rectangle:
            size: self.size
            pos: self.pos
    rv_bottom: rv_bottom
    orientation: 'vertical'
    
    GridLayout:
        cols: 1
        rows: 1
        size_hint_y: None
        height: dp(50)
        padding: dp(8)
        spacing: dp(16)

        BoxLayout:
            spacing: dp(8)
            Button:
                text: 'Exibir'
                on_press: root.populate()
            Label:
                text: "Nome"
            Label:
                text: "CPF"
            Label:
                text: 'Vencimento'
            Label:
                text: 'Telefones' 
                

    RecycleView:
        id: rv_bottom
        scroll_type: ['content']
        scroll_wheel_distance: dp(114)
        # bar_width: dp(10)
        # size_hint: 1.
        viewclass: 'Row3'
        RecycleBoxLayout:
            default_size: None, dp(30)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'


<RVCalculo>:
    canvas:
        Color:
            rgba: 0, 0, 0, 0
        Rectangle:
            size: self.size
            pos: self.pos
    rv_calculo: rv_calculo
    orientation: 'vertical'
    
    BoxLayout: 
        orientation: 'vertical'
        GridLayout:
            cols: 1
            rows: 1
            height: dp(50)
            padding: dp(8)
            spacing: dp(16)
            size_hint_y: None

            BoxLayout:
                spacing: dp(8)
                Label:
                    text: "Prazo"
                Label:
                    text: "Valor"
                Label:
                    text: 'Vencimento'
    
    
        RecycleView:
            id: rv_calculo
            scroll_type: ['content']
            scroll_wheel_distance: dp(114)
            # bar_width: dp(10)
            height: 100
            size_hint_y: .8
            viewclass: 'Row4'
            RecycleBoxLayout:
                default_size: None, dp(35)
                default_size_hint: 1, None
                height: self.minimum_height
                size_hint_y: None
                orientation: 'vertical'
        GridLayout:
            cols:2
            rows:1
            size_hint_y: None
            padding: dp(10)
            spacing: dp(20)
            Button:
                text: 'Enviar para cliente'
                on_release: root.enviar_cliente()
            Label:
                valign: 'bottom'
                halign: 'center'
                id: calculo
                text_size: self.size
                
<RVCalculoLiquidacao>:
    canvas:
        Color:
            rgba: 0, 0, 0, 0
        Rectangle:
            size: self.size
            pos: self.pos
    rv_calculo_liquidacao: rv_calculo_liquidacao
    orientation: 'vertical'
    
    BoxLayout: 
        orientation: 'vertical'
        GridLayout:
            cols: 1
            rows: 1
            height: dp(50)
            padding: dp(8)
            spacing: dp(16)
            size_hint_y: None

            BoxLayout:
                spacing: dp(8)
                Label:
                    text: "Contrato"
                Label:
                    text: "Valor"
                Label:
                    text: 'Encargos/Desconto'
                    
    
    
        RecycleView:
            id: rv_calculo_liquidacao
            scroll_type: ['content']
            scroll_wheel_distance: dp(114)
            # bar_width: dp(10)
            height: 100
            size_hint_y: .8
            viewclass: 'Row5'
            RecycleBoxLayout:
                default_size: None, dp(35)
                default_size_hint: 1, None
                height: self.minimum_height
                size_hint_y: None
                orientation: 'vertical'
        GridLayout:
            cols:3
            rows:1
            size_hint_y: None
            padding: dp(10)
            spacing: dp(20)
            Button:
                text: 'Enviar para cliente'
                on_release: root.enviar_cliente()
            Label:
                valign: 'bottom'
                halign: 'center'
                id: calculo_liquidacao
                text_size: self.size
            Label:
                id: valor_total

# <Row2@RecycleKVIDsDataViewBehavior+BoxLayout>:
#     # canvas.before:
#     #     Color:
#     #         rgba: 0.3, 0.3, 0.3, 1
#     #     Rectangle:
#     #         size: self.size
#     #         pos: self.pos
#     value: ''
#     Label:
#         id: contrato
#     Label:
#         id: avaliacao
#     Label:
#         id: emprestimo    
#     Label:
#         id: vencimento

    
<Row3@RecycleKVIDsDataViewBehavior+BoxLayout>:
    canvas.before:
        Color:
            rgba: 0.2, 0.2, 0.2, 1
        Rectangle:
            size: self.size
            pos: self.pos

    Label:
        id: nome
    Label:
        id: cpf
    Label:
        id: vencimento    
    Label:
        id: telefones
        
<Row4@RecycleKVIDsDataViewBehavior+BoxLayout>
    canvas.before:
        Color:
            rgba: 0.2, 0.1, 0.1, .05
        Rectangle:
            size: self.size
            pos: self.pos
    Label:
        id: prazo
    Label:
        id: valor
    Label:
        id: vencimento
        

<Row5@RecycleKVIDsDataViewBehavior+BoxLayout>
    canvas.before:
        Color:
            rgba: 0.2, 0.1, 0.1, .05
        Rectangle:
            size: self.size
            pos: self.pos
    Label:
        id: contrato
    Label:
        id: valor
    Label:
        id: encargos
"""


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class Row(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(Row, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(Row, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            global indice
            global cpf
            indice = self.index
            cpf = rv.data[index]['text'].split('|')[1]
            cpf = cpf.strip()


class Row1(RecycleDataViewBehavior, Label):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(Row1, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(Row1, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            global indice_1
            indice_1 = self.index
            global telefone_enviar
            telefone_enviar = rv.data[index]['text']


class Row2(RecycleDataViewBehavior, Label):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    global lista_de_contratos
    lista_de_contratos = set()

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(Row2, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(Row2, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            contrato = " ".join((rv.data[index]['text']).split()).split(" ")
            if contrato not in lista_de_contratos:
                lista_de_contratos.append(contrato)

        else:
            if len(lista_de_contratos) != 0:
                contrato = " ".join((rv.data[index]['text']).split()).split(" ")
                try:
                    lista_de_contratos.remove(contrato)
                except Exception as e:
                    print(e)


class RVTelefonesEnviar(BoxLayout):

    def populate(self):
        try:
            self.rv_telefone.data = self.listar_exibicao_telefones()
        except Exception as e:
            logging.basicConfig(filename='app.log', level=logging.INFO)

    def enviar_mensagem(self):
        whats.worker.envio_msg.send_whatsapp_msg_valor(texto=mensagem, numero=telefone_enviar)

    def listar_exibicao_telefones(self):
        """
        Função para listar os clientes com telefone
        """
        id = pesquisa_id(cpf)
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            f'SELECT t.numero, t.id_cliente, c.id, c.cpf FROM telefones as t, clientes as c where c.id = id_cliente and c.id = {id}')
        clientes = cursor.fetchall()
        lista_clientes = []
        if len(clientes) > 0:
            for cliente in clientes:
                cliente = {'text': str(cliente[0])}
                lista_clientes.append(cliente)
        else:
            print('Não existem clientes cadastrados.')
        desconectar(conn)
        return lista_clientes

class RVTelefones(BoxLayout):

    def populate(self):
        try:
            self.rv_telefone.data = self.listar_exibicao_telefones()
        except Exception as e:
            logging.basicConfig(filename='app.log', level=logging.INFO)

    def insert(self, value):
        if len(value) >= 12:
            try:
                id = pesquisa_id(cpf)
                inserir_telefone(value, id)
                self.populate()
            except Exception as e:
                logging.basicConfig(filename='app.log', level=logging.INFO)

    def remove(self):
        if self.rv_telefone.data[indice_1]:
            numero = int(self.rv_telefone.data[indice_1]['text'])

            self.rv_telefone.data.pop(indice_1)
            try:
                deletar_telefone(numero)
            except Exception as e:
                logging.basicConfig(filename='app.log', level=logging.INFO)

    def listar_exibicao_telefones(self):
        """
        Função para listar os clientes com telefone
        """
        id = pesquisa_id(cpf)
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            f'SELECT t.numero, t.id_cliente, c.id, c.cpf FROM telefones as t, clientes as c where c.id = id_cliente and c.id = {id}')
        clientes = cursor.fetchall()
        lista_clientes = []
        if len(clientes) > 0:
            for cliente in clientes:
                cliente = {'text': str(cliente[0])}
                lista_clientes.append(cliente)
        else:
            print('Não existem clientes cadastrados.')
        desconectar(conn)
        return lista_clientes


class RVContratos(BoxLayout):

    def populate(self, dt=None):
        try:
            self.rv_contratos.data = self.lista_contratos()
        except Exception as e:
            logging.basicConfig(filename='app.log', level=logging.INFO)

    def lista_contratos(self):
        """
                Função para listar os contratos do cliente
                """
        try:
            conn = conectar()
            cursor = conn.cursor()
            id = pesquisa_id(cpf)

            cursor.execute(
                f'SELECT contratos.numero, contratos.valor_avaliacao, contratos.valor_emprestimo, contratos.vencimento FROM contratos, clientes WHERE contratos.id_cliente = clientes.id and clientes.id = {id}')
            clientes = cursor.fetchall()
            lista_clientes = []
            if len(clientes) > 0:
                for cliente in clientes:
                    char = 50 - len(str(locale.currency(cliente[1])))
                    char1 = 50 - len(str(locale.currency(cliente[2])))
                    vencimento = datetime.datetime.strftime(
                        datetime.datetime.strptime(cliente[3].split(' ')[0], '%Y-%m-%d'), '%d/%m/%Y')
                    cliente_exibicao = {'text': str(cliente[0]) + (" " * char) + locale.currency(cliente[1], grouping=True) + (" " * char1) +  locale.currency(cliente[2], grouping=True) + (" " * char) + vencimento}


                    lista_clientes.append(cliente_exibicao)
            else:
                print('Não existem contratos cadastrados para esse cliente.')
            desconectar(conn)
            return lista_clientes
        except Exception as e:
            logging.basicConfig(filename='app.log', level=logging.INFO)

    def calcular(self):
        content_calculo = RVCalculo()
        self._popup = Popup(title="Cálculo de Juros", content=content_calculo, size_hint=(0.6, 0.5))

        self._popup.open()
        content_calculo.populate()

    def calcular1(self):
        content_calculo = RVCalculo()
        self._popup = Popup(title="Cálculo de Juros", content=content_calculo, size_hint=(0.6, 0.5))

        self._popup.open()
        content_calculo.populate1()

    def calcular2(self, data):
        global data_futura_1
        if '/' in data:
            data_futura_1 = data
        elif len(data) == 8 and "/" not in data:
            data_futura_1 = data[0:2] + '/' + data[2:4] + '/' + data[4::]

        content_calculo = RVCalculo()
        self._popup = Popup(title="Cálculo de Juros", content=content_calculo, size_hint=(0.6, 0.5))

        self._popup.open()
        content_calculo.populate2()

    def calcular_margem(self):
        content_calculo = RVCalculo()
        self._popup = Popup(title="Cálculo de Juros", content=content_calculo, size_hint=(0.6, 0.5))

        self._popup.open()
        content_calculo.populate_margem()

    def calcular_liquidacao(self):
        content_calculo = RVCalculoLiquidacao()
        self._popup = Popup(title="Cálculo Liquidação", content=content_calculo, size_hint=(0.6, 0.5))

        self._popup.open()
        content_calculo.populate_liquidacao()

    def incluir_contrato(self):
        content = RVIncluirContrato()
        self._popup = Popup(title="Incluir Contrato", content=content, size_hint=(0.9, 0.3))
        self._popup.open()

class RVIncluirContrato(BoxLayout):

    def insert(self, value):
        if len(value) >= 12:
            try:
                id = pesquisa_id(cpf)
                inserir_telefone(value, id)
                self.populate()
            except Exception as e:
                logging.basicConfig(filename='app.log', level=logging.INFO)

    def remove(self):
        if self.rv_telefone.data[indice_1]:
            numero = int(self.rv_telefone.data[indice_1]['text'])

            self.rv_telefone.data.pop(indice_1)
            try:
                deletar_telefone(numero)
            except Exception as e:
                logging.basicConfig(filename='app.log', level=logging.INFO)

    def listar_exibicao_telefones(self):
        """
        Função para listar os clientes com telefone
        """
        id = pesquisa_id(cpf)
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            f'SELECT t.numero, t.id_cliente, c.id, c.cpf FROM telefones as t, clientes as c where c.id = id_cliente and c.id = {id}')
        clientes = cursor.fetchall()
        lista_clientes = []
        if len(clientes) > 0:
            for cliente in clientes:
                cliente = {'text': str(cliente[0])}
                lista_clientes.append(cliente)
        else:
            print('Não existem clientes cadastrados.')
        desconectar(conn)
        return lista_clientes


class RVContratos1(BoxLayout):

    def populate(self):
        clientes = []
        try:
            for cliente in clientes_importados:
                try:
                    if type(cliente['Vencimento']) == str:
                        vencimento = cliente['Vencimento'].split(' ')
                        vencimento = datetime.datetime.strptime(vencimento[0], '%Y-%m-%d')
                        vencimento = datetime.datetime.strftime(vencimento, '%d/%m/%Y')
                    else:
                        vencimento = datetime.datetime.strftime(cliente['Vencimento'], '%d/%m/%Y')
                    cliente = {'nome.text': cliente['Nome'], 'cpf.text': cliente['CPF'], 'vencimento.text': vencimento,
                               'telefones.text': str(cliente['Telefones'])}
                    clientes.append(cliente)
                except Exception as e:
                    cliente = {'nome.text': cliente['Nome'], 'cpf.text': cliente['CPF'], 'vencimento.text': '00/00/00',
                               'telefones.text': str(cliente['Telefones'])}
                    clientes.append(cliente)

            self.rv_bottom.data = clientes
        except Exception as e:
            logging.exception(str(e))


class RV(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ordenado = 'c.valor_avaliacao'
        self.asc_desc = 'DESC'

    def exibir(self):
        content1 = RVTelefones()
        self._popup = Popup(title="Telefones", content=content1,
                            size_hint=(0.6, 0.5))

        self._popup.open()
        content1.populate()

    def exibir_contratos(self):
        global lista_de_contratos
        lista_de_contratos = []
        content = RVContratos()
        self._popup = Popup(title="Contratos", content=content,
                            size_hint=(0.9, 0.7))

        self._popup.open()
        content.populate()

    def populate(self):
        self.rv.data = self.listar_exibicao()

    def populate_contratos(self):
        self.rv.data = self.listar_exibicao_contratos()

    def spinner_ordenado(self, comando):
        if comando == 'Contrato':
            self.ordenado = 'c.numero'
            self.populate_contratos()
        elif comando == 'Empréstimo':
            self.ordenado = 'c.valor_emprestimo'
            self.populate_contratos()
        elif comando == 'Avaliação':
            self.ordenado = 'c.valor_avaliacao'
            self.populate_contratos()
        elif comando == 'Vencimento':
            self.ordenado = 'c.vencimento'
            self.populate_contratos()

    def spinner_asc_desc(self, comando):
        if comando == 'Ascendente':
            self.asc_desc = 'ASC'
            self.populate_contratos()

        elif comando == 'Descendente':
            self.asc_desc = 'DESC'
            self.populate_contratos()

    def sort(self):
        self.rv.data = sorted(self.rv.data, key=lambda x: x['text'])

    def insert(self, value, value_2):
        nome = value.upper()
        nome = nome.strip()
        value_2 = value_2.strip()
        try:
            if len(nome) > 0 and len(value_2) > 0:

                self.rv.data.insert(0, {
                    'text': nome + '    ' + '|' + '    ' + value_2})
        except Exception as e:
            logging.exception(str(e))
        try:
            if len(nome) > 0 and len(value_2) > 0:
                inserir_cliente(nome, value_2)
        except Exception as e:
            logging.exception(str(e))

    def search(self, pesquisa: str):
        if ".213." not in self.rv.data[0]['text']:
            #     # self.populate_contratos()
            #     pass
            # else:
            self.populate()
        lista = []
        nome = pesquisa.upper()
        for i in range(0, len(self.rv.data)):
            if nome in self.rv.data[i]['text']:
                lista.append(self.rv.data[i])
        self.rv.data = lista

    def remove(self):
        if self.rv.data[indice]:
            try:
                deletar_cliente(self.rv.data[indice]['text'].split(',')[1])
                self.rv.data.pop(indice)
            except Exception as e:
                logging.exception(str(e))

    def listar_exibicao(self):
        """
        Função para listar os clientes com telefone
        """
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT cli.nome, cli.cpf FROM  clientes as cli')
        clientes = cursor.fetchall()
        lista_clientes = []
        if len(clientes) > 0:
            for cliente in clientes:
                cliente = {'text': str(cliente[0] + '    ' + '|' + '    ' + str(cliente[1]))}
                lista_clientes.append(cliente)
        else:
            print('Não existem clientes cadastrados.')
        desconectar(conn)
        return lista_clientes

    def listar_exibicao_contratos(self):
        """
        Função para listar os clientes com telefone
        """

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            f'SELECT cli.nome, cli.cpf, c.numero, c.valor_avaliacao, c.valor_emprestimo, c.vencimento FROM  clientes as cli, contratos as c WHERE c.id_cliente = cli.id ORDER BY {self.ordenado} {self.asc_desc}')
        clientes = cursor.fetchall()
        lista_clientes = []
        if len(clientes) > 0:
            for cliente in clientes:
                char = 45 - len(cliente[0])
                vencimento = datetime.datetime.strftime(
                    datetime.datetime.strptime(cliente[5].split(' ')[0], '%Y-%m-%d'), "%d/%m/%Y")
                cliente = {'text': str(
                    cliente[0] + (' ' * char) + '|' + '    ' + str(cliente[1]) + '    ' + '|' + '    ' + str(
                        cliente[2]) + '    ' + '|' + '    ' + locale.currency(cliente[3],
                                                                              grouping=True) + '    ' + locale.currency(
                        cliente[4], grouping=True) + '    ' + '|' + '    ' + vencimento)}
                lista_clientes.append(cliente)
        else:
            print('Não existem clientes cadastrados.')
        desconectar(conn)
        return lista_clientes


class RVCalculo(BoxLayout):

    def populate(self):
        try:
            self.rv_calculo.data = self.lista_calculo()
        except Exception as e:
            logging.exception(str(e))

    def populate1(self):
        try:
            # self.rv_calculo.data = self.lista_calculo_vencidos()
            self.rv_calculo.data = self.calcula_juros_selecionados()

        except Exception as e:
            logging.exception(str(e))

    def populate2(self):
        try:
            self.rv_calculo.data = self.lista_calculo_futuro(data=data_futura_1)
        except Exception as e:
            logging.exception(str(e))

    def populate_margem(self):
        try:
            self.rv_calculo.data = self.lista_calculo_margem()
            if not self.possui_margem:
                self.ids.calculo.text = 'Cliente não possui margem, ou não cobre todo o valor dos juros para 30 dias'
            elif 20000 < self.total_emprestimo <= 120000:
                self.ids.calculo.text = 'Serão necessários 2 avaliadores para autorizar a alçada, conforme AL021'
            elif self.total_emprestimo > 120000:
                self.ids.calculo.text = 'Será necessário Comitê de Crédito para autorizar a alçada, conforme AL021'
            else:
                self.ids.calculo.text = ''


        except Exception as e:
            logging.exception(str(e))

    # def populate_liquidacao(self):
    #     try:
    #         self.rv_calculo.data = self.lista_calculo_margem()
    #         if not self.possui_margem:
    #             self.ids.calculo.text = 'Cliente não possui margem, ou não cobre todo o valor dos juros para 30 dias'
    #         elif 20000 < self.total_emprestimo <= 120000:
    #             self.ids.calculo.text = 'Serão necessários 2 avaliadores para autorizar a alçada, conforme AL021'
    #         elif self.total_emprestimo > 120000:
    #             self.ids.calculo.text = 'Será necessário Comitê de Crédito para autorizar a alçada, conforme AL021'
    #         else:
    #             self.ids.calculo.text = ''


        except Exception as e:
            logging.exception(str(e))

    def enviar_cliente(self):
        telefones = listar_telefones_por_cpf(cpf)
        if len(telefones) > 1:
            content = RVTelefonesEnviar()
            self._popup = Popup(title="Selecione o telefone para enviar", content=content,
                                size_hint=(0.4, 0.4))
            self._popup.open()
            content.populate()
        else:
            whats.worker.envio_msg.send_whatsapp_msg_valor(texto=mensagem, numero=telefones)


    def calcula_juros_selecionados(self):
        calculos = []
        global mensagem
        mensagem = []
        d30 = 0
        d60 = 0
        d90 = 0
        d120 = 0

        data30, data60, data90, data120 = calcular_data()
        # lista_de_contratos = set(lista_de_contratos)
        for contrato in lista_de_contratos:
            valor_avaliacao = float(contrato[2].replace(".", '').replace(",", "."))
            valor_emprestimo = float(contrato[4].replace(".", '').replace(",", "."))

            d30_t, d60_t, d90_t, d120_t = calcular_juros(valor_avaliacao, valor_emprestimo,
                                                     datetime.datetime.strptime(contrato[5], '%d/%m/%Y'), consulta_prazo(contrato[0]))
            d30 += d30_t
            d60 += d60_t
            d90 += d90_t
            d120 += d120_t

        calculo = {'prazo.text': '30 dias', 'valor.text': locale.currency(d30, grouping=True),
                   'vencimento.text': data30 or '00/00/0000'}
        calculos.append(calculo)
        calculo = {'prazo.text': '60 dias', 'valor.text': locale.currency(d60, grouping=True),
                   'vencimento.text': data60 or ' 00/00/0000'}
        calculos.append(calculo)
        calculo = {'prazo.text': '90 dias', 'valor.text': locale.currency(d90, grouping=True),
                   'vencimento.text': data90 or '00/00/0000'}
        calculos.append(calculo)
        calculo = {'prazo.text': '120 dias', 'valor.text': locale.currency(d120, grouping=True),
                   'vencimento.text': data120 or '00/00/0000'}
        calculos.append(calculo)

        msg_vazia = " "
        mensagem.append(msg_vazia)
        msg = f'Renovação para 30 dias  {locale.currency(d30, grouping=True)} - Novo Vencimento {data30}'
        mensagem.append(msg)
        mensagem.append(msg_vazia)
        msg = f'Renovação para 60 dias  {locale.currency(d60, grouping=True)} - Novo Vencimento {data60}'
        mensagem.append(msg)
        mensagem.append(msg_vazia)
        msg = f'Renovação para 90 dias  {locale.currency(d90, grouping=True)} - Novo Vencimento {data90}'
        mensagem.append(msg)
        mensagem.append(msg_vazia)
        msg = f'Renovação para 120 dias  {locale.currency(d120, grouping=True)} - Novo Vencimento {data120}'
        mensagem.append(msg)
        mensagem.append(msg_vazia)

        return calculos

    def lista_calculo(self):
        """
                       Função para listar os contratos do cliente
                       """
        data30, data60, data90, data120 = calcular_data()

        try:
            conn = conectar()
            cursor = conn.cursor()
            id = pesquisa_id(cpf)
            calculos = []
            global mensagem
            mensagem = []
            d30 = 0
            d60 = 0
            d90 = 0
            d120 = 0
            cursor.execute(
                f'select contratos.numero, contratos.vencimento, contratos.valor_avaliacao, contratos.valor_emprestimo, contratos.prazo, contratos.id_cliente, clientes.id from contratos, clientes where contratos.id_cliente = clientes.id AND clientes.id = {id}')
            clientes = cursor.fetchall()
            if len(clientes) > 0:
                for cliente in clientes:
                    vencimento = datetime.datetime.strptime(cliente[1].split(' ')[0], '%Y-%m-%d')
                    prazo = cliente[4]
                    self.total_avaliacao = cliente[2]
                    self.total_emprestimo = cliente[3]
                    d30_t, d60_t, d90_t, d120_t = calcular_juros(self.total_avaliacao, self.total_emprestimo,
                                                                 vencimento, prazo)
                    d30 += d30_t
                    d60 += d60_t
                    d90 += d90_t
                    d120 += d120_t
                calculo = {'prazo.text': '30 dias', 'valor.text': locale.currency(d30, grouping=True),
                           'vencimento.text': data30 or '00/00/0000'}
                calculos.append(calculo)
                calculo = {'prazo.text': '60 dias', 'valor.text': locale.currency(d60, grouping=True),
                           'vencimento.text': data60 or ' 00/00/0000'}
                calculos.append(calculo)
                calculo = {'prazo.text': '90 dias', 'valor.text': locale.currency(d90, grouping=True),
                           'vencimento.text': data90 or '00/00/0000'}
                calculos.append(calculo)
                calculo = {'prazo.text': '120 dias', 'valor.text': locale.currency(d120, grouping=True),
                           'vencimento.text': data120 or '00/00/0000'}
                calculos.append(calculo)

                msg_vazia = " "
                mensagem.append(msg_vazia)
                msg = f'Renovação para 30 dias  {locale.currency(d30, grouping=True)} - Novo Vencimento {data30}'
                mensagem.append(msg)
                mensagem.append(msg_vazia)
                msg = f'Renovação para 60 dias  {locale.currency(d60, grouping=True)} - Novo Vencimento {data60}'
                mensagem.append(msg)
                mensagem.append(msg_vazia)
                msg = f'Renovação para 90 dias  {locale.currency(d90, grouping=True)} - Novo Vencimento {data90}'
                mensagem.append(msg)
                mensagem.append(msg_vazia)
                msg = f'Renovação para 120 dias  {locale.currency(d120, grouping=True)} - Novo Vencimento {data120}'
                mensagem.append(msg)
                mensagem.append(msg_vazia)

            else:
                print('Não existem contratos cadastrados para esse cliente.')
            desconectar(conn)
            return calculos
        except Exception as e:
            logging.exception(str(e))

    def lista_calculo_vencidos(self):
        """
                Função para listar os contratos do cliente
                """
        data30, data60, data90, data120 = calcular_data()

        try:
            conn = conectar()
            cursor = conn.cursor()
            id = pesquisa_id(cpf)
            calculos = []
            global mensagem
            mensagem = []
            hoje = datetime.datetime.today()
            d30 = 0
            d60 = 0
            d90 = 0
            d120 = 0
            cursor.execute(
                f"SELECT contratos.numero, contratos.vencimento, contratos.valor_avaliacao AS 'Avaliacao', contratos.valor_emprestimo, contratos.prazo, contratos.id_cliente, clientes.id FROM contratos, clientes WHERE contratos.id_cliente = clientes.id AND clientes.id = {id}")
            clientes = cursor.fetchall()
            if len(clientes) > 0:
                for cliente in clientes:
                    vencimento = datetime.datetime.strptime(cliente[1].split(' ')[0], '%Y-%m-%d')
                    if vencimento <= hoje:
                        self.vencimento = cliente[1]
                        prazo = cliente[4]
                        self.total_avaliacao = cliente[2]
                        self.total_emprestimo = cliente[3]
                        d30_t, d60_t, d90_t, d120_t = calcular_juros(self.total_avaliacao, self.total_emprestimo,
                                                                     vencimento, prazo)
                        d30 += d30_t
                        d60 += d60_t
                        d90 += d90_t
                        d120 += d120_t
                calculo = {'prazo.text': '30 dias', 'valor.text': locale.currency(d30, grouping=True),
                           'vencimento.text': data30 or '00/00/0000'}
                calculos.append(calculo)
                calculo = {'prazo.text': '60 dias', 'valor.text': locale.currency(d60, grouping=True),
                           'vencimento.text': data60 or ' 00/00/0000'}
                calculos.append(calculo)
                calculo = {'prazo.text': '90 dias', 'valor.text': locale.currency(d90, grouping=True),
                           'vencimento.text': data90 or '00/00/0000'}
                calculos.append(calculo)
                calculo = {'prazo.text': '120 dias', 'valor.text': locale.currency(d120, grouping=True),
                           'vencimento.text': data120 or '00/00/0000'}
                calculos.append(calculo)

                msg_vazia = " "
                mensagem.append(msg_vazia)
                msg = f'Renovação para 30 dias  {locale.currency(d30, grouping=True)} - Novo Vencimento {data30}'
                mensagem.append(msg)
                mensagem.append(msg_vazia)
                msg = f'Renovação para 60 dias  {locale.currency(d60, grouping=True)} - Novo Vencimento {data60}'
                mensagem.append(msg)
                mensagem.append(msg_vazia)
                msg = f'Renovação para 90 dias  {locale.currency(d90, grouping=True)} - Novo Vencimento {data90}'
                mensagem.append(msg)
                mensagem.append(msg_vazia)
                msg = f'Renovação para 120 dias  {locale.currency(d120, grouping=True)} - Novo Vencimento {data120}'
                mensagem.append(msg)
                mensagem.append(msg_vazia)

            else:
                print('Não existem contratos cadastrados para esse cliente.')
            desconectar(conn)
            return calculos
        except Exception as e:
            logging.exception(str(e))

    def lista_calculo_futuro(self, data):
        """
                Função para listar os contratos do cliente
                """
        data30, data60, data90, data120 = calcular_data_futura(data)
        data = datetime.datetime.strptime(data, '%d/%m/%Y')

        try:
            conn = conectar()
            cursor = conn.cursor()
            id = pesquisa_id(cpf)
            calculos = []
            global mensagem
            mensagem = []
            d30 = 0
            d60 = 0
            d90 = 0
            d120 = 0
            cursor.execute(
                f'select contratos.numero, contratos.vencimento, contratos.valor_avaliacao, contratos.valor_emprestimo, contratos.prazo, contratos.id_cliente, clientes.id from contratos, clientes where contratos.id_cliente = clientes.id AND clientes.id = {id}')
            clientes = cursor.fetchall()
            if len(clientes) > 0:
                for cliente in clientes:
                    vencimento = datetime.datetime.strptime(cliente[1].split(" ")[0], '%Y-%m-%d')
                    if vencimento <= data:
                        prazo = cliente[4]
                        self.total_avaliacao = cliente[2]
                        self.total_emprestimo = cliente[3]
                        d30_t, d60_t, d90_t, d120_t = calcular_juros_futuros(self.total_avaliacao,
                                                                             self.total_emprestimo,
                                                                             vencimento, prazo, data)
                        d30 += d30_t
                        d60 += d60_t
                        d90 += d90_t
                        d120 += d120_t
                calculo = {'prazo.text': '30 dias', 'valor.text': locale.currency(d30, grouping=True),
                           'vencimento.text': data30 or '00/00/0000'}
                calculos.append(calculo)
                calculo = {'prazo.text': '60 dias', 'valor.text': locale.currency(d60, grouping=True),
                           'vencimento.text': data60 or ' 00/00/0000'}
                calculos.append(calculo)
                calculo = {'prazo.text': '90 dias', 'valor.text': locale.currency(d90, grouping=True),
                           'vencimento.text': data90 or '00/00/0000'}
                calculos.append(calculo)
                calculo = {'prazo.text': '120 dias', 'valor.text': locale.currency(d120, grouping=True),
                           'vencimento.text': data120 or '00/00/0000'}
                calculos.append(calculo)

                msg_vazia = " "
                mensagem.append(msg_vazia)
                msg = f'Renovação para 30 dias {locale.currency(d30, grouping=True)} - Novo Vencimento {data30}'
                mensagem.append(msg)
                mensagem.append(msg_vazia)
                msg = f'Renovação para 60 dias {locale.currency(d60, grouping=True)} - Novo Vencimento {data60}'
                mensagem.append(msg)
                mensagem.append(msg_vazia)
                msg = f'Renovação para 90 dias {locale.currency(d90, grouping=True)} - Novo Vencimento {data90}'
                mensagem.append(msg)
                mensagem.append(msg_vazia)
                msg = f'Renovação para 120 dias {locale.currency(d120, grouping=True)} - Novo Vencimento {data120}'
                mensagem.append(msg)
                mensagem.append(msg_vazia)

            else:
                print('Não existem contratos cadastrados para esse cliente.')
            desconectar(conn)
            return calculos
        except Exception as e:
            logging.exception(str(e))

    def lista_calculo_margem(self):
        """
                Função para listar os contratos do cliente
                """
        data30, data60, data90, data120 = calcular_data()

        try:
            conn = conectar()
            cursor = conn.cursor()
            id = pesquisa_id(cpf)
            calculos = []
            global mensagem
            mensagem = []
            d30 = 0
            d60 = 0
            d90 = 0
            d120 = 0
            self.total_emprestimo = 0
            cursor.execute(
                f'select SUM(contratos.valor_avaliacao) as total, clientes.limite from contratos, clientes where contratos.id_cliente = clientes.id AND clientes.id = {id}')
            cliente = cursor.fetchall()
            total = cliente[0][0]
            self.limite = cliente[0][1]
            cursor.execute(
                f'select contratos.numero, contratos.vencimento, contratos.valor_avaliacao, contratos.valor_emprestimo, contratos.prazo, contratos.id_cliente, clientes.id from contratos, clientes where contratos.id_cliente = clientes.id AND clientes.id = {id}')
            clientes = cursor.fetchall()
            if len(clientes) > 0:
                for cliente in clientes:
                    vencimento = datetime.datetime.strptime(cliente[1].split(' ')[0], '%Y-%m-%d')
                    self.vencimento = cliente[1]
                    prazo = cliente[4]
                    self.avaliacao = cliente[2]
                    self.emprestimo = cliente[3]
                    # self.limite = cliente[5]
                    if self.limite == 100:
                        self.total_emprestimo += self.avaliacao
                    else:
                        self.total_emprestimo += self.avaliacao * .85
                    d30_t, d60_t, d90_t, d120_t = calcular_margem(self.avaliacao, self.emprestimo,
                                                                  vencimento, prazo, self.limite, total)
                    d30 += d30_t
                    d60 += d60_t
                    d90 += d90_t
                    d120 += d120_t
                calculo = {'prazo.text': '30 dias', 'valor.text': locale.currency(d30, grouping=True),
                           'vencimento.text': data30 or '00/00/0000'}
                calculos.append(calculo)
                calculo = {'prazo.text': '60 dias', 'valor.text': locale.currency(d60, grouping=True),
                           'vencimento.text': data60 or ' 00/00/0000'}
                calculos.append(calculo)
                calculo = {'prazo.text': '90 dias', 'valor.text': locale.currency(d90, grouping=True),
                           'vencimento.text': data90 or '00/00/0000'}
                calculos.append(calculo)
                calculo = {'prazo.text': '120 dias', 'valor.text': locale.currency(d120, grouping=True),
                           'vencimento.text': data120 or '00/00/0000'}
                calculos.append(calculo)

                msg_vazia = " "
                mensagem.append(msg_vazia)
                msg = f'Renovação para 30 dias  {locale.currency(d30, grouping=True)} - Novo Vencimento {data30}'
                mensagem.append(msg)
                mensagem.append(msg_vazia)
                msg = f'Renovação para 60 dias  {locale.currency(d60, grouping=True)} - Novo Vencimento {data60}'
                mensagem.append(msg)
                mensagem.append(msg_vazia)
                msg = f'Renovação para 90 dias  {locale.currency(d90, grouping=True)} - Novo Vencimento {data90}'
                mensagem.append(msg)
                mensagem.append(msg_vazia)
                msg = f'Renovação para 120 dias  {locale.currency(d120, grouping=True)} - Novo Vencimento {data120}'
                mensagem.append(msg)
                mensagem.append(msg_vazia)

            else:
                print('Não existem contratos cadastrados para esse cliente.')
            desconectar(conn)
            if d30 > 0:
                self.possui_margem = False
            else:
                self.possui_margem = True
            return calculos
        except Exception as e:
            logging.exception(str(e))


class RVCalculoLiquidacao(BoxLayout):

    def populate_liquidacao(self):
        try:
            self.rv_calculo_liquidacao.data = set(self.rv_calculo_liquidacao.data)
            self.rv_calculo_liquidacao.data = self.lista_calculo_liquidacao()

            # if not self.possui_margem:
            #     self.ids.calculo.text = 'Cliente não possui margem, ou não cobre todo o valor dos juros para 30 dias'
            # elif 20000 < self.total_emprestimo <= 120000:
            #     self.ids.calculo.text = 'Serão necessários 2 avaliadores para autorizar a alçada, conforme AL021'
            # elif self.total_emprestimo > 120000:
            #     self.ids.calculo.text = 'Será necessário Comitê de Crédito para autorizar a alçada, conforme AL021'
            # else:
            #     self.ids.calculo.text = ''


        except Exception as e:
            logging.exception(str(e))

    def enviar_cliente(self):
        telefones = listar_telefones_por_cpf(cpf)
        if len(telefones) > 1:
            content = RVTelefonesEnviar()
            self._popup = Popup(title="Selecione o telefone para enviar", content=content,
                                size_hint=(0.4, 0.4))
            self._popup.open()
            content.populate()
        else:
            whats.envia_msg.send_whatsapp_msg_valor(texto=mensagem, numero=telefones)



    def lista_calculo_liquidacao(self):
        """
                Função para listar os contratos do cliente
                """
        try:
            calculos = []
            global mensagem
            mensagem = []
            self.total_emprestimo = 0
            valor_total = 0
            msg_vazia = " "
            if len(lista_de_contratos) > 0:
                for contrato in lista_de_contratos:
                    # valor_avaliacao = float(contrato[2].replace(".", '').replace(",", "."))
                    valor_emprestimo = float(contrato[4].replace(".", '').replace(",", "."))

                    liquidacao, encargo = calcular_liquidacao(valor_emprestimo, datetime.datetime.strptime(contrato[5], '%d/%m/%Y'), consulta_prazo(contrato[0]))

                    calculo = {'contrato.text': contrato[0], 'valor.text': locale.currency(liquidacao, grouping=True),
                               'encargos.text': locale.currency(encargo, grouping=True) or 0}
                    calculos.append(calculo)

                    valor_total += liquidacao

                    mensagem.append(msg_vazia)
                    msg = f'Contrato: {contrato[0]}  Valor: {locale.currency(liquidacao, grouping=True)}'
                    mensagem.append(msg)
                    mensagem.append(msg_vazia)

                mensagem.append(msg_vazia)
                msg = f' Valor Total: {locale.currency(valor_total, grouping=True)}'
                mensagem.append(msg)
                mensagem.append(msg_vazia)
                self.ids.calculo_liquidacao = locale.currency(valor_total, grouping=True)
                calculo = {'contrato.text': "TOTAL", 'valor.text': locale.currency(valor_total, grouping=True),
                           'encargos.text': " " or 0}
                calculos.append(calculo)
            else:
                print('Não existem contratos cadastrados para esse cliente.')

            return calculos
        except Exception as e:
            logging.exception(str(e))


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class ProgBar(ProgressBar):
    progress_bar = ObjectProperty()

    def __init__(self, **kwa):
        super(ProgBar, self).__init__(**kwa)
        self.progress_bar = ProgressBar()



class EventLoopWorker(EventDispatcher):

    # __events__ = ('whatsapp',)  # defines this EventDispatcher's sole event

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(EventLoopWorker, cls).__new__(cls)
        return cls.instance
    def __init__(self):
        self.register_event_type("on_envio")
        super(EventLoopWorker, self).__init__()
        self._thread = threading.Thread(target=self._run_loop)  # note the Thread target here
        # self._thread_envio = threading.Thread(target=self._run_loop2)
        self._thread.daemon = True
        self.loop = None
        self.loop_envio = None
        self.cliente = None
        self.envio_task = None
        self.envio_msg = EnviaMensagem()
        self.msg = None
        self.dados = asyncio.Queue()
        self.contador = 0
        self.clientes = None
        self.falha = 0
        self.enviado_sucesso = 0

    def on_envio(self, *_):
        print("Aqui")
        pass

    def _run_loop(self, dt=None):
        self._restart_pulse()

    def start_teste_telefone(self):
        self.clientes = App.get_running_app().clientes
        self._run_loop_teste_telefone()

    @threaded
    def _run_loop_teste_telefone(self):
        self.cria_task_teste_telefone()

    def cria_task_teste_telefone(self):
        if self.envio_task is not None:
            self.envio_task.cancel()
        # self.loop.stop()
        try:
            self.loop = asyncio.get_event_loop()
        except:
            self.loop = asyncio.get_event_loop_policy().new_event_loop()

        self.envio_task = self.loop.create_task(coro=self.testa_telefone_whats())
        try:
            self.loop.run_until_complete(self.envio_task)
        except Exception as e:
            print(e)


    async def testa_telefone_whats(self):
        if self.envio_msg == None:
            self.envio_msg = EnviaMensagem()
            if not self.envio_msg.verifica_login():
                self.envio_msg.chama_driver(head=False)
        @mainthread
        def kivy_update_status(text):
            texto = App.get_running_app().root.ids.right_content
            texto.text = text
        @mainthread
        def progbar_runner():
            valor = 100/len(self.clientes)
            progbar = App.get_running_app().root.ids.progbar
            progbar.value += valor
        @mainthread
        def zera_progbar():
            progbar = App.get_running_app().root.ids.progbar
            progbar.value = 0


        for cliente in self.clientes:
            kivy_update_status(f" Testando {cliente['Nome']}, número {cliente['Telefones']}\n{self.contador + 1}/{len(self.clientes)}")
            await asyncio.sleep(1)
            sucesso = await self.envio_msg.teste(numero=cliente['Telefones'], cpf=cliente['CPF'])
            await asyncio.sleep(1)
            if sucesso == True:
                self.enviado_sucesso += 1
                self.contador += 1
            else:
                self.falha += 1
                self.contador += 1

            progbar_runner()

        zera_progbar()
        swhats = len(self.envio_msg.sem_whats)
        qtd_enviada = self.contador - swhats - self.falha
        fim = time.time()
        horas, minutos, segundos = tempo_execucao(App.get_running_app().inicio, fim)
        kivy_update_status(f'Foram enviadas {qtd_enviada}, {swhats} números não possuem whatsapp, {self.falha} números falharam no envio. \nTempo de execução {horas}:{minutos}:{segundos}')
        self.contador = 0
        self.falha = 0
        self.enviado_sucesso = 0
        deletar_lista()


    def start(self):
        try:
            self._thread.start()
        except RuntimeError:
            self._thread.join()
            self.clientes = App.get_running_app().clientes_hoje
            self._thread = threading.Thread(target=self._run_loop)
            self._thread.start()


    async def envio_whatsapp(self):
        if self.envio_msg == None:
            self.envio_msg = EnviaMensagem()
            if not self.envio_msg.verifica_login():
                self.envio_msg.chama_driver(head=False)
        @mainthread
        def kivy_update_status(text):
            texto = App.get_running_app().root.ids.right_content
            texto.text = text
        @mainthread
        def progbar_runner():
            valor = 100/len(self.clientes)
            progbar = App.get_running_app().root.ids.progbar
            progbar.value += valor
        @mainthread
        def zera_progbar():
            progbar = App.get_running_app().root.ids.progbar
            progbar.value = 0


        for cliente in self.clientes:
            kivy_update_status(f"Enviando mensagem para {cliente['Nome']}, número {cliente['Telefones']}\n{self.contador + 1}/{len(self.clientes)}")
            await asyncio.sleep(1)
            sucesso = await self.envio_msg.send_whatsapp_msg(cliente['Telefones'], self.msg, cliente['Nome'], cliente['CPF'])
            await asyncio.sleep(1)
            if sucesso == True:
                self.enviado_sucesso += 1
                self.contador += 1
            else:
                self.falha += 1
                self.contador += 1

            progbar_runner()

        zera_progbar()
        swhats = len(self.envio_msg.sem_whats)
        qtd_enviada = self.contador - swhats - self.falha
        fim = time.time()
        horas, minutos, segundos = tempo_execucao(App.get_running_app().inicio, fim)
        kivy_update_status(f'Foram enviadas {qtd_enviada}, {swhats} números não possuem whatsapp, {self.falha} números falharam no envio. \nTempo de execução {horas}:{minutos}:{segundos}')
        self.contador = 0
        self.falha = 0
        self.enviado_sucesso = 0
        deletar_lista()



    def _restart_pulse(self, dt=None):
        """Helper to start/reset the pulse task when the pulse changes."""
        if self.envio_task is not None:
            self.envio_task.cancel()
        # self.loop.stop()
        try:
            self.loop = asyncio.get_event_loop()
        except:
            self.loop = asyncio.get_event_loop_policy().new_event_loop()

        self.envio_task = self.loop.create_task(coro=self.envio_whatsapp())
        try:
            self.loop.run_until_complete(self.envio_task)
        except Exception as e:
            print(e)
        # self.loop.run_forever()
        # await self.envio_task




    def parar(self):
        # if self.loop is not None:
        texto = App.get_running_app().root.ids.right_content
        progbar = App.get_running_app().root.ids.progbar
        progbar.value = 0
        self.envio_task.cancel()

            # self._thread.join()


## Teste de numeros marcados como Sem Whatsapp
    def start_testa_sem_whats(self):
        self.clientes = App.get_running_app().lista_sem_whats
        self._run_loop_teste_telefone()

    @threaded
    def _run_loop_teste_telefone(self):
        self.cria_task_teste_sem_whats()

    def cria_task_teste_sem_whats(self):
        if self.envio_task is not None:
            self.envio_task.cancel()
        # self.loop.stop()
        try:
            self.loop = asyncio.get_event_loop()
        except:
            self.loop = asyncio.get_event_loop_policy().new_event_loop()

        self.envio_task = self.loop.create_task(coro=self.testa_sem_whats())
        try:
            self.loop.run_until_complete(self.envio_task)
        except Exception as e:
            print(e)


    async def testa_sem_whats(self):
        if self.envio_msg == None:
            self.envio_msg = EnviaMensagem()
            if not self.envio_msg.verifica_login():
                self.envio_msg.chama_driver(head=False)
        @mainthread
        def kivy_update_status(text):
            texto = App.get_running_app().root.ids.right_content
            texto.text = text
        @mainthread
        def progbar_runner():
            valor = 100/len(self.clientes)
            progbar = App.get_running_app().root.ids.progbar
            progbar.value += valor
        @mainthread
        def zera_progbar():
            progbar = App.get_running_app().root.ids.progbar
            progbar.value = 0


        for numero in self.clientes:
            kivy_update_status(f" Testando {numero}\n{self.contador + 1}/{len(self.clientes)}")
            await asyncio.sleep(1)
            sucesso = await self.envio_msg.testa(numero)
            await asyncio.sleep(1)
            if sucesso == True:
                self.enviado_sucesso += 1
                self.contador += 1
            else:
                self.falha += 1
                self.contador += 1

            progbar_runner()

        zera_progbar()
        swhats = len(self.envio_msg.sem_whats)
        qtd_enviada = self.contador - swhats - self.falha
        fim = time.time()
        horas, minutos, segundos = tempo_execucao(App.get_running_app().inicio, fim)
        kivy_update_status(f'Foram enviadas {qtd_enviada}, {swhats} números não possuem whatsapp, {self.falha} números falharam no envio. \nTempo de execução {horas}:{minutos}:{segundos}')
        self.contador = 0
        self.falha = 0
        self.enviado_sucesso = 0
        deletar_lista()



class Whats(App, ProgBar):
    # All Labels use these properties, set to Label defaults
    valign = StringProperty('center')
    halign = StringProperty('left')
    headless = BooleanProperty(False)
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Whats, self).__init__(**kwargs)
        # self.worker.envio_msg = EnviaMensagem()
        self.worker = EventLoopWorker()
        self.worker.envio_msg = EnviaMensagem()
        # self.texto = self.root.ids.right_content.text

    def on_start(self):
        try:
            mkdir(path.join(path.expanduser('~'), 'whatsrelatorios'))
        except Exception as e:
            logging.exception(str(e))

    def build(self):
        self.evento1 = None
        self.evento2 = None
        self.evento3 = None
        self.evento4 = True
        return Builder.load_string(_kv_code)

    def importa_formata(self, arquivo):
        self.clientes = leia_arquivo(arquivo)
        global clientes_importados
        clientes_importados = self.clientes

    def chama(self):
        try:
            self.worker.envio_msg.fecha_driver()
        except Exception as e:
            logging.exception(str(e))
            pass
        try:
            if self.worker is None:
                self.worker = EventLoopWorker()
            self.worker.envio_msg.chama_driver(self.headless)
            # self.worker.envio_msg.chama_driver(self.headless)
            # if self.worker.envio_msg.verifica_login():
            #     self.root.ids.right_content.text = "Logado"
            # else:
            #     self.root.ids.right_content.text = 'Escaneie o código QR'
            #     if self.headless:
            #         Clock.schedule_once(self.code, 0.5)
        except Exception as erro_chama:
            logging.exception(str(erro_chama))
            self.root.ids.right_content.text = str(erro_chama)

    def next(self, dt):
        if self.root.ids.progbar.value >= 100:
            return False

    def puopen(self):
        Clock.schedule_interval(self.next, 1 / 25)

    def set_atalho(self):
        self.msgs = self.root.ids.left_content.text
        self.worker.msg = self.msgs.split('\n')
        self.root.ids.right_content.text = 'Mensagem definida!'

    def limpar(self):
        self.root.ids.left_content.text = ""

    def selecionar(self):
        texto = self.root.ids.left_content
        texto.select_all()

    def spinner_headless(self, comando):
        if comando == 'Ativar':
            self.headless = True
            self.root.ids.right_content.text = "Modo headless ativado!\n\nNesta opção o navegador fica oculto"
        elif comando == 'Desativar':
            self.headless = False
            self.root.ids.right_content.text = "Modo Headless desativado!\n\nNesta opção o navegador é mostrado"
        else:
            pass

    def spinner_mensagem(self, comando):
        # self.root.ids.left_content.text = ''
        if comando == 'Vencimento':
            self.nome_arquivo = 'vencimento'
            try:
                self.mensagem = leia_texto('vencimento')
                self.root.ids.left_content.text = self.mensagem
            except Exception as e:
                logging.exception(str(e))
                # self.mensagem = None
                self.root.ids.right_content.text = "Salve uma mensagem, você pode salvar até 5 mensagens padrão"
        elif comando == 'Margem':
            self.nome_arquivo = 'margem'
            try:
                self.mensagem = leia_texto('margem')
                self.root.ids.left_content.text = self.mensagem

            except Exception as e:
                logging.exception(str(e))
                # self.mensagem = None
                self.root.ids.right_content.text = "Salve uma mensagem, você pode salvar até 5 mensagens padrão"
        elif comando == 'Vencidos':
            self.nome_arquivo = 'vencidos'
            try:
                self.mensagem = leia_texto('vencidos')
                self.root.ids.left_content.text = self.mensagem
            except Exception as e:
                logging.exception(str(e))
                # self.mensagem = None
                self.root.ids.right_content.text = "Salve uma mensagem, você pode salvar até 5 mensagens padrão"
        elif comando == 'Leilao':
            self.nome_arquivo = 'Leilao'
            try:
                self.mensagem = leia_texto('Leilao')
                self.root.ids.left_content.text = self.mensagem

            except Exception as e:
                logging.exception(str(e))
                # self.mensagem = None
                self.root.ids.right_content.text = "Salve uma mensagem, você pode salvar até 5 mensagens padrão"
        elif comando == 'msg2':
            self.nome_arquivo = 'msg2'
            try:
                self.mensagem = leia_texto('msg2')
                self.root.ids.left_content.text = self.mensagem
            except Exception as e:
                logging.exception(str(e))

                # self.mensagem = None
                self.root.ids.right_content.text = "Salve uma mensagem, você pode salvar até 5 mensagens padrão"
        else:
            pass

    def salva_mensagem(self):
        self.msgs = self.root.ids.left_content.text
        texto = self.msgs.split('\n')
        try:
            salva_texto(texto, self.nome_arquivo)
            self.root.ids.right_content.text = "Mensagem salva com sucesso"
        except Exception as e:
            logging.exception(str(e))

            self.root.ids.right_content.text = 'Selecione uma opção em *Mensagem* antes de salvar, esta mensagem será salva para utlização futura'

    def clientes_com_whats_vcard(self):
        try:
            csv_para_vcf()
            self.root.ids.right_content.text = "Criado arquivo vCARD (contatos.vcf) com os clientes importados que possuem whats, na última abertura de arquivo csv , transfira o arquivo contatos.vfc para celular e importe o arquivo nas configurações de contato"
        except Exception as e:
            self.root.ids.right_content.text = "Não existe arquivo de clientes ainda, importe a base de dados primeiro."


    def cria_iter(self, clientes, dt=None):
        """Cria um iterável a partir da lista de clientes, e inicializa as váriaveis entes do envio da mensagens"""
        if not self.worker.msg:
            self.set_atalho()
            self.root.ids.right_content.text = "Salve uma mensagem, você pode salvar até 5 mensagens padrão antes de enviar"
            return

        try:
            self.worker.clientes = clientes
        except Exception as e:
            logging.exception(str(e))
            self.root.ids.right_content.text = "Escolha um arquivo com base de clientes"
            return
        if self.worker.envio_msg.driver == None:
            self.worker.envio_msg.chama_driver(False)

        self.evento4 = True
        self.puopen()
        self.progress_bar.value = 0
        self.value = 100 / len(clientes)
        self.contador = 0
        self.inicio = time.time()
        self.qtd = len(clientes)
        self.worker.envio_msg.sem_whats = []
        try:
            self.worker.start()
        except AssertionError as e:
            self.root.ids.right_content.text = "Processo iniciado aguarde"



    def cria_iter_sem(self):
        """Cria um iterável com a lista de telefones sem whatsapp a partir do arquivo sem_whats.csv e inicializa as váriavel"""
        self.evento4 = True
        try:
            self.lista_sem_whats = lista_telefones(0)
        except Exception as e:
            logging.exception(str(e))
            self.root.ids.right_content.text = 'Ainda não existe lista de telefones sem Whatsapp'
            return
        if self.worker.envio_msg.driver == None:
            self.root.ids.right_content.text = 'Escaneie o código QR e clique Testar sem whats novamente'
            self.worker.envio_msg.chama_driver(False)
            return
        self.inicio = time.time()
        self.qtd_inicial = len(self.lista_sem_whats)
        self.puopen()
        self.progress_bar.value = 0
        self.value = 100 / self.qtd_inicial
        self.contador = 0
        self.lista = str(self.lista_sem_whats).split(",")
        # self.root.ids.right_content.text = str(self.lista)
        self.worker.start_testa_sem_whats()

    # def testa_sem(self, dt=None):
    #     """Testa os número sem whatsapp"""
    #     if len(self.lista_sem_whats) == 0:
    #         self.root.ids.right_content.text = "Ainda não existe arquivo com a lista de telefones sem whatsapp"
    #     else:
    #         try:
    #             self.numero = next(self.it)
    #         except StopIteration:
    #             fim = time.time()
    #             horas, minutos, segundos = tempo_execucao(self.inicio, fim)
    #             self.root.ids.right_content.text = f'Foram testados {self.contador} números {self.worker.envio_msg.excluidos} excluídos da lista  em {horas}:{minutos}:{segundos}'
    #             self.root.ids.progbar.value = 0
    #
    #             return
    #         if self.qtd_inicial > 0:
    #             try:
    #                 # id_sem = pesquisa_id_por_telefone(self.numero)
    #                 self.tem_whats = self.worker.envio_msg.testa(numero=self.numero)
    #                 self.contador += 1
    #                 self.root.ids.progbar.value += self.value
    #                 if self.tem_whats:
    #                     self.root.ids.right_content.text = f"{self.numero} não tem whatsapp\n{self.contador}/{self.qtd_inicial}"
    #                 else:
    #                     self.root.ids.right_content.text = f"{self.numero} tem whatsapp\n{self.contador}/{self.qtd_inicial}"
    #
    #             except Exception as erro_teste:
    #                 self.root.ids.right_content.text = str(erro_teste)
    #                 self.worker.envio_msg.is_connected()
    #         if self.evento4 == False:
    #             self.evento2.cancel()
    #             self.evento2 = None
    #             self.root.ids.right_content.text = "Teste parado"
    #             self.root.ids.progbar.value = 0
    #
    #             return
    #         else:
    #             self.evento2 = Clock.schedule_once(self.testa_sem, 0.5)

    def cria_iter_importados(self):
        """Cria um iterável a partir da lista de clientes importados e inicializa as variáveis para teste dos telefones importados"""
        if self.evento3 is not None:
            self.evento3.cancel()
            self.evento3 = None

        try:
            self.clientes = listar_clientes_telefone()
            # self.qtd_teste = len(self.clientes)
            # self.it_importados = iter(self.clientes)
        except Exception as e:
            logging.exception(str(e))
            self.root.ids.right_content.text = "Importe um arquivo csv do APP Bezel com os clientes para testar se os telefones tem Whatsapp antes!"
            return
        if self.worker.envio_msg.driver == None:
            # self.root.ids.right_content.text = 'Escaneie o código QR e clique Testar Base de Dados novamente'
            self.worker.envio_msg.chama_driver()
            return
        self.evento4 = True
        self.puopen()
        self.progress_bar.value = 0
        self.value = 100 / len(self.clientes)
        self.inicio = time.time()
        self.contador = 0

        self.worker.start_teste_telefone()

    def somente_teste(self, dt=None):
        """Faz o teste dos telefones importados verificando se o número possui whatsapp pelo campo de envia mensagem, caso o número não possua whatsapp é apresentado
        mensagem de número inválido"""
        try:
            self.cliente = next(self.it_importados)
        except StopIteration:
            fim = time.time()
            horas, minutos, segundos = tempo_execucao(self.inicio, fim)
            self.worker.envio_msg.sem_whats = []
            self.root.ids.right_content.text = f'Foram identificados {len(self.worker.envio_msg.sem_whats)} números sem whats, foram testados {self.contador} números, em {horas}:{minutos}:{segundos}'
            self.root.ids.progbar.value = 0

            return
        try:
            self.worker.envio_msg.teste(self.cliente['Telefones'], self.cliente['CPF'])
            self.contador += 1
            self.root.ids.progbar.value += self.value
            self.root.ids.right_content.text = f"Testando telefone {self.cliente['Telefones']} do cliente {self.cliente['Nome']}\n AGUARDE!!!\n{self.contador} / {len(self.clientes)}"
        except Exception as e:
            logging.exception(str(e))
            self.worker.envio_msg.is_connected()

        if self.evento4 is False:
            self.evento3.cancel()
            self.evento3 = None
            self.root.ids.right_content.text = "Teste parado "
            self.root.ids.progbar.value = 0
            return
        else:
            pass
            self.evento3 = Clock.schedule_once(self.somente_teste, 0.5)



    def enviar_vencimento(self):
        try:
            self.cria_iter(self.clientes_hoje)
        except Exception as e:
            logging.exception(str(e))
            self.root.ids.right_content.text = "Selecione um arquivo do APP Bezel antes de tentar enviar, esta opção " \
                                               "filtra os clientes com contratos vencendo no dia, para funcionar é " \
                                               "necessária a importação de um relatório com todos os clientes, " \
                                               "de preferência atualizado.\nNo app Bezel, na aba Gerenciar Contratos " \
                                               "> Criar CSV "

    @threaded
    def filtra_hoje(self):
        try:
            self.clientes_hoje = None
            self.clientes_hoje = filtra_vencimento()
            global clientes_importados
            clientes_importados = None
            clientes_importados = self.clientes_hoje
            self.root.ids.right_content.text = f"{len(self.clientes_hoje)} Números de telefones para envio"
        except Exception as e:
            logging.exception(str(e))
            self.root.ids.right_content.text = "Base de dados ainda não existe, importe um arquivo da bezel primeiro, relatório de margem da bezel não cria banco de dados"


    @threaded
    def criar_lista(self):
        try:
            try:
                self.clientes_hoje = None
                self.clientes_hoje = criar_lista_envio()
            except Exception as e:
                logging.exception(str(e))
                self.root.ids.right_content.text = ''
                return
            self.root.ids.right_content.text = f'Lista criada'

        except Exception as e:
            logging.exception(str(e))
            self.root.ids.right_content.text = "Banco de dados ainda não existe, importe um arquivo primeiro"

    @threaded
    def filtra_margem(self):
        try:
            try:
               deletar_lista()
            except Exception as e:
                logging.exception(str(e))
                self.root.ids.right_content.text = e
                return
            self.root.ids.right_content.text = f'Lista de Envio apagada'

        except Exception as e:
            logging.exception(str(e))
            self.root.ids.right_content.text = e

    def filtra_licitacao(self):
        try:
            try:
                self.clientes_hoje = None
                self.clientes_hoje = listar_contratos_licitacao(self.root.ids.conteudo_licitacao.text)
            except Exception as e:
                logging.exception(str(e))
                self.root.ids.right_content.text = 'Data em Formato desconhecido, digite uma data no formato dd/mm/aaaa'
                return
            global clientes_importados
            clientes_importados = None
            clientes_importados = self.clientes_hoje
            # self.imprime_importados()
            self.root.ids.right_content.text = f'{len(self.clientes_hoje)} clientes com contratos vencidos\nClique em exibir para mostrar os clientes\n\nEsta opção filtra todos contratos vencidos da base de dados importada, importante atualizar a base de dados pelo menos uma vez por semana importando um relatório com todos os contratos do aplicativo bezel'
        except Exception as e:
            logging.exception(str(e))
            self.root.ids.right_content.text = "Banco de dados ainda não existe, importe um arquivo primeiro"

    def filtra_data(self):
        try:
            try:
                self.clientes_hoje = None
                self.clientes_hoje = filtra_data(self.root.ids.middle_content.text)
                global clientes_importados
                clientes_importados = self.clientes_hoje
                # self.imprime_importados()
            except Exception as e:
                logging.exception(str(e))
                self.root.ids.right_content.text = 'Nada encontrado'
                return
            self.root.ids.right_content.text = f'{len(self.clientes_hoje)} clientes com nome/data  {self.root.ids.middle_content.text}\nEsta opção filtra contratos com vencimento no dia digitado, use o formato DD/MM/AAAA, ou pelo NOME do cliente\nPode clicar enter com o campo de pesquisa em branco para mostrar todos os clientes.\n\nCliente em exibir para mostrar os clientes'

        except Exception as e:
            logging.exception(str(e))
            self.root.ids.right_content.text = "Base de dados ainda não existe, importe uma base de dados primeiro"

    def parar(self):
        self.worker.parar()
        self.root.ids.right_content.text = "Envio Cancelado"
        self.worker = None
        self.worker = EventLoopWorker()

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        try:
            arquivo = os.path.join(path, filename[0])
            if arquivo:
                self.importa_formata(arquivo)
                if self.clientes:
                    self.root.ids.right_content.text = f'Foram importados {len(self.clientes)} clientes.\nArquivos criados na pasta c:/User/usuario/whatsrelatorios'
                else:
                    self.root.ids.right_content.text = f'Contratos atualizados com sucesso'

            self.dismiss_popup()
        except Exception as e:
            logging.exception(str(e))
            return

    def on_stop(self):
        self.worker.envio_msg.fecha_driver()


    def exibir(self):
        content = RV()
        self._popup = Popup(title="Clientes", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
        content.populate()

    def exibir_contratos(self):
        content = RV()
        self._popup = Popup(title="Contratos", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
        content.populate_contratos()


if __name__ == '__main__':
    whats = Whats()
    whats.run()