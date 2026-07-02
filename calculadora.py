from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout

class Calculadora(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        naranja = (1, 0.45, 0, 1)
        gris_oscuro = (0.15, 0.15, 0.15, 1)

        self.historial = []

        fondo = MDBoxLayout(
            orientation="vertical",
            md_bg_color=gris_oscuro,
        )

        toolbar = MDTopAppBar(
            title="Calculadora",
            anchor_title="center",
            md_bg_color=naranja
        )

        self.pantalla = MDLabel(
            text="0",
            halign="right",
            font_style="H4",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
            height="80dp"
        )

        botones = GridLayout(
            cols=4,
            spacing=5,
            padding=10,
            size_hint_y=None,
            height="320dp"
        )

        textos = [
            "C", "±", "%", "÷",
            "7", "8", "9", "×",
            "4", "5", "6", "-",
            "1", "2", "3", "+",
            "H", "0", ".", "=",
        ]

        for texto in textos:
            if texto in ["÷", "×", "-", "+", "="]:
                color = naranja
            elif texto in ["C", "±", "%", "H"]:
                color = (0.5, 0.5, 0.5, 1)
            else:
                color = (0.3, 0.3, 0.3, 1)

            btn = MDRaisedButton(
                text=texto,
                md_bg_color=color,
                size_hint=(1, None),
                height="70dp"
            )
            btn.bind(on_press=self.presionar)
            botones.add_widget(btn)

        fondo.add_widget(toolbar)
        fondo.add_widget(self.pantalla)
        fondo.add_widget(botones)
        self.add_widget(fondo)

    def presionar(self, btn):
        texto = btn.text

        if texto == "C":
            self.pantalla.text = "0"

        elif texto == "H":
            self.manager.current = "historial"

        elif texto == "=":
            try:
                expresion = self.pantalla.text
                expresion = expresion.replace("÷", "/").replace("×", "*")
                resultado = str(eval(expresion))
                self.historial.append(self.pantalla.text + " = " + resultado)
                self.pantalla.text = resultado
            except:
                self.pantalla.text = "Error"

        elif texto == "±":
            try:
                valor = float(self.pantalla.text)
                self.pantalla.text = str(-valor)
            except:
                pass

        elif texto == "%":
            try:
                valor = float(self.pantalla.text)
                self.pantalla.text = str(valor / 100)
            except:
                pass

        else:
            if self.pantalla.text == "0":
                self.pantalla.text = texto
            else:
                self.pantalla.text += texto


class Historial(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        naranja = (1, 0.45, 0, 1)
        gris_oscuro = (0.15, 0.15, 0.15, 1)

        fondo = MDBoxLayout(
            orientation="vertical",
            md_bg_color=gris_oscuro,
        )

        toolbar = MDTopAppBar(
            title="Historial",
            anchor_title="center",
            md_bg_color=naranja
        )

        self.lista = StackLayout(
            size_hint=(1, None),
            spacing=5,
            padding=10
        )
        self.lista.bind(minimum_height=self.lista.setter("height"))

        scroll = ScrollView()
        scroll.add_widget(self.lista)

        boton_volver = MDRaisedButton(
            text="VOLVER",
            pos_hint={"center_x": 0.5},
            md_bg_color=naranja,
            size_hint_y=None,
            height="50dp",
            on_press=self.volver
        )

        fondo.add_widget(toolbar)
        fondo.add_widget(scroll)
        fondo.add_widget(boton_volver)
        self.add_widget(fondo)

    def on_enter(self):
        self.lista.clear_widgets()
        calc = self.manager.get_screen("calculadora")
        for operacion in calc.historial:
            self.lista.add_widget(MDLabel(
                text=operacion,
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                size_hint=(1, None),
                height="40dp"
            ))

    def volver(self, obj):
        self.manager.current = "calculadora"


class MiApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        sm = ScreenManager()
        sm.add_widget(Calculadora(name="calculadora"))
        sm.add_widget(Historial(name="historial"))
        return sm

if __name__ == "__main__":
    MiApp().run()