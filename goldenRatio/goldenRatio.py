from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex as gc
from kivy.metrics import dp, sp


class GoldenRatioScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(GoldenRatio())


class TxtInput(TextInput):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input_filter = "float"
        self.background_color = gc("222222")
        self.foreground_color = gc("FFFFFF")
        self.font_size = sp(40)
        self.multiline = False
        self.size_hint = (1, None)
        self.height = sp(40)*2


class Lbel(Image):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = gc("333333")
        self.height = sp(32)*2
        self.display_label()
        self.bind(pos=self.change_ps, size=self.change_ps)
        self.y = dp(100)

    def change_ps(self, *_):
        if hasattr(self, "label"):
            self.label.pos = self.pos
            self.label.size = self.size

    def display_label(self):
        self.label = Label()
        self.label.text = "0"
        self.label.color = gc("FFD700")
        self.label.font_size = sp(32)
        self.add_widget(self.label)


class GoldenRatio(Image):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.phi = 1.618033988749895
        self.size = Window.size
        self.source = "assets/GoldenRatio.png"
        self.keep_ratio = False
        self.allow_stretch = True
        self.display_title()
        self.display_field()

    def display_title(self):
        self.label_background = Image(
            pos=(0, Window.height-dp(50)),
            size=(Window.width, dp(50)),
            color=gc("111111")
        )
        self.label = Label(
            pos=(0, Window.height-dp(50)),
            size=(Window.width, dp(50)),
            font_size=sp(32),
            text="Golden Ratio"
        )
        self.add_widget(self.label_background)
        self.add_widget(self.label)

    def display_field(self):
        self.grid = GridLayout(
            padding=dp(20),
            spacing=dp(20),
            size=(Window.width*0.8, Window.height-dp(50+60+100)),
            pos=(Window.width*0.1, dp(100)),
            cols=1,
            rows=3
        )
        self.generate_button = Button(
            text="Generate Missing Slot",
            font_size=sp(32),
            background_color=gc("222222"),
            size=(Window.width*0.8-dp(40), dp(76)),
            pos=(Window.width*0.1+dp(20), dp(12))
        )
        self.method1 = Lbel(
            width=((Window.width*0.8-dp(20))-dp(40))/2,
            x=dp(Window.width*0.1+dp(20))
        )
        self.method1.label.text = "Method 1"
        self.method2 = Lbel(
            width=((Window.width*0.8-dp(20))-dp(40))/2,
            x=self.method1.right + dp(20)
        )
        self.method2.label.text = "Method 2"
        self.generate_button.bind(on_release=self.calculate_golden_ratio)
        self.A_input = TxtInput()
        self.B_input = TxtInput()
        self.S_input = TxtInput()
        for i in "ABS":
            getattr(self, f"{i}_input").hint_text = f"{i} Slot"
            self.grid.add_widget(getattr(self, f"{i}_input"))
        self.add_widget(self.grid)
        self.add_widget(self.method1)
        self.add_widget(self.method2)
        self.add_widget(self.generate_button)

    def check_if_golden_ratio(self, A, B, S):
        self.label.color = gc("FFD700") if (round((S / A), 3) == round(self.phi, 3) and
                                            round((A / B), 3) == round(self.phi, 3)) else gc("FFFFFF")
        self.method1.label.text = str(round((S / A), 3))
        self.method2.label.text = str(round((A / B), 3))

    def calculate_golden_ratio(self, *_):
        AS = self.A_input.text
        BS = self.B_input.text
        SS = self.S_input.text
        if (AS == "" and BS == "" and SS == ""):
            self.A_input.text = "1"
            self.B_input.text = str(1/self.phi)
            self.S_input.text = str(self.phi)
            self.check_if_golden_ratio(
                float(self.A_input.text),
                float(self.B_input.text),
                float(self.S_input.text)
            )
            return
        if AS != "":
            AS = float(AS)
        if BS != "":
            BS = float(BS)
            if AS == "":
                AS = self.phi * BS
        if SS != "":
            SS = float(SS)
            if AS == "":
                AS = SS / self.phi
            if BS == "":
                BS = AS / self.phi
        if AS != "":
            if BS == "":
                BS = AS / self.phi
            if SS == "":
                SS = AS + BS
        if BS != "":
            if SS == "":
                SS = AS + BS
        self.A_input.text = str(AS)
        self.B_input.text = str(BS)
        self.S_input.text = str(SS)
        self.check_if_golden_ratio(AS, BS, SS)
