import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.clipboard import Clipboard
from kivy.utils import get_color_from_hex
from PIL import Image, ImageDraw, ImageFont  # Biblioteca de desenho

class InterApp(App):
    def build(self):
        self.main_layout = BoxLayout(orientation='vertical', padding=30, spacing=15)

        self.main_layout.add_widget(Label(text="GERADOR DE COMPROVANTE VISUAL", font_size='20sp', bold=True, size_hint_y=None, height=50))

        # Campos de Entrada
        self.main_layout.add_widget(Label(text="Chave PIX:", size_hint_y=None, height=30))
        self.chave_input = TextInput(multiline=False, hint_text="Ex: 123456789", size_hint_y=None, height=45)
        self.main_layout.add_widget(self.chave_input)

        self.main_layout.add_widget(Label(text="Valor (R$):", size_hint_y=None, height=30))
        self.valor_input = TextInput(multiline=False, hint_text="Ex: 150.00", size_hint_y=None, height=45)
        self.main_layout.add_widget(self.valor_input)

        self.main_layout.add_widget(Label(text="Descrição:", size_hint_y=None, height=30))
        self.desc_input = TextInput(multiline=False, hint_text="Ex: Pagamento", size_hint_y=None, height=45)
        self.main_layout.add_widget(self.desc_input)

        # Botões
        self.btn_copiar = Button(text="COPIAR DADOS", background_color=get_color_from_hex('#2ecc71'), size_hint_y=None, height=50)
        self.btn_copiar.bind(on_press=self.acao_copiar)
        self.main_layout.add_widget(self.btn_copiar)

        self.btn_comprovante = Button(text="GERAR IMAGEM (COMPROVANTE)", background_color=get_color_from_hex('#e74c3c'), size_hint_y=None, height=50)
        self.btn_comprovante.bind(on_press=self.acao_comprovante)
        self.main_layout.add_widget(self.btn_comprovante)

        self.status_label = Label(text="Status: Pronto", size_hint_y=None, height=40)
        self.main_layout.add_widget(self.status_label)

        return self.main_layout

    def acao_copiar(self, instance):
        dados = f"PIX: {self.chave_input.text} | Valor: {self.valor_input.text}"
        Clipboard.copy(dados)
        self.status_label.text = "Status: Copiado!"
        self.status_label.color = get_color_from_hex('#2ecc71')

    def acao_comprovante(self, instance):
        chave = self.chave_input.text
        valor = self.valor_input.text
        desc = self.desc_input.text

        if not chave or not valor:
            self.status_label.text = "Status: Preencha os dados!"
            return

        try:
            # --- LÓGICA DE CRIAÇÃO DA IMAGEM (SIMULANDO INTERFACE) ---
            # 1. Criar um fundo (Canvas)
            largura, altura = 800, 1000
            img = Image.new('RGB', (largura, altura), color=(255, 255, 255)) # Fundo Branco
            draw = ImageDraw.Draw(img)

            # 2. Desenhar um cabeçalho (Simulando cor do app)
            draw.rectangle([0, 0, largura, 200], fill=(0, 160, 180)) # Azul Inter
            
            # 3. Escrever Textos (Simulação de layout)
            # Nota: Em dispositivos reais, precisamos carregar uma fonte .ttf
            # Para este exemplo, usaremos a fonte padrão do sistema
            try:
                font_titulo = ImageFont.load_default()
                font_texto = ImageFont.load_default()
            except:
                font_titulo = font_texto = ImageFont.load_default()

            # Escrevendo no Comprovante
            draw.text((50, 50), "COMPROVANTE DE TRANSAÇÃO", fill=(255, 255, 255), font=font_titulo)
            draw.text((50, 250), f"STATUS: REALIZADA", fill=(0, 150, 0), font=font_texto)
            draw.text((50, 350), f"DATA: {time.strftime('%d/%m/%Y %H:%M')}", fill=(50, 50, 50), font=font_texto)
            draw.text((50, 450), f"VALOR: R$ {valor}", fill=(0, 0, 0), font=font_texto)
            draw.text((50, 550), f"CHAVE: {chave}", fill=(50, 50, 50), font=font_texto)
            draw.text((50, 650), f"DESCRIÇÃO: {desc}", fill=(50, 50, 50), font=font_texto)
            
            # Rodapé decorativo
            draw.rectangle([0, 900, largura, altura], fill=(230, 230, 230))
            draw.text((50, 920), "Transação Gerada via Sistema de Automação", fill=(100, 100, 100), font=font_texto)

            # 4. Salvar a imagem
            nome_arquivo = f"comprovante_img_{int(time.time())}.png"
            img.save(nome_arquivo)

            self.status_label.text = f"Status: Imagem salva: {nome_arquivo}"
            self.status_label.color = get_color_from_hex('#f1c40f')

        except Exception as e:
            self.status_label.text = f"Erro: {str(e)}"
            self.status_label.color = get_color_from_hex('#e74c3c')

if __name__ == '__main__':
    InterApp().run()
