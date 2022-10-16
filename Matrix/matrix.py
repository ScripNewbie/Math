from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.utils import get_color_from_hex as gc, platform
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.metrics import dp, sp
from kivy.uix.screenmanager import Screen


class MatrixScreen(Screen):

    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(Matrix())


class TxtInput(TextInput):

    def __init__(self, fsize=20, **kwargs):
        super().__init__(**kwargs)
        self.input_filter = "int"
        self.text = "0"
        self.hint_text = "0"
        self.background_color = gc("222222")
        self.foreground_color = gc("FFFFFF")
        self.font_size = sp(fsize)
        self.multiline = False


class Matrix(Image):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = Window.size
        self.source = "assets/MathBG.png"
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
            text="Matrix"
        )
        self.add_widget(self.label_background)
        self.add_widget(self.label)

    def on_touch_down(self, touch):
        if self.label.collide_point(*touch.pos):
            self.parent.manager.transition.direction = "right"
            self.parent.manager.current = "field"
        return super().on_touch_down(touch)

    def display_field(self):
        self.rows = self.cols = 5
        self.first_matrix = list()
        self.second_matrix = list()
        self.grid = GridLayout(
            size=(Window.width*0.8, Window.height*0.6),
            pos=(Window.width*0.1, Window.height*0.2),
            padding=dp(5),
            spacing=dp(5),
            rows=self.rows,
            cols=self.cols
        )

        for i in range(self.cols * self.rows):
            self.grid.add_widget(TxtInput(100/self.rows))

        self.add_widget(self.grid)
